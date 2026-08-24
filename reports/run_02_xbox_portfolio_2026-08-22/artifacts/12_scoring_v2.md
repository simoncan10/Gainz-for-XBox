# Stage 12 — Scoring v2: rebuild after red-team verdict REBUILD

`artifacts/11_redteam_scoring.md` verdict was **REBUILD**, not "stands narrowed." This
document is the rebuilt model. v1 (`10_scoring.md`, `10_candidates.csv`, `10_model.json`)
is left in place unchanged — the progression from v1 to v2 is part of the deliverable.

## Zero — a discrepancy caught during verification, not accepted on trust

The coordinator's forwarded "reported yield" was **pool=926, 44.2% metacritic presence**,
topped by SnowRunner, Dead Space, Guardians of the Galaxy, Verdun, ICARUS, Persona 3
Reload, Edith Finch, Journey, Lies of P, Temtem. Per the explicit instruction to verify
rather than trust this, direct queries show:

- **926 is the pool count WITHOUT `has_controller_support=true` applied.** The literal
  rebuild spec's screen table lists that gate as an addition. Applying it (as instructed)
  gives **pool = 638**, not 926.
- **Temtem and ICARUS — both in the reported top-10 — have `has_controller_support=false`**
  in this dataset (verified directly). Neither could appear in a pool that actually
  applies the gate the spec calls for.

This run implements the gate **literally, as the coordinator's bulleted spec states it**,
and reports the resulting numbers (638 / 215) rather than the ungated ones (926 / ~320).
The discrepancy is recorded here and in `DECISIONS.md` rather than silently resolved either
way.

## Step 1 — determinism (RT-01, FATAL, fixed)

`sql/11v2_fit_model_population.sql` adds `ORDER BY f.app_id`. `scripts/11v2_build_fit_model.py`
additionally re-sorts by `app_id` in pandas before every `train_test_split` call — belt and
suspenders, so a future edit to the SQL can't silently reintroduce the bug. **Verified: two
independent re-runs of the full v2 pipeline in this session produced identical
eligible_pool_n (638), n_qualifying (215), and identical top-20 order both times.** Model
artifacts (`_ridge_coef_v2.npy`, `_ridge_intercept_v2.txt`, `_feature_cols_v2.json`) are
committed to `artifacts/` so `scripts/12v2_score_candidates.py` runs end to end from a
clean checkout — v1 shipped without them.

## Step 2 — the rebuilt eligibility screen

