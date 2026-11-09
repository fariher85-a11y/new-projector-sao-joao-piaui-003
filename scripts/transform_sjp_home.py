#!/usr/bin/env python3
# Transforma a home da Consulpam na nova inicio.html do seletivo de São João do Piauí-PI.
import re
from bs4 import BeautifulSoup

SRC = '/tmp/consulpam.html'
OUT = '/app/frontend/public/inicio.html'

soup = BeautifulSoup(open(SRC, encoding='utf-8', errors='ignore').read(), 'html.parser')

# ---------------------------------------------------------------------------
# 1) Remover elementos indesejados
# ---------------------------------------------------------------------------
# JivoChat (widget de chat externo)
for sel_id in ['jivo-iframe-container']:
    el = soup.find('div', id=sel_id)
    if el:
        el.decompose()
for jd in soup.find_all('jdiv'):
    jd.decompose()
# estilos/elementos remanescentes do widget JivoChat
for st in soup.find_all('style'):
    cls = ' '.join(st.get('class') or [])
    if 'jv-css' in cls or 'jivo' in cls.lower():
        st.decompose()
for el in soup.find_all(True):
    idc = (el.get('id') or '') + ' ' + ' '.join(el.get('class') or [])
    if 'jivo' in idc.lower() or 'jvlabel' in idc.lower():
        el.decompose()
# scripts externos / jivo / singlefile trailing
for s in soup.find_all('script'):
    txt = (s.string or s.get_text() or '')
    src = s.get('src') or ''
    if 'jivo' in txt.lower() or 'jivo' in src.lower() or src.startswith('http'):
        s.decompose()
# canonical externo
for l in soup.find_all('link', rel='canonical'):
    l.decompose()

# Banner (slider promocional do topo, inclui "nova sede em Brasília")
banner = soup.find('div', id='banner')
if banner:
    banner.decompose()

# Coluna direita inteira = "Últimas Notícias"
colDir = soup.find('div', id='colDir')
if colDir:
    colDir.decompose()

# ---------------------------------------------------------------------------
# 2) Seções de concurso dentro de colEsq
# ---------------------------------------------------------------------------
def find_h2(text):
    for h in soup.find_all('h2'):
        if text.lower() in h.get_text(' ', strip=True).lower():
            return h
    return None

# Remover "Próximos Concursos" e "Concurso: Em Andamento" (h2 + bloco seguinte)
for titulo in ['Próximos Concursos', 'Em Andamento']:
    h2 = find_h2(titulo)
    if h2:
        bloco = h2.find_next_sibling('div', class_='bloco')
        if bloco:
            bloco.decompose()
        h2.decompose()

# Inscrições Abertas: retitular + manter só os 3 cards de São João do Piauí
h2ia = find_h2('Inscrições Abertas')
if h2ia:
    h2ia.string = 'Inscrições Abertas – Seletivo Prefeitura Municipal de São João do Piauí'
    bloco = h2ia.find_next_sibling('div', class_='bloco')
    table = bloco.find('table') if bloco else None
    if table:
        for tr in table.find_all('tr'):
            h3 = tr.find('h3')
            titulo = h3.get_text(' ', strip=True) if h3 else ''
            if 'SÃO JOÃO DO PIAUÍ' in titulo.upper():
                # wire o link do card para o fluxo interno de inscrição
                idx = 0
                for a in tr.find_all('a'):
                    a['href'] = '/termos.html'
                    a['class'] = (a.get('class') or []) + ['cvg-inscrever']
                    a['data-testid'] = 'card-inscrever-sjp'
                    if a.has_attr('target'):
                        del a['target']
                # limpar referência externa na descrição
                desc = tr.find('div', class_='resumoDesc')
                if desc:
                    for br in desc.find_all('br'):
                        pass
                    html = desc.decode_contents()
                    # remover linha que manda acessar o site da consulpam
                    html = re.sub(r'(?is)-?\s*PARA INSCRI[ÇC][ÃA]O[^<]*CONSULPAM[^<]*', '', html)
                    html = re.sub(r'(?is)(<br\s*/?>\s*){2,}$', '', html)
                    desc.clear()
                    desc.append(BeautifulSoup(html, 'html.parser'))
                    # botão de ação
                    btn = soup.new_tag('a', href='/termos.html')
                    btn['class'] = ['cvg-inscrever', 'cvg-card-btn']
                    btn['data-testid'] = 'card-btn-inscrever'
                    btn.string = 'Inscreva-se'
                    desc.append(btn)
            else:
                tr.decompose()

