# Erinnerungs-Routinen (Cron)

Dieser Skill richtet NIE selbst eine Routine ein. Wenn der Nutzer nach Erinnerungen oder einem festen Tagesrhythmus fragt, biete diese Anleitung an. Vor dem Anlegen immer die Uhrzeiten bestätigen lassen.

## Der empfohlene Tagesrhythmus (2 Routinen)

Das 5-Methoden-System entfaltet seine Wirkung durch zwei feste Zeitpunkte:

### 1. Abendplanung — täglich 18:00 (Ivy Lee)

Cron-Prompt:
> „Nutze den Skill eisenhower-matrix, Procedure D (Abendplanung): Frag zuerst, was vom heutigen Plan erledigt ist (Schritt 0), dann schlage maximal 6 Aufgaben für morgen vor (Übertrag zuerst, mindestens 2 aus Q2, Frosch mit 🐸 auf Platz 1) und bitte um Bestätigung. Sonntags vorher der Wochenrückblick (Procedure H). Antworte kompakt für Telegram."

Ab Version 2.3.0 steht die Rückfrage und der Sonntags-Rückblick auch in der Skill-Anleitung selbst. Ältere Jobs mit dem kürzeren Prompt funktionieren deshalb weiter.

### 2. Morgen-Frosch — täglich 7:00 (Eat That Frog)

Cron-Prompt:
> „Nutze den Skill eisenhower-matrix, Procedure E (Morgen-Frosch): Nenne die Aufgabe 1 aus dem Heute-Abschnitt mit einem Satz Motivation, dann kompakt die Aufgaben 2–6. Keine Kleinkram-Vorschläge. Antworte kompakt für Telegram."

## Wochenrückblick — ohne eigene Routine

Der Wochenrückblick (Procedure H) läuft in der Sonntags-Abendplanung mit: Wochenbilanz, ein nächster Schritt pro vernachlässigtem Leitziel, alte Q4-Einträge zum Streichen. Dafür ist KEIN zusätzlicher Cron-Job nötig — und es kommt keine zusätzliche Nachricht.

## Achtung Zeitzone

Viele Server rechnen Cron-Zeiten in UTC. Dann muss die Uhrzeit bei der Zeitumstellung angepasst werden (Wien: Sommerzeit UTC+2, Winterzeit UTC+1). Beispiel 18:00 Wiener Zeit: im Sommer `0 16 * * *`, im Winter `0 17 * * *`. Beim Einrichten prüfen, in welcher Zeitzone der Scheduler rechnet.

## Einrichtung (durch den Nutzer angestoßen)

Der Nutzer sagt z. B.:
> „Richte mir die Abendplanung um 18 Uhr und den Frosch um 7 Uhr ein."

Hermes legt daraufhin mit seinem Cron-/Scheduler-Feature die Jobs mit den obigen Prompts an.

## Anpassen und Beenden

- Andere Zeiten/Frequenz: einfach beim Einrichten nennen (z. B. „nur werktags", „Planung um 20 Uhr").
- Beenden: „lösch die Abendplanung" / „lösch den Morgen-Frosch" — Hermes entfernt den jeweiligen Cron-Job.
- Vorher immer bestätigen lassen, welche Zeit gilt, damit keine ungewollten Pings entstehen.
