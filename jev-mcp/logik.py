"""Entscheidungslogik: aus Jev-Wahrscheinlichkeiten werden Quadrant und Urteil.

Die Schwellen stehen nur hier. Hermes bekommt das fertige Urteil.
"""

UNTEN = 0.35  # darunter: sicher "nein"
OBEN = 0.65  # darüber: sicher "ja"
SCHNELL_AB = 0.8  # ab hier: "mach's gleich"


def ist_unklar(p: float) -> bool:
    return UNTEN <= p <= OBEN


def quadrant(wichtig: float, dringend: float) -> str:
    w = wichtig >= 0.5
    d = dringend >= 0.5
    if w and d:
        return "Q1"
    if w:
        return "Q2"
    if d:
        return "Q3"
    return "Q4"


def bewerte_einsortierung(wichtig: float, dringend: float) -> dict:
    unklar = [name for name, p in (("wichtig", wichtig), ("dringend", dringend)) if ist_unklar(p)]
    return {
        "wichtig": round(wichtig, 2),
        "dringend": round(dringend, 2),
        "quadrant": quadrant(wichtig, dringend),
        "sicher": not unklar,
        "unklar": unklar,
    }


def bewerte_zwei_minuten(schnell: float) -> dict:
    return {"schnell": round(schnell, 2), "sofort_erledigen": schnell >= SCHNELL_AB}


def sortiere_rangfolge(paare: list[tuple[str, float]]) -> list[dict]:
    geordnet = sorted(paare, key=lambda p: p[1], reverse=True)
    return [{"aufgabe": a, "wert": round(w, 2)} for a, w in geordnet]
