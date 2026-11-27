---
title: "Übungsblatt"
parent: "Block 09 – Rechnen und Auswerten"
grand_parent: "Grundkurs"
nav_order: 1
---

# Übungsblatt Block 09 – Rechnen und Auswerten

**Sie brauchen:** einen PC mit Excel und die Übungsdatei `Block-09-Auswertung.xlsx` von der [Seite zu Block 09](Block-09.md#uebungsdateien). Die Lösungsdatei `Block-09-Loesung-Auswertung.xlsx` zeigt alle Ergebnisse – sehen Sie sie erst am Ende an. Das Übungsblatt gibt es auf der Seite auch als Word-Datei zum Ausdrucken.

**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Petra Schönfeld von der Hausverwaltung möchte für die Jahresabrechnung wissen, wie viel Strom das Haus 2025 verbraucht hat, wie hoch die Nebenkostenvorauszahlungen der Mieter sind und welches Reinigungsmaterial nachbestellt werden muss. Die Datei hat dafür drei Tabellenblätter.

## Aufgabe 1 – Datei vorbereiten

1. Öffnen Sie `Block-09-Auswertung.xlsx` aus dem Ordner Downloads und klicken Sie auf **„Bearbeitung aktivieren“**.
2. Speichern Sie die Datei in `Dokumente\Haus-Lichtblick` unter dem Namen `Auswertung-2025`.
3. Sehen Sie sich die drei Tabellenblätter an: **„Strom 2025“**, **„Nebenkosten“**, **„Inventar“** – ein Klick auf das Register unten wechselt das Blatt.

## Aufgabe 2 – Den Verbrauch berechnen

Blatt **„Strom 2025“**. Der Verbrauch für Januar steht schon da (Wert vom Stromversorger). Für die übrigen Monate rechnen Sie: Zählerstand dieses Monats minus Zählerstand des Vormonats.

1. Klicken Sie auf **C5** (Februar) und geben Sie ein: `=B5-B4`, **Enter**.
2. Klicken Sie wieder auf C5 und ziehen Sie das **Ausfüllkästchen** nach unten bis **C15** (Dezember). Oder doppelklicken Sie darauf.
3. Klicken Sie auf **C10** (Juli). Welche Formel steht in der Bearbeitungsleiste, welcher Wert in der Zelle?
4. Wie viel Strom hat das Haus im Dezember verbraucht?

## Aufgabe 3 – Funktionen

Bleiben Sie auf dem Blatt „Strom 2025“. Geben Sie in Spalte C die Funktionen ein – jeweils für den Bereich **C4:C15**.

| Zelle | Beschriftung in Spalte A | Funktion |
|---|---|---|
| C17 | Summe | `=SUMME(C4:C15)` |
| C18 | Mittelwert | `=MITTELWERT(C4:C15)` |
| C19 | Kleinster Wert | `=MIN(C4:C15)` |
| C20 | Größter Wert | `=MAX(C4:C15)` |
| C21 | Anzahl Monate | `=ANZAHL(C4:C15)` |

1. Wie hoch war der Jahresverbrauch 2025?
2. In welchem Monat war der Verbrauch am kleinsten, in welchem am größten?
3. Zeigt der Mittelwert eine Nachkommastelle? Klicken Sie auf C18 und dann auf **„Dezimalstelle löschen“**. Was ändert sich in der Zelle, was in der Bearbeitungsleiste?

## Aufgabe 4 – Nebenkosten mit AutoSumme und Währung

Blatt **„Nebenkosten“**.

1. Klicken Sie auf **D12** (unter den Nebenkosten) und dann auf **„AutoSumme“** (Σ). Prüfen Sie den gestrichelten Bereich und drücken Sie **Enter**.
2. Summieren Sie genauso die Fläche in **C12**.
3. Markieren Sie **D4 bis D12** und wählen Sie auf der Registerkarte „Start“ in der Gruppe „Zahl“ das Format **„Währung“**.
4. Wie hoch sind die Nebenkostenvorauszahlungen aller acht Mieter zusammen im Monat? Wie groß ist ihre Fläche zusammen?

## Aufgabe 5 – Sortieren und Filtern

Blatt **„Inventar“**.

1. Klicken Sie auf eine Zelle in der Spalte **„Bestand“** (zum Beispiel B4). Sortieren Sie über **„Daten“** → **„Sortieren“** nach Bestand, **aufsteigend**. Welcher Artikel steht jetzt oben?
2. Prüfen Sie: Steht neben jedem Artikel noch die richtige Einheit? (Glasreiniger: Flaschen, Wischmopps: Stück.)
3. Schalten Sie den Filter ein: **„Daten“** → **„Filtern“**.
4. Filtern Sie die Spalte **„Nachbestellen“** auf **„Ja“**. Welche Artikel bleiben übrig? Welche Zeilennummern sehen Sie?
5. Heben Sie den Filter auf: **„Daten“** → **„Filtern“**. Sind alle zehn Artikel wieder da?
6. Für Schnelle: Filtern Sie die Spalte **„Einheit“** auf **„Flaschen“**. Wie viele Artikel sind es? Heben Sie den Filter danach wieder auf.
7. Speichern Sie mit **Strg+S**.

## Selbstcheck

- [ ] Ich habe eine Formel mit dem Ausfüllkästchen nach unten übertragen und eine Zelle geprüft.
- [ ] Ich habe SUMME, MITTELWERT, MIN, MAX und ANZAHL eingegeben.
- [ ] Ich habe AutoSumme benutzt und den Bereich geprüft.
- [ ] Ich habe Beträge als Währung formatiert.
- [ ] Ich habe eine Liste sortiert, gefiltert und den Filter wieder aufgehoben.

## Lösungen

<details markdown="block">
<summary>Lösungen anzeigen</summary>

**Aufgabe 2** – In C10 steht `=B10-B9`, in der Zelle **3.320** (Juli). Im Dezember hat das Haus **4.530 kWh** verbraucht.

| Monat | Verbrauch (kWh) |
|---|---|
| Januar | 4.850 |
| Februar | 4.670 |
| März | 4.530 |
| April | 4.240 |
| Mai | 3.890 |
| Juni | 3.540 |
| Juli | 3.320 |
| August | 3.240 |
| September | 3.360 |
| Oktober | 3.650 |
| November | 4.030 |
| Dezember | 4.530 |

**Aufgabe 3**

| Funktion | Ergebnis |
|---|---|
| Summe | 47.850 kWh |
| Mittelwert | 3.987,5 kWh |
| Kleinster Wert | 3.240 kWh |
| Größter Wert | 4.850 kWh |
| Anzahl Monate | 12 |

1. Jahresverbrauch 2025: **47.850 kWh**
2. Am kleinsten im **August** (3.240 kWh), am größten im **Januar** (4.850 kWh)
3. Die Zelle zeigt **3.988** (gerundet), die Bearbeitungsleiste weiter die Formel. Der Wert dahinter bleibt 3.987,5.

**Aufgabe 4** – Nebenkosten zusammen **7.140,00 €** im Monat, Fläche zusammen **2.380 m²**. (Kontrolle: 2.380 m² × 3 € = 7.140 €.)

**Aufgabe 5**

- **Schritt 1:** Oben steht **Wischmopps** (Bestand 4).
- **Schritt 2:** Ja – Excel hat ganze Zeilen sortiert.
- **Schritt 4:** **Glasreiniger** und **Einweghandschuhe**. Die Zeilennummern springen, weil die übrigen Zeilen ausgeblendet sind: Nach dem Sortieren steht Einweghandschuhe in Zeile 5, Glasreiniger in Zeile 7.
- **Schritt 5:** Ja, alle zehn Artikel sind wieder sichtbar.
- **Schritt 6:** **4 Artikel**: Allzweckreiniger, Glasreiniger, Bodenreiniger, Desinfektionsmittel.

</details>
