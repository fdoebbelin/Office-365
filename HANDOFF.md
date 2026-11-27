# Übergabe

| | |
|---|---|
| Stand | 2026-11-27 |
| Branch | main (nicht gepusht) |

## Stand

Der Kurs ist auf Microsoft 365 mit dem neuen Outlook umgestellt und für **Selbststudium und Einzelcoaching ohne festen Zeitplan** ausgerichtet. Jeder Grundkurs-Block ist eine Lerneinheit (Leitfaden, Handout und Folien gebündelt, Folien als SVG, farbige Kästen) mit eigenem Übungsblatt (Seite und `.docx`) und echten Übungsdateien. Regeln in `AGENTS.md`.

**Committet:** Block 01 bis 06 und 08 bis 12.
**Fertig, aber nicht committet:** Block 07 – liegt im Arbeitsverzeichnis (siehe „Nächster Schritt“).

## Erledigt

- Struktur, Umstellung auf Microsoft 365, Website mit Just the Docs, Downloads, Kästen (frühere Sitzungen)
- **Block 01** als Muster
- **Block 02–05** (Outlook E-Mail, Kalender, Word Texte, Word Struktur) und **Block 08–12** (Excel-Grundlagen, Rechnen und Auswerten, Diagramme, Programme verknüpfen, Abschluss mit Kurzreferenz): je Lerneinheit, Folien, Übungsblatt, Übungsdateien mit Lösungen; Skripte `_werkzeuge/folien-block-NN.py`, `block-NN-docx.js`, `block-NN-xlsx.py`
- **Block 06 „Praxis Outlook und Word“** statt Tagesrückblick (Entscheidung 2026-11-27): durchgehender Fall „Heizung im 3. OG“
- Eigene Dateien der Lernenden liegen jetzt in `Dokumente\Haus-Lichtblick` statt `C:\Kurs\Uebungen` (README nachgeführt)
- Excel-Lösungsdateien: Formeln mit englischen Funktionsnamen in der Datei, Ergebnisse vorberechnet und als zwischengespeicherte Werte eingetragen (`cache_values`), im Skript per `assert` gegen die Lösungen geprüft – Regel in `AGENTS.md`
- `AGENTS.md`: Prüfbefehle für Liquid-Zeichen und Zeitangaben geschärft
- Korrigiert u. a.: Excel-Diagramm wird in Word eingebettet, nicht als Bild eingefügt (Block 11); „Format > Absatz“ → Layout → Abstand (Block 04)

## Nächster Schritt

1. **Block 07 „Selbsttest Outlook und Word“ durchsehen und committen** (Entscheidung 2026-11-27: Übungsblock statt Wiederholung). Uncommittet im Arbeitsverzeichnis: `Grundkurs/Block-07.md`, `Block-07-Uebungsblatt.md`, `_resources/Grundkurs/Block-07/`, `assets/folien/block-07/`, `_werkzeuge/*-block-07.*`, Löschung `Block-07-Leitfaden.md`, dazu angepasste Titel in `Grundkurs/index.md`, `index.md`, `README.md` und „Weiter“ in `Block-05.md`. Vorher die Prüfbefehle aus `AGENTS.md` laufen lassen.
2. Alle Word- und Excel-Dateien einmal in Microsoft 365 öffnen (lokal nur gegen das Schema geprüft bzw. ausgelesen, nicht angesehen), besonders die Diagramme in `Block-10-Loesung-Diagramme.xlsx` und `Block-11-Strom.xlsx`.
3. Die Punkte unter „Vor dem ersten Kurs prüfen“ in `README.md` an einem PC kontrollieren (viele neue Menünamen aus Block 02–11).
4. Push nach Freigabe; danach unter „Actions“ den Pages-Build prüfen.
5. `AGENTS.md` aufräumen: Abschnitte zu „noch nicht umgestellten Blöcken“ betreffen im Grundkurs nichts mehr.
6. Später: Aufbaumodule und Materialien mit Kopfzeilen in die Navigation holen (`defaults` mit `nav_exclude` in `_config.yml` entfernen).

## Offene Entscheidungen

- **Materialien:** Zellbezüge (TechVision) und Pivot-Leitfaden (Online-Shop) ins Szenario Haus Lichtblick übertragen?
- **Veröffentlichung:** In der Wissensbasis `fdoebbelin/Knowledge` trägt die Quelle „Microsoft 365 im Facility Management – Grundkurs und Aufbaumodule“ `draft: true`. Wird der Kurs öffentlich, dort `draft` entfernen.

## Werkzeuge

- npm-Paket `docx@9` und Python mit `openpyxl`, `lxml`, `defusedxml` in einem Arbeitsordner außerhalb des Repositorys (`NODE_PATH` setzen); Word-Dateien mit dem `validate.py` der docx-Skill prüfen; Folien mit `magick` als PNG ansehen
- Block 11: Diagrammbild erst mit `block-11-xlsx.py` als SVG erzeugen, mit `magick` in PNG wandeln, dann `block-11-docx.js … <png>`
