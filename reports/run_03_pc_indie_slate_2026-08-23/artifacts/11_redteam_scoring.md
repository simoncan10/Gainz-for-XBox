# Stage 11 — Red team of the Stage 10 scoring model

**Verdict up front: REBUILD.** The composite score does not implement the brief. It is
arithmetically constructed so that the two pillars encoding "recognition high, ownership
low" cancel each other out, leaving a ranking driven by predicted-popularity and low price
— i.e. by low production budget. The symptom (The Confession, The Horrorscope, BBQ
Simulator at the top) is not a cosmetic ranking wobble; it is the model working exactly as
specified.

Everything below was verified by re-executing the analyst's own SQL and scripts against
`parquet/`, not by reading `10_scoring.md`. Red-team working script:
`/tmp/claude-0/-home-claude/453a9486-7e85-5dd6-b3bc-a364ccc6e6a8/scratchpad/rt.py`.

**What reproduced cleanly:** eligible pool n = 15,921 (exact); qualifying n = 1,881 at
composite ≥ 0.60 (exact); Valve's review-bucket boundaries in `sql/09_review_bucket_check.sql`
(exact — "Positive" spans review_total 10–49, "Very Positive" starts at 50; "Mixed" tops out
at ratio 0.700 and "Mostly Positive" starts at 0.700). The eligibility screen's *thresholds*
are honestly sourced. The *scoring* built on top of them is not.

---

## RT-01 — The pipeline is non-deterministic; the published r = 0.564 does not reproduce

- **Target:** `10_model_fit.json` out-of-sample Pearson r = 0.564; every downstream number
  that depends on `fit_pct` (the 1,881 count, the ranked order, the tier counts, the
  monoculture percentages).
- **Objection:** `sql/11_fit_model_population.sql` has no `ORDER BY`. DuckDB returns the
  60,502 rows in a **different order on every execution** — verified by md5-hashing the
  returned `app_id` column across four fresh connections: `4abbdc68…`, `271ffd00…`,
  `83332586…`, `e47381fa…`, four different hashes. `scripts/11_build_fit_model.py` then
  calls `train_test_split(..., random_state=42)`, which partitions **by row position**. A
  fixed seed over a shuffled input is not a fixed split. Every run therefore fits a
  different model on a different fold.
- **Severity: FATAL** (to reproducibility, and therefore to every figure in Stage 10).
- **Evidence:** three re-runs of the analyst's unmodified `scripts/11_build_fit_model.py`
  produced out-of-sample Pearson r = **0.5495 / 0.5599 / 0.5506** (R² 0.3014 / 0.3134 /
  0.3029). The published **0.564 was not reproduced in any run** and sits above the whole
  observed range. Coefficients move materially too: published `tag_Multiplayer` = 0.9666,
  re-runs = 0.9409. Scoped-to-candidate-population r published as 0.527, re-runs gave
  0.5151. Because `fit_pct` drives the composite (see RT-02), the *list itself* is not
  reproducible: my deterministic refit (rows sorted by `app_id` before the split, r =
  0.5578) yields tier counts **539 / 494 / 848** against the published **538 / 487 / 856**,
  and a top-30 genre mix of Adventure 18 / Indie 18 / Simulation 17 against the published
  Indie 19 / Adventure 18 / Simulation 16.
- **Secondary defect:** `scripts/12_score_candidates.py` reads
  `artifacts/_ridge_coef.npy`, `artifacts/_ridge_intercept.txt` and
  `artifacts/_feature_cols.json`. **None of the three exists in `artifacts/`.** The scoring
  script as shipped cannot be executed at all; `10_candidates.csv` cannot be regenerated
  from the committed artifacts.
- **Resolution:** append `ORDER BY f.app_id` to `sql/11_fit_model_population.sql` (or
  `.sort_values("app_id").reset_index(drop=True)` before `train_test_split`); commit the
  three `_ridge_*` / `_feature_cols` artifacts; re-run and republish every dependent figure.
  Until then no number in `10_scoring.md` may be spoken to a board.

> **Note on file state:** running `scripts/11_build_fit_model.py` overwrites
> `artifacts/10_model_fit.json`. My verification runs did so. I have restored the
> originally-published performance values to that file and added a `_redteam_note` key
> recording the overwrite and the three observed r values. The coefficient block in that
> file is from a re-run and differs slightly from the published one — that difference *is*
> the finding.

---

