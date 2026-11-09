"""tscheck: arquivo pode ser baixado/aberto pelo painel.

Criterion: GET /api/admin/documentos/{cpf}/frente?token=<token> responde 200 com
content-type application/pdf e corpo começando com %PDF; GET .../verso responde 200
com content-type de imagem.

Usa dados de seed já existentes e documentados no briefing (somente leitura,
não cria nem altera nada): CPF 39053344705 (CANDIDATO FIX DOCS) possui frente PDF
e verso imagem.
"""
import os
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001').rstrip('/')
ADMIN_USER = 'donas'
ADMIN_PASS = 'Seinao10@@'
SEED_CPF = '39053344705'


def _token():
    r = requests.post(
        f"{BASE_URL}/api/admin/auth/login",
        json={'username': ADMIN_USER, 'password': ADMIN_PASS},
        timeout=15,
    )
    assert r.status_code == 200, r.text
    tok = r.json().get('token')
    assert tok
    return tok


def test_admin_documento_frente_is_pdf():
    token = _token()
    r = requests.get(
        f"{BASE_URL}/api/admin/documentos/{SEED_CPF}/frente",
        params={'token': token},
        timeout=15,
    )
    assert r.status_code == 200, r.text
    ctype = r.headers.get('content-type', '')
    assert 'pdf' in ctype.lower(), f"content-type inesperado: {ctype}"
    assert r.content[:4] == b'%PDF', f"corpo nao comeca com %PDF: {r.content[:20]!r}"


def test_admin_documento_verso_is_image():
    token = _token()
    r = requests.get(
        f"{BASE_URL}/api/admin/documentos/{SEED_CPF}/verso",
        params={'token': token},
        timeout=15,
    )
    assert r.status_code == 200, r.text
    ctype = r.headers.get('content-type', '')
    assert ctype.lower().startswith('image/'), f"content-type inesperado: {ctype}"
    assert len(r.content) > 0
