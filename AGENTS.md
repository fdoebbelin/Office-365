# Office-365 – Regeln für KI-Agenten

Dieses Repository enthält den Kurs **„Microsoft 365 – Outlook, Word und Excel im Facility Management“**: einen zweitägigen Grundkurs und drei Aufbaumodule für Einsteigerinnen und Einsteiger. Inhalte auf Deutsch, Zielgruppe der Materialien sind Lehrkräfte (Leitfäden) und Teilnehmende (Handouts, Übungen). Das Repository ist privat.

Diese Datei ist die **einzige Quelle** für die Regeln. Claude Code liest sie über `CLAUDE.md` (`@AGENTS.md`), andere Agenten (OpenCode, Codex …) lesen sie direkt. Wer eine Regel ändert, ändert sie hier.

## Sitzungen

1. **Zu Beginn** `HANDOFF.md` lesen: Stand, nächster Schritt, offene Entscheidungen. Danach `README.md` für den Überblick.
2. **Während der Arbeit** kleine Schritte, je abgeschlossener Einheit ein Commit (siehe unten).
3. **Am Ende** `HANDOFF.md` nachführen und committen: Stand, Erledigtes, nächster Schritt, offene Entscheidungen. Kurz halten – Details stehen in den Commits.

## Arbeitsweise

- **Erst lesen, dann schreiben.** Vor jeder Änderung den betroffenen Block bzw. die Einheit, die Nachbarblöcke (Übergänge!) und `00 Referenz Haus Lichtblick.md` lesen.
- **Nachfragen statt raten.** Neue Blöcke, Umbauten der Struktur oder des Szenarios erst vorschlagen und bestätigen lassen.
- **Nichts erfinden.** Keine Menübefehle, Tastenkürzel oder Funktionen angeben, die nicht sicher stimmen. Ungeprüfte Angaben kennzeichnen und in `README.md` unter „Vor dem ersten Kurs prüfen“ eintragen.
- **Nicht löschen** ohne ausdrückliche Freigabe. Zusammenführen ist erlaubt, wenn es vereinbart ist; die Historie bewahrt das Alte.
- **Kein Push** ohne Freigabe.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `README.md` | Kursübersicht, Version und Umgebung, ungeprüfte Angaben, fehlende Dateien, Herkunft |
| `00 Referenz Haus Lichtblick.md` | **Szenario-Daten**: Gebäude, Räume, Personen, Dienstleister, Mieterliste, Inventar, Energieverbrauch, Wartungsprotokoll, Checklisten |
| `Grundkurs/` | `Block-NN-Leitfaden.md` für Block 01–12, dazu `Block-NN-Handout.md` und `Block-NN-Praesentation.md` (Folientexte), wo vorhanden |
| `Aufbau-Word/`, `Aufbau-Excel/`, `Aufbau-Verknüpfung/` | je `00 Ablauf.md` und nummerierte Einheiten `NN Thema.md`, Ergänzungen als `NNa Thema.md` |
| `Materialien/Word/`, `Materialien/Excel/` | Nachschlage- und Vertiefungsmaterial ohne festen Platz im Ablauf |
| `AGENTS.md`, `CLAUDE.md`, `HANDOFF.md` | Regeln und Übergabe für Agenten |

## Inhaltliche Regeln

### Version und Umgebung

- **Microsoft 365 Apps** (Word, Excel) als Desktop-Programme auf **Windows 11**, **neues Outlook für Windows**. Das klassische Outlook nur, wo es nötig ist (Serien-E-Mail aus Word), und dann ausdrücklich benennen.
- **Deutsche Oberfläche:** Menü-, Registerkarten- und Dialognamen so, wie sie im deutschen Microsoft 365 heißen („Tabellenentwurf“, „Bildformat“, „Diagrammentwurf“, „PivotTable-Analyse“, „Formatvorlagen“, „Bearbeitungsleiste“, „Namenfeld“).
- **Deutsche Tastenkürzel:** Fett Strg+Umschalt+F, Kursiv Strg+Umschalt+K, Unterstrichen Strg+Umschalt+U, Blocksatz Strg+B. Englische Kürzel (Strg+B/I/U für Schriftschnitte, Strg+J) sind Fehler.
- **Deutsche Funktionsnamen** in Excel (SUMME, MITTELWERT, XVERWEIS, TEXTKETTE …), Argumente mit Semikolon. Ausnahme: Formeln in Word-Tabellen verwenden englische Namen (`=SUM(ABOVE)`).
- **Excel:** XVERWEIS ist der Standard; SVERWEIS und INDEX/VERGLEICH nur, um ältere Mappen lesen zu können. TEXTKETTE/`&` statt VERKETTEN.
- **Copilot** nur als Ausblick (Block 12), keine Übungen, die eine Lizenz voraussetzen.
- Keine Versionsnummern wie „Office 2019“; das Paket heißt „Microsoft 365“.

