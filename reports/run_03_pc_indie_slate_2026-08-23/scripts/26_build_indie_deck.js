const pptxgen = require("pptxgenjs");

const BG = "160F2E";        // deep violet-black
const PANEL = "271B4D";     // raised panel
const PANEL2 = "1F1540";    // recessed panel
const AMBER = "F5A623";     // accent — the idea
const MINT = "41D6A8";      // accent — supporting
const ROSE = "E2607A";      // accent — the failure / the cost
const WHITE = "FFFFFF";
const MUTED = "B0A4D6";

const HFONT = "Cambria";
const BFONT = "Calibri";

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";           // 13.3 x 7.5
pres.author = "Game Pass portfolio analysis";
pres.title = "Buying breadth, not blockbusters";

const W = 13.3, H = 7.5;

function bg(slide) { slide.background = { color: BG }; }

function title(slide, text, y) {
  slide.addText(text, {
    x: 0.7, y: y === undefined ? 0.5 : y, w: W - 1.4, h: 0.9,
    fontFace: HFONT, fontSize: 38, bold: true, color: WHITE, align: "left", margin: 0
  });
}

function kicker(slide, text, y) {
  slide.addText(text, {
    x: 0.7, y: y, w: W - 1.4, h: 0.35,
    fontFace: BFONT, fontSize: 13, bold: true, color: AMBER, charSpacing: 2, margin: 0
  });
}

function card(slide, opts) {
  slide.addShape(pres.ShapeType.roundRect, {
    x: opts.x, y: opts.y, w: opts.w, h: opts.h,
    fill: { color: opts.fill || PANEL }, line: { color: opts.line || PANEL, width: 1 },
    rectRadius: 0.12
  });
}

/* ─────────────────────────── SLIDE 1 — the question ─────────────────────────── */
{
  const s = pres.addSlide();
  bg(s);

  s.addText("Buying breadth,\nnot blockbusters", {
    x: 0.8, y: 1.55, w: 7.6, h: 2.4,
    fontFace: HFONT, fontSize: 54, bold: true, color: WHITE, lineSpacing: 58, margin: 0
  });

  s.addText("An indie slate for PC Game Pass", {
    x: 0.8, y: 4.05, w: 7.6, h: 0.5,
    fontFace: BFONT, fontSize: 22, color: AMBER, margin: 0
  });

  s.addText("Which games should the service buy — and why should you\ntrust the filter that chose them?", {
    x: 0.8, y: 4.85, w: 7.8, h: 1.0,
    fontFace: BFONT, fontSize: 17, color: MUTED, lineSpacing: 26, margin: 0
  });

  // 21 slot tiles: 4 clean adds (amber), 5 restarts (mint), 12 breadth (muted violet)
  const cols = 3;
  const tw = 0.72, th = 0.5, gx = 0.22, gy = 0.18;
  const ox = 9.55, oy = 1.6;
  for (let i = 0; i < 21; i++) {
    const c = i % cols, r = Math.floor(i / cols);
    const col = i < 4 ? AMBER : (i < 9 ? MINT : "3A2A6E");
    s.addShape(pres.ShapeType.roundRect, {
      x: ox + c * (tw + gx), y: oy + r * (th + gy), w: tw, h: th,
      fill: { color: col }, line: { color: col, width: 1 }, rectRadius: 0.08
    });
  }
  s.addText("21 catalogue slots", {
    x: 9.55, y: 6.45, w: 2.6, h: 0.3,
    fontFace: BFONT, fontSize: 12, color: MUTED, align: "center", margin: 0
  });

  s.addNotes("The question, not the method. Do not open with who we are or how we did it. The tiles on the right are the whole recommendation: 21 slots, four clean adds, five restarts, twelve breadth titles.");
}

