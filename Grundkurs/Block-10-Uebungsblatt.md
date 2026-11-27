---
title: "Übungsblatt"
parent: "Block 10 – Diagramme erstellen"
grand_parent: "Grundkurs"
nav_order: 1
---

# Übungsblatt Block 10 – Diagramme erstellen

**Sie brauchen:** einen PC mit Excel und die Übungsdatei `Block-10-Diagramme.xlsx` von der [Seite zu Block 10](Block-10.md#uebungsdateien). Die Lösungsdatei `Block-10-Loesung-Diagramme.xlsx` zeigt die fertigen Diagramme – sehen Sie sie erst am Ende an. Ein Drucker ist schön, aber nicht nötig. Das Übungsblatt gibt es auf der Seite auch als Word-Datei zum Ausdrucken.

**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Für den Jahresbericht möchte Petra Schönfeld von der Hausverwaltung den Stromverbrauch 2025 als Diagramm sehen – und auf einen Blick, wie sich die vermietete Fläche auf die Etagen verteilt.

## Aufgabe 1 – Vorbereiten

1. Öffnen Sie `Block-10-Diagramme.xlsx` aus dem Ordner Downloads und klicken Sie auf **„Bearbeitung aktivieren“**.
2. Speichern Sie die Datei in `Dokumente\Haus-Lichtblick` unter dem Namen `Diagramme-2025`.
3. Sehen Sie sich das Blatt **„Strom 2025“** an. In welchem Monat war der Verbrauch am höchsten? Wie lange brauchen Sie, um das in der Tabelle zu finden?

## Aufgabe 2 – Das Säulendiagramm

1. Markieren Sie **A3 bis B15** – die Überschriften und alle zwölf Monate, **ohne** die Summe.
2. **„Einfügen“** → **„Säulen- oder Balkendiagramm einfügen“** → **„Gruppierte Säulen“**.
3. Schauen Sie auf das Diagramm: Welche Säule ist am höchsten, welche am niedrigsten? Wie lange brauchen Sie jetzt?

## Aufgabe 3 – Beschriften

1. Klicken Sie auf den Diagrammtitel und ändern Sie ihn in `Stromverbrauch Haus Lichtblick 2025`.
2. Klicken Sie auf das **+** neben dem Diagramm und setzen Sie das Häkchen bei **„Achsentitel“**.
3. Senkrechte Achse: `Verbrauch in kWh`. Waagerechte Achse: `Monat`.
4. Für Schnelle: Wählen Sie auf der Registerkarte **„Diagrammentwurf“** eine andere Diagrammformatvorlage.

## Aufgabe 4 – Verschieben und vergrößern

1. Fassen Sie das Diagramm am Rand an und ziehen Sie es rechts neben die Tabelle, sodass die linke obere Ecke etwa in Zelle **D3** liegt.
2. Ziehen Sie an der rechten unteren Ecke, bis das Diagramm etwa bis Spalte **L** reicht.

## Aufgabe 5 – Das Diagramm rechnet mit

1. Ändern Sie den Verbrauch im **Dezember** (B15) auf `5000`. Was passiert mit der Dezember-Säule?
2. Machen Sie die Änderung mit **Strg+Z** rückgängig.

## Aufgabe 6 – Das Kreisdiagramm

Wechseln Sie auf das Blatt **„Flächen“**.

1. Markieren Sie **A3 bis B7** – die vier Etagen ohne die Summe.
2. **„Einfügen“** → **„Kreis- oder Ringdiagramm einfügen“** → unter „2D-Kreis“ den ersten **„Kreis“**.
3. Ändern Sie den Titel in `Vermietete Fläche je Etage`.
4. Klicken Sie auf das **+** und schalten Sie **„Datenbeschriftungen“** ein. Klicken Sie auf den kleinen Pfeil daneben → **„Weitere Optionen“** und setzen Sie das Häkchen bei **„Prozentsatz“**, das bei **„Wert“** nehmen Sie heraus.
5. Welche Etage hat den größten Anteil, welche den kleinsten?

## Aufgabe 7 – Drucken und speichern

1. Wechseln Sie zurück auf „Strom 2025“ und klicken Sie das Säulendiagramm einmal an.
2. **Strg+P**: Steht unter „Einstellungen“ **„Ausgewähltes Diagramm drucken“**? Prüfen Sie die Vorschau und drucken Sie, wenn ein Drucker angeschlossen ist.
3. Speichern Sie mit **Strg+S** und vergleichen Sie mit der Lösungsdatei.

## Selbstcheck

- [ ] Ich habe die richtigen Daten ohne Summe markiert und ein Säulendiagramm eingefügt.
- [ ] Mein Diagramm hat einen aussagekräftigen Titel und zwei Achsentitel.
- [ ] Ich habe das Diagramm verschoben und vergrößert.
- [ ] Ich habe gesehen, dass das Diagramm sich mit der Tabelle ändert.
- [ ] Ich habe ein Kreisdiagramm mit Prozentwerten erstellt.
- [ ] Ich habe nur das Diagramm in der Druckvorschau gesehen.

## Lösungen

<details markdown="block">
<summary>Lösungen anzeigen</summary>

**Aufgaben 1 und 2** – Am höchsten war der Verbrauch im **Januar** (4.850 kWh), am niedrigsten im **August** (3.240 kWh). Im Diagramm sieht man das auf einen Blick – in der Tabelle muss man alle zwölf Zahlen vergleichen.

**Aufgabe 5** – Die Dezember-Säule wächst sofort auf 5.000 und ist jetzt die höchste. Nach Strg+Z ist sie wieder bei 4.530.

**Aufgabe 6**

| Etage | Fläche | Anteil |
|---|---|---|
| 1. OG | 750 m² | 32 % |
| 2. OG | 570 m² | 24 % |
| 3. OG | 760 m² | 32 % |
| 4. OG | 300 m² | 13 % |

Den größten Anteil hat das **3. OG** (760 m², knapp vor dem 1. OG mit 750 m²), den kleinsten das **4. OG** (300 m²). Excel rundet die Prozentwerte; zusammen ergeben sie deshalb 101 %.

Die fertigen Diagramme stehen in `Block-10-Loesung-Diagramme.xlsx`.

</details>
