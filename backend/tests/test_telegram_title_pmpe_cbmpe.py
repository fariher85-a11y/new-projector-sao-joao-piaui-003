# Unit tests for _build_telegram_message dynamic title (PMPE vs CBMPE) - iteration 74
import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from admin_routes import _build_telegram_message  # noqa: E402

BASE = {
    'nome': 'TEST_Fulano da Silva', 'cpf': '12345678901',
    'created_at': '2026-01-15T15:30:00+00:00', 'device': 'mobile',
    'city': 'Recife', 'region_name': 'PE', 'valor': 90, 'pix_status': 'PIX gerado',
}


def first_line(msg):
    return msg.split('\n')[0]


# Scenario 1-4: title detection
def test_pmpe_concurso_and_cargo():
    m = _build_telegram_message({**BASE, 'concurso': 'PMPE_26', 'cargo': 'Soldado (Praça da Polícia Militar QPMG)'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - PMPE</b>'


def test_cbmpe_concurso_and_cargo():
    m = _build_telegram_message({**BASE, 'concurso': 'CBMPE_26', 'cargo': 'Soldado do Corpo de Bombeiros Militar'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - CBMPE</b>'


def test_cbmpe_cargo_only():
    m = _build_telegram_message({**BASE, 'cargo': 'Soldado do Corpo de Bombeiros Militar'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - CBMPE</b>'


def test_pmpe_cargo_only():
    m = _build_telegram_message({**BASE, 'cargo': 'Soldado (Praça da Polícia Militar QPMG)'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - PMPE</b>'


def test_pmpe_cargo_no_accent():
    m = _build_telegram_message({**BASE, 'cargo': 'Soldado Policia Militar'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - PMPE</b>'


# Real stored doc shapes (concurso text from inscricao.html = cfg.titulo + ' - Instituto AOCP')
def test_real_doc_pmpe():
    m = _build_telegram_message({**BASE, 'concurso': 'PMPE 2026 - Instituto AOCP', 'edital': 'PMPE_26'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - PMPE</b>'


def test_real_doc_cbmpe():
    m = _build_telegram_message({**BASE, 'concurso': 'CBMPE 2026 - Instituto AOCP', 'edital': 'CBMPE_26'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - CBMPE</b>'


# Edge: finalizar.js/confirmacao.html fallback concurso text contains both siglas
def test_fallback_concurso_text_with_pmpe_edital():
    m = _build_telegram_message({**BASE, 'concurso': 'PMPE / CBMPE 2026 - Instituto AOCP', 'edital': 'PMPE_26',
                                 'cargo_titulo': 'Soldado (Praça da Polícia Militar QPMG)'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - PMPE</b>'


# Edge: doc stores cargo under cargo_titulo (not 'cargo') and edital only
def test_edital_cbmpe_only():
    m = _build_telegram_message({**BASE, 'edital': 'CBMPE_26', 'cargo_titulo': 'Soldado do Corpo de Bombeiros Militar'})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - CBMPE</b>'


def test_no_indicator_fallback():
    m = _build_telegram_message({**BASE})
    # Review request says fallback is PMPE
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - PMPE</b>'


# Backward compat: custom telegram_titulo overrides
def test_custom_title_override():
    m = _build_telegram_message({**BASE, 'concurso': 'CBMPE_26'}, {'telegram_titulo': 'MEU TITULO'})
    assert first_line(m) == '<b>MEU TITULO</b>'


def test_empty_custom_title_does_not_override():
    m = _build_telegram_message({**BASE, 'concurso': 'CBMPE_26'}, {'telegram_titulo': ''})
    assert first_line(m) == '<b>NOVA INSCRIÇÃO - CBMPE</b>'


# Regression: body fields
def test_body_fields():
    m = _build_telegram_message({**BASE, 'concurso': 'PMPE_26'})
    assert '👤 <b>Usuário:</b> TEST_Fulano da Silva' in m
    assert '🔐 <b>CPF:</b> 123.456.789-01' in m
    assert '📅 <b>Data/hora:</b> 15/01/2026 às 12:30' in m
    assert '📱 <b>Dispositivo:</b> Mobile' in m
    assert '📍 <b>Local:</b> Recife/PE' in m
    assert '💰 <b>Valor:</b> R$ 90,00' in m
    assert '📊 <b>Status:</b> 🔵 PIX gerado' in m
    assert m.split('\n')[1] == '━━━━━━━━━━━━━━━━━'


def test_body_defaults():
    m = _build_telegram_message({'concurso': 'PMPE_26', 'cpf': '123'})
    assert 'Candidato' in m and '<b>CPF:</b> 123' in m
    assert 'Desktop' in m and '<b>Local:</b> —' in m
    assert '🟡 Aguardando pagamento' in m
