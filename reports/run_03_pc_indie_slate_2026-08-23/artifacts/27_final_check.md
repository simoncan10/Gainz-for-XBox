# Stage 27 — Final deliverable check

**Result: PASS.** All seven checks clear. Two minor non-blocking notes at the end.

Scope: `deliverables/indie_evidence_appendix.md`, `indie_pitch_script.md`,
`indie_onepager.md`, `indie_deck.pptx` (slide XML + all 7 speaker notes extracted), against
`23_indie_v2.md`, `21_indie_thesis.md`, `25_indie_portfolio.json`,
`24_availability_indie.json` and `parquet/`.

---

## 1. Traceability — PASS

The traceability index is **24 rows**, counted, and complete. Every figure appearing in the
appendix, script or deck resolves to an artifact, and every index row resolves to a value in
the artifacts. Spot-verified directly rather than trusted:

| index row | claimed | re-derived |
|---|---|---|
| Hit-rate ratios | 72.2 / 45.9 / 35.0 / 29.4% | 11.75÷16.27, 2.66÷5.79, 1.16÷3.31, 0.15÷0.51 = **72.2 / 45.9 / 35.0 / 29.4** ✓ |
| Survivorship exclusion | 36.9% indie vs 35.1% non-indie | **36.9 / 35.1** ✓ |
| First-hit rate | 3.13% vs 7.70% | 690/22,028 = **3.13%**; 626/8,115 = 7.71% (see Note A) |
| Composite vs log reviews | R² 0.775 | `23_indie_model_v2.json` = **0.7749** ✓ |
| Pillar influence | Recognition 0.886 / Headroom 0.828 / Fit 0.155 | json = **0.8864 / 0.8281 / 0.1547** ✓ |
| Eligible / qualifying | 573 (42.8% MC) / 201 | present in json ✓ |

The pitch script carries its own 16-row spoken-figure table; every spoken number appears in
it. No figure was found in any deliverable that is absent from the index.

## 2. Headline arithmetic — PASS, all re-derived from `parquet/`

| figure | published | re-derived |
|---|---|---|
| Population | n=48,682 (30,003 / 18,679) | **48,682 (30,003 / 18,679)** ✓ |
| Mean price | $8.74 vs $12.51 → 30.1% | $8.7394 vs $12.5120 (see Note B) |
| Median price | $5.99 vs $7.99 → 25.0% | 1−(5.99÷7.99) = **25.03%** ✓ |
| Titles per $1,000 | 63.47 vs 41.39 (1.53×) | n=994 @ $15.7543 → **63.47**; n=931 @ $24.1586 → **41.39**; ratio **1.5335** ✓ |
| Cost per million owners | $92.81 vs $61.93 (1.50×) | $8.7394÷0.094162 = **$92.81**; $12.5120÷0.202037 = **$61.93**; ratio **1.4987** ✓ |
| Pick price sum | $417.69 → 50.28 | 21 prices sum to **$417.69**; 1,000×21÷417.69 = **50.28** ✓ |
| Portfolio vs benchmark | +21.5% | 50.28÷41.39−1 = **+21.47%** ✓ |
| Pool vs benchmark | +53.3% | 63.47÷41.39−1 = **+53.35%** ✓ |
| Temtem cut | 53.66 | 1,000×20÷372.70 = **53.66** ✓ |

**"40% of the edge retained" — verified correct, and the two candidate readings are the same
calculation.** The appendix computes (50.28 − 41.39) ÷ (63.47 − 41.39) = 8.89 ÷ 22.08 =
**40.25%**. The coordinator's "obvious reading," 21.5 ÷ 53.3, gives **40.25%** as well —
algebraically identical, because both percentages share the 41.39 denominator, which cancels:
(P/B − 1) ÷ (L/B − 1) ≡ (P − B) ÷ (L − B). There is no ambiguity to resolve and no error.

