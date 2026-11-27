# Microsoft 365 – Outlook, Word und Excel im Facility Management

Kursmaterial für Einsteigerinnen und Einsteiger: ein **Grundkurs** mit zwölf Blöcken und drei **Aufbaumodule**, zum **Selbststudium** und für das **Einzelcoaching**, ohne festen Zeitplan. Alle Übungen spielen im Szenario **Haus Lichtblick**, einem Berliner Bürogebäude, das die Lernenden als Koordination des Facility Managements betreuen.

## Aufbau

| Teil | Inhalt |
|---|---|
| [Grundkurs](Grundkurs/) | Block 01–12: Orientierung, Outlook (E-Mail, Kalender), Word (Texte, Struktur), Excel (Eingabe, Formeln, Auswertung, Diagramme), Programme verknüpfen, Abschluss mit Ausblick auf Copilot |
| [Aufbau-Word](Aufbau-Word/) | Absätze, Bilder, Tabellen, Rechnen in Tabellen, Felder, Kopf- und Fußzeilen, Formatvorlagen und Inhaltsverzeichnis, Dokumentvorlagen, Geschäftsbrief nach DIN 5008 |
| [Aufbau-Excel](Aufbau-Excel/) | WENN, SUMMEWENN, XVERWEIS, SVERWEIS, INDEX/VERGLEICH, Text verbinden, Sortieren und Filtern mit dynamischen Arrays, bedingte Formatierung, Pivot-Tabellen |
| [Aufbau-Verknüpfung](Aufbau-Verknüpfung/) | Kassenbuch mit Datenüberprüfung und Schutz, Excel-Tabellen in Word einfügen, einbetten oder verknüpfen, Serien-E-Mail |
| [Materialien](Materialien/) | Nachschlage- und Vertiefungsmaterial: Oberflächen, Befehle, Begriffe, Zellbezüge (Handout, Arbeitsblatt, Dozentenfassung), Diagramme, Dozentenleitfaden Pivot-Tabellen |

Jeder Block des Grundkurses wird zu einer **Lerneinheit** auf einer Seite: Erklärungen mit Folienabbildungen, Schritt-für-Schritt-Anleitungen, farbige Hinweiskästen, Selbstcheck und Hinweise für Coaching. Dazu gehören ein **Übungsblatt** (als Seite und als Word-Datei) und **Übungsdateien** in Word und Excel. Umgestellt sind bisher **Block 01 bis 05, 08 und 09**; die übrigen Blöcke haben noch einen Leitfaden mit Zeitplan für Gruppenkurse. Die Aufbaumodule beginnen mit `00 Ablauf.md`.

Die Gebäudedaten, Kontakte, Mieterliste, Inventar, Energieverbrauch und Checklisten des Szenarios stehen in [`00 Referenz Haus Lichtblick.md`](00%20Referenz%20Haus%20Lichtblick.md). Alle Namen, Firmen und Adressen sind erfunden.

## Website und Downloads

Alle Kursunterlagen stehen als Website mit Navigation und Suche auf **<https://fdoebbelin.github.io/Office-365/>** (GitHub Pages, Theme Just the Docs). Im Grundkurs hat jeder Block eine eigene Seite mit allen Unterlagen und den Übungsdateien. Die Startseite listet alle Handouts und Übungsdateien, geordnet nach Modul und im Grundkurs nach Block. Die Word- und Excel-Dateien liegen in [`_resources/`](_resources/) – je Modul ein Ordner, im Grundkurs `_resources/Grundkurs/Block-NN/`. Die Seite listet neue Dateien nach dem Push von selbst auf. Einzelheiten: [`_resources/README.md`](_resources/README.md).

## Version und Umgebung

- **Microsoft 365 Apps** (Word, Excel) als Desktop-Programme auf **Windows 11**
- **Neues Outlook für Windows**; das klassische Outlook nur dort, wo es nötig ist – für den Versand von Serien-E-Mails aus Word (Aufbau-Verknüpfung, Thema 3)
- Standardschrift **Aptos**; Übungsdateien kommen aus dem Ordner „Downloads“, eigene Dateien speichern die Lernenden in `Dokumente\Haus-Lichtblick` (ab Block 04); AutoSpeichern und OneDrive werden erklärt, aber nicht vorausgesetzt
- Menübezeichnungen und Tastenkürzel der **deutschen** Programmversionen
- **Copilot** nur als kurzer Ausblick in Block 12, ohne Übungen

## Vor dem ersten Kurs prüfen

