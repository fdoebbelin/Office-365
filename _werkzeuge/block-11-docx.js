// Word-Dateien Block 11 erzeugen (Berichtsvorlage, Lösung mit Tabelle und Diagrammbild, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-11-docx.js _resources/Grundkurs/Block-11 <diagramm.png>
// Das Diagrammbild erzeugt block-11-xlsx.py als SVG; vorher mit magick in PNG umwandeln.
// Das Übungsblatt muss inhaltlich Grundkurs/Block-11-Uebungsblatt.md entsprechen.
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
const { ImageRun } = d;
const PNG = process.argv[3];
const PROTOKOLL = [['Datum', 'Gewerk', 'Befund', 'Maßnahme', 'Erledigt'],
  ['15.04.2025', 'Elektro', 'Deckenlampe Flur EG flackert', 'Leuchtmittel getauscht', 'Ja'],
  ['18.04.2025', 'Sanitär', 'Wasserhahn Teeküche 2. OG tropft', 'Dichtung erneuert', 'Ja'],
  ['22.04.2025', 'Heizung', 'Heizkörper Büro 305 bleibt kalt', 'Entlüftet', 'Ja'],
  ['25.04.2025', 'Brandschutz', 'Feuerlöscher EG-Flur abgelaufen', 'Neuen Löscher installiert', 'Ja']];
const STROM = [['Monat', 'Verbrauch (kWh)'], ['Januar', '4.850'], ['Februar', '4.670'], ['März', '4.530'], ['April', '4.240'], ['Mai', '3.890'], ['Juni', '3.540'],
  ['Juli', '3.320'], ['August', '3.240'], ['September', '3.360'], ['Oktober', '3.650'], ['November', '4.030'], ['Dezember', '4.530'], ['**Summe**', '**47.850**']];
const MAILTEXT = ['Hallo Frau Schönfeld,', 'anbei der Jahresbericht Facility Management 2025 für das Haus Lichtblick mit dem Stromverbrauch, den Störungen im April und dem Stand im Lager.',
  'Bei Fragen melden Sie sich gern.', 'Viele Grüße', '[Ihr Name]', 'Koordination Facility Management, Haus Lichtblick'];

function bericht(loesung) {
  const L = (a, b) => (loesung ? b : a);
  return [
    TITLE('Jahresbericht Facility Management 2025'),
    SUB('Haus Lichtblick · Sonnenallee 45, 10115 Berlin'),
    P('**An:** Immobilien Fischer GmbH, Petra Schönfeld'),
    P('**Von:** Koordination Facility Management'),
    H1('1. Stromverbrauch 2025'),
    P(`Der Stromverbrauch lag 2025 bei ${L('________', '**47.850**')} kWh. Am höchsten war er im ${L('________', '**Januar**')}, am niedrigsten im ${L('________', '**August**')}. Im Winter ist der Verbrauch deutlich höher als im Sommer.`),
    ...(loesung ? [table([3000, 2500], STROM),
      new Paragraph({ spacing: { before: 240, after: 120 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(PNG), transformation: { width: 600, height: 320 } })] })]
      : [P('[Tabelle aus Excel hier einfügen]'), P('[Diagramm aus Excel hier einfügen]')]),
    H1('2. Störungen und Wartung'),
    P('Im April 2025 wurden vier Störungen gemeldet und behoben:'),
    table([1300, 1350, 2700, 2620, 1100], PROTOKOLL),
    H1('3. Lager Reinigungsmaterial'),
    P('Unter der Mindestmenge und nachzubestellen:', { spacing: { before: 160, after: 120 } }),
    BUL('Glasreiniger: 8 Flaschen, Mindestmenge 10'),
    BUL('Einweghandschuhe: 5 Pakete, Mindestmenge 10'),
    P('Mit freundlichen Grüßen', { spacing: { before: 360, after: 0 } }),
    P(L('[Ihr Name]', 'Ihr Name'), { spacing: { before: 240, after: 0 } }),
    P('Koordination Facility Management, Haus Lichtblick'),
  ];
}

