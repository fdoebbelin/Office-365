# 3. Bedingte Formatierung

**Dauer:** 60 Minuten · **Daten:** Energieverbrauch und Inventar aus `00 Referenz Haus Lichtblick.md`

Bedingte Formatierung ändert das Aussehen einer Zelle abhängig von ihrem Inhalt: Was auffallen soll, fällt auf – und ändert sich mit, wenn sich die Zahlen ändern.

Alle Befehle: „Start“ → Gruppe „Formatvorlagen“ → **„Bedingte Formatierung“**.

## Übung 1: Mehr- und Minderverbrauch Strom

### Daten

Übernehmen Sie die Tabelle „Energieverbrauch 2025“ aus der Referenzliste in A1:C13 (Monat, Zählerstand, Verbrauch). In D1 „Veränderung zum Vormonat“, in D3 `=C3-C2`, nach unten bis D13 kopieren.

### Regel für Mehrverbrauch (rot)

1. D3:D13 markieren.
2. „Bedingte Formatierung“ → „Regeln zum Hervorheben von Zellen“ → „Größer als…“.
3. Wert `0`, Format „Hellrote Füllung“ oder „Benutzerdefiniertes Format…“ → Registerkarte „Ausfüllen“ → Rot.
4. „OK“.

### Regel für Einsparung (grün)

1. D3:D13 bleibt markiert.
2. „Bedingte Formatierung“ → „Regeln zum Hervorheben von Zellen“ → „Kleiner als…“.
3. Wert `0`, Format „Grüne Füllung mit dunkelgrüner Schrift“.
4. „OK“.

### Ergebnis

Februar bis August sind grün (der Verbrauch sinkt zum Sommer), September bis Dezember rot. Ein Wert von genau 0 bliebe ohne Farbe.

### Regeln verwalten

„Bedingte Formatierung“ → **„Regeln verwalten…“** zeigt alle Regeln des markierten Bereichs bzw. des Blatts („Formatierungsregeln anzeigen für: Dieses Arbeitsblatt“). Hier lassen sich Regeln bearbeiten, löschen und in der Reihenfolge verschieben.

## Übung 2: Inventar unter Mindestmenge

### Daten

Übernehmen Sie die Inventarliste aus der Referenz in A1:E11 (Artikel, Lagerort, Bestand, Mindestmenge, Einheit).

### Regel mit Formel – die ganze Zeile färben

1. A2:E11 markieren (ohne Überschrift). Die aktive Zelle ist A2.
2. „Bedingte Formatierung“ → „Neue Regel…“ → **„Formel zur Ermittlung der zu formatierenden Zellen verwenden“**.
3. Formel: `=$C2<$D2`
4. „Formatieren…“ → „Ausfüllen“ → Hellrot → „OK“ → „OK“.

Das Dollarzeichen vor C und D hält die Spalten fest, die Zeile bleibt beweglich: Jede Zelle einer Zeile prüft den Bestand derselben Zeile. Ergebnis: Glasreiniger (8 von 10) und Einweghandschuhe (5 von 10) werden rot.

Ändern Sie den Bestand Glasreiniger auf 12 – die Zeile wird sofort wieder weiß.

## Weitere Regeln zum Ausprobieren

- **Datenbalken:** Verbrauch C2:C13 markieren → „Bedingte Formatierung“ → „Datenbalken“ – ein kleines Balkendiagramm in den Zellen.
- **Farbskalen:** grün bis rot nach Höhe des Werts.
- **Obere/untere Regeln:** z. B. die drei Monate mit dem höchsten Verbrauch.

Weiter mit `03a Wochenenden hervorheben.md`.
