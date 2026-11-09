"""Unit tests for email From-name feature.

Covers:
  - email_service.send_email / try_send_email building the Resend `from` header
    as "<display_name> <email>" for each from_name scenario (and fallback).
  - admin_routes._from_name_inscricao helper mapping.
  - reply_to inclusion when EMAIL_REPLY_TO is a valid email.
"""
import sys
import os
import types
import asyncio
import functools
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


def sync(fn):
    """Run an async test function via asyncio.run (no pytest-asyncio needed)."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))
    return wrapper

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import email_service
from admin_routes import _from_name_inscricao


# --------------------------------------------------------------------------
# Helper: patch httpx.AsyncClient used inside email_service and capture body
# --------------------------------------------------------------------------
def _make_mock_client(captured, resp_json=None, status=200):
    resp = MagicMock()
    resp.json.return_value = resp_json or {"id": "mock-id-123"}
    resp.raise_for_status = MagicMock()
    resp.status_code = status

    async def fake_post(url, headers=None, json=None):
        captured["url"] = url
        captured["headers"] = headers
        captured["body"] = json
        return resp

    client = MagicMock()
    client.post = AsyncMock(side_effect=fake_post)
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=client)
    cm.__aexit__ = AsyncMock(return_value=False)
    return MagicMock(return_value=cm)


HTML = "<p>Olá, sua inscrição foi confirmada.</p>"
TO = "contato@concursoamapa.online"


@pytest.mark.parametrize("from_name,expected_prefix", [
    ("Instituto AOCP", "Instituto AOCP <"),
    ("Inscrição Polícia Militar PE", "Inscrição Polícia Militar PE <"),
    ("Inscrição Bombeiro Militar PE", "Inscrição Bombeiro Militar PE <"),
    ("Inscrição Pendente", "Inscrição Pendente <"),
])
@sync
async def test_from_header_per_from_name(from_name, expected_prefix):
    # Ensure BYOK Resend path is active
    assert email_service.RESEND_API_KEY and email_service.RESEND_FROM
    captured = {}
    with patch.object(email_service.httpx, "AsyncClient", _make_mock_client(captured)):
        rid = await email_service.send_email(to=TO, subject="Teste", html=HTML, from_name=from_name)
    assert rid == "mock-id-123"
    assert captured["url"] == "https://api.resend.com/emails"
    frm = captured["body"]["from"]
    assert frm.startswith(expected_prefix), f"from header was {frm!r}"
    assert frm.endswith("@concursoamapa.online>"), f"from header was {frm!r}"
    # recipient + subject intact
    assert captured["body"]["to"] == [TO]
    assert captured["body"]["subject"] == "Teste"


@sync
async def test_from_header_fallback_when_no_from_name():
    captured = {}
    with patch.object(email_service.httpx, "AsyncClient", _make_mock_client(captured)):
        await email_service.send_email(to=TO, subject="Teste", html=HTML)  # no from_name
    frm = captured["body"]["from"]
    # Falls back to EMAIL_FROM_NAME (default 'Instituto AOCP')
    assert frm.startswith(f"{email_service.EMAIL_FROM_NAME} <"), f"from header was {frm!r}"
    assert frm.endswith("@concursoamapa.online>")


@sync
async def test_from_header_handles_wrapped_resend_from():
    """If RESEND_FROM already has a display-name wrapper, only the email is extracted."""
    captured = {}
    with patch.object(email_service, "RESEND_FROM", "Old Name <contato@concursoamapa.online>"), \
         patch.object(email_service.httpx, "AsyncClient", _make_mock_client(captured)):
        await email_service.send_email(to=TO, subject="Teste", html=HTML, from_name="Inscrição Pendente")
    frm = captured["body"]["from"]
    assert frm == "Inscrição Pendente <contato@concursoamapa.online>", f"from header was {frm!r}"


@sync
async def test_reply_to_included_when_valid():
    captured = {}
    with patch.object(email_service, "EMAIL_REPLY_TO", "reply@concursoamapa.online"), \
         patch.object(email_service.httpx, "AsyncClient", _make_mock_client(captured)):
        await email_service.send_email(to=TO, subject="Teste", html=HTML, from_name="Instituto AOCP")
    assert captured["body"].get("reply_to") == "reply@concursoamapa.online"


@sync
async def test_reply_to_excluded_when_invalid_placeholder():
    # Current env has placeholder -> EMAIL_REPLY_TO should be None -> not included
    assert email_service.EMAIL_REPLY_TO is None
    captured = {}
    with patch.object(email_service.httpx, "AsyncClient", _make_mock_client(captured)):
        await email_service.send_email(to=TO, subject="Teste", html=HTML, from_name="Instituto AOCP")
    assert "reply_to" not in captured["body"]


@sync
async def test_try_send_email_passes_from_name_and_returns_true():
    captured = {}
    with patch.object(email_service.httpx, "AsyncClient", _make_mock_client(captured)):
        ok = await email_service.try_send_email(
            to=TO, subject="Teste", html=HTML, from_name="Inscrição Bombeiro Militar PE")
    assert ok is True
    assert captured["body"]["from"] == "Inscrição Bombeiro Militar PE <contato@concursoamapa.online>"


@sync
async def test_try_send_email_invalid_recipient_returns_false():
    ok = await email_service.try_send_email(to="not-an-email", subject="x", html=HTML)
    assert ok is False


# --------------------------------------------------------------------------
# _from_name_inscricao helper
# --------------------------------------------------------------------------
@pytest.mark.parametrize("concurso,cargo,expected", [
    ("PMPE_26", "Soldado QPMG", "Inscrição Polícia Militar PE"),
    ("CBMPE_26", "Soldado", "Inscrição Bombeiro Militar PE"),
    ("", "2º Tenente do Corpo de Bombeiros Militar", "Inscrição Bombeiro Militar PE"),
    ("", "", "Inscrição Polícia Militar PE"),
])
def test_from_name_inscricao(concurso, cargo, expected):
    assert _from_name_inscricao(concurso, cargo) == expected
