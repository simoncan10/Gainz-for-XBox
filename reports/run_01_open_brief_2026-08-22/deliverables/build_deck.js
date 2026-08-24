const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.3 x 7.5
pres.author = "Stage 7";
pres.title = "Game Pass catalogue decision";

const DARK = "12161C";
const DARK2 = "1C222B";
const LIGHT = "FFFFFF";
const GREEN = "6BD425";
const RED = "E0523A";
const GREY = "8A94A0";
const INK = "12161C";

const H = "Cambria";
const B = "Calibri";

function darkSlide(titleText) {
  const s = pres.addSlide();
  s.background = { color: DARK };
  if (titleText) {
    s.addText(titleText, {
      x: 0.7, y: 0.45, w: 11.9, h: 0.95, fontFace: H, fontSize: 40, bold: true,
      color: LIGHT, align: "left", margin: 0,
    });
  }
  return s;
}
function lightSlide(titleText) {
  const s = pres.addSlide();
  s.background = { color: LIGHT };
  if (titleText) {
    s.addText(titleText, {
      x: 0.7, y: 0.45, w: 11.9, h: 0.95, fontFace: H, fontSize: 40, bold: true,
      color: INK, align: "left", margin: 0,
    });
  }
  return s;
}
function statCard(s, x, y, w, big, label, bigColor, cardColor) {
  s.addShape(pres.ShapeType.roundRect, {
    x, y, w, h: 1.85, fill: { color: cardColor }, rectRadius: 0.12,
    line: { color: cardColor },
  });
  s.addText(big, {
    x: x + 0.05, y: y + 0.22, w: w - 0.1, h: 0.85, fontFace: H, fontSize: 40, bold: true,
    color: bigColor, align: "center", margin: 0,
  });
  s.addText(label, {
    x: x + 0.2, y: y + 1.08, w: w - 0.4, h: 0.6, fontFace: B, fontSize: 13,
    color: "D6DCE3", align: "center", margin: 0,
  });
}

/* ---------------- Slide 1 — the recommendation as a sentence ---------------- */
{
  const s = pres.addSlide();
  s.background = { color: DARK };
  s.addText("Spend nothing today.", {
    x: 0.7, y: 1.15, w: 11.9, h: 1.15, fontFace: H, fontSize: 60, bold: true,
    color: LIGHT, margin: 0,
  });
  s.addText("Read the 500-deal experiment you already paid for — then a pre-committed rule decides.", {
    x: 0.7, y: 2.35, w: 11.3, h: 0.75, fontFace: B, fontSize: 21, color: GREEN, margin: 0,
  });
  statCard(s, 0.7, 3.5, 3.7, "$0", "Capital requested today", GREEN, DARK2);
  statCard(s, 4.8, 3.5, 3.7, "6 weeks", "Internal audit, no new data collection", LIGHT, DARK2);
  statCard(s, 8.9, 3.5, 3.7, "0.025pp", "Churn per title-year that makes it a yes", LIGHT, DARK2);
  s.addText("Microsoft / Xbox board  ·  22 August 2026", {
    x: 0.7, y: 5.75, w: 8, h: 0.35, fontFace: B, fontSize: 12, color: GREY, margin: 0,
  });
  s.addNotes("Open flat and slow. The hook is the pause after 'nobody has ever measured'.");
}

/* ---------------- Slide 2 — hit concentration ---------------- */
{
  const s = lightSlide("Breadth is worthless");
  s.addText("Share of a genre's estimated audience held by its top 10% of titles", {
    x: 0.7, y: 1.35, w: 11.9, h: 0.4, fontFace: B, fontSize: 17, color: GREY, margin: 0,
  });
  s.addChart(pres.ChartType.bar, [{
    name: "Top-decile share",
    labels: ["Action", "RPG", "Strategy", "Indie", "Sports"],
    values: [87, 85, 80, 78, 78],
  }], {
    x: 0.6, y: 1.95, w: 8.3, h: 4.0,
    barDir: "col",
    chartColors: [INK, INK, INK, INK, INK],
    showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '0"%"',
    dataLabelColor: INK, dataLabelFontSize: 18, dataLabelFontBold: true, dataLabelFontFace: B,
    catAxisLabelColor: INK, catAxisLabelFontSize: 16, catAxisLabelFontFace: B,
    valAxisLabelColor: GREY, valAxisLabelFontSize: 13, valAxisMaxVal: 100, valAxisMinVal: 0,
    valGridLine: { color: "E4E8EC", size: 1 },
    catGridLine: { style: "none" },
    barGapWidthPct: 55,
  });
  s.addShape(pres.ShapeType.roundRect, {
    x: 9.2, y: 2.1, w: 3.4, h: 2.3, fill: { color: "F1F4F7" }, rectRadius: 0.12,
    line: { color: "F1F4F7" },
  });
  s.addText("Buying a hundred games buys you ninety bad ones.", {
    x: 9.45, y: 2.35, w: 2.9, h: 1.8, fontFace: H, fontSize: 21, bold: true, color: INK,
    margin: 0, valign: "middle",
  });
  s.addText("SteamSpy owner buckets, n = 4,732–82,552 per genre. Read this as a shape, not a measured share — 83% of the catalogue sits in one bottom bucket. Source: F1, 03_findings.md.", {
    x: 9.2, y: 4.6, w: 3.4, h: 1.5, fontFace: B, fontSize: 10, color: GREY, margin: 0,
  });
  s.addNotes("Concentration is the reason the tranche is 20 titles, not 200. It is also conservative: delisted failures are absent from the snapshot.");
}

