---
name: eisenhower-matrix
description: Capture tasks from text, images, or voice notes; suggest an urgency/importance quadrant with reasoning; keep a persistent Eisenhower matrix shown compactly in chat or as an HTML file.
version: 1.1.0
author: Besarion
metadata:
  hermes:
    tags: [productivity, tasks, prioritization]
    category: productivity
    config:
      - key: eisenhower.file
        description: "Pfad zur Matrix-Datei — absolut oder relativ zum Hermes-Home (HERMES_HOME)"
        default: "workspace/eisenhower.md"
---

# Eisenhower-Matrix

Persönlicher Priorisierungs-Assistent nach der Eisenhower-Methode. Aufgaben kommen als Text, Bild oder Sprachnachricht herein; du analysierst sie, schlägst einen Quadranten begründet vor und pflegst eine dauerhafte Matrix-Datei.

## When to Use

- Nachrichten wie „Notiz: …", „ich muss noch …", „neue Aufgabe: …", „merk dir: …"
- Bilder mit Aufgabenbezug (Rechnung, Terminbrief, handschriftliche Liste)
- Sprachnachrichten mit Erledigungen oder Erinnerungen
- „zeig meine Matrix", „was steht an", „meine Prioritäten"
- „X erledigt", „verschieb X", „streich X", „räum die Matrix auf"
- Explizit: `/eisenhower-matrix …`

## Quick Reference

- Matrix-Datei: Config-Key `eisenhower.file`; relative Pfade ab dem Hermes-Home (HERMES_HOME) auflösen, absolute Pfade unverändert nutzen. Standard: `workspace/eisenhower.md`
- Tipp: Zeigt `eisenhower.file` in einen Obsidian-Vault (z. B. `obsidian-vault/Eisenhower-Matrix.md`), erscheint die Matrix automatisch als Notiz in Obsidian
- Fehlt die Datei: aus `templates/eisenhower.md` anlegen und Nutzer kurz informieren
- Quadranten: 🔴 Q1 dringend & wichtig (sofort) · 🟡 Q2 wichtig, nicht dringend (einplanen) · 🔵 Q3 dringend, nicht wichtig (delegieren) · ⚪ Q4 weder noch (streichen/irgendwann) · ✅ Erledigt (Archiv)
- Einstufungsregeln und Beispiele: `references/classification-guide.md`
- HTML-Ansicht: `templates/eisenhower.html` befüllen (Platzhalter `<!--Q1_ITEMS-->` … `<!--Q4_ITEMS-->`, `<!--UPDATED-->`)
- Erinnerungs-Routine gewünscht? Anleitung in `references/cron-setup.md` — niemals ungefragt einrichten

## Procedure

### A. Aufgabe erfassen

1. Eingabe analysieren:
   - **Text:** Aufgabe(n) direkt extrahieren.
   - **Bild:** Kurz benennen, was du erkennst („Rechnung von Stadtwerke, fällig 15.07."), daraus die Aufgabe ableiten.
   - **Sprachnachricht:** Aus der Transkription die Aufgabe(n) extrahieren.
2. Quadranten **vorschlagen** (Standardweg), mit Ein-Satz-Begründung. Regeln: `references/classification-guide.md`. Format:
   > „Ich habe notiert: *<Aufgabe>*. Mein Vorschlag: <Emoji> <Q?> — <Begründung>. Passt das? (ja / oder 1–4 für einen anderen Quadranten)"
3. Antwort auswerten: „ja"/👍 → speichern; Zahl 1–4 oder freie Formulierung → Korrektur übernehmen.
4. Nur wenn keine belastbare Einschätzung möglich ist: offene Frage ohne Vorschlag —
   1️⃣ dringend & wichtig · 2️⃣ wichtig, nicht dringend · 3️⃣ dringend, nicht wichtig · 4️⃣ weder noch
5. Speichern: Zeile `- [ ] <Aufgabe> (hinzugefügt: <YYYY-MM-DD>)` in den Quadranten-Abschnitt einfügen; Deadline in Klammern ergänzen, falls bekannt („bis <YYYY-MM-DD>"). `Zuletzt aktualisiert` im Kopf aktualisieren. Gezielte Edits — die Datei nie komplett überschreiben.
6. Bestätigen: ein Satz mit Quadrant und Handlungsempfehlung (Q1 sofort, Q2 einplanen, Q3 delegieren, Q4 streichen/irgendwann).
7. **Mehrere Aufgaben in einer Eingabe:** alle mit je einem Vorschlag auflisten, EINE gesammelte Bestätigung einholen.

### B. Matrix anzeigen

1. Standard (Chat/Telegram): kompakte Textliste je Quadrant mit Emoji-Marker; leere Quadranten als „—"; bei >10 Einträgen pro Quadrant nur die ersten 10 plus „(+n weitere)".
2. Auf Wunsch („als Datei", „schön formatiert"): `templates/eisenhower.html` kopieren, Platzhalter mit `<li>`-Einträgen befüllen, im Workspace speichern (z. B. `eisenhower-<YYYY-MM-DD>.html`) und über den aktiven Kanal als Datei senden.

### C. Matrix pflegen

- **Abhaken** („X erledigt"): Zeile als `- [x] <Aufgabe> (erledigt: <YYYY-MM-DD>)` ins Archiv verschieben.
- **Verschieben** („das ist jetzt dringend"): Zeile in den anderen Quadranten-Abschnitt bewegen.
- **Löschen** („streich X"): einzige destruktive Aktion — erst rückbestätigen, dann Zeile entfernen.
- **Aufräumen:** Kandidaten nennen (Q4-Einträge älter als 30 Tage, überfällige Deadlines) und fragen, was damit geschehen soll.
- Bei mehrdeutiger Referenz („das ist erledigt" bei mehreren offenen Aufgaben): nachfragen, nie raten.

## Pitfalls

- Matrix-Datei unlesbar/fremdes Format → NICHT überschreiben; Nutzer fragen (reparieren vs. neu anlegen), vorher Kopie als `eisenhower.md.bak` sichern.
- Unklare Antwort auf die Einstufungsfrage → einmal präzisierend nachfragen; danach Q2 als sicherer Standard mit Hinweis, dass es korrigierbar ist.
- Keine Aufgabe erkennbar (Text, Bild oder Sprache) → sagen, was erkannt wurde, und fragen, ob/was gespeichert werden soll — nichts erfinden.
- Bild/Audio ohne verwertbaren Inhalt (kein Vision/Transkript im Setup) → ehrlich sagen und um Textfassung bitten.
- Nutzer bearbeitet die Datei auch von Hand → Abschnittsüberschriften und Checkbox-Format respektieren, unbekannte Zusatznotizen stehen lassen.

## Verification

- Neue Text-Notiz → Vorschlag mit Begründung → „ja" → Eintrag steht mit Datum im vorgeschlagenen Quadranten.
- Foto einer Rechnung mit Frist → extrahierte Aufgabe samt Deadline und passendem Quadrant-Vorschlag.
- „zeig meine Matrix" → 4 Quadranten kompakt im Chat, leere als „—".
- „X erledigt" → Eintrag im Archiv mit Erledigt-Datum, nicht mehr im Quadranten.
- „als Datei" → HTML-Datei erzeugt und versendet, öffnet als 2×2-Grid im Browser.
- Vage Notiz ohne Prioritätssignale → offene 1–4-Frage statt erfundenem Vorschlag.
