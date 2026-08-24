# Pitch script — Game Pass catalogue decision
**Audience:** Microsoft / Xbox board · **Date:** 22 August 2026

> **Word count (spoken body only): 412 words**
> **Runtime at 130 wpm: 3 min 10 sec · at 150 wpm: 2 min 45 sec**
> Inside the 390–450 budget. If the timer is hard-stopped at three minutes, cut the two sentences
> marked **[CUT FIRST]** and **[CUT SECOND]** in Evidence: that gives **381 words — 2 min 56 sec
> at 130 wpm**, 2 min 32 sec at 150. Cutting only the first gives 390 words, which is exactly
> three minutes at 130 — take both.
>
> *Revised after `artifacts/07_final_check.md`: four figures corrected (estimated subscriber base,
> "candidates" not "licensable", the price-lever range restored, six-to-eight weeks).*

**Delivery key:** **bold** = land the word · `//` = full stop, one beat · `///` = two beats, look up.

---

## HOOK — 0:00–0:20 (43 words)

Microsoft has already run **five hundred** Game Pass licensing deals. `//`
Nobody has ever measured what a single one of them did to churn. `///`

That is a five-hundred-deal experiment. Already paid for. Sitting unread. `//`

So my recommendation is this. **Spend nothing today.** Read it.

> *Delivery: open flat and slow. Do not smile through "nobody has ever measured."
> The two-beat pause before "That is" is the whole hook — hold it.*

---

## TENSION — 0:20–0:45 (67 words)

In April you cut Ultimate from thirty dollars to **twenty-three**. `//`
Against churn, that is somewhere between **four hundred million and one and a quarter
billion** a year, given up. `//` **Fourteen to forty times** any licensing programme anyone
would ask you for. `///`

You chose price over catalogue, at scale, without ever measuring which one works. `//`
I am not asking you to choose. I am asking you to **measure**.

> *Delivery: "fourteen to forty times" is the number they will remember. Slow down on it —
> and say "somewhere between" clearly, because the range is the honest part.*

---

## EVIDENCE — 0:45–1:45 (115 words)

**One. Breadth is worthless.** `//` In every major genre we looked at, the top tenth of titles
takes roughly **four-fifths or more** of the audience. Buying a hundred games buys you ninety
bad ones.

**Two. You already hold the answer.** `//` Five hundred deals, priced from fifty thousand
dollars to over fifty million. **[CUT FIRST]** *And licence expiries were fixed by contracts
signed years ago — so they are close to a natural experiment, not a management choice.*

**Three. The prize is real and bounded.** `//` Around **six hundred and fifty** proven titles
screen through as **candidates**. At a million and a half each, a full sweep is
order-of-magnitude **a billion dollars**. `///` **[CUT SECOND]** *That is worth measuring. It is
not worth guessing.*

> *Delivery: count them on fingers. One breath per finding. Do not rush finding three —
> the billion is what makes the audit worth six weeks of someone's time.*

---

## RECOMMENDATION — 1:45–2:30 (110 words)

So: approve the audit — **six to eight weeks, no capital** — and pre-commit, today, to this rule. `///`

**Break-even is twenty-five thousandths of a percentage point of annual churn, per title-year.**

Here is where that comes from. `//` One point of churn, on an estimated thirty million
subscribers, is three hundred thousand people. Times a hundred and sixty-eight dollars, at sixty percent margin.
That is **thirty million dollars a year**. `//` A licence at one and a half million, over
twenty-four months, costs **seven hundred and fifty thousand** per title-year. `//`
Seven-fifty into thirty million is **nought-point-nought-two-five**.

Above that line, licensing pays, and you scale it. Below it, you do not buy at that price.

> *Delivery: this is the arithmetic slide — point at it, do not read it. Three numbers, three beats.*

---

## RISK AND ASK — 2:30–3:00 (77 words)

The obvious objection, and it is the right one. `//` This is **Steam PC data**. Your subscribers
are on console, spend about half as much again, and play different genres. `///`
So I am not asking you to act on my dataset. My dataset proves only that the retention signal
does not exist **anywhere outside this building**. The number that decides this is yours. `//`

Approve six to eight weeks, no money, and the rule. `///` **Then hold me to it.**

> *Delivery: concede the objection with your chin up, not apologetically. Final line — stop, look up,
> stay silent. Do not add "thank you" until they react.*

---

## Number trace

| Spoken | Source |
|---|---|
| 500+ Game Pass deals | 04_context.md §3 `gp-deal-cost-range` (MacIntyre, 500+ deals, $50K–$50M+) |
| $29.99 → $22.99, April 2026 | 04_context.md §1 [FACT], Xbox Wire 2026-04-21 |
| $420M–$1.26B a year | 06_redteam_v2.md §2 — $7.00 × 12 × 5M/10M/15M Ultimate subs; arithmetic exact, subscriber split unsourced, so the **range** is spoken, never the $840M midpoint |
| 14×–42× ("fourteen to forty") | Same range ÷ the $30M tranche; redteam_v2 §2 confirms both ends |
| top tenth takes ~four-fifths+ | F1, 03_findings.md — 78–93%; per M7 spoken as a *shape*, never to a decimal |
| ~650 **candidates** | 05_theses_final.json `R1_confirmed` — range 646–652, spoken as "around 650". **Before** netting against Game Pass's existing titles, before rights clearance, before a console-penetration screen this data cannot support (05_decision_tree.md line 43) — hence "candidates", never "licensable" |
| ~$1B full sweep | 05_decision_tree.md — 650 × $1.5M ≈ $975M, order of magnitude only |
| 0.025pp / title-year | 05_decision_tree.md Branch A — 750K ÷ 30.24M = 0.0248pp |
| "an estimated thirty million" subs | 04_sources.json `gp-subscribers-estimate-2026` — third-party aggregator, confidence LOW, band 30–34M. Microsoft does not disclose it, so it is never spoken as fact |
| $168, 60%, $30.24M | 05_decision_tree.md Branch A; all three inputs flagged unsourced in `assumptions` and replaced by measured internal values once the audit runs |
| six to eight weeks | 05_theses_final.json T2 `first_step` — the artifact says 6–8; the ask states the full range rather than the optimistic end |
| console spends ~half again more | 04_context.md §5 — ARPPU $81.68 console vs $55.47 PC (~48%) |

**Not said, deliberately:** anything about engagement or playtime (no such data exists);
any per-title effect claim (R8); any annual programme figure (withdrawn at R1);
any studio-investment recommendation (T3 withdrawn).
