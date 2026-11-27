# 1. Formeln und Funktionen

**Dauer:** 120 Minuten · **Daten:** Mieterliste Haus Lichtblick

## Ausgangsdaten

Übernehmen Sie die Mieterliste aus `00 Referenz Haus Lichtblick.md` in ein Blatt „Mieter“, Zellen A1:F9:

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| 1 | Firma | Etage | Fläche m² | Ansprechpartner | Mietbeginn | Nebenkosten €/Monat |
| 2 | TechSolutions | 1. OG | 420 | Anna Klein | 01.03.2018 | 1260 |
| 3 | DesignWerk | 2. OG | 310 | Michael Braun | 15.07.2019 | 930 |
| 4 | Consulting Plus | 3. OG | 520 | Sarah Meyer | 01.01.2017 | 1560 |
| 5 | Steuerbüro Hahn | 1. OG | 180 | Jürgen Hahn | 01.10.2020 | 540 |
| 6 | Praxis am Park | 2. OG | 260 | Lena Ott | 01.04.2021 | 780 |
| 7 | Lernwerk Akademie | 3. OG | 240 | Tim Rauch | 15.02.2022 | 720 |
| 8 | Kanzlei Berg & Partner | 4. OG | 300 | Nina Berg | 01.09.2016 | 900 |
| 9 | Grünraum Architekten | 1. OG | 150 | Paul Grün | 01.06.2023 | 450 |

Die Übungen schreiben ihre Ergebnisse rechts neben die Tabelle (ab Spalte H). Wer die Liste mit „Als Tabelle formatieren“ angelegt hat, sieht in Formeln statt `C2` oft `[@[Fläche m²]]` – das ist dasselbe, nur mit Spaltennamen. Für die Übungen vorher „Tabellenentwurf“ → „In Bereich konvertieren“ wählen, dann entsprechen die Formeln genau den Beispielen.

## 1. WENN

Die WENN-Funktion prüft eine Bedingung und liefert einen Wert, wenn sie wahr ist, und einen anderen, wenn sie falsch ist.

```
=WENN(Prüfung; Dann_Wert; Sonst_Wert)
```

### Übung

1. H1: „Größe“.
2. H2: `=WENN(C2>=300; "groß"; "klein")`
3. Mit dem Füllkästchen bis H9 kopieren.

Ergebnis: „groß“ bei TechSolutions, DesignWerk, Consulting Plus und Kanzlei Berg & Partner, sonst „klein“.

**Menübefehl:** „Formeln“ → „Logisch“ → „WENN“.

## 2. SUMMEWENN

Summiert nur die Werte, deren Zeile ein Kriterium erfüllt.

```
=SUMMEWENN(Bereich; Kriterium; [Summe_Bereich])
```

### Übung

1. J1: „Etage“, K1: „Fläche gesamt“.
2. J2 bis J5: „1. OG“, „2. OG“, „3. OG“, „4. OG“.
3. K2: `=SUMMEWENN($B$2:$B$9; J2; $C$2:$C$9)` und nach unten kopieren.

Ergebnis: 1. OG 750, 2. OG 570, 3. OG 760, 4. OG 300 m².

Die Dollarzeichen halten die Bereiche fest, während J2 beim Kopieren zu J3, J4 … wird. F4 setzt sie beim Eingeben (siehe `Materialien/Excel/Zellbezüge Handout.md`).

Für mehrere Bedingungen gibt es **SUMMEWENNS**, für das Zählen **ZÄHLENWENN**: `=ZÄHLENWENN(B2:B9; "1. OG")` ergibt 3.

## 3. XVERWEIS

XVERWEIS sucht einen Wert in einer Spalte und gibt den Wert aus derselben Zeile einer anderen Spalte zurück. Er ist in Microsoft 365 der Standard für Nachschlagen und löst SVERWEIS ab.

```
=XVERWEIS(Suchkriterium; Suchmatrix; Rückgabematrix; [wenn_nicht_gefunden]; [Vergleichsmodus]; [Suchmodus])
```

- **Suchkriterium:** was gesucht wird
- **Suchmatrix:** die Spalte, in der gesucht wird
- **Rückgabematrix:** die Spalte, aus der das Ergebnis kommt
- **wenn_nicht_gefunden:** Text statt Fehlermeldung `#NV`
- **Vergleichsmodus:** 0 = exakt (Standard), -1 = exakt oder nächstkleiner, 1 = exakt oder nächstgrößer

### Übung 1: Ansprechpartner zu einer Firma

```
=XVERWEIS("DesignWerk"; A2:A9; D2:D9; "nicht gefunden")
```

Ergebnis: „Michael Braun“. Geben Sie statt „DesignWerk“ einen Zellbezug an (z. B. M2) und tippen Sie verschiedene Firmen in M2.

### Übung 2: Firma zu einer Ansprechpartnerin – Suche nach links

```
=XVERWEIS("Sarah Meyer"; D2:D9; A2:A9)
```