## RT-02 — Proven and Scarcity cancel; the "four-pillar" score is a two-pillar score

- **Target:** `10_scoring.md` Step 3 — "Pillars 1 and 2 pull in opposite directions by
  construction … a title strong on **both at once** is the 'punches above its weight'
  profile." And `10_model.json` `why_equal_weights`.
- **Objection:** averaging two pillars that are strongly negatively correlated does not
  reward titles strong on both — it **makes their contribution near-constant across the
  pool**, so neither influences the ordering. The brief's central tension is not encoded;
  it is annihilated. Measured in the eligible pool (n = 15,921): Spearman(proven, scarcity)
  = **−0.762**. Variance of (proven + scarcity) = **0.0381**; variance of (fit + cheap) =
  **0.0837** — more than double. Rank influence, measured directly as Spearman of each
  pillar against the composite it feeds:

  | pillar | Spearman vs composite |
  |---|---|
  | fit | **0.540** |
  | proven | 0.329 |
  | cheap | 0.263 |
  | **scarcity** | **0.030** |

  Scarcity — one of the four nominally equal 25% pillars — has essentially **zero**
  influence on the ranking. The equal-weight *label* is not the equal-weight *effect*.
- **Severity: FATAL.**
- **Evidence:** above; plus pillar lift of qualifiers over the eligible-pool mean of 0.500:
  fit **+0.223**, cheap **+0.207**, proven +0.112, scarcity +0.050. Top-100 pillar means:
  fit 0.821, cheap 0.839, proven 0.639, scarcity 0.705. The bar at 0.60 selects on fit and
  cheap.
- **Resolution:** stop averaging two negatively-correlated pillars. Encode "punches above
  its weight" as a **single ratio** — `ln(review_total) − ln(owners_mid)` (reviews per
  owner) — which is what "high recognition relative to ownership" actually means, and keep
  a separate absolute recognition term. Tested in the rebuild spec below; the two are then
  Spearman +0.331 (complementary, not cancelling).

**Hypothesis tested and rejected:** the task asked whether Scarcity and Cheap double-count
low-budget obscurity. They do not — Spearman(scarcity, cheap) = **+0.147** only. The
double-counting is Proven-against-Scarcity cancellation, not Scarcity-with-Cheap
reinforcement. Reporting this as rejected rather than quietly dropping it.

---

## RT-03 — The recognisable titles are already in the pool, and the model ranks them below the median

- **Target:** the entire ranked list; `10_scoring.md` "The list's *membership at the top*
  (Anchor tier, high composite) is far more robust than its precise order near the cutoff."
- **Objection:** the eligible pool contains exactly the titles a Game Pass board would
  expect. The composite buries them. This is the single most damaging fact in the review,
  because it removes the defence that "the data has no recognisable titles in it."
- **Severity: FATAL.**
- **Evidence** — composite rank out of 15,921 eligible:

  | title | metacritic | reviews | composite rank |
  |---|---|---|---|
  | A Hat in Time | 79 | 50,390 | **9,968** |
  | Lies of P | — | 41,414 | 8,944 |
  | Hi-Fi RUSH | **90** | 31,971 | **8,439** |
  | Unpacking | 83 | 32,385 | 8,530 |
  | Phoenix Wright: Ace Attorney Trilogy | 80 | 33,505 | 8,210 |
  | Temtem | 79 | 38,583 | 8,596 |
  | Dead Space | 87 | 43,575 | 7,729 |
  | Marvel's Guardians of the Galaxy | — | 35,789 | 7,720 |
  | ENDER LILIES | 86 | 35,018 | 7,468 |
  | What Remains of Edith Finch | 89 | 41,326 | 5,357 |

  Every one is below the pool median. **Only 8 of the 100 most-reviewed eligible titles
  clear composite ≥ 0.60** (56 of the top 500). Metacritic presence — the only
  press-coverage signal in the dataset, and one the model never uses — is 14.4% of the
  eligible pool, 13.9% of the 1,881 qualifiers, **13.0% of the top 100, and 3 of the top
  30**. The score carries no recognition signal whatsoever; if anything it is faintly
  negative. Median owners_mid falls from 35,000 (pool) to 10,000 (top 100); median price
  falls from $9.99 to $2.12.
- **Resolution:** add a recognition term the model cannot cancel (RT-02 resolution), and
  raise the Proven floor (RT-06). Both are demonstrated to work in the rebuild spec.

