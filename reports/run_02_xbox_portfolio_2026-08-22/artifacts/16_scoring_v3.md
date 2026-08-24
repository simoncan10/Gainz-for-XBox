# Stage 16 — Scoring v3: reweight Fit, disclose Headroom, move the floor

`artifacts/15_redteam_portfolio.md` Part A verdict on the v2 scoring model: **stands
narrowed.** Per the coordinator's explicit scope (only Part A's two findings, plus two
cheap fixes), this document does **not** reopen Part B (the downstream portfolio/tiering
document, T1–T4) — that is a separate stage's artifact. v1 and v2 outputs are left in
place unchanged.

## Credit where due

The critic verified the Stage-12 controller-support-gate catch was correct and conceded
its own Stage-11 reported yield (pool=926) was wrong — 5 of its own 13 named titles,
including Temtem and ICARUS, fail the gate it prescribed. It also ran the full v2
pipeline **five** consecutive times and got byte-identical output every time (md5
`104ad4df…`), and independently reproduced the 5,000-review elbow exactly before
sharpening it. **638/215 stands as correct.**

## Fix 1 (A-4) — Fit cut from 20% to 10%

**Finding:** `12_model_v2_fit.json` reports the Fit model's in-population R² (scoped to
the actual eligible pool) as **−1.34** — the model predicts *worse* than simply using the
population mean. A pillar performing below a constant-prediction baseline cannot carry
20% of a ranking.

**Fix:** weights changed from Recognition 0.45 / Headroom 0.35 / Fit 0.20 to
**Recognition 0.50 / Headroom 0.40 / Fit 0.10** — the split the critic itself proposed.

**What moved,** isolating the reweight's own effect (pool held fixed at v2's 638 titles,
only the weights changed):

| | old (45/35/20) | new (50/40/10) |
|---|---|---|
| n qualifying (bar=0.60) | 215 | 228 |
| Membership changed | — | **33 of 638 titles (13.9% of the affected union)** |
| Top-30 changed | — | **3 of 30** |

This is a smaller swing than the critic's own "drop Fit entirely" test (21/215
memberships, 10/30 top-30) — expected, since cutting a weight from 20% to 10% is a
materially smaller intervention than removing it outright. Both figures are reported so
they are not conflated. Fit's measured influence on the final composite drops from
Spearman 0.18–0.54 (v2, depending on pool) to **0.04** on the final v3 pool — Fit is now
a genuine tiebreaker, not a driver.

## Fix 2 (A-3) — Headroom is not an independent pillar: verified, documented, not fixable

**Verified myself, on the exact pool the critic tested (v2, n=638):**

| owners_mid bucket | n | Spearman(recognition_raw, headroom_raw) |
|---|---|---|
| 150,000 | 31 | **1.0000** |
| 350,000 | 243 | **1.0000** |
| 750,000 | 360 | **1.0000** |

Confirmed exactly. `owners_mid` has only **5 distinct values** in the 638-title pool
(10,000 / 35,000 / 150,000 / 350,000 / 750,000), and these three buckets alone hold
**634 of 638 titles (99.4%)**. Within any one bucket, `owners_mid` is a constant, so
`headroom_raw = ln(review_total) − ln(owners_mid)` is **Recognition minus a constant** —
a title's Headroom rank inside its bucket is mechanically identical to its Recognition
rank. On the v3 pool (n=802, floor moved to 4,000) the same check holds: within-bucket
Spearman is again 1.0000 in every bucket with n≥5.

