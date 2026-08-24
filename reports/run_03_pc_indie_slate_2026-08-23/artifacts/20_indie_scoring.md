# Stage 20 — Indie scoring: rescoped to indie + PC-eligible

Client-directed rescope, three changes. `sql/20_indie_candidate_screen.sql` is the
eligibility screen; `scripts/20_score_indie_candidates.py` builds the composite;
`artifacts/20_indie_candidates.csv` is the ranked list (138 rows); `artifacts/
20_indie_model.json` carries every threshold, sensitivity table, and diagnostic in full.
The separate thesis test (cheaper + engagement) is in `artifacts/21_indie_thesis.md` —
not repeated here.

## Change 1 — indie definition

Steam's `is_indie` genre flag alone covers **82,552 of 122,191 non-demo titles (67.6%)**
(`sql/20_indie_definition_check.sql`) — two-thirds of the whole catalogue. That is not a
segment; it is most of the store. It is also a **floor**: 87 apps are `NULL` because
their only category/genre rows are non-English (`02_cleaning_report.md`), so even the
raw flag slightly undercounts true indie titles.

**Chosen definition: `is_indie=true AND is_self_published=true`** (developer=publisher,
from SteamSpy). `is_indie` is Steam's self-declared genre tag — necessary but far too
broad alone. `is_self_published` is a structural, harder-to-game signal: no separate,
larger publisher backing the title. Combined: **44,920 titles (36.8% of the catalogue)**
— still broad in absolute terms (this catalogue skews indie throughout), but now a real,
structurally distinct segment rather than a majority label.

An alternative — `is_indie=true AND (self-published OR publisher has ≤5 titles
catalogue-wide)` — was tested and gives a similar, slightly broader pool (541 vs. 406
within the full screen). Not adopted: self-published is a clean binary requiring no
threshold; "≤5 titles" is an arbitrary cutoff this run found no principled way to set.

## Change 2 — dropped the Xbox console requirement

`has_controller_support=true` was added at Stage 12/16 specifically as a Steam-PC→
Xbox-**console** platform-fit proxy (certification, control-scheme risk). Game Pass on
PC has no such requirement. **Decision: dropped the hard gate.**

Tested three notional treatments (keep / drop / demote-to-scored-feature) and found drop
and demote are **the same outcome in practice**: the Fit model (reused unchanged from
v2/v3 per Change 3) already includes `has_controller_i` as a Ridge feature — its single
strongest positive coefficient, +0.0387. Dropping the SQL gate automatically demotes
controller support to a 10%-weighted scored input rather than eliminating its influence.