---

## RT-04 — "Cheap" is not a licensing-cost proxy; it is a production-budget filter

- **Target:** `10_model.json` pillar 4: "proxy for licensing cost … assumes lower retail
  price broadly correlates with lower Game Pass acquisition cost, which is a reasonable but
  unverified assumption."
- **Objection:** the assumption is not merely unverified, it is **biased in exactly the
  dimension being compared**, which is the failure mode that invalidates a proxy rather
  than merely weakening it. Retail price in this catalogue is a monotone proxy for
  production budget and press coverage. Ranking on inverse price therefore ranks on
  *absence of budget*, and does so with a ~12× selection penalty.
- **Severity: FATAL.**
- **Evidence** — eligible pool, by price band:

  | price band | n | % with metacritic | median reviews | **qualify rate** |
  |---|---|---|---|---|
  | ≤ $2 | 1,956 | 5.7% | 152 | **24.8%** |
  | $2–5 | 3,241 | 7.3% | 161 | **21.2%** |
  | $5–10 | 4,186 | 14.6% | 217 | 11.8% |
  | $10–20 | 4,817 | 19.5% | 352 | 3.7% |
  | > $20 | 1,721 | 22.5% | 864 | **2.1%** |

  Metacritic presence rises monotonically 5.7% → 22.5% with price; median review volume
  rises 152 → 864; qualify rate falls 24.8% → 2.1%. Spearman(price, review_total) = +0.293;
  Spearman(price, metacritic) = +0.197. The "Cheap" pillar is a quality-and-recognition
  penalty wearing a cost label.
- **On the proxy's own terms:** Game Pass back-catalogue deals are negotiated as minimum
  guarantees against expected subscriber engagement, which scales with recognition, not
  with sticker price. A $1.99 title with 200 reviews is not cheap to license *per
  subscriber-hour delivered*; it is cheap because nobody wants it. The proxy has the
  economics backwards.
- **Resolution:** remove price from the scored composite entirely. Carry `price_usd` as a
  **cost annotation column** on the ranked list, and, if a budget constraint is genuinely
  binding, apply it as a **hard gate** (`price_usd ≤ $X`) that the board can see and argue
  with — not as a silent 25% weight on the ordering.

---

## RT-05 — Fit is a noisy restatement of Proven, and it outranks the measurement it restates

- **Target:** `10_scoring.md` Step 2 and pillar 3; `10_model.json` "That separation (fit
  population != scoring population) is what keeps the 'what wins' signal from being a
  restatement of the screens we already apply."
- **Objection:** the out-of-sample validation the analyst relies on tests whether the model
  generalises to unseen *rows*. It cannot detect the actual circularity, which is that the
  model's **target is the same quantity as pillar 1**. Fit predicts `ln(1+review_total)`;
  Proven *is* the percentile of `ln(review_total)`. Fitting on a broader population changes
  nothing about that: the composite is averaging a measurement with an r≈0.53 prediction
  **of that same measurement**, for 15,921 titles where the measurement is observed for
  every row. Substituting a prediction for an available measurement adds noise, never
  information. And the noise wins: fit drives the ranking (Spearman 0.540) roughly 1.6×
  harder than the measured value it approximates (0.329).
- **Severity: FATAL** (to the 25% weight; the model is salvageable as a small tiebreaker).
- **Evidence:** target definition in `10_model_fit.json` (`ln(1 + review_total)`) vs. pillar
  1 definition in `scripts/12_score_candidates.py` (`pct_rank(np.log(df["review_total"]))`).
  Spearman(fit_pct, proven_pct) in the eligible pool = **+0.412** — the prediction agrees
  with the observed value only moderately, and the ranking follows the disagreement.
  Compounding this: the fit score's stated top drivers are `tag_Multiplayer` (+0.97),
  `has_controller` (+0.46), `has_coop` (+0.23) — but the actual winners are singleplayer
  $2 interactive fiction. High `fit_pct` is being earned by **lacking penalised traits**
  (`tag_3D` −0.57, `has_vr` −0.43, `is_self_pub` −0.38, `tag_Colorful` −0.36, `tag_2D`
  −0.36, `tag_Arcade` −0.35), not by possessing rewarded ones. A sparse, minimally-tagged
  text-based title scores high on "fit" by default.
