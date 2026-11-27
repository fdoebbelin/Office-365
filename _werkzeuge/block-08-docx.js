// Word-Dateien Block 08 erzeugen (Übungsblatt; die Excel-Dateien erzeugt block-08-xlsx.py).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-08-docx.js _resources/Grundkurs/Block-08
// Das Übungsblatt muss inhaltlich Grundkurs/Block-08-Uebungsblatt.md entsprechen.
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
const DIFF = [['Allzweckreiniger', '5'], ['Müllbeutel 120 l', '50'], ['Handtuchpapier', '20'], ['Toilettenpapier', '20'], ['Glasreiniger', '-2'],
  ['Bodenreiniger', '4'], ['Desinfektionsmittel', '1'], ['Schwämme', '5'], ['Einweghandschuhe', '-5'], ['Wischmopps', '1']];

(async () => {
  await save('Block-08-Uebungsblatt.docx', 'Übungsblatt Block 08 – Excel-Grundlagen', [
    TITLE('Übungsblatt Block 08'),
    SUB('Excel-Grundlagen'),
    P('**Sie brauchen:** einen PC mit Excel und die Übungsdatei Block-08-Inventarliste.xlsx von der Seite zu Block 08. Die Lösungsdatei Block-08-Loesung-Inventarliste.xlsx zeigt die fertige Liste – sehen Sie sie erst am Ende an.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Maria Schmidt aus der Reinigung hat angefangen, das Reinigungsmaterial im Lagerraum EG-01 zu zählen, und die ersten fünf Artikel eingetragen. Sie ergänzen den Rest und finden heraus, was nachbestellt werden muss.'),
    H1('Aufgabe 1 – Excel erkunden'),
    ...STEPS(['Öffnen Sie Block-08-Inventarliste.xlsx aus dem Ordner Downloads und klicken Sie auf **„Bearbeitung aktivieren“**.',
      'Suchen Sie Namenfeld, Bearbeitungsleiste, Spaltenköpfe, Zeilennummern und das Tabellenblatt „Inventar“.',
      'Klicken Sie auf die Zelle **C5**. Was steht im Namenfeld, was in der Bearbeitungsleiste?']),
    H1('Aufgabe 2 – Sich bewegen'),
    ...STEPS(['Klicken Sie ins **Namenfeld**, tippen Sie C9 und drücken Sie **Enter**. Welche Zahl steht dort, und zu welchem Artikel gehört sie?',
      'Drücken Sie **Strg+Pos1**. Wo sind Sie jetzt?',
      'Klicken Sie auf **A4** und drücken Sie **Strg+Pfeil nach unten**. In welcher Zeile landen Sie?']),
    H1('Aufgabe 3 – Unter eigenem Namen speichern'),
    P('Speichern Sie die Datei mit **„Datei“** → **„Speichern unter“** → **„Durchsuchen“** in Dokumente\\Haus-Lichtblick unter dem Namen Inventarliste.'),
    H1('Aufgabe 4 – Daten eingeben'),
    ...STEPS(['Klicken Sie auf **B2** (neben „Stand:“) und tippen Sie das heutige Datum mit Punkten, zum Beispiel 15.04.2025. Drücken Sie **Enter**.',
      'Tragen Sie ab Zeile 10 die übrigen fünf Artikel ein. Springen Sie mit **Tab** nach rechts; nach der letzten Zelle einer Zeile bringt Sie **Enter** an den Anfang der nächsten.']),
    table([2600, 2200, 1300, 1650, 1320], [['Artikel', 'Lagerort', 'Bestand', 'Mindestmenge', 'Einheit'],
      ['Bodenreiniger', 'Lagerraum EG-01', '12', '8', 'Flaschen'], ['Desinfektionsmittel', 'Lagerraum EG-01', '6', '5', 'Flaschen'],
      ['Schwämme', 'Lagerraum EG-01', '25', '20', 'Stück'], ['Einweghandschuhe', 'Lagerraum EG-01', '5', '10', 'Pakete'],
      ['Wischmopps', 'Lagerraum EG-01', '4', '3', 'Stück']]),
    P('Prüfen Sie: Stehen alle Zahlen rechts in der Zelle? Steht eine links, ist sie als Text eingegeben – neu tippen.', { spacing: { before: 160, after: 120 } }),
    H1('Aufgabe 5 – Spaltenbreite und Kopfzeile'),
    ...STEPS(['Markieren Sie die Spaltenköpfe **A bis E** und doppelklicken Sie auf eine Trennlinie zwischen zwei Spaltenköpfen. Alle Spalten passen sich an.',
      'Markieren Sie die Kopfzeile **A4 bis E4** und machen Sie sie **fett** (Strg+Umschalt+F).',
      'Geben Sie der Kopfzeile eine helle **Füllfarbe**.']),
    H1('Aufgabe 6 – Die erste Formel'),
    ...STEPS(['Tippen Sie in **F4** die Überschrift Differenz. Formatieren Sie sie wie die übrige Kopfzeile.',
      'Klicken Sie auf **F5** und geben Sie die Formel ein: **=** tippen, **C5** anklicken, **-** tippen, **D5** anklicken, **Enter**.',
      'Schauen Sie in die Bearbeitungsleiste von F5: Dort steht =C5-D5, in der Zelle das Ergebnis.',
      'Geben Sie die Formel genauso für die Zeilen 6 bis 14 ein – in jeder Zeile mit den Zellen dieser Zeile (=C6-D6, =C7-D7 …).']),
    H1('Aufgabe 7 – Auswerten'),
    ...STEPS(['Welche Artikel haben eine **negative** Differenz und müssen nachbestellt werden?',
      'Bei welchem Artikel ist am meisten über der Mindestmenge?',
      'Eine Lieferung kommt: 4 Flaschen Glasreiniger. Ändern Sie den Bestand von Glasreiniger auf 12. Was zeigt jetzt die Differenz?',
      'Machen Sie die Änderung mit **Strg+Z** rückgängig – die Lieferung war nur eine Übung.',
      'Speichern Sie mit **Strg+S** und vergleichen Sie mit der Lösungsdatei.']),
    H1('Selbstcheck'),
    CHECK('Ich habe Namenfeld und Bearbeitungsleiste gefunden und mit dem Namenfeld eine Zelle angesprungen.'),
    CHECK('Ich habe Text, Zahlen und ein Datum eingegeben.'),
    CHECK('Ich habe Spaltenbreiten angepasst und die Kopfzeile hervorgehoben.'),
    CHECK('Ich habe eine Formel mit Zelladressen eingegeben.'),
    CHECK('Ich habe gesehen, dass Excel neu rechnet, wenn sich eine Zahl ändert.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 1'),
    P('Im Namenfeld steht C5, in der Bearbeitungsleiste 15 (Bestand Allzweckreiniger).'),
    H2('Aufgabe 2'),
    ...STEPS(['In C9 steht **8** – der Bestand von Glasreiniger.', 'In **A1**.',
      'In **Zeile 9** – dem letzten ausgefüllten Artikel, bevor Sie die Liste ergänzt haben. Nach Aufgabe 4 landen Sie in Zeile 14.']),
    H2('Aufgabe 6'),
    table([4000, 2000], [['Artikel', 'Differenz'], ...DIFF]),
    H2('Aufgabe 7'),
    ...STEPS(['**Glasreiniger** (-2) und **Einweghandschuhe** (-5)', '**Müllbeutel 120 l** mit 50 Stück über der Mindestmenge',
      'Die Differenz ist jetzt **2** (12 − 10).']),
  ], 'Übungsblatt Block 08 · Microsoft 365 im Facility Management');
})();
