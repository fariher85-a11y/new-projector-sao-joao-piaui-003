# Regression: mobile white-screen fix (mobile.css) + core /api routes
import os
import requests
import pytest

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL').rstrip('/')
API = f"{BASE_URL}/api"


@pytest.fixture(scope="module")
def token():
    r = requests.post(f"{API}/admin/auth/login", json={"username": "donas", "password": "Seinao10@@"}, timeout=15)
    assert r.status_code == 200, r.text
    d = r.json()
    t = d.get("token") or d.get("access_token")
    assert isinstance(t, str) and t
    return t


# Root API
def test_api_root():
    r = requests.get(f"{API}/", timeout=15)
    assert r.status_code == 200


# KPIs protected
def test_kpis_requires_auth():
    r = requests.get(f"{API}/admin/dashboard/kpis", timeout=15)
    assert r.status_code == 401


def test_kpis_with_token(token):
    r = requests.get(f"{API}/admin/dashboard/kpis", headers={"Authorization": f"Bearer {token}"}, timeout=15)
    assert r.status_code == 200
    assert isinstance(r.json(), dict)


# Static mobile.css fix present
def test_mobile_css_excludes_body():
    r = requests.get(f"{BASE_URL}/assets/mobile.css", timeout=15)
    assert r.status_code == 200
    css = r.text
    assert '[class*="vlibras"]:not(body):not(html)' in css
    assert '[class*="vw-"]:not(body):not(html)' in css
    assert '[class*="vpw-"]:not(body):not(html)' in css


def test_inicio_html_served():
    r = requests.get(f"{BASE_URL}/inicio.html", timeout=15)
    assert r.status_code == 200
    assert "/api/track/access" in r.text
    assert "mobile.css" in r.text