**Effect on pool size** (indie filter not yet applied, isolating the gate's own effect):
**802 → 1,179 titles (+377, +47.0%)**. Applied on top of the indie filter, dropping the
gate admits **165 titles** to the indie+self-published pool that could not have entered
before it — including Five Nights at Freddy's 2 and 4, Fran Bow, Pony Island, There Is No
Game: Wrong Dimension, Finding Paradise, and KovaaK's. This is a real cost, not free:
metacritic presence among these 165 is 25.5%, against 40.7% for the controller-supported
subset of the same pool — `has_controller_i`'s positive coefficient is picking up a
genuine signal, which is exactly why it stays in the Fit pillar rather than being dropped
too.

**On the named 7-title watchlist** (Wandering Sword, The Hungry Lamb, SANABI, Journey,
Path Of Wuxia, Senren＊Banka, Sanfu): checked directly — all seven already carry
`has_controller_support=true` and were already present in the v3 scoring list. Their
exclusion from the actual **portfolio** happened at a downstream stage (unverified Xbox
console SKU), not at this scoring gate. Dropping the console requirement removes the
*reason* that downstream exclusion existed; it does not change anything in this scoring
pool, since these titles were never blocked here.

## Change 3 — carried forward, then re-tested (not assumed)

**Review floor (4,000) and owners ceiling (750,000): both re-derived within the
indie+self-published population and kept.**

- The metacritic-presence elbow that cleanly justified 4,000 in the general population
  (Stage 16) does **not** cleanly reproduce here — the curve is flat-to-noisy from 2,000
  to 5,000 reviews (33.4% / 35.4% / 34.5% / 34.2% metacritic presence), likely because
  indie Metacritic coverage is bottlenecked by press attention, not community size. No
  floor in that range clearly dominates 4,000, so it stays.
- The 750,000 ceiling still excludes 173 of 579 indie titles (29.9%) that clear every
  other screen, and relaxing it keeps buying metacritic density (34.5%→37.0%→38.8% at
  1.5M/3.5M) at the direct cost of the "not already widely owned" test — the same
  trade-off that justified it originally still holds. Still bucket-equivalent to
  ≤1,499,999 (6 distinct `owners_mid` values remain).
- **Weights (Recognition 0.50 / Headroom 0.40 / Fit 0.10) and the Fit model itself: both
  reused verbatim, no retraining**, per explicit instruction.

**The Headroom disclosure still holds.** Re-verified on this pool (n=406, 6 distinct
`owners_mid` values): within-bucket Spearman(recognition, headroom) = **1.0000 exactly**
in every bucket with n≥5 (75,000 / 150,000 / 350,000 / 750,000). The composite remains,
honestly, **Recognition — continuous, 0.50-weighted — banded by a three-level ownership
step**, not a genuine multi-pillar blend.

## Result

**Eligible pool: 406 titles (34.5% carry a Metacritic score). Qualifying at composite ≥
0.60: 138 titles.** Of those, **48 (34.8%) have `has_controller_support=false`** and
could not have appeared under the previous (v3) screen at all — a direct, quantified
answer to "what enters that could not before."

| Tier | n | Rule |
|---|---|---|
| Anchor | 106 | review_total≥10,000 OR (metacritic present AND owners≥350,000) — recalibrated from v3's 20,000 floor, which would have left only 23/406 (5.7%) eligible given this population's lower review-volume scale (qualifying-list median ≈13,000 vs. v3's ≈16,200) |
| Depth | 16 | remainder |
| Low-cost option | 16 | price≤$10 — raised from v3's $5 to reflect indie's own lower price scale (eligible-pool median price $14.99) |

Monoculture check (methodology unchanged): Indie is 100% by definition; next-largest
genre share is Action 47.8%, Adventure 44.9% — no non-definitional monoculture. Developer
concentration: max 3 titles (Fireproof Games, Quiet River, Total Mayhem Games). 138
qualifying rows collapse to 137 distinct licensable properties (only the Five Nights at
Freddy's franchise contributes 2 rows).

## Top 20 by composite score

| # | app_id | name | tier | composite | reviews | owners | price | metacritic |
|---|---|---|---|---|---|---|---|---|
| 1 | 253230 | A Hat in Time | Anchor | 0.973 | 50,390 | 500k–1M | $29.99 | 79 |
| 2 | 2273430 | BlazBlue Entropy Effect | Anchor | 0.960 | 23,190 | 200k–500k | $19.99 | — |
| 3 | 1256670 | Library Of Ruina | Anchor | 0.935 | 29,181 | 500k–1M | $29.99 | — |
| 4 | 1189630 | Path Of Wuxia | Anchor | 0.928 | 30,091 | 500k–1M | $34.99 | — |
| 5 | 1055540 | A Short Hike | Anchor | 0.926 | 17,323 | 200k–500k | $7.99 | 82 |
| 6 | 2218750 | Halls of Torment | Anchor | 0.916 | 24,864 | 500k–1M | $4.99 | 88 |
| 7 | 241600 | Rogue Legacy | Anchor | 0.909 | 18,349 | 200k–500k | $14.99 | 85 |
| 8 | 1703340 | The Stanley Parable: Ultra Deluxe | Anchor | 0.908 | 28,048 | 500k–1M | $24.99 | — |
| 9 | 1604000 | Milk inside a bag of milk inside a bag of milk | Anchor | 0.902 | 15,928 | 200k–500k | $8.99 | — |
| 10 | 1948280 | Stacklands | Anchor | 0.902 | 24,557 | 500k–1M | $7.99 | — |
| 11 | 824270 | KovaaK's | Anchor | 0.899 | 32,859 | 200k–500k | $9.99 | — |
| 12 | 288160 | The Room | Anchor | 0.895 | 27,490 | 500k–1M | $4.99 | 73 |
| 13 | 1240210 | There Is No Game: Wrong Dimension | Anchor | 0.895 | 22,272 | 500k–1M | $12.99 | 89 |
| 14 | 425580 | The Room Two | Anchor | 0.893 | 18,916 | 200k–500k | $4.99 | — |
| 15 | 1584090 | Touhou Mystia's Izakaya | Anchor | 0.892 | 23,399 | 500k–1M | $4.79 | — |
| 16 | 406150 | Refunct | Anchor | 0.885 | 17,257 | 200k–500k | $2.99 | — |
| 17 | 2212330 | Your Only Move Is HUSTLE | Anchor | 0.884 | 25,746 | 500k–1M | $4.99 | — |
| 18 | 736260 | Baba Is You | Anchor | 0.882 | 20,757 | 500k–1M | $14.99 | 87 |
| 19 | 242860 | Verdun | Anchor | 0.881 | 37,045 | 500k–1M | $14.99 | 70 |
| 20 | 303210 | The Beginner's Guide | Anchor | 0.868 | 21,206 | 500k–1M | $9.99 | — |

(Titles 9, 11, 12, 13, 14, 17 have `has_controller_support=false` — direct examples of
what Change 2 admits that v3 could not.)

## Confidence statement

Same structure as v3: screen thresholds are now justified against the indie population
specifically (not carried over blind), the composite's real structure (Recognition banded
by a coarse ownership step, Fit a minor tiebreaker) is unchanged and re-verified. The
controller-support decision trades a measured, real quality gap (40.7% vs. 25.5%
metacritic presence) for a 47% larger pool and PC-platform correctness — a defensible
trade given Game Pass on PC does not require controller support, not a free one.
