# tests/test_zustand.py
import zustand

BEISPIEL = """---
type: matrix
---
# Eisenhower-Matrix
|Zuletzt aktualisiert: 06.10.2026

## 🐸 Heute (2026-09-18)

1. 🐸 ☎️ **Versicherung anrufen** (übertragen: 3×)
2. 💼 **Bewerbung schreiben** ✅
3. 💳 **Bank anrufen** (übertragen: 1×)

## 🎯 Leitziele (Jahreskompass)

1. 💼 **Gesünder leben**
2. 🗣️ **Spanisch lernen**

## 🔴 Q1 — Dringend & wichtig (sofort erledigen)

1. ☎️ **Versicherung anrufen** (hinzugefügt: 06.07.2026)
2. 🧾 **Steuer zahlen** (hinzugefügt: 2026-10-01) (bis 2026-10-09)

## 🟡 Q2 — Wichtig, nicht dringend (einplanen)

1. 🏠 **Vermieter anrufen** (hinzugefügt: 09.07.2026)
- [ ] Pass verlängern (hinzugefügt: 2026-09-01) (bis 10.10.2026)
- [ ] Rechnung zahlen (hinzugefügt: 2026-09-01) (bis 2026-10-01)

## 🔵 Q3 — Dringend, nicht wichtig (delegieren / schnell weg)

_(leer – nichts offen ✅)_

## ⚪ Q4 — Weder noch (streichen oder irgendwann)

1. 🎲 **Neues Brettspiel testen** (hinzugefügt: 09.07.2026)
- [ ] Neues Hobby (hinzugefügt: 2026-10-01)

## ✅ Erledigt (Archiv)

- [x] Geld abheben (erledigt: 06.07.2026)
- [x] Fenster putzen (erledigt: 2026-10-02)
- [x] Regal kaufen (erledigt: 14.09.2026, Lieferung: 16.09.2026)
"""


def _z(text=BEISPIEL, heute="2026-10-06"):
    return zustand.pruefe(text, heute)


def namen(liste):
    return [e["aufgabe"] for e in liste]


def test_plan_veraltet_mit_offenen_und_erledigten():
    plan = _z()["plan"]
    assert plan["datum"] == "2026-09-18"
    assert plan["veraltet"] is True
    assert plan["tage_alt"] == 18
    assert plan["offen"] == [{"aufgabe": "Versicherung anrufen", "uebertragen": 18},
                             {"aufgabe": "Bank anrufen", "uebertragen": 18}]
    assert plan["erledigt"] == ["Bewerbung schreiben"]


def test_plan_von_heute_ist_nicht_veraltet():
    plan = _z(heute="2026-09-18")["plan"]
    assert plan["veraltet"] is False and plan["tage_alt"] == 0


def test_ohne_heute_abschnitt():
    plan = _z(BEISPIEL.replace("## 🐸 Heute (2026-09-18)", "## Notizen"))["plan"]
    assert plan == {"datum": None, "veraltet": True, "tage_alt": None, "offen": [], "erledigt": []}


def test_festsitzend_ab_drei_uebertragungen():
    assert _z(heute="2026-09-19")["festsitzend"] == [{"aufgabe": "Versicherung anrufen", "uebertragen": 3}]


def test_liegengebliebener_plan_zaehlt_als_uebertragen():
    assert _z()["festsitzend"] == [{"aufgabe": "Versicherung anrufen", "uebertragen": 18},
                                   {"aufgabe": "Bank anrufen", "uebertragen": 18}]


def test_frist_bald_macht_dringend_und_ueberfaellig():
    z = _z()
    assert z["jetzt_dringend"] == [{"aufgabe": "Pass verlängern", "quadrant": "Q2", "frist": "2026-10-10",
                                    "tage_bis_frist": 4, "neuer_quadrant": "Q1"}]
    assert z["ueberfaellig"] == [{"aufgabe": "Rechnung zahlen", "quadrant": "Q2", "frist": "2026-10-01",
                                  "tage_bis_frist": -5}]


def test_q1_ohne_frist_zu_lange():
    z = _z()
    assert z["q1_ohne_frist_alt"] == [{"aufgabe": "Versicherung anrufen", "tage_alt": 92}]
    assert z["q1_anzahl"] == 2


def test_q4_alt_nur_ueber_30_tage():
    assert namen(_z()["q4_alt"]) == ["Neues Brettspiel testen"]


def test_leitziele_und_wochenbilanz():
    z = _z()
    assert z["leitziele"] == ["Gesünder leben", "Spanisch lernen"]
    assert z["erledigt_letzte_7_tage"] == ["Fenster putzen"]


def test_platzhalter_wird_ignoriert():
    assert "Q3" not in [e["quadrant"] for e in zustand.aufgaben(BEISPIEL)]


def test_falsches_datum_wird_abgelehnt():
    r = zustand.pruefe(BEISPIEL, "morgen")
    assert r["fehler"] == "heute muss YYYY-MM-DD sein"