/* ─────────────────────────── SLIDE 2 — the funnel ─────────────────────────── */
{
  const s = pres.addSlide();
  bg(s);
  kicker(s, "THE FUNNEL", 0.55);
  title(s, "From the whole of Steam to twenty-one names", 0.95);

  const steps = [
    { n: "122,191", label: "non-demo titles on Steam", w: 11.9, col: "3A2A6E", tc: WHITE },
    { n: "573", label: "eligible — paid, reviewed, well-liked, not already everywhere, genuinely indie", w: 10.2, col: "4A3488", tc: WHITE },
    { n: "201", label: "qualifying on the composite", w: 8.5, col: "6247A8", tc: WHITE },
    { n: "25", label: "checked by hand against Game Pass", w: 7.0, col: MINT, tc: "10281F" },
    { n: "21", label: "picks", w: 5.6, col: AMBER, tc: "3A2400" }
  ];

  let y = 2.1;
  steps.forEach((st) => {
    const x = 0.7;
    s.addShape(pres.ShapeType.roundRect, {
      x: x, y: y, w: st.w, h: 0.78,
      fill: { color: st.col }, line: { color: st.col, width: 1 }, rectRadius: 0.1
    });
    s.addText(st.n, {
      x: x + 0.25, y: y, w: 2.0, h: 0.78,
      fontFace: HFONT, fontSize: 26, bold: true, color: st.tc, valign: "middle", margin: 0
    });
    s.addText(st.label, {
      x: x + 2.25, y: y, w: st.w - 2.4, h: 0.78,
      fontFace: BFONT, fontSize: 14, color: st.tc, valign: "middle", margin: 0
    });
    y += 0.94;
  });

  s.addText("Every step is a filter we can explain. Two of them we had to rebuild first.", {
    x: 0.7, y: 6.85, w: 11.6, h: 0.4,
    fontFace: BFONT, fontSize: 16, italic: true, color: AMBER, margin: 0
  });

  s.addNotes("Say the numbers as a rhythm, four descending beats. The point of the slide is that the funnel is narrow and every narrowing is defensible. Owners, price and review counts behind these filters are all Steam data — estimates, not sales.");
}

/* ─────────────────── SLIDE 3 — why these filters, part one ─────────────────── */
{
  const s = pres.addSlide();
  bg(s);
  kicker(s, "WHY THESE FILTERS · 1 OF 2", 0.55);
  title(s, "The first model put shovelware at the top", 0.95);

  // Left: the symptom
  card(s, { x: 0.7, y: 2.1, w: 4.5, h: 4.7, fill: PANEL2, line: ROSE });
  s.addText("What it ranked #1", {
    x: 1.0, y: 2.35, w: 3.9, h: 0.4, fontFace: BFONT, fontSize: 14, bold: true, color: ROSE, margin: 0
  });
  s.addText([
    { text: "The Confession", options: { bullet: true, breakLine: true } },
    { text: "The Horrorscope", options: { bullet: true, breakLine: true } },
    { text: "BBQ Simulator", options: { bullet: true } }
  ], {
    x: 1.0, y: 2.9, w: 3.9, h: 1.5, fontFace: BFONT, fontSize: 19, color: WHITE,
    paraSpaceAfter: 8, margin: 0
  });
  s.addText("Not a ranking wobble. The model working exactly as specified.", {
    x: 1.0, y: 5.65, w: 3.9, h: 0.9, fontFace: BFONT, fontSize: 14, italic: true, color: MUTED, margin: 0
  });

  // Right: two causes
  const causes = [
    {
      h: "Recognition cancelled itself out",
      b: "Two pillars pulled in opposite directions and were averaged. Their contribution became near-constant, so neither moved the ranking. The brief's central idea was not encoded — it was annihilated."
    },
    {
      h: "“Cheap” was a budget filter",
      b: "Retail price tracks production budget and press coverage. Ranking on low price ranks on the absence of both. The pillar was a quality penalty wearing a cost label."
    }
  ];
  let cy = 2.1;
  causes.forEach((c) => {
    card(s, { x: 5.5, y: cy, w: 7.1, h: 1.65 });
    s.addText(c.h, { x: 5.85, y: cy + 0.18, w: 6.4, h: 0.4, fontFace: BFONT, fontSize: 18, bold: true, color: AMBER, margin: 0 });
    s.addText(c.b, { x: 5.85, y: cy + 0.62, w: 6.45, h: 0.9, fontFace: BFONT, fontSize: 13.5, color: MUTED, lineSpacing: 17, margin: 0 });
    cy += 1.85;
  });

  card(s, { x: 5.5, y: 5.8, w: 7.1, h: 1.0, fill: "0E2A22", line: MINT });
  s.addText("Rebuilt: one recognition term, one headroom ratio — and price removed from the score entirely.", {
    x: 5.85, y: 5.8, w: 6.45, h: 1.0, fontFace: BFONT, fontSize: 15, bold: true, color: MINT, valign: "middle", lineSpacing: 19, margin: 0
  });

  s.addNotes("A filter you can explain the failure of is more trustworthy than one presented as obvious. Price now does no ranking work anywhere in the recommendation; it is carried as an annotation only.");
}