/* ---------------- Slide 3 — price vs catalogue ---------------- */
{
  const s = darkSlide("You already chose price. Nobody measured it.");
  s.addText("Money aimed at churn: the price lever, per year, against the catalogue ask", {
    x: 0.7, y: 1.35, w: 11.9, h: 0.4, fontFace: B, fontSize: 17, color: GREY, margin: 0,
  });
  s.addChart(pres.ChartType.bar, [{
    name: "$M per year",
    labels: ["April 2026 Ultimate\nprice rollback", "Catalogue licensing\ntranche (one-off)"],
    values: [840, 30],
  }], {
    x: 0.6, y: 1.95, w: 8.3, h: 4.05,
    barDir: "col",
    chartColors: [GREEN, GREY],
    showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '"$"#,##0"M"',
    dataLabelColor: LIGHT, dataLabelFontSize: 20, dataLabelFontBold: true, dataLabelFontFace: B,
    catAxisLabelColor: LIGHT, catAxisLabelFontSize: 15, catAxisLabelFontFace: B,
    valAxisLabelColor: GREY, valAxisLabelFontSize: 13, valAxisMinVal: 0, valAxisMaxVal: 1000,
    valGridLine: { color: "2A313B", size: 1 },
    catGridLine: { style: "none" },
    barGapWidthPct: 90,
    plotArea: { fill: { color: DARK } },
  });
  s.addShape(pres.ShapeType.roundRect, {
    x: 9.2, y: 2.1, w: 3.4, h: 1.75, fill: { color: DARK2 }, rectRadius: 0.12, line: { color: DARK2 },
  });
  s.addText("28×", {
    x: 9.2, y: 2.25, w: 3.4, h: 0.85, fontFace: H, fontSize: 52, bold: true, color: GREEN,
    align: "center", margin: 0,
  });
  s.addText("the size of the catalogue ask", {
    x: 9.35, y: 3.15, w: 3.1, h: 0.5, fontFace: B, fontSize: 13, color: "D6DCE3",
    align: "center", margin: 0,
  });
  s.addText("$29.99 → $22.99 in April 2026, on an estimated 10M Ultimate subscribers. Verified range across 5–15M subscribers: $420M–$1.26B a year, i.e. 14× to 42×. Cost per retained subscriber: unmeasured.", {
    x: 9.2, y: 4.05, w: 3.4, h: 1.7, fontFace: B, fontSize: 10, color: GREY, margin: 0,
  });
  s.addNotes("500+ Game Pass deals already run, $50K to $50M+. Expiry timing was set years ago, so it is closer to exogenous than additions are.");
}

