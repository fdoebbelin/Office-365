# 4. Rechnen in Word-Tabellen

**Dauer:** 20 Minuten · **Übung:** Materialbestellung

Word kann in Tabellen einfache Berechnungen ausführen – Summen, Durchschnitte, Produkte. Die Möglichkeiten sind deutlich kleiner als in Excel; für mehr als eine Summenzeile gehört die Tabelle nach Excel (siehe Aufbaumodul „Programme verknüpfen“).

## Eine Formel einfügen

1. In die Zelle klicken, in der das Ergebnis stehen soll.
2. Registerkarte „Layout“ (Tabelle) → Gruppe „Daten“ → **„Formel“**.
3. Im Dialog „Formel“ die Berechnung eingeben und mit „OK“ bestätigen.

Word schlägt oft schon `=SUM(ABOVE)` vor. Die Funktionsnamen in Word-Formeln sind englisch – auch im deutschen Word.

## Bezüge auf Zellen

**Richtungsangaben** beziehen sich auf alle Zahlen in einer Richtung, bis zur ersten leeren Zelle oder zum Tabellenrand:

| Angabe | Bedeutung | Beispiel |
|---|---|---|
| `ABOVE` | Zellen darüber | `=SUM(ABOVE)` |
| `BELOW` | Zellen darunter | `=SUM(BELOW)` |
| `LEFT` | Zellen links | `=SUM(LEFT)` |
| `RIGHT` | Zellen rechts | `=SUM(RIGHT)` |

**Zelladressen wie in Excel:** Spalten heißen A, B, C …, Zeilen 1, 2, 3 …; die erste Zelle oben links ist A1.

```
=SUM(D2;D3;D4)
=SUM(D2:D4)
=B2*C2
```

Einzelne Zellen werden im deutschen Word mit Semikolon getrennt, Bereiche mit Doppelpunkt gebildet.

## Unterschiede zu Excel

- **Keine automatische Aktualisierung:** Ändert sich eine Zahl, bleibt das Ergebnis stehen. Formel markieren und **F9** drücken; für alle Formeln: Strg+A, dann F9.
- **Wenige Funktionen:** u. a. SUM, AVERAGE, MIN, MAX, PRODUCT, COUNT.
- **Formeln lassen sich nicht kopieren** und passen sich nicht an wie in Excel.

Die Formel ist ein Feld – mit **Alt+F9** sieht man den Feldcode, z. B. `{ =SUM(ABOVE) }` (siehe `05 Feldfunktionen.md`).

## Übung: Materialbestellung

Legen Sie eine Bestellung für den Lagerraum EG-01 an:

| Artikel | Menge | Einzelpreis € | Gesamt € |
|---|---|---|---|
| Glasreiniger | 10 | 3,20 | |
| Einweghandschuhe (Paket) | 8 | 6,50 | |
| Allzweckreiniger | 5 | 2,80 | |
| **Summe** | | | |

1. Berechnen Sie „Gesamt“ in jeder Zeile mit einer Formel (z. B. `=B2*C2`).
2. Berechnen Sie die Summe mit `=SUM(ABOVE)`.
3. Ändern Sie die Menge Glasreiniger auf 12 und aktualisieren Sie die Ergebnisse mit F9.
4. Wählen Sie im Dialog „Formel“ unter „Zahlenformat“ ein Format mit zwei Nachkommastellen.