Ergebnis: „Consulting Plus“. Mit SVERWEIS geht das nicht, weil SVERWEIS nur rechts von der Suchspalte zurückgeben kann.

## 4. SVERWEIS

SVERWEIS ist der Vorgänger von XVERWEIS. Man findet ihn in fast jeder älteren Arbeitsmappe, deshalb muss man ihn lesen können.

```
=SVERWEIS(Suchkriterium; Matrix; Spaltenindex; [Bereich_Verweis])
```

- **Matrix:** der ganze Tabellenbereich; gesucht wird immer in dessen **erster** Spalte
- **Spaltenindex:** die wievielte Spalte der Matrix zurückgegeben wird
- **Bereich_Verweis:** FALSCH = exakte Übereinstimmung; WAHR = nächstkleinerer Wert, erste Spalte muss aufsteigend sortiert sein

### Übung 1: Exakte Übereinstimmung

```
=SVERWEIS("DesignWerk"; A2:F9; 4; FALSCH)
```

Ergebnis: „Michael Braun“ – Spalte 4 der Matrix ist „Ansprechpartner“.

### Übung 2: Ungefähre Übereinstimmung – Reinigungsintervall nach Fläche

Legen Sie eine Staffel an (H12:I15):

| ab Fläche m² | Reinigung |
|---|---|
| 0 | 1× pro Woche |
| 200 | 2× pro Woche |
| 400 | täglich |

In G2: `=SVERWEIS(C2; $H$13:$I$15; 2; WAHR)` und nach unten kopieren.

Ergebnis: TechSolutions (420) und Consulting Plus (520) „täglich“, Steuerbüro Hahn (180) und Grünraum (150) „1× pro Woche“, alle anderen „2× pro Woche“. SVERWEIS nimmt jeweils die letzte Stufe, die nicht größer als die Fläche ist.

Dasselbe mit XVERWEIS: `=XVERWEIS(C2; $H$13:$H$15; $I$13:$I$15; ; -1)`

## 5. INDEX und VERGLEICH

Vor XVERWEIS war die Kombination aus INDEX und VERGLEICH der Weg, flexibel – auch nach links – zu suchen. Auch sie begegnet einem in bestehenden Arbeitsmappen.

```
=INDEX(Matrix; Zeile; [Spalte])
=VERGLEICH(Suchkriterium; Suchmatrix; [Vergleichstyp])
```

- **VERGLEICH** liefert die *Position* eines Wertes in einem Bereich (Vergleichstyp 0 = exakt).
- **INDEX** liefert den Wert an einer Position.

### Übung: Welche Firma hat die größte Fläche?

1. `=MAX(C2:C9)` ergibt 520.
2. `=VERGLEICH(520; C2:C9; 0)` ergibt 3 – der dritte Eintrag.
3. `=INDEX(A2:A9; 3)` ergibt „Consulting Plus“.
4. Alles in einer Formel: `=INDEX(A2:A9; VERGLEICH(MAX(C2:C9); C2:C9; 0))`

Zum Vergleich mit XVERWEIS: `=XVERWEIS(MAX(C2:C9); C2:C9; A2:A9)`

## 6. Text verbinden und formatieren

| Funktion | Zweck | Beispiel | Ergebnis |
|---|---|---|---|
| `&` | Texte aneinanderhängen | `=A2&" – "&B2` | TechSolutions – 1. OG |
| TEXTKETTE | wie `&`, auch für Bereiche | `=TEXTKETTE(A2; " – "; B2)` | TechSolutions – 1. OG |
| TEXTVERKETTEN | Bereich mit Trennzeichen verbinden, leere Zellen überspringen | `=TEXTVERKETTEN(", "; WAHR; A2:A4)` | TechSolutions, DesignWerk, Consulting Plus |
| TEXT | Zahl oder Datum als Text formatieren | `=A2&" seit "&TEXT(E2; "MM.JJJJ")` | TechSolutions seit 03.2018 |

VERKETTEN gibt es noch, damit alte Arbeitsmappen funktionieren; in neuen Formeln TEXTKETTE oder `&` verwenden.

### Übung

1. N1: „Firma und Etage“.
2. N2: `=TEXTKETTE(A2; " – "; B2)` und bis N9 kopieren.
3. N11: alle Firmen des 1. OG in einer Zelle – Bonus mit FILTER (siehe `02 Sortieren und Filtern.md`): `=TEXTVERKETTEN(", "; WAHR; FILTER(A2:A9; B2:B9="1. OG"))`

## Zusammenfassung

- **WENN** entscheidet, **SUMMEWENN** und **ZÄHLENWENN** werten mit Bedingung aus.
- **XVERWEIS** ist der Standard zum Nachschlagen; **SVERWEIS** und **INDEX/VERGLEICH** muss man in älteren Mappen lesen können.
- Texte verbindet man mit **&**, **TEXTKETTE** oder **TEXTVERKETTEN**.
