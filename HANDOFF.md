# Übergabe

| | |
|---|---|
| Stand | 2026-11-27 |
| Branch | main |

## Stand

Der Kurs ist aus zwei älteren Kursen der Wissensbasis entstanden (*Office-Short*: Grundkurs Office 2019; *Office-Basics*: Word- und Excel-Sitzungen) und vollständig auf Microsoft 365 mit dem neuen Outlook umgestellt. Alle Texte liegen als Markdown vor; Übungsdateien, die meisten Handouts und Präsentationen fehlen noch.

## Erledigt

- Struktur: `Grundkurs/` (Block 01–12), `Aufbau-Word/`, `Aufbau-Excel/`, `Aufbau-Verknüpfung/`, `Materialien/`, `README.md`
- PDFs entfernt; Block 01 Handout und Präsentation als Markdown neu
- Grundkurs auf Microsoft 365, neues Outlook, Windows 11; Copilot-Ausblick in Block 12
- Aufbaumodule zusammengeführt, ins Szenario Haus Lichtblick übertragen, fachliche Fehler korrigiert (Tastenkürzel, DIN 5008, Pivot, Blattschutz)
- Mieterliste in der Referenzliste ergänzt
- `AGENTS.md`, `CLAUDE.md`, `HANDOFF.md` für die Arbeit mit Agenten
- Repository und Seite sind öffentlich – so gewollt (bestätigt 2026-11-27), Leitfäden und Lösungen eingeschlossen
- GitHub Pages aktiv mit Theme Just the Docs: Startseite `index.md` (Kursaufbau, alle Handouts und Übungsdateien), Ordner `_resources/` für Word- und Excel-Dateien je Modul; Regeln in `AGENTS.md` unter „Website über GitHub Pages“
- Grundkurs auf der Website: Übersicht `Grundkurs/index.md` mit Tagesplan, je Block eine Seite `Block-NN.md`, Kopfzeilen in Leitfäden, Handouts, Folientexten und der Referenzliste

## Nächster Schritt

1. Website ansehen (Grundkurs). Passt die Navigation, folgen **Aufbaumodule und Materialien**: je Modul `index.md` als Modulseite, Kopfzeilen in allen Einheiten, Modulseiten auf der Startseite verlinken, die übergangsweisen `defaults` mit `nav_exclude` in `_config.yml` und die Ausnahmen im Kopfzeilen-Check in `AGENTS.md` entfernen.
2. Danach fehlende Teilnehmermaterialien, beginnend mit den Handouts für Block 02, 04 und 05 nach dem Muster von `Grundkurs/Block-03-Handout.md` (Kopfzeile wie dort). Liste: `README.md`, „Fehlende Dateien“.

## Offene Entscheidungen

- **Erste Übungsdatei prüfen:** GitHub Pages ist aktiv (<https://fdoebbelin.github.io/Office-365/>, Branch `main`, `/`), Handouts erscheinen, `_resources/` wird veröffentlicht. Die Download-Tabelle ist noch ungetestet, weil es keine Office-Datei gibt – nach dem ersten Push einer Übungsdatei prüfen, ob sie im richtigen Block erscheint und sich herunterladen lässt.
- **Präsentationen:** Folientexte als Markdown (wie Block 01) für alle Blöcke, oder echte Präsentationsdateien?
- **Nummerierung der Übungen:** Nummer 07 ist doppelt (Quiz Block 07, Wartungsprotokoll Block 05) – neu durchnummerieren?
- **Materialien:** Zellbezüge (TechVision) und Pivot-Leitfaden (Online-Shop) ins Szenario Haus Lichtblick übertragen?
- **Vor dem ersten Kurs** an einem Kurs-PC prüfen, was `README.md` unter „Vor dem ersten Kurs prüfen“ aufführt (Bezeichnungen im neuen Outlook, Serien-E-Mail über das neue Outlook, Startmenü-Position).
- **Veröffentlichung:** In der Wissensbasis `fdoebbelin/Knowledge` trägt die Quelle „Microsoft 365 im Facility Management – Grundkurs und Aufbaumodule“ `draft: true`. Wird der Kurs öffentlich, dort `draft` entfernen.
