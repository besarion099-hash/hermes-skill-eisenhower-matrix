# tests/test_logik.py
import logik


def test_grenzen_sind_unklar():
    assert logik.ist_unklar(0.35)
    assert logik.ist_unklar(0.5)
    assert logik.ist_unklar(0.65)
    assert not logik.ist_unklar(0.34)
    assert not logik.ist_unklar(0.66)


def test_quadranten():
    assert logik.quadrant(0.9, 0.9) == "Q1"
    assert logik.quadrant(0.9, 0.1) == "Q2"
    assert logik.quadrant(0.1, 0.9) == "Q3"
    assert logik.quadrant(0.1, 0.1) == "Q4"
    assert logik.quadrant(0.5, 0.5) == "Q1"


def test_einsortierung_sicher():
    r = logik.bewerte_einsortierung(0.92, 0.12)
    assert r == {"wichtig": 0.92, "dringend": 0.12, "quadrant": "Q2", "sicher": True, "unklar": []}


def test_einsortierung_ein_punkt_unklar():
    r = logik.bewerte_einsortierung(0.55, 0.05)
    assert r["sicher"] is False
    assert r["unklar"] == ["wichtig"]
    assert r["quadrant"] == "Q2"


def test_einsortierung_beide_unklar():
    assert logik.bewerte_einsortierung(0.4, 0.6)["unklar"] == ["wichtig", "dringend"]


def test_zwei_minuten_schwelle():
    assert logik.bewerte_zwei_minuten(0.8) == {"schnell": 0.8, "sofort_erledigen": True}
    assert logik.bewerte_zwei_minuten(0.79)["sofort_erledigen"] is False


def test_rangfolge_absteigend_und_duplikate_bleiben():
    r = logik.sortiere_rangfolge([("A", 0.2), ("B", 0.9), ("A", 0.5)])
    assert [x["wert"] for x in r] == [0.9, 0.5, 0.2]
    assert [x["aufgabe"] for x in r] == ["B", "A", "A"]


def test_werte_werden_gerundet():
    assert logik.bewerte_einsortierung(0.123456, 0.987654)["wichtig"] == 0.12
