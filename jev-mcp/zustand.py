"""Zustand der Matrix-Datei ausrechnen: Plan-Alter, Übertragungen, Fristen, Alter der Einträge.

Reine Buchhaltung ohne Jev und ohne Netz. Liest nur Text, schreibt nie.
Versteht beide Schreibweisen der Datei: `- [ ] Aufgabe (hinzugefügt: 2026-10-06)` und
`1. 📞 **Aufgabe** (hinzugefügt: 06.10.2026)`.
"""

import datetime as dt
import re

FEST_AB = 3  # so oft übertragen gilt eine Aufgabe als festsitzend
DRINGEND_TAGE = 7  # Frist in höchstens so vielen Tagen = dringend
Q4_ALT_TAGE = 30

_DATUM = r"(\d{4}-\d{2}-\d{2}|\d{1,2}\.\d{1,2}\.\d{4})"
_EINTRAG = re.compile(r"^\s*(?:[-*]\s+(?:\[[ xX]\]\s+)?|\d+\.\s+)(.+?)\s*$")
_ANMERKUNG = re.compile(r"\((?:hinzugefügt|bis|erledigt|übertragen|frist)\b[^)]*\)", re.IGNORECASE)
_SPALTEN = ("Q1", "Q2", "Q3", "Q4")


def datum(text: str | None) -> dt.date | None:
    if not text:
        return None
    try:
        if "-" in text:
            return dt.date.fromisoformat(text)
        tag, monat, jahr = (int(x) for x in text.split("."))
        return dt.date(jahr, monat, tag)
    except ValueError:
        return None


def _wert(zeile: str, schluessel: str) -> str | None:
    m = re.search(rf"\({schluessel}:?\s*{_DATUM}", zeile, re.IGNORECASE)
    return m.group(1) if m else None


def _name(roh: str) -> str:
    s = _ANMERKUNG.sub("", roh).replace("**", "").replace("✅", "").replace("🐸", "")
    while s and not s[0].isalnum():
        s = s[1:]
    return s.strip()


def _abschnitt(ueberschrift: str) -> str | None:
    if "Heute" in ueberschrift:
        return "heute"
    if "Leitziele" in ueberschrift:
        return "leitziele"
    if "Erledigt" in ueberschrift or "Archiv" in ueberschrift:
        return "archiv"
    for q in _SPALTEN:
        if re.search(rf"\b{q}\b", ueberschrift):
            return q
    return None


def zerlege(text: str) -> tuple[dict, str | None]:
    """Gibt ({abschnitt: [roh-zeilen]}, heute-datum-text) zurück."""
    teile: dict[str, list[str]] = {}
    plan_datum = None
    aktuell = None
    for zeile in text.splitlines():
        if zeile.startswith("## "):
            aktuell = _abschnitt(zeile)
            if aktuell == "heute":
                m = re.search(rf"\({_DATUM}\)", zeile)
                plan_datum = m.group(1) if m else None
            continue
        if aktuell is None:
            continue
        m = _EINTRAG.match(zeile)
        if m:
            teile.setdefault(aktuell, []).append(m.group(1))
    return teile, plan_datum


def aufgaben(text: str) -> list[dict]:
    """Alle offenen Einträge aus Q1–Q4."""
    teile, _ = zerlege(text)
    liste = []
    for q in _SPALTEN:
        for roh in teile.get(q, []):
            liste.append({
                "aufgabe": _name(roh),
                "quadrant": q,
                "hinzugefuegt": datum(_wert(roh, "hinzugefügt")),
                "frist": datum(_wert(roh, "bis") or _wert(roh, "frist")),
            })
    return liste


def pruefe(text: str, heute: str) -> dict:
    tag = datum(heute)
    if tag is None or "-" not in heute:
        return {"fehler": "heute muss YYYY-MM-DD sein"}
    teile, plan_text = zerlege(text)

    plan_tag = datum(plan_text)
    offen, erledigt, festsitzend = [], [], []
    for roh in teile.get("heute", []) if plan_tag else []:
        name = _name(roh)
        if "✅" in roh:
            erledigt.append(name)
            continue
        m = re.search(r"\(übertragen:\s*(\d+)", roh, re.IGNORECASE)
        # Ein liegengebliebener Plan zählt wie tägliches Übertragen, auch ohne Zähler in der Datei.
        n = max(int(m.group(1)) if m else 0, (tag - plan_tag).days)
        offen.append({"aufgabe": name, "uebertragen": n})
        if n >= FEST_AB:
            festsitzend.append({"aufgabe": name, "uebertragen": n})
    plan = {
        "datum": plan_tag.isoformat() if plan_tag else None,
        "veraltet": plan_tag is None or plan_tag < tag,
        "tage_alt": (tag - plan_tag).days if plan_tag else None,
        "offen": offen,
        "erledigt": erledigt,
    }

    jetzt_dringend, ueberfaellig, q1_ohne_frist_alt, q4_alt = [], [], [], []
    liste = aufgaben(text)
    for a in liste:
        if a["frist"]:
            rest = (a["frist"] - tag).days
            eintrag = {"aufgabe": a["aufgabe"], "quadrant": a["quadrant"],
                       "frist": a["frist"].isoformat(), "tage_bis_frist": rest}
            if rest < 0:
                ueberfaellig.append(eintrag)
            elif rest <= DRINGEND_TAGE and a["quadrant"] in ("Q2", "Q4"):
                jetzt_dringend.append({**eintrag, "neuer_quadrant": "Q1" if a["quadrant"] == "Q2" else "Q3"})
        alt = (tag - a["hinzugefuegt"]).days if a["hinzugefuegt"] else None
        if a["quadrant"] == "Q1" and not a["frist"] and alt is not None and alt > DRINGEND_TAGE:
            q1_ohne_frist_alt.append({"aufgabe": a["aufgabe"], "tage_alt": alt})
        if a["quadrant"] == "Q4" and alt is not None and alt > Q4_ALT_TAGE:
            q4_alt.append({"aufgabe": a["aufgabe"], "tage_alt": alt})

    woche = []
    for roh in teile.get("archiv", []):
        fertig = datum(_wert(roh, "erledigt"))
        if fertig and 0 <= (tag - fertig).days < 7:
            woche.append(_name(roh))

    return {
        "heute": tag.isoformat(),
        "plan": plan,
        "festsitzend": festsitzend,
        "jetzt_dringend": jetzt_dringend,
        "ueberfaellig": ueberfaellig,
        "q1_ohne_frist_alt": q1_ohne_frist_alt,
        "q1_anzahl": sum(1 for a in liste if a["quadrant"] == "Q1"),
        "q4_alt": q4_alt,
        "leitziele": [_name(r) for r in teile.get("leitziele", [])],
        "erledigt_letzte_7_tage": woche,
    }
