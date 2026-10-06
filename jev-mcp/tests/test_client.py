# tests/test_client.py
import json

import httpx
import pytest

import jev_client as jc


def _client(handler):
    return httpx.Client(transport=httpx.MockTransport(handler), timeout=jc.ZEITLIMIT)


def test_schluessel_aus_umgebung(monkeypatch, tmp_path):
    monkeypatch.setenv("TYPESAFE_API_KEY", " k-env ")
    assert jc.lade_schluessel(tmp_path / "fehlt") == "k-env"


def test_schluessel_aus_datei(monkeypatch, tmp_path):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    d = tmp_path / "key"
    d.write_text("k-datei\n", encoding="utf-8")
    assert jc.lade_schluessel(d) == "k-datei"


def test_kein_schluessel(monkeypatch, tmp_path):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    with pytest.raises(jc.JevFehler, match="kein Schlüssel"):
        jc.lade_schluessel(tmp_path / "fehlt")


def test_schluessel_mit_bom(monkeypatch, tmp_path):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    d = tmp_path / "key"
    d.write_text("﻿k-bom", encoding="utf-8")
    assert jc.lade_schluessel(d) == "k-bom"


def test_schluessel_utf16_ist_jevfehler(monkeypatch, tmp_path):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    d = tmp_path / "key"
    d.write_text("k", encoding="utf-16")
    with pytest.raises(jc.JevFehler, match="kein Schlüssel"):
        jc.lade_schluessel(d)


def test_schluessel_nicht_ascii_ist_jevfehler_ohne_schluesseltext(monkeypatch, tmp_path):
    monkeypatch.delenv("TYPESAFE_API_KEY", raising=False)
    d = tmp_path / "key"
    d.write_text("k-geheim-ü", encoding="utf-8")
    with pytest.raises(jc.JevFehler) as e:
        jc.lade_schluessel(d)
    assert "geheim" not in str(e.value)


def test_schluessel_umgebung_nicht_ascii_ist_jevfehler(monkeypatch, tmp_path):
    monkeypatch.setenv("TYPESAFE_API_KEY", "k-ü")
    with pytest.raises(jc.JevFehler, match="kein Schlüssel"):
        jc.lade_schluessel(tmp_path / "fehlt")


def test_frage_sendet_richtigen_aufruf():
    gesehen = {}

    def handler(req):
        gesehen["url"] = str(req.url)
        gesehen["auth"] = req.headers["authorization"]
        gesehen["body"] = json.loads(req.content)
        return httpx.Response(200, json={"answers": {"x": {"type": "noul", "noul": 0.9}}})

    antworten = jc.frage({"aufgabe": "A"}, {"x": {"type": "noul", "instructions": "?"}},
                         schluessel="geheim", client=_client(handler))
    assert antworten == {"x": {"type": "noul", "noul": 0.9}}
    assert gesehen["url"] == jc.API_URL
    assert gesehen["auth"] == "Bearer geheim"
    assert gesehen["body"]["model"] == "jev-latest"
    assert gesehen["body"]["state"] == {"aufgabe": "A"}


def test_http_fehler_ohne_schluessel_in_meldung():
    c = _client(lambda req: httpx.Response(401, json={"error": "bad key"}))
    with pytest.raises(jc.JevFehler) as e:
        jc.frage("s", {}, schluessel="geheim", client=c)
    assert "401" in str(e.value)
    assert "geheim" not in str(e.value)


def test_zeitueberschreitung_wird_jevfehler():
    def handler(req):
        raise httpx.ReadTimeout("zu langsam", request=req)

    with pytest.raises(jc.JevFehler, match="nicht erreichbar"):
        jc.frage("s", {}, schluessel="k", client=_client(handler))


def test_kaputte_antwort_wird_jevfehler():
    c = _client(lambda req: httpx.Response(200, text="kein json"))
    with pytest.raises(jc.JevFehler, match="unerwartete Antwort"):
        jc.frage("s", {}, schluessel="k", client=c)


@pytest.mark.parametrize("body", [[], "x", None, 5, {"foo": 1}, {"answers": None}, {"answers": []}])
def test_json_ohne_objekt_wird_jevfehler(body):
    # content statt json=: httpx schickt bei json=None sonst einen leeren Body statt "null"
    c = _client(lambda req: httpx.Response(
        200, content=json.dumps(body).encode(), headers={"content-type": "application/json"}))
    with pytest.raises(jc.JevFehler, match="unerwartete Antwort"):
        jc.frage("s", {}, schluessel="k", client=c)


def test_fragen_einsortieren_sind_nouls():
    f = jc.fragen_einsortieren()
    assert set(f) == {"wichtig", "dringend"}
    assert all(q["type"] == "noul" for q in f.values())


def test_fragen_rangfolge_eine_frage_pro_aufgabe():
    f = jc.fragen_rangfolge(["A", "B"])
    assert list(f) == ["a0", "a1"]
    assert f["a0"]["type"] == "score"
    assert f["a0"]["instructions"]["aufgabe"] == "A"
    assert len(f["a0"]["criteria"]) == jc.STUFEN


@pytest.mark.parametrize("antworten", [{}, {"schnell": {}}, {"schnell": None}, {"schnell": {"noul": "x"}}])
def test_verbindungstest_meldet_falsche_antwort_ohne_absturz(monkeypatch, capsys, antworten):
    monkeypatch.setattr(jc, "lade_schluessel", lambda: "k")
    monkeypatch.setattr(jc, "frage", lambda *a, **k: antworten)
    assert jc._verbindungstest() == 1
    assert "Jev NICHT erreichbar: unerwartete Antwort" in capsys.readouterr().out