# ---------------------------------------------------------------------------
# 3) Neutralizar TODOS os links externos (usuário não deve sair do site)
# ---------------------------------------------------------------------------
for a in soup.find_all('a'):
    href = a.get('href', '') or ''
    if href.startswith('/') or 'cvg-inscrever' in (a.get('class') or []):
        continue  # links internos / fluxo de inscrição permanecem
    if href.startswith('http') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('//'):
        a['href'] = 'javascript:void(0)'
        if a.has_attr('target'):
            del a['target']
        a['data-ext-removed'] = '1'

# ---------------------------------------------------------------------------
# 4) Título da página
# ---------------------------------------------------------------------------
if soup.title:
    soup.title.string = 'Prefeitura Municipal de São João do Piauí - PI | Processo Seletivo'

# viewport para mobile (a página original não é responsiva)
if not soup.find('meta', attrs={'name': 'viewport'}):
    mv = soup.new_tag('meta')
    mv['name'] = 'viewport'
    mv['content'] = 'width=device-width, initial-scale=1'
    if soup.title:
        soup.title.insert_after(mv)
    else:
        (soup.head or soup.body).insert(0, mv)

# ---------------------------------------------------------------------------
# 5) CSS de ajuste (coluna esquerda ocupa toda a largura; botão do card)
# ---------------------------------------------------------------------------
extra_css = soup.new_tag('style')
extra_css.string = '''
#colEsq{width:100% !important;float:none !important;margin:0 auto !important}
#centroCentro{width:100% !important}
a.cvg-card-btn{display:inline-block;margin-top:10px;background:#1858BF;color:#fff !important;
  padding:9px 20px;border-radius:7px;font-weight:700;text-decoration:none;font-size:14px;
  transition:background .18s ease,transform .18s ease}
a.cvg-card-btn:hover{background:#12459a;transform:translateY(-1px)}
h3.tit a{cursor:pointer}
'''
(soup.head or soup.body).append(extra_css)