- **Additional defect:** `genre_Indie` and `is_indie_i` are perfectly collinear (identical
  fitted coefficients, −0.1155 each, which is Ridge splitting one effect across two
  duplicate columns). "Indie" is therefore double-counted at −0.231 in every fit score.
- **Resolution:** either drop Fit, or retarget it at something Proven does not already
  measure — `review_positive_ratio`, or reviews-per-owner — and cap its weight at ≤20%.
  Drop `is_indie_i` (keep `genre_Indie`).

---

## RT-06 — `review_total ≥ 50` is a statistical-validity floor being used as a recognition floor

- **Target:** `sql/12_candidate_screen.sql` "This is the 'Proven' screen"; `10_scoring.md`
  Step 1 row 2.
- **Objection:** the sourcing is correct and the inference is wrong. `sql/09_review_bucket_check.sql`
  genuinely establishes 50 as Valve's boundary (verified: "Positive" spans review_total
  10–49, "Very Positive" starts at 50). But that threshold answers *"is this rating
  statistically meaningful?"* It does not answer *"would a Game Pass subscriber recognise
  this game?"* — which is the question the brief asks. The analyst imported an external
  threshold that is authoritative for a different question.
- **Severity: MATERIAL** (the screen is defensible; its use as the Proven pillar's floor is
  not).
- **Evidence** — same composite, re-run at three floors:

  | floor | pool n | n ≥ 0.60 | top of list |
  |---|---|---|---|
  | ≥ 50 | 15,921 | 1,881 | The Confession, The Horrorscope, BBQ Simulator |
  | ≥ 500 | 5,502 | 667 | Peekaboo, POSTAL Redux, Garfield Kart, CASE 2 |
  | **≥ 5,000** | **926** | **135** | Garfield Kart, Blazing Sails, Isonzo, Friends vs Friends, Lunch Lady, Contraband Police, RAGE, The Room 4: Old Sins, The Room Two |

  At ≥ 5,000 the list becomes something a board could act on — with **no other change to
  the model**. The 50-review floor is doing more damage than any single pillar.
- **Resolution:** raise the Proven floor to `review_total ≥ 5,000`, or `≥ 2,000` with an
  alternative qualifying path for titles carrying a metacritic score. State the new floor's
  justification as a *recognition* threshold in its own right, not by borrowing Valve's.

---

## RT-07 — The "Anchor" tier does not contain anchors

- **Target:** `10_scoring.md` Tiers table; `scripts/12_score_candidates.py`
  `ANCHOR_REVIEW_FLOOR = 1000` and its comment "these are the names credible enough to lead
  the pitch with."
- **Objection:** a 1,000-review floor with no ownership, price or press condition does not
  produce leadable names. The brief requires tiers readable "as a portfolio"; a board shown
  this Anchor tier will reject the label on sight.
- **Severity: MATERIAL.**
- **Evidence:** Anchor tier (n = 539 on my deterministic refit): median price **$5.00**,
  **60.5% priced ≤ $5**, only **33.2% carry any metacritic score**, **5.6% sit in the
  0–20,000 owners bucket**, median review_total 2,561. "The Horrorscope" — 1,086 reviews,
  under 20,000 owners, $1.99 — is classified **Anchor**. So is "Cats Hidden in Maple
  Hollow" (1,020 reviews, <20k owners, $0.77) and "BBQ Simulator: The Squad".
- **Resolution:** define Anchor by recognition, e.g. `review_total ≥ 10,000` **OR**
  (`metacritic_score IS NOT NULL` AND `owners_mid ≥ 200,000`). Demote price to an
  annotation; "Low-cost option" is a cost fact, not a portfolio role, and should not be a
  tier competing with the other two.

---

## RT-08 — The monoculture check is constructed so it cannot fail, and a real monoculture is present

- **Target:** `10_scoring.md` "Monoculture check … no single micro-genre dominates … tops
  out at RPG 378/1,881 (20.1%) — genuinely diverse." Brief, FORBIDDEN OUTCOMES §4 requires
  checking "whether it is a real finding or just the ranking metric restating its own
  inputs."
- **Objection:** the top-30 check counts **genre memberships**, not a distribution. The 30
  titles carry **99 genre memberships between them — 3.3 genres per title**. "Spans 6+
  genres" is therefore arithmetically guaranteed by the tagging density and proves nothing.
  Meanwhile the concentration that does exist is at the **producer and format** level,
  which a genre-only check is structurally incapable of seeing.
