# eisenhower-matrix — Hermes-Agent-Skill (v2.3)

*Deutsch | [English below ⬇](#english)*

![Projekt-Übersicht (Deutsch)](docs/projekt-uebersicht-de.png)

Persönliches **Produktivitätssystem aus 5 Methoden** für den [Hermes Agent](https://hermes-agent.nousresearch.com/) — die Methoden greifen wie ein Fließband ineinander, statt sich zu widersprechen:

| Station | Methode | Frage |
|---|---|---|
| 1. Erfassen | **2-Minuten-Regel** | Unter 2 Minuten? Sofort machen, nicht speichern |
| 2. Sortieren | **Eisenhower-Matrix** | Muss ICH das tun — und wann? |
| 3. Gewichten | **Pareto 80/20** | Welche Aufgaben bringen den größten Effekt? |
| 4. Tagesplan | **Ivy Lee** | Abends max. 6 Aufgaben für morgen wählen |
| 5. Ausführen | **Eat That Frog** | Morgens mit Aufgabe Nr. 1 (dem 🐸 Frosch) starten |

## Funktionen

- 📥 **Erfassen:** Notiz schicken — als Text, Foto (Rechnung, Brief, Liste) oder Sprachnachricht; Kleinkram unter 2 Minuten wird gar nicht erst gespeichert, sondern gleich erledigt
- 🤖 **KI-Vorschlag:** Hermes schlägt einen Quadranten mit Begründung vor — bestätigen mit „ja" oder korrigieren mit 1–4
- 🎯 **Leitziele:** Bis zu 3 persönliche Jahresziele in der Matrix-Datei machen aus „ist das wichtig?" die klare Frage „zahlt das auf Ziel 1–3 ein?" — der Maßstab für Einstufung UND Abendplanung
- 🌙 **Abendplanung (Ivy Lee):** „plane meinen Tag" → max. 6 Aufgaben für morgen, Übertrag zuerst, mindestens 2 wichtige-nicht-dringende (Pareto-Schutz), Frosch auf Platz 1
- 🐸 **Morgen-Frosch:** „was ist mein Frosch?" → die wichtigste & unangenehmste Aufgabe zuerst — kein Kleinkram vor dem Frosch
- 🗂️ **Dauerhafte Matrix:** Alle Aufgaben in einer Markdown-Datei (funktioniert wunderbar in einem Obsidian-Vault), Tagesplan als „🐸 Heute"-Abschnitt obendrauf
- 👀 **Ansehen:** „zeig meine Matrix" → kompakte Übersicht im Chat; „als Datei" → HTML-Ansicht (Heute-Band + 2×2-Grid)
- ✅ **Pflegen in normaler Sprache:** „X erledigt", „verschieb X", „streich X", „Tag abschließen"
- ⏰ **Optional:** fester Tagesrhythmus per Hermes-Cron (z. B. 18:00 Abendplanung, 7:00 Frosch) — wird nie automatisch eingerichtet

## Die 4 Konfliktregeln

Damit die 5 Methoden harmonieren statt konkurrieren:

1. Die 2-Minuten-Regel gilt nur beim **Erfassen** — nie als Start in den Tag (sonst frisst Kleinkram den Frosch-Morgen).
2. Mindestens **2 der 6 Tagesplätze** gehören Q2-Aufgaben (sonst gewinnt immer das Dringende).
3. Unerledigtes wandert **kommentarlos als Übertrag** an die Spitze des nächsten Tagesplans.
4. Q3/Q4 belegen **nie** Tagesplan-Plätze.

## Installation

1. Diesen Ordner (`eisenhower-matrix/`) in das Skills-Verzeichnis deines Hermes kopieren:
   - **Linux/macOS:** `~/.hermes/skills/productivity/eisenhower-matrix/`
   - **Windows:** `%USERPROFILE%\.hermes\skills\productivity\eisenhower-matrix\`
   - **Docker:** in den Daten-Ordner, der als Hermes-Home gemountet ist, z. B. `<datenordner>/skills/productivity/eisenhower-matrix/`
2. Prüfen: `hermes skills list` → `eisenhower-matrix` muss erscheinen.
3. Loslegen: eine Notiz schicken — die Matrix-Datei wird beim ersten Einsatz automatisch angelegt.

Der Skill funktioniert auch in anderen Agenten (z. B. Claude Code): Ordner ins jeweilige Skills-Verzeichnis kopieren und in `SKILL.md` den Pfad zur Matrix-Datei anpassen.

## Konfiguration (optional)

Speicherort der Matrix-Datei über den Config-Key `eisenhower.file` ändern (absolut oder relativ zum Hermes-Home; Standard `workspace/eisenhower.md`):

```
hermes config set eisenhower.file "obsidian-vault/Eisenhower-Matrix.md"
```

💡 Zeigt der Pfad in einen Obsidian-Vault, erscheint die Matrix automatisch als Notiz in Obsidian.

## Ordnerstruktur

```
eisenhower-matrix/
├── SKILL.md                      # Verhaltensanleitung (5-Methoden-System)
├── templates/
│   ├── eisenhower.md             # Vorlage der Matrix-Datei (mit 🐸 Heute-Abschnitt)
│   └── eisenhower.html           # HTML-Ansicht (Heute-Band + 2×2-Grid)
├── references/
│   ├── classification-guide.md   # Eisenhower-Einstufungsregeln + Beispiele
│   ├── tagesplan-guide.md        # Ivy Lee, Pareto & Frosch-Wahl
│   └── cron-setup.md             # Tagesrhythmus-Routinen (18:00 / 7:00)
├── jev-mcp/                      # optionaler MCP-Server für Jev
└── README.md
```

Alles ist reines Markdown/HTML und direkt editierbar. Der Skill selbst braucht keine Skripte; nur die optionale Jev-Anbindung bringt einen kleinen Python-Server mit.

## Optional: Jev (TypeSafe)

Ab 2.3.0 hat das System einen Rückkanal: Jede Abendplanung fragt zuerst, was erledigt ist. Aufgaben, die dreimal übertragen wurden, werden in einen kleinen ersten Schritt zerlegt. Fristen werden jeden Abend neu geprüft (Q2 wird Q1, sobald die Frist näher als 7 Tage ist), und sonntags gibt es einen kurzen Wochenrückblick mit einem nächsten Schritt pro vernachlässigtem Leitziel. Das Rechnen (Plan-Alter, Übertragungen, Fristen) übernimmt das Werkzeug `zustand_pruefen` im Ordner `jev-mcp/`. Es läuft lokal und schickt nichts ins Netz.

Ab 2.2.0 kann Hermes Aufgaben mit TypeSafes Entscheidungsmodell Jev einsortieren (Ordner `jev-mcp/`, MCP-Server `jev`). Eindeutige Fälle trägt Hermes direkt ein, bei unklaren fragt er nach. Ohne Jev läuft alles wie bisher. Einrichtung: Schlüssel mit `jev-mcp/schluessel_eintragen.py` speichern und den Server in der Hermes-Konfiguration unter `mcp_servers` als `jev` eintragen (`command`: Python des Hermes-venv, `args`: Pfad zu `jev-mcp/jev_mcp.py`). Datenschutz: Aufgabentext, Datum und Leitziele werden dafür an api.typesafe.ai geschickt. Nach Updates von Hermes mit `hermes mcp test jev` prüfen, ob der Server noch lädt — fehlt er, arbeitet der Skill still ohne Jev weiter.

---

<a name="english"></a>

# eisenhower-matrix — Hermes Agent Skill (v2.3, English)

![Project overview (English)](docs/project-overview-en.png)

A personal **5-method productivity system** for the [Hermes Agent](https://hermes-agent.nousresearch.com/) — the methods work as one pipeline instead of competing:

| Stage | Method | Question |
|---|---|---|
| 1. Capture | **2-minute rule** | Under 2 minutes? Do it now, don't store it |
| 2. Sort | **Eisenhower matrix** | Do I have to do this — and when? |
| 3. Weigh | **Pareto 80/20** | Which tasks create the biggest impact? |
| 4. Daily plan | **Ivy Lee** | Pick max. 6 tasks for tomorrow, every evening |
| 5. Execute | **Eat That Frog** | Start the morning with task #1 (the 🐸 frog) |

## Features

- 📥 **Capture:** send a note — text, photo (invoice, letter, list), or voice message; anything under 2 minutes is done immediately instead of stored
- 🤖 **AI suggestion:** Hermes proposes a quadrant with a one-sentence reason — confirm with "yes" or correct with 1–4
- 🎯 **Guiding goals:** up to 3 personal yearly goals in the matrix file turn "is this important?" into the clear question "does it advance goal 1–3?" — the benchmark for classification AND evening planning
- 🌙 **Evening planning (Ivy Lee):** "plan my day" → max. 6 tasks for tomorrow, carry-over first, at least 2 important-not-urgent ones (Pareto guard), frog in slot 1
- 🐸 **Morning frog:** "what's my frog?" → the most important & most unpleasant task first — no small stuff before the frog
- 🗂️ **Persistent matrix:** all tasks in one Markdown file (works beautifully inside an Obsidian vault), with the daily plan as a "🐸 Today" section on top
- 👀 **View:** "show my matrix" → compact overview in chat; "as a file" → HTML view (today band + 2×2 grid)
- ✅ **Maintain in plain language:** "X is done", "move X", "delete X", "close the day"
- ⏰ **Optional:** fixed daily rhythm via Hermes cron (e.g. 6 pm planning, 7 am frog) — never set up automatically

## The 4 conflict rules

So the 5 methods harmonize instead of competing:

1. The 2-minute rule applies only at **capture time** — never as the way to start the day.
2. At least **2 of the 6 daily slots** go to Q2 tasks (otherwise the urgent always wins).
3. Unfinished tasks **carry over without comment** to the top of the next daily plan.
4. Q3/Q4 **never** occupy daily-plan slots.

## Installation

1. Copy this folder (`eisenhower-matrix/`) into your Hermes skills directory:
   - **Linux/macOS:** `~/.hermes/skills/productivity/eisenhower-matrix/`
   - **Windows:** `%USERPROFILE%\.hermes\skills\productivity\eisenhower-matrix\`
   - **Docker:** into the data folder mounted as the Hermes home, e.g. `<data-dir>/skills/productivity/eisenhower-matrix/`
2. Verify: `hermes skills list` → `eisenhower-matrix` should appear.
3. Start: just send a note — the matrix file is created automatically on first use.

The skill also works in other agents (e.g. Claude Code): copy the folder into that agent's skills directory and adjust the matrix file path in `SKILL.md`.

## Configuration (optional)

Change where the matrix file is stored via the `eisenhower.file` config key (absolute, or relative to the Hermes home; default `workspace/eisenhower.md`):

```
hermes config set eisenhower.file "obsidian-vault/Eisenhower-Matrix.md"
```

💡 Point the path into an Obsidian vault and the matrix automatically shows up as a note in Obsidian.

## Folder structure

Same as above, including the `jev-mcp/` folder (optional MCP server for Jev). Everything is plain Markdown/HTML and directly editable. The skill itself needs no scripts; only the optional Jev connection ships a small Python server.

## Optional: Jev (TypeSafe)

Since 2.3.0 the system has a feedback loop: every evening planning first asks what got done. Tasks carried over three times are broken down into a tiny first step. Deadlines are re-checked every evening (Q2 becomes Q1 once the deadline is less than 7 days away), and on Sundays there is a short weekly review with one next step per neglected goal. The bookkeeping (plan age, carry-overs, deadlines) is done by the tool `zustand_pruefen` in `jev-mcp/`. It runs locally and sends nothing over the network.

Since 2.2.0, Hermes can classify tasks with TypeSafe's decision model Jev (folder `jev-mcp/`, MCP server `jev`). Clear-cut cases are filed directly, and Hermes asks only when something is unclear. Without Jev everything works as before. Setup: store the key with `jev-mcp/schluessel_eintragen.py` and register the server in the Hermes configuration under `mcp_servers` as `jev` (`command`: Python of the Hermes venv, `args`: path to `jev-mcp/jev_mcp.py`). Privacy: task text, date and goals are sent to api.typesafe.ai. After Hermes updates, run `hermes mcp test jev` to check the server still loads — if it is missing, the skill silently works without Jev.

---

**Autor / Author:** Besarion · Erstellt mit / Created with Claude · Lizenz / License: MIT
