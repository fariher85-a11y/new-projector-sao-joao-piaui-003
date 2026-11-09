/* Upload de documentos (frente/verso) — robusto.
 *
 * Problema que este arquivo resolve:
 * a conversão do arquivo para base64 podia travar para sempre (quando os
 * eventos de carregamento da imagem nunca disparavam), o envio nunca saía e
 * o candidato era levado para a página seguinte mesmo assim — perdendo o
 * documento silenciosamente.
 *
 * Garantias:
 *  - a conversão SEMPRE termina (timeout em cada etapa, com fallback);
 *  - o que foi convertido fica guardado como "pendente" e é reenviado
 *    automaticamente nas páginas seguintes até o servidor confirmar;
 *  - quem chama sabe se o envio foi confirmado ou não.
 */
(function () {
  var KEY = 'pending_docs_upload';

  function post(path, body) {
    return fetch(window.location.origin + path, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {})
    });
  }

  // Converte um arquivo em data URL. Nunca fica pendurado: sempre resolve.
  function toDataUrl(f, timeoutMs) {
    return new Promise(function (res) {
      if (!f) { res(''); return; }
      var done = false;
      function finish(v) { if (done) return; done = true; res(String(v || '')); }

      var guard = setTimeout(function () { finish(''); }, timeoutMs || 30000);
      var r = new FileReader();
      r.onerror = function () { clearTimeout(guard); finish(''); };
      r.onabort = function () { clearTimeout(guard); finish(''); };
      r.onload = function () {
        var raw = String(r.result || '');
        var isImg = /^image\//.test(f.type || '');
        // PDF (ou qualquer formato não-imagem): envia exatamente como veio.
        if (!isImg || !raw) { clearTimeout(guard); finish(raw); return; }

        // Imagem: tenta comprimir. Se a imagem não carregar, usa o original.
        var img = new Image();
        var imgGuard = setTimeout(function () { clearTimeout(guard); finish(raw); }, 10000);
        img.onload = function () {
          clearTimeout(imgGuard); clearTimeout(guard);
          try {
            var MAX = 1600, w = img.width, h = img.height;
            if (!w || !h) { finish(raw); return; }
            if (w > MAX || h > MAX) {
              if (w >= h) { h = Math.round(h * MAX / w); w = MAX; }
              else { w = Math.round(w * MAX / h); h = MAX; }
            }
            var c = document.createElement('canvas');
            c.width = w; c.height = h;
            c.getContext('2d').drawImage(img, 0, 0, w, h);
            var out = String(c.toDataURL('image/jpeg', 0.8) || '');
            finish(out.length > 64 ? out : raw);
          } catch (e) { finish(raw); }
        };
        img.onerror = function () { clearTimeout(imgGuard); clearTimeout(guard); finish(raw); };
        img.src = raw;
      };
      try { r.readAsDataURL(f); } catch (e) { clearTimeout(guard); finish(''); }
    });
  }

  function savePending(p) { try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {} }
  function readPending() { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; } }
  function clearPending() { try { localStorage.removeItem(KEY); } catch (e) {} }

  function send(p) {
    if (!p || !p.cpf || (!p.doc_frente && !p.doc_verso)) return Promise.resolve(false);
    return post('/api/track/documents', p).then(function (r) {
      if (!r || !r.ok) return false;
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (j && j.ok === false) return false;
        clearPending();
        return true;
      });
    }).catch(function () { return false; });
  }

  /* Converte e envia os documentos.
   * Resolve com { enviado: bool, vazio: bool } — nunca rejeita. */
  window.__docsUpload = function (fileFrente, fileVerso, cpf, docTipo) {
    return Promise.all([toDataUrl(fileFrente), toDataUrl(fileVerso)]).then(function (b) {
      var payload = {
        cpf: cpf || '',
        doc_tipo: docTipo || 'RG',
        doc_frente: b[0] || '',
        doc_verso: b[1] || ''
      };
      if (!payload.doc_frente && !payload.doc_verso) {
        return { enviado: false, vazio: true };
      }
      // Guarda antes de enviar: se a rede falhar, as próximas páginas reenviam.
      savePending(payload);
      return send(payload).then(function (ok) { return { enviado: ok, vazio: false }; });
    });
  };

  /* Reenvia um upload pendente. Usado pelas páginas seguintes do fluxo. */
  window.__docsFlushPending = function () {
    var p = readPending();
    if (!p) return Promise.resolve(false);
    return send(p);
  };

  // Tenta reenviar assim que qualquer página que inclua este script abrir.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { window.__docsFlushPending(); });
  } else {
    window.__docsFlushPending();
  }
})();
