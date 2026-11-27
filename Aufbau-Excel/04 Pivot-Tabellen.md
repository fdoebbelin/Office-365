# 4. Pivot-Tabellen

**Dauer:** 75 Minuten · **Übung:** Wartungskosten Haus Lichtblick im 1. Quartal

Eine Pivot-Tabelle fasst eine lange Liste zusammen – Summen nach Monat, nach Gewerk, nach Etage –, ohne dass man eine einzige Formel schreibt. Durch Ziehen der Felder betrachtet man dieselben Daten aus verschiedenen Blickwinkeln.

Ausführlicher Dozentenleitfaden mit größerem Datensatz, typischen Fehlern und Prüfungsaufgabe: `Materialien/Excel/Pivot-Tabellen Dozentenleitfaden.md`.

## Ausgangsdaten

Blatt „Wartungskosten“, Zellen A1:D11:

| Monat | Gewerk | Etage | Kosten € |
|---|---|---|---|
| Januar | Heizung | EG | 320 |
| Januar | Elektro | 1. OG | 85 |
| Januar | Sanitär | 2. OG | 140 |
| Februar | Heizung | EG | 320 |
| Februar | Aufzug | EG | 450 |
| Februar | Elektro | 3. OG | 60 |
| März | Heizung | EG | 320 |
| März | Sanitär | 1. OG | 95 |
| März | Elektro | 2. OG | 120 |
| März | Brandschutz | 4. OG | 210 |

Regeln für Pivot-taugliche Daten: eine Überschriftenzeile, keine leeren Zeilen oder Spalten, keine Zwischensummen, in jeder Spalte nur eine Art von Inhalt.

## Schritt 1: Pivot-Tabelle einfügen

1. Eine Zelle in den Daten anklicken.
2. „Einfügen“ → **„PivotTable“** → „Aus Tabelle/Bereich“.
3. Im Dialog: Bereich prüfen (`Wartungskosten!$A$1:$D$11`), „Neues Arbeitsblatt“ → „OK“.

Links entsteht eine leere Pivot-Tabelle, rechts der Bereich **„PivotTable-Felder“**. Oben erscheinen die Registerkarten **„PivotTable-Analyse“** und **„Entwurf“**.

Tipp: „Einfügen“ → „Empfohlene PivotTables“ zeigt fertige Vorschläge – gut, um zu sehen, was möglich ist.

## Schritt 2: Felder anordnen

Ziehen Sie im Bereich „PivotTable-Felder“:

- **Monat** in den Bereich „Zeilen“,
- **Gewerk** in den Bereich „Spalten“,
- **Kosten €** in den Bereich „Werte“.

Ergebnis:

| Summe von Kosten € | Aufzug | Brandschutz | Elektro | Heizung | Sanitär | Gesamtergebnis |
|---|---|---|---|---|---|---|
| Januar | | | 85 | 320 | 140 | 545 |
| Februar | 450 | | 60 | 320 | | 830 |
| März | | 210 | 120 | 320 | 95 | 745 |
| **Gesamtergebnis** | **450** | **210** | **265** | **960** | **235** | **2120** |

Die Monate stehen in Kalenderreihenfolge, weil Excel Monatsnamen als benutzerdefinierte Liste kennt.

## Schritt 3: Gestalten

1. In die Pivot-Tabelle klicken.
2. Registerkarte **„Entwurf“** → Katalog „PivotTable-Formate“ → ein Format wählen.
3. Zahlenformat: Rechtsklick auf einen Wert → „Zahlenformat…“ → „Währung“.

## Schritt 4: Filtern

1. **Etage** in den Bereich „Filter“ ziehen.
2. Über der Tabelle erscheint ein Auswahlfeld. „EG“ wählen.

Jetzt zeigt die Tabelle nur noch Kosten im Erdgeschoss: Heizung 960, Aufzug 450.

Anschaulicher sind **Datenschnitte**: „PivotTable-Analyse“ → „Datenschnitt einfügen“ → „Etage“ – Schaltflächen zum Anklicken statt eines Auswahlfelds.

## Schritt 5: Werte anders anzeigen

1. Filter wieder auf „(Alle)“ stellen.
2. Rechtsklick auf einen Wert → „Wertfeldeinstellungen…“ → Registerkarte **„Werte anzeigen als“**.
3. **„% des Spaltenergebnisses“** → „OK“.

Jetzt zeigt jede Spalte, wie sich die Kosten eines Gewerks auf die Monate verteilen; jede Spalte ergibt 100 %. Mit „% des Gesamtergebnisses“ sieht man den Anteil jeder Zelle an allen Kosten (Heizung gesamt: rund 45 %).

## Schritt 6: Aktualisieren

Ändern sich die Ausgangsdaten, rechnet die Pivot-Tabelle **nicht** von selbst neu.

- Rechtsklick in die Pivot-Tabelle → „Aktualisieren“, oder
- „PivotTable-Analyse“ → „Aktualisieren“, oder **Alt+F5**.

Übung: Ändern Sie die Aufzugswartung im Februar auf 480 € und aktualisieren Sie.

Kommen neue Zeilen dazu, erfasst die Pivot-Tabelle sie nur, wenn die Quelle mitwächst. Deshalb die Ausgangsdaten vorher mit „Als Tabelle formatieren“ anlegen – dann reicht „Aktualisieren“.

## Schritt 7 (Bonus): Pivot-Diagramm

1. In die Pivot-Tabelle klicken → „PivotTable-Analyse“ → **„PivotChart“** → „Gestapelte Säulen“ → „OK“.
2. Das Diagramm folgt jedem Filter und Datenschnitt der Pivot-Tabelle.

## Zusammenfassung

- Pivot-Tabellen fassen Listen durch Ziehen von Feldern zusammen: Zeilen, Spalten, Werte, Filter.
- „Werte anzeigen als“ zeigt Anteile statt Summen.
- Nach Änderungen der Daten: aktualisieren.
