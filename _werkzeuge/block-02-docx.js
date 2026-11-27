// Word-Dateien Block 02 erzeugen (Mailtexte, Übungsblatt).
// Voraussetzung: npm-Paket docx (npm install docx@9 in einem Arbeitsordner außerhalb des Repositorys, NODE_PATH setzen).
// Aufruf: node _werkzeuge/block-02-docx.js _resources/Grundkurs/Block-02
// Das Übungsblatt muss inhaltlich Grundkurs/Block-02-Uebungsblatt.md entsprechen.
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
const MAIL = (betreff, lines) => BOX('', ['**Betreff:** ' + betreff, '', ...lines], SOFT, NAVY);
const ROLLE = '**Ihre Rolle:** Sie sind die Koordination des Facility Managements im Haus Lichtblick. Heute Morgen meldet Lena Ott von der Praxis am Park: Der Wasserhahn in der Teeküche im 2. OG tropft. Sie geben die Meldung an den Hausmeister weiter, halten die Hausverwaltung auf dem Laufenden und sortieren danach Ihre Post.';
const NUR_EIGENE = 'Senden Sie alle E-Mails **nur an Ihre eigene Adresse**. Die Adressen im Haus Lichtblick sind erfunden. Wo „an Thomas Weber“ oder „an Petra Schönfeld“ steht, tragen Sie Ihre eigene Adresse ein.';

