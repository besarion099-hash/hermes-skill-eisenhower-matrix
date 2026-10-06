---
name: eisenhower-matrix
description: Persönliches Produktivitätssystem aus 5 Methoden — Aufgaben erfassen (2-Minuten-Filter), nach Eisenhower sortieren, per Pareto gewichten, abends max. 6 Tagesaufgaben wählen (Ivy Lee) und morgens mit dem Frosch starten (Eat That Frog). Eine dauerhafte Matrix-Datei, kompakt im Chat oder als HTML.
version: 2.3.0
author: Besarion
metadata:
  hermes:
    tags: [productivity, tasks, prioritization, daily-planning]
    category: productivity
    config:
      - key: eisenhower.file
        description: "Pfad zur Matrix-Datei — absolut oder relativ zum Hermes-Home (HERMES_HOME)"
        default: "workspace/eisenhower.md"
---

# Eisenhower-Matrix — das 5-Methoden-Produktivitätssystem

Persönlicher Priorisierungs-Assistent. Fünf Methoden greifen wie ein Fließband ineinander:

**Erfassen (2-Minuten-Filter) → Sortieren (Eisenhower) → Gewichten (Pareto 80/20) → Tagesplan (Ivy Lee, max. 6) → Ausführen (Frosch zuerst).**

Aufgaben kommen als Text, Bild oder Sprachnachricht herein; du analysierst sie, schlägst einen Quadranten begründet vor und pflegst eine dauerhafte Matrix-Datei. Abends fragst du zuerst, was erledigt ist, und hilfst dann, die 6 Aufgaben für morgen zu wählen; morgens nennst du den Frosch.