/* ---------------- Slide 4 — the rule ---------------- */
{
  const s = lightSlide("The rule, pre-committed");
  s.addText("Break-even = 0.025pp of annual churn per title-year", {
    x: 0.7, y: 1.35, w: 11.9, h: 0.45, fontFace: B, fontSize: 19, bold: true, color: GREEN, margin: 0,
  });
  s.addChart(pres.ChartType.bar, [{
    name: "$K per title-year",
    labels: ["Cost of one licence\n$1.5M over 24 months", "If measured effect is\n0.01pp per title", "If measured effect is\n0.04pp per title"],
    values: [750, 302, 1210],
  }], {
    x: 0.6, y: 1.95, w: 8.3, h: 4.05,
    barDir: "col",
    chartColors: [GREY, RED, GREEN],
    showLegend: false,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: '"$"#,##0"K"',
    dataLabelColor: INK, dataLabelFontSize: 18, dataLabelFontBold: true, dataLabelFontFace: B,
    catAxisLabelColor: INK, catAxisLabelFontSize: 14, catAxisLabelFontFace: B,
    valAxisLabelColor: GREY, valAxisLabelFontSize: 13, valAxisMinVal: 0, valAxisMaxVal: 1400,
    valGridLine: { color: "E4E8EC", size: 1 },
    catGridLine: { style: "none" },
    barGapWidthPct: 65,
  });
  s.addShape(pres.ShapeType.roundRect, {
    x: 9.2, y: 1.95, w: 3.4, h: 3.35, fill: { color: "F1F4F7" }, rectRadius: 0.12, line: { color: "F1F4F7" },
  });
  s.addText([
    { text: "1pp of churn\n", options: { fontSize: 15, bold: true, color: INK, breakLine: true } },
    { text: "300,000 subs × $168 × 60% margin\n= $30.2M a year\n\n", options: { fontSize: 13, color: "44505E", breakLine: true } },
    { text: "One licence\n", options: { fontSize: 15, bold: true, color: INK, breakLine: true } },
    { text: "$1.5M ÷ 24 months = $750K per title-year\n\n", options: { fontSize: 13, color: "44505E", breakLine: true } },
    { text: "$750K ÷ $30.2M = 0.025pp", options: { fontSize: 14, bold: true, color: GREEN } },
  ], { x: 9.45, y: 2.12, w: 2.95, h: 2.7, fontFace: B, margin: 0, valign: "top", lineSpacingMultiple: 1.02 });
  s.addText("Above the line, licensing pays — scale toward the pool ceiling (~650 screened titles). Below it, it does not pay at $1.5M. Subscriber, ARPU and margin inputs are estimates and are replaced by measured internal values the moment the audit runs.", {
    x: 9.2, y: 5.5, w: 3.4, h: 1.4, fontFace: B, fontSize: 10, color: GREY, margin: 0,
  });
  s.addNotes("Worked shapes: 0.5pp across a 50-title cohort-year fails by 2.5x. 2.0pp across the same cohort clears comfortably.");
}

/* ---------------- Slide 5 — the ask ---------------- */
{
  const s = darkSlide("The ask");
  s.addText("Approve six weeks, no capital, and the rule.", {
    x: 0.7, y: 1.38, w: 11.9, h: 0.5, fontFace: B, fontSize: 21, color: GREEN, margin: 0,
  });
  const branches = [
    ["A", "Effect above 0.025pp", "Skip the experiment. Size a standing programme off the measured effect.", GREEN],
    ["B", "No effect identifiable", "Buy the $30M, 20-title instrumented tranche — with randomisation written in before signature.", "D6DCE3"],
    ["C", "Effect negative or below", "Drop the catalogue argument. Redirect the renewal book to cost reduction.", RED],
  ];
  branches.forEach((br, i) => {
    const x = 0.7 + i * 4.1;
    s.addShape(pres.ShapeType.roundRect, {
      x, y: 2.15, w: 3.7, h: 2.75, fill: { color: DARK2 }, rectRadius: 0.12, line: { color: DARK2 },
    });
    s.addShape(pres.ShapeType.ellipse, {
      x: x + 0.28, y: 2.42, w: 0.62, h: 0.62, fill: { color: br[3] }, line: { color: br[3] },
    });
    s.addText(br[0], {
      x: x + 0.28, y: 2.48, w: 0.62, h: 0.5, fontFace: H, fontSize: 22, bold: true,
      color: DARK, align: "center", margin: 0,
    });
    s.addText(br[1], {
      x: x + 1.05, y: 2.46, w: 2.45, h: 0.6, fontFace: H, fontSize: 17, bold: true,
      color: LIGHT, margin: 0,
    });
    s.addText(br[2], {
      x: x + 0.28, y: 3.25, w: 3.15, h: 1.4, fontFace: B, fontSize: 13, color: "AEB8C4", margin: 0,
    });
  });
  s.addText("Caveat I am naming myself: this is Steam PC data. Console ARPPU is ~48% higher and the genre mix differs. No engagement or playtime data exists in any source available here — which is exactly why the deciding number has to come from inside Microsoft.", {
    x: 0.7, y: 5.2, w: 11.9, h: 0.9, fontFace: B, fontSize: 12, color: GREY, margin: 0,
  });
  s.addNotes("Final line: 'Then hold me to it.' Stop. Look up. Say nothing else.");
}

pres.writeFile({ fileName: "/home/claude/run_2026-08-22/deliverables/pitch_deck.pptx" })
  .then(f => console.log("wrote", f));