/* ─────────────────── SLIDE 4 — why these filters, part two ─────────────────── */
{
  const s = pres.addSlide();
  bg(s);
  kicker(s, "WHY THESE FILTERS · 2 OF 2", 0.55);
  title(s, "Then the indie test failed at both ends", 0.95);

  s.addText("The rule was: developer must equal publisher.", {
    x: 0.7, y: 1.9, w: 11.9, h: 0.4, fontFace: BFONT, fontSize: 17, italic: true, color: MUTED, margin: 0
  });

  // Wrongly out
  card(s, { x: 0.7, y: 2.5, w: 5.85, h: 2.9, fill: PANEL2, line: ROSE });
  s.addText("Thrown out as “not indie”", {
    x: 1.0, y: 2.72, w: 5.2, h: 0.4, fontFace: BFONT, fontSize: 15, bold: true, color: ROSE, margin: 0
  });
  s.addText([
    { text: "Papers, Please", options: { bullet: true, breakLine: true } },
    { text: "Return of the Obra Dinn", options: { bullet: true, breakLine: true } },
    { text: "What Remains of Edith Finch", options: { bullet: true, breakLine: true } },
    { text: "Journey", options: { bullet: true } }
  ], { x: 1.0, y: 3.22, w: 5.2, h: 1.5, fontFace: BFONT, fontSize: 17, color: WHITE, paraSpaceAfter: 6, margin: 0 });
  s.addText("Lucas Pope's own label is spelled “3909”. A name mismatch, not a signal.", {
    x: 1.0, y: 4.72, w: 5.2, h: 0.6, fontFace: BFONT, fontSize: 13, italic: true, color: MUTED, lineSpacing: 17, margin: 0
  });

  // Wrongly in
  card(s, { x: 6.75, y: 2.5, w: 5.85, h: 2.9, fill: PANEL2, line: ROSE });
  s.addText("Waved in as “indie”", {
    x: 7.05, y: 2.72, w: 5.2, h: 0.4, fontFace: BFONT, fontSize: 15, bold: true, color: ROSE, margin: 0
  });
  s.addText([
    { text: "An asset-flip mill with 181 titles", options: { bullet: true, breakLine: true } },
    { text: "Another with 163", options: { bullet: true, breakLine: true } },
    { text: "Another with 130", options: { bullet: true, breakLine: true } },
    { text: "…and two more like them", options: { bullet: true } }
  ], { x: 7.05, y: 3.22, w: 5.2, h: 1.5, fontFace: BFONT, fontSize: 17, color: WHITE, paraSpaceAfter: 6, margin: 0 });
  s.addText("Mills self-publish. So the rule read them as independent studios.", {
    x: 7.05, y: 4.72, w: 5.2, h: 0.6, fontFace: BFONT, fontSize: 13, italic: true, color: MUTED, lineSpacing: 17, margin: 0
  });

  card(s, { x: 0.7, y: 5.7, w: 11.9, h: 1.1, fill: "0E2A22", line: MINT });
  s.addText("Rebuilt: indie means a small developer, not a missing publisher — then hand-checked, name by name, at both ends.", {
    x: 1.05, y: 5.7, w: 11.2, h: 1.1, fontFace: BFONT, fontSize: 16, bold: true, color: MINT, valign: "middle", lineSpacing: 20, margin: 0
  });

  s.addNotes("This is the answer to the hostile question 'you excluded Edith Finch from an indie portfolio?' — we did, we caught it, and here is the rebuilt rule. Eight of the wrongly-excluded canonical titles now sit inside the top twenty.");
}

