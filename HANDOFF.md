# Übergabe

| | |
|---|---|
| Stand | 2026-11-27 |
| Branch | main |

## Stand

Der Kurs ist aus zwei älteren Kursen der Wissensbasis entstanden (*Office-Short*: Grundkurs Office 2019; *Office-Basics*: Word- und Excel-Sitzungen) und vollständig auf Microsoft 365 mit dem neuen Outlook umgestellt. Neue Ausrichtung (2026-11-27): **Selbststudium und Einzelcoaching ohne festen Zeitplan**. Jeder Grundkurs-Block wird zu einer Lerneinheit (Leitfaden, Handout und Folien gebündelt, Folien als SVG-Abbildungen, farbige Kästen) mit eigenem Übungsblatt und echten Übungsdateien. **Block 01 ist fertig** und dient als Muster; Regeln in `AGENTS.md`.

## Erledigt

- Struktur: `Grundkurs/` (Block 01–12), `Aufbau-Word/`, `Aufbau-Excel/`, `Aufbau-Verknüpfung/`, `Materialien/`, `README.md`
- Grundkurs auf Microsoft 365, neues Outlook, Windows 11; Copilot-Ausblick in Block 12
- Aufbaumodule zusammengeführt, ins Szenario Haus Lichtblick übertragen, fachliche Fehler korrigiert (Tastenkürzel, DIN 5008, Pivot, Blattschutz)
- Repository und Seite sind öffentlich – so gewollt (bestätigt 2026-11-27), Lösungen eingeschlossen
- GitHub Pages mit Just the Docs: Startseite, Grundkurs-Übersicht, Blockseiten, Downloads aus `_resources/`, farbige Kästen (`_config.yml` → `callouts`, `_sass/custom/custom.scss`)
- Zeitangaben aus Startseite, Grundkurs-Übersicht und Blockseiten entfernt; Block 07 heißt jetzt „Wiederholung Outlook und Word“
- **Block 01 – Orientierung in Microsoft 365:** Lerneinheit `Grundkurs/Block-01.md` (ohne Vorstellungsrunde und Zeitplan), sechs Folien in `assets/folien/block-01/`, Übungsblatt als Seite und `.docx`, Übungsdateien `Block-01-Willkommen.docx` und `Block-01-Mieterliste.xlsx`; alter Leitfaden, Handout und Folientexte darin aufgegangen und entfernt; Skripte in `_werkzeuge/`

## Nächster Schritt

1. Block 01 auf der Website ansehen und Rückmeldung zu Aufbau, Kästen, Folien und Übungsdateien einholen. Word- und Excel-Dateien einmal in Microsoft 365 öffnen (lokal ließen sie sich nur gegen das Schema prüfen, nicht ansehen).
2. Danach **Block 02 – E-Mail-Grundlagen** nach dem Muster von Block 01 umstellen, dann die weiteren Blöcke der Reihe nach.
3. Später: Aufbaumodule und Materialien mit Modulseiten und Kopfzeilen in die Navigation holen, die übergangsweisen `defaults` mit `nav_exclude` in `_config.yml` und die Ausnahmen im Kopfzeilen-Check in `AGENTS.md` entfernen.

## Offene Entscheidungen

- **Block 06 „Tagesrückblick und Fragen“ und Block 07 „Wiederholung Outlook und Word“** stammen aus dem Zwei-Tage-Format. Für Selbststudium umbauen (z. B. zu Wiederholungs- und Übungsblöcken mit gemischten Aufgaben), zusammenlegen oder streichen?
- **Excel-Funktionen in Übungsdateien:** XVERWEIS & Co. lassen sich beim Erzeugen nicht vorrechnen. Übungsdateien mit solchen Formeln vor der Veröffentlichung einmal in Excel öffnen und speichern, oder die Formeln von den Lernenden eingeben lassen?
- **Materialien:** Zellbezüge (TechVision) und Pivot-Leitfaden (Online-Shop) ins Szenario Haus Lichtblick übertragen?
- **Vor dem ersten Einsatz** an einem PC prüfen, was `README.md` unter „Vor dem ersten Kurs prüfen“ aufführt.
- **Veröffentlichung:** In der Wissensbasis `fdoebbelin/Knowledge` trägt die Quelle „Microsoft 365 im Facility Management – Grundkurs und Aufbaumodule“ `draft: true`. Wird der Kurs öffentlich, dort `draft` entfernen.
