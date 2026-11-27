// Word-Dateien Block 12 erzeugen (Kurzreferenz, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-12-docx.js _resources/Grundkurs/Block-12
// Das Übungsblatt muss inhaltlich Grundkurs/Block-12-Uebungsblatt.md entsprechen.
const fs = require('fs');
const path = require('path');
const d = require('docx');
const { Document, Packer, Paragraph, TextRun, HeadingLevel, Table, TableRow, TableCell, WidthType,
  ShadingType, BorderStyle, AlignmentType, LevelFormat, Footer, PageBreak, PageNumber } = d;
const OUT = process.argv[2];
const FONT = 'Aptos';
const NAVY = '1F3A5F', LINE = 'BFC7D2', SOFT = 'EEF2F7', YELLOW = 'FFF4D6', BLUE = 'E6F0FA';
const CONTENT = 9070; // A4 width 11906 - 2*1418

const styles = {
  default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { after: 120, line: 288 } } } },
  paragraphStyles: [
    { id: 'Title', name: 'Title', basedOn: 'Normal', run: { font: FONT, size: 44, bold: true, color: NAVY }, paragraph: { spacing: { before: 0, after: 80 }, keepNext: true } },
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 30, bold: true, color: NAVY }, paragraph: { spacing: { before: 320, after: 120 }, keepNext: true, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true, run: { font: FONT, size: 24, bold: true, color: NAVY }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 1 } },
  ],
};
const numbering = { config: [
  { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 283 } } } }] },
  { reference: 'steps', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 567, hanging: 340 } } } }] },
] };

// inline **bold** parsing
function runs(s, extra = {}) {
  return s.split(/(\*\*[^*]+\*\*)/).filter(Boolean).map(t =>
    t.startsWith('**') ? new TextRun({ text: t.slice(2, -2), bold: true, ...extra }) : new TextRun({ text: t, ...extra }));
}
const P = (s, o = {}) => new Paragraph({ children: runs(s), ...o });
const H1 = s => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [new TextRun(s)] });
const H2 = s => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [new TextRun(s)] });
const TITLE = s => new Paragraph({ heading: HeadingLevel.TITLE, children: [new TextRun(s)] });
const SUB = s => new Paragraph({ children: [new TextRun({ text: s, color: '5B6472', size: 24 })], spacing: { after: 240 },
  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: NAVY, space: 6 } } });
const BUL = s => new Paragraph({ children: runs(s), numbering: { reference: 'bullets', level: 0 } });
let inst = 0;
const STEPS = arr => { inst++; return arr.map(s => new Paragraph({ children: runs(s), numbering: { reference: 'steps', level: 0, instance: inst } })); };
const BOX = (title, lines, fill = YELLOW, color = 'E8A33D') => lines.map((s, i) => new Paragraph({
  children: i === 0 && title ? [new TextRun({ text: title + ' ', bold: true }), ...runs(s)] : runs(s),
  shading: { type: ShadingType.CLEAR, color: 'auto', fill },
  border: { left: { style: BorderStyle.SINGLE, size: 24, color, space: 8 } },
  indent: { left: 170, right: 170 }, spacing: { before: i === 0 ? 120 : 0, after: i === lines.length - 1 ? 160 : 0 } }));
const CHECK = s => new Paragraph({ children: [new TextRun({ text: '☐  ', size: 26 }), ...runs(s)], indent: { left: 340 } });

const cellBorder = { style: BorderStyle.SINGLE, size: 4, color: LINE };
const borders = { top: cellBorder, bottom: cellBorder, left: cellBorder, right: cellBorder };
function table(widths, rows, { header = true, minHeight } = {}) {
  return new Table({ width: { size: widths.reduce((a, b) => a + b, 0), type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, ri) => new TableRow({ tableHeader: header && ri === 0, height: minHeight && ri > 0 ? { value: minHeight, rule: 'atLeast' } : undefined,
      children: r.map((c, ci) => new TableCell({ borders, width: { size: widths[ci], type: WidthType.DXA },
        shading: header && ri === 0 ? { type: ShadingType.CLEAR, color: 'auto', fill: SOFT } : undefined,
        margins: { top: 60, bottom: 60, left: 110, right: 110 },
        children: [new Paragraph({ spacing: { after: 0 }, children: runs(c, header && ri === 0 ? { bold: true } : {}) })] })) })) });
}
const footer = text => ({ default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.LEFT,
  border: { top: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 4 } },
  children: [new TextRun({ text, size: 16, color: '5B6472' }), new TextRun({ text: '\tSeite ', size: 16, color: '5B6472' }),
    new TextRun({ children: [PageNumber.CURRENT], size: 16, color: '5B6472' })],
  tabStops: [{ type: 'right', position: CONTENT }] })] }) });
