# 2. Excel-Tabelle in Word

**Dauer:** 60 Minuten · **Übung:** Kassenbericht März für die Hausverwaltung

Das Kassenbuch aus Übung 1 soll in einen Word-Bericht. Dafür gibt es drei Wege, die sich darin unterscheiden, ob die Daten später noch mit Excel verbunden sind. Welcher passt, zeigt `02a Einbetten oder verknüpfen.md`.

Für alle drei Wege zuerst in Excel den Bereich markieren (z. B. A1:D7) und mit **Strg+C** kopieren. Dann in Word den Cursor an die Zielstelle setzen.

## Methode 1: Als Word-Tabelle einfügen (ohne Verbindung)

- **Strg+V** in Word.
- Am Ende der eingefügten Tabelle erscheint die Schaltfläche „Einfügeoptionen“ (Strg). Die Wahl:
  - **Ursprüngliche Formatierung beibehalten** – sieht aus wie in Excel
  - **Zielformatvorlagen verwenden** – passt sich dem Word-Dokument an
  - **Nur den Text übernehmen** – Tabulatoren statt Tabelle

Ergebnis: eine normale Word-Tabelle. Zahlen sind jetzt Text; ändert sich das Kassenbuch, muss man neu kopieren.

## Methode 2: Als eingebettetes Excel-Objekt

1. „Start“ → Pfeil unter „Einfügen“ → **„Inhalte einfügen…“** (oder Strg+Alt+V).
2. Option **„Einfügen“** wählen.
3. Als: **„Microsoft Excel-Arbeitsblatt-Objekt“** → „OK“.

Ergebnis: Ein Stück Excel steckt im Word-Dokument. Doppelklick öffnet es zum Bearbeiten mit Excel-Menüs direkt in Word; Formeln rechnen weiter. Mit der ursprünglichen Excel-Datei ist es nicht mehr verbunden.

## Methode 3: Als verknüpftes Excel-Objekt

1. „Start“ → Pfeil unter „Einfügen“ → „Inhalte einfügen…“.
2. Option **„Verknüpfung einfügen“** wählen.
3. Als: „Microsoft Excel-Arbeitsblatt-Objekt“ → „OK“.

Ergebnis: Word zeigt den Bereich an, die Daten bleiben in der Excel-Datei. Ändert man das Kassenbuch, übernimmt Word die Änderung – beim Öffnen des Dokuments fragt Word, ob verknüpfte Daten aktualisiert werden sollen. Von Hand: Rechtsklick auf das Objekt → „Verknüpfung aktualisieren“.

Alle Verknüpfungen eines Dokuments: „Datei“ → „Informationen“ → „Verknüpfungen mit Dateien bearbeiten“ (erscheint nur, wenn es Verknüpfungen gibt). Dort lässt sich auch die Quelle ändern, wenn die Excel-Datei verschoben wurde.

Die Einfügeoptionen von Methode 1 bieten dasselbe in kurz: „Verknüpfen und ursprüngliche Formatierung beibehalten“ fügt eine verknüpfte Tabelle ein, die beim Aktualisieren neue Werte holt.

## Diagramme

Ein Excel-Diagramm wird mit Strg+C / Strg+V ebenfalls eingefügt; die Einfügeoptionen bieten „Arbeitsmappe einbetten“, „Daten verknüpfen“ oder „Bild“. Für einen Bericht, der so bleiben soll, ist **Bild** am robustesten.

## Übung: Kassenbericht März

1. Neues Word-Dokument „Kassenbericht März 2026“ mit Überschrift und einem Satz Einleitung.
2. Fügen Sie das Kassenbuch als **verknüpftes Objekt** ein.
3. Speichern Sie Word- und Excel-Datei im selben Ordner.
4. Tragen Sie im Kassenbuch eine neue Ausgabe ein (z. B. 28.03.2026, Werkzeug, Bithalter, -8,90) – Achtung: Die Verknüpfung umfasst nur den ursprünglich kopierten Bereich. Fügen Sie die Zeile deshalb *innerhalb* des Bereichs ein (Zeile 7 einfügen), nicht darunter.
5. Speichern Sie Excel, wechseln Sie zu Word und aktualisieren Sie die Verknüpfung.
6. Fügen Sie dieselbe Tabelle ein zweites Mal als **Word-Tabelle** (Methode 1) ein und vergleichen Sie: Welche ändert sich, welche nicht?