(async () => {
  // Mailtexte
  await save('Block-02-Mailtexte.docx', 'Mailtexte Block 02 – Störungsmeldung Teeküche 2. OG', [
    TITLE('Mailtexte'),
    SUB('Block 02 – E-Mail-Grundlagen · Störungsmeldung Teeküche 2. OG'),
    P('Diese Texte brauchen Sie für das Übungsblatt Block 02. Markieren Sie einen Text, kopieren Sie ihn mit **Strg+C** und fügen Sie ihn in Outlook mit **Strg+V** ein. Oder tippen Sie ihn ab.'),
    ...ACHTUNG(NUR_EIGENE),
    H1('Wer ist wer?'),
    table([2300, 2700, 2570, 1500], [
      ['Person', 'Rolle', 'Adresse im Szenario', 'In der Übung'],
      ['Thomas Weber', 'Hausmeister', 'thomas.weber@haus-lichtblick.de', 'Ihre Adresse'],
      ['Petra Schönfeld', 'Hausverwaltung, Immobilien Fischer GmbH', 'p.schoenfeld@fischer-immo.de', 'Ihre Adresse'],
      ['Lena Ott', 'Mieterin, Praxis am Park (2. OG)', '–', '–'],
    ]),
    H1('Mailtext 1 – Störungsmeldung (Aufgabe 3)'),
    P('An: Thomas Weber · Cc: Petra Schönfeld'),
    ...MAIL('Störungsmeldung – Wasserhahn tropft, Teeküche 2. OG', [
      'Hallo Herr Weber,',
      'in der Teeküche im 2. OG tropft der Wasserhahn. Frau Ott von der Praxis am Park hat es heute Morgen gemeldet. Bitte sehen Sie sich das an und geben Sie mir kurz Bescheid, ob eine neue Dichtung reicht.',
      'Vielen Dank und viele Grüße',
      '[Ihr Name]',
      'Koordination Facility Management, Haus Lichtblick']),
    H1('Mailtext 2 – Antwort des Hausmeisters (Aufgabe 6)'),
    P('Mit „Antworten“ auf Mailtext 1 – der Betreff ist schon eingetragen.'),
    ...MAIL('(wird von Outlook eingetragen)', [
      'Hallo,',
      'danke für die Meldung. Ich sehe mir den Wasserhahn heute Nachmittag an. Eine neue Dichtung habe ich da.',
      'Viele Grüße',
      'Thomas Weber',
      'Hausmeister, Haus Lichtblick']),
    H1('Mailtext 3 – Kommentar beim Weiterleiten (Aufgabe 7)'),
    P('Mit „Weiterleiten“ an Petra Schönfeld – der Kommentar steht über dem weitergeleiteten Text.'),
    ...MAIL('(wird von Outlook eingetragen)', [
      'Hallo Frau Schönfeld,',
      'zur Information: In der Teeküche im 2. OG tropft der Wasserhahn. Herr Weber kümmert sich heute Nachmittag darum. Falls ein Installateur nötig wird, melde ich mich wieder.',
      'Viele Grüße',
      '[Ihr Name]',
      'Koordination Facility Management, Haus Lichtblick']),
  ], 'Übungsdatei Block 02 · Microsoft 365 im Facility Management · Namen, Firmen und Adressen sind erfunden');

  // Übungsblatt
  await save('Block-02-Uebungsblatt.docx', 'Übungsblatt Block 02 – E-Mail-Grundlagen', [
    TITLE('Übungsblatt Block 02'),
    SUB('E-Mail-Grundlagen'),
    P('**Sie brauchen:** einen PC mit dem neuen Outlook und Ihrem E-Mail-Konto, Word zum Öffnen der Übungsdatei und die Übungsdatei Block-02-Mailtexte.docx von der Seite zu Block 02.'),
    P(ROLLE),
    ...ACHTUNG(NUR_EIGENE),
    H1('Aufgabe 1 – Outlook erkunden'),
    ...STEPS(['Öffnen Sie das neue Outlook über das Startmenü.',
      'Suchen Sie auf dem Bildschirm die fünf Bereiche: App-Leiste, Ordnerbereich, Nachrichtenliste, Lesebereich, Menüband. Zeigen Sie mit der Maus auf jeden und sagen Sie seinen Namen.',
      'Klicken Sie im Ordnerbereich nacheinander auf „Posteingang“, „Entwürfe“ und „Gesendete Elemente“. Was ändert sich in der Nachrichtenliste?',
      'Klicken Sie wieder auf „Posteingang“.']),
    H1('Aufgabe 2 – Eine Test-E-Mail an sich selbst'),
    ...STEPS(['Klicken Sie auf der Registerkarte „Start“ auf **„Neue E-Mail“**.',
      'Tragen Sie unter **„An“** Ihre eigene Adresse ein.',
      'Betreff: Test – meine erste E-Mail',
      'Text: eine Anrede, ein Satz, ein Gruß mit Ihrem Namen.',
      'Klicken Sie auf **„Senden“**. Nach kurzer Zeit erscheint die E-Mail in Ihrem Posteingang.',
      'Sehen Sie im Ordner „Gesendete Elemente“ nach: Dort liegt sie auch.']),
    H1('Aufgabe 3 – Die Störungsmeldung'),
    ...STEPS(['Öffnen Sie in Word die Übungsdatei Block-02-Mailtexte.docx. Ordnen Sie Word und Outlook nebeneinander an (Block 01).',
      'Erstellen Sie in Outlook eine neue E-Mail.',
      '**An:** Ihre eigene Adresse – sie steht für Thomas Weber, den Hausmeister.',
      'Blenden Sie mit **„Cc“** die Zeile Cc ein und tragen Sie noch einmal Ihre eigene Adresse ein – sie steht für Petra Schönfeld von der Hausverwaltung.',
      'Übernehmen Sie Betreff und Text von **Mailtext 1**: in Word markieren, **Strg+C**, in Outlook ins Feld klicken, **Strg+V**. Oder tippen Sie ab.',
      'Ersetzen Sie „[Ihr Name]“ durch Ihren Namen und klicken Sie auf **„Senden“**.']),
    P('Kommt die E-Mail zweimal an? Das liegt daran, dass Ihre Adresse in „An“ und in „Cc“ steht. Löschen Sie eine davon.', { spacing: { before: 120, after: 120 } }),
    H1('Aufgabe 4 – Bessere Betreffzeilen'),
    P('Diese E-Mails haben einen schlechten Betreff. Schreiben Sie einen besseren: erst das Thema, dann Ort oder Einzelheit.'),
    table([600, 1700, 3470, 3300], [
      ['Nr.', 'Schlechter Betreff', 'Worum geht es?', 'Ihr Betreff'],
      ['1', 'Hallo', 'Der Heizkörper in Büro 305 bleibt kalt.', ''],
      ['2', 'Frage', 'Sie möchten bei Lift-Service Nord einen Termin für die Wartung der Aufzüge vereinbaren.', ''],
      ['3', '(kein Betreff)', 'Der Feuerlöscher im Flur des Erdgeschosses ist abgelaufen.', ''],
      ['4', 'Dringend!!!', 'Die Zugangskarten der Firma DesignWerk im 2. OG funktionieren nicht.', ''],
    ], { minHeight: 700 }),
    H1('Aufgabe 5 – An, Cc oder Bcc?'),
    P('Entscheiden Sie: Wer kommt in „An“, wer in „Cc“, wer in „Bcc“? Diese E-Mails senden Sie nicht ab.'),
    table([600, 4070, 1500, 1500, 1400], [
      ['Nr.', 'Situation', 'An', 'Cc', 'Bcc'],
      ['1', 'Elektro Schulze soll die flackernde Deckenlampe im Flur EG tauschen. Jan Müller aus der Technik soll Bescheid wissen.', '', '', ''],
      ['2', 'Sie informieren alle acht Mieter über die Wartung der Aufzüge. Niemand soll die Adressen der anderen sehen.', '', '', ''],
      ['3', 'Klara Nowak von Sauber & Rein soll den Konferenzraum 3.10 zusätzlich reinigen. Sarah Meyer von Consulting Plus hat darum gebeten und soll wissen, dass es erledigt wird.', '', '', ''],
      ['4', 'Petra Schönfeld bittet Sie um die Mieterliste. Nur sie braucht sie.', '', '', ''],
    ], { minHeight: 700 }),
    H1('Aufgabe 6 – Antworten'),
    P('Jetzt spielen Sie den Hausmeister und antworten auf die Störungsmeldung.'),
    ...STEPS(['Klicken Sie im Posteingang die Störungsmeldung aus Aufgabe 3 an.',
      'Klicken Sie oben im Lesebereich auf **„Antworten“**.',
      'Schauen Sie auf den Betreff: Womit beginnt er jetzt?',
      'Übernehmen Sie **Mailtext 2** aus der Übungsdatei über den alten Text und klicken Sie auf **„Senden“**.']),
    H1('Aufgabe 7 – Weiterleiten mit Kommentar'),
    P('Die Hausverwaltung soll erfahren, dass sich der Hausmeister kümmert.'),
    ...STEPS(['Klicken Sie im Posteingang die Antwort aus Aufgabe 6 an (Betreff mit „AW:“).',
      'Klicken Sie oben im Lesebereich auf **„Weiterleiten“**.',
      '**An:** Ihre eigene Adresse – sie steht für Petra Schönfeld.',
      'Übernehmen Sie **Mailtext 3** als Kommentar **über** den weitergeleiteten Text.',
      'Schauen Sie auf den Betreff: Womit beginnt er jetzt? Klicken Sie auf **„Senden“**.']),
    H1('Aufgabe 8 – Ordnung im Posteingang'),
    ...STEPS(['Klicken Sie mit der rechten Maustaste auf **„Posteingang“** und wählen Sie **„Neuen Unterordner erstellen“**. Name: Störungsmeldungen, dann **Enter**.',
      'Legen Sie genauso den Ordner Hausverwaltung an.',
      'Ziehen Sie die Störungsmeldung und die Antwort (AW:) mit der Maus in den Ordner „Störungsmeldungen“.',
      'Verschieben Sie die weitergeleitete E-Mail (WG:) in den Ordner „Hausverwaltung“ – diesmal mit Rechtsklick → **„Verschieben“**.',
      'Löschen Sie die Test-E-Mail aus Aufgabe 2: anklicken, **Entf** drücken. Sie liegt jetzt in „Gelöschte Elemente“.',
      'Klicken Sie auf die beiden neuen Ordner und prüfen Sie, ob alles am richtigen Platz ist.']),
    H1('Selbstcheck'),
    CHECK('Ich habe die fünf Bereiche des neuen Outlook gefunden.'),
    CHECK('Ich habe eine E-Mail an mich selbst geschrieben und gesendet.'),
    CHECK('Ich habe eine Störungsmeldung mit An und Cc und gutem Betreff gesendet.'),
    CHECK('Ich habe vier bessere Betreffzeilen geschrieben.'),
    CHECK('Ich weiß, wann ich An, Cc und Bcc verwende.'),
    CHECK('Ich habe auf eine E-Mail geantwortet und eine E-Mail mit Kommentar weitergeleitet.'),
    CHECK('Ich habe zwei Ordner angelegt und E-Mails hineingeschoben.'),
    H2('Notizen'),
    ...[1, 2, 3].map(() => new Paragraph({ spacing: { before: 300, after: 0 }, border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: LINE, space: 1 } }, children: [] })),
    new Paragraph({ children: [new PageBreak()] }),
    H1('Lösungen'),
    H2('Aufgabe 4'),
    P('Beispiele – andere Formulierungen sind genauso richtig, wenn Thema und Ort darin stehen:'),
    ...STEPS(['Störungsmeldung – Heizkörper Büro 305 bleibt kalt', 'Aufzugswartung – Bitte um Terminvorschlag',
      'Feuerlöscher Flur EG abgelaufen – Bitte um Austausch', 'Zugangskarten DesignWerk (2. OG) funktionieren nicht']),
    H2('Aufgabe 5'),
    ...STEPS(['An: Elektro Schulze · Cc: Jan Müller', 'An: Ihre eigene Adresse · Bcc: alle acht Mieter',
      'An: Klara Nowak · Cc: Sarah Meyer', 'An: Petra Schönfeld · kein Cc, kein Bcc']),
    H2('Aufgabe 6'),
    P('Der Betreff beginnt mit **AW:** (Antwort).'),
    H2('Aufgabe 7'),
    P('Der Betreff beginnt mit **WG:** (weitergeleitet), also „WG: AW: Störungsmeldung – …“.'),
  ], 'Übungsblatt Block 02 · Microsoft 365 im Facility Management');
})();
