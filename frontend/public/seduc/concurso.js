(function(){
  var CIDADES = [['SÃO JOÃO DO PIAUÍ/PI', 'SÃO JOÃO DO PIAUÍ/PI']];
  var EDITAIS = [['003','Edital nº 003/2026'],['004','Edital nº 004/2026'],['005','Edital nº 005/2026']];
  var CARGOS = [{"v": "003-001", "ed": "003", "num": "001", "t": "Médico(A) Caps", "vg": "5", "p": "110.00"}, {"v": "003-002", "ed": "003", "num": "002", "t": "Médico(A)", "vg": "5", "p": "110.00"}, {"v": "003-003", "ed": "003", "num": "003", "t": "Médico(A) Perito(A) Municipal", "vg": "2", "p": "110.00"}, {"v": "003-004", "ed": "003", "num": "004", "t": "Médico(A) Plantonista-Maternidade", "vg": "5", "p": "110.00"}, {"v": "003-005", "ed": "003", "num": "005", "t": "Médico(A) Plantonista-Samu", "vg": "5", "p": "110.00"}, {"v": "003-006", "ed": "003", "num": "006", "t": "Enfermeiro(A)", "vg": "15", "p": "110.00"}, {"v": "003-007", "ed": "003", "num": "007", "t": "Enfermeiro(A) Plantonista-Maternidade", "vg": "21", "p": "110.00"}, {"v": "003-008", "ed": "003", "num": "008", "t": "Enfermeiro(A) Plantonista-Samu", "vg": "9", "p": "110.00"}, {"v": "003-009", "ed": "003", "num": "009", "t": "Técnico(A) De Enfermagem", "vg": "27", "p": "90.00"}, {"v": "003-010", "ed": "003", "num": "010", "t": "Técnico(A) De Enfermagem Plantonista-Maternidade", "vg": "30", "p": "90.00"}, {"v": "003-011", "ed": "003", "num": "011", "t": "Técnico(A) De Enfermagem Plantonista-Samu", "vg": "9", "p": "90.00"}, {"v": "003-012", "ed": "003", "num": "012", "t": "Dentista(Cirurgião-Dentista)", "vg": "9", "p": "110.00"}, {"v": "003-013", "ed": "003", "num": "013", "t": "Dentista (Cirurgião-Dentista)-Buco Maxilo", "vg": "3", "p": "110.00"}, {"v": "003-014", "ed": "003", "num": "014", "t": "Dentista (Cirurgião-Dentista)-Cirurgia Oral Menor", "vg": "3", "p": "110.00"}, {"v": "003-015", "ed": "003", "num": "015", "t": "Dentista (Cirurgião-Dentista)-Endodontia", "vg": "3", "p": "110.00"}, {"v": "003-016", "ed": "003", "num": "016", "t": "Técnico(A) Em Saúde Bucal", "vg": "12", "p": "90.00"}, {"v": "003-017", "ed": "003", "num": "017", "t": "Assistente Social", "vg": "51", "p": "110.00"}, {"v": "003-018", "ed": "003", "num": "018", "t": "Educador(A) Físico(A)", "vg": "18", "p": "110.00"}, {"v": "003-019", "ed": "003", "num": "019", "t": "Farmacêutico(A)", "vg": "6", "p": "110.00"}, {"v": "003-020", "ed": "003", "num": "020", "t": "Fisioterapeuta", "vg": "6", "p": "110.00"}, {"v": "003-021", "ed": "003", "num": "021", "t": "Fisioterapeuta Plantonista - Maternidade", "vg": "9", "p": "110.00"}, {"v": "003-022", "ed": "003", "num": "022", "t": "Terapeuta Ocupacional", "vg": "9", "p": "110.00"}, {"v": "003-023", "ed": "003", "num": "023", "t": "Fonoaudiólogo(A)", "vg": "6", "p": "110.00"}, {"v": "003-024", "ed": "003", "num": "024", "t": "Nutricionista", "vg": "42", "p": "110.00"}, {"v": "003-025", "ed": "003", "num": "025", "t": "Orientador(A) Social-Zona Urbana", "vg": "6", "p": "90.00"}, {"v": "003-026", "ed": "003", "num": "026", "t": "Psicólogo(A)", "vg": "39", "p": "110.00"}, {"v": "003-027", "ed": "003", "num": "027", "t": "Educador(A) Social", "vg": "9", "p": "90.00"}, {"v": "003-028", "ed": "003", "num": "028", "t": "Instrutor(A) De Capoeira", "vg": "9", "p": "90.00"}, {"v": "003-029", "ed": "003", "num": "029", "t": "Instrutor(A) De Divers.,Territ. E Sustent.", "vg": "12", "p": "90.00"}, {"v": "003-030", "ed": "003", "num": "030", "t": "Instrutor(A) De Educação Digital", "vg": "12", "p": "90.00"}, {"v": "003-031", "ed": "003", "num": "031", "t": "Instrutor(A) De Lab. De Líng. Port.", "vg": "12", "p": "90.00"}, {"v": "003-032", "ed": "003", "num": "032", "t": "Instrutor(A) De Lab. De Mat.", "vg": "12", "p": "90.00"}, {"v": "003-033", "ed": "003", "num": "033", "t": "Instrutor(A) De Produção Artística", "vg": "6", "p": "90.00"}, {"v": "003-034", "ed": "003", "num": "034", "t": "Instrutor De Música - Violão", "vg": "12", "p": "90.00"}, {"v": "003-035", "ed": "003", "num": "035", "t": "Instrutor(A) De Música-Flauta Doce", "vg": "3", "p": "90.00"}, {"v": "003-036", "ed": "003", "num": "036", "t": "Instrutor(A) De Música-Sopro", "vg": "3", "p": "90.00"}, {"v": "003-037", "ed": "003", "num": "037", "t": "Instrutor(A) De Música-Violino", "vg": "3", "p": "90.00"}, {"v": "003-038", "ed": "003", "num": "038", "t": "Psicopedagogo(A) - Educação", "vg": "9", "p": "110.00"}, {"v": "003-039", "ed": "003", "num": "039", "t": "Arquiteto(A)", "vg": "3", "p": "110.00"}, {"v": "003-040", "ed": "003", "num": "040", "t": "Biólogo(A)", "vg": "3", "p": "110.00"}, {"v": "003-041", "ed": "003", "num": "041", "t": "Engenheiro(A) Elétrico(A)", "vg": "3", "p": "110.00"}, {"v": "003-042", "ed": "003", "num": "042", "t": "Monitor De Transporte Escolar", "vg": "18", "p": "90.00"}, {"v": "003-043", "ed": "003", "num": "043", "t": "Operador(A) De Sist. De Infor. Em Saúde", "vg": "9", "p": "90.00"}, {"v": "003-044", "ed": "003", "num": "044", "t": "Técnico(A) Em Farmácia", "vg": "3", "p": "90.00"}, {"v": "003-045", "ed": "003", "num": "045", "t": "Técnico(A) Em Farmácia Plant-Mater", "vg": "12", "p": "90.00"}, {"v": "003-046", "ed": "003", "num": "046", "t": "Técnico(A) Em Informática", "vg": "10", "p": "90.00"}, {"v": "003-047", "ed": "003", "num": "047", "t": "Condutor(A) Socorrista Plantonista - Samu", "vg": "12", "p": "60.00"}, {"v": "003-048", "ed": "003", "num": "048", "t": "Mecânico(A)", "vg": "3", "p": "60.00"}, {"v": "003-049", "ed": "003", "num": "049", "t": "Motorista", "vg": "12", "p": "60.00"}, {"v": "003-050", "ed": "003", "num": "050", "t": "Motorista Categoria Ab", "vg": "12", "p": "60.00"}, {"v": "003-051", "ed": "003", "num": "051", "t": "Motorista Transporte Escolar", "vg": "45", "p": "60.00"}, {"v": "003-052", "ed": "003", "num": "052", "t": "Motorista Categoria D", "vg": "6", "p": "60.00"}, {"v": "003-053", "ed": "003", "num": "053", "t": "Condutor Socorrista-Maternidade", "vg": "9", "p": "60.00"}, {"v": "003-054", "ed": "003", "num": "054", "t": "Operador(A) De Máquinas", "vg": "18", "p": "60.00"}, {"v": "003-055", "ed": "003", "num": "055", "t": "Auxiliar De Cozinha", "vg": "9", "p": "60.00"}, {"v": "003-056", "ed": "003", "num": "056", "t": "Auxiliar De Serviços Gerais/Zelador(A)", "vg": "393", "p": "60.00"}, {"v": "003-057", "ed": "003", "num": "057", "t": "Cozinheiro(A)", "vg": "16", "p": "60.00"}, {"v": "003-058", "ed": "003", "num": "058", "t": "Magarefe", "vg": "9", "p": "60.00"}, {"v": "003-059", "ed": "003", "num": "059", "t": "Vigia/Vigilante", "vg": "111", "p": "60.00"}, {"v": "003-060", "ed": "003", "num": "060", "t": "Orientador(A) Social - Região De Cima", "vg": "3", "p": "90.00"}, {"v": "003-061", "ed": "003", "num": "061", "t": "Orientador(A) Social - Região De Baixo", "vg": "3", "p": "90.00"}, {"v": "003-062", "ed": "003", "num": "062", "t": "Psicopedagogo(A) - Saúde", "vg": "9", "p": "110.00"}, {"v": "003-063", "ed": "003", "num": "063", "t": "Técnico Em Zootecnia", "vg": "4", "p": "90.00"}, {"v": "003-064", "ed": "003", "num": "064", "t": "Mediador De Apoio Educacional Especializado - Zona Rural", "vg": "60", "p": "90.00"}, {"v": "003-065", "ed": "003", "num": "065", "t": "Mediador De Apoio Educacional Especializado - Zona Urbana", "vg": "70", "p": "90.00"}, {"v": "004-001", "ed": "004", "num": "001", "t": "Professor(A) De Ciências - Zona Rural", "vg": "6", "p": "110.00"}, {"v": "004-002", "ed": "004", "num": "002", "t": "Professor(A) De Ciências - Zona Urbana", "vg": "6", "p": "110.00"}, {"v": "004-003", "ed": "004", "num": "003", "t": "Professor De Educação Física-Zona Rural", "vg": "6", "p": "110.00"}, {"v": "004-004", "ed": "004", "num": "004", "t": "Professor De Educação Física-Zona Urbana", "vg": "21", "p": "110.00"}, {"v": "004-005", "ed": "004", "num": "005", "t": "Professor(A) De Física - Zona Urbana", "vg": "6", "p": "110.00"}, {"v": "004-006", "ed": "004", "num": "006", "t": "Professor(A) De Geografia - Zona Urbana", "vg": "3", "p": "110.00"}, {"v": "004-007", "ed": "004", "num": "007", "t": "Professor(A) De História-Zona Rural", "vg": "6", "p": "110.00"}, {"v": "004-008", "ed": "004", "num": "008", "t": "Professor(A) De História-Zona Urbana", "vg": "6", "p": "110.00"}, {"v": "004-009", "ed": "004", "num": "009", "t": "Professor(A) De Língua Inglesa-Zona Rural", "vg": "3", "p": "110.00"}, {"v": "004-010", "ed": "004", "num": "010", "t": "Professor(A) De Língua Inglesa-Zona Urbana", "vg": "15", "p": "110.00"}, {"v": "004-011", "ed": "004", "num": "011", "t": "Professor(A) De Língua Portuguesa-Zona Rural", "vg": "9", "p": "110.00"}, {"v": "004-012", "ed": "004", "num": "012", "t": "Professor De Língua Portuguesa-Zona Urbana", "vg": "9", "p": "110.00"}, {"v": "004-013", "ed": "004", "num": "013", "t": "Professor De Matemática-Zona Rural", "vg": "6", "p": "110.00"}, {"v": "004-014", "ed": "004", "num": "014", "t": "Professor De Matemática-Zona Urbana", "vg": "12", "p": "110.00"}, {"v": "004-015", "ed": "004", "num": "015", "t": "Professor Pedagogo-Zona Rural", "vg": "60", "p": "110.00"}, {"v": "004-016", "ed": "004", "num": "016", "t": "Professor Pedagogo-Zona Urbana", "vg": "150", "p": "110.00"}, {"v": "005-001", "ed": "005", "num": "001", "t": "Agente De Combate A Endemias", "vg": "21", "p": "90.00"}, {"v": "005-002", "ed": "005", "num": "002", "t": "Agente Comunitário De Saúde(Acs)-Ubs Tia Diva-Barro Vermelho", "vg": "30", "p": "90.00"}, {"v": "005-003", "ed": "005", "num": "003", "t": "Agente Comunitário De Saúde (Acs) - Ubs Dr. Jose Abel - Alto Sertanejo", "vg": "30", "p": "90.00"}, {"v": "005-004", "ed": "005", "num": "004", "t": "Agente Comunitário De Saúde (Acs) - Ubs Josefa Dias De Sousa - Lisboa", "vg": "15", "p": "90.00"}, {"v": "005-005", "ed": "005", "num": "005", "t": "Agente Comunitário De Saúde(Acs)-Ubs Simplicio Ferreira De Carvalho-Piçarra", "vg": "24", "p": "90.00"}, {"v": "005-006", "ed": "005", "num": "006", "t": "Agente Comunitário De Saúde (Acs) - Ubs Mãe Helena - Grajaú", "vg": "15", "p": "90.00"}];
  var cur = {
    titulo:'Processo Seletivo 2026 – São João do Piauí/PI', sigla:'PMSJP',
    orgao:'Prefeitura Municipal de São João do Piauí',
    edital_opt:'Processo Seletivo 2026 - São João do Piauí - PI',
    edital_curto:'Editais nº 003, 004 e 005/2026',
    orgao_edital:'Prefeitura Municipal de São João do Piauí - PI',
    logo:'/assets/sjp-logo.jpg', cargos: CARGOS, pagina:'/termos.html'
  };
  window.SEAD_CONCURSO = {key:'pmsjp', cfg:cur};

  function optHtml(list){
    if(!list.length) return '<option value="">Selecione o edital primeiro</option>';
    return '<option value="">Selecione</option>' + list.map(function(c){
      return '<option value="'+c.v+'" data-price="'+c.p+'" data-ed="'+c.ed+'">'+
             c.num+'  -  '+c.t+'  -  '+c.vg+' vaga(s)  -  R$ '+c.p.replace('.',',')+'</option>';
    }).join('');
  }

  function fill(){
    document.querySelectorAll('[data-c]').forEach(function(el){
      var k=el.getAttribute('data-c'); if(cur[k]!=null && el.textContent!==cur[k]) el.textContent=cur[k];
    });
    document.querySelectorAll('[data-c-src]').forEach(function(el){
      var k=el.getAttribute('data-c-src'); if(cur[k]!=null && el.getAttribute('src')!==cur[k]) el.setAttribute('src',cur[k]);
    });
    var vaga=document.getElementById('VAGA');
    if(vaga && !vaga.dataset.cfg){
      vaga.dataset.cfg='pmsjp';
      vaga.innerHTML=optHtml([]);
      if(!document.getElementById('EDITAL')){
        var host=vaga.closest('.campo, .form-group, .form-row, p') || vaga.parentNode;
        var wrap=document.createElement('div'); wrap.className='campo-edital'; wrap.style.margin='0 0 12px';
        wrap.innerHTML='<label for="EDITAL" style="display:block;font-weight:600;margin-bottom:4px">Edital</label>'+
          '<select id="EDITAL" style="width:100%"><option value="">Selecione o edital</option>'+
          EDITAIS.map(function(e){return '<option value="'+e[0]+'">'+e[1]+'</option>';}).join('')+'</select>';
        host.parentNode.insertBefore(wrap,host);
        document.getElementById('EDITAL').addEventListener('change',function(){
          var ed=this.value;
          var list=ed?CARGOS.filter(function(c){return c.ed===ed;}):[];
          vaga.innerHTML=optHtml(list);
          vaga.dispatchEvent(new Event('change',{bubbles:true}));
        });
      }
    }
    var mp=document.getElementById('MUNICIPIO_PROVA');
    if(mp && !mp.dataset.cfg){
      mp.dataset.cfg='pmsjp'; var prev=mp.value;
      mp.innerHTML='<option value="">Selecione</option>'+CIDADES.map(function(c){return '<option value="'+c[0]+'" data-uf="PI">'+c[1]+'</option>';}).join('');
      if(CIDADES.some(function(c){return c[0]===prev;})) mp.value=prev;
    }
    var uf=document.getElementById('UF_PROVA'); if(uf) uf.value='PI';
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',fill); else fill();
  try{
    var mo=new MutationObserver(function(){var v=document.getElementById('VAGA'); if(v){fill(); if(v.dataset.cfg) mo.disconnect();}});
    mo.observe(document.documentElement,{childList:true,subtree:true});
  }catch(e){}
  window.addEventListener('load',function(){
    var v=document.getElementById('VAGA'); if(!v) return;
    var sv='',ed=''; try{var d=JSON.parse(localStorage.getItem('inscricao_dados')||'{}'); sv=d.VAGA||''; }catch(e){}
    if(sv){ ed=sv.split('-')[0]; var es=document.getElementById('EDITAL'); if(es){ es.value=ed; es.dispatchEvent(new Event('change',{bubbles:true})); } v.value=sv; }
    v.dispatchEvent(new Event('change',{bubbles:true}));
  });
})();