/* ─────────────────── SLIDE 5 — the investment idea ─────────────────── */
{
  const s = pres.addSlide();
  bg(s);
  kicker(s, "THE INVESTMENT IDEA", 0.55);
  title(s, "A subscription buys slots, not owners", 0.95);

  // Left — the losing yardstick
  card(s, { x: 0.9, y: 2.35, w: 5.4, h: 3.3, fill: PANEL2, line: "4A3060" });
  s.addText("Per owner reached", {
    x: 1.25, y: 2.6, w: 4.7, h: 0.4, fontFace: BFONT, fontSize: 17, bold: true, color: MUTED, margin: 0
  });
  s.addText("1.50×", {
    x: 1.25, y: 3.05, w: 4.7, h: 1.5, fontFace: HFONT, fontSize: 90, bold: true, color: ROSE, margin: 0
  });
  s.addText("more expensive.\nIndie loses this one, clearly.", {
    x: 1.25, y: 4.6, w: 4.7, h: 0.9, fontFace: BFONT, fontSize: 17, color: WHITE, lineSpacing: 24, margin: 0
  });

  // Right — the winning yardstick
  card(s, { x: 7.0, y: 2.35, w: 5.4, h: 3.3, fill: "3A2400", line: AMBER });
  s.addText("Per catalogue slot", {
    x: 7.35, y: 2.6, w: 4.7, h: 0.4, fontFace: BFONT, fontSize: 17, bold: true, color: AMBER, margin: 0
  });
  s.addText("1.53×", {
    x: 7.35, y: 3.05, w: 4.7, h: 1.5, fontFace: HFONT, fontSize: 90, bold: true, color: AMBER, margin: 0
  });
  s.addText("more breadth per dollar.\nThis is what a subscription buys.", {
    x: 7.35, y: 4.6, w: 4.8, h: 0.9, fontFace: BFONT, fontSize: 17, color: WHITE, lineSpacing: 24, margin: 0
  });

  s.addText("Both are true. Only one of them is the question a subscription asks.", {
    x: 0.9, y: 6.0, w: 11.5, h: 0.5, fontFace: BFONT, fontSize: 20, italic: true, color: WHITE, align: "center", margin: 0
  });
  s.addText("Measured on Steam retail price, identically on both groups. A comparison, not a cost.", {
    x: 0.9, y: 6.6, w: 11.5, h: 0.4, fontFace: BFONT, fontSize: 12, color: MUTED, align: "center", margin: 0
  });

  s.addNotes("The yardstick flip, and nothing else on this slide. Concede the left-hand number out loud before anyone reaches it. Do NOT say engagement — there is no playtime data in this dataset and no engagement claim is made anywhere in this analysis.");
}

