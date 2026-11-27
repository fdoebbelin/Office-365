// Word-Dateien Block 07 erzeugen (Trainingsdokument roh und als Lösung, Übungsblatt mit Quiz).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-07-docx.js _resources/Grundkurs/Block-07
// Das Übungsblatt muss inhaltlich Grundkurs/Block-07-Uebungsblatt.md entsprechen.
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
const AUF = s => new Paragraph({ spacing: { before: 280, after: 80 }, shading: { type: ShadingType.CLEAR, color: 'auto', fill: SOFT },
  children: runs(s, { color: NAVY }) });
const plain = s => new Paragraph({ spacing: { after: 0 }, children: s ? [new TextRun(s)] : [] });
const T = (text, o = {}) => new TextRun({ text, ...o });
const LEER2 = ['Eingangshalle', '', '', 'Empfang', '', 'Briefkastenraum'];
if (LEER2.filter(s => s === '').length !== 3) throw new Error('Aufgabe 2: 3 leere Absätze erwartet');
const RAEUME = ['Technikraum 1 (Heizung)', 'Lagerraum EG-01', 'Archivraum', 'Serverraum'];
const PRUEF = ['Notbeleuchtung funktionsfähig', 'Rauchmelder getestet', 'Erste-Hilfe-Kästen vollständig'];
const BESPR = [['Etage', 'Raum'], ['1. OG', 'Besprechungsraum 1.10'], ['2. OG', 'Besprechungsraum 2.10'], ['3. OG', 'Konferenzraum 3.10']];
const A = ['**Aufgabe 1** – Machen Sie das Wort „Fluchtwege“ fett und den ganzen Satz kursiv.',
  '**Aufgabe 2** – Blenden Sie die Formatierungszeichen ein und löschen Sie die leeren Absätze zwischen den drei Räumen.',
  '**Aufgabe 3** – Machen Sie aus den vier Räumen eine Aufzählung.',
  '**Aufgabe 4** – Machen Sie aus den drei Prüfpunkten eine nummerierte Liste.',
  '**Aufgabe 5** – Weisen Sie der Zeile „Besprechungsräume“ die Formatvorlage Überschrift 2 zu.',
  '**Aufgabe 6** – Fügen Sie unter „Besprechungsräume“ eine Tabelle mit 2 Spalten und 4 Zeilen ein und füllen Sie sie: Etage | Raum; 1. OG | Besprechungsraum 1.10; 2. OG | Besprechungsraum 2.10; 3. OG | Konferenzraum 3.10. Erste Zeile fett.',
  '**Aufgabe 7** – Fassen Sie Name und Firma mit Umschalt+Enter in einem Absatz zusammen.'];
