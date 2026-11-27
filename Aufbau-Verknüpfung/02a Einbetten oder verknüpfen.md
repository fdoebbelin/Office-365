# Einbetten oder verknüpfen?

## Eingebettetes Objekt

Die Excel-Daten werden **in** das Word-Dokument kopiert und dort gespeichert.

**Vorteile:**

- **Eigenständig:** Das Word-Dokument enthält alle Daten und funktioniert ohne die Excel-Datei.
- **Bearbeitbar in Word:** Doppelklick öffnet das Objekt mit Excel-Werkzeugen.
- **Weitergeben unproblematisch:** Per E-Mail verschickt, kommt alles an.

**Nachteile:**

- **Größere Datei:** Die Excel-Daten stecken im Dokument.
- **Keine Aktualisierung:** Änderungen in der ursprünglichen Excel-Datei kommen nicht an.

## Verknüpftes Objekt

Das Word-Dokument enthält nur einen **Verweis** auf die Excel-Datei und zeigt deren Daten an.

**Vorteile:**

- **Aktuell:** Änderungen in Excel lassen sich in Word übernehmen.
- **Kleine Datei:** Die Daten bleiben in Excel.

**Nachteile:**

- **Abhängig:** Wird die Excel-Datei verschoben, umbenannt oder gelöscht, kann Word nicht mehr aktualisieren und zeigt den letzten Stand.
- **Bearbeiten nur in Excel:** Doppelklick öffnet die Quelldatei.
- **Weitergeben heikel:** Wer nur das Word-Dokument bekommt, hat keinen Zugriff auf die Quelle – und sieht unter Umständen den Pfad zu Ihren Dateien. Vor dem Versand die Verknüpfung lösen („Datei“ → „Informationen“ → „Verknüpfungen mit Dateien bearbeiten“ → „Verknüpfung aufheben“) oder als PDF verschicken.

## Übersicht

| Eigenschaft | Word-Tabelle | Eingebettetes Objekt | Verknüpftes Objekt |
|---|---|---|---|
| Daten gespeichert in | Word | Word | Excel-Datei |
| Abhängig von der Excel-Datei | nein | nein | ja |
| Aktualisierung aus Excel | nein | nein | ja |
| Bearbeiten | in Word wie Text | in Word mit Excel-Werkzeugen | nur in Excel |
| Dateigröße Word | klein | größer | klein |
| Zum Weitergeben | gut | gut | nur mit Quelle oder als PDF |

## Wann was?

- **Word-Tabelle:** Die Zahlen sind fertig und sollen nur gezeigt werden – z. B. im Protokoll.
- **Eingebettet:** Das Dokument wird weitergegeben, und der Empfänger soll noch rechnen können.
- **Verknüpft:** Ein Bericht, der jeden Monat mit denselben, fortgeschriebenen Daten neu entsteht – z. B. der Kassenbericht.