/* ─────────────────── SLIDE 6 — the games ─────────────────── */
{
  const s = pres.addSlide();
  bg(s);
  kicker(s, "THE SLATE", 0.55);
  title(s, "Twenty-one titles, three jobs", 0.95);

  const tiers = [
    {
      n: "4", col: AMBER, tc: "3A2400", head: "Clean adds",
      role: "Nothing to explain. No prior run, no publisher mid-crisis.",
      names: "A Hat in Time\nReturn of the Obra Dinn\nRogue Legacy\nThe Stanley Parable: Ultra Deluxe"
    },
    {
      n: "5", col: MINT, tc: "10281F", head: "Precedent restarts",
      role: "Licences Microsoft has already signed once. Cheapest to execute.",
      names: "VA-11 Hall-A\nLibrary Of Ruina\nUnpacking\nWhat Remains of Edith Finch\nJourney"
    },
    {
      n: "12", col: "8A6BE0", tc: "FFFFFF", head: "Breadth block",
      role: "This tier is the investment case. Breadth is title count at a quality bar.",
      names: "ENDER LILIES · SANABI\nChants of Sennaar · Firework\nWandering Sword · Potion Craft\nCARRION · A Short Hike\nPath Of Wuxia · The Hungry Lamb\nSanfu · Temtem"
    }
  ];

  let x = 0.7;
  tiers.forEach((t) => {
    card(s, { x: x, y: 2.0, w: 3.95, h: 4.55, fill: PANEL2, line: PANEL });
    s.addShape(pres.ShapeType.roundRect, {
      x: x + 0.3, y: 2.28, w: 0.85, h: 0.7,
      fill: { color: t.col }, line: { color: t.col, width: 1 }, rectRadius: 0.1
    });
    s.addText(t.n, { x: x + 0.3, y: 2.28, w: 0.85, h: 0.7, fontFace: HFONT, fontSize: 26, bold: true, color: t.tc, align: "center", valign: "middle", margin: 0 });
    s.addText(t.head, { x: x + 1.3, y: 2.28, w: 2.5, h: 0.7, fontFace: HFONT, fontSize: 19, bold: true, color: WHITE, valign: "middle", margin: 0 });
    s.addText(t.role, { x: x + 0.3, y: 3.1, w: 3.35, h: 0.9, fontFace: BFONT, fontSize: 13.5, color: MUTED, lineSpacing: 17, margin: 0 });
    s.addText(t.names, { x: x + 0.3, y: 3.95, w: 3.4, h: 2.4, fontFace: BFONT, fontSize: 13.5, color: WHITE, lineSpacing: 21, margin: 0 });
    x += 4.2;
  });

  s.addText("Recognition and price rise together: these 21 keep 40% of the pool's breadth advantage, not all of it.", {
    x: 0.7, y: 6.85, w: 11.9, h: 0.4, fontFace: BFONT, fontSize: 15, italic: true, color: AMBER, margin: 0
  });

  s.addNotes("Tier 1 leads because it is the only tier with nothing to explain. Tier 2 is ordered stable counterparty first — Annapurna and Humble both lost their entire staff in 2024. Tier 3 is the investment case. Temtem is ranked last on purpose and is the designated first cut.");
}

/* ─────────────────── SLIDE 7 — the ask ─────────────────── */
{
  const s = pres.addSlide();
  bg(s);
  kicker(s, "THE ASK", 0.55);
  title(s, "What we want approved today", 0.95);

  const asks = [
    { n: "1", t: "Open negotiations", b: "The four clean adds, and the two restarts with a stable counterparty." },
    { n: "2", t: "Extend the screen", b: "Availability research from rank 25 to rank 60 — 35 titles, and where the genre gap closes." },
    { n: "3", t: "Accept the first cut", b: "Temtem goes first if the budget bites. Dropping it alone improves breadth per dollar." }
  ];

  let y = 2.1;
  asks.forEach((a) => {
    card(s, { x: 0.7, y: y, w: 11.9, h: 1.25 });
    s.addShape(pres.ShapeType.roundRect, {
      x: 1.0, y: y + 0.28, w: 0.7, h: 0.7,
      fill: { color: AMBER }, line: { color: AMBER, width: 1 }, rectRadius: 0.1
    });
    s.addText(a.n, { x: 1.0, y: y + 0.28, w: 0.7, h: 0.7, fontFace: HFONT, fontSize: 24, bold: true, color: "3A2400", align: "center", valign: "middle", margin: 0 });
    s.addText(a.t, { x: 1.95, y: y + 0.2, w: 3.4, h: 0.45, fontFace: HFONT, fontSize: 21, bold: true, color: WHITE, margin: 0 });
    s.addText(a.b, { x: 1.95, y: y + 0.68, w: 10.3, h: 0.45, fontFace: BFONT, fontSize: 14.5, color: MUTED, margin: 0 });
    y += 1.45;
  });

  card(s, { x: 0.7, y: 6.45, w: 11.9, h: 0.75, fill: PANEL2, line: PANEL2 });
  s.addText("No engagement claim is made: this data has no playtime at all. Owners are bucketed estimates, not sales. Retail price is not licensing cost — no indie-tier Game Pass price exists in the public record.", {
    x: 1.0, y: 6.45, w: 11.3, h: 0.75, fontFace: BFONT, fontSize: 12, color: MUTED, valign: "middle", lineSpacing: 15, margin: 0
  });

  s.addNotes("State the ask, then stop talking. The honesty footer is the answer to three of the four most likely questions and should be read aloud only if challenged.");
}

pres.writeFile({ fileName: "/home/claude/run_portfolio/deliverables/indie_deck.pptx" })
  .then(f => console.log("wrote", f));