const QUIZ = [['Nr.', 'Frage', 'a', 'b', 'c'],
  ['1', 'Womit wechseln Sie im neuen Outlook zwischen E-Mail und Kalender?', 'Menüband', 'App-Leiste', 'Lesebereich'],
  ['2', 'Wer steht in „Bcc“?', 'wer etwas tun soll', 'wer Bescheid wissen soll', 'wer eine Kopie bekommt, ohne dass die anderen es sehen'],
  ['3', 'Welcher Betreff ist am besten?', 'Dringend!!!', 'Frage zur Heizung', 'Heizungsausfall – Büro 305 bleibt kalt'],
  ['4', 'Wo liegt eine angefangene, noch nicht gesendete E-Mail?', 'Entwürfe', 'Gesendete Elemente', 'Gelöschte Elemente'],
  ['5', '„Allen antworten“ geht an …', 'nur die Person, die geschrieben hat', 'sie und alle aus „An“ und „Cc“', 'alle Kontakte im Adressbuch'],
  ['6', 'Womit beginnt im neuen Outlook jeder Kalendereintrag?', '„Neuer Termin“', '„Neue Besprechung“', '„Neues Ereignis“'],
  ['7', 'Der Aufzug ist einen ganzen Tag gesperrt. Was legen Sie an?', 'Termin von 0 bis 24 Uhr', 'ganztägiges Ereignis', 'Serie'],
  ['8', 'Sie löschen einen Termin einer Serie. Was fragt Outlook?', 'nichts', 'nur dieses Ereignis oder die ganze Serie', 'nach dem Kennwort'],
  ['9', 'Welches Tastenkürzel macht in Word Text fett?', 'Strg+F', 'Strg+Umschalt+F', 'Alt+F'],
  ['10', 'Was zeigt das Zeichen ¶?', 'ein Absatzende (Enter)', 'ein Leerzeichen', 'einen Seitenumbruch'],
  ['11', 'Wie beginnen Sie eine neue Zeile im selben Absatz?', 'Enter', 'Umschalt+Enter', 'Tab'],
  ['12', 'Was passiert mit einem Dokument, das Sie nie gespeichert haben, wenn Sie Word schließen?', 'Word speichert es immer selbst', 'es ist weg, wenn Sie „Nicht speichern“ wählen', 'es landet im Papierkorb'],
  ['13', 'Prüfpunkte, auf die man sich mit „Punkt 6“ bezieht, stehen am besten als …', 'Aufzählung', 'nummerierte Liste', 'Fließtext'],
  ['14', 'Wie springen Sie in einer Word-Tabelle in die nächste Zelle?', 'Enter', 'Tab', 'Leertaste'],
  ['15', 'Wo sehen Sie vor dem Drucken, wie die Seite aussieht?', '„Datei“ → „Drucken“', '„Ansicht“ → „Lineal“', '„Layout“ → „Seitenränder“']];
const LOES = [['Nr.', 'Richtig', 'Nachschlagen'], ['1', 'b – App-Leiste', 'Block 02'], ['2', 'c – Kopie, die die anderen nicht sehen', 'Block 02'],
  ['3', 'c – Was und wo stehen im Betreff', 'Block 02'], ['4', 'a – Entwürfe', 'Block 02'], ['5', 'b – Absender und alle aus „An“ und „Cc“', 'Block 02'],
  ['6', 'c – „Neues Ereignis“', 'Block 03'], ['7', 'b – ganztägiges Ereignis', 'Block 03'], ['8', 'b – nur dieses Ereignis oder die ganze Serie', 'Block 03'],
  ['9', 'b – Strg+Umschalt+F', 'Block 04'], ['10', 'a – Absatzende', 'Block 04'], ['11', 'b – Umschalt+Enter', 'Block 04'], ['12', 'b – ohne Speichern ist es weg', 'Block 04'],
  ['13', 'b – nummerierte Liste', 'Block 05'], ['14', 'b – Tab', 'Block 05'], ['15', 'a – „Datei“ → „Drucken“, Vorschau rechts', 'Block 05']];
const FU = 'Übungsdatei Block 07 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden';
const FL = 'Lösungsdatei Block 07 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden';

