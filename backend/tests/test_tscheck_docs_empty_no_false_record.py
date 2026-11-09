"""tscheck: envio sem anexar arquivo não deve criar registro de documento falso.

Criterion: POST /api/track/documents com doc_frente e doc_verso vazios responde
{ok:false, error:'no_docs'} e o CPF NAO passa a aparecer em GET /api/admin/documentos.
"""
import os
import random
import requests

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001').rstrip('/')
ADMIN_USER = 'donas'
ADMIN_PASS = 'Seinao10@@'


def gen_cpf():
    n = [random.randint(0, 9) for _ in range(9)]

    def dv(digits):
        s = sum(d * w for d, w in zip(digits, range(len(digits) + 1, 1, -1)))
        r = s % 11
        return 0 if r < 2 else 11 - r

    d1 = dv(n)
    d2 = dv(n + [d1])
    return ''.join(map(str, n + [d1, d2]))


def test_track_documents_both_empty_rejected():
    cpf = gen_cpf()
    r = requests.post(
        f"{BASE_URL}/api/track/documents",
        json={'cpf': cpf, 'doc_tipo': 'RG', 'doc_frente': '', 'doc_verso': ''},
        timeout=15,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data.get('ok') is False, data
    assert data.get('error') == 'no_docs', data

    # confirm CPF did not get registered in admin documentos listing
    login = requests.post(
        f"{BASE_URL}/api/admin/auth/login",
        json={'username': ADMIN_USER, 'password': ADMIN_PASS},
        timeout=15,
    )
    assert login.status_code == 200, login.text
    token = login.json().get('token')
    assert token

    listing = requests.get(
        f"{BASE_URL}/api/admin/documentos",
        headers={'Authorization': f'Bearer {token}'},
        params={'q': cpf},
        timeout=15,
    )
    assert listing.status_code == 200, listing.text
    items = listing.json().get('items', [])
    match = [i for i in items if i.get('cpf') == cpf]
    assert not match, f"CPF {cpf} indevidamente apareceu em /admin/documentos: {match}"