- **Severity: MATERIAL.**
- **Evidence:**
  - **Randumb Studios holds 6 of the top 30 and 21 of the 1,881 qualifiers.** All 21 are
    priced $1.99–$4.99; all are the same ~$2 quiz / interactive-fiction format. Twelve of
    the 21 sit in the 0–20,000 owners bucket; four have under 100 reviews (60, 69, 73, 85).
  - Full-tag counts across the top 30: **Horror 12/30, Psychological Horror 10/30, Visual
    Novel 10/30, Atmospheric 19/30, Singleplayer 19/30**. Mean price **$2.53**, max $6.29.
    That is a single micro-segment — cheap first-person horror/VN — described as diverse
    because its members carry three generic genre labels each.
  - **Catalogue fragmentation:** 20 qualifiers are episodes/chapters of a serial.
    "Higurashi When They Cry Hou" contributes **7 separate qualifying rows**; "Midnight
    Scenes" 4; "The Test", "Purrfect Apawcalypse", "Reigns", "Tomb Raider", "TT Isle of
    Man", "Bot.Vinnik Chess", "Lawnmower Game" 3 each. These are single licensable
    properties inflating the list count and the diversity denominator.
  - **The model penalises its own success stories:** Randumb's "The Test" — 19,646 reviews,
    500k–1M owners, the studio's genuine hit — scores 0.6866 and ranks *below eleven of its
    own studio's 60-to-400-review siblings*.
- **Resolution:** run the diversity check on **developer**, **price band** and **tag
  cluster** as well as genre; report the top-30 concentration as a share of *titles*, never
  of memberships; collapse serialised chapters to one row per licensable property before
  counting.

---

## RT-09 — Scarcity has six levels, 41.6% of the pool ties at its maximum, and the ceiling sensitivity table is vacuous

- **Target:** pillar 2; `10_model.json` "Eligible-pool size at ceiling = 200k/350k/**750k**/**1M**/1.5M/3.5M
  … 18,172 / **18,955** / **18,955** / 19,427" and the rationale "750,000 keeps the top of
  the 500k-1M bucket."
- **Objection:** `owners_mid` is a bucket midpoint taking **13 distinct values in the whole
  catalogue** and **6 within the eligible pool**. There is **no owners_mid value between
  750,000 and 1,500,000**, so a 750k ceiling and a 1M ceiling are *the identical cut* —
  which is why the sensitivity table reports the same 18,955 twice. The stated rationale
  describes a discrimination the data cannot make. Worse, because percentile ranks average
  ties, the most-scarce bucket receives `scarcity_pct = 0.7921` — which is simultaneously
  the **maximum achievable value** and shared by **41.6% of the pool (6,622 titles)**.
  Among bottom-bucket titles — where the entire top of the ranking lives — Scarcity is a
  **constant** and does literally no ranking work. This is the mechanism behind RT-02's
  0.030 correlation.
- **Severity: MATERIAL.**
- **Evidence:** eligible-pool scarcity levels — 0–20k → 0.792 (n=6,622); 20–50k → 0.478
  (3,369); 50–100k → 0.306 (2,110); 100–200k → 0.188 (1,639); 200–500k → 0.090 (1,494);
  500k–1M → 0.022 (687). Six values, no others.
- **Separately, what the ceiling excludes:** 888 titles pass every other screen and are cut
  by `owners_mid > 750,000`. **64.2% of them carry a metacritic score, against 14.4% of the
  eligible pool** — a 4.5× concentration of press-covered titles. Most are correctly
  excluded (Terraria at 35M owners is not a Game Pass whitespace opportunity), so this is
  not fatal on its own. But it means the recognisable stratum is thinned at the top by the
  ceiling and then buried at the bottom by the composite (RT-03), leaving the list with no
  recognisable titles anywhere.
- **Resolution:** state honestly that the ceiling is `owners_mid ≤ 750,000 ≡ ≤ 1,499,999`
  given bucket granularity. Replace the raw `−owners_mid` pillar with the reviews-per-owner
  ratio (RT-02), which uses ownership as a denominator rather than as a six-step ladder.

---

## RT-10 — The reported weight sensitivity uses a statistic blind to the part of the list that matters

- **Target:** `10_scoring.md` "**Weight sensitivity:** re-weighting toward fit (55%) leaves
  ranking largely intact (Spearman 0.75) … re-weighting toward cheap (50%) shifts it more
  (Spearman 0.56)."
