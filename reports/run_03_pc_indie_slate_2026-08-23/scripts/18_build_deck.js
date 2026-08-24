const pptxgen = require('pptxgenjs');
const p = new pptxgen();
p.layout = 'LAYOUT_WIDE';           // 13.3 x 7.5
const W = 13.3, H = 7.5;

const DARK='10281A', GREEN='2C5F2D', MOSS='97BC62', CREAM='F5F5F5', INK='1A1A1A', MUTE='6B7B6E';
const HF='Cambria', BF='Calibri';

const dark = () => { const s=p.addSlide(); s.background={color:DARK}; return s; };
const light= () => { const s=p.addSlide(); s.background={color:'FFFFFF'}; return s; };

const chartQuiet = {
  showLegend:false, chartColors:[GREEN], valAxisLabelColor:MUTE, catAxisLabelColor:INK,
  valGridLine:{color:'E4E9E4', size:1}, catGridLine:{style:'none'},
  valAxisLabelFontFace:BF, catAxisLabelFontFace:BF,
};

/* ---------- 1. TITLE ---------- */
{
  const s = dark();
  s.addText('Seventeen names.', {x:0.8,y:0.75,w:11.7,h:1.0,fontFace:HF,fontSize:54,bold:true,color:CREAM});
  s.addText('17 back-catalogue titles to license into Game Pass, plus a 7-title watchlist that is explicitly not a buy.',
    {x:0.8,y:1.8,w:11.0,h:0.5,fontFace:BF,fontSize:17,color:MOSS});

  const lead = [
    ['A Hat in Time','50,390 reviews · Metacritic 79'],
    ['Return of the Obra Dinn','26,518 reviews · Metacritic 89'],
    ['Baba Is You','20,757 reviews · Metacritic 87'],
  ];
  lead.forEach((t,i)=>{
    const x = 0.8 + i*3.95;
    s.addShape(p.ShapeType.roundRect,{x,y:2.75,w:3.6,h:1.95,fill:{color:'1B4526'},rectRadius:0.1,
      shadow:{type:'outer',blur:12,offset:3,angle:90,color:'000000',opacity:0.35}});
    s.addText(String(i+1),{x:x+0.25,y:2.9,w:0.6,h:0.4,fontFace:HF,fontSize:16,bold:true,color:MOSS,margin:0});
    s.addText(t[0],{x:x+0.25,y:3.3,w:3.1,h:0.8,fontFace:HF,fontSize:20,bold:true,color:CREAM,margin:0});
    s.addText(t[1],{x:x+0.25,y:4.15,w:3.1,h:0.4,fontFace:BF,fontSize:12,color:MOSS,margin:0});
  });
  s.addText('The three that lead: never on Game Pass · Xbox version confirmed · no blocker.',
    {x:0.8,y:5.0,w:11.7,h:0.4,fontFace:BF,fontSize:15,italic:true,color:CREAM});
  s.addText('Microsoft / Xbox board · 22 August 2026 · every title sourced from the Steam snapshot, none from the web',
    {x:0.8,y:6.6,w:11.7,h:0.35,fontFace:BF,fontSize:11,color:MUTE});
  s.addNotes('Hook. Land 122,191 and 17 as a pair. Name the three games slowly, one beat each. Do not explain them.');
}

/* ---------- 2. FUNNEL ---------- */
{
  const s = light();
  s.addText('122,191 games in. 17 out.',{x:0.8,y:0.55,w:11.7,h:0.8,fontFace:HF,fontSize:40,bold:true,color:INK});
  s.addText('Screened by stated thresholds, not by taste. Every stage is checkable.',
    {x:0.8,y:1.35,w:11.7,h:0.4,fontFace:BF,fontSize:16,color:MUTE});

  s.addChart(p.ChartType.bar, [{
    name:'Titles remaining',
    labels:['Non-demo\ngames','Eligible\n(review floor 4,000)','Qualifying\n(composite ≥ 0.60)','Availability\nscreened','Picks'],
    values:[122191,802,275,30,17]
  }], {
    x:0.7,y:1.95,w:8.3,h:4.5, barDir:'col', ...chartQuiet,
    showValue:true, dataLabelPosition:'outEnd', dataLabelFontFace:BF, dataLabelFontSize:11,
    dataLabelColor:INK, dataLabelFormatCode:'#,##0',
    catAxisLabelFontSize:10, valAxisLabelFontSize:9, barGapWidthPct:55,
    valAxisMaxVal:135000, valAxisMinVal:0, valAxisMajorUnit:20000,
  });

  s.addShape(p.ShapeType.roundRect,{x:9.3,y:2.1,w:3.3,h:4.2,fill:{color:'EEF3EE'},rectRadius:0.1});
  s.addText([
    {text:'0.014%\n',options:{fontFace:HF,fontSize:34,bold:true,color:GREEN,breakLine:true}},
    {text:'of the catalogue survives the funnel. The bar is stated up front — a review floor of 4,000, a composite of 0.60, and an external Game Pass and Xbox-version check on every candidate that got that far.',
      options:{fontFace:BF,fontSize:13,color:INK}},
  ],{x:9.55,y:2.35,w:2.8,h:3.7,valign:'top'});

  s.addText('Sources: 02_cleaning_report.md · 16_scoring_v3.md · 13_availability.md (screened Aug 2026)',
    {x:0.8,y:6.75,w:11.7,h:0.3,fontFace:BF,fontSize:10,color:MUTE});
  s.addNotes('Say the four numbers, then hold a beat on "Seventeen survived." 17/122,191 = 0.014%.');
}

