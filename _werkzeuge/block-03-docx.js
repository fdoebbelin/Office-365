// Word-Dateien Block 03 erzeugen (Terminplan, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-03-docx.js _resources/Grundkurs/Block-03
// Das Übungsblatt muss inhaltlich Grundkurs/Block-03-Uebungsblatt.md entsprechen.
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
const RED = 'FBE9E7';
const ACHTUNG = s => BOX('Achtung:', [s], RED, 'B3261E');
const SUBBUL = s => new Paragraph({ children: runs(s), numbering: { reference: 'bullets', level: 0 }, indent: { left: 1134, hanging: 283 } });
const CHECKLISTE = ['Fluchtwege frei und beleuchtet', 'Feuerlöscher vorhanden und geprüft', 'Notbeleuchtung funktionsfähig', 'Rauchmelder getestet',
  'Erste-Hilfe-Kästen vollständig', 'Brandschutztüren schließen ordnungsgemäß', 'Notausgänge gekennzeichnet und zugänglich', 'Elektrische Geräte geprüft (VDE-Plakette)'];

(async () => {
  // Terminplan
  await save('Block-03-Terminplan.docx', 'Terminplan Facility Management – Haus Lichtblick', [
    TITLE('Terminplan'),
    SUB('Facility Management Haus Lichtblick · für die nächsten Wochen'),
    P('Guten Tag,'),
    P('hier die Termine, die Sie bitte in Ihren Kalender übernehmen. Für die Wartungen mit Dienstleistern empfehle ich eine Erinnerung einen Tag vorher – dann bleibt Zeit, Schlüssel und Zugang zu klären und die Mieter zu informieren.'),
    H1('Termine'),
    table([500, 2700, 2300, 1900, 1670], [
      ['Nr.', 'Was', 'Wann', 'Wo', 'Art'],
      ['1', 'Fluchtwege prüfen (Kontrollgang)', 'morgen, 10:00–10:30 Uhr', 'alle Etagen', 'Termin'],
      ['2', 'Aufzug gesperrt – Wartung Lift-Service Nord', 'ein Tag in der nächsten Woche, ganztägig', 'Personenaufzug', 'ganztägig'],
      ['3', 'Heizungswartung, Heizungstechnik Berlin', 'jeden ersten Montag im Monat, 08:00–09:30 Uhr', 'Technikraum 1 (Heizung)', 'Serie, monatlich'],
      ['4', 'Sicherheitsbegehung mit Thomas Weber und Jan Müller', 'nächster Donnerstag, 14:00–15:30 Uhr', 'Treffpunkt Eingangshalle', 'Besprechung'],
    ]),
    H1('Wiederkehrende Wartungen im Haus'),
    table([3000, 3070, 3000], [
      ['Anlage', 'Dienstleister', 'Intervall'],
      ['Heizung (Gas-Brennwertkessel)', 'Heizungstechnik Berlin', 'monatlich, jeden 1. Montag'],
      ['Aufzüge (Personen- und Lastenaufzug)', 'Lift-Service Nord', 'quartalsweise'],
      ['Feuerlöscher (15 Stück)', '–', 'jährlich'],
    ]),
    H1('Checkliste Sicherheitsbegehung'),
    P('Für Termin 4 – bitte in die Einladung übernehmen:'),
    ...STEPS(CHECKLISTE),
    P('Viele Grüße', { spacing: { before: 240, after: 0 } }),
    P('Petra Schönfeld', { spacing: { before: 0, after: 0 } }),
    P('Immobilien Fischer GmbH – Hausverwaltung Haus Lichtblick'),
  ], 'Übungsdatei Block 03 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden');

  // Übungsblatt
  await save('Block-03-Uebungsblatt.docx', 'Übungsblatt Block 03 – Kalender und Termine', [
    TITLE('Übungsblatt Block 03'),
    SUB('Kalender und Termine'),
    P('**Sie brauchen:** einen PC mit dem neuen Outlook und Ihrem E-Mail-Konto, Word zum Öffnen der Übungsdatei und die Übungsdatei Block-03-Terminplan.docx von der Seite zu Block 03.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Petra Schönfeld von der Hausverwaltung hat Ihnen den Terminplan für die nächsten Wochen geschickt. Tragen Sie die Termine in Ihren Outlook-Kalender ein, damit Sie rechtzeitig erinnert werden.'),
    ...ACHTUNG('Laden Sie zu Besprechungen **nur eigene Adressen** ein. Die Personen im Haus Lichtblick sind erfunden. Am Ende löschen Sie die Übungstermine wieder (Aufgabe 8).'),
    H1('Aufgabe 1 – Kalender und Ansichten'),
    ...STEPS(['Öffnen Sie Outlook und klicken Sie in der App-Leiste links auf das **Kalendersymbol**.',
      'Wechseln Sie nacheinander in die Ansichten **Tag**, **Arbeitswoche** und **Monat**.',
      'Blättern Sie mit den Pfeilen einen Monat vor und springen Sie mit **„Heute“** zurück.',
      'Bleiben Sie in der Ansicht **Arbeitswoche**.']),
    H1('Aufgabe 2 – Termin, Besprechung oder ganztägig?'),
    P('Entscheiden Sie für jede Situation.'),
    table([600, 5470, 3000], [
      ['Nr.', 'Situation', 'Termin, Besprechung oder ganztägig?'],
      ['1', 'Sauber & Rein reinigt am Samstag die Teppiche im 3. OG – ohne feste Uhrzeit.', ''],
      ['2', 'Sie möchten daran denken, die Zählerstände für Strom abzulesen.', ''],
      ['3', 'Hausmeisterrunde mit Thomas Weber, Maria Schmidt und Jan Müller im Besprechungsraum 1.10', ''],
      ['4', 'Die Feuerlöscher werden einmal im Jahr geprüft.', ''],
    ], { minHeight: 600 }),
    H1('Aufgabe 3 – Ein Termin mit Erinnerung'),
    P('Öffnen Sie in Word die Übungsdatei Block-03-Terminplan.docx. Dort steht als Nummer 1 der Kontrollgang „Fluchtwege prüfen“.'),
    ...STEPS(['Klicken Sie im Kalender auf **„Neues Ereignis“**.', 'Titel: Fluchtwege prüfen',
      'Datum: morgen, Beginn 10:00 Uhr, Ende 10:30 Uhr', 'Ort: alle Etagen', 'Erinnerung: **15 Minuten vorher**',
      'Klicken Sie auf **„Speichern“**. Prüfen Sie: Steht der Termin im Kalender?']),
    H1('Aufgabe 4 – Ein ganztägiges Ereignis'),
    P('Nummer 2 im Terminplan: Lift-Service Nord wartet den Personenaufzug. Er ist den ganzen Tag gesperrt.'),
    ...STEPS(['Öffnen Sie **„Neues Ereignis“**.', 'Titel: Aufzug gesperrt – Wartung Lift-Service Nord',
      'Datum: ein Tag Ihrer Wahl in der nächsten Woche', 'Schalten Sie **„Ganztägig“** ein.',
      'Erinnerung: **1 Tag vorher**. Klicken Sie auf **„Speichern“**.', 'Wo steht das Ereignis in der Arbeitswoche?']),
    H1('Aufgabe 5 – Die Heizungswartung als Serie'),
    P('Nummer 3 im Terminplan: Heizungstechnik Berlin wartet die Heizung jeden ersten Montag im Monat von 08:00 bis 09:30 Uhr im Technikraum 1.'),
    ...STEPS(['Öffnen Sie **„Neues Ereignis“**. Titel: Heizungswartung, Ort: Technikraum 1 (Heizung).',
      'Datum: der **erste Montag des nächsten Monats**, Beginn 08:00 Uhr, Ende 09:30 Uhr.',
      'Klicken Sie auf **„Serie erstellen“** (oder „Wiederholen“).',
      'Muster: **Monatlich**, **am ersten Montag**. Ende: ein Datum in einem halben Jahr. Übernehmen Sie die Einstellung.',
      'Erinnerung: **1 Tag vorher**. Klicken Sie auf **„Speichern“**.',
      'Wechseln Sie in die Ansicht **Monat** und blättern Sie vor: Steht die Heizungswartung jeden Monat am ersten Montag?']),
    H1('Aufgabe 6 – Die Sicherheitsbegehung'),
    P('Nummer 4 im Terminplan: eine Sicherheitsbegehung mit Thomas Weber und Jan Müller.'),
    ...STEPS(['Öffnen Sie **„Neues Ereignis“**. Titel: Sicherheitsbegehung, Ort: Treffpunkt Eingangshalle.',
      'Datum: nächster Donnerstag, Beginn 14:00 Uhr, Ende 15:30 Uhr.',
      'Kopieren Sie die **Checkliste Sicherheitsbegehung** aus dem Terminplan in das große Textfeld (Strg+C, Strg+V).',
      'Tragen Sie im Feld **„Teilnehmende einladen“** eine Adresse ein:']),
    SUBBUL('Haben Sie eine **zweite eigene Adresse**, nehmen Sie diese – sie steht für Thomas Weber. Klicken Sie auf **„Senden“** und sehen Sie im zweiten Postfach nach: Die Einladung ist da. Sagen Sie zu.'),
    SUBBUL('Haben Sie **nur eine Adresse**, tragen Sie sie ein und beobachten Sie, wie aus „Speichern“ **„Senden“** wird. Löschen Sie die Adresse wieder und klicken Sie auf **„Speichern“** – so bleibt die Begehung als Termin in Ihrem Kalender.'),
    H1('Aufgabe 7 – Verschieben und ändern'),
    ...STEPS(['Ziehen Sie den Termin „Fluchtwege prüfen“ mit der Maus auf 11:00 Uhr.',
      'Die Heizungswartung im zweiten Monat fällt aus und findet einen Tag später statt: Öffnen Sie **nur diesen einen Termin** der Serie und ändern Sie das Datum auf den Dienstag. Achten Sie auf die Frage von Outlook: nur dieses Ereignis, nicht die ganze Serie.',
      'Prüfen Sie im Monatsblick: Nur dieser eine Termin ist verschoben.',
      'Für Schnelle: Markieren Sie die Heizungswartung mit Rechtsklick → **„Kategorisieren“** rot.']),
    H1('Aufgabe 8 – Aufräumen'),
    ...STEPS(['Löschen Sie „Fluchtwege prüfen“, das Ereignis „Aufzug gesperrt“ und die Sicherheitsbegehung: anklicken, **Entf**.',
      'Löschen Sie die Heizungswartung: Wählen Sie diesmal die **ganze Serie**.',
      'Prüfen Sie im Monatsblick, dass alle Übungstermine verschwunden sind.']),
    H1('Selbstcheck'),
    CHECK('Ich bin zwischen E-Mail und Kalender gewechselt und habe die Ansicht geändert.'),
    CHECK('Ich kann Termin, Besprechung und ganztägiges Ereignis unterscheiden.'),
    CHECK('Ich habe einen Termin mit Erinnerung und ein ganztägiges Ereignis angelegt.'),
    CHECK('Ich habe die Heizungswartung als monatliche Serie angelegt.'),
    CHECK('Ich habe gesehen, wie aus „Speichern“ „Senden“ wird.'),
    CHECK('Ich habe einen Termin verschoben und einen einzelnen Termin einer Serie geändert.'),
    CHECK('Ich habe die Übungstermine und die Serie wieder gelöscht.'),
    H2('Notizen'),
    ...[1, 2, 3].map(() => new Paragraph({ spacing: { before: 300, after: 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 1 } }, children: [] })),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 2'),
    ...STEPS(['Ganztägiges Ereignis – kein fester Zeitpunkt', 'Termin – nur für Sie',
      'Besprechung – drei Personen werden eingeladen', 'Termin als Serie: jährlich']),
    H2('Aufgabe 4'),
    P('Ganztägige Ereignisse stehen ganz oben über dem Tag, nicht zwischen den Uhrzeiten.'),
    H2('Aufgabe 5'),
    P('Die Heizungswartung steht in jedem Monat am ersten Montag von 08:00 bis 09:30 Uhr – bis zum Enddatum, das Sie gewählt haben.'),
  ], 'Übungsblatt Block 03 · Microsoft 365 im Facility Management');
})();
