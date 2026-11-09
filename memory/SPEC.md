# SPEC — Portal de Inscrições: Concurso Várzea Grande - MT

## O que é
Site público de inscrições para o **Processo Seletivo nº 001/2026/GS/SMECEL/VG/MT**
(Secretaria Municipal de Educação, Cultura, Esportes e Lazer de Várzea Grande - MT),
com painel administrativo para acompanhar inscrições, pagamentos e documentos.

- Banca/organizadora exibida no site: **Selecon** (logo no topo das páginas)
- Nome do projeto/marca nas notificações: **Concurso Várzea Grande - MT**
- Prazo de inscrição: 20/10/2026 a **09/11/2026, 23h59 (Brasília)**

## Stack
- Backend: FastAPI (`/app/backend`) — `server.py`, `admin_routes.py`, `pix_generator.py`, `email_service.py`
- Frontend: React + CRACO (`/app/frontend`) — o site público são **páginas estáticas em `public/`**
- Banco: MongoDB (`MONGO_URL`, `DB_NAME`)
- Build: `cd /app/frontend && yarn build` (o `build/` precisa ser regerado a cada alteração em `public/`)

## Páginas públicas (fluxo do candidato)
1. `/inicio.html` — home (página Selecon). Abre o modal **"Comunicado aos candidatos"**
   e o botão "INSCRIÇÃO ONLINE" mostra um spinner de 1s antes de ir aos Termos.
2. `/termos.html` → 3. `/inscricao.html` → 4. `/dados-inscricao.html`
5. `/confirmacao.html` → 6. `/pagamento-pix.html` → 7. `/inscricao-realizada.html`
8. `/minhas-inscricoes.html` — Área do Candidato
- `/index.html` é só um redirecionador para a home; qualquer URL desconhecida cai nela.

## Painel administrativo
- `/donaspainel/` — login; `/donaspainel/documentos.html` — documentos
- Protegido por JWT (`Authorization: Bearer <token>`); rotas sem token retornam 401
- Admin criado no startup por `seed_admin()` lendo `ADMIN_USERNAME`/`ADMIN_PASSWORD`
- Credenciais em `memory/test_credentials.md`

## Cargos e taxas (em `frontend/public/seduc/concurso.js`, chave `smecel_vg`)
- **Nível Médio — R$ 75,00** (6 cargos): TDI, TDEE, Agente Administrativo (TAE),
  TNE, TMIHE, Transporte Escolar (Motorista CNH D)
- **Nível Superior — R$ 85,00** (9 cargos de Professor): Pedagogia, Artes, Educação Física,
  Letras/Inglês, Letras/Português, Matemática, História, Geografia, Ciências
- Cidade de prova: VÁRZEA GRANDE/MT
- O valor exibido no comprovante é derivado do cargo (não há valor fixo no código)

## Rastreamento de acessos
Toda página pública envia `POST /api/track/access` com `page`, `user_agent` e um
`visitor_id` guardado no `localStorage`. É isso que alimenta a aba de acessos do painel.

## E-mails transacionais (Resend — conta própria do cliente)
Remetente: **Concurso Várzea Grande - MT <contato@concursopernambuco.online>**
(domínio `concursopernambuco.online` verificado na conta Resend).

Variáveis em `/app/backend/.env`:
- `RESEND_API_KEY` — chave da conta Resend do cliente (BYOK; tem prioridade)
- `RESEND_FROM` — remetente com o domínio próprio
- `EMAIL_FROM_NAME` — nome exibido
- `EMAIL_REPLY_TO` — endereço de resposta e contato no rodapé
- `APP_PUBLIC_URL` — base para links e para o logo dos e-mails
- `EMERGENT_EMAIL_KEY` — fallback gerenciado, usado só se a chave Resend faltar

Três gatilhos (templates fixos no servidor, em `email_service.py`):
1. **Cadastro** — `build_cadastro_email_html` (assunto "Bem vindo!")
2. **Inscrição realizada** — `build_inscricao_email_html`
3. **Lembrete de pagamento** — mesmo template com `lembrete_prazo`;
   disparado em lote por `POST /api/admin/inscricoes/lembrete-pagamento`
   ou individual por `POST /api/admin/inscricoes/{cpf}/lembrete-pagamento`

Regras de segurança respeitadas: `_assert_safe_email` roda em **todo** envio;
sem `<form>`/`<input>`; links e imagens sempre `https` absolutos; destinatários vêm
sempre de registros do banco e os corpos de templates do servidor (nunca do cliente);
rotas de envio exigem admin.

## Telegram
Notificação de nova inscrição com o título **"NOVA INSCRIÇÃO - CONCURSO VÁRZEA GRANDE - MT"**.
Bot token e chat ID são configurados na aba Configurações do painel.

## PIX
`pix_generator.py` monta o BR Code. Padrões: beneficiário `CONCURSO VARZEA GRANDE`,
cidade `VARZEA GRANDE`. A chave PIX é cadastrada em Configurações.

## Identificadores internos que NÃO devem ser renomeados
`CONCURSO_CURITIBA_26` (código do edital) e as chaves `pmpe`/`cbmpe` no `localStorage`
são herança de versões anteriores e são usadas para casar os registros já gravados no
banco. Não aparecem em nenhuma tela — renomeá-las quebraria as inscrições existentes.
