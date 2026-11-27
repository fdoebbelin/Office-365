# 3. Serien-E-Mail an die Mieter

**Dauer:** 60 Minuten · **Übung:** Einladung zur Brandschutzunterweisung

Eine Serien-E-Mail verschickt denselben Text an viele Empfänger – jeweils mit persönlicher Anrede. Die Adressen kommen aus Excel, der Text aus Word, verschickt wird über Outlook.

> **Voraussetzung:** Word verschickt Serien-E-Mails über das E-Mail-Programm des PCs. Mit dem **neuen Outlook** funktioniert das bisher nicht; nötig ist das **klassische Outlook**, eingerichtet mit dem Kurskonto. Vor dem Kurs auf einem Kurs-PC testen – Microsoft ergänzt Funktionen im neuen Outlook laufend.

> **Wichtig für die Übung:** Verschickt wird an die Kursadressen der Teilnehmenden, nie an die fiktiven Adressen aus der Referenzliste – die Domains könnten echten Firmen gehören.

## Schritt 1: Adressliste in Excel

1. Neue Arbeitsmappe, A1 bis E1: **Anrede**, **Vorname**, **Nachname**, **Firma**, **E-Mail**.
2. Datensätze nach der Mieterliste:

| Anrede | Vorname | Nachname | Firma | E-Mail |
|---|---|---|---|---|
| Frau | Anna | Klein | TechSolutions | *Kursadresse 1* |
| Herr | Michael | Braun | DesignWerk | *Kursadresse 2* |
| Frau | Sarah | Meyer | Consulting Plus | *Kursadresse 3* |
| Herr | Jürgen | Hahn | Steuerbüro Hahn | *Kursadresse 4* |
| Frau | Lena | Ott | Praxis am Park | *Kursadresse 5* |

3. Speichern als `Mieter-Adressliste.xlsx` und Excel schließen (Word kann die Datei sonst nicht immer lesen).

## Schritt 2: Serien-E-Mail in Word anlegen

1. Neues leeres Word-Dokument.
2. Registerkarte **„Sendungen“** → „Seriendruck starten“ → **„E-Mail-Nachrichten“**.
3. „Empfänger auswählen“ → **„Vorhandene Liste verwenden…“** → `Mieter-Adressliste.xlsx` → Tabelle „Tabelle1$“ → „Erste Datenzeile enthält Spaltenüberschriften“ angehakt → „OK“.
4. Text schreiben:

```
Sehr geehrte<<Anrede-Regel>> <<Nachname>>,

am Donnerstag, 16. April 2026, findet um 10:00 Uhr im Konferenzraum 3.10 eine Brandschutzunterweisung für alle Mieter von Haus Lichtblick statt. Bitte geben Sie die Einladung auch an Ihre Mitarbeitenden bei <<Firma>> weiter.

Mit freundlichen Grüßen

Facility Management Haus Lichtblick
```

### Anrede über eine Regel

„Sehr geehrte Frau“ und „Sehr geehrter Herr“ unterscheiden sich in einem Buchstaben. Die Regel ergänzt ihn:

1. Cursor direkt hinter „Sehr geehrte“ setzen (ohne Leerzeichen).
2. „Sendungen“ → „Regeln“ → **„Wenn…Dann…Sonst…“**.
3. Feldname „Anrede“, Vergleich „Gleich“, Vergleichswert `Herr`.
4. „Dann diesen Text einfügen“: `r Herr` · „Sonst diesen Text einfügen“: ` Frau` (mit Leerzeichen davor).
5. „OK“.

Mit Alt+F9 sieht man das Feld:

```
Sehr geehrte{ IF { MERGEFIELD Anrede } = "Herr" "r Herr" " Frau" } { MERGEFIELD Nachname },
```

6. Cursor hinter die Regel, Leerzeichen, „Seriendruckfeld einfügen“ → „Nachname“; im Text ebenso „Firma“.

Einfacher und für alle Geschlechter passend: Die Anrede komplett in die Excel-Liste schreiben („Sehr geehrte Frau Klein“, „Guten Tag Alex Muster“) und nur dieses Feld einfügen.

## Schritt 3: Vorschau und Kontrolle

1. „Sendungen“ → **„Vorschau Ergebnisse“**.
2. Mit den Pfeilen „Nächster Datensatz“ / „Vorheriger Datensatz“ jeden Empfänger prüfen: Anrede, Name, Firma.
3. Fehler in den Daten in Excel korrigieren und die Liste neu einlesen („Empfängerliste bearbeiten“ → Datenquelle → „Aktualisieren“).

## Schritt 4: Senden

1. „Sendungen“ → **„Fertig stellen und zusammenführen“** → **„E-Mail-Nachrichten senden…“**.
2. Im Dialog:
   - **An:** Feld „E-Mail“
   - **Betreffzeile:** „Einladung zur Brandschutzunterweisung am 16. April“
   - **E-Mail-Format:** HTML
   - **Datensätze:** alle
3. „OK“. Die Nachrichten liegen danach im Ordner „Gesendete Elemente“ des klassischen Outlook.

Tipp: Vor dem echten Versand den Seriendruck mit einer Liste testen, die nur die eigene Adresse enthält.

## Zusammenfassung

- Adressen in Excel, Text in Word, Versand über das klassische Outlook.
- Regeln wie „Wenn…Dann…Sonst…“ passen den Text je Empfänger an.
- Jeden Datensatz in der Vorschau prüfen, bevor man sendet – eine verschickte E-Mail lässt sich nicht zurückholen.
