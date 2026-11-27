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
- GitHub Pages vorbereitet: `_config.yml`, Downloadseite `index.md` (füllt sich selbst aus den Handouts und `_resources/`), Ordner `_resources/` für Word- und Excel-Dateien je Modul; Regeln in `AGENTS.md` unter „Downloads über GitHub Pages“

## Nächster Schritt

Fehlende Teilnehmermaterialien für den Grundkurs schreiben, beginnend mit den Handouts für Block 02, 04 und 05 nach dem Muster von `Grundkurs/Block-03-Handout.md`. Liste aller fehlenden Dateien: `README.md`, Abschnitt „Fehlende Dateien“.

## Offene Entscheidungen

- **GitHub Pages aktivieren:** nach dem Push unter Settings → Pages „Deploy from a branch“, `main`, `/ (root)`. Der Jekyll-Build mit `_resources` ist lokal nicht getestet – nach dem ersten Push mit einer echten Übungsdatei prüfen, ob sie auf der Seite erscheint und sich herunterladen lässt.
- **Sichtbarkeit:** Das Repository ist auf GitHub öffentlich (Stand 2026-11-27), früher hieß es hier „privat“. Damit sind auch Leitfäden und Lösungen öffentlich. Bleibt das so?
- **Präsentationen:** Folientexte als Markdown (wie Block 01) für alle Blöcke, oder echte Präsentationsdateien?
- **Nummerierung der Übungen:** Nummer 07 ist doppelt (Quiz Block 07, Wartungsprotokoll Block 05) – neu durchnummerieren?
- **Materialien:** Zellbezüge (TechVision) und Pivot-Leitfaden (Online-Shop) ins Szenario Haus Lichtblick übertragen?
- **Vor dem ersten Kurs** an einem Kurs-PC prüfen, was `README.md` unter „Vor dem ersten Kurs prüfen“ aufführt (Bezeichnungen im neuen Outlook, Serien-E-Mail über das neue Outlook, Startmenü-Position).
- **Veröffentlichung:** In der Wissensbasis `fdoebbelin/Knowledge` trägt die Quelle „Microsoft 365 im Facility Management – Grundkurs und Aufbaumodule“ `draft: true`. Wird der Kurs öffentlich, dort `draft` entfernen.
