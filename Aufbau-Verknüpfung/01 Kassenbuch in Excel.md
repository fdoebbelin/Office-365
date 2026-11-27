# 1. Kassenbuch in Excel

**Dauer:** 75 Minuten · **Übung:** Hausmeisterkasse Haus Lichtblick

Der Hausmeister bezahlt Kleinigkeiten bar aus einer Kasse, die die Hausverwaltung regelmäßig auffüllt. Das Kassenbuch soll Fehleingaben verhindern und auf einen Blick zeigen, was hereinkam und was hinausging.

## Ausgangsdaten

Neue Arbeitsmappe, Blatt „Kasse“, Überschriften in A1:D1: **Datum**, **Kategorie**, **Beschreibung**, **Betrag €**.

| Datum | Kategorie | Beschreibung | Betrag € |
|---|---|---|---|
| 02.03.2026 | Einzahlung | Kasse aufgefüllt durch Hausverwaltung | 300,00 |
| 04.03.2026 | Ersatzteile | Leuchtmittel Flur EG | -24,90 |
| 07.03.2026 | Reinigungsmittel | Glasreiniger, Notkauf | -12,80 |
| 10.03.2026 | Werkzeug | Entlüftungsschlüssel Heizkörper | -6,50 |
| 16.03.2026 | Büromaterial | Laminierfolien für Aushänge | -9,99 |
| 25.03.2026 | Ersatzteile | Dichtungen Teeküche 2. OG | -4,60 |

## 1. Bedingte Formatierung

### Wochenenden markieren

1. A2:A100 markieren.
2. „Start“ → „Bedingte Formatierung“ → „Neue Regel…“ → „Formel zur Ermittlung der zu formatierenden Zellen verwenden“.
3. Formel: `=WOCHENTAG(A2;2)>5`
4. „Formatieren…“ → hellrote Füllung → „OK“.

Der 07.03.2026 ist ein Samstag und wird markiert – eine Ausgabe am Wochenende, die man nachfragen sollte.

### Einnahmen grün, Ausgaben rot

1. D2:D100 markieren.
2. „Bedingte Formatierung“ → „Regeln zum Hervorheben von Zellen“ → „Größer als…“ → `0` → grüne Füllung.
3. Noch einmal mit „Kleiner als…“ → `0` → hellrote Füllung.

## 2. Datenüberprüfung: Beträge zwischen -500 und 500 €

Die Kasse enthält nie mehr als 500 €. Größere Beträge sind Tippfehler.

1. D2:D100 markieren.
2. „Daten“ → Gruppe „Datentools“ → **„Datenüberprüfung“**.
3. Registerkarte „Einstellungen“: Zulassen „Dezimal“, Daten „zwischen“, Minimum `-500`, Maximum `500`.
4. Registerkarte „Fehlermeldung“: Titel „Betrag prüfen“, Text „Beträge der Hausmeisterkasse liegen zwischen -500 und 500 €.“
5. „OK“. Testen Sie mit `2490` statt `-24,90`.

## 3. Datenüberprüfung: Kategorie aus einer Liste

### Schritt 1: Kategorienliste auf eigenem Blatt

1. Neues Blatt „Kategorien“.
2. A1 bis A5: Einzahlung, Reinigungsmittel, Ersatzteile, Werkzeug, Büromaterial.
3. A1:A5 markieren → ins **Namenfeld** links über Spalte A „Kategorien“ tippen → Enter.
   (Alternativ: „Formeln“ → „Namens-Manager“ → „Neu…“.)

### Schritt 2: Auswahlliste einrichten

1. Zurück zum Blatt „Kasse“, B2:B100 markieren.
2. „Daten“ → „Datenüberprüfung“.
3. Zulassen „Liste“, Quelle `=Kategorien`.
4. „OK“. In Spalte B erscheint jetzt ein Auswahlpfeil; andere Eingaben weist Excel ab.

Neue Kategorie? Auf dem Blatt „Kategorien“ eine Zeile einfügen *innerhalb* des Bereichs (z. B. vor A5) – dann wächst der Name mit.

## 4. Schützen

### Blatt „Kategorien“ ausblenden

Rechtsklick auf den Blattreiter „Kategorien“ → „Ausblenden“.

Ausgeblendet heißt nicht geschützt: Jeder kann es über Rechtsklick → „Einblenden…“ zurückholen.

### Arbeitsmappe schützen – gegen Einblenden und Löschen von Blättern

1. „Überprüfen“ → Gruppe „Schützen“ → **„Arbeitsmappe schützen“**.
2. „Struktur“ angehakt lassen, Kennwort vergeben (optional) → „OK“.

Jetzt lässt sich „Kategorien“ nicht mehr einblenden, und Blätter lassen sich weder löschen noch umbenennen.

### Blatt „Kasse“ schützen – Formatierung und Regeln bewahren

1. „Überprüfen“ → **„Blatt schützen“**.
2. Bei den erlaubten Aktionen nur „Nicht gesperrte Zellen auswählen“ zulassen – vorher müssen dafür die Eingabezellen A2:D100 entsperrt werden: markieren → Rechtsklick → „Zellen formatieren…“ → Registerkarte „Schutz“ → Häkchen „Gesperrt“ entfernen.
3. Kennwort (optional) → „OK“.

Jetzt kann man Buchungen eintragen, aber weder Überschriften noch Regeln verändern.

Ein Kennwort, das man vergisst, lässt sich nicht wiederherstellen. Im Kurs ohne Kennwort arbeiten.
