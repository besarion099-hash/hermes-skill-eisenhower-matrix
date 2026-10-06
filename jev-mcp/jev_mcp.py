"""MCP-Server `jev`: Einschätzungen für die Eisenhower-Matrix über TypeSafes Jev.

Gibt nur Einschätzungen zurück und schreibt nie in die Matrix-Datei.
Ist Jev nicht nutzbar, kommt {"verfuegbar": False, ...} zurück, und Hermes arbeitet wie ohne Jev.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402

import jev_client as jc  # noqa: E402
import logik  # noqa: E402

server = MCPServer(
    name="jev",
    instructions=(
        "Einschätzungen für die Eisenhower-Matrix. Wie die Antworten zu verwenden sind "
        "(auch bei verfuegbar=false und melden=true), steht im Skill eisenhower-matrix."
    ),
)

_fehler_in_folge = 0
MELDEN_BEI = 3


def _fehlschlag(grund: str) -> dict:
    global _fehler_in_folge
    _fehler_in_folge += 1
    return {"verfuegbar": False, "grund": grund, "melden": _fehler_in_folge == MELDEN_BEI}


def _erfolg(urteil: dict) -> dict:
    """Erst wenn ein Werkzeug seine Felder gelesen hat, zählt der Aufruf als Erfolg."""
    global _fehler_in_folge
    _fehler_in_folge = 0
    return {"verfuegbar": True, **urteil}


def _frage(state, questions):
    """Gibt (antworten, None) oder (None, fehler-dict) zurück."""
    try:
        antworten = jc.frage(state, questions, schluessel=jc.lade_schluessel())
    except jc.JevFehler as e:
        return None, _fehlschlag(str(e))
    return antworten, None


@server.tool()
def einsortieren(aufgabe: str, leitziele: str = "", heute: str = "") -> dict:
    """Wie wichtig und wie dringend ist eine Aufgabe? Liefert Quadrant (Q1-Q4) und ob das Ergebnis sicher ist.

    aufgabe: die Aufgabe als ein Satz. leitziele: Text des Abschnitts 🎯 Leitziele (leer, wenn keine).
    heute: heutiges Datum YYYY-MM-DD.
    """
    antworten, fehler = _frage({"aufgabe": aufgabe, "leitziele": leitziele, "heute": heute},
                               jc.fragen_einsortieren())
    if fehler:
        return fehler
    try:
        urteil = logik.bewerte_einsortierung(antworten["wichtig"]["noul"], antworten["dringend"]["noul"])
    except (KeyError, TypeError):
        return _fehlschlag("unerwartete Antwort")
    return _erfolg(urteil)


@server.tool()
def zwei_minuten(aufgabe: str) -> dict:
    """Ist die Aufgabe in unter 2 Minuten erledigt? sofort_erledigen=true heißt: zum Sofort-Erledigen raten."""
    antworten, fehler = _frage({"aufgabe": aufgabe}, jc.fragen_zwei_minuten())
    if fehler:
        return fehler
    try:
        urteil = logik.bewerte_zwei_minuten(antworten["schnell"]["noul"])
    except (KeyError, TypeError):
        return _fehlschlag("unerwartete Antwort")
    return _erfolg(urteil)


@server.tool()
def rangfolge(aufgaben: list[str], leitziele: str = "") -> dict:
    """Sortiert Aufgaben danach, wie stark sie morgen die Leitziele voranbringen (wert 0-1, absteigend)."""
    if not aufgaben:
        return {"verfuegbar": True, "reihenfolge": []}
    antworten, fehler = _frage({"leitziele": leitziele}, jc.fragen_rangfolge(aufgaben))
    if fehler:
        return fehler
    try:
        paare = [(a, min(1.0, max(0.0, antworten[f"a{i}"]["score"] / (jc.STUFEN - 1))))
                 for i, a in enumerate(aufgaben)]
    except (KeyError, TypeError):
        return _fehlschlag("unerwartete Antwort")
    return _erfolg({"reihenfolge": logik.sortiere_rangfolge(paare)})


if __name__ == "__main__":
    server.run()