- **Objection:** Spearman across 15,921 rows is dominated by the middle of the distribution
  and is nearly insensitive to reordering at the extreme — which is the only region the
  decision uses. The conclusion "largely intact" is not supported by the statistic quoted.
  Measured on the top of the list, the ranking is **completely unstable**.
- **Severity: MATERIAL.**
- **Evidence** — top 8 under alternative weightings (same pool, same fit model):

  | weighting | top of list | overlap with published top 8 |
  |---|---|---|
  | published 25/25/25/25 | The Confession, The Horrorscope, BBQ Simulator, FURRY BACKROOMS, Lawnmower Game, Chushpan Simulator, Cats Hidden…, Horrorscope: Fatal Awakening | — |
  | drop Cheap (33/33/33/0) | Golden Light, I Am Future, Youtubers Life 2, Niche, Life is Strange: Double Exposure, BattleGroupVR, The Backrooms: Survival, Folklore Hunter | **0 of 8** |
  | recognition-led (50/25/15/10) | Fear & Hunger 2: Termina, Niche, POOLS, The Confession, The Horrorscope, BBQ Simulator, POSTAL Redux, Golden Light | 3 of 8 |
  | Proven+Scarcity only (50/50) | Fear & Hunger 2: Termina, Cassette Beasts, Niche, Moonstone Island, POOLS, Röki, I Am Future, SONIC X SHADOW GENERATIONS | **0 of 8** |

  Dropping the Cheap pillar alone replaces the entire top of the list and moves the
  qualifying count from 1,881 to 4,040. The equal-weight choice, described in
  `10_model.json` as "the transparent, no-further-assumptions default," is in fact the
  single most consequential assumption in Stage 10.
- **Resolution:** report **top-30 set overlap (Jaccard)** under reweighting, not full-list
  Spearman. Any weighting scheme whose top 30 shares fewer than ~half its members with the
  alternatives has not been shown to be stable and must be justified on substance rather
  than on simplicity.

---

## RT-11 — Steam-PC → Xbox-console population transfer is unaddressed at exactly the point it bites hardest

- **Target:** `10_scoring.md` "Confidence statement"; brief, CONSTRAINTS ON HONESTY.
- **Objection:** the brief requires stating the Steam→Xbox transfer before the board does.
  `10_scoring.md`'s confidence statement discusses model r and threshold ambiguity and
  never mentions it. This is not a generic caveat: the transfer risk is **strongly
  correlated with the profile the model selects**. A $1.99 Steam interactive-fiction /
  Russian-language meme-simulator title is the *least* transferable segment in the
  catalogue to a console audience — no controller-first design guarantee, no console
  certification history, and a discovery mechanism (Steam store algorithms, review-bombing
  culture, regional pricing) that does not exist on Xbox. The model's own fit coefficients
  concede the point: `has_controller_i` is the third-strongest positive trait (+0.46), yet
  the ranking's winners are largely not controller-native.
- **Severity: MATERIAL.**
- **Resolution:** state the transfer explicitly in the scoring artifact; add
  `has_controller_support = true` as a **hard platform-fit gate** alongside the existing
  adult-content gate (it is already established as the model's third-strongest positive
  coefficient, so this is evidence-backed, not taste); report what share of the qualifying
  list survives it.

---

## RT-12 — Documentation inconsistencies (minor)

- `scripts/12_score_candidates.py` docstring, line 2: "score the eligible pool
  (sql/12_candidate_screen.sql, **n=18,955**)". The actual value is **15,921** (verified).
  18,955 is the pre-adult-content, pre-price>0 count. A reader tracing the pipeline through
  the code gets the wrong denominator.
- `10_scoring.md` quotes "r≈0.53 in-population" as the honest read; that figure is from a
  run I could not reproduce (see RT-01; re-runs gave 0.515).
- `10_scoring.md` Tiers table reports Anchor price range "$0.49–$49.99" — a range this wide
  on a tier called "Anchor" should itself have prompted the RT-07 question during Stage 10.

---

# Verdict on the scoring model: **REBUILD**

Not "stands narrowed." The screen is sound; the composite is not narrowable into
correctness because its central defect is structural — it contains no term that survives to
express recognition (RT-02), it ranks on a budget proxy mislabelled as a cost proxy
(RT-04), and it prefers a prediction of review volume over the observed review volume
(RT-05). Narrowing the claim cannot fix a score whose ordering is the opposite of what the
brief asks for.

