# Office-365 – Regeln für KI-Agenten

Dieses Repository enthält den Kurs **„Microsoft 365 – Outlook, Word und Excel im Facility Management“**: einen Grundkurs mit zwölf Blöcken und drei Aufbaumodule für Einsteigerinnen und Einsteiger. Die Unterlagen sind für das **Selbststudium** und das **Einzelcoaching** gedacht und folgen **keinem festen Zeitplan**. Inhalte auf Deutsch. Das Repository ist öffentlich; alle Kursunterlagen erscheinen als Website mit Navigation auf GitHub Pages (<https://fdoebbelin.github.io/Office-365/>), dort gibt es auch die Übungsdateien zum Herunterladen.

Diese Datei ist die **einzige Quelle** für die Regeln. Claude Code liest sie über `CLAUDE.md` (`@AGENTS.md`), andere Agenten (OpenCode, Codex …) lesen sie direkt. Wer eine Regel ändert, ändert sie hier.

## Sitzungen

1. **Zu Beginn** `HANDOFF.md` lesen: Stand, nächster Schritt, offene Entscheidungen. Danach `README.md` für den Überblick.
2. **Während der Arbeit** kleine Schritte, je abgeschlossener Einheit ein Commit (siehe unten).
3. **Am Ende** `HANDOFF.md` nachführen und committen: Stand, Erledigtes, nächster Schritt, offene Entscheidungen. Kurz halten – Details stehen in den Commits.

## Arbeitsweise

- **Erst lesen, dann schreiben.** Vor jeder Änderung den betroffenen Block bzw. die Einheit, die Nachbarblöcke (Verweise „Weiter“!) und `00 Referenz Haus Lichtblick.md` lesen.
- **Nachfragen statt raten.** Neue Blöcke, Umbauten der Struktur oder des Szenarios erst vorschlagen und bestätigen lassen.
- **Nichts erfinden.** Keine Menübefehle, Tastenkürzel oder Funktionen angeben, die nicht sicher stimmen. Ungeprüfte Angaben kennzeichnen und in `README.md` unter „Vor dem ersten Kurs prüfen“ eintragen.
- **Nicht löschen** ohne ausdrückliche Freigabe. Zusammenführen ist erlaubt, wenn es vereinbart ist; die Historie bewahrt das Alte. Vereinbart ist: Beim Umstellen eines Blocks gehen Leitfaden, Handout und Folientexte in der Lerneinheit auf und werden danach entfernt.
- **Kein Push** ohne Freigabe.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `README.md` | Kursübersicht, Version und Umgebung, ungeprüfte Angaben, fehlende Dateien, Herkunft |
| `00 Referenz Haus Lichtblick.md` | **Szenario-Daten**: Gebäude, Räume, Personen, Dienstleister, Mieterliste, Inventar, Energieverbrauch, Wartungsprotokoll, Checklisten |
| `Grundkurs/` | `index.md` (Übersicht), je Block die Lerneinheit `Block-NN.md` und das Übungsblatt `Block-NN-Uebungsblatt.md`; noch nicht umgestellte Blöcke haben stattdessen `Block-NN-Leitfaden.md` und zum Teil `Block-NN-Handout.md` |
| `Aufbau-Word/`, `Aufbau-Excel/`, `Aufbau-Verknüpfung/` | je `00 Ablauf.md` und nummerierte Einheiten `NN Thema.md`, Ergänzungen als `NNa Thema.md` |
| `Materialien/Word/`, `Materialien/Excel/` | Nachschlage- und Vertiefungsmaterial ohne festen Platz im Ablauf |
| `assets/folien/block-NN/` | Folien als SVG-Abbildungen, eingebunden in die Lerneinheit |
| `_resources/` | Word- und Excel-Dateien zum Download, je Modul ein Unterordner |
| `_werkzeuge/` | Skripte, die Folien und Office-Dateien erzeugen (nicht auf der Website) |
| `index.md`, `_config.yml`, `_includes/`, `_sass/` | Startseite, Konfiguration, Bausteine und Farben der Website |
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
- Die Lernenden sind die **Koordination des Facility Managements** im Haus Lichtblick.
- Namen und Adressen sind erfunden. In Übungen, die wirklich E-Mails verschicken, **nur eigene Adressen** der Lernenden verwenden, nie die Szenario-Adressen.
- Rechenergebnisse und Antworten in Übungen (Summen, Filterergebnisse, Pivot-Tabellen, Lösungen) an den Übungsdateien nachprüfen, bevor sie im Text stehen.
- Die Materialien unter `Materialien/` dürfen eigene Beispiele behalten.

### Selbststudium und Coaching

- **Kein Zeitplan:** keine Uhrzeiten, keine Minutenangaben, keine Ablaufpläne, keine Pausen, keine Kurstage. Reihenfolge ergibt sich aus den Blöcken.
- **Keine Gruppenformate:** keine Vorstellungsrunde, kein Flipchart, kein Beamer, keine Partner- oder Gruppenarbeit. Jeder Block führt direkt ins Thema ein.
- **Anrede „Sie“**, gerichtet an die Lernenden. Hinweise für Coaches stehen gesammelt im Kasten „Für Coaching“.
- Didaktischer Stil: kurze Sätze, Alltagsvergleiche, Beispiele aus dem Haus Lichtblick, erst erklären und zeigen (Abbildung), dann Schritt für Schritt, dann selbst üben.

### Lerneinheit im Grundkurs (`Block-NN.md`)

Leitfaden, Handout und Folien eines Blocks sind in **einer** Seite gebündelt. Muster: `Grundkurs/Block-01.md`. Aufbau:

1. Kopfzeile (Front Matter), H1 „Block NN – Thema“ mit `{: .no_toc }`
2. Kurztabelle: Programme, Voraussetzung, Übungsblatt, Übungsdateien
3. Einführung ins Thema (zwei, drei Sätze), Kasten `lernziele`
4. Aufklappbares Inhaltsverzeichnis (`<details>` mit `{:toc}`)
5. Themenabschnitte (`##`): Folienabbildung → Erklärung → Schritt-für-Schritt-Anleitung → Kästen (`merke`, `tipp`, `achtung`, `praxis`)
6. „Jetzt üben“: Kasten `uebung` mit Link zum Übungsblatt, darunter `### Übungsdateien` mit `{: #uebungsdateien }` und dem Baustein `downloads.html`
7. „Häufige Fragen“, „Wenn es hakt“ (Tabelle Problem – Lösung), „Selbstcheck“ (Aufgabenliste `- [ ]`)
8. „Für Coaching“: Kasten `coaching` (Vorbereitung, Tempo, Bildschirm teilen, Erfolg sichtbar machen, Zusatzaufgaben)
9. „Weiter“: Link auf den nächsten Block

### Farbige Kästen (Callouts)

Schreibweise: Zeile `{: .art }` direkt vor einem Absatz oder einem Zitatblock (`> …`). Arten und Titel stehen in `_config.yml` unter `callouts`, die Hintergrundfarben in `_sass/custom/custom.scss`.

| Art | Titel | Farbe | Wofür |
|---|---|---|---|
| `lernziele` | Das lernen Sie | lila | Lernziele am Anfang |
| `merke` | Merke | blau | Begriffe, Regeln, Wichtiges |
| `tipp` | Tipp | grün | Abkürzungen, Tastenkürzel, Alternativen |
| `uebung` | Jetzt üben | grün | Verweis auf Übungsblatt |
| `achtung` | Achtung | rot | Datenverlust, typische Fehler |
| `praxis` | Im Haus Lichtblick | gelb | Beispiele aus dem Szenario |
| `coaching` | Für Coaching | grau | Hinweise für Coaches |

Sparsam einsetzen: höchstens ein, zwei Kästen je Abschnitt.

### Folien als Abbildungen

- Folien sind **SVG-Dateien** in `assets/folien/block-NN/`, Name `NN-thema.svg` (`02-drei-programme.svg`), Format 1280 × 720.
- Einheitliches Layout: dunkelblaue Kopfleiste mit Titel, Fußzeile „Block NN · Thema“ und „Haus Lichtblick – Microsoft 365 · Folie N“, Programmfarben Outlook `#0F6CBD`, Word `#185ABD`, Excel `#107C41`. Keine Logos, keine Bildschirmfotos fremder Herkunft.
- Jede SVG hat `<title>` und `<desc>`; im Markdown ein Alternativtext, der den Inhalt beschreibt: `![Folie: …](../assets/folien/block-NN/NN-thema.svg)`.
- Folien zeigen Schemata und Kernaussagen; der vollständige Text steht in der Lerneinheit. Keine Titelfolie, keine Zusammenfassungsfolie.
- Erzeugt mit `_werkzeuge/folien-block-NN.py`; Änderungen im Skript machen und neu erzeugen, dann als PNG ansehen (z. B. `magick`).

### Übungsblatt und Übungsdateien

- **Jeder Block hat ein eigenes Übungsblatt**: `Grundkurs/Block-NN-Uebungsblatt.md` (Titel „Übungsblatt“, Unterseite der Lerneinheit) **und** dieselben Aufgaben als Word-Datei `Block-NN-Uebungsblatt.docx` zum Ausdrucken. Beide Fassungen inhaltlich gleich halten.
- Aufbau des Übungsblatts: „Sie brauchen“, „Ihre Rolle“ (Situation im Haus Lichtblick), nummerierte Aufgaben mit Schritten, Selbstcheck, Lösungen (auf der Seite aufklappbar, in der Word-Datei auf der letzten Seite).
- **Übungsdateien** sind echte Word- und Excel-Dateien, mit denen die Aufgaben gelöst werden. Namen: `Block-NN-Thema.docx` / `.xlsx`, Lösungsdateien `Block-NN-Loesung-Thema.xlsx`. Ohne Leerzeichen und Umlaute.
- Inhalt nur aus der Referenzliste; Schrift Aptos, A4, Fußzeile mit „Übungsdatei Block NN“ und dem Hinweis, dass Namen erfunden sind.
- Excel-Dateien für Lese- oder Einstiegsübungen mit festen Werten. Formeln nur, wo die Übung sie braucht – heruntergeladene Dateien öffnen in der „Geschützten Ansicht“, ungerechnete Formeln zeigen dort nichts an.
- Erzeugt mit `_werkzeuge/` (`block-NN-docx.js` mit dem npm-Paket `docx`, `block-NN-xlsx.py` mit `openpyxl`). Nach dem Erzeugen prüfen: Word-Dateien gegen das Schema validieren, Excel-Werte auslesen und mit den Lösungen vergleichen.
- Ältere Leitfäden nennen noch Dateien wie `Uebung-11-Energieverbrauch.xlsx`; beim Umstellen des Blocks auf das neue Namensschema wechseln und `README.md` („Fehlende Dateien“) nachführen.

### Noch nicht umgestellte Blöcke und Aufbaumodule

- Blöcke ohne Lerneinheit behalten vorerst Leitfaden (mit Zeitplan) und Handout. Beim Umstellen nach dem Muster von Block 01 vorgehen und den Block in `Grundkurs/index.md` und `HANDOFF.md` als umgestellt vermerken.
- **Einheiten der Aufbaumodule:** Kopfzeile mit Übung → Erklärung mit Menüwegen → Übung im Szenario. Neue Einheiten in `00 Ablauf.md` eintragen. Zeitangaben entfallen beim Umstellen.

### Form

- **Markdown für alle Texte.** Office-Dateien (`.docx`, `.dotx`, `.xlsx`, `.xltx`) nur in `_resources/`, Folien als SVG nur in `assets/folien/`, sonst keine Office-Dateien, Bilder oder PDFs.
- Eine H1-Überschrift je Datei, Gliederung mit `##`/`###`.
- Deutsche Anführungszeichen „…“, Umlaute statt ae/oe/ue (außer in Datei- und Ankernamen), Pfeile → für Menüwege („Einfügen“ → „Tabelle“).

## Website über GitHub Pages

GitHub Pages veröffentlicht den Branch `main` (Ordner `/`) mit Jekyll und dem Theme **Just the Docs** (in `_config.yml` als `remote_theme` auf eine Version gepinnt). Jede Kursdatei ist eine Seite; die Seitenleiste entsteht aus den Kopfzeilen der Dateien.

### Kopfzeilen (Front Matter)

Jede Kursdatei beginnt mit einer Kopfzeile. Sie bestimmt Titel und Platz in der Navigation.

```yaml
---
title: "Übungsblatt"
parent: "Block 01 – Orientierung in Microsoft 365"
grand_parent: "Grundkurs"
nav_order: 1
---
```

- `parent` ist der **Titel** der übergeordneten Seite, wörtlich gleich. Titel von Seiten mit Unterseiten müssen eindeutig sein.
- `nav_order` als Zahl; sie legt die Reihenfolge unter derselben übergeordneten Seite fest.
- Grundkurs: `Grundkurs/index.md` → Lerneinheit `Block-NN.md` (Titel „Block NN – Thema“, `has_children: true`) → Übungsblatt (1); bei nicht umgestellten Blöcken Leitfaden (1), Handout (2).
- Ändert sich Titel oder Programm eines Blocks, auch die Tabelle in `Grundkurs/index.md` und die Verweise „Weiter“ der Nachbarblöcke anpassen.
- `AGENTS.md`, `CLAUDE.md`, `HANDOFF.md`, `README.md` haben keine Kopfzeile und stehen in `_config.yml` unter `exclude`.
- Übergangsweise blendet `_config.yml` (`defaults`) Aufbaumodule und Materialien noch aus der Navigation aus, bis sie Kopfzeilen haben.

### Downloads

- **Zuordnung zum Modul über den Ordner:** `_resources/Grundkurs/Block-NN/`, `_resources/Aufbau-Word/`, `_resources/Aufbau-Excel/`, `_resources/Aufbau-Verknüpfung/`, `_resources/Materialien/`. Ordnernamen genau wie die Modulordner; die Module und ihre Reihenfolge stehen in `_config.yml` unter `module`.
- Die Seiten listen die Dateien selbst auf (Baustein `_includes/downloads.html`): die Startseite alle, jede Lerneinheit die ihres Blocks. Dateien mit „Loesung“ im Namen erscheinen als Lösung.
- Office-Dateien lassen sich nicht als Text prüfen – Inhalt im Commit beschreiben.

### Technik

- **Öffentlich:** Seite und Repository sind öffentlich, Lösungen eingeschlossen (so gewollt).
- Jekyll lässt Ordner mit `_` sonst weg; `_resources` steht deshalb in `_config.yml` unter `include`. `_werkzeuge` bleibt bewusst draußen.
- Kursdateien dürfen kein `{{` oder `{%` enthalten, sonst stört das den Build. Ausnahmen: `index.md` und die Blockseiten `Grundkurs/Block-NN.md` (für `downloads.html` und `relative_url`).
- Anker mit Umlauten sind unzuverlässig; eigene Anker ASCII schreiben (`{: #uebungsdateien }`).
- Nach dem Push zeigt GitHub unter „Actions“ („pages build and deployment“), ob der Build geklappt hat.

## Prüfen vor dem Commit

Es gibt keine automatischen Tests. Vor jedem Commit:

```bash
git -c core.quotePath=false ls-files | grep -vE '\.md$|^_config\.yml$|^_includes/.+\.html$|^_sass/.+\.scss$|^_werkzeuge/.+\.(py|js)$|^assets/folien/.+\.svg$|^_resources/.+\.(docx|dotx|xlsx|xltx)$'   # darf nichts liefern
grep -rn "2019\|2016\|Office 20\|Tabellentools\|Diagrammtools" --include=*.md .   # alte Versionen/Menüs
grep -rn "Strg *+ *[BIU]\b" --include=*.md .                      # englische Kürzel – Treffer einzeln prüfen
grep -rnE "=(SUM|AVERAGE|COUNT|IF|VLOOKUP)\(" --include=*.md Aufbau-Excel Materialien/Excel Grundkurs   # englische Funktionen in Excel
grep -rln "{{\|{%" --include=*.md . | grep -vE '^(\./)?(index|AGENTS)\.md$|^(\./)?Grundkurs/Block-[0-9]{2}\.md$'   # Liquid-Zeichen stören Jekyll – darf nichts liefern
git -c core.quotePath=false ls-files '*.md' | grep -vE '^(AGENTS|CLAUDE|HANDOFF|README)\.md$|^_resources/|^Aufbau-|^Materialien/' | while IFS= read -r f; do head -1 "$f" | grep -qx -- '---' || echo "ohne Kopfzeile: $f"; done   # darf nichts liefern
grep -rnE "[0-9]{1,2}:[0-9]{2}( |–|-)|Minuten|Min\b|Tag [12]\b" Grundkurs/Block-[0-9][0-9].md Grundkurs/*Uebungsblatt.md | grep -vE 'Uhr|Minuten vorher'   # Zeitangaben in Lerneinheiten – darf nichts liefern (Uhrzeiten von Terminen mit „Uhr“ und Erinnerungen sind erlaubt)
```

Dazu: Verweise auf andere Dateien (Dateinamen in Backticks, Links) existieren, Folien und Übungsdateien, die eine Lerneinheit nennt, liegen vor.

## Commits

- Ein Commit je abgeschlossener Einheit (ein Block, eine Einheit, ein Material).
- Nachricht auf Deutsch, erste Zeile `Bereich: was` – z. B. `Grundkurs Block 05: Lerneinheit und Übungsblatt`, `Aufbau-Excel: Einheit Datenüberprüfung`, `Referenz: Wartungskosten Q2`. Im Text, was korrigiert oder bewusst weggelassen wurde.
- Am Ende der Sitzung eigener Commit `handoff: …`.