**Plain statement, as instructed:** the pooled Spearman(Recognition, Headroom) = +0.542
(v2 pool) / +0.492 (v3 pool) reported in `12_scoring_v2.md` as evidence the two pillars
are "complementary, not cancelling" is **real but entirely a between-bucket artifact** —
a Simpson's-paradox-shaped correlation produced by aggregating across a coarse step
function, not evidence of two independently-informative measurements. **The composite is
not a three-way blend. It is Recognition — a continuous, 0.50-weighted term — banded by a
three-level ownership step.** Within any given ownership tier, the ranking is
"most-reviewed first," full stop; Headroom's only real job is moving a title between the
three tiers, not ordering it within one. This is not a bug to fix — `owners_mid`'s
coarseness is a property of the underlying SteamSpy bucket data (documented since
`01_profile.md`), and no reformulation of Headroom from the same column changes it. It is
disclosed here and in `12_scoring_v2.md` (updated below) rather than papered over.

**This does not undo the v2 rebuild's core achievement** — the composite still correctly
surfaces recognisable titles at the top (Hi-Fi RUSH, A Hat in Time, Edith Finch, Obra
Dinn all remain near the top of the v3 list below). What changes is how that success
should be described: as a Recognition-led ranking with a coarse ownership pre-screen, not
as a four-pillar or even three-pillar blend.

## Related (B-5) — the ownership ceiling is close to defining the portfolio, stated as a known property