/* ---------- 3. TIERS ---------- */
{
  const s = light();
  s.addText('Three tiers, ordered by risk — not by taste',{x:0.8,y:0.5,w:11.7,h:0.7,fontFace:HF,fontSize:38,bold:true,color:INK});
  s.addText('All 17 picks have a confirmed native Xbox console SKU. There is no port risk anywhere on the buy list.',
    {x:0.8,y:1.25,w:11.7,h:0.4,fontFace:BF,fontSize:16,color:GREEN,bold:true});

  s.addChart(p.ChartType.bar, [{
    name:'Titles',
    labels:['1 · Clean spine','2 · Restarts','3 · Confirm-then-sign','Watchlist (not a buy)'],
    values:[3,6,8,7]
  }], {
    x:0.7,y:1.9,w:5.4,h:4.3, barDir:'bar', ...chartQuiet,
    chartColors:[GREEN,GREEN,GREEN,'BFCFC1'], varyColors:true,
    showValue:true, dataLabelPosition:'outEnd', dataLabelFontFace:BF, dataLabelFontSize:14,
    dataLabelColor:INK, catAxisLabelFontSize:11, valAxisLabelFontSize:9, barGapWidthPct:45,
    valAxisMaxVal:10,
  });

  const cards = [
    ['1 · Clean spine — 3','Never on Game Pass, Xbox SKU confirmed, no blocker. The only tier with no unanswered question. It leads.',GREEN],
    ['2 · Restarts — 6','Previously on Game Pass. Port shipped, certification passed, rights holder already said yes once. Cheapest to execute — second on purpose.',GREEN],
    ['3 · Confirm-then-sign — 8','Xbox SKU confirmed for all eight. Only the current subscription status is open. One check, then sign.',GREEN],
    ['Watchlist — 7','No verified Xbox version. Named so the board sees them; explicitly NOT a buy. Promoted only on confirmation.','8A8F86'],
  ];
  cards.forEach((c,i)=>{
    const y = 1.9 + i*1.12;
    s.addShape(p.ShapeType.roundRect,{x:6.5,y,w:6.1,h:1.0,fill:{color:i===3?'F2F3F1':'EEF3EE'},rectRadius:0.08});
    s.addText(c[0],{x:6.72,y:y+0.07,w:5.7,h:0.3,fontFace:HF,fontSize:14,bold:true,color:c[2],margin:0});
    s.addText(c[1],{x:6.72,y:y+0.38,w:5.7,h:0.58,fontFace:BF,fontSize:11,color:INK,margin:0});
  });

  s.addText('Source: 17_portfolio_final.json · availability verdicts 13_availability.json',
    {x:0.8,y:6.75,w:11.7,h:0.3,fontFace:BF,fontSize:10,color:MUTE});
  s.addNotes('Second finding: no port risk. Flat, fast, factual. Do not decorate it.');
}