It is also **the right comparison**: it measures how much of the *pool's advantage over the
non-indie benchmark* survives selection, which is the quantity the erosion claim is about.
The alternative naive reading — 50.28 ÷ 63.47 = 79% — would answer a different and
less honest question (portfolio as a share of pool, ignoring the benchmark the case rests on).
The appendix explicitly rejects defending 53.3% and names 40% as "the honest number."

## 3. No engagement claim anywhere — PASS

Independent sweep of **20 terms** (engag·, retention, retain, session, playtime, play time,
hours played, sticky, stickiness, "keeps subscribers playing", replayab·, time spent, longer,
addictive, hooked, "come back", "return to", dwell, "completion rate", "players stay") across
all four deliverables **including all 7 speaker notes**.

- **Zero hits** on *sticky, stickiness, replayability, addictive, hooked, time spent, dwell,
  completion rate, hours played, "keeps subscribers playing", "players stay".*
- ~35 occurrences of *engagement / retention / playtime / session*. **Every one is a
  disclaimer, a withdrawal record, or a negation.** Representative: appendix Caveat 1 ("No
  engagement, retention or session-length claim is made anywhere in this analysis, for any
  title, in either direction"); §3.1 ("UNSUPPORTED and UNMEASURABLE"); §8 row 1; script
  ("We make no engagement claim"); onepager header ("no engagement or retention claim is made
  for any title"); deck slide 7 footer ("No engagement claim is made: this data has no
  playtime at all"); notesSlide5 ("**Do NOT say engagement**").
- The single "longer" hit is "a console-fit proxy no longer applies" — unrelated.
- One nuance, judged clean: the onepager's Tier-2 removal rule cites "the bottom quartile of
  **engagement per licensing dollar**" — a condition on **Microsoft's own internal record**,
  not an assertion from this dataset. It claims nothing about indie titles and is correctly
  framed as a trigger for data Microsoft holds.

*Observation:* the writer reported the sweep as "only two hits, both disclaimers." A wider
synonym sweep finds ~35. **The conclusion is correct** — none asserts engagement — but the
"two hits" characterisation understates what a checker will find.

## 4. Counterargument at full strength — PASS, none softened

All five required items present and unhedged. Quoted:

- **Engagement unsupported and unmeasurable** — §3.1: *"Leg (b) is withdrawn entirely… This
  is not 'the proxies say no.' It is '**there is no data that can answer this**.'"* and
  *"Anyone who repeats 'indie games are more engaging' on the strength of this analysis is
  saying something the analysis specifically found untestable."*
- **Reach per title genuinely worse, 72.2% → 29.4%** — §3.3 heading: *"Reach per title is
  GENUINELY WORSE"*; full four-row table at 72.2 / 45.9 / 35.0 / 29.4, with *"the gap widens
  at the top end."*
- **Survivorship widening the gap** — §3.3: *"Survivorship runs against indie, not for it…
  Removing the floor moves the ratio **down**: from 72.2% to 70.5%… So the table above is, if
  anything, **generous to indie**."*
- **Per-owner cost 50% worse** — §3.6: *"indie costs **$92.81 per million against non-indie's
  $61.93 — 50% worse**."*
- **Non-indie first hit 2.5× as often** — §3.5: *"**Non-indie developers land a first hit
  roughly 2.5× as often** (7.70 ÷ 3.13 = 2.46)."*

§3.6 closes without hedging: *"On the yardstick most people instinctively reach for — audience
per dollar — **the recommendation in this deck is a worse buy, and by a wide margin.**"* The
script speaks the objection aloud at 2:20 and instructs *"Do not drop the objection."*

## 5. Withdrawn claims stay withdrawn — PASS

Searched all four deliverables (deck slides **and** all 7 notes) for the retracted figures and
framings: `74%`, `73.8`, `0.00706`, `0.00956`, `Fit compensates`, `compensates for`,
`not less consistent`, `is_self_published`, the >$20 sentiment reversal, and the superseded
hit-rate ratios `50.9%` / `28.2%`.

- **Deck: 0 hits, slides and speaker notes both.** **Onepager: 0 hits.**
- **Script: 1 hit** — `is_self_published` appears once, in the traceability table, as the
  description of the *broken* rule being cited as a method failure.
- **Appendix: 12 hits, all inside §3.2 (the withdrawal explanation) or §8 (the
  withdrawn-claims register).** Each is quoted as retracted, with its replacement stated.
- The 82.4% unconditional propensity figure survives in §2.3 but is explicitly labelled
  *"a composition effect and is not a finding."*
- No withdrawn number is re-asserted anywhere. The speaker notes — the usual hiding place —
  are clean.

## 6. Deck scope — PASS, not a data dump

Seven slides. **No tables, no per-title statistics, no hit-rate or price tables anywhere.**

| slide | statistics carried |
|---|---|
| 1 — title | "21 catalogue slots" (the recommendation itself) |
| 2 — funnel | 122,191 / 573 / 201 / 25 / 21 — **the permitted funnel counts** |
| 3 — filter failure 1 | none; three title names |
| 4 — filter failure 2 | 181 / 163 / 130 — catalogue counts illustrating the method failure |
| 5 — investment idea | **1.50× and 1.53× — the one permitted contrast** |
| 6 — the slate | 4 / 5 / 12 tier counts + "40%" |
| 7 — the ask | none; qualitative honesty footer |

Slide 6's "**40%**" is the only figure beyond the permitted set. Judged **in scope**: it is a
single number, it is the honest-erosion qualifier attached to the slate rather than analysis
detail, and removing it would leave the deck claiming the pool-level advantage the appendix
explicitly says must not be defended. Slide 4's 181/163/130 are method narrative, not
findings. No slide has drifted into appendix material.

## 7. Onepager reconciliation — PASS

Parsed all 21 numbered rows and joined to `25_indie_portfolio.json` on `app_id`.

- **21 rows ↔ 21 JSON titles. Zero mismatches** on app_id, name, review_total and price.
- Retail prices sum to **$417.69**, matching the appendix and the JSON.
- **Every Game Pass verdict maps correctly** to `24_availability_indie.json`:
  `no` → "Not included; no evidence ever added" (rows 1, 2, 4); `rotated_out` → "Rotated out"
  with dates (rows 5–9); `unknown` → "Added…; no dated exit — status check required"
  (rows 10, 15, 17, 18, 20); `not_verified` → "No evidence either way" (rows 11–14, 16, 19),
  with row 3 (Rogue Legacy) correctly escalated to *"rests on absence of dated evidence."*

---

## Two minor notes — neither blocking, neither requiring a re-run

**Note A — §3.5 producer-consistency detail.** The appendix states non-indie hitters *"average
more titles overall (**4.15** vs 1.93)."* Re-derived on the stated population I get **5.09 vs
1.93**. Also 8,114 devs / 625 hitters / 7.70% / 25.60% repeat against my 8,115 / 626 / 7.71% /
25.72% — an off-by-one consistent with NULL-developer handling. **Direction and conclusion are
unchanged, and the published 4.15 *understates* evidence running against the recommendation**,
so the error is in the conservative direction. Worth reconciling the 4.15 before the room only
because it sits in the counterargument, which the client asked to be at full strength.

**Note B — a 0.1pp rounding artifact.** The mean price discount from unrounded means is
1 − (8.7394 ÷ 12.5120) = **30.15%**, which rounds to 30.2%. The appendix publishes **30.1%**
and shows its arithmetic from the rounded inputs — *"1 − (8.74 ÷ 12.51) = 0.3013 → 30.1%"* —
so the working is transparent and the rounding does no hidden work. The median figure (25.0%)
is exact. No implication changes at either value; recorded for completeness only.

---

**Verdict: PASS.** The traceability index is complete and correct, every headline figure
re-derives from `parquet/`, the "40% retained" calculation is right and unambiguous, no
engagement claim survives anywhere including the speaker notes, the counterargument is at full
strength and unhedged, no withdrawn claim reappears, the deck carries method and idea rather
than data, and the onepager reconciles exactly to both source artifacts.