const page = { size: { width: 11906, height: 16838 }, margin: { top: 1418, bottom: 1418, left: 1418, right: 1418 } };

async function save(name, title, children, foot) {
  const doc = new Document({ creator: 'Microsoft 365 im Facility Management', title, styles, numbering,
    sections: [{ properties: { page }, footers: footer(foot), children }] });
  fs.writeFileSync(path.join(OUT, name), await Packer.toBuffer(doc));
  console.log('geschrieben', name);
}
// Die Kurzreferenz fasst nur zusammen, was in den Lerneinheiten Block 01–11 steht.
const FRAGEN = [
  ['1', 'Wofür nutzen Sie Outlook, Word und Excel im Haus Lichtblick? (01)'], ['2', 'Wann setzen Sie jemanden in „Cc“? (02)'],
  ['3', 'Was bedeutet „WG:“ vor einem Betreff? (02)'], ['4', 'Woran sehen Sie, dass aus einem Termin eine Besprechung geworden ist? (03)'],
  ['5', 'Wie tragen Sie die Heizungswartung am ersten Montag jedes Monats mit einem Mal ein? (03)'], ['6', 'Was müssen Sie tun, bevor Sie Text fett machen? (04)'],
  ['7', 'Was bewirkt Umschalt+Enter in Word? (04)'], ['8', 'Warum Überschriften mit der Formatvorlage „Überschrift 1“ statt von Hand? (05)'],
  ['9', 'Womit beginnt jede Formel in Excel? (08)'], ['10', 'Was bedeutet der Doppelpunkt in =SUMME(C4:C15)? (09)'],
  ['11', 'Sind beim Filtern Zeilen gelöscht? (09)'], ['12', 'Warum speichern Sie einen Bericht, bevor Sie ihn anhängen? (11)']];
const LOES = ['Outlook für E-Mails und Termine (Störungsmeldungen, Wartungstermine), Word für Texte (Aushänge, Protokolle, Berichte), Excel für Listen und Zahlen (Mieterliste, Inventar, Stromverbrauch).',
  'Wenn die Person Bescheid wissen soll, aber nichts tun muss.', 'Die E-Mail wurde **weitergeleitet**.',
  'Sobald jemand eingeladen ist, heißt die Schaltfläche „Senden“ statt „Speichern“.', 'Als **Serie**: „Serie erstellen“, Muster monatlich, am ersten Montag.',
  'Den Text **markieren**.', 'Eine **neue Zeile im selben Absatz** (Zeilenumbruch).',
  'Alle Überschriften sehen gleich aus, es geht schneller, und Word erkennt die Gliederung, zum Beispiel im Navigationsbereich.',
  'Mit dem **Gleichheitszeichen =**.', '**„bis“** – von C4 bis C15.', '**Nein**, sie sind nur ausgeblendet.',
  'Outlook hängt die Datei so an, wie sie gespeichert ist. Ungespeicherte Änderungen fehlen im Anhang.'];