| Screen | v1 | v2 | Why changed |
|---|---|---|---|
| Not free, price known | keep | keep | unchanged |
| Quality (review_positive_ratio) | ≥0.70 | ≥0.70 | unchanged (Valve's own boundary) |
| No adult-content tag | keep | keep | unchanged |
| **Proven floor** | review_total≥**50** | review_total≥**5,000** | RT-06: 50 answered "is this rating statistically meaningful" (Valve's own bucket-nuance threshold), a different question from "would a subscriber recognise this." |
| **Ownership ceiling** | owners_mid≤750,000 | owners_mid≤750,000 | **kept per explicit instruction** |
| **Controller support** | — | **added: has_controller_support=true** | RT-11: evidence-backed (strongest surviving positive Fit coefficient) Steam-PC→Xbox-console platform-fit gate |

**Result: 122,191 non-demo games → 638 eligible (0.52% of the catalogue), 48.0% carrying
a Metacritic score** — up from 14.4% in v1's 15,921-title pool. The controller gate alone
removes 288 titles from the pre-gate 926 and *raises* metacritic presence from 44.2% to
48.0%, i.e. it concentrates recognition rather than diluting it.

### Justifying 5,000 reviews (not borrowed, tested on its own terms)

Metacritic presence (the dataset's only independent press-coverage signal, and one the
composite never uses directly) rises steeply with the floor, then flattens:

| floor | n | metacritic % |
|---|---|---|
| ≥500 | 3,241 | 33.4% |
| ≥1,000 | 2,239 | 38.2% |
| ≥2,000 | 1,442 | 42.2% |
| ≥3,000 | 1,047 | 44.6% |
| **≥5,000** | **638** | **48.0%** |
| ≥7,500 | 399 | 47.4% |
| ≥10,000 | 271 | 47.6% |
| ≥15,000 | 132 | 44.7% |

5,000 sits at the elbow: raising the floor further (7,500/10,000/15,000) buys no further
recognition-density and only shrinks the pool, sometimes reversing (15,000's 44.7% is
below 5,000's 48.0%, likely noise at n=132). This is a threshold justified on its own
terms, not borrowed from Valve's unrelated 50-review nuance boundary. Full table in
`sql/17_threshold_sensitivity_v2.sql`.

### Justifying (or rather, honestly restating) the 750,000 ownership ceiling

Kept per instruction. Stated plainly per RT-09: `owners_mid` has only **6 distinct values**
in this eligible pool (10,000 / 35,000 / 75,000 / 150,000 / 350,000 / 750,000), and there
is **no value between 750,000 and 1,499,999** — so a 750,000 ceiling and a 1,000,000
ceiling produce the *identical* pool (both n=638, confirmed). The ceiling should be read
as "≤ the 500k–1M bucket," not as a fine 750,000-unit cut. Relaxing it further does
increase metacritic presence (50.2% at 1.5M, 52.9% at 3.5M) but at the cost of including
titles the brief's "not already widely owned" test would reject.

## Step 3 — the rebuilt fit model (RT-05)

**Retargeted** from `ln(1+review_total)` (which the red team showed IS the Recognition
pillar, observed for every candidate — predicting it added noise, not information, and
the noise outranked the measurement) to **`review_positive_ratio`** — a quantity neither
Recognition nor Headroom encodes at all. `price_usd` is excluded from its features (so
price cannot re-enter the composite through the Fit door) and `is_indie_i` is dropped
(was perfectly collinear with `genre_Indie` in v1).

**Out-of-sample performance, reported as a range across 5 seeds** (per the requirement —
the single point estimate is exactly what v1 got wrong):

| | Pearson r | R² |
|---|---|---|
| Range across seeds {42,7,123,2024,99} | **0.377 – 0.388** | 0.142 – 0.151 |
| Mean | 0.384 | 0.147 |
| Canonical model (seed 42), scoped to the actual v2 eligible population (n=221 in the holdout fold) | 0.391 | −1.34 (negative — the model does not generalize well within this specific small slice; reported honestly, not hidden) |

**This is a substantially weaker fit than v1's (Pearson ~0.56).** That is expected and
appropriate: predicting reception *quality* from structural genre/tag traits is inherently
harder than predicting review *volume* (which correlates with age, marketing reach, and
multiplayer virality — all of which v1's target absorbed). Fit's weight was cut to 20% to
match this weaker, but now non-redundant, signal.

## Step 4 — the rebuilt composite (RT-02, RT-04)

```
composite_score = 0.45 × Recognition_pct + 0.35 × Headroom_pct + 0.20 × Fit_pct
```

- **Recognition** = percentile of `ln(review_total)`.
- **Headroom** = percentile of `ln(review_total) − ln(owners_mid)` — reviews-per-owner,
  replacing v1's Proven+Scarcity pair (Spearman **−0.762**, which made their *sum*
  near-constant and gave Scarcity ~0 effective influence). Headroom directly encodes
  "punches above its weight" as one ratio instead of two cancelling percentiles.
- **Fit** = the retargeted model above.
- **Price is removed from the score entirely.** `price_usd` is a reported column only,
  used to assign the Low-cost tier label, never to compute rank.

**Verification that RT-02 does not reproduce:** Recognition and Headroom are now Spearman
**+0.542** (complementary, not cancelling). Measured pillar influence on the composite
(Spearman of each pillar against the final score): **Recognition 0.870, Headroom 0.812,
Fit 0.179** — all three pillars visibly move the ranking; none is a dead weight.

> **Correction added at Stage 16, after Stage 15 red team (A-3) — read this before citing
> the +0.542 figure above.** That pooled correlation is real but is a **between-bucket
> artifact**, not evidence of two independent pillars. `owners_mid` has only 5 distinct
> values in this pool, and three buckets hold 634 of 638 titles (99.4%). **Within every
> bucket, Spearman(recognition_raw, headroom_raw) = 1.0000 exactly** — verified directly:
> 150,000-bucket (n=31): 1.0000; 350,000-bucket (n=243): 1.0000; 750,000-bucket (n=360):
> 1.0000. Headroom is Recognition minus a per-bucket constant. The honest framing is that
> this composite is **Recognition (continuous, 0.45–0.50 weighted), banded by a
> three-level ownership step** — not a four-way or even three-way blend. Within any given
> ownership tier, the ranking is "most-reviewed first," full stop; Headroom's only real
> job is moving a title between three coarse tiers, not ordering it within one. This
> cannot be fixed by reformulating Headroom from the same `owners_mid` column — the
> coarseness is in the underlying SteamSpy bucket data (documented since
> `01_profile.md`), so it is disclosed, not resolved. Full verification and the related
> finding that 60–83% of the qualifying/portfolio list sits against the 750,000-owner
> ceiling (the ceiling is closer to *defining* the list than *filtering* it) are in
> `artifacts/16_scoring_v3.md` and `DECISIONS.md`, Stage 16.

## Step 5 — the qualifying bar

Same logic as v1 (percentile-weighted pillars summing to 1.0 still center an unremarkable
title at ~0.50): **bar = composite ≥ 0.60 → 215 qualifying titles (33.7% of the 638-title
eligible pool, 0.176% of the whole catalogue).**

| bar | 0.50 | 0.55 | **0.60** | 0.65 | 0.70 | 0.75 |
|---|---|---|---|---|---|---|
| n qualifying | 301 | 261 | **215** | 172 | 134 | 84 |

**Reweighting stability, reported as top-30 Jaccard overlap (RT-10 — Spearman across the
whole pool is blind to reordering at the extreme, which is the only region a shortlist
uses):** recognition-heavy (60/25/15) keeps **87.5%** of the published top-30; headroom-heavy
(25/60/15) keeps 57.9%; fit-heavy (25/25/50) keeps 42.9%. The published 45/35/20 weighting
sits closest to recognition-heavy — a reason to prefer it, not an arbitrary pick.

## Step 6 — tiers, recalibrated to the new population (RT-07)

Reusing v1's absolute review-count floor for "Anchor" would have made Anchor ~90% of the
list again (194/215 titles already clear 10,000 reviews once the Proven floor itself is
5,000) — the same defect RT-07 flagged, under new numbers. Recalibrated to this
population's own distribution (qualifying-list median review_total ≈ 16,200):

**Anchor** = `review_total≥20,000` OR (`metacritic_score` present AND `owners_mid≥350,000`).
**Low-cost option** = `price_usd≤$5` (annotation-driven, not composite-driven). **Depth** =
the remainder.

| Tier | n | Role |
|---|---|---|
| Anchor | 131 | Recognizable enough to lead the pitch with |
| Depth | 74 | Solid, qualifies, rounds out breadth |
| Low-cost option | 10 | Cheap regardless of composite rank — price is a cost fact, not a ranking input |

## Step 7 — monoculture check, done properly (RT-08)

The v1 check counted genre *memberships* across the top 30 (99 memberships / 30 titles =
3.3 tags each), which is arithmetically guaranteed to "span many genres" regardless of
real concentration. Fixed on three axes, computed over the full 215-title qualifying list:

- **By title, not membership:** genre shares (non-exclusive, tags overlap) — Indie 64.2%,
  Adventure 57.7%, Action 50.7%, RPG 28.4%, Simulation 20.0%, Casual 19.5%, Strategy
  13.0%, Early Access 8.4%, Racing 5.6%, Massively Multiplayer 2.3%, Sports 1.9%. No
  micro-genre dominates; Indie's high share reflects its near-universal tagging across
  the whole catalogue (documented in `01_profile.md`), not a scoring artifact.
- **Developer concentration:** maximum is **3** qualifying titles from one developer
  (Square Enix, Telltale Games) — nothing resembling v1's Randumb Studios (21 of 1,881).
  Thirteen developers place 2 titles each (Capcom, ATLUS, SEGA, DONTNOD, etc.) — healthy
  repeat-quality signal, not concentration risk.
- **Serial-chapter collapse:** grouping by (developer, heuristic base title — stripping
  trailing episode/chapter/roman-numeral/digit suffixes) collapses 215 qualifying rows to
  **213 distinct licensable properties**. Only two franchises contribute 2 qualifying rows
  each (Garfield Kart, The Walking Dead). The 5,000-review floor structurally excludes
  most low-volume serialized chapters (v1's Higurashi-at-7-rows problem) as a side effect
  of the RT-06 fix, not a separate intervention.
- **Price-band distribution** of the 215 qualifiers: $10–20 (86), $20–40 (62), $5–10 (33),
  >$40 (19), ≤$5 (15) — spread across bands, not clustered at the cheap end the way v1's
  list was (v1's top-20 median price was ~$2; v2's is $17.49).

**Verdict: not a monocolture on any of the four axes tested.**

## Top 15 by composite score

| # | app_id | name | tier | composite | reviews | owners | price | metacritic |
|---|---|---|---|---|---|---|---|---|
| 1 | 787480 | Phoenix Wright: Ace Attorney Trilogy | Anchor | 0.970 | 33,505 | 500k–1M | $29.99 | 80 |
| 2 | 1288310 | Firework | Anchor | 0.966 | 39,637 | 500k–1M | $9.99 | — |
| 3 | 1135690 | Unpacking | Anchor | 0.963 | 32,385 | 500k–1M | $19.99 | 83 |
| 4 | 1562700 | SANABI | Anchor | 0.946 | 30,102 | 500k–1M | $14.99 | — |
| 5 | 253230 | A Hat in Time | Anchor | 0.942 | 50,390 | 500k–1M | $29.99 | 79 |
| 6 | 2273430 | BlazBlue Entropy Effect | Anchor | 0.936 | 23,190 | 200k–500k | $19.99 | — |
| 7 | 2593370 | The Hungry Lamb: Traveling in the Late Ming Dynasty | Anchor | 0.929 | 38,601 | 500k–1M | $7.49 | — |
| 8 | 413420 | Danganronpa 2: Goodbye Despair | Anchor | 0.906 | 25,177 | 500k–1M | $19.99 | 83 |
| 9 | 1055540 | A Short Hike | Anchor | 0.906 | 17,323 | 200k–500k | $7.99 | 82 |
| 10 | 960170 | DJMAX RESPECT V | Anchor | 0.902 | 26,951 | 500k–1M | $49.99 | — |
| 11 | 1659420 | UNCHARTED: Legacy of Thieves Collection | Anchor | 0.895 | 24,060 | 500k–1M | $49.99 | — |
| 12 | 1256670 | Library Of Ruina | Anchor | 0.890 | 29,181 | 500k–1M | $29.99 | — |
| 13 | 1876890 | Wandering Sword | Depth | 0.888 | 19,877 | 200k–500k | $24.99 | — |
| 14 | 1880330 | Sanfu | Depth | 0.886 | 15,929 | 200k–500k | $10.99 | — |
| 15 | 1931770 | Chants of Sennaar | Anchor | 0.885 | 17,036 | 200k–500k | $12.99 | 86 |

(**Hi-Fi RUSH** — the title RT-03 used as its central example, Metacritic 90, previously
ranked 8,439 of 15,921 — is #18 at composite 0.877 in this rebuild. **What Remains of
Edith Finch** (RT-03's other flagged example, Metacritic 89, previously ranked 5,357) is
#15 at composite 0.882.)

## Confidence statement

The screen is now built on thresholds justified on their own terms (an elbow in
metacritic-presence for the review floor; an honest bucket-granularity statement for the
ownership ceiling) rather than one borrowed threshold doing double duty. The composite
verifiably encodes the brief's central tension (Recognition/Headroom Spearman +0.542, both
pillars moving the ranking) rather than cancelling it. The Fit model is honest about being
weaker than v1's (Pearson 0.38 vs 0.56) — that is the correct price of no longer
restating a measurement already in the score. The list's *membership* is far more robust
than v1's was (recognizable titles now populate the top, not the bottom); its *exact order*
is still only as reliable as a 20%-weighted, r≈0.38 model plus two directly-measured
75%-weighted pillars — good enough to rank, not good enough to defend to the decimal.

**Steam-PC → Xbox-console transfer (stated per the brief's own requirement, and per RT-11):**
this rebuild's `has_controller_support` gate addresses one dimension of console
transferability (control scheme) directly. It does not address console certification
history, regional pricing and discovery mechanics that differ between Steam and the
Microsoft Store, or the genre-mix and ~48% higher console ARPPU documented in
`artifacts/04_context.md` §5. The v2 list is materially more console-plausible than v1's
(RPG/JRPG/adventure/action titles with existing console ports and Metacritic coverage,
rather than mouse-and-keyboard interactive fiction) but this has not been independently
verified per title — that is exactly the `screen_gamepass_availability` /
console-availability check a later stage must still perform.