60.0% of the v3 qualifying list (275 titles) sits in the top 750,000-owner bucket, against
48.1% of the eligible pool — a real concentration, and a direct consequence of A-3: because
Recognition is continuous and weighted 0.50 (0.90 combined with Headroom) while ownership
only acts as a coarse three-level pre-screen, the model reliably selects **the most-owned
titles that still clear the ceiling**. This is stated here as a known property of the
scoring design, per the coordinator's instruction — the downstream portfolio document's
own treatment of this (B-5's suggested 200k–500k sensitivity view) is not re-derived here,
since that document is a separate stage not reopened this round.

## Cheap fix — floor moved from 5,000 to 4,000 (A-2)

Finer-grained sensitivity (500-unit steps, `sql/19_threshold_sensitivity_v3_fine.sql`,
reproducing the critic's table exactly):

| floor | 3,000 | **4,000** | 4,500 | **5,000** | 5,500 | 6,000 | 7,000 | 7,500 |
|---|---|---|---|---|---|---|---|---|
| n | 1,047 | **802** | 713 | **638** | 576 | 519 | 439 | 399 |
| metacritic % | 44.6 | **47.3** | 47.8 | **48.0** | 48.1 | 48.0 | 48.1 | 47.4 |

The plateau genuinely begins at 4,000, not 5,000 — choosing 5,000 was costing 164 titles
(−20% of the pool) for +0.7pp of metacritic density, a trade with no offsetting benefit
found. **Moved the floor to 4,000.** No other threshold changed. New eligible pool:
**802 titles, 47.3% metacritic presence.**

## Result

**Eligible pool: 802 (was 638). Qualifying list at composite ≥ 0.60: 275 titles (was
215).** Tiers (same rule as v2, unchanged): Anchor 157, Depth 106, Low-cost option 12.

Monoculture check (methodology unchanged from v2, re-run on the new pool): no genre
exceeds 63.3% of the list (Indie, near-universal per `01_profile.md`); developer
concentration max 3 titles (ATLUS, Square Enix, SEGA, Telltale Games, Total Mayhem
Games); 275 qualifying rows collapse to 273 distinct licensable properties after
chapter-collapsing (only Garfield Kart and The Walking Dead contribute 2 rows each). Not
a monoculture.

## Data-quality item: Deep Rock Galactic: Survivor — flags confirmed correct

Checked directly against the raw source data (app_id 2321470): categories are clean
English text (`Single-player`, `Full controller support`, `Family Sharing`, `Steam
Achievements`, `Steam Cloud`) with **no** Co-op or Multi-player category present, and no
Co-op/Multiplayer tag either. This is **not** an instance of the documented non-English-
metadata undercount hazard (`02_cleaning_report.md`) — the source data is neither
non-English nor ambiguous. Deep Rock Galactic: Survivor is a genuinely single-player
roguelite spin-off, distinct from the base **Deep Rock Galactic** (app_id 548430, correctly
flagged `has_coop=True`/`has_multiplayer=True`, a real 4-player co-op game). **Verdict:
the flags are correct; the downstream portfolio artifact's "co-op alternate" label was the
error, not this dataset's cleaning.** No cleaning-stage fix needed; logged here for the
record since the question was explicitly asked.

## Top 20 by composite score (v3)

| # | app_id | name | tier | composite | reviews | owners | price | metacritic |
|---|---|---|---|---|---|---|---|---|
| 1 | 1288310 | Firework | Anchor | 0.974 | 39,637 | 500k–1M | $9.99 | — |
| 2 | 787480 | Phoenix Wright: Ace Attorney Trilogy | Anchor | 0.971 | 33,505 | 500k–1M | $29.99 | 80 |
| 3 | 253230 | A Hat in Time | Anchor | 0.969 | 50,390 | 500k–1M | $29.99 | 79 |
| 4 | 1135690 | Unpacking | Anchor | 0.966 | 32,385 | 500k–1M | $19.99 | 83 |
| 5 | 2593370 | The Hungry Lamb: Traveling in the Late Ming Dynasty | Anchor | 0.956 | 38,601 | 500k–1M | $7.49 | — |
| 6 | 1562700 | SANABI | Anchor | 0.955 | 30,102 | 500k–1M | $14.99 | — |
| 7 | 2273430 | BlazBlue Entropy Effect | Anchor | 0.953 | 23,190 | 200k–500k | $19.99 | — |
| 8 | 501300 | What Remains of Edith Finch | Anchor | 0.932 | 41,326 | 500k–1M | $19.99 | 89 |
| 9 | 1369630 | ENDER LILIES: Quietus of the Knights | Anchor | 0.924 | 35,018 | 500k–1M | $24.99 | 86 |
| 10 | 960170 | DJMAX RESPECT V | Anchor | 0.924 | 26,951 | 500k–1M | $49.99 | — |
| 11 | 1256670 | Library Of Ruina | Anchor | 0.924 | 29,181 | 500k–1M | $29.99 | — |
| 12 | 1817230 | Hi-Fi RUSH | Anchor | 0.922 | 31,971 | 500k–1M | $29.99 | 90 |
| 13 | 1876890 | Wandering Sword | Depth | 0.922 | 19,877 | 200k–500k | $24.99 | — |
| 14 | 413420 | Danganronpa 2: Goodbye Despair | Anchor | 0.919 | 25,177 | 500k–1M | $19.99 | 83 |
| 15 | 638230 | Journey | Anchor | 0.919 | 32,370 | 500k–1M | $14.99 | — |
| 16 | 1055540 | A Short Hike | Anchor | 0.919 | 17,323 | 200k–500k | $7.99 | 82 |
| 17 | 1189630 | Path Of Wuxia | Anchor | 0.918 | 30,091 | 500k–1M | $34.99 | — |
| 18 | 1088850 | Marvel's Guardians of the Galaxy | Anchor | 0.917 | 35,789 | 500k–1M | $59.99 | — |
| 19 | 653530 | Return of the Obra Dinn | Anchor | 0.913 | 26,518 | 500k–1M | $13.39 | 89 |
| 20 | 1693980 | Dead Space | Anchor | 0.912 | 43,575 | 500k–1M | $59.99 | 87 |

## Confidence statement

The screen thresholds are now each justified on data-driven grounds (metacritic-presence
elbow at 4,000; bucket-equivalence of the ownership ceiling stated honestly). The
composite's real structure is now disclosed rather than overstated: it is Recognition,
weighted 0.50 and reinforced by a near-collinear Headroom term (0.40, but redundant
within any ownership tier), lightly adjusted by a Fit signal that performs below its own
population mean and is weighted accordingly (0.10). The list's membership is robust —
recognisable, well-reviewed, controller-supported titles populate the top on every
variant tested across v2 and v3. Its *within-tier ordering* should be read as "ranked by
review volume," not as evidence of a richer multi-factor model, because that is what it
now honestly is.