/* ---------- 4. RESTARTS ---------- */
{
  const s = light();
  s.addText('Six of them, we already licensed once',{x:0.8,y:0.5,w:11.7,h:0.7,fontFace:HF,fontSize:38,bold:true,color:INK});
  s.addText('The port shipped. Certification passed. The rights holder already said yes. Cheapest tier to execute.',
    {x:0.8,y:1.25,w:11.7,h:0.4,fontFace:BF,fontSize:16,color:MUTE});

  s.addChart(p.ChartType.bar, [{
    name:'Steam reviews',
    labels:['What Remains of Edith Finch','Phoenix Wright: Ace Attorney Trilogy','Unpacking','Persona 3 Reload','Library Of Ruina','Danganronpa 2'],
    values:[41326,33505,32385,29312,29181,25177]
  }], {
    x:0.7,y:1.9,w:7.4,h:4.4, barDir:'bar', ...chartQuiet,
    showValue:true, dataLabelPosition:'outEnd', dataLabelFontFace:BF, dataLabelFontSize:11,
    dataLabelColor:INK, dataLabelFormatCode:'#,##0',
    catAxisLabelFontSize:10, valAxisLabelFontSize:9, barGapWidthPct:45,
    valAxisMaxVal:50000,
    showTitle:true, title:'Steam reviews (recognition — not sales, not engagement)',
    titleFontFace:BF, titleFontSize:11, titleColor:MUTE,
  });

  s.addShape(p.ShapeType.roundRect,{x:8.4,y:1.9,w:4.2,h:2.1,fill:{color:'EEF3EE'},rectRadius:0.1});
  s.addText([
    {text:'Unpacking left ~2 months ago\n',options:{fontFace:HF,fontSize:18,bold:true,color:GREEN,breakLine:true}},
    {text:'The warmest counterparty in the set, and the one call that can be made this week.',options:{fontFace:BF,fontSize:13,color:INK}},
  ],{x:8.62,y:2.1,w:3.8,h:1.7,valign:'top'});

  s.addShape(p.ShapeType.roundRect,{x:8.4,y:4.2,w:4.2,h:2.1,fill:{color:'3A2419'},rectRadius:0.1});
  s.addText([
    {text:'But they do not lead.\n',options:{fontFace:HF,fontSize:18,bold:true,color:'E8C39E',breakLine:true}},
    {text:'Either the publisher declined to renew — or we did, on engagement data this analysis has never seen. We cannot tell from outside. You can, from inside, in a day.',
      options:{fontFace:BF,fontSize:12,color:'F0E6DC'}},
  ],{x:8.62,y:4.4,w:3.8,h:1.7,valign:'top'});

  s.addText('Departures verified with dated sources, Aug 2026 · 13_availability.md Group C',
    {x:0.8,y:6.75,w:11.7,h:0.3,fontFace:BF,fontSize:10,color:MUTE});
  s.addNotes('Slow down through the six names. Then raise the objection yourself before anyone else does.');
}

/* ---------- 5. THE ASK ---------- */
{
  const s = dark();
  s.addText('The ask',{x:0.8,y:0.6,w:11.7,h:0.8,fontFace:HF,fontSize:44,bold:true,color:CREAM});

  const asks = [
    ['1','Approve the seventeen','As a licensing slate, worked in tier order: clean spine, then restarts, then confirm-then-sign. No studio purchase. No price change. No new development.'],
    ['2','Authorise one internal lookup','Our own engagement record for the six restart titles during their prior runs. It costs nothing externally, takes a day, and closes the only open question on the list.'],
  ];
  asks.forEach((a,i)=>{
    const y = 1.75 + i*1.75;
    s.addShape(p.ShapeType.ellipse,{x:0.8,y:y+0.1,w:0.72,h:0.72,fill:{color:MOSS}});
    s.addText(a[0],{x:0.8,y:y+0.1,w:0.72,h:0.72,align:'center',valign:'middle',fontFace:HF,fontSize:26,bold:true,color:DARK,margin:0});
    s.addText(a[1],{x:1.8,y:y+0.05,w:10.6,h:0.45,fontFace:HF,fontSize:26,bold:true,color:CREAM,margin:0});
    s.addText(a[2],{x:1.8,y:y+0.55,w:10.6,h:0.85,fontFace:BF,fontSize:14,color:MOSS,margin:0});
  });

  s.addShape(p.ShapeType.roundRect,{x:0.8,y:5.35,w:11.7,h:1.15,fill:{color:'1B4526'},rectRadius:0.08});
  s.addText([
    {text:'Stated, not patched:  ',options:{fontFace:BF,fontSize:13,bold:true,color:MOSS}},
    {text:'no defensible per-title price exists for this tier, so none is offered — commit tier by tier and stop when the quotes stop making sense. Steam PC data behind an Xbox console decision. Picks are under a fifth Action against more than half the qualifying pool; the remedy was tested, did not work, and was withdrawn.',
      options:{fontFace:BF,fontSize:13,color:CREAM}},
  ],{x:1.05,y:5.5,w:11.2,h:0.9,valign:'top'});

  s.addNotes('Land the ask on two fingers. Then stop talking. Do not add a closing thought.');
}

p.writeFile({fileName:'/home/claude/run_portfolio/deliverables/pitch_deck.pptx'}).then(f=>console.log('wrote',f));
