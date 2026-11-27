// Word-Dateien Block 10 erzeugen (Übungsblatt; die Excel-Dateien erzeugt block-10-xlsx.py).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-10-docx.js _resources/Grundkurs/Block-10
// Das Übungsblatt muss inhaltlich Grundkurs/Block-10-Uebungsblatt.md entsprechen.
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
(async () => {
  await save('Block-10-Uebungsblatt.docx', 'Übungsblatt Block 10 – Diagramme erstellen', [
    TITLE('Übungsblatt Block 10'),
    SUB('Diagramme erstellen'),
    P('**Sie brauchen:** einen PC mit Excel und die Übungsdatei Block-10-Diagramme.xlsx von der Seite zu Block 10. Die Lösungsdatei Block-10-Loesung-Diagramme.xlsx zeigt die fertigen Diagramme – sehen Sie sie erst am Ende an. Ein Drucker ist schön, aber nicht nötig.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Für den Jahresbericht möchte Petra Schönfeld von der Hausverwaltung den Stromverbrauch 2025 als Diagramm sehen – und auf einen Blick, wie sich die vermietete Fläche auf die Etagen verteilt.'),
    H1('Aufgabe 1 – Vorbereiten'),
    ...STEPS(['Öffnen Sie Block-10-Diagramme.xlsx aus dem Ordner Downloads und klicken Sie auf **„Bearbeitung aktivieren“**.',
      'Speichern Sie die Datei in Dokumente\\Haus-Lichtblick unter dem Namen Diagramme-2025.',
      'Sehen Sie sich das Blatt **„Strom 2025“** an. In welchem Monat war der Verbrauch am höchsten? Wie lange brauchen Sie, um das in der Tabelle zu finden?']),
    H1('Aufgabe 2 – Das Säulendiagramm'),
    ...STEPS(['Markieren Sie **A3 bis B15** – die Überschriften und alle zwölf Monate, **ohne** die Summe.',
      '**„Einfügen“** → **„Säulen- oder Balkendiagramm einfügen“** → **„Gruppierte Säulen“**.',
      'Schauen Sie auf das Diagramm: Welche Säule ist am höchsten, welche am niedrigsten? Wie lange brauchen Sie jetzt?']),
    H1('Aufgabe 3 – Beschriften'),
    ...STEPS(['Klicken Sie auf den Diagrammtitel und ändern Sie ihn in Stromverbrauch Haus Lichtblick 2025.',
      'Klicken Sie auf das **+** neben dem Diagramm und setzen Sie das Häkchen bei **„Achsentitel“**.',
      'Senkrechte Achse: Verbrauch in kWh. Waagerechte Achse: Monat.',
      'Für Schnelle: Wählen Sie auf der Registerkarte **„Diagrammentwurf“** eine andere Diagrammformatvorlage.']),
    H1('Aufgabe 4 – Verschieben und vergrößern'),
    ...STEPS(['Fassen Sie das Diagramm am Rand an und ziehen Sie es rechts neben die Tabelle, sodass die linke obere Ecke etwa in Zelle **D3** liegt.',
      'Ziehen Sie an der rechten unteren Ecke, bis das Diagramm etwa bis Spalte **L** reicht.']),
    H1('Aufgabe 5 – Das Diagramm rechnet mit'),
    ...STEPS(['Ändern Sie den Verbrauch im **Dezember** (B15) auf 5000. Was passiert mit der Dezember-Säule?',
      'Machen Sie die Änderung mit **Strg+Z** rückgängig.']),
    H1('Aufgabe 6 – Das Kreisdiagramm'),
    P('Wechseln Sie auf das Blatt **„Flächen“**.'),
    ...STEPS(['Markieren Sie **A3 bis B7** – die vier Etagen ohne die Summe.',
      '**„Einfügen“** → **„Kreis- oder Ringdiagramm einfügen“** → unter „2D-Kreis“ den ersten **„Kreis“**.',
      'Ändern Sie den Titel in Vermietete Fläche je Etage.',
      'Klicken Sie auf das **+** und schalten Sie **„Datenbeschriftungen“** ein. Klicken Sie auf den kleinen Pfeil daneben → **„Weitere Optionen“** und setzen Sie das Häkchen bei **„Prozentsatz“**, das bei **„Wert“** nehmen Sie heraus.',
      'Welche Etage hat den größten Anteil, welche den kleinsten?']),
    H1('Aufgabe 7 – Drucken und speichern'),
    ...STEPS(['Wechseln Sie zurück auf „Strom 2025“ und klicken Sie das Säulendiagramm einmal an.',
      '**Strg+P**: Steht unter „Einstellungen“ **„Ausgewähltes Diagramm drucken“**? Prüfen Sie die Vorschau und drucken Sie, wenn ein Drucker angeschlossen ist.',
      'Speichern Sie mit **Strg+S** und vergleichen Sie mit der Lösungsdatei.']),
    H1('Selbstcheck'),
    CHECK('Ich habe die richtigen Daten ohne Summe markiert und ein Säulendiagramm eingefügt.'),
    CHECK('Mein Diagramm hat einen aussagekräftigen Titel und zwei Achsentitel.'),
    CHECK('Ich habe das Diagramm verschoben und vergrößert.'),
    CHECK('Ich habe gesehen, dass das Diagramm sich mit der Tabelle ändert.'),
    CHECK('Ich habe ein Kreisdiagramm mit Prozentwerten erstellt.'),
    CHECK('Ich habe nur das Diagramm in der Druckvorschau gesehen.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgaben 1 und 2'),
    P('Am höchsten war der Verbrauch im **Januar** (4.850 kWh), am niedrigsten im **August** (3.240 kWh). Im Diagramm sieht man das auf einen Blick – in der Tabelle muss man alle zwölf Zahlen vergleichen.'),
    H2('Aufgabe 5'),
    P('Die Dezember-Säule wächst sofort auf 5.000 und ist jetzt die höchste. Nach Strg+Z ist sie wieder bei 4.530.'),
    H2('Aufgabe 6'),
    table([2500, 2500, 2000], [['Etage', 'Fläche', 'Anteil'], ['1. OG', '750 m²', '32 %'], ['2. OG', '570 m²', '24 %'], ['3. OG', '760 m²', '32 %'], ['4. OG', '300 m²', '13 %']]),
    P('Den größten Anteil hat das **3. OG** (760 m², knapp vor dem 1. OG mit 750 m²), den kleinsten das **4. OG** (300 m²). Excel rundet die Prozentwerte; zusammen ergeben sie deshalb 101 %.', { spacing: { before: 160, after: 120 } }),
    P('Die fertigen Diagramme stehen in Block-10-Loesung-Diagramme.xlsx.'),
  ], 'Übungsblatt Block 10 · Microsoft 365 im Facility Management');
})();
