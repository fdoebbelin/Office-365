# Aufbaumodul Excel – Ablauf

**Programm:** Microsoft Excel (Microsoft 365)
**Dauer:** ein Kurstag, ca. 6 Stunden ohne Pausen
**Voraussetzung:** Grundkurs Block 08–10 (Eingabe, Formeln, SUMME & Co., Sortieren, AutoFilter, Diagramm)
**Szenario:** Haus Lichtblick – Mieterliste, Inventar, Energieverbrauch und Wartungskosten aus `00 Referenz Haus Lichtblick.md`

## Überblick

| Nr. | Thema | Dauer | Datei |
|---|---|---|---|
| 0 | Begrüßung, Wiederholung, Mieterliste anlegen | 30 Min | – |
| 1 | Formeln und Funktionen: WENN, SUMMEWENN, XVERWEIS, SVERWEIS, INDEX/VERGLEICH, Text verbinden | 120 Min | `01 Formeln und Funktionen.md` |
| 2 | Sortieren und Filtern, dynamische Arrays | 60 Min | `02 Sortieren und Filtern.md` |
| 3 | Bedingte Formatierung | 60 Min | `03 Bedingte Formatierung.md`, `03a Wochenenden hervorheben.md` |
| 4 | Pivot-Tabellen | 75 Min | `04 Pivot-Tabellen.md` |
| – | Fragen, Feedback | 15 Min | – |

Vertiefung zu Zellbezügen (relativ, absolut, gemischt, 3D, extern) und ein ausführlicher Dozentenleitfaden zu Pivot-Tabellen liegen unter `Materialien/Excel/`.

## 0. Einstieg: Mieterliste anlegen

- Wiederholung: Formel beginnt mit `=`, Füllkästchen, relative Bezüge
- Mieterliste aus der Referenz in ein neues Blatt „Mieter“ übernehmen (A1:F9)
- Bereich markieren → „Start“ → „Als Tabelle formatieren“: Kopfzeile mit Filterpfeilen, gebänderte Zeilen, Formeln wachsen mit neuen Zeilen mit

## 1. Formeln und Funktionen

**WENN** – eine Bedingung prüfen und je nach Ergebnis zwei verschiedene Werte liefern:

```
=WENN(Prüfung; Dann_Wert; Sonst_Wert)
=WENN(C2>=300; "groß"; "klein")
```

**SUMMEWENN** – nur die Werte summieren, die ein Kriterium erfüllen:

```
=SUMMEWENN(Bereich; Kriterium; [Summe_Bereich])
=SUMMEWENN(B2:B9; "1. OG"; C2:C9)
```

**XVERWEIS** – einen Wert in einer Spalte suchen und den passenden Wert aus einer anderen Spalte zurückgeben; Nachfolger von SVERWEIS:

```
=XVERWEIS(Suchkriterium; Suchmatrix; Rückgabematrix; [wenn_nicht_gefunden])
=XVERWEIS("DesignWerk"; A2:A9; D2:D9; "nicht gefunden")
```

**TEXTKETTE / TEXTVERKETTEN** – Texte verbinden; ersetzen das ältere VERKETTEN:

```
=TEXTKETTE(A2; " – "; B2)
=TEXTVERKETTEN(", "; WAHR; A2:A9)
```

Menübefehl für alle Funktionen: Registerkarte „Formeln“ → Gruppe „Funktionsbibliothek“ → Kategorie („Logisch“, „Nachschlagen und Verweisen“, „Text“ …) oder „Funktion einfügen“ (fx).

## 2. Sortieren und Filtern

- **Sortieren:** „Daten“ → Gruppe „Sortieren und Filtern“ → „Sortieren“; mehrere Ebenen mit „Ebene hinzufügen“.
- **Filtern:** „Daten“ → „Filtern“; Dropdown-Pfeile in der Kopfzeile; Text- und Zahlenfilter.
- **Mit Formeln:** FILTER, SORTIEREN und EINDEUTIG liefern sortierte oder gefilterte Kopien, die sich bei Änderungen selbst aktualisieren.

## 3. Bedingte Formatierung

- „Start“ → Gruppe „Formatvorlagen“ → „Bedingte Formatierung“.
- Fertige Regeln („Regeln zum Hervorheben von Zellen“, Datenbalken, Farbskalen) und eigene Regeln mit Formel.
- Übungen: Inventar unter Mindestmenge, Mehr- und Minderverbrauch Strom, Wochenenden im Wartungskalender.

## 4. Pivot-Tabellen

- „Einfügen“ → „PivotTable“ → „Aus Tabelle/Bereich“.
- Felder in die Bereiche Filter, Spalten, Zeilen, Werte ziehen.
- Übung: Wartungskosten nach Monat und Gewerk, Anteile als „% des Spaltenergebnisses“, Pivot-Diagramm.

## Abschluss

- Fragen und Feedback
- Ausblick: Aufbaumodul „Programme verknüpfen“ (Kassenbuch, Excel-Tabelle in Word, Serien-E-Mail)
