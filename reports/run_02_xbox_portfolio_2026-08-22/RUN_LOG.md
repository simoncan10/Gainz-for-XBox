# Run log — portfolio run

- **Question:** Which specific games should Xbox ADD to the Game Pass portfolio?
- **Output required:** a ranked list of every title clearing a justified threshold.
- **Constraint:** all candidates must originate in the Steam snapshot. No web-sourced titles.
- **Reused from run_2026-08-22:** cleaned parquet store (validated, idempotent), profile,
  cleaning report, and external Xbox context. Stages 1-2 not re-run.

## Stage 10 — Scoring (2026-08-22)

- **Checked for `data/reference/web_indie_2025_2026.csv`** (the file the GOAL_STATEMENT
  asks Simon to settle before running) — not present anywhere on this filesystem. Decision
  recorded in DECISIONS.md: proceeded without it; no web-sourced signal was used to define
  "winning" or to supply any candidate.
- **Eligibility screen** (`sql/12_candidate_screen.sql`): not-free & price known,
  review_total>=50, review_positive_ratio>=0.70, owners_mid<=750,000, no adult-content
  tag. 122,191 non-demo games -> 15,921 eligible (13.0%).
- **Fit model** (`sql/11_fit_model_population.sql`, `scripts/11_build_fit_model.py`):
  Ridge regression predicting ln(1+review_total) from structural features only, fit on
  60,502 titles (broader than the eligible pool), validated on a 30% holdout: out-of-
  sample Pearson r=0.564 (whole holdout), r=0.527 scoped to the actual candidate
  population. Moderate, real, non-circular signal.
- **Composite score**: mean of 4 percentile ranks (proven / scarcity / fit / cheap) within
  the eligible pool. Bar set at composite>=0.60 -> 1,881 qualifying titles (1.54% of the
  whole catalogue). Full sensitivity table and weight-reweighting stability in
  `artifacts/10_model.json`.
- **Tiers** assigned by role (review_total/price rule, not a score re-slice): Anchor 538,
  Depth 487, Low-cost option 856.
- **Monoculture check**: top-30-by-composite genre mix spans 6+ genres; qualifying-list
  primary genre tops out at 20.1% (RPG). Not a monoculture.
- **Producer-level finding**: Randumb Studios (21 qualifying titles), Chilla's Art (10),
  07th Expansion (8) — repeatable-formula evidence, flagged with caveats.
- **Did NOT check Game Pass availability** — not in this dataset per the hard limits;
  every candidate row is marked `screen_gamepass_availability=PENDING_EXTERNAL_CHECK`.
- Outputs: `artifacts/10_candidates.csv` (1,881 rows), `artifacts/10_model.json`,
  `artifacts/10_model_fit.json`, `artifacts/10_scoring.md`. Queries: `sql/09_review_
  bucket_check.sql`, `sql/11_fit_model_population.sql`, `sql/12_candidate_screen.sql`,
  `sql/12b_ownership_ceiling_spotcheck.sql`, `sql/14_producer_check.sql`. Scripts:
  `scripts/11_build_fit_model.py`, `scripts/12_score_candidates.py`,
  `scripts/13_build_model_json.py`.

## Stage 11 — Red team (2026-08-22)

- Verdict on Stage 10 scoring: **REBUILD**. See `artifacts/11_redteam_scoring.md` in full.
  Fatal findings: non-deterministic pipeline (RT-01: unordered SQL + position-based train/
  test split meant the published r=0.564 reproduced in none of 3 re-runs, and model
  artifacts were never committed so the scoring script couldn't even run from a clean
  checkout); Proven/Scarcity pillars Spearman -0.762 so their average carried ~0 net
  recognition signal (RT-02); recognisable titles (Hi-Fi RUSH, A Hat in Time, Edith Finch)
  ranked in the bottom half of 15,921 (RT-03); "Cheap" pillar was a production-budget
  filter in disguise, 12x qualify-rate gap by price band (RT-04); Fit predicted the same
  quantity as Proven, adding noise not information (RT-05). Material findings: the
  review_total>=50 floor answered a different question than "recognisable" (RT-06);
  Anchor tier had no recognition condition (RT-07); monoculture check counted genre
  memberships not titles and missed a real producer/format concentration plus serialized
  chapters (RT-08); owners_mid has only 6 distinct values in the pool, the 750k/1M
  ceilings were literally identical (RT-09); reported reweighting stability used a
  statistic blind to the top of the list (RT-10); Steam-PC to Xbox transfer risk
  unaddressed (RT-11).

## Stage 12 — Scoring rebuild (2026-08-22)

