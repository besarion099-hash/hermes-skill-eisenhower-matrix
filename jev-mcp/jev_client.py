"""Aufrufe an TypeSafes Jev (System One API). Schreibt nichts, gibt nie den Schlüssel aus."""

import os
import pathlib
import sys

import httpx

API_URL = "https://api.typesafe.ai/v1/systemone"
MODELL = "jev-latest"
ZEITLIMIT = 3.0
SCHLUESSEL_DATEI = pathlib.Path.home() / ".typesafe_api_key"
STUFEN = 4


class JevFehler(Exception):
    """Jev nicht nutzbar: kein Schlüssel, nicht erreichbar oder falsche Antwort."""


def lade_schluessel(datei: pathlib.Path = SCHLUESSEL_DATEI) -> str:
    schluessel = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if not schluessel:
        try:
            schluessel = datei.read_text(encoding="utf-8-sig").strip()
        except (OSError, UnicodeError):
            schluessel = ""
    # Nicht-ASCII (z. B. Reste einer UTF-16-Datei) würde später httpx beim Senden abstürzen lassen.
    # Die Meldung nennt nie den Schlüsseltext.
    if not schluessel or not schluessel.isascii():
        raise JevFehler("kein Schlüssel")
    return schluessel


def frage(state, questions: dict, *, schluessel: str, client: httpx.Client | None = None) -> dict:
    body = {"state": state, "model": MODELL, "questions": questions}
    c = client or httpx.Client(timeout=ZEITLIMIT)
    try:
        antwort = c.post(API_URL, json=body, headers={"Authorization": f"Bearer {schluessel}"})
    except httpx.HTTPError as e:
        raise JevFehler(f"nicht erreichbar ({type(e).__name__})") from e
    finally:
        if client is None:
            c.close()
    if antwort.status_code != 200:
        raise JevFehler(f"HTTP {antwort.status_code}")
    try:
        antworten = antwort.json()["answers"]
    except (ValueError, KeyError, TypeError) as e:
        raise JevFehler("unerwartete Antwort") from e
    if not isinstance(antworten, dict):
        raise JevFehler("unerwartete Antwort")
    return antworten


def fragen_einsortieren() -> dict:
    return {
        "wichtig": {
            "type": "noul",
            "instructions": (
                "Is `aufgabe` important for this person: does it advance one of the goals in "
                "`leitziele`, or avoid real harm to health, money, family, home or legal duties?"
            ),
            "criteria": {
                "true": "Advances a goal or prevents real harm if left undone",
                "false": "Little effect on goals or wellbeing if it never gets done",
            },
        },
        "dringend": {
            "type": "noul",
            "instructions": (
                "Must `aufgabe` be done within the next 7 days from `heute` "
                "(deadline, appointment, or clear consequences of waiting)?"
            ),
            "criteria": {
                "true": "Deadline or consequences within 7 days",
                "false": "Can wait longer than 7 days without consequences",
            },
        },
    }


def fragen_zwei_minuten() -> dict:
    return {
        "schnell": {
            "type": "noul",
            "instructions": (
                "Can one person finish `aufgabe` completely in under 2 minutes, "
                "right now, without preparation, travel or waiting for others?"
            ),
        }
    }


def fragen_rangfolge(aufgaben: list[str]) -> dict:
    stufen = [
        "No contribution to the goals in `leitziele`",
        "Small contribution",
        "Clear contribution",
        "Major contribution to one of the goals",
    ]
    return {
        f"a{i}": {
            "type": "score",
            "instructions": {
                "aufgabe": aufgabe,
                "question": "How much does doing `aufgabe` tomorrow advance the goals in `leitziele`?",
            },
            "criteria": stufen,
        }
        for i, aufgabe in enumerate(aufgaben)
    }


def _verbindungstest() -> int:
    try:
        antworten = frage("Steuererklärung bis morgen abgeben", fragen_zwei_minuten(),
                          schluessel=lade_schluessel())
        wert = f"{antworten['schnell']['noul']:.2f}"
    except JevFehler as e:
        print(f"Jev NICHT erreichbar: {e}")
        return 1
    except (KeyError, TypeError, ValueError):
        print("Jev NICHT erreichbar: unerwartete Antwort")
        return 1
    print(f"Jev erreichbar. Testantwort: {wert}")
    return 0


if __name__ == "__main__" and "--test" in sys.argv:
    sys.exit(_verbindungstest())
