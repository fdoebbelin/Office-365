# 2. Sortieren und Filtern

**Dauer:** 60 Minuten · **Daten:** Mieterliste Haus Lichtblick (A1:F9, siehe `01 Formeln und Funktionen.md`)

## Daten sortieren

### Einfache Sortierung

1. Eine Zelle in der Spalte anklicken, nach der sortiert werden soll – Excel erkennt die zusammenhängende Liste selbst.
2. „Daten“ → Gruppe „Sortieren und Filtern“ → „Von A bis Z“ / „Von Z bis A“ (bei Zahlen: aufsteigend / absteigend).

Achtung: Nie nur eine Spalte markieren und sortieren – dann werden die Zeilen auseinandergerissen. Excel warnt in diesem Fall; „Markierung erweitern“ wählen.

### Übung 1: Nach Fläche sortieren

Sortieren Sie die Mieterliste nach „Fläche m²“, größte zuerst. Oben steht danach Consulting Plus (520), unten Grünraum Architekten (150).

### Mehrstufige Sortierung

1. Eine Zelle in der Liste anklicken.
2. „Daten“ → „Sortieren“.
3. Im Dialog „Sortieren“:
   - Erste Ebene: „Etage“, „Zellwerte“, „A bis Z“.
   - „Ebene hinzufügen“: „Fläche m²“, „Zellwerte“, „Nach Größe (absteigend)“.
   - „Daten haben Überschriften“ muss angehakt sein.
4. „OK“.

### Übung 2

Sortieren Sie nach Etage und innerhalb jeder Etage nach Fläche absteigend. Im 1. OG steht danach TechSolutions vor Steuerbüro Hahn und Grünraum Architekten.

## Daten filtern (AutoFilter)

1. Eine Zelle in der Liste anklicken.
2. „Daten“ → „Filtern“ (oder Strg+Umschalt+L). In jeder Spaltenüberschrift erscheint ein Dropdown-Pfeil.
3. Pfeil anklicken → „(Alle auswählen)“ abwählen → gewünschte Werte anhaken → „OK“.

Gefilterte Zeilen sind nur ausgeblendet, nicht gelöscht. Die Zeilennummern werden blau, und der Pfeil wird zum Trichter.

### Übung 3: Nur das 2. OG

Filtern Sie die Spalte „Etage“ auf „2. OG“. Es bleiben DesignWerk und Praxis am Park.

### Übung 4: Zahlenfilter

1. Filter der Spalte „Etage“ wieder aufheben (Trichter → „Filter löschen aus …“).
2. Spalte „Fläche m²“ → „Zahlenfilter“ → „Größer als…“ → 250 → „OK“.

Es bleiben TechSolutions, DesignWerk, Consulting Plus, Praxis am Park und Kanzlei Berg & Partner.

3. Alle Filter auf einmal aufheben: „Daten“ → „Löschen“.

## Sortieren und Filtern mit Formeln (dynamische Arrays)

In Microsoft 365 können Formeln mehrere Zellen auf einmal füllen. Man schreibt die Formel in **eine** Zelle, Excel lässt das Ergebnis nach unten und rechts „überlaufen“. Der Vorteil gegenüber dem AutoFilter: Die Ausgangsliste bleibt unverändert, und das Ergebnis aktualisiert sich bei jeder Änderung.

| Funktion | Zweck | Beispiel |
|---|---|---|
| FILTER | Zeilen, die eine Bedingung erfüllen | `=FILTER(A2:D9; B2:B9="1. OG"; "keine")` |
| SORTIEREN | sortierte Kopie | `=SORTIEREN(A2:C9; 3; -1)` – nach der 3. Spalte, absteigend |
| EINDEUTIG | jeden Wert nur einmal | `=EINDEUTIG(B2:B9)` – die vier Etagen |

Steht im Überlaufbereich schon etwas, zeigt Excel `#ÜBERLAUF!`. Den Bereich freiräumen, dann erscheint das Ergebnis.

### Übung 5

1. In H2: `=FILTER(A2:C9; C2:C9>250; "keine")` – vergleichen Sie mit Übung 4.
2. In H12: `=SORTIEREN(EINDEUTIG(B2:B9))` – eine sortierte Liste der Etagen.
3. Ändern Sie die Fläche von Grünraum Architekten auf 280 und beobachten Sie, wie sich das Ergebnis aus Schritt 1 sofort anpasst.