## Precise rebuild spec — tested, not guessed

I ran the following against the same parquet store to confirm it produces a defensible
list before prescribing it.

**1. Determinism (blocking).** Add `ORDER BY f.app_id` to `sql/11_fit_model_population.sql`.
Commit `_ridge_coef.npy`, `_ridge_intercept.txt`, `_feature_cols.json` to `artifacts/`.
Republish every Stage-10 figure.

**2. Screen — change one threshold, keep the rest.**

| screen | from | to |
|---|---|---|
| paid, price > 0 | keep | keep |
| `review_positive_ratio ≥ 0.70` | keep | keep |
| adult-content tag | keep | keep |
| **`review_total ≥ 50`** | 50 | **≥ 5,000** |
| `owners_mid ≤ 750,000` | keep | keep, but document that it is `≡ ≤ 1,499,999` |
| — | — | **add `has_controller_support = true`** (RT-11) |

**3. Pillars — three, not four.**

| pillar | definition | weight |
|---|---|---|
| **Recognition** | percentile of `ln(review_total)` | **0.45** |
| **Headroom** | percentile of `ln(review_total) − ln(owners_mid)` — "punches above its weight" as one ratio, replacing the cancelling Proven/Scarcity pair | **0.35** |
| **Fit** | structural Ridge prediction, retargeted off `review_total` (use `review_positive_ratio` or reviews-per-owner), `is_indie_i` dropped | **0.20** |
| ~~Cheap~~ | **removed from scoring**; `price_usd` becomes a cost annotation column, plus a hard gate if a budget constraint is real | — |

Recognition and Headroom are Spearman **+0.331** — complementary, so both influence the
ordering (measured drivers: recognition 0.873, headroom 0.670, fit 0.389 against the
composite). Nothing cancels.

**4. Tiers.** Anchor = `review_total ≥ 10,000` OR (`metacritic_score IS NOT NULL` AND
`owners_mid ≥ 200,000`). Depth = the remainder above the bar. Delete "Low-cost option" as a
tier; carry price as a column.

**5. Hygiene.** Collapse serialised chapters to one licensable property. Run the diversity
check on developer / price band / tag cluster. Report reweighting stability as top-30
Jaccard overlap.

### What the rebuild produces — same data, same 750k ownership ceiling

Pool n = **926** (44.2% carry a metacritic score, against 14.4% under the current screen);
**320** clear a 0.60 bar. Top of the ranked list:

> SnowRunner · Dead Space · Marvel's Guardians of the Galaxy · Verdun · ICARUS · Zero Hour ·
> Hurtworld · Persona 3 Reload · What Remains of Edith Finch · Deadside · Journey ·
> Lies of P · Temtem · City Car Driving · UNCHARTED: Legacy of Thieves Collection

Every title originates in the Steam snapshot, no web sourcing, no relaxation of the
ownership ceiling. The failure was never the data.

*(For reference, relaxing the ceiling to 3.5M — a separate decision the board should make
explicitly, not one I am recommending — yields Assassin's Creed Odyssey, Battlefield 1,
Squad, Far Cry 5, Stellaris, Half-Life 2, Horizon Zero Dawn, Ready or Not, Crusader Kings
III, Dark Souls: Remastered, Spider-Man Remastered, The Last of Us Part I. Those are
arguably too widely owned to be subscription whitespace; the 750k list above is the more
defensible answer to the brief as written.)*

---

## The three questions a hostile board member will ask

1. **"You are recommending games none of us have heard of. Walk me through how a model
   asked for high recognition and low ownership put Hi-Fi RUSH — a Microsoft-published,
   Metacritic-90 title — at number 8,439 out of 15,921, behind BBQ Simulator: The Squad."**
   There is no good answer under the current model. Under the rebuild, the question does
   not arise.

2. **"A quarter of your score is inverse price, and you told us that stands in for
   licensing cost. Titles under $2 qualify at 24.8% and titles over $20 at 2.1%. Did you
   build a portfolio, or did you build a filter for games that were cheap to make?"**
   Pre-empt by removing price from the score and presenting it as a cost column the board
   can trade against recognition itself.

3. **"You re-ran this before showing it to us — did you get the same list?"**
   Currently: no. Three re-runs of the fit script gave three different models and three
   different lists, and the published r = 0.564 appeared in none of them. Fix RT-01 before
   the pitch, or this question ends the meeting.