- **Verified rather than trusted the coordinator-forwarded "reported yield."** Pool=926
  matches EXACTLY the count without `has_controller_support=true` applied, despite the
  rebuild spec's own bullet list instructing that gate be added; Temtem and ICARUS (both
  in the reported top-10) have `has_controller_support=false` and cannot appear in a
  gated pool. Implemented the gate literally as instructed. Documented in
  `artifacts/12_scoring_v2.md` "Step Zero" and in DECISIONS.md.
- **Determinism (RT-01) fixed and verified**: `sql/11v2_fit_model_population.sql` adds
  `ORDER BY app_id`; `scripts/11v2_build_fit_model.py` re-sorts defensively in pandas
  before every split. Two independent re-runs in this session produced identical
  eligible_pool_n (638), n_qualifying (215), and top-20 order both times. Canonical model
  artifacts committed to `artifacts/` (`_ridge_coef_v2.npy`, `_ridge_intercept_v2.txt`,
  `_feature_cols_v2.json`).
- **Screen**: review_total>=50 -> **>=5,000** (elbow in metacritic-presence, sql/17_
  threshold_sensitivity_v2.sql); owners_mid<=750,000 kept per instruction, stated honestly
  as bucket-equivalent to <=1,499,999 (only 6 distinct owners_mid values in the pool);
  added has_controller_support=true (RT-11). Pool: 122,191 -> **638** (48.0% metacritic
  presence, vs 14.4% under the v1 screen).
- **Fit model retargeted** (RT-05) from ln(1+review_total) to review_positive_ratio;
  price and is_indie_i dropped from its features. Out-of-sample Pearson r reported as a
  **range across 5 seeds: 0.377-0.388** (mean 0.384) -- much weaker than v1's 0.564, as
  expected for a harder, non-redundant target; weight cut to 20% accordingly.
- **Composite rebuilt** (RT-02, RT-04): Recognition 0.45 (ln review_total) + Headroom 0.35
  (ln review_total - ln owners_mid, replacing the cancelling Proven/Scarcity pair) + Fit
  0.20. Price removed from scoring entirely, kept as a reported/tiering-only column.
  Verified fix: Recognition/Headroom now Spearman +0.542 (was -0.762); pillar influence
  on composite Recognition 0.870 / Headroom 0.812 / Fit 0.179 (was Fit 0.540 / Proven
  0.329 / Cheap 0.263 / Scarcity 0.030 in v1).
- **Bar**: composite>=0.60 -> **215 qualifying titles** (33.7% of the 638-title pool).
  Reweighting stability reported as top-30 Jaccard overlap (RT-10), not full-pool
  Spearman: 0.875 / 0.579 / 0.429 under three alternative weightings.
- **Tiers recalibrated** to the new population's own distribution (RT-07): Anchor
  (review_total>=20,000 OR metacritic-present-and-owners>=350,000) 131, Depth 74,
  Low-cost option (price<=$5, price no longer drives rank) 10.
- **Monoculture check redone properly** (RT-08): by title not genre membership (no genre
  >65% of the list), by developer (max 3 titles, one developer), and with serial chapters
  collapsed to one licensable property per franchise (215 rows -> 213 distinct
  properties, only 2 franchises with 2+ qualifying rows). Verdict: not a monoculture on
  any axis tested.