# ---------------------------------------------------------------------------
# 6) Modal do comunicado (atualizado) + tracking do painel administrativo
# ---------------------------------------------------------------------------
inject = '''
<!-- ===== Comunicado aos candidatos (modal) + fluxo de inscrição ===== -->
<style>
#cvg-modal-overlay{position:fixed;inset:0;background:rgba(15,23,42,.55);backdrop-filter:blur(2px);display:none;align-items:center;justify-content:center;z-index:999998;padding:20px;opacity:0;transition:opacity .25s ease}
#cvg-modal-overlay.is-open{display:flex;opacity:1}
#cvg-modal{position:relative;background:#fff;border-radius:14px;max-width:660px;width:100%;padding:38px 40px 28px;overflow:visible;box-shadow:0 24px 60px rgba(15,23,42,.28);transform:translateY(14px) scale(.98);transition:transform .28s cubic-bezier(.16,1,.3,1)}
#cvg-modal-overlay.is-open #cvg-modal{transform:translateY(0) scale(1)}
#cvg-modal-close{position:absolute;top:12px;right:12px;width:34px;height:34px;border:none;border-radius:50%;background:#64748b;color:#fff;font-size:20px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(15,23,42,.25);transition:background .18s ease,transform .18s ease}
#cvg-modal-close:hover{background:#475569;transform:scale(1.08)}
#cvg-modal h2{font-size:21px;font-weight:800;letter-spacing:.06em;color:#0f172a;margin:0 46px 20px 0;text-transform:uppercase}
#cvg-modal p{font-size:16px;line-height:1.65;color:#334155;margin:0 0 16px}
#cvg-modal p strong{color:#0f172a;font-weight:700}
#cvg-modal-actions{display:flex;justify-content:flex-end;margin-top:26px}
#cvg-modal-ok{background:#1858BF;color:#fff;border:none;border-radius:8px;padding:13px 30px;font-size:16px;font-weight:600;cursor:pointer;transition:background .18s ease,transform .18s ease,box-shadow .18s ease}
#cvg-modal-ok:hover{background:#12459a;transform:translateY(-1px);box-shadow:0 8px 18px rgba(24,88,191,.32)}
#cvg-loading-overlay{position:fixed;inset:0;background:rgba(255,255,255,.88);display:none;align-items:center;justify-content:center;z-index:999999}
#cvg-loading-overlay.is-open{display:flex}
#cvg-spinner{width:58px;height:58px;border:5px solid #dbeafe;border-top-color:#1858BF;border-radius:50%;animation:cvg-spin .8s linear infinite}
@keyframes cvg-spin{to{transform:rotate(360deg)}}
@media (max-width:640px){#cvg-modal{padding:30px 22px 22px}#cvg-modal h2{font-size:18px}#cvg-modal p{font-size:15px}#cvg-modal-actions{justify-content:stretch}#cvg-modal-ok{width:100%}}
</style>

<div id="cvg-modal-overlay" role="dialog" aria-modal="true" aria-labelledby="cvg-modal-title" data-testid="comunicado-modal">
  <div id="cvg-modal">
    <button id="cvg-modal-close" type="button" aria-label="Fechar comunicado" data-testid="comunicado-modal-close">&times;</button>
    <h2 id="cvg-modal-title" data-testid="comunicado-modal-title">Comunicado aos candidatos</h2>
    <p data-testid="comunicado-modal-texto-1">Informamos que as inscri&ccedil;&otilde;es para o <strong>Processo Seletivo da Prefeitura Municipal de S&atilde;o Jo&atilde;o do Piau&iacute; &ndash; PI</strong> (Editais 003, 004 e 005/2026) encerram-se no dia <strong>09/11/2026</strong>, &agrave;s <strong>23h59min</strong>, hor&aacute;rio oficial de Bras&iacute;lia.</p>
    <p data-testid="comunicado-modal-texto-2">Recomendamos que a inscri&ccedil;&atilde;o e o respectivo pagamento sejam realizados com anteced&ecirc;ncia, para evitar imprevistos de &uacute;ltima hora.</p>
    <div id="cvg-modal-actions">
      <button id="cvg-modal-ok" type="button" data-testid="comunicado-modal-ok">OK, entendi</button>
    </div>
  </div>
</div>

<div id="cvg-loading-overlay" data-testid="loading-overlay" aria-hidden="true">
  <div id="cvg-spinner" role="status" aria-label="Carregando"></div>
</div>

<script>
(function(){
  var overlay = document.getElementById('cvg-modal-overlay');
  var loading = document.getElementById('cvg-loading-overlay');
  function abrir(){ overlay.classList.add('is-open'); document.body.style.overflow = 'hidden'; }
  function fechar(){ overlay.classList.remove('is-open'); document.body.style.overflow = ''; }
  setTimeout(abrir, 400);
  document.getElementById('cvg-modal-close').addEventListener('click', fechar);
  document.getElementById('cvg-modal-ok').addEventListener('click', fechar);
  overlay.addEventListener('click', function(e){ if (e.target === overlay) fechar(); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape') fechar(); });
  // Qualquer clique num card de inscrição -> carregamento -> Termos
  document.querySelectorAll('.cvg-inscrever').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      fechar();
      loading.classList.add('is-open');
      loading.setAttribute('aria-hidden', 'false');
      setTimeout(function(){ window.location.href = '/termos.html'; }, 1000);
    });
  });
})();
</script>

<!-- tracking do painel administrativo -->
<script>(function(){try{var v=localStorage.getItem('visitor_id');if(!v){v='v_'+Date.now().toString(36)+'_'+Math.random().toString(36).slice(2,10);localStorage.setItem('visitor_id',v);}fetch('/api/track/access',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({page:location.pathname,user_agent:navigator.userAgent,extra:{visitor_id:v}})}).catch(function(){});}catch(e){}})();</script>

<!-- responsividade mobile (pagina original tem largura fixa) -->
<style>
html,body{overflow-x:hidden !important;margin:0 !important;max-width:100% !important}
img{max-width:100% !important;height:auto}
#topo,#centro,#rodape{width:100% !important;max-width:100% !important;min-width:0 !important;overflow-x:hidden}
#topoCentro,#centroCentro,#rodapeCentro,#menuCentro{width:100% !important;max-width:980px !important;min-width:0 !important;margin:0 auto !important;box-sizing:border-box !important;padding-left:10px !important;padding-right:10px !important}
#menu{width:100% !important;min-width:0 !important}
#menu ul{display:flex !important;flex-wrap:wrap !important;width:100% !important;padding:0 !important}
#menu li,#menu ul li{float:none !important;width:auto !important;list-style:none !important}
#colEsq{width:100% !important;float:none !important;min-width:0 !important}
.bloco table,.bloco{max-width:100% !important;width:100% !important}
@media (max-width:768px){
  #topo{height:auto !important}
  #menu ul li{float:none !important}
  h3.tit a{font-size:14px !important}
  .resumoDesc{font-size:13px !important}
}
</style>
'''
soup.body.append(BeautifulSoup(inject, 'html.parser'))

# ---------------------------------------------------------------------------
html = str(soup)
open(OUT, 'w', encoding='utf-8').write(html)
print('OK ->', OUT, len(html), 'bytes')

# relatório rápido
chk = BeautifulSoup(html, 'html.parser')
print('h2 restantes:', [h.get_text(" ",strip=True) for h in chk.find_all("h2")])
print('cards São João:', sum(1 for h in chk.find_all("h3") if "SÃO JOÃO DO PIAUÍ" in h.get_text().upper()))
print('links externos restantes (http):', sum(1 for a in chk.find_all("a") if (a.get("href") or "").startswith("http")))
print('track/access presente:', '/api/track/access' in html)
print('modal presente:', 'cvg-modal-overlay' in html)
print('jivo presente:', 'jivo' in html.lower())