**Der Rückkanal hält das Fließband in Gang:** Ohne Rückmeldung („was ist erledigt?") wird jeden Tag dieselbe Liste übertragen. Deshalb beginnt jede Abendplanung mit der Rückfrage, festsitzende Aufgaben werden in kleine Schritte zerlegt, Fristen werden täglich neu geprüft und sonntags gibt es einen kurzen Wochenrückblick.

## When to Use

- Nachrichten wie „Notiz: …", „ich muss noch …", „neue Aufgabe: …", „merk dir: …"
- Bilder mit Aufgabenbezug (Rechnung, Terminbrief, handschriftliche Liste)
- Sprachnachrichten mit Erledigungen oder Erinnerungen
- „zeig meine Matrix", „was steht an", „meine Prioritäten"
- „X erledigt", „verschieb X", „streich X", „räum die Matrix auf"
- **„plane meinen Tag", „Abendplanung", „Tagesplan für morgen"** → Procedure D
- **Kurze Antworten auf die Abendplanung**, z. B. „1 und 3 erledigt", „passt", „nichts geschafft, passt" → Procedure D, Schritt 0 (Antwort verarbeiten) und Schritt 5
- **„was ist mein Frosch?", „womit fange ich an?", „guten Morgen"-Routine** → Procedure E
- **„Tag abschließen", „Feierabend", „was habe ich heute geschafft?"** → Procedure F
- **„meine Ziele", „zeig meine Leitziele", „ändere Ziel 2"** → Procedure G
- **„Wochenrückblick", „wie lief die Woche?"** und jede Abendplanung an einem Sonntag → Procedure H
- Explizit: `/eisenhower-matrix …`

## Quick Reference

- Matrix-Datei: Config-Key `eisenhower.file`; relative Pfade ab dem Hermes-Home (HERMES_HOME) auflösen, absolute Pfade unverändert nutzen. Standard: `workspace/eisenhower.md`
  - Ohne Hermes (z. B. Claude Code am PC): Obsidian-Vault-Datei `C:\Users\Lenovo\Documents\Obsidian Vault\06-Ideen\Eisenhower-Matrix.md` verwenden
- Tipp: Zeigt `eisenhower.file` in einen Obsidian-Vault, erscheint die Matrix automatisch als Notiz in Obsidian
- Fehlt die Datei: aus `templates/eisenhower.md` anlegen und Nutzer kurz informieren
- Quadranten: 🔴 Q1 dringend & wichtig (sofort) · 🟡 Q2 wichtig, nicht dringend (einplanen) · 🔵 Q3 dringend, nicht wichtig (delegieren) · ⚪ Q4 weder noch (streichen/irgendwann) · ✅ Erledigt (Archiv)
- Tagesplan: Abschnitt `## 🐸 Heute (<YYYY-MM-DD>)` ganz oben in der Matrix-Datei, nummerierte Liste 1–6, Platz 1 = Frosch. Übertragene Aufgaben tragen einen Zähler: `(übertragen: 2×)`
- Schreibweise: Den Stil der vorhandenen Datei beibehalten (z. B. Emojis, fett, nummeriert). Wichtig sind nur die Anmerkungen in Klammern: `(hinzugefügt: …)`, `(bis …)`, `(erledigt: …)`, `(übertragen: N×)`. Neue Daten als `YYYY-MM-DD` schreiben; ältere `TT.MM.JJJJ` stehen lassen.
- Zustand ausrechnen: Werkzeug `zustand_pruefen(matrix, heute)` vom MCP-Server `jev` (siehe unten)
- Leitziele: Abschnitt `## 🎯 Leitziele` (max. 3) in der Matrix-Datei — der Maßstab für „wichtig?" und für die Pareto-Auswahl abends
- Einstufungsregeln und Beispiele: `references/classification-guide.md`
- Tagesplanungs-Regeln (Ivy Lee, Pareto, Frosch): `references/tagesplan-guide.md`
- HTML-Ansicht: `templates/eisenhower.html` befüllen (Platzhalter `<!--TODAY_ITEMS-->`, `<!--Q1_ITEMS-->` … `<!--Q4_ITEMS-->`, `<!--UPDATED-->`)
- Erinnerungs-Routinen (18:00 Abendplanung, 7:00 Frosch): Anleitung in `references/cron-setup.md` — niemals ungefragt einrichten

## Die 5 Konfliktregeln (immer beachten)

1. **2-Minuten-Regel nur beim Erfassen**, nie als Start in den Tag — morgens gilt: erst der Frosch, dann alles andere. (Ausnahme: der Mini-Schritt aus Regel 5.)
2. **Mindestens 2 der 6 Tagesplätze für 🟡 Q2** — sonst gewinnt immer das Dringende und die langfristig wichtigen Dinge (Pareto!) bleiben liegen.
3. **Unerledigtes wandert kommentarlos als Übertrag an die Spitze des nächsten Tagesplans** — kein Vorwurf, das ist bei Ivy Lee so vorgesehen. Der Zähler `(übertragen: N×)` steigt dabei um 1.
4. **🔵 Q3 und ⚪ Q4 belegen nie Tagesplan-Plätze** — Q3 wird delegiert oder nebenbei erledigt, Q4 gestrichen.
5. **Festsitzende Aufgaben werden zerlegt, nicht endlos übertragen.** Ab 3 Übertragungen (oder wenn der Plan 3+ Tage liegen geblieben ist) fragst du EINMAL: „*<Aufgabe>* wandert jetzt schon <N>-mal mit. Was wäre der allerkleinste erste Schritt — etwas, das keine 5 Minuten dauert?" Der Mini-Schritt wird der neue Frosch (Zähler beginnt neu), die große Aufgabe bleibt im Quadranten stehen. Will der Nutzer nicht zerlegen, kurz fragen, ob die Aufgabe noch wichtig ist (sonst nach Q2/Q4). Das löst den Widerspruch zwischen Ivy Lee (übertragen) und Eat That Frog (der Frosch muss gegessen werden).

## Jev (optional): Einschätzungen vom MCP-Server `jev`

Ist der MCP-Server `jev` eingebunden, holst du die Einschätzungen von dort, statt sie selbst zu schätzen. Er hat drei Werkzeuge: `einsortieren`, `zwei_minuten`, `rangfolge`.

**Dazu das Rechen-Werkzeug `zustand_pruefen(matrix, heute)`** — Text der Matrix-Datei und heutiges Datum (`YYYY-MM-DD`) übergeben. Es braucht weder Jev-Schlüssel noch Netz und gehört nicht zur Ausfall-Regel unten. Es liefert fertig ausgerechnet: `plan` (Datum, `veraltet`, `tage_alt`, `offen` mit `uebertragen`, `erledigt`), `festsitzend`, `jetzt_dringend` (mit `neuer_quadrant`), `ueberfaellig`, `q1_ohne_frist_alt`, `q1_anzahl`, `q4_alt`, `leitziele`, `erledigt_letzte_7_tage`. Daten vergleichen, Tage zählen und Übertragungen zählen machst du NIE selbst, wenn das Werkzeug da ist — du übernimmst die Zahlen und entscheidest nur, was du dem Nutzer sagst. Ohne das Werkzeug (Server nicht eingebunden) schätzt du dieselben Punkte selbst aus der Datei.

- **Leitziele mitgeben:** `einsortieren` bekommt immer den Text des Abschnitts 🎯 Leitziele (leer, wenn keiner da ist) und das heutige Datum (`YYYY-MM-DD`). `rangfolge` bekommt die Leitziele und wird nur gerufen, wenn welche definiert sind; sonst gilt der Standardweg (Procedure D).
- **Ausfall:**
  - Eine Antwort mit `verfuegbar: false` und ein Werkzeug-Fehler bzw. eine Ausnahme statt einer JSON-Antwort zählen gleich.
  - Dann so arbeiten, als gäbe es Jev nicht (Standardweg dieser Procedure).
  - Nach einem fehlgeschlagenen Jev-Aufruf keine weiteren Jev-Aufrufe im selben Ablauf (dieselbe Nachricht, dieselbe Planung); den Rest mit dem Standardweg erledigen.
  - „(ohne Jev)“ an die Bestätigung (Procedure A) bzw. die Vorschlagszeile (Procedure D) anhängen, sobald das Einsortieren oder die Rangfolge wegen eines Ausfalls ohne Jev gelaufen ist — auch wenn Jev nach einem früheren Fehlschlag im selben Ablauf gar nicht mehr gefragt wurde. Wurde `rangfolge` nur übersprungen, weil keine Leitziele definiert sind, kein „(ohne Jev)“.
  - Ist `melden: true`, einmal sagen: „Hinweis: Jev ist gerade nicht erreichbar (<grund>). Ich sortiere solange selbst.“
- **Werkzeug fehlt ganz** (Server nicht eingebunden): Standardweg ohne Hinweis.
- **Was du liest:** `verfuegbar`, `grund`, `melden`; bei `einsortieren` zusätzlich `quadrant`, `sicher`, `unklar`; bei `zwei_minuten` `sofort_erledigen`; bei `rangfolge` `reihenfolge` (nur die Reihenfolge). Die Zahlenwerte (`wichtig`, `dringend`, `schnell`, `wert`) wertest du nie selbst aus — die Schwellen entscheidet der Server.

## Procedure

### A. Aufgabe erfassen

0. **2-Minuten-Filter:** Mit Jev: `zwei_minuten(aufgabe)` rufen. Nur bei `sofort_erledigen: true` vorschlagen, sie SOFORT zu erledigen. Ohne Jev selbst einschätzen: Wirkt die Aufgabe in unter 2 Minuten erledigbar (kurzer Anruf, eine Antwort-Nachricht, etwas wegwerfen)? Vorschlag:
   > „Das dauert keine 2 Minuten — mach es am besten gleich, dann muss ich es gar nicht notieren. Trotzdem speichern?"
   Nutzer will speichern → normal weiter mit Schritt 1.
1. Eingabe analysieren:
   - **Text:** Aufgabe(n) direkt extrahieren.
   - **Bild:** Kurz benennen, was du erkennst („Rechnung von Stadtwerke, fällig 15.07."), daraus die Aufgabe ableiten.
   - **Sprachnachricht:** Aus der Transkription die Aufgabe(n) extrahieren.
2. **Mit Jev:** `einsortieren(aufgabe, leitziele, heute)` rufen; gelesen werden `quadrant` (Q1–Q4), `sicher` und `unklar`.
   - `sicher: true` → direkt speichern (Schritt 5) und kurz melden, mit Ein-Satz-Begründung (Leitziel nennen, wenn eines passt) und Handlungsempfehlung (Q1 sofort, Q2 einplanen, Q3 delegieren, Q4 streichen/irgendwann). `<Emoji> <Q?>` kommt aus `quadrant`:
     > „✅ *<Aufgabe>* → <Emoji> <Q?> — <Begründung>. <Handlungsempfehlung>. (Anders? Sag 1–4.)"
   - `sicher: false` → NUR den unklaren Punkt fragen. Die schon sichere Dimension liest du am Buchstaben in `quadrant` ab, nie an den Zahlen: Q1/Q2 ⇒ wichtig ja, Q3/Q4 ⇒ wichtig nein; Q1/Q3 ⇒ dringend ja, Q2/Q4 ⇒ dringend nein.
     - `unklar: ["wichtig"]` → „Ist *<Aufgabe>* wichtig für dich bzw. deine Ziele? (ja/nein)"
     - `unklar: ["dringend"]` → „Muss *<Aufgabe>* in den nächsten 7 Tagen erledigt sein? (ja/nein)"
     - beide → beide Fragen in EINER Nachricht.
     Aus der Antwort und der sicheren Dimension den Quadranten bilden (wichtig+dringend=Q1, nur wichtig=Q2, nur dringend=Q3, keins=Q4), dann speichern.
   - Ausfall (siehe Jev-Abschnitt) → weiter mit dem Standardweg (Schritt 3), Bestätigung mit „(ohne Jev)“.
3. **Standardweg (ohne Jev):** Quadranten **vorschlagen**, mit Ein-Satz-Begründung. Wichtigkeit prüfen in dieser Reihenfolge: (a) Zahlt die Aufgabe auf ein 🎯 Leitziel ein? — dann das Ziel in der Begründung nennen („→ zahlt auf Ziel 2 ein"); (b) sonst die Konsequenz-Frage: „Was passiert, wenn es liegen bleibt?" Regeln: `references/classification-guide.md`. Format:
   > „Ich habe notiert: *<Aufgabe>*. Mein Vorschlag: <Emoji> <Q?> — <Begründung>. Passt das? (ja / oder 1–4 für einen anderen Quadranten)"
   Antwort auswerten: „ja"/👍 → speichern; Zahl 1–4 oder freie Formulierung → Korrektur übernehmen.
4. Nur wenn keine belastbare Einschätzung möglich ist (ohne Jev): offene Frage ohne Vorschlag —
   1️⃣ dringend & wichtig · 2️⃣ wichtig, nicht dringend · 3️⃣ dringend, nicht wichtig · 4️⃣ weder noch
5. Speichern: Zeile `- [ ] <Aufgabe> (hinzugefügt: <YYYY-MM-DD>)` in den Quadranten-Abschnitt einfügen; Deadline in Klammern ergänzen, falls bekannt („bis <YYYY-MM-DD>"). `Zuletzt aktualisiert` im Kopf aktualisieren. Gezielte Edits — die Datei nie komplett überschreiben.
6. Bestätigen: ein Satz mit Quadrant und Handlungsempfehlung (Q1 sofort, Q2 einplanen, Q3 delegieren, Q4 streichen/irgendwann). (Entfällt, wenn in Schritt 2 mit Jev schon gemeldet wurde.)
7. **Mehrere Aufgaben in einer Eingabe:** alle mit je einem Vorschlag auflisten, EINE gesammelte Bestätigung einholen. Mit Jev: je Aufgabe `zwei_minuten` und `einsortieren`. EINE Sammelmeldung für alle sicheren Aufgaben (direkt eintragen) und in derselben Nachricht die Fragen zu den unklaren Punkten der übrigen.

### B. Matrix anzeigen

1. Standard (Chat/Telegram): erst der 🐸 Heute-Abschnitt (falls vorhanden), dann kompakte Textliste je Quadrant mit Emoji-Marker; leere Quadranten als „—"; bei >10 Einträgen pro Quadrant nur die ersten 10 plus „(+n weitere)".
2. Auf Wunsch („als Datei", „schön formatiert"): `templates/eisenhower.html` kopieren, Platzhalter mit `<li>`-Einträgen befüllen, im Workspace speichern (z. B. `eisenhower-<YYYY-MM-DD>.html`) und über den aktiven Kanal als Datei senden.

### C. Matrix pflegen

- **Abhaken** („X erledigt"): Zeile als `- [x] <Aufgabe> (erledigt: <YYYY-MM-DD>)` ins Archiv verschieben. Steht die Aufgabe auch im Heute-Abschnitt: dort mit `✅` markieren (nicht löschen — der Tagesüberblick bleibt vollständig).
- **Verschieben** („das ist jetzt dringend"): Zeile in den anderen Quadranten-Abschnitt bewegen.
- **Löschen** („streich X"): einzige destruktive Aktion — erst rückbestätigen, dann Zeile entfernen.
- **Aufräumen:** Kandidaten nennen (Q4-Einträge älter als 30 Tage, überfällige Deadlines) und fragen, was damit geschehen soll.
- Bei mehrdeutiger Referenz („das ist erledigt" bei mehreren offenen Aufgaben): nachfragen, nie raten.

### D. Abendplanung — die 6 Aufgaben für morgen (Ivy Lee)

Regeln im Detail: `references/tagesplan-guide.md`.

0. **Rückmeldung zuerst (der Rückkanal):** Matrix lesen und `zustand_pruefen` rufen. Gibt es einen Heute-Abschnitt mit offenen Aufgaben, IMMER zuerst fragen:
   > „🌙 Kurzer Rückblick: Was davon hast du heute geschafft? 1. … · 2. … · 3. … (z. B. ‚1 und 3' oder ‚nichts')"
   Erledigtes wie in Procedure C abhaken, der Rest wird Übertrag. Kommt keine Antwort, den alten Plan NICHT stillschweigend übernehmen und nichts in die Datei schreiben — beim nächsten Kontakt wird er als veraltet erkannt (Procedure E, Schritt 4).
   **Automatischer Lauf (Cron):** Die Antwort des Nutzers kommt dann oft in einer anderen Unterhaltung an. Deshalb Rückfrage, Zustands-Hinweise (0b) und Vorschlag (Schritt 4) in EINER Nachricht schicken, mit der Bitte um eine einzige Antwort: „Sag mir kurz, was erledigt ist, und ob der Plan passt (z. B. ‚1 erledigt, passt')." Eine solche Antwort später im Chat (auch ohne Zusammenhang, z. B. „2 und 3 erledigt, Plan passt") wird so verarbeitet: abhaken (Procedure C), dann Schritt 5 mit dem zuletzt vorgeschlagenen Plan ohne die erledigten Aufgaben. Ist heute Sonntag: nach der Rückmeldung zuerst Procedure H (Wochenrückblick), dann weiter mit Schritt 0b.
0b. **Zustand bereinigen (aus `zustand_pruefen`), höchstens eine kurze Nachricht:**
   - `jetzt_dringend` → Verschieben vorschlagen: „*<Aufgabe>* ist in <N> Tagen fällig — nach Q1?" (`neuer_quadrant`).
   - `ueberfaellig` → kurz nennen und fragen: noch erledigen, neue Frist oder streichen?
   - `q1_ohne_frist_alt` → „Diese Aufgaben stehen ohne Frist seit über einer Woche in Q1 — eher wichtig als dringend. Nach Q2?" (Dringend heißt: Frist in den nächsten 7 Tagen.)
   - `festsitzend` → Konfliktregel 5 (Mini-Schritt) für die oberste festsitzende Aufgabe; weitere erst am nächsten Abend.
   - Nichts davon vorhanden → direkt weiter. Pro Abend nicht mehr als diese eine Sammelnachricht, damit die Planung kurz bleibt.
1. Kandidaten sammeln in dieser Reihenfolge:
   a. **Übertrag:** unerledigte Aufgaben aus dem aktuellen Heute-Abschnitt (ohne ✅) — die kommen zuerst.
   b. Alle offenen 🔴 Q1-Aufgaben.
   c. 🟡 Q2-Aufgaben — per Pareto auswählen: „Welche bringt morgen Ziel 1–3 (🎯 Leitziele) am weitesten voran?" Mit Jev und definierten Leitzielen: alle offenen Q1- und Q2-Aufgaben (Übertrag inklusive) an `rangfolge(aufgaben, leitziele)` geben und dessen Reihenfolge als Pareto-Antwort nehmen (oberste zuerst). Ohne Jev, bei Ausfall oder ohne Leitziele: selbst einschätzen (Standardweg). Sind keine Leitziele definiert: EINMAL anbieten, jetzt bis zu 3 festzulegen (Procedure G) — lehnt der Nutzer ab, nie wieder ungefragt nachhaken.
   d. **Q1-Überlauf-Check:** Stehen mehr als 5 offene Aufgaben in Q1, kann nicht alles gleich dringend UND wichtig sein — anbieten, die Einstufung gemeinsam zu prüfen, bevor geplant wird.
2. Daraus **maximal 6** vorschlagen, davon **mindestens 2 aus Q2** (Konfliktregel 2). Q3/Q4 nie (Konfliktregel 4). `rangfolge` ändert nur die Reihenfolge innerhalb dieser Regeln (Übertrag zuerst, max. 6, min. 2× Q2, Q3/Q4 nie).
3. **Frosch bestimmen:** die wichtigste UND unangenehmste Aufgabe auf Platz 1 — im Zweifel fragen: „Welche davon schiebst du am längsten vor dir her?" Liegt eine `rangfolge` vor, ist der Frosch-Kandidat die höchstplatzierte Aufgabe daraus, die im Vorschlag steht; ist eine andere Aufgabe deutlich unangenehmer, im Zweifel fragen.
4. Vorschlag als nummerierte Liste zeigen, Frosch markiert:
   > „Mein Vorschlag für morgen: 1. 🐸 … · 2. … · 3. … — Passt das? (ja / oder sag mir, was du tauschen willst)"
   Ist `rangfolge` ausgefallen, die Vorschlagszeile mit „(ohne Jev)“ beenden.
5. Nach Bestätigung: alten Heute-Abschnitt ersetzen durch `## 🐸 Heute (<morgiges Datum>)` mit der Liste 1–6 ganz oben in der Matrix-Datei (direkt unter `Zuletzt aktualisiert`). Bei jeder übertragenen Aufgabe den Zähler `(übertragen: N×)` um 1 erhöhen (fehlt er, mit `(übertragen: 1×)` beginnen); neu gewählte Aufgaben und Mini-Schritte bekommen keinen Zähler. Aufgaben bleiben zusätzlich in ihren Quadranten stehen.
6. Weniger als 6 Kandidaten? Völlig okay — lieber 3 echte als 6 aufgefüllte. Mehr als 6 gewünscht? Freundlich ablehnen: „Ivy Lee wirkt gerade WEIL es nur 6 sind — was davon kann auf übermorgen?"

### E. Morgen-Frosch (Eat That Frog)

0. **Zuerst** `zustand_pruefen` rufen. Ist `plan.veraltet`, direkt Schritt 4 — die Schritte 1–3 entfallen.
1. Aufgabe 1 aus dem Heute-Abschnitt nennen, mit einem Satz Motivation:
   > „🐸 Dein Frosch heute: *<Aufgabe>*. Danach fühlt sich der Rest des Tages leicht an — fang damit an, bevor du irgendetwas anderes machst."
2. Danach die restlichen Tagesaufgaben 2–6 kompakt auflisten.
3. **Morgens KEINE 2-Minuten-Aufgaben oder Kleinkram vorschlagen** (Konfliktregel 1) — erst wenn der Frosch erledigt gemeldet ist.
4. **Plan veraltet** (`plan.veraltet` aus `zustand_pruefen`, oder kein Heute-Abschnitt)? Die alte Liste NICHT als heutigen Plan ausgeben. Stattdessen:
   > „🐸 Guten Morgen! Dein letzter Plan ist vom <Datum> — er ist liegen geblieben. Was davon ist inzwischen erledigt? Danach planen wir heute in 2 Minuten neu."
   Dann Mini-Version von Procedure D (Rückmeldung → Zustand → Vorschlag). Ist der alte Frosch `festsitzend`, gleich Konfliktregel 5 anwenden.

### F. Tag abschließen

1. Fragen, was vom Tagesplan geschafft wurde (oder aus „X erledigt"-Meldungen des Tages ableiten).
2. Erledigtes: wie in Procedure C ins Archiv, im Heute-Abschnitt mit ✅ markieren.
3. Unerledigtes: kommentarlos als Übertrag für die nächste Abendplanung vormerken (Konfliktregel 3) — kein Vorwurf, keine Rechtfertigungsfragen.
4. Wenn der Nutzer mag, direkt in die Abendplanung (Procedure D) übergehen — das ist der Ivy-Lee-Idealfall: Tag abschließen + morgen planen in einem Rutsch. (Die Abendplanung enthält die Rückfrage ohnehin als Schritt 0; nach einem Tagesabschluss nicht noch einmal fragen.)

### G. Leitziele pflegen

Die Leitziele beantworten: „Was will ich dieses Jahr voranbringen?" Sie machen aus der schwammigen Frage „ist das wichtig?" die klare Frage „zahlt das auf Ziel 1, 2 oder 3 ein?".

1. **Anzeigen** („meine Ziele"): die bis zu 3 Ziele aus dem 🎯-Abschnitt nennen.
2. **Festlegen/Ändern** („ändere Ziel 2", „mein neues Ziel ist …"): Formulierung des Nutzers wörtlich übernehmen (ein bis zwei Sätze), Abschnitt aktualisieren, kurz bestätigen.
3. **Maximal 3 Ziele** — bei mehr freundlich begrenzen: mit 5+ Zielen ist wieder alles „wichtig" und der Maßstab ist weg.
4. **Noch keine Ziele definiert:** alles funktioniert wie bisher (Konsequenz-Frage als Maßstab). Einmalig bei einer Abendplanung anbieten, Ziele festzulegen — nie wiederholt nerven.
5. Ziele sind langfristig: bei der Einstufung und Abendplanung nur LESEN, nie ungefragt umformulieren.

### H. Wochenrückblick (Pareto auf Wochenebene)

Läuft automatisch in der Sonntags-Abendplanung (Procedure D, Schritt 0) oder auf Zuruf. Kurz halten — eine Nachricht, eine Rückfrage.

1. `zustand_pruefen` rufen (falls nicht schon geschehen).
2. **Bilanz:** `erledigt_letzte_7_tage` zählen und kurz würdigen („Diese Woche: 6 Aufgaben erledigt, u. a. …"). Kein Vorwurf bei wenig.
3. **Leitziel-Check (der Kern):** Für jedes 🎯 Leitziel prüfen: Hat diese Woche eine erledigte Aufgabe darauf eingezahlt, und steht dafür eine offene Aufgabe in Q1/Q2? Das ist eine inhaltliche Einschätzung — die machst du selbst. Für jedes Ziel ohne erledigten Schritt UND ohne offene Aufgabe EINEN konkreten nächsten Schritt vorschlagen:
   > „🎯 Für ‚<Ziel>' ist gerade nichts geplant. Vorschlag für Q2: *<konkreter Schritt, max. 1 Stunde>* — aufnehmen? (ja/nein/anders)"
   Höchstens ein Vorschlag pro Ziel. Bei „ja" mit `(hinzugefügt: <heute>)` in Q2 eintragen.
4. **Aufräumen:** `q4_alt` als Streich-Kandidaten nennen (Nutzer entscheidet, Löschen wie in Procedure C mit Rückbestätigung).
5. Danach normal mit der Abendplanung (Procedure D, Schritt 0b) weitermachen. Neu aufgenommene Leitziel-Schritte sind gute Q2-Kandidaten für die 2er-Quote.

## Pitfalls

- Matrix-Datei unlesbar/fremdes Format → NICHT überschreiben; Nutzer fragen (reparieren vs. neu anlegen), vorher Kopie als `eisenhower.md.bak` sichern.
- Unklare Antwort auf die Einstufungsfrage → einmal präzisierend nachfragen; danach Q2 als sicherer Standard mit Hinweis, dass es korrigierbar ist.
- Keine Aufgabe erkennbar (Text, Bild oder Sprache) → sagen, was erkannt wurde, und fragen, ob/was gespeichert werden soll — nichts erfinden.
- Bild/Audio ohne verwertbaren Inhalt (kein Vision/Transkript im Setup) → ehrlich sagen und um Textfassung bitten.
- Nutzer bearbeitet die Datei auch von Hand → Abschnittsüberschriften und Checkbox-Format respektieren, unbekannte Zusatznotizen stehen lassen.
- Heute-Abschnitt existiert bereits → bei neuer Planung ERSETZEN, nie einen zweiten anlegen.
- Nutzer will 8 oder 10 Tagesaufgaben → bei max. 6 bleiben und den Grund nennen (Fokus ist der Kern von Ivy Lee).
- Nutzer startet den Tag mit Kleinkram-Fragen („soll ich erst die Mails machen?") → freundlich an den Frosch erinnern, nicht belehren.
- 2-Minuten-Filter zu aggressiv → im Zweifel speichern; der Filter ist ein Angebot, kein Zwang.
- Leitziele sind Nutzer-Text → beim Einstufen/Planen nur lesen, nie umformulieren oder löschen; Änderungen nur auf ausdrücklichen Wunsch (Procedure G).
- Q1 quillt über (>5 Einträge) → nicht stumm weiterplanen; Einstufungs-Check anbieten.
- Jev-Werte sind Einschätzungen, keine Wahrheit → Korrekturen des Nutzers („nein, das ist Q3") haben immer Vorrang und werden ohne Diskussion übernommen.
- `verfuegbar: false` mehrmals am Tag → bei `melden: true` einmal hinweisen, danach still mit „(ohne Jev)“ weiterarbeiten, bis Jev wieder antwortet.
- Alten Plan morgens einfach wiederholen → genau dieser Fehler ließ früher Pläne wochenlang stehen. Bei `plan.veraltet` immer erst Rückmeldung holen (Procedure E, Schritt 4).
- Konfliktregel 5 als Druckmittel benutzen → nein. Einmal freundlich nach dem Mini-Schritt fragen; lehnt der Nutzer ab, akzeptieren und erst nach 3 weiteren Übertragungen wieder fragen.
- Abendplanung mit Rückfragen überladen → Rückmeldung, eine Sammelnachricht zum Zustand, dann der Vorschlag. Mehr nicht.
- Dateistil des Nutzers „aufräumen" → nein. Emojis, Fettdruck und Nummerierung stehen lassen; nur die Klammer-Anmerkungen müssen stimmen.

## Verification

- Abendplanung mit offenem Heute-Abschnitt → erste Nachricht ist die Rückfrage „Was hast du heute geschafft?", erst danach der Vorschlag.
- Plan 3+ Tage alt, Morgen-Frosch → kein Wiederholen der alten Liste, sondern Hinweis „liegen geblieben" + Rückfrage.
- Aufgabe mit `(übertragen: 3×)` → einmalige Mini-Schritt-Frage; der Mini-Schritt wird Platz 1 mit 🐸.
- Q2-Aufgabe mit Frist in 4 Tagen → Vorschlag „nach Q1?".
- Q1-Aufgabe ohne Frist, 10 Tage alt → Vorschlag „nach Q2?".
- Sonntag-Abendplanung → Wochenbilanz + höchstens ein Vorschlag pro vernachlässigtem Leitziel, danach normale Planung.
- Nach bestätigter Planung steht bei übertragenen Aufgaben der Zähler `(übertragen: N×)` um 1 höher.
- Neue Text-Notiz → Vorschlag mit Begründung → „ja" → Eintrag steht mit Datum im vorgeschlagenen Quadranten.
- Kleinstaufgabe („Zahnarzt kurz anrufen") → 2-Minuten-Hinweis kommt zuerst.
- Foto einer Rechnung mit Frist → extrahierte Aufgabe samt Deadline und passendem Quadrant-Vorschlag.
- „zeig meine Matrix" → Heute-Abschnitt zuerst, dann 4 Quadranten kompakt im Chat, leere als „—".
- „plane meinen Tag" → max. 6 Aufgaben, Frosch auf Platz 1 markiert, ≥2 aus Q2, Übertrag zuerst; nach „ja" steht `## 🐸 Heute` oben in der Matrix-Datei.
- „meine Ziele" → die 3 Leitziele werden genannt (oder das einmalige Angebot, sie festzulegen).
- Aufgabe mit Leitziel-Bezug → Begründung nennt das Ziel („→ zahlt auf Ziel 2 ein").
- „was ist mein Frosch?" → Aufgabe 1 aus Heute, kein Kleinkram-Angebot.
- „X erledigt" → Eintrag im Archiv mit Erledigt-Datum, im Heute-Abschnitt ✅.
- Nächste Abendplanung → gestriges Unerledigtes erscheint als Übertrag ganz oben im Vorschlag.
- „als Datei" → HTML-Datei erzeugt und versendet, öffnet als Heute-Band + 2×2-Grid im Browser.
- Vage Notiz ohne Prioritätssignale → offene 1–4-Frage statt erfundenem Vorschlag.
- Mit Jev, eindeutige Aufgabe („Steuererklärung, Frist morgen") → direkt in Q1 eingetragen, kurze Meldung ohne Rückfrage.
- Mit Jev, unklare Aufgabe → genau eine Ja/Nein-Frage zum unklaren Punkt, danach Eintrag.
- Jev nicht erreichbar → Vorschlag wie ohne Jev, Bestätigung endet mit „(ohne Jev)“; beim 3. Fehlschlag in Folge ein Hinweis.
- Abendplanung mit Jev (und Leitzielen) → Q2-Auswahl folgt der `rangfolge`, Ivy-Lee-Regeln bleiben erfüllt.