(async () => {
  await save('Block-12-Kurzreferenz.docx', 'Kurzreferenz Microsoft 365 – Haus Lichtblick', [
    TITLE('Kurzreferenz'),
    SUB('Outlook, Word und Excel – alles Wichtige aus dem Grundkurs'),
    H1('Tastenkürzel'),
    table([2600, 3900, 2570], [['Kürzel', 'Wirkung', 'Wo'],
      ['Strg+S', 'Speichern', 'Word, Excel'], ['Strg+Z / Strg+Y', 'Rückgängig / Wiederherstellen', 'alle drei / Word, Excel'],
      ['Strg+C / Strg+V', 'Kopieren / Einfügen', 'alle drei'], ['Strg+P', 'Drucken mit Vorschau', 'Word, Excel'], ['Strg+F', 'Suchen', 'Word, Excel'],
      ['Strg+Umschalt+F / K / U', 'Fett / Kursiv / Unterstrichen', 'Word, Excel'], ['Strg+E', 'Zentrieren', 'Word'],
      ['Umschalt+Enter', 'Neue Zeile im selben Absatz', 'Word'], ['Strg+A', 'Alles markieren', 'Word, Excel'],
      ['Strg+Pos1', 'Zu Zelle A1', 'Excel'], ['Tab / Umschalt+Tab', 'Nächste / vorige Zelle', 'Excel, Word-Tabellen'],
      ['F2', 'Zelle bearbeiten', 'Excel'], ['Alt+Tab', 'Programm wechseln', 'Windows'], ['Windows-Taste+Pfeil links/rechts', 'Fenster an den Rand', 'Windows'],
      ['AltGr+Q', '@-Zeichen', 'Tastatur']]),
    H1('Outlook'),
    table([3500, 5570], [['Aufgabe', 'So geht\'s'],
      ['Neue E-Mail', 'E-Mail (App-Leiste) → Start → Neue E-Mail'], ['Cc / Bcc einblenden', 'rechts neben „An“ auf „Cc“ oder „Bcc“'],
      ['Antworten / Weiterleiten', 'oben im Lesebereich; Betreff AW: bzw. WG:'], ['Ordner anlegen', 'Rechtsklick auf Posteingang → Neuen Unterordner erstellen'],
      ['Termin', 'Kalender → Neues Ereignis → Speichern'], ['Besprechung', 'Neues Ereignis → Teilnehmende einladen → Senden'],
      ['Serie', 'im Ereignis „Serie erstellen“'], ['Anhang', 'Einfügen → Datei anfügen → Diesen PC durchsuchen']]),
    H1('Word'),
    table([3500, 5570], [['Aufgabe', 'So geht\'s'],
      ['Speichern unter', 'Datei → Speichern unter → Durchsuchen'], ['Formatierungszeichen', 'Start → Absatz → ¶'],
      ['Aufzählung / Nummerierung', 'Start → Absatz'], ['Überschrift', 'Start → Formatvorlagen → Überschrift 1 / 2'],
      ['Navigationsbereich', 'Ansicht → Navigationsbereich'], ['Tabelle', 'Einfügen → Tabelle → Raster'],
      ['Zeile löschen', 'Layout (Tabelle) → Löschen → Zeilen löschen'], ['Seitenränder', 'Layout → Seitenränder'], ['Abstand vor/nach', 'Layout → Abstand']]),
    H1('Excel'),
    table([3500, 5570], [['Aufgabe', 'So geht\'s'],
      ['Formel', '= tippen, Zelle anklicken, Rechenzeichen, Zelle anklicken, Enter'], ['Formel ausfüllen', 'Ausfüllkästchen ziehen oder doppelklicken'],
      ['AutoSumme', 'Start → AutoSumme (Σ)'], ['Zahlenformat', 'Start → Zahl → Währung, Datum …'],
      ['Sortieren', 'eine Zelle anklicken → Daten → Sortieren'], ['Filtern', 'Daten → Filtern; noch einmal klicken hebt auf'],
      ['Diagramm', 'Daten markieren → Einfügen → Diagramme'], ['Achsentitel', 'Diagramm anklicken → + → Achsentitel']]),
    H2('Funktionen'),
    table([3500, 5570], [['Funktion', 'Rechnet'], ['=SUMME(C4:C15)', 'alles zusammen'], ['=MITTELWERT(C4:C15)', 'den Durchschnitt'],
      ['=MIN(…) / =MAX(…)', 'kleinsten / größten Wert'], ['=ANZAHL(…)', 'wie viele Zellen eine Zahl enthalten']]),
    H1('Häufige Fehler'),
    BUL('Nicht gespeichert → früh und oft **Strg+S**'), BUL('Zahl statt Formel → mit **=** beginnen, Zellen anklicken'),
    BUL('Formatiert ohne Markierung → **erst markieren**, dann formatieren'), BUL('Falscher Empfänger → An und Betreff **vor** dem Senden prüfen'),
    BUL('Alte Fassung angehängt → **erst speichern**, dann anhängen'), BUL('Mehrmals Enter für Abstand → Layout → Abstand'),
    BUL('Liste falsch sortiert → nur **eine** Zelle anklicken; sonst sofort Strg+Z'),
  ], 'Kurzreferenz · Microsoft 365 im Facility Management · Haus Lichtblick');

  await save('Block-12-Uebungsblatt.docx', 'Übungsblatt Block 12 – Abschluss und Ausblick', [
    TITLE('Übungsblatt Block 12'),
    SUB('Abschluss und Ausblick'),
    P('**Sie brauchen:** einen PC mit dem neuen Outlook und Ihrem E-Mail-Konto und die Kurzreferenz Block-12-Kurzreferenz.docx von der Seite zu Block 12.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick – inzwischen mit allen drei Programmen vertraut. Zum Abschluss prüfen Sie Ihr Wissen, erledigen eine letzte Störungsmeldung und planen, wie es weitergeht.'),
    H1('Aufgabe 1 – Selbsttest'),
    P('Beantworten Sie die Fragen ohne nachzusehen. In Klammern steht der Block, in dem Sie die Antwort finden.'),
    table([600, 4970, 3500], [['Nr.', 'Frage', 'Ihre Antwort'], ...FRAGEN.map(f => [f[0], f[1], ''])], { minHeight: 600 }),
    H1('Aufgabe 2 – Eine letzte Störungsmeldung'),
    P('Michael Braun von DesignWerk (2. OG) meldet: Die Zugangskarten seiner Firma funktionieren nicht.'),
    ...STEPS(['Schreiben Sie eine E-Mail an **Ihre eigene Adresse** – sie steht für Jan Müller aus der Technik. Setzen Sie Ihre Adresse noch einmal in **Cc** – sie steht für die Hausverwaltung.',
      'Wählen Sie einen Betreff, der sagt, was los ist und wo.',
      'Bitten Sie im Text um Prüfung und Rückmeldung bis morgen Mittag. Senden Sie die E-Mail.',
      'Legen Sie im Kalender für morgen um 13:00 Uhr einen Termin „Rückfrage Zugangskarten DesignWerk“ an, Erinnerung 15 Minuten vorher.',
      'Verschieben Sie die E-Mail in Ihren Ordner „Störungsmeldungen“ aus Block 02 (oder legen Sie ihn an).',
      'Löschen Sie den Termin wieder, wenn Sie fertig sind.']),
    H1('Aufgabe 3 – Die Kurzreferenz'),
    ...STEPS(['Laden Sie Block-12-Kurzreferenz.docx herunter und öffnen Sie sie.',
      'Drucken Sie sie aus oder speichern Sie sie in Dokumente\\Haus-Lichtblick.',
      'Markieren Sie die drei Kürzel oder Menüwege, die Sie am häufigsten brauchen werden.']),
    H1('Aufgabe 4 – Ihr Plan'),
    table([4500, 4570], [['Frage', 'Ihre Antwort'],
      ['Welche drei Dinge aus dem Kurs werde ich nächste Woche bei der Arbeit nutzen?', ''],
      ['Welchen Block möchte ich noch einmal wiederholen?', ''],
      ['Welches Aufbaumodul nehme ich mir als Nächstes vor: Word, Excel oder Verknüpfung?', '']], { minHeight: 900 }),
    H1('Selbstcheck'),
    CHECK('Ich habe mindestens zehn der zwölf Fragen ohne Nachsehen beantwortet.'),
    CHECK('Ich habe eine Störungsmeldung mit gutem Betreff geschrieben und einen Termin dazu angelegt.'),
    CHECK('Ich habe die Kurzreferenz griffbereit.'),
    CHECK('Ich weiß, wie es für mich weitergeht.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 1'),
    ...STEPS(LOES),
    H2('Aufgabe 2'),
    P('Ein guter Betreff ist zum Beispiel „Störungsmeldung – Zugangskarten DesignWerk (2. OG) funktionieren nicht“. Die E-Mail gehört in „An“ an die Technik, in „Cc“ an die Hausverwaltung.'),
  ], 'Übungsblatt Block 12 · Microsoft 365 im Facility Management');
})();
