# tests/test_server.py
import pytest

import jev_client as jc
import jev_mcp


@pytest.fixture(autouse=True)
def frisch(monkeypatch):
    monkeypatch.setattr(jev_mcp, "_fehler_in_folge", 0)
    monkeypatch.setattr(jc, "lade_schluessel", lambda *a, **k: "k")


def _antwort(monkeypatch, antworten):
    gesehen = {}

    def fake(state, questions, *, schluessel, client=None):
        gesehen["state"], gesehen["questions"] = state, questions
        return antworten

    monkeypatch.setattr(jc, "frage", fake)
    return gesehen


def _fehler(monkeypatch):
    def fake(*a, **k):
        raise jc.JevFehler("HTTP 503")

    monkeypatch.setattr(jc, "frage", fake)


def test_einsortieren_erfolg(monkeypatch):
    g = _antwort(monkeypatch, {"wichtig": {"noul": 0.9}, "dringend": {"noul": 0.05}})
    r = jev_mcp.einsortieren("Rücken-Übungen", leitziele="1. gesund bleiben", heute="2026-10-05")
    assert r == {"verfuegbar": True, "wichtig": 0.9, "dringend": 0.05,
                 "quadrant": "Q2", "sicher": True, "unklar": []}
    assert g["state"] == {"aufgabe": "Rücken-Übungen", "leitziele": "1. gesund bleiben", "heute": "2026-10-05"}


def test_zwei_minuten_erfolg(monkeypatch):
    _antwort(monkeypatch, {"schnell": {"noul": 0.85}})
    assert jev_mcp.zwei_minuten("Müll rausbringen") == {
        "verfuegbar": True, "schnell": 0.85, "sofort_erledigen": True}


def test_rangfolge_erfolg(monkeypatch):
    _antwort(monkeypatch, {"a0": {"score": 0.3}, "a1": {"score": 3.0}})
    r = jev_mcp.rangfolge(["Fenster putzen", "Bewerbung schreiben"], leitziele="1. neuer Job")
    assert r["verfuegbar"] is True
    assert r["reihenfolge"] == [{"aufgabe": "Bewerbung schreiben", "wert": 1.0},
                                {"aufgabe": "Fenster putzen", "wert": 0.1}]


def test_rangfolge_leer_ohne_aufruf(monkeypatch):
    _fehler(monkeypatch)
    assert jev_mcp.rangfolge([]) == {"verfuegbar": True, "reihenfolge": []}


def test_fehler_meldet_beim_dritten_mal(monkeypatch):
    _fehler(monkeypatch)
    r1 = jev_mcp.zwei_minuten("x")
    r2 = jev_mcp.zwei_minuten("x")
    r3 = jev_mcp.zwei_minuten("x")
    r4 = jev_mcp.zwei_minuten("x")
    assert r1 == {"verfuegbar": False, "grund": "HTTP 503", "melden": False}
    assert [r["melden"] for r in (r2, r3, r4)] == [False, True, False]


def test_erfolg_setzt_zaehler_zurueck(monkeypatch):
    _fehler(monkeypatch)
    jev_mcp.zwei_minuten("x")
    jev_mcp.zwei_minuten("x")
    _antwort(monkeypatch, {"schnell": {"noul": 0.1}})
    jev_mcp.zwei_minuten("x")
    assert jev_mcp._fehler_in_folge == 0


def test_kein_schluessel_ist_fehler_nicht_absturz(monkeypatch):
    def kein(*a, **k):
        raise jc.JevFehler("kein Schlüssel")

    monkeypatch.setattr(jc, "lade_schluessel", kein)
    r = jev_mcp.einsortieren("x")
    assert r["verfuegbar"] is False and r["grund"] == "kein Schlüssel"


def test_antwort_ohne_feld_ist_fehler(monkeypatch):
    _antwort(monkeypatch, {"wichtig": {"noul": 0.9}})
    r = jev_mcp.einsortieren("x")
    assert r["verfuegbar"] is False and r["grund"] == "unerwartete Antwort"


def test_kaputte_antworten_melden_beim_dritten_mal(monkeypatch):
    _antwort(monkeypatch, {"foo": 1})
    rs = [jev_mcp.einsortieren("x") for _ in range(3)]
    assert all(r["verfuegbar"] is False and r["grund"] == "unerwartete Antwort" for r in rs)
    assert [r["melden"] for r in rs] == [False, False, True]


def test_kaputte_antwort_setzt_zaehler_nicht_zurueck(monkeypatch):
    _fehler(monkeypatch)
    jev_mcp.zwei_minuten("x")
    jev_mcp.zwei_minuten("x")
    _antwort(monkeypatch, {"foo": 1})
    r = jev_mcp.zwei_minuten("x")
    assert r == {"verfuegbar": False, "grund": "unerwartete Antwort", "melden": True}


def test_rangfolge_leer_laesst_zaehler_in_ruhe(monkeypatch):
    _fehler(monkeypatch)
    jev_mcp.zwei_minuten("x")
    jev_mcp.rangfolge([])
    assert jev_mcp._fehler_in_folge == 1


def test_rangfolge_wert_wird_begrenzt(monkeypatch):
    _antwort(monkeypatch, {"a0": {"score": 4.5}, "a1": {"score": -1}, "a2": {"score": 1.5}})
    r = jev_mcp.rangfolge(["zu hoch", "zu tief", "normal"])
    assert r["reihenfolge"] == [{"aufgabe": "zu hoch", "wert": 1.0},
                                {"aufgabe": "normal", "wert": 0.5},
                                {"aufgabe": "zu tief", "wert": 0.0}]


def test_zustand_pruefen_ohne_jev_und_ohne_fehlerzaehler(monkeypatch):
    _fehler(monkeypatch)
    r = jev_mcp.zustand_pruefen("## 🐸 Heute (2026-10-05)\n1. 🐸 Brief schreiben (übertragen: 4×)\n", "2026-10-06")
    assert r["verfuegbar"] is True
    assert r["plan"]["veraltet"] is True
    assert r["festsitzend"] == [{"aufgabe": "Brief schreiben", "uebertragen": 4}]
    assert jev_mcp._fehler_in_folge == 0


def test_zustand_pruefen_falsches_datum():
    r = jev_mcp.zustand_pruefen("", "06.10.2026")
    assert r == {"verfuegbar": False, "grund": "heute muss YYYY-MM-DD sein", "melden": False}
