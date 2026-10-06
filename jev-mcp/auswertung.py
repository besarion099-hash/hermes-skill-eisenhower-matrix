"""Live-Test: 15 Beispielaufgaben gegen Jev. Erfolg = mindestens 12 richtig eingeordnet."""

import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import jev_mcp  # noqa: E402

LEITZIELE = sys.argv[1] if len(sys.argv) > 1 else "1. gesund bleiben 2. finanziell abgesichert sein 3. Englisch lernen"
heute = datetime.date.today().isoformat()
beispiele = json.loads((pathlib.Path(__file__).parent / "beispiele.json").read_text(encoding="utf-8"))

richtig = unklar = zm_treffer = zm_gesamt = 0
for b in beispiele:
    r = jev_mcp.einsortieren(b["aufgabe"], leitziele=LEITZIELE, heute=heute)
    if not r["verfuegbar"]:
        print(f"ABBRUCH: Jev nicht verfügbar ({r['grund']})")
        sys.exit(2)
    ok = r["quadrant"] == b["soll"]
    richtig += ok
    unklar += not r["sicher"]
    zm = ""
    if "zwei_min" in b:
        z = jev_mcp.zwei_minuten(b["aufgabe"])
        zm_gesamt += 1
        zm_treffer += z.get("sofort_erledigen") == b["zwei_min"]
        zm = f" · 2min {z.get('schnell')}"
    print(f"{'OK ' if ok else 'XX '}{r['quadrant']} (soll {b['soll']}) w={r['wichtig']} d={r['dringend']}"
          f"{' UNKLAR ' + ','.join(r['unklar']) if r['unklar'] else ''}{zm} · {b['aufgabe']}")

print(f"\nrichtig: {richtig}/{len(beispiele)} · unklar: {unklar}/{len(beispiele)} · 2-Min-Treffer: {zm_treffer}/{zm_gesamt}")
sys.exit(0 if richtig >= 12 else 1)
