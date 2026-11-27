// Word-Dateien Block 01 erzeugen (Begrüßungsmappe, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-01-docx.js _resources/Grundkurs/Block-01
// Das Übungsblatt muss inhaltlich Grundkurs/Block-01-Uebungsblatt.md entsprechen.
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
  // Begrüßungsmappe
  await save('Block-01-Willkommen.docx', 'Willkommen im Haus Lichtblick', [
    TITLE('Willkommen im Haus Lichtblick'),
    SUB('Begrüßungsmappe für die Koordination des Facility Managements'),
    P('Herzlich willkommen im Team! Sie übernehmen ab sofort die Koordination des Facility Managements im Haus Lichtblick. Diese Mappe gibt Ihnen einen ersten Überblick über das Gebäude, die Menschen, mit denen Sie zusammenarbeiten, und Ihre Aufgaben.'),
    H1('Das Gebäude'),
    table([2600, 6470], [
      ['Angabe', 'Haus Lichtblick'],
      ['Adresse', 'Sonnenallee 45, 10115 Berlin'],
      ['Typ', 'Bürogebäude'],
      ['Baujahr', '2010'],
      ['Geschosse', '5 (Erdgeschoss und 4 Obergeschosse)'],
      ['Nutzfläche', 'ca. 3.200 m²'],
      ['Mieter', '12 verschiedene Firmen'],
    ]),
    H1('Was wo ist'),
    BUL('**Erdgeschoss:** Eingangshalle, Empfang, Briefkastenraum, Technikraum 1 (Heizung), Lagerraum EG-01'),
    BUL('**1. bis 3. Obergeschoss:** Büros, je ein Besprechungs- oder Konferenzraum, Teeküche, WC'),
    BUL('**4. Obergeschoss:** Büros 401–406, Archivraum, Serverraum, Technikraum 2 (Lüftung)'),
    H1('Ihr Team im Haus'),
    table([2600, 2600, 3870], [
      ['Name', 'Aufgabe', 'E-Mail'],
      ['Thomas Weber', 'Hausmeister', 'thomas.weber@haus-lichtblick.de'],
      ['Maria Schmidt', 'Reinigungskraft', 'maria.schmidt@haus-lichtblick.de'],
      ['Jan Müller', 'Techniker', 'jan.mueller@haus-lichtblick.de'],
    ]),
    H1('Externe Dienstleister'),
    table([2600, 3270, 3200], [
      ['Bereich', 'Firma', 'Ansprechperson'],
      ['Hausverwaltung', 'Immobilien Fischer GmbH', 'Petra Schönfeld'],
      ['Gebäudereinigung', 'Sauber & Rein GmbH', 'Klara Nowak'],
      ['Heizungswartung', 'Heizungstechnik Berlin', '–'],
      ['Elektriker', 'Elektro Schulze', '–'],
      ['Aufzugswartung', 'Lift-Service Nord', '–'],
    ]),
    H1('Ihre Aufgaben'),
    BUL('Störungsmeldungen annehmen und an Hausmeister, Technik oder Dienstleister weitergeben – mit **Outlook**'),
    BUL('Wartungstermine für Heizung, Aufzüge und Brandschutz planen – mit **Outlook**'),
    BUL('Aushänge, Protokolle und Briefe an die Mieter schreiben – mit **Word**'),
    BUL('Listen führen: Mieter, Reinigungsmaterial, Energieverbrauch – mit **Excel**'),
    P('Die Mieterliste erhalten Sie als Excel-Datei. Bei Fragen erreichen Sie mich jederzeit.', { spacing: { before: 240, after: 120 } }),
    P('Petra Schönfeld', { spacing: { before: 240, after: 0 } }),
    P('Immobilien Fischer GmbH – Hausverwaltung Haus Lichtblick'),
  ], 'Übungsdatei Block 01 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden');

  // Übungsblatt
  const Q = [['Nr.', 'Frage', 'Ihre Antwort'],
    ['1', 'Wie heißt der Hausmeister des Hauses Lichtblick?', ''],
    ['2', 'Wie viele Geschosse hat das Gebäude?', ''],
    ['3', 'Welche Firma hat die größte Fläche gemietet?', ''],
    ['4', 'Wer ist Ansprechpartnerin der Praxis am Park?', ''],
    ['5', 'Welche Firmen sitzen im 1. OG?', '']];
  await save('Block-01-Uebungsblatt.docx', 'Übungsblatt Block 01 – Orientierung in Microsoft 365', [
    TITLE('Übungsblatt Block 01'),
    SUB('Orientierung in Microsoft 365'),
    P('**Sie brauchen:** einen PC mit Windows 11 und Microsoft 365 (Outlook, Word, Excel) und die Übungsdateien Block-01-Willkommen.docx und Block-01-Mieterliste.xlsx von der Seite zu Block 01.'),
    P('**Ihre Rolle:** Sie sind neu in der Koordination des Facility Managements im Haus Lichtblick. Die Hausverwaltung hat Ihnen eine Begrüßungsmappe (Word) und die Mieterliste (Excel) geschickt. Verschaffen Sie sich einen Überblick.'),
    H1('Aufgabe 1 – Dateien bereitlegen'),
    ...STEPS(['Laden Sie die beiden Übungsdateien herunter: anklicken, fertig.',
      'Die Dateien landen im Ordner **Downloads**. Dort holen Sie sie in Aufgabe 3 ab.']),
    H1('Aufgabe 2 – Programme starten und schließen'),
    ...STEPS(['Öffnen Sie über das Startmenü **Outlook**. Lassen Sie es geöffnet.',
      'Öffnen Sie über das Startmenü **Word**, danach **Excel**. Nutzen Sie dafür einmal das Suchfeld und einmal die Liste unter „Alle“.',
      'Prüfen Sie in der Taskleiste: Sehen Sie drei Programmsymbole mit einem Strich darunter?',
      'Schließen Sie Word und Excel wieder mit dem **X** oben rechts. Outlook bleibt offen.']),
    H1('Aufgabe 3 – Dateien öffnen'),
    ...STEPS(['Klicken Sie in der Taskleiste auf das Ordnersymbol (**Explorer**) und links auf **Downloads**.',
      'Doppelklicken Sie auf Block-01-Willkommen.docx. Die Datei öffnet sich in Word.',
      'Doppelklicken Sie auf Block-01-Mieterliste.xlsx. Die Datei öffnet sich in Excel.']),
    ...BOX('Merke:', ['Oben erscheint eine gelbe Leiste **„Geschützte Ansicht“**? Dateien aus dem Internet öffnen Word und Excel zuerst schreibgeschützt. Zum Lesen müssen Sie nichts tun. Möchten Sie etwas ändern, klicken Sie auf **„Bearbeitung aktivieren“**.'], BLUE, '2C7BC0'),
    H1('Aufgabe 4 – Zwei Fenster nebeneinander'),
    ...STEPS(['Ziehen Sie das Word-Fenster an der Titelleiste an den **linken** Bildschirmrand, bis es einrastet.',
      'Windows zeigt die übrigen Fenster. Klicken Sie auf Excel – es füllt die **rechte** Hälfte.']),
    H1('Aufgabe 5 – Hin und her'),
    P('Beantworten Sie die Fragen. Die Antworten stehen in der Begrüßungsmappe (Word) oder in der Mieterliste (Excel).'),
    table([700, 4570, 3800], Q, { minHeight: 600 }),
    P('Holen Sie anschließend Outlook in den Vordergrund – einmal über die Taskleiste, einmal mit **Alt+Tab**.', { spacing: { before: 160, after: 120 } }),
    H1('Aufgabe 6 – Drei Programme auf einen Blick'),
    ...STEPS(['Halten Sie die Maus über die Schaltfläche **„Maximieren“** im Outlook-Fenster.',
      'Wählen Sie ein Layout mit **drei Spalten** und klicken Sie das linke Feld an.',
      'Füllen Sie die beiden anderen Felder mit Word und Excel.']),
    H1('Aufgabe 7 – Aufräumen'),
    P('Schließen Sie Excel, Word und Outlook mit dem **X**. Fragt ein Programm, ob Sie speichern möchten, wählen Sie **„Nicht speichern“**.'),
    H1('Selbstcheck'),
    CHECK('Ich habe alle drei Programme über das Startmenü geöffnet.'),
    CHECK('Ich habe zwei Dateien aus dem Ordner Downloads geöffnet.'),
    CHECK('Ich habe zwei Fenster nebeneinander und drei Fenster im Andocklayout angeordnet.'),
    CHECK('Ich bin mit der Taskleiste und mit Alt+Tab zwischen den Programmen gewechselt.'),
    CHECK('Ich habe alle Programme wieder geschlossen.'),
    H2('Notizen'),
    ...[1, 2, 3, 4].map(() => new Paragraph({ spacing: { before: 300, after: 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 1 } }, children: [] })),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen zu Aufgabe 5'),
    ...STEPS(['Thomas Weber', 'Fünf: Erdgeschoss und vier Obergeschosse', 'Consulting Plus mit 520 m²', 'Lena Ott',
      'TechSolutions, Steuerbüro Hahn und Grünraum Architekten']),
  ], 'Übungsblatt Block 01 · Microsoft 365 im Facility Management');
})();
