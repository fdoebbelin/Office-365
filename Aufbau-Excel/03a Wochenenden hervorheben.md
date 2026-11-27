# 3a. Wochenenden hervorheben

**Ziel:** Im Wartungskalender von Haus Lichtblick sollen Samstage und Sonntage farbig erscheinen, damit niemand eine Wartung auf ein Wochenende legt.

## Übung 1: Datumsreihe erstellen

1. Neues Blatt „Wartungskalender“.
2. A1: „Datum“, B1: „Wartung“.
3. A2: `01.05.2026`.
4. Füllkästchen von A2 nach unten bis A32 ziehen – Excel füllt die Tage bis 31.05.2026.

## Übung 2: Regel für Wochenenden

1. A2:A32 markieren.
2. „Start“ → „Bedingte Formatierung“ → „Neue Regel…“.
3. „Formel zur Ermittlung der zu formatierenden Zellen verwenden“.
4. Formel:

   ```
   =WOCHENTAG(A2;2)>5
   ```

   - `WOCHENTAG(A2;2)` liefert den Wochentag mit Montag = 1 bis Sonntag = 7.
   - `>5` trifft also Samstag (6) und Sonntag (7).

5. „Formatieren…“ → „Ausfüllen“ → Hellgrau oder Hellrot → „OK“ → „OK“.

Ergebnis: Der 2., 3., 9., 10., 16., 17., 23., 24., 30. und 31. Mai 2026 sind markiert.

## Übung 3: Bereich erweitern

1. Datumsreihe bis zum 31.12.2026 verlängern (Füllkästchen bis Zeile 246).
2. „Bedingte Formatierung“ → „Regeln verwalten…“ → Regel auswählen.
3. In der Spalte **„Wird angewendet auf“** den Bereich auf `=$A$2:$A$246` ändern → „Übernehmen“ → „OK“.
4. Prüfen, dass auch im Dezember die Wochenenden markiert sind.

Tipp: Wer die Datumsliste von Anfang an mit „Als Tabelle formatieren“ anlegt, muss den Bereich nicht nachziehen – die Regel wächst mit der Tabelle mit.

## Übung 4 (Bonus): Wartungstage eintragen

1. In Spalte B für jeden ersten Montag im Monat „Heizungswartung“ eintragen.
2. Zweite Regel für A2:A246: `=B2<>""` mit blauer Schrift – Tage mit Wartung fallen zusätzlich auf.
