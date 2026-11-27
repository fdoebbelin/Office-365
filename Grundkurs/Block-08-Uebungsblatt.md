---
title: "Übungsblatt"
parent: "Block 08 – Excel-Grundlagen"
grand_parent: "Grundkurs"
nav_order: 1
---

# Übungsblatt Block 08 – Excel-Grundlagen

**Sie brauchen:** einen PC mit Excel und die Übungsdatei `Block-08-Inventarliste.xlsx` von der [Seite zu Block 08](Block-08.md#uebungsdateien). Die Lösungsdatei `Block-08-Loesung-Inventarliste.xlsx` zeigt die fertige Liste – sehen Sie sie erst am Ende an. Das Übungsblatt gibt es auf der Seite auch als Word-Datei zum Ausdrucken.

**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Maria Schmidt aus der Reinigung hat angefangen, das Reinigungsmaterial im Lagerraum EG-01 zu zählen, und die ersten fünf Artikel eingetragen. Sie ergänzen den Rest und finden heraus, was nachbestellt werden muss.

## Aufgabe 1 – Excel erkunden

1. Öffnen Sie `Block-08-Inventarliste.xlsx` aus dem Ordner Downloads und klicken Sie auf **„Bearbeitung aktivieren“**.
2. Suchen Sie Namenfeld, Bearbeitungsleiste, Spaltenköpfe, Zeilennummern und das Tabellenblatt „Inventar“.
3. Klicken Sie auf die Zelle **C5**. Was steht im Namenfeld, was in der Bearbeitungsleiste?

## Aufgabe 2 – Sich bewegen

1. Klicken Sie ins **Namenfeld**, tippen Sie `C9` und drücken Sie **Enter**. Welche Zahl steht dort, und zu welchem Artikel gehört sie?
2. Drücken Sie **Strg+Pos1**. Wo sind Sie jetzt?
3. Klicken Sie auf **A4** und drücken Sie **Strg+Pfeil nach unten**. In welcher Zeile landen Sie?

## Aufgabe 3 – Unter eigenem Namen speichern

Speichern Sie die Datei mit **„Datei“** → **„Speichern unter“** → **„Durchsuchen“** in `Dokumente\Haus-Lichtblick` unter dem Namen `Inventarliste`.

## Aufgabe 4 – Daten eingeben

1. Klicken Sie auf **B2** (neben „Stand:“) und tippen Sie das heutige Datum mit Punkten, zum Beispiel `15.04.2025`. Drücken Sie **Enter**.
2. Tragen Sie ab Zeile 10 die übrigen fünf Artikel ein. Springen Sie mit **Tab** nach rechts; nach der letzten Zelle einer Zeile bringt Sie **Enter** an den Anfang der nächsten.

| Artikel | Lagerort | Bestand | Mindestmenge | Einheit |
|---|---|---|---|---|
| Bodenreiniger | Lagerraum EG-01 | 12 | 8 | Flaschen |
| Desinfektionsmittel | Lagerraum EG-01 | 6 | 5 | Flaschen |
| Schwämme | Lagerraum EG-01 | 25 | 20 | Stück |
| Einweghandschuhe | Lagerraum EG-01 | 5 | 10 | Pakete |
| Wischmopps | Lagerraum EG-01 | 4 | 3 | Stück |

3. Prüfen Sie: Stehen alle Zahlen rechts in der Zelle? Steht eine links, ist sie als Text eingegeben – neu tippen.

## Aufgabe 5 – Spaltenbreite und Kopfzeile

1. Markieren Sie die Spaltenköpfe **A bis E** und doppelklicken Sie auf eine Trennlinie zwischen zwei Spaltenköpfen. Alle Spalten passen sich an.
2. Markieren Sie die Kopfzeile **A4 bis E4** und machen Sie sie **fett** (Strg+Umschalt+F).
3. Geben Sie der Kopfzeile eine helle **Füllfarbe**.

## Aufgabe 6 – Die erste Formel

1. Tippen Sie in **F4** die Überschrift `Differenz`. Formatieren Sie sie wie die übrige Kopfzeile.
2. Klicken Sie auf **F5** und geben Sie die Formel ein: **=** tippen, **C5** anklicken, **-** tippen, **D5** anklicken, **Enter**.
3. Schauen Sie in die Bearbeitungsleiste von F5: Dort steht `=C5-D5`, in der Zelle das Ergebnis.
4. Geben Sie die Formel genauso für die Zeilen 6 bis 14 ein – in jeder Zeile mit den Zellen dieser Zeile (`=C6-D6`, `=C7-D7` …).

## Aufgabe 7 – Auswerten

1. Welche Artikel haben eine **negative** Differenz und müssen nachbestellt werden?
2. Bei welchem Artikel ist am meisten über der Mindestmenge?
3. Eine Lieferung kommt: 4 Flaschen Glasreiniger. Ändern Sie den Bestand von Glasreiniger auf `12`. Was zeigt jetzt die Differenz?
4. Machen Sie die Änderung mit **Strg+Z** rückgängig – die Lieferung war nur eine Übung.
5. Speichern Sie mit **Strg+S** und vergleichen Sie mit der Lösungsdatei.

## Selbstcheck

- [ ] Ich habe Namenfeld und Bearbeitungsleiste gefunden und mit dem Namenfeld eine Zelle angesprungen.
- [ ] Ich habe Text, Zahlen und ein Datum eingegeben.
- [ ] Ich habe Spaltenbreiten angepasst und die Kopfzeile hervorgehoben.
- [ ] Ich habe eine Formel mit Zelladressen eingegeben.
- [ ] Ich habe gesehen, dass Excel neu rechnet, wenn sich eine Zahl ändert.

## Lösungen

<details markdown="block">
<summary>Lösungen zu den Aufgaben 1, 2, 6 und 7 anzeigen</summary>

**Aufgabe 1** – Im Namenfeld steht `C5`, in der Bearbeitungsleiste `15` (Bestand Allzweckreiniger).

**Aufgabe 2**

1. In C9 steht **8** – der Bestand von Glasreiniger.
2. In **A1**.
3. In **Zeile 9** – dem letzten ausgefüllten Artikel, bevor Sie die Liste ergänzt haben. Nach Aufgabe 4 landen Sie in Zeile 14.

**Aufgabe 6**

| Artikel | Differenz |
|---|---|
| Allzweckreiniger | 5 |
| Müllbeutel 120 l | 50 |
| Handtuchpapier | 20 |
| Toilettenpapier | 20 |
| Glasreiniger | -2 |
| Bodenreiniger | 4 |
| Desinfektionsmittel | 1 |
| Schwämme | 5 |
| Einweghandschuhe | -5 |
| Wischmopps | 1 |

**Aufgabe 7**

1. **Glasreiniger** (-2) und **Einweghandschuhe** (-5)
2. **Müllbeutel 120 l** mit 50 Stück über der Mindestmenge
3. Die Differenz ist jetzt **2** (12 − 10).

</details>