(async () => {
  await save('Block-07-Training.docx', 'Trainingsdokument Word', [
    P('Trainingsdokument Word – Haus Lichtblick'),
    AUF(A[0]), plain('Fluchtwege müssen immer frei und beleuchtet sein.'),
    AUF(A[1]), ...LEER2.map(plain),
    AUF(A[2]), ...RAEUME.map(plain),
    AUF(A[3]), ...PRUEF.map(plain),
    AUF(A[4]), plain('Besprechungsräume'),
    AUF(A[5]), plain(''),
    AUF(A[6]), plain('Petra Schönfeld'), plain('Immobilien Fischer GmbH'),
  ], FU);
  await save('Block-07-Loesung-Training.docx', 'Trainingsdokument Word (Lösung)', [
    P('Trainingsdokument Word – Haus Lichtblick'),
    AUF(A[0]), new Paragraph({ spacing: { after: 0 }, children: [T('Fluchtwege', { bold: true, italics: true }), T(' müssen immer frei und beleuchtet sein.', { italics: true })] }),
    AUF(A[1]), ...LEER2.filter(Boolean).map(plain),
    AUF(A[2]), ...RAEUME.map(BUL),
    AUF(A[3]), ...STEPS(PRUEF),
    AUF(A[4]), H2('Besprechungsräume'),
    AUF(A[5]), table([3000, 4000], BESPR),
    AUF(A[6]), new Paragraph({ spacing: { after: 0 }, children: [T('Petra Schönfeld'), new TextRun({ break: 1 }), T('Immobilien Fischer GmbH')] }),
  ], FL);

  await save('Block-07-Uebungsblatt.docx', 'Übungsblatt Block 07 – Selbsttest Outlook und Word', [
    TITLE('Übungsblatt Block 07'),
    SUB('Selbsttest Outlook und Word'),
    P('**Sie brauchen:** einen PC mit dem neuen Outlook, Ihrem E-Mail-Konto und Word sowie das Trainingsdokument Block-07-Training.docx von der Seite zu Block 07.'),
    P('**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Bevor Sie mit Excel die Listen und Zahlen des Hauses übernehmen, prüfen Sie, wie sicher Sie in Outlook und Word schon sind.'),
    H1('Teil 1 – Quiz'),
    P('Kreuzen Sie je Frage **eine** Antwort an. Nicht nachsehen!'),
    table([500, 3170, 1800, 1800, 1800], QUIZ),
    P('**Meine Punktzahl:** ____ von 15', { spacing: { before: 200, after: 120 } }),
    H1('Teil 2 – Trainingsdokument Word'),
    ...STEPS(['Öffnen Sie Block-07-Training.docx, klicken Sie auf „Bearbeitung aktivieren“ und speichern Sie die Datei in Dokumente\\Haus-Lichtblick als Training-Word.',
      'Im Dokument stehen **sieben kurze Aufgaben**, jede unter einer eigenen Zeile „Aufgabe …“. Lösen Sie sie der Reihe nach – möglichst ohne nachzusehen.',
      'Speichern Sie und vergleichen Sie mit Block-07-Loesung-Training.docx.']),
    H1('Teil 3 – Drei schnelle Aufgaben in Outlook'),
    P('Nur an **Ihre eigene Adresse**.'),
    ...STEPS(['**Bcc:** Schreiben Sie eine E-Mail mit dem Betreff Test Bcc. Ihre Adresse steht nur in **Bcc**, das Feld „An“ bleibt leer. Senden Sie. Kommt sie an?',
      '**Weiterleiten:** Leiten Sie die E-Mail „Test Bcc“ an Ihre eigene Adresse weiter und schreiben Sie einen Satz Kommentar darüber. Womit beginnt der Betreff?',
      '**Ganztägig:** Legen Sie für einen Samstag im nächsten Monat das ganztägige Ereignis Reinigung Teppiche 3. OG – Sauber & Rein an. Löschen Sie es danach wieder, ebenso die beiden Test-E-Mails.']),
    H1('Selbstcheck'),
    CHECK('Ich habe mindestens 12 der 15 Quizfragen richtig beantwortet.'),
    CHECK('Ich habe die sieben Aufgaben im Trainingsdokument gelöst.'),
    CHECK('Ich habe die drei Outlook-Aufgaben erledigt und wieder aufgeräumt.'),
    CHECK('Ich weiß, welche Blöcke ich noch einmal ansehen möchte.'),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Teil 1 – Quiz'),
    table([700, 5870, 2500], LOES),
    H2('Teil 2'),
    P('Die gelösten Aufgaben stehen in Block-07-Loesung-Training.docx. In Aufgabe 2 sind es **3 leere Absätze**.'),
    H2('Teil 3'),
    ...STEPS(['Ja, die E-Mail kommt an. Bcc-Empfänger bekommen die E-Mail, auch wenn niemand in „An“ steht – nur sieht sie keiner.',
      'Der Betreff beginnt mit **WG:**.', 'Das ganztägige Ereignis steht oben über dem Samstag, nicht zwischen den Uhrzeiten.']),
  ], 'Übungsblatt Block 07 · Microsoft 365 im Facility Management');
})();
