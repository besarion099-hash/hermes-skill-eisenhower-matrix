# Optionaler Morgen-Check (Cron)

Dieser Skill richtet NIE selbst eine Routine ein. Wenn der Nutzer nach Erinnerungen, einem täglichen Überblick o. Ä. fragt, biete diese Anleitung an.

## Was der Morgen-Check tut

Zu einer festen Zeit (z. B. werktags 08:00) schickt Hermes proaktiv:
1. Alle offenen 🔴 Q1-Aufgaben („heute dran")
2. Hinweise auf überfällige Deadlines in allen Quadranten
3. Optional: Aufräum-Kandidaten (⚪ Q4-Einträge älter als 30 Tage)

## Einrichtung (durch den Nutzer angestoßen)

Der Nutzer sagt z. B.:
> „Richte mir einen täglichen Eisenhower-Check werktags um 8 Uhr ein."

Hermes legt daraufhin mit seinem Cron-/Scheduler-Feature einen Job an, dessen Prompt lautet:
> „Nutze den Skill eisenhower-matrix: Zeige alle offenen Q1-Aufgaben, nenne überfällige Deadlines und schlage höchstens drei Aufräum-Kandidaten aus Q4 vor. Antworte kompakt für Telegram."

## Anpassen und Beenden

- Andere Zeiten/Frequenz: einfach beim Einrichten nennen (z. B. „nur montags", „abends 18 Uhr").
- Beenden: „lösch den täglichen Eisenhower-Check" — Hermes entfernt den Cron-Job.
- Vorher immer bestätigen lassen, welche Zeit gilt, damit keine ungewollten Pings entstehen.
