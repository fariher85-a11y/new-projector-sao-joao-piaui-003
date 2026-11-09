# PRD — Clone do Repositório (Processo Seletivo Várzea Grande / MT 001)

## Problem Statement
Clonar integralmente o repositório `https://github.com/cleitonafmelo-tech/new-projetctor-varzea-grande-mt-001`
em `/app`, substituindo o conteúdo atual sem alterar a arquitetura, preservando obrigatoriamente:
`/app/.git`, `/app/.emergent`, `/app/frontend/.env`, `/app/backend/.env`.

Observação importante: o repositório NÃO é um projeto AACD (como o resumo antigo sugeria).
É um sistema institucional de inscrições de Processo Seletivo (Selecon — SMECEL/VG/MT),
com home estática em `public/index.html` e painel administrativo React em `/donaspainel`.
O usuário confirmou explicitamente: "Clonar o projeto exatamente como está" / "faça igual".

## Arquitetura
- Backend: FastAPI (`/app/backend/server.py`, `admin_routes.py`, `pix_generator.py`, `email_service.py`).
- Frontend: React 19 + CRACO + Yarn. Home pública renderizada de `public/index.html` (App.js retorna null).
- MongoDB via `MONGO_URL` + `DB_NAME` (preservados).
- Auth admin via JWT (HS256). Admin semeado no startup por `seed_admin()`.

## Implementado (2026-11-09)
- Repositório clonado para `/app` preservando `.git`, `.emergent`, `backend/.env`, `frontend/.env`.
- Dependências instaladas: `pip install -r requirements.txt` (backend) e `yarn install` (frontend).
- Adicionada variável nova `JWT_SECRET` (valor forte) ao `backend/.env` — nenhuma variável protegida alterada.
- Serviços reiniciados via Supervisor (backend + frontend RUNNING).
- Validações manuais OK:
  - GET /api/ -> {"message":"Painel Administrativo API"}
  - POST /api/admin/auth/login (donas/Seinao10@@) -> token + user
  - GET /api/admin/auth/me sem token -> 401 ; com token -> 200
  - GET /api/admin/dashboard/kpis com token -> 200
  - Home institucional renderiza corretamente.

## Credenciais
- Admin: donas / Seinao10@@ (ver test_credentials.md)

## Backlog / Próximos
- P2: Configurar chave PIX pelo painel (Configurações) — seed de PIX está desativado por design.
- P2: Variáveis Resend (RESEND_API_KEY, RESEND_FROM, APP_PUBLIC_URL) ausentes — e-mail opcional no preview.
