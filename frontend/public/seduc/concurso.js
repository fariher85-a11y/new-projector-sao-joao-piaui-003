(function(){
  // Cidade(s) de prova — São João do Piauí/PI
  var CIDADES = [['SÃO JOÃO DO PIAUÍ/PI', 'SÃO JOÃO DO PIAUÍ/PI']];
  var C = {
    smecel_vg: {
      titulo: 'Processo Seletivo 2026 – São João do Piauí/PI', sigla: 'PMSJP', orgao: 'Prefeitura Municipal de São João do Piauí',
      edital_opt: 'Processo Seletivo 2026 - São João do Piauí - PI',
      edital_curto: 'Editais nº 003, 004 e 005/2026',
      orgao_edital: 'Prefeitura Municipal de São João do Piauí - PI',
      logo: '/assets/sjp-logo.jpg',
      cargos: [
        {v: '101', n: 'Médio', t: 'Técnico de Desenvolvimento Infantil (TDI)', p: '75.00'},
        {v: '102', n: 'Médio', t: 'Técnico de Desenvolvimento Educacional Especializado (TDEE)', p: '75.00'},
        {v: '103', n: 'Médio', t: 'Agente Administrativo (TAE)', p: '75.00'},
        {v: '104', n: 'Médio', t: 'Técnico em Nutrição Escolar (TNE)', p: '75.00'},
        {v: '105', n: 'Médio', t: 'Técnico de Manutenção da Infraestrutura e Higienização Escolar (TMIHE)', p: '75.00'},
        {v: '106', n: 'Médio', t: 'Transporte Escolar - Motorista CNH D (TSAE)', p: '75.00'},
        {v: '201', n: 'Superior', t: 'Professor - Pedagogia', p: '85.00'},
        {v: '202', n: 'Superior', t: 'Professor - Artes', p: '85.00'},
        {v: '203', n: 'Superior', t: 'Professor - Educação Física', p: '85.00'},
        {v: '204', n: 'Superior', t: 'Professor - Letras/Língua Inglesa', p: '85.00'},
        {v: '205', n: 'Superior', t: 'Professor - Letras/Língua Portuguesa', p: '85.00'},
        {v: '206', n: 'Superior', t: 'Professor - Matemática', p: '85.00'},
        {v: '207', n: 'Superior', t: 'Professor - História', p: '85.00'},
        {v: '208', n: 'Superior', t: 'Professor - Geografia', p: '85.00'},
        {v: '209', n: 'Superior', t: 'Professor - Ciências', p: '85.00'}
      ],
      pagina: '/termos.html'
    }
  };
  // Aliases aceitos na URL (?c=...)
  var ALIAS = {smecel: 'smecel_vg', vg: 'smecel_vg', concurso: 'smecel_vg', seletivo: 'smecel_vg', pss: 'smecel_vg', curitiba: 'smecel_vg', curitiba_concurso: 'smecel_vg', curitiba_seletivo: 'smecel_vg'};
  function norm(k){ k = (ALIAS[k] || k); return C[k] ? k : ''; }
  var key = 'smecel_vg';
  try {
    var q = norm(new URLSearchParams(location.search).get('c') || '');
    if (q) { key = q; localStorage.setItem('concurso_sel', q); }
    else { var s = norm(localStorage.getItem('concurso_sel') || ''); if (s) { key = s; localStorage.setItem('concurso_sel', s); } }
  } catch (e) {}
  var cur = C[key];
  window.SEAD_CONCURSO = {key: key, cfg: cur};

  function optHtml(list){
    return '<option value="">Selecione</option>' + list.map(function(c){
      return '<option value="' + c.v + '" data-price="' + c.p + '" data-nivel="' + (c.n || '') + '">' +
             c.v + '  -  ' + c.t + '  -  R$ ' + c.p.replace('.', ',') + '</option>';
    }).join('');
  }

  function fill(){
    document.querySelectorAll('[data-c]').forEach(function(el){
      var k = el.getAttribute('data-c');
      if (cur[k] != null && el.textContent !== cur[k]) el.textContent = cur[k];
    });
    document.querySelectorAll('[data-c-src]').forEach(function(el){
      var k = el.getAttribute('data-c-src');
      if (cur[k] != null && el.getAttribute('src') !== cur[k]) el.setAttribute('src', cur[k]);
    });
    var vaga = document.getElementById('VAGA');
    if (vaga && !vaga.dataset.cfg) {
      vaga.dataset.cfg = key;
      vaga.innerHTML = optHtml(cur.cargos);

      // Campo "Nível de escolaridade" que filtra as vagas por nível
      var niveis = cur.cargos.map(function(c){ return c.n; }).filter(function(v, i, a){ return v && a.indexOf(v) === i; });
      if (niveis.length > 1 && !document.getElementById('NIVEL')) {
        var host = vaga.closest('.campo, .form-group, .form-row, p') || vaga.parentNode;
        var wrap = document.createElement('div');
        wrap.className = 'campo-nivel';
        wrap.style.margin = '0 0 12px';
        wrap.innerHTML = '<label for="NIVEL" style="display:block;font-weight:600;margin-bottom:4px">Nível de escolaridade</label>' +
          '<select id="NIVEL" style="width:100%"><option value="">Todos os níveis</option>' +
          niveis.map(function(n){ return '<option value="' + n + '">' + n + '</option>'; }).join('') + '</select>';
        host.parentNode.insertBefore(wrap, host);
        document.getElementById('NIVEL').addEventListener('change', function(){
          var nv = this.value;
          var list = nv ? cur.cargos.filter(function(c){ return c.n === nv; }) : cur.cargos;
          vaga.innerHTML = optHtml(list);
          vaga.dispatchEvent(new Event('change', {bubbles: true}));
        });
      }
    }
    var mp = document.getElementById('MUNICIPIO_PROVA');
    if (mp && !mp.dataset.cfg) {
      mp.dataset.cfg = key;
      var prev = mp.value;
      mp.innerHTML = '<option value="">Selecione</option>' + CIDADES.map(function(c){ return '<option value="' + c[0] + '" data-uf="PI">' + c[1] + '</option>'; }).join('');
      if (CIDADES.some(function(c){ return c[0] === prev; })) mp.value = prev;
    }
    var uf = document.getElementById('UF_PROVA'); if (uf) uf.value = 'PI';
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fill); else fill();
  // Formulário multi-etapas: o campo #VAGA pode ser injetado só ao avançar de etapa.
  // Observa até o VAGA aparecer e então desconecta (evita loop com outras mutações).
  try {
    var mo = new MutationObserver(function(){
      var v = document.getElementById('VAGA');
      if (v) { fill(); if (v.dataset.cfg) mo.disconnect(); }
    });
    mo.observe(document.documentElement, {childList: true, subtree: true});
  } catch (e) {}
  window.addEventListener('load', function(){
    var v = document.getElementById('VAGA'); if (!v) return;
    var sv = ''; try { sv = (JSON.parse(localStorage.getItem('inscricao_dados') || '{}').VAGA) || ''; } catch (e) {}
    v.value = sv; v.dispatchEvent(new Event('change', {bubbles: true}));
    if (v.selectedIndex < 0) v.selectedIndex = 0;
  });
})();