Diese Angaben ließen sich beim Umstellen auf Microsoft 365 nicht an einer laufenden Installation prüfen und sollten auf den Kurs-PCs kontrolliert werden:

- Neues Outlook: Beschriftung der Serien-Schaltfläche im Ereignisfenster („Serie erstellen“ oder „Wiederholen“), des Felds „Teilnehmende einladen“ und der Optionen beim Ändern einer Serie
- Neues Outlook: Pfade in den Einstellungen (Zahnrad) für Zeitzone und Standard-Erinnerung
- Ob Word Serien-E-Mails inzwischen auch über das neue Outlook versenden kann
- Ob das Startmenü auf den Kurs-PCs mittig oder links steht (Windows 11 Taskleistenausrichtung)
- Block 01: Beschriftung „Alle“ im Startmenü, gelbe Leiste „Geschützte Ansicht“ mit „Bearbeitung aktivieren“ beim Öffnen heruntergeladener Dateien
- Block 02 (neues Outlook): Platzhalter „Betreff hinzufügen“, Schaltflächen „Cc“/„Bcc“ rechts neben „An“, Beschriftung „Antworten“, „Allen antworten“, „Weiterleiten“ oben im Lesebereich, Kontextmenü „Neuen Unterordner erstellen“ und „Verschieben“, Ordner „Archiv“ in der Ordnerliste, Menübandoption „Klassisches Menüband“
- Block 03 (neues Outlook): Ansichten „Tag“, „Arbeitswoche“, „Woche“, „Monat“ und „Heute“, Schalter „Ganztägig“, im Seriendialog „Monatlich“ mit „Am ersten Montag“ und Enddatum, Frage „nur dieses Ereignis / ganze Serie“ beim Ändern und Löschen, „Kategorisieren“ im Kontextmenü, Einladung mit „Zusagen“, „Mit Vorbehalt“, „Ablehnen“
- Block 04 (Word): beim ersten Strg+S „Weitere Speicheroptionen“ und „Durchsuchen“, QuickInfo „Alle anzeigen“ für ¶, Registerkarte „Layout“ → „Abstand“ mit „Vor“ und „Nach“
- Block 05 (Word): Tabellen-Registerkarten „Tabellenentwurf“ und „Layout“ (in neueren Versionen evtl. „Tabellenlayout“) mit „Darunter einfügen“ und „Löschen“ → „Zeilen löschen“, Kontextmenü „Neu beginnen mit 1“, Katalog „Tabellenformatvorlagen“
- Block 09 (Excel): im Dialog „Sortieren“ die Reihenfolge „Nach Größe (aufsteigend)“, im Filtermenü „Nach Größe sortieren (aufsteigend)“ und „Von A bis Z sortieren“, Schaltflächen „Dezimalstelle hinzufügen/löschen“, Ergebnis der Schaltfläche „1.000er-Trennzeichen“ (zwei Nachkommastellen?)

## Fehlende Dateien

Die Leitfäden verweisen auf Übungs- und Lösungsdateien, Präsentationen und Handouts, die im Archiv nicht enthalten waren und neu erstellt werden müssen:

- **Folien und Übungsblätter:** die Blöcke 06, 07 und 10 bis 12 – entstehen beim Umstellen auf Lerneinheiten (Folien als SVG, Übungsblatt als Seite und `.docx`)
- **Übungen Grundkurs:** `Uebung-07-Quiz.docx`, `Uebung-13-Energiediagramm.xlsx`, `Uebung-14-Monatsbericht.docx` und `.xlsx`, dazu die Lösungsdateien `Loesung-07` (Quiz) und `Loesung-13`, `Loesung-14`. Sie entstehen beim Umstellen der Blöcke neu nach dem Schema `Block-NN-Thema`.
- **Übungen Aufbau-Word:** `Uebung-A1-Hausordnung.docx`, `Uebung-A7-Betriebshandbuch.docx` – der Text steht jeweils in der Einheit und lässt sich auch abtippen
- **Bild** der früheren Briefvorlage nach DIN 5008

## Arbeiten mit KI-Agenten

Regeln für Coding-Agenten stehen in [`AGENTS.md`](AGENTS.md) (Claude Code liest sie über `CLAUDE.md`), der Stand für die nächste Sitzung in [`HANDOFF.md`](HANDOFF.md).

## Herkunft

Zusammengeführt aus zwei Kursen der früheren Wissensbasis: *Office-Short* (Grundkurs, Office 2019) und *Office-Basics* (Word- und Excel-Sitzungen ohne Versionsbezug). Die Historie beider Ordner ist in diesem Repository erhalten.