### Szenario Haus Lichtblick

- Alle Übungen im Grundkurs und in den Aufbaumodulen spielen im Haus Lichtblick. **Daten nur aus der Referenzliste** verwenden; neue Daten (Personen, Firmen, Tabellen) zuerst dort eintragen, dann in den Übungen nutzen.
- Namen und Adressen sind erfunden. In Übungen, die wirklich E-Mails verschicken, **nur Kursadressen** der Teilnehmenden verwenden, nie die Szenario-Adressen.
- Rechenergebnisse in Übungen (Summen, Filterergebnisse, Pivot-Tabellen) nachrechnen, bevor sie im Text stehen.
- Die Materialien unter `Materialien/` dürfen eigene Beispiele behalten.

### Form

- **Nur Markdown.** Keine PDFs, keine Office-Dateien im Repository, solange nicht anders vereinbart. Übungsdateien (`Uebung-…`, `Loesung-…`) sind bisher nur Verweise; welche fehlen, steht in `README.md`.
- Eine H1-Überschrift je Datei, Gliederung mit `##`/`###`.
- **Leitfäden im Grundkurs** behalten ihren Aufbau: Kopftabelle (Block, Titel, Programm, Dauer) → Lernziele → Vorbereitung → Ablaufplan (Tabelle mit Zeit, Minuten, Aktivität, Inhalt, Hinweise) → Inhaltliche Hinweise → Didaktische Hinweise → Übergänge → Notfall-Tipps → Erfolgskontrolle bzw. Bewertungskriterien. Uhrzeiten müssen über die Blöcke hinweg zusammenpassen.
- **Einheiten der Aufbaumodule:** Kopfzeile mit Dauer und Übung → Erklärung mit Menüwegen → Übung im Szenario. Neue Einheiten in `00 Ablauf.md` eintragen.
- Deutsche Anführungszeichen „…“, Umlaute statt ae/oe/ue, Pfeile → für Menüwege („Einfügen“ → „Tabelle“).
- Didaktischer Stil der Zielgruppe: kurze Sätze, Alltagsvergleiche, „Zeigen – Nachmachen – Selbst anwenden“.

## Prüfen vor dem Commit

Es gibt keine automatischen Tests. Vor jedem Commit:

```bash
git -c core.quotePath=false ls-files | grep -v '\.md$'                                # darf nichts liefern
grep -rn "2019\|2016\|Office 20\|Tabellentools\|Diagrammtools" --include=*.md .   # alte Versionen/Menüs
grep -rn "Strg *+ *[BIU]\b" --include=*.md .                      # englische Kürzel – Treffer einzeln prüfen
grep -rnE "=(SUM|AVERAGE|COUNT|IF|VLOOKUP)\(" --include=*.md Aufbau-Excel Materialien/Excel Grundkurs   # englische Funktionen in Excel
```

Dazu: Verweise auf andere Dateien (Dateinamen in Backticks) existieren, Übergänge zwischen Blöcken passen noch.

## Commits

- Ein Commit je abgeschlossener Einheit (ein Block, eine Einheit, ein Material).
- Nachricht auf Deutsch, erste Zeile `Bereich: was` – z. B. `Grundkurs Block 05: Handout ergänzt`, `Aufbau-Excel: Einheit Datenüberprüfung`, `Referenz: Wartungskosten Q2`. Im Text, was korrigiert oder bewusst weggelassen wurde.
- Am Ende der Sitzung eigener Commit `handoff: …`.