- Top of the list now contains exactly the recognisable titles RT-03 said were missing:
  Hi-Fi RUSH (was rank 8,439/15,921, now #18/215), What Remains of Edith Finch (was
  5,357, now #15).
- Outputs: `artifacts/12_scoring_v2.md`, `artifacts/12_candidates_v2.csv` (215 rows),
  `artifacts/12_model_v2.json`, `artifacts/12_model_v2_fit.json`. v1 outputs
  (`10_scoring.md`, `10_candidates.csv`, `10_model.json`) left unchanged in place. Queries:
  `sql/11v2_fit_model_population.sql`, `sql/12v2_candidate_screen.sql`, `sql/17_threshold_
  sensitivity_v2.sql`. Scripts: `scripts/11v2_build_fit_model.py`,
  `scripts/12v2_score_candidates.py`, `scripts/13v2_build_model_json.py`.

## Stage 15 — Red team of v2 rebuild + portfolio (2026-08-22)

- Part A verdict on scoring v2: **stands narrowed.** Confirmed sound: determinism (5
  consecutive byte-identical full-pipeline re-runs, md5 `104ad4df...`), the controller
  gate (and conceded the critic's OWN Stage-11 reported yield of 926 was wrong -- 5 of its
  13 named titles including Temtem/ICARUS fail the gate it prescribed), the 5,000-review
  elbow (reproduced exactly, but sharpened: true plateau starts at 4,000), and the
  monoculture check (now genuine, correctly reports no monoculture). Narrowed: A-3
  (Headroom collapses to Recognition-minus-a-constant within every owners_mid bucket,
  Spearman=1.0000 -- the pooled +0.542 is a between-bucket artifact) and A-4 (Fit's
  in-population R^2 is -1.34, worse than the mean, yet carried 20% weight and reorders a
  third of the top 30). Part B (portfolio construction, T1-T4) separately red-teamed;
  out of scope for the scoring-stage fix that follows.

## Stage 16 — Scoring v3 (2026-08-22)

- **Scope, per explicit coordinator instruction: only A-4, A-3 (+B-5 echo), the cheap A-2
  floor fix, and the Deep Rock Galactic: Survivor data-quality check.** Part B (portfolio
  tiers T1-T4) NOT reopened.
- **A-4 fixed**: weights Recognition/Headroom/Fit changed 0.45/0.35/0.20 ->
  **0.50/0.40/0.10**. Isolated effect (pool held fixed at v2's 638): 33/638 titles'
  qualifying status changed (13.9%), 3/30 top-30 changed. Fit's composite influence drops
  to Spearman 0.04 on the final v3 pool -- now a genuine tiebreaker, not a driver.
- **A-3 verified and disclosed, not fixed (cannot be fixed):** confirmed within-bucket
  Spearman(recognition_raw, headroom_raw) = 1.0000 exactly in every owners_mid bucket with
  n>=5, on both the v2 pool (n=638) and the new v3 pool (n=802). Plain statement added to
  `artifacts/12_scoring_v2.md` (inline correction) and this stage's own
  `16_scoring_v3.md`: the composite is Recognition (continuous, 0.50-weighted) banded by
  a three-level ownership step, not a genuine multi-pillar blend. Within-tier ordering is
  "most-reviewed first."
- **B-5 echoed as a known design property** (not re-litigated in the portfolio document
  this round): 60.0% of the v3 qualifying list sits in the 750k-owner bucket vs 48.1% of
  the eligible pool -- the ceiling is close to defining, not just filtering, the list.
- **A-2 cheap fix applied**: review floor moved 5,000 -> **4,000** (verified plateau start
  via `sql/19_threshold_sensitivity_v3_fine.sql`, exact match to the critic's finer
  table). Eligible pool 638 -> **802** (47.3% metacritic presence).
- **Deep Rock Galactic: Survivor (app_id 2321470) data-quality check**: confirmed
  `has_coop=False`/`has_multiplayer=False` are CORRECT -- raw categories/tags are clean
  English with no co-op/multiplayer marker at all; not an instance of the non-English-
  metadata hazard. The base Deep Rock Galactic (548430) is correctly flagged
  co-op/multiplayer=True. The error was the downstream portfolio artifact's "co-op
  alternate" label, not this dataset's cleaning. No cleaning-stage fix logged.
- **Result: 275 qualifying titles** (was 215), tiers Anchor 157 / Depth 106 / Low-cost 12.
  Monoculture check re-run on the new pool, methodology unchanged: still not a
  monoculture (max genre share 63.3% Indie/near-universal; max developer 3 titles; 275
  rows -> 273 distinct properties after chapter-collapse).
- Outputs: `artifacts/16_scoring_v3.md`, `artifacts/16_candidates_v3.csv` (275 rows),
  `artifacts/16_model_v3.json`. v1 and v2 outputs left unchanged; `12_scoring_v2.md`
  received one inline correction block per explicit instruction. Queries:
  `sql/18_candidate_screen_v3.sql`, `sql/19_threshold_sensitivity_v3_fine.sql`. Scripts:
  `scripts/16v3_score_candidates.py`, `scripts/17v3_build_model_json.py`.

## Stage 11 — Red team of the scoring stage (2026-08-22)

- **Scope:** adversarial verification of Stage 10 (`10_scoring.md`, `10_model.json`,
  `10_model_fit.json`, `10_candidates.csv`, `sql/*.sql`, `scripts/*.py`) against the
  parquet store. Every figure re-executed, not read.
- **Reproduced exactly:** eligible pool n=15,921; qualifying n=1,881 at composite>=0.60;
  Valve review-bucket boundaries in `sql/09_review_bucket_check.sql` (Positive 10-49,
  Very Positive 50+; Mixed max ratio 0.700, Mostly Positive min 0.700).
- **Did NOT reproduce:** out-of-sample Pearson r=0.564. `sql/11_fit_model_population.sql`
  has no ORDER BY; DuckDB row order varies per run (4 runs, 4 different app_id hashes) and
  `train_test_split(random_state=42)` splits by position. Three re-runs gave r=0.5495 /
  0.5599 / 0.5506. Tier counts and top-30 genre mix also move. Additionally
  `artifacts/_ridge_coef.npy`, `_ridge_intercept.txt`, `_feature_cols.json` are absent, so
  `scripts/12_score_candidates.py` cannot be executed as shipped.
- **NOTE — artifact touched:** re-running `scripts/11_build_fit_model.py` overwrites
  `artifacts/10_model_fit.json`. The originally-published performance values were restored
  and a `_redteam_note` key added recording the overwrite and the three observed r values.
  The coefficient block in that file is from a re-run and differs from the published one.
- **Diagnosis of the obscure-titles symptom (5 fatal findings):**
  RT-01 non-determinism; RT-02 Proven/Scarcity are Spearman -0.762 so they cancel (pillar
  influence on composite: fit 0.540, proven 0.329, cheap 0.263, scarcity 0.030 — the
  brief's central tension contributes nothing to the ordering); RT-03 the recognisable
  titles are in the pool and ranked below median (Hi-Fi RUSH 8,439th; A Hat in Time
  9,968th; only 8 of the 100 most-reviewed eligible titles clear the bar; metacritic
  presence 14.4% pool vs 13.0% top-100); RT-04 "Cheap" is a production-budget filter
  (qualify rate 24.8% at <=$2 vs 2.1% at >$20, a 12x penalty, while metacritic presence
  rises 5.7%->22.5% with price); RT-05 Fit predicts ln(review_total), the same quantity
  Proven measures, and drives the rank 1.6x harder than the measurement it approximates.
- **Hypothesis tested and REJECTED:** Scarcity and Cheap do not double-count
  (Spearman +0.147). The double-counting is Proven-vs-Scarcity cancellation.
- **Material findings:** RT-06 review_total>=50 is a statistical-validity floor used as a
  recognition floor (at >=5,000 the same model returns Isonzo / Contraband Police / RAGE /
  The Room); RT-07 "Anchor" tier is 60.5% priced <=$5 and only 33.2% metacritic-scored;
  RT-08 the monoculture check counts 99 genre memberships across 30 titles so it cannot
  fail, while Randumb Studios holds 6 of the top 30 and 21 qualifiers and 20 qualifiers are
  serial chapters (Higurashi Hou alone = 7 rows); RT-09 scarcity has 6 levels with 41.6%
  tied at its own maximum, and 750k == 1M ceiling given bucket granularity; RT-10 the
  reported weight-sensitivity Spearman is blind to the top of the list (dropping Cheap
  replaces all of the top 8); RT-11 Steam->Xbox transfer is unaddressed and bites hardest
  on exactly the $2 profile the model selects.
- **Verdict: REBUILD** (not "stands narrowed"). Rebuild spec written and TESTED against the
  parquet store: raise Proven floor to review_total>=5,000, add has_controller_support
  gate, keep the 750k ownership ceiling, replace the four pillars with Recognition 0.45 /
  Headroom (ln reviews - ln owners) 0.35 / Fit 0.20, and remove price from the score
  (cost annotation + optional hard gate). Produces pool n=926 (44.2% metacritic-scored),
  320 qualifying, topped by SnowRunner, Dead Space, Marvel's Guardians of the Galaxy,
  Verdun, ICARUS, Persona 3 Reload, What Remains of Edith Finch, Journey, Lies of P,
  Temtem. All from the Steam snapshot; no web sourcing; no relaxation of the ceiling.
- **Output:** `artifacts/11_redteam_scoring.md`.

## Stage 13 — External Game Pass availability check (2026-08-22)

- **Scope:** verified, with dated external sources, Game Pass status / ownership /
  Xbox-console availability for the **top 30** ranked candidates in
  `artifacts/12_candidates_v2.csv`. No new titles introduced — exclude/annotate only, per
  GOAL_STATEMENT hard rule.
- **Structural exclusions confirmed (2 of top 30):** #11 UNCHARTED: Legacy of Thieves
  Collection — PlayStation Publishing LLC, no Xbox version exists, Sony will not license to
  a competing subscription. #26 The Outer Worlds — Microsoft already owns the IP
  (Obsidian/Xbox Game Studios; Private Division's distribution role is legacy, not
  ownership) **and** it is independently confirmed currently on Game Pass — doubly not a
  licensing decision.
- **Already-on-Game-Pass exclusions confirmed (3 of top 30, as of Aug 2026):** #6 BlazBlue
  Entropy Effect (ships on Xbox as "BlazBlue Entropy Effect X," added Feb 2026), #19 Hi-Fi
  RUSH (the flagged case — Microsoft **sold** Tango Gameworks and the Hi-Fi RUSH franchise
  to **Krafton** in Aug 2024, so it is third-party-owned now, but it remains in Game Pass
  Premium under an apparent continuing licence — nothing to acquire or license), #22 Halls
  of Torment.
- **8 confirmed rotated-out** (previously licensed, since removed — cheaper "bring-back"
  cases): Phoenix Wright: Ace Attorney Trilogy, Unpacking (left ~June 2026, very recent),
  Danganronpa 2, Library Of Ruina, What Remains of Edith Finch, Journey, Marvel's Guardians
  of the Galaxy (publisher now Embracer Group, not Square Enix — Embracer acquired
  Eidos-Montréal + IP for ~$300M in 2022), Persona 3 Reload (left Aug 15, 2025).
- **3 clean candidates** (confirmed never on Game Pass, confirmed native Xbox release, no
  blockers found): A Hat in Time, Return of the Obra Dinn, Baba Is You.
- **7 with confirmed past GP addition but unreconfirmed current status** ("unknown," not
  guessed): A Short Hike, DJMAX RESPECT V, Chants of Sennaar, ENDER LILIES, Rhythm Doctor,
  CARRION, Potion Craft, plus Firework (rank 2).
- **Console-port gap found:** #13 Wandering Sword has **no Xbox release at all** as of Aug
  2026 — console versions (PS5/Switch/Xbox Series) delayed to 21 January 2027; PC-only on
  Xbox platform today. Five more titles (SANABI, The Hungry Lamb, Sanfu, Path Of Wuxia,
  Senren＊Banka) have no evidence of any Xbox release in any source checked — flagged
  PC-only pending direct confirmation, not confirmed absent.
- **Deal-cost context (all dated, sourced):** Axios (Sept 19, 2023) reported an internal
  Xbox 2023 leak sizing day-one AAA licensing at $5M (Baldur's Gate 3) to $300M (Star Wars
  Jedi: Survivor); GTA V back-catalogue licensing ≈$12-15M/month. No dated, sourced figure
  for indie/back-catalogue-tier minimum guarantees (the tier most of this list sits in) was
  found — flagged explicitly as an unquantified input for the sizing stage, not
  extrapolated from the AAA numbers.
- **What could not be verified:** exact departure dates for 3 rotated-out titles; current
  status for 8 titles with confirmed past-but-unconfirmed-present GP inclusion; Xbox
  console existence for 6 titles; whether Journey's 2024 addition included a native Xbox
  console SKU or PC only; ranks 31+ (out of scope, not checked).
- **Outputs:** `artifacts/13_availability.md`, `artifacts/13_availability.json` (30 entries,
  one per top-30 title, each with sourced claims, dates, and confidence).

---

## Stage 14 — Portfolio synthesis (2026-08-22)

- **Inputs read in full:** `GOAL_STATEMENT.md`, `12_candidates_v2.csv` (215 qualifying),
  `12_scoring_v2.md`, `13_availability.md` + `13_availability.json` (30 entries),
  `11_redteam_scoring.md`, `04_context.md`.
- **Output: a portfolio of 24 named titles with app_ids, ranked 1–24, in four role tiers.**
  Not a framework, not an audit, not a refusal. Files: `artifacts/14_portfolio.json`
  (structured, one row per title with full provenance), `artifacts/14_portfolio.md`
  (readable), `scripts/14_build_portfolio.py` (the generator).
- **Traceability is enforced in code, not asserted in prose.** The build script joins
  `12_candidates_v2.csv` to `13_availability.json` on `app_id` and aborts if a title is
  absent from either. Every row carries its v2 rank, composite, the three pillar
  percentiles, review_total, owners bucket, Metacritic, the availability verdict, the
  blocker list and the source URLs behind that verdict.
- **Tiers, by role and by execution cost (cheapest first):**
  - **T1 Restarts (6):** Unpacking, Phoenix Wright: Ace Attorney Trilogy, Danganronpa 2,
    What Remains of Edith Finch, Library Of Ruina, Persona 3 Reload. Deals already signed
    once; ports exist; contract templates exist.
  - **T2 Clean spine (3):** A Hat in Time, Return of the Obra Dinn, Baba Is You. The only
    three confirmed never-on-GP + native-Xbox + no-blocker titles in the screened 30.
  - **T3 Confirm-then-sign breadth (8):** Chants of Sennaar, ENDER LILIES, A Short Hike,
    CARRION, Potion Craft, Firework, Rhythm Doctor, DJMAX RESPECT V.
  - **T4 Dated and PC-first options (7):** Wandering Sword (Xbox SKU dated 21 Jan 2027),
    SANABI, The Hungry Lamb, Path Of Wuxia, Sanfu, Journey, Senren＊Banka.
- **Named alternates, one per tier, all from ranks 31+ with the missing availability
  verdict stated:** Marvel's Guardians of the Galaxy (T1), ANIMAL WELL (T2, Metacritic 91),
  The Stanley Parable: Ultra Deluxe (T3), FINAL FANTASY X/X-2 HD Remaster (T4).
- **All 30 screened titles accounted for:** 24 picks + 5 stated exclusions (UNCHARTED,
  The Outer Worlds, BlazBlue Entropy Effect, Hi-Fi RUSH, Halls of Torment) + 1 alternate.
  Verified in code, not by eye.
- **The rotated-out group handled openly rather than resolved by assertion.** Argued both
  ways: deal precedent and existing ports versus the fact that a departure means either the
  publisher declined renewal (price too high) or Microsoft declined it (its own data said
  no). No source settles which, for any of the eight. Tier 1 still leads because Microsoft
  can settle the question at zero external cost from first-party data — attached as a tier
  removal RULE, never as the headline recommendation.
- **Sizing: no per-title price invented.** Used the one sourced range that spans this tier
  (MacIntyre, $50K–$50M+ across 500+ deals, TweakTown 2025-07-13, no low/high breakdown
  published) and stated that the AAA figures ($5M–$300M day-one; $12–15M/month for GTA V
  back-catalogue, Axios 2023-09-19) are the wrong order of magnitude to extrapolate from.
  Made the portfolio robust to the gap by ordering tiers on deal structure.
- **RT-04 not resurrected:** retail price does no work in the ordering, and is carried in
  the JSON only as `price_usd_retail_not_licence_cost`.
- **Weaknesses stated up front:** portfolio is Action 4/24 and multiplayer 4/24 against a
  qualifying list that is Action 50.7% and multiplayer 30.7% (n=215) — a real concentration,
  with five named co-op/multiplayer remedy titles from ranks 40–58; 20 of 24 sit in the
  500k–1M owner bucket, against the ceiling; Fit r 0.377–0.388; zero playtime data; bucketed
  owners; Steam-PC data against an Xbox-console decision (+47.3% console ARPPU, derived).
- **Decisions and six rejected portfolio structures recorded in `DECISIONS.md`, Stage 14.**

## Stage 15 — Red team of the v2 rebuild and the 24-title portfolio (2026-08-22)

- **Scope:** verify the Stage 12 rebuild landed, then attack Stage 14's portfolio. All
  figures re-executed against `parquet/` and the shipped artifacts.
- **CORRECTION AGAINST MY OWN STAGE 11 ARTIFACT — the analyst is right and I was wrong.**
  My rebuild spec listed `has_controller_support=true` as a hard gate, then reported a
  yield (pool=926) computed WITHOUT it. Verified: ungated=926, gated=638. Temtem and
  ICARUS both have has_controller_support=false and could not appear in a correctly gated
  pool; 5 of the 13 names I listed fail the gate. 638/215 are the correct numbers. The
  analyst verified rather than trusting my figure and documented the divergence properly.
- **RT-01 determinism: RESOLVED, verified beyond the claim.** Five consecutive full-pipeline
  re-runs produced byte-identical `12_candidates_v2.csv` (md5 104ad4df…) and
  `_ridge_coef_v2.npy` (md5 73b30d2b…), all matching the shipped artifact.
- **5,000-review elbow: holds, MINOR overstatement.** Published table reproduces exactly.
  Finer granularity shows the plateau begins at 4,000 (47.3%), not 5,000 — choosing 5,000
  costs 164 titles (-20%) for +0.7pp density. Defensible, not uniquely determined.
- **A-3 MATERIAL — Headroom is not an independent pillar.** Pooled Spearman(Recognition,
  Headroom)=+0.542 reproduces, but `owners_mid` has 5 distinct values in the pool with 3
  buckets holding 634/638 (99.4%). WITHIN every such bucket Spearman(rec_raw,hr_raw) =
  **1.0000** — Headroom is Recognition minus a constant. The +0.542 is between-bucket
  variation only; reporting it as complementarity is a Simpson-style artifact.
- **A-4 MATERIAL — Fit.** r=0.377–0.388 across 5 seeds reproduces, range-reporting is the
  right fix. But in-population R²=−1.34 (worse than the mean), and dropping Fit changes
  21/215 memberships and 10/30 of the top-30. Recommend cutting to 10%.
- **A-5 monoculture check: genuine and passes.** Now by-title on four axes, each able to
  fail; developer max 3 (v1: 21); 215 rows → 213 distinct properties.
- **B-1 traceability: enforcement real** (sys.exit on missing app_id, 0/24 rank mismatches),
  but "no row was typed by hand" is overstated — tier membership, ordering and rationale
  strings are hand-authored; only figures are joined.
- **Portfolio findings:** B-2 T1 leads on executability mistaken for desirability — reorder
  behind T2 (MATERIAL). B-3 exposure is unequal and the artifact UNDER-sells T3: all 8 T3
  titles have a confirmed Xbox SKU, only current-GP status is open; T4 is the real exposure
  (6/7 unverified Xbox SKU, 5 on a single source, 2 at confidence:low, and the portfolio's
  own removal rule is inoperative on them). B-4 the concentration remedy FAILS: ranks 31-60
  are identically multiplayer/co-op to ranks 1-30 (16.7%/13.3% in both), and Deep Rock
  Galactic: Survivor — 1 of the 5 named co-op alternates — has has_coop=False AND
  has_multiplayer=False. Mechanism identified: v2 Fit penalises genre_Massively Multiplayer
  (-0.0851), genre_Action (-0.0247), has_multiplayer_i (-0.0095) because retargeting onto
  review_positive_ratio made it a sentiment proxy. B-5 the ceiling is defining rather than
  filtering the portfolio (20/24 vs 63.7% in the 500k-1M bucket). B-6 $50K-$50M is a 1000x
  span quoted as a sizing anchor; the deal-structure ordering is the real answer.
- **Verdicts:** T1 stands narrowed (must not lead); T2 **stands**; T3 **stands** (stronger
  than claimed); T4 stands narrowed (relabel picks → named port-gap watchlist; headline
  becomes 17 picks + 7 watchlist). Scoring model v2: **stands narrowed** (A-3, A-4).
- **Output:** `artifacts/15_redteam_portfolio.md`.

---

## Stage 17 — Final portfolio, rebuilt on scoring v3 (2026-08-22)

- **Inputs:** `15_redteam_portfolio.md` (Part B verdicts), `16_scoring_v3.md`,
  `16_candidates_v3.csv` (275 qualifying; R 0.50 / H 0.40 / F 0.10; review floor 4,000;
  pool 802), `13_availability.json`. Outputs: `artifacts/17_portfolio_final.json`,
  `artifacts/17_portfolio_final.md`, `scripts/17_build_portfolio_final.py`.
  `14_*` left in place unchanged.
- **Headline changed per B-3: 17 named picks + a 7-title port-gap watchlist**, replacing
  v2's 24 picks. Verified in code: **17/17 picks have a confirmed native Xbox console SKU**;
  6 of the 7 watchlist entries do not, 5 rest on a single source and 2 at confidence:low.
- **Tier order changed per B-2: the clean spine leads, restarts follow.** Leading with
  rotated-out titles mistook executability for desirability; the reorder costs nothing and
  removes the strongest opening attack.
  - **T1 Clean spine (3, leads):** A Hat in Time, Return of the Obra Dinn, Baba Is You.
  - **T2 Restarts (6):** Unpacking, Phoenix Wright, What Remains of Edith Finch, Library Of
    Ruina, Danganronpa 2, Persona 3 Reload.
  - **T3 Confirm-then-sign breadth (8):** Firework, ENDER LILIES, DJMAX RESPECT V, A Short
    Hike, Potion Craft, Chants of Sennaar, CARRION, Rhythm Doctor.
  - **Watchlist (7, NOT picks):** Wandering Sword (Xbox SKU dated 21 Jan 2027), The Hungry
    Lamb, SANABI, Journey, Path Of Wuxia, Senren*Banka, Sanfu. Disciplined by a **promotion
    trigger** (two independent dated sources, or one primary) rather than a removal rule,
    because the picks' removal rule cannot be evaluated on six of them.
- **Alternates, all with their availability status stated:** ANIMAL WELL (v3 #46, MC 91,
  never screened), Marvel's Guardians of the Galaxy (v3 #18, screened), The Stanley Parable:
  Ultra Deluxe (v3 #33, never screened), FINAL FANTASY X/X-2 HD Remaster (v3 #62, never
  screened).
- **Model disclosure carried into the portfolio's opening section:** the composite is
  Recognition (0.50) banded by a three-level ownership step — within-bucket
  Spearman(recognition, headroom) = 1.0000 exactly, so the pooled +0.492 is entirely a
  between-bucket artifact. Described as a multi-pillar blend nowhere. Fit at 0.10
  (in-population R2 -1.34, measured influence Spearman 0.04) is a tiebreaker only.
- **B-4 concentration:** picks are Action 17.6% / multiplayer 17.6% / co-op 11.8% against a
  qualifying list of 53.8% / 33.5% / 24.4%. Stated as an accepted, explained property. The
  v2 "extend to rank 60" remedy is withdrawn — but measured on v3, ranks 31-60 are 23.3%
  multiplayer against v2's 16.7%, confirming that cutting Fit to 10% reduced the sentiment
  tilt. Density still only doubles past rank 60 (61-120: 38.3%). Deep Rock Galactic:
  Survivor withdrawn and the error acknowledged as ours, not the dataset's. 22 titles with
  co-op AND multiplayer flags **verified in code** are listed as the cost of a real remedy.
- **B-5 ceiling:** 60.0% of the qualifying list vs 48.1% of the pool; 15 of 17 picks in the
  top bucket. Full mechanism stated. The 200k-500k sensitivity is computed (110 of 275;
  11 of its top 15 never screened; surfaces ANIMAL WELL MC 91, Neon White MC 89, Rogue
  Legacy MC 85).
- **B-6 sizing:** the $50K-$50M line moved out of sizing into Q&A context. No per-title
  price offered; execution ordering by deal structure, never by retail price (RT-04).
- **B-1 traceability:** all ranks now derive from one method (v3 CSV position, sort asserted
  in code); the claim restated as "every figure joined, never typed; tier membership and
  rationale are authored judgments."
- **Flagged and did not pick:** Dead Space (v3 #20, MC 87) and Lies of P (v3 #21) — new to
  the v3 top 30, never availability-screened. Named as the first two titles any screen
  extension should cover.
- Objection-by-objection responses recorded in `DECISIONS.md`, Stage 17.

---

## Stage 18 — Deliverables: spoken pitch, deck, Q&A, one-pager (2026-08-22)

- **Inputs read in full:** `GOAL_STATEMENT.md`, `17_portfolio_final.json` and `.md`,
  `16_scoring_v3.md`, `15_redteam_portfolio.md`, `13_availability.md`, `04_context.md`.
- **Outputs:** `deliverables/pitch_script.md`, `deliverables/pitch_deck.pptx`,
  `deliverables/qa_prep.md`, `deliverables/portfolio_onepager.md`. Generators:
  `scripts/18_build_onepager.py` (one-pager, joined from the Stage 17 JSON) and
  `scripts/18_build_deck.js` (pptxgenjs).
- **Pitch script: 439 spoken words — 3:23 at 130 wpm, 2:56 at 150 wpm.** Stated at the top
  of the file, with per-segment counts and one marked optional cut (→ 430 words). Structure:
  hook 45 / tension 45 / evidence 105 / recommendation 114 / risk-and-ask 130.
- **Opening follows B-2's resolution:** the first words after the funnel number are
  A Hat in Time, Return of the Obra Dinn, Baba Is You — the clean spine, the only tier with
  no unanswered question. The restarts are named third, as evidence, not as the lead.
- **The red team's Q1 is raised by the speaker, unprompted, at 2:30**: "Six of these we
  already had, and gave up. Either the publisher declined to renew, or we did, on engagement
  data this analysis has never seen." Answered with the internal lookup, which is half the
  ask.
- **The ask is two items:** (1) approve the 17 as a licensing slate, worked in tier order;
  (2) authorise one internal lookup on the six prior Game Pass runs. No budget figure is
  requested, because none is defensible.
- **Traceability table at the foot of the script** lists every spoken figure with its type
  ([M]easured / [S]ourced / [D]erived) and its backing artifact, plus a second table for
  figures that appear only on slides (0.014% funnel survival; per-title review counts and
  Metacritic). A third block records **figures deliberately not spoken and why** — no
  per-title price, no engagement or retention claim, no subscriber count, no "owners as
  sales", and no description of the composite as a multi-pillar blend.
- **Honesty constraints checked against the script line by line:** the model is described
  (in Q&A only, never in the speech) as Recognition 0.50 banded by a three-level ownership
  step; Fit is named as a 0.10 tiebreaker with R2 -1.34; concentration is spoken as "under a
  fifth Action against more than half the qualifying pool" with the remedy stated as tested,
  failed and withdrawn; the Steam-PC / Xbox-console transfer is named by the speaker before
  the board can raise it.
- **Deck: 5 slides, one idea each** — the 17 with the lead three named; the funnel
  122,191 → 802 → 275 → 30 → 17; the three tiers and what each is for; the restarts, with
  the "they do not lead" objection on the same slide; the two-part ask with the standing
  caveats in one strip. Validated (`validate.py`: all passed) and visually QA'd at 110 dpi.
- **Q&A sheet: 10 questions**, opening with the red team's own three hostile questions
  (re-buy risk, concentration, ownership ceiling), then "why do you not know what these
  cost". **Two questions are answered "we cannot answer that yet"** with what would settle
  each: Q6 engagement (no playtime data exists; the internal record settles it for 6 of 17,
  nothing external settles the other 11) and Q10 the watchlist ports (settled by two
  independent dated sources or one primary; Wandering Sword has a date, 21 Jan 2027).
  Closes with a fast-reference figure card, including three figures marked **do not quote**.
- **One-pager: all 24 rows** (17 picks + 7 watchlist) with rank, title, app_id, v3 rank,
  composite, reviews, SteamSpy owners bucket, Metacritic, availability verdict and source
  count/confidence, plus per-tier removal rule, per-tier named alternate, per-title rationale
  and trigger, the excluded five, the two unscreened top-30 titles, and the standing caveats.
  Every figure is joined from `17_portfolio_final.json` by the generator, which aborts on any
  missing rank, review count, owners bucket or availability verdict, and on any unmapped
  (`on_gamepass`, `xbox_version`) pair. No numeric literal is typed into the generator.