(async () => {
  await save('Block-11-Bericht.docx', 'Jahresbericht Facility Management 2025 (Vorlage)', bericht(false),
    'Übungsdatei Block 11 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden');
  await save('Block-11-Loesung-Bericht.docx', 'Jahresbericht Facility Management 2025 (Lösung)', bericht(true),
    'Lösungsdatei Block 11 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden');

  await save('Block-11-Uebungsblatt.docx', 'Übungsblatt Block 11 – Programme verknüpfen', [
    TITLE('Übungsblatt Block 11'),
    SUB('Programme verknüpfen'),
    P('**Sie brauchen:** einen PC mit Excel, Word und dem neuen Outlook, Ihr E-Mail-Konto und die Übungsdateien Block-11-Strom.xlsx und Block-11-Bericht.docx von der Seite zu Block 11. Die Lösungsdatei Block-11-Loesung-Bericht.docx zeigt den fertigen Bericht.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Der Jahresbericht 2025 für die Hausverwaltung ist fast fertig – es fehlen nur noch die Stromzahlen aus Excel. Sie bauen Tabelle und Diagramm ein, füllen die Lücken und schicken den Bericht an Petra Schönfeld.'),
    ...BOX('Achtung:', ['Senden Sie die E-Mail **nur an Ihre eigene Adresse** – sie steht für Petra Schönfeld. Die Adressen im Haus Lichtblick sind erfunden.'], 'FBE9E7', 'B3261E'),
    H1('Aufgabe 1 – Vorbereiten'),
    ...STEPS(['Öffnen Sie Block-11-Bericht.docx in Word und klicken Sie auf **„Bearbeitung aktivieren“**. Speichern Sie den Bericht in Dokumente\\Haus-Lichtblick als Jahresbericht-2025.',
      'Öffnen Sie Block-11-Strom.xlsx in Excel und klicken Sie auf **„Bearbeitung aktivieren“**.',
      'Ordnen Sie die Fenster nebeneinander: Klicken Sie in Excel und drücken Sie **Windows-Taste+Pfeil links**. Windows zeigt die übrigen Fenster – klicken Sie auf Word.']),
    H1('Aufgabe 2 – Die Tabelle einfügen'),
    ...STEPS(['Markieren Sie in Excel **A3 bis B16** – Überschriften, zwölf Monate und Summe. Drücken Sie **Strg+C**.',
      'Markieren Sie in Word die Zeile „[Tabelle aus Excel hier einfügen]“ und drücken Sie **Strg+V**. Die Tabelle ersetzt den Platzhalter.',
      'Lassen Sie das kleine Symbol „(Strg)“ einfach stehen – eingefügt ist schon.']),
    H1('Aufgabe 3 – Das Diagramm einfügen'),
    ...STEPS(['Klicken Sie in Excel einmal auf den **Rand** des Diagramms und drücken Sie **Strg+C**.',
      'Markieren Sie in Word die Zeile „[Diagramm aus Excel hier einfügen]“ und drücken Sie **Strg+V**.',
      'Ist das Diagramm zu groß, klicken Sie es an und ziehen Sie an einer Ecke, bis es in die Seitenbreite passt.']),
    H1('Aufgabe 4 – Die Lücken füllen'),
    P('Im ersten Absatz des Berichts fehlen drei Angaben. Lesen Sie sie aus der Excel-Tabelle oder dem Diagramm ab und tragen Sie sie ein:'),
    table([4500, 4570], [['Lücke', 'Ihre Angabe'], ['Stromverbrauch 2025 in kWh', ''], ['Monat mit dem höchsten Verbrauch', ''], ['Monat mit dem niedrigsten Verbrauch', '']], { minHeight: 500 }),
    P('Ersetzen Sie unten „[Ihr Name]“ durch Ihren Namen und speichern Sie mit **Strg+S**.', { spacing: { before: 160, after: 120 } }),
    H1('Aufgabe 5 – Der Versand'),
    ...STEPS(['Wechseln Sie zu Outlook und klicken Sie auf **„Neue E-Mail“**.',
      '**An:** Ihre eigene Adresse. **Betreff:** Jahresbericht Facility Management 2025 – Haus Lichtblick',
      'Schreiben Sie den Text unten oder einen eigenen.',
      'Registerkarte **„Einfügen“** → **„Datei anfügen“** → **„Diesen PC durchsuchen“**. Wählen Sie Jahresbericht-2025 aus Dokumente\\Haus-Lichtblick.',
      'Prüfen Sie: Steht der Anhang unter dem Betreff? Klicken Sie auf **„Senden“**.',
      'Öffnen Sie die E-Mail in Ihrem Posteingang und den Anhang mit Doppelklick. Ist alles drin?']),
    ...BOX('', MAILTEXT, SOFT, NAVY),
    H1('Aufgabe 6 – Kopie oder Verbindung?'),
    ...STEPS(['Ändern Sie in Excel den Verbrauch im Januar (B4) auf 6000.',
      'Schauen Sie in Word: Ändert sich die Tabelle? Ändert sich das Diagramm?',
      'Machen Sie die Änderung in Excel mit **Strg+Z** rückgängig und schließen Sie Excel ohne zu speichern.']),
    H1('Selbstcheck'),
    CHECK('Ich habe Excel und Word nebeneinander angeordnet.'),
    CHECK('Ich habe eine Tabelle und ein Diagramm von Excel nach Word kopiert.'),
    CHECK('Ich habe den Bericht gespeichert, bevor ich ihn angehängt habe.'),
    CHECK('Ich habe eine E-Mail mit Anhang an mich selbst geschickt und den Anhang geöffnet.'),
    CHECK('Ich weiß, dass die eingefügte Tabelle eine Kopie ist.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 4'),
    table([4500, 4570], [['Lücke', 'Angabe'], ['Stromverbrauch 2025 in kWh', '47.850'], ['Monat mit dem höchsten Verbrauch', 'Januar (4.850 kWh)'], ['Monat mit dem niedrigsten Verbrauch', 'August (3.240 kWh)']]),
    H2('Aufgabe 6'),
    P('Weder Tabelle noch Diagramm ändern sich in Word. Beim normalen Einfügen nimmt Word eine **Kopie** mit: Die Tabelle wird eine Word-Tabelle, das Diagramm bringt seine Daten mit. Ändern sich die Zahlen in Excel, kopieren Sie Tabelle und Diagramm neu. Wie man beides **verknüpft**, sodass Word sich mitändert, zeigt das Aufbaumodul „Verknüpfung“.'),
    P('Der fertige Bericht steht in Block-11-Loesung-Bericht.docx.'),
  ], 'Übungsblatt Block 11 · Microsoft 365 im Facility Management');
})();
