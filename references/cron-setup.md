# Erinnerungs-Routinen (Cron)

Dieser Skill richtet NIE selbst eine Routine ein. Wenn der Nutzer nach Erinnerungen oder einem festen Tagesrhythmus fragt, biete diese Anleitung an. Vor dem Anlegen immer die Uhrzeiten bestätigen lassen.

## Der empfohlene Tagesrhythmus (2 Routinen)

Das 5-Methoden-System entfaltet seine Wirkung durch zwei feste Zeitpunkte:

### 1. Abendplanung — täglich 18:00 (Ivy Lee)

Cron-Prompt:
> „Nutze den Skill eisenhower-matrix, Procedure D (Abendplanung): Lies die Matrix, schlage maximal 6 Aufgaben für morgen vor (Übertrag zuerst, mindestens 2 aus Q2, Frosch mit 🐸 auf Platz 1) und bitte um Bestätigung. Antworte kompakt für Telegram."

### 2. Morgen-Frosch — täglich 7:00 (Eat That Frog)

Cron-Prompt:
> „Nutze den Skill eisenhower-matrix, Procedure E (Morgen-Frosch): Nenne die Aufgabe 1 aus dem Heute-Abschnitt mit einem Satz Motivation, dann kompakt die Aufgaben 2–6. Keine Kleinkram-Vorschläge. Antworte kompakt für Telegram."

## Optional: Wochenrück- und -ausblick

Zusätzlich möglich (z. B. sonntags 18:00): Aufräum-Kandidaten (Q4 älter als 30 Tage), überfällige Deadlines, Archiv-Bilanz der Woche. Nur einrichten, wenn ausdrücklich gewünscht.

## Einrichtung (durch den Nutzer angestoßen)

Der Nutzer sagt z. B.:
> „Richte mir die Abendplanung um 18 Uhr und den Frosch um 7 Uhr ein."

Hermes legt daraufhin mit seinem Cron-/Scheduler-Feature die Jobs mit den obigen Prompts an.

## Anpassen und Beenden

- Andere Zeiten/Frequenz: einfach beim Einrichten nennen (z. B. „nur werktags", „Planung um 20 Uhr").
- Beenden: „lösch die Abendplanung" / „lösch den Morgen-Frosch" — Hermes entfernt den jeweiligen Cron-Job.
- Vorher immer bestätigen lassen, welche Zeit gilt, damit keine ungewollten Pings entstehen.
