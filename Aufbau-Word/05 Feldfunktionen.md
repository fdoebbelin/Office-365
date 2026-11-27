# 5. Feldfunktionen

**Dauer:** 30 Minuten

Felder sind Platzhalter, die Word selbst ausfüllt: das heutige Datum, die Seitenzahl, die Zahl der Seiten, ein Inhaltsverzeichnis. Jedes Feld hat zwei Gesichter – den **Feldcode** (die Anweisung) und das **Feldergebnis** (was man sieht).

## Wichtige Felder

| Feld | Feldcode | Verwendung |
|---|---|---|
| Seitenzahl | `{ PAGE }` | Kopf- und Fußzeilen |
| Anzahl der Seiten | `{ NUMPAGES }` | „Seite X von Y“ |
| Aktuelles Datum | `{ DATE }` | Briefe, Aushänge |
| Inhaltsverzeichnis | `{ TOC }` | Berichte, Handbücher |
| Titel des Dokuments | `{ TITLE }` | Kopfzeile, Titelseite |
| Autor | `{ AUTHOR }` | Fußzeile |
| Querverweis | `{ REF }` | Verweise auf Abbildungen, Tabellen, Überschriften |

## Felder über Menüs einfügen

Meist entsteht ein Feld, ohne dass man es merkt:

- **Seitenzahl:** „Einfügen“ → „Seitenzahl“ → Position und Format wählen.
- **Datum:** „Einfügen“ → „Datum und Uhrzeit“ → Format wählen und **„Automatisch aktualisieren“** anhaken. Ohne Häkchen wird das Datum als fester Text eingefügt.
- **Inhaltsverzeichnis:** „Referenzen“ → „Inhaltsverzeichnis“.
- **Dokumenteigenschaften (Titel, Autor):** „Einfügen“ → „Schnellbausteine“ → „Dokumenteigenschaft“.
- **Jedes andere Feld:** „Einfügen“ → „Schnellbausteine“ → **„Feld…“** → Feldname wählen.

## Tasten für Felder

| Tasten | Wirkung |
|---|---|
| **Alt+F9** | Feldcodes im ganzen Dokument zeigen bzw. wieder Ergebnisse zeigen |
| **Umschalt+F9** | Feldcode nur des markierten Feldes umschalten |
| **F9** | Markierte Felder aktualisieren |
| **Strg+A**, dann **F9** | Alle Felder im Dokumenttext aktualisieren |
| **Strg+F9** | Leere Feldklammer `{ }` einfügen, um einen Feldcode von Hand zu schreiben |

Die geschweiften Klammern eines Feldes lassen sich nicht eintippen – nur mit Strg+F9 entsteht ein echtes Feld.

Felder in Kopf- und Fußzeilen erfasst Strg+A nicht; sie werden beim Drucken bzw. in der Druckvorschau aktualisiert.

## Standardanzeige festlegen

Ob Word beim Öffnen Feldcodes oder Ergebnisse zeigt, ist eine Einstellung:

1. „Datei“ → „Optionen“ → „Erweitert“.
2. Abschnitt „Dokumentinhalt anzeigen“ → **„Feldfunktionen anstelle von Werten anzeigen“**.
3. Häkchen setzen = Feldcodes; Häkchen entfernen = Ergebnisse (empfohlen).
4. Mit „OK“ bestätigen.

Unabhängig davon schaltet Alt+F9 jederzeit um.

## Praxistipps

- Feld zeigt Unsinn oder Fehlermeldung? Mit Alt+F9 den Feldcode prüfen.
- Vor dem Drucken oder Versenden: Strg+A, F9 – damit Datum, Verzeichnisse und Querverweise stimmen.
- Felder sind grau hinterlegt, sobald man hineinklickt – daran erkennt man sie im Text.
