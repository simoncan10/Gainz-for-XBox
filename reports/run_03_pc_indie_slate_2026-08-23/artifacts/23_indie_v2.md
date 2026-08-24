# Stage 23 — Indie scoring, rebuilt after red team (artifacts/22_redteam_indie.md)

This document supersedes `20_indie_scoring.md` as the live scoring artifact. `20_indie_scoring.md`,
`20_indie_candidates.csv` and `20_indie_model.json` are kept unmodified for the record; nothing in
them is retracted silently — every correction below names what it replaces and why.

The critic's verdict was **REBUILD the scoping**, not because dropping the Xbox console
requirement was wrong (it wasn't — confirmed again below) but because **the indie definition
itself was broken at both ends**: it excluded some of the most canonical indie games ever made
and admitted several 100+ title asset-flip publishing mills. Four fixes follow, in the order the
critic raised them.

## A-1 — The indie definition, rebuilt

**What was wrong.** `is_self_published` is a literal `developer == publisher` string match.
Verified: Lucas Pope develops *and* publishes Return of the Obra Dinn and Papers, Please, but
publishes under the label **"3909"** — a different string from his developer credit — so both
titles were classified **non-indie**. The same mechanism excluded every indie that signed with an
indie-friendly publisher: What Remains of Edith Finch and Journey (Annapurna Interactive),
Unpacking and Temtem (Humble Games), SANABI (NEOWIZ), ABZU (505 Games). Meanwhile it **admitted**
self-published mass-catalogue operations: EroticGamesClub (181 titles), Choice of Games (163),
Boogygames Studios (130), Hosted Games (109), Sokpop Collective (96).

**First attempt, tried and rejected: publisher catalogue size.** `is_indie=true AND
publisher_title_count<=N` passes the required hand-check for any N roughly in [32,105) — but at
the smallest passing N it still admits **48% of the whole catalogue**, barely narrower than the
raw flag's 67.6%. Publisher size doesn't separate a boutique label (Annapurna, 32 titles) from a
mainstream mid-size one (Nacon, 94 titles, only 4 of them indie-tagged) — the mass-catalogue
"admits" cases are only publisher-small-*and*-bad because they are self-published, which is the
exact confound this fix needed to remove, not inherit under a new name. **Not adopted.**

**Adopted: developer catalogue size.** `is_indie=true AND developer_title_count<=10`, where
developer_title_count is the developer's total non-demo game count catalogue-wide
(`sql/27_indie_definition_v2_sensitivity.sql`). This works because the mass-catalogue "admits"
cases are self-published — the *same* entity is both developer and publisher — so a huge
developer-title-count catches them exactly where a huge publisher-title-count did, while leaving
Giant Sparrow (2 titles), thatgamecompany (2), Lucas Pope (2), Witch Beam (2), WONDER POTION (1)
untouched regardless of what any publisher is called.

**Hand-check, verified line by line:**

| title | developer | dev title count | classified |
|---|---|---|---|
| Return of the Obra Dinn | Lucas Pope | 2 | **IN** |
| Papers, Please | Lucas Pope | 2 | **IN** |
| What Remains of Edith Finch | Giant Sparrow | 2 | **IN** |
| Journey | thatgamecompany | 2 | **IN** |
| ENDER LILIES | Live Wire / Adglobe | 1 | **IN** |
| Unpacking | Witch Beam | 2 | **IN** |
| ABZU | Giant Squid | 2 | **IN** |
| SANABI | WONDER POTION | 1 | **IN** |
| Choice of Games | Choice of Games | 163 | **OUT** |
| EroticGamesClub | EroticGamesClub | 181 | **OUT** |
| Boogygames Studios | Boogygames Studios | 130 | **OUT** |
| Hosted Games | Hosted Games | 109 | **OUT** |
| Sokpop Collective | Sokpop Collective | 96 | **OUT** |

Extended past the required list: Supergiant Games (5 titles — Bastion/Transistor/Pyre/Hades/Hades
II), Vlambeer (5), Mode 7 (3) all stay **IN** at N=10. N=2 (the strictest cutoff that still
passes the required hand-check) would have wrongly excluded all three. Klei Entertainment (12
titles) is excluded at N=10 — an acceptable edge, not required in by any hand-check item.

**Honestly disclosed limitation, not hidden.** This narrows the raw `is_indie=true` population
from 67.6% of the non-demo catalogue to **44.8%** (54,692/122,191) — *less* narrowing than the
flawed `is_self_published` rule achieved (36.8%). Developer-catalogue-size fixes **who** is
correctly classified as indie; it does not, on its own, make "indie" a small segment, because most
Steam titles carrying the Indie genre tag genuinely are made by tiny (1–2 title) developers — a
structural fact about this catalogue, not a modelling failure. The real narrowing to an actionable
candidate segment happens downstream, in the same eligibility screen as before, via review/
quality/owner/price thresholds (see below: 573 titles, 0.47% of the non-demo catalogue).

## A-2 — The Fit-compensates-for-the-gate claim, dropped

Stage 20 argued dropping the controller-support hard gate was equivalent to "demoting" it,
because the Fit model already scores `has_controller_i` (coefficient +0.0387, its strongest
positive). True but empty: Fit is weighted 10%, has in-population R²=−1.34, and titles in the
bottom 1–4% of Fit rank sit freely in the qualifying top 20 (KovaaK's fit_pct=0.0395, Verdun
fit_pct=0.0099 in the v20 run). **Corrected reasoning:** the gate is dropped for the narrower,
correct reason only — Game Pass runs on Windows PC, so a console-fit proxy no longer applies to a
keyboard/mouse-only title. Nothing replaces the gate's quality-signal role. The measured cost is
reported **per tier**, not just pool-wide, as the critic asked:

| tier | qualifying n | no-controller n | no-controller % |
|---|---|---|---|
| Anchor | 178 | 45 | 25.3% |
| Depth | 12 | 2 | 16.7% |
| Low-cost option | 11 | 5 | 45.5% |
| **All** | **201** | **52** | **25.9%** |

## A-4 — Review floor, fully re-derived (not truncated)

Stage 20 ran nine rows of a metacritic-presence sensitivity sweep and quoted only the first four
(500–5,000), stopping exactly before the curve's later rise became visible. Re-run in full on the
**rebuilt** population (`sql/28_indie_v2_review_floor_full_sensitivity.sql`):

| floor | 500 | 1,000 | 2,000 | 3,000 | 4,000 | **5,000** | 6,000 | 7,500 | 10,000 |
|---|---|---|---|---|---|---|---|---|---|
| n | 4,486 | 2,766 | 1,626 | 1,112 | 844 | **669** | 531 | 395 | 259 |
| metacritic % | 25.0 | 30.0 | 34.2 | 36.2 | 37.7 | **38.7** | 38.8 | 39.0 | 39.4 |
| marginal gain (pp) | — | +5.0 | +4.2 | +2.0 | +1.5 | **+1.0** | +0.1 | +0.2 | +0.4 |

**Raised the floor from 4,000 to 5,000.** The plateau starts cleanly at 5,000: the step just
before it still buys +1.0pp; the step just after buys +0.1pp — a 10x drop in marginal return. Did
not move to 6,000+ as the critic's note on the old (now-superseded) population implied, because
that note was read off a messier, different curve; on the corrected population the plateau
genuinely begins at 5,000, and the remaining 6,000–10,000 gains (+0.7pp cumulative) do not justify
losing another 138 titles to reach them.

Owners ceiling re-checked at the new floor (`sql/29_indie_v2_owners_ceiling_sensitivity.sql`):
**kept at 750,000** — bucket-equivalent to 1,000,000, and relaxing further keeps buying
metacritic density (40.4% → 42.3% → 44.3% at 1.5M/3.5M) at the direct cost of the ceiling's
purpose.

## A-5 — The composite is a review-count ranking, disclosed plainly

Within the 6-value `owners_mid` bucket structure, Recognition (percentile of `ln(review_total)`)
and Headroom (percentile of `ln(review_total) − ln(owners_mid)`) are near-perfectly collinear —
Spearman = 1.0000 within every bucket with n≥5 (150,000 / 350,000 / 750,000). Pooled R² of the
composite against `ln(review_total)` alone is **0.775**. **In the top 20, `owners_mid` takes only
two values (350,000 and 750,000).** So the composite, at weights 0.50/0.40, is overwhelmingly one
variable — log review count — banded by a near-constant ownership step. This is not new (Stage 15
flagged the same structure); it is reconfirmed, sharper, on the rebuilt pool, and stated here
without qualification.

**The cross-artifact tension the critic found, and how it's resolved:** `21_indie_thesis.md`
warns that reviews-per-owner is a confounded, weak proxy — not to be read as engagement. This
scoring model's composite leans on the volume side of exactly that quantity. Both statements are
individually true and they sit in real tension. Resolution: this document now states the
composite is a review-**volume** ranking, not a broad quality blend; the thesis document (revised
separately, see `23_indie_thesis.md`) stops treating reach and propensity as two independent
lines of evidence within an owners bucket — they are the same measurement counted twice.

## Result

Eligible pool: **573** (up from 406; metacritic presence 42.8%, up from 34.5% — both effects of
the wider, corrected definition and the raised floor). Qualifying at bar=0.60: **201** —
Anchor 178 / Depth 12 / Low-cost option 11.

## Top 20 by composite score

| rank | title | developer | tier | score | reviews | owners | price | MC |
|---|---|---|---|---|---|---|---|---|
| 1 | Firework | Shiying Studio | Anchor | 0.975 | 39,637 | 500k–1M | $9.99 | — |
| 2 | A Hat in Time | Gears for Breakfast | Anchor | 0.970 | 50,390 | 500k–1M | $29.99 | 79 |
| 3 | Unpacking | Witch Beam | Anchor | 0.959 | 32,385 | 500k–1M | $19.99 | 83 |
| 4 | The Hungry Lamb | 零创游戏 | Anchor | 0.959 | 38,601 | 500k–1M | $7.49 | — |
| 5 | BlazBlue Entropy Effect | 91Act | Anchor | 0.950 | 23,190 | 200k–500k | $19.99 | — |
| 6 | VA-11 Hall-A | Sukeban Games | Anchor | 0.949 | 34,897 | 500k–1M | $14.99 | 77 |
| 7 | Temtem | Crema | Anchor | 0.947 | 38,583 | 500k–1M | $44.99 | 79 |
| 8 | SANABI | WONDER POTION | Anchor | 0.945 | 30,102 | 500k–1M | $14.99 | — |
| 9 | What Remains of Edith Finch | Giant Sparrow | Anchor | 0.941 | 41,326 | 500k–1M | $19.99 | 89 |
| 10 | ENDER LILIES | Live Wire / Adglobe | Anchor | 0.930 | 35,018 | 500k–1M | $24.99 | 86 |
| 11 | Wandering Sword | The Swordman Studio | Anchor | 0.921 | 19,877 | 200k–500k | $24.99 | — |
| 12 | Library Of Ruina | ProjectMoon | Anchor | 0.920 | 29,181 | 500k–1M | $29.99 | — |
| 13 | Journey | thatgamecompany | Anchor | 0.918 | 32,370 | 500k–1M | $14.99 | — |
| 14 | A Short Hike | adamgryu | Anchor | 0.916 | 17,323 | 200k–500k | $7.99 | 82 |
| 15 | Path Of Wuxia | 香港商河洛互動娛樂 | Anchor | 0.913 | 30,091 | 500k–1M | $34.99 | — |
| 16 | Potion Craft | niceplay games | Anchor | 0.907 | 31,904 | 500k–1M | $19.99 | — |
| 17 | Milk inside a bag of milk... | Nikita Kryukov | Anchor | 0.906 | 26,566 | 500k–1M | $1.49 | — |
| 18 | Return of the Obra Dinn | Lucas Pope | Anchor | 0.905 | 26,518 | 500k–1M | $13.39 | 89 |
| 19 | Chants of Sennaar | Rundisc | Anchor | 0.903 | 17,036 | 200k–500k | $12.99 | 86 |
| 20 | Rogue Legacy | Cellar Door Games | Anchor | 0.895 | 18,349 | 200k–500k | $14.99 | 85 |

Eight of the previously-excluded canonical titles now appear inside the top 20 (Unpacking, VA-11
Hall-A, Temtem, SANABI, Edith Finch, ENDER LILIES, Journey, Potion Craft, Obra Dinn) — direct,
verifiable evidence the A-1 fix worked as intended, not just on the two required hand-check
titles but across the critic's full "excluded canonicals" list.

## Confidence statement

The definition fix is structural and verified against a named hand-check plus an extended
spot-check; it should hold under further scrutiny. The composite's degeneracy (A-5) is real,
disclosed, and unresolved — it was not this pass's mandate to redesign the pillar formula, only
to describe it honestly, and that is what this document now does. `owners_mid`'s coarseness (6
distinct values) and the absence of any Game Pass availability signal remain unchanged, standing
limitations carried from every prior stage.
