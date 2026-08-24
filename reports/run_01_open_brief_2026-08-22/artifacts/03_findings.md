# Stage 3 — Findings

Steam catalogue evidence for the Xbox / Game Pass investment decision (license back-catalogue vs. acquire/fund studios). All queries in `sql/1*.sql`. Every statistic below carries its own n and caveats — there is no general disclaimer at the end standing in for them.

**Standing scope limits (apply to every finding that uses them):** this dataset has **zero playtime/engagement signal** (all playtime columns are constant zero) — nothing below measures retention. `owners_mid` is a **linear midpoint of a SteamSpy bucketed range**, not a measured count; 83.2% of the catalogue sits in the single bottom bucket (0..20,000 owners), so it has almost no resolution below ~20k and every owners-based statistic is driven by the upper tail. This is **Steam PC data**; Stage 3's context establishes console ARPPU ~48% higher than PC and a genre-mix gap (PC skews shooter, Xbox console skews sports) — direct transfer to Xbox console is a stated limitation.

## F1 — Reach is extremely hit-concentrated in every major genre
Top 10% of titles by `owners_mid` capture **78–93%** of a genre's total estimated audience; **75–86%** of titles sit in the bottom SteamSpy bucket (<~20k owners).

| Genre | n | % titles in bottom bucket | % audience in top decile |
|---|---|---|---|
| Action | 50,449 | 79.6 | 86.6 |
| RPG | 23,271 | 76.8 | 84.6 |
| Strategy | 23,129 | 76.7 | 80.2 |
| Indie | 82,552 | 81.0 | 78.4 |
| Sports | 4,732 | 81.7 | 78.1 |

*Caveat:* reach/ownership concentration, not engagement. Proxy caveat applies throughout. `sql/11_reach_concentration.sql`

## F2 — Title supply has grown ~6.5x since 2015 (real, uncensored measurement)
2,487 titles (2015) → 16,050 titles (2024, 10-month partial). n=90,858 total. This count is a direct measurement, immune to right-censoring. *Caveat:* 2024 figure is right-truncated (no Nov/Dec data); 20.4% of the catalogue has no release date and is excluded. `sql/17_cohort_trend.sql`

## F3 — The apparent demand decline across cohorts is mostly a censoring artifact
Mean `owners_mid` falls from 199,630 (2015 cohort, n=2,487) to 32,096 (2023, n=15,030); median review_total falls from 147 to 11 over the same window. **Do not read this as shrinking demand for new titles** — older cohorts have simply had years longer to accumulate owners/reviews. This is the textbook right-censoring trap the brief warned against. `sql/17_cohort_trend.sql`

## F4 — A weak-but-real out-of-sample segment model already flags Xbox's own studios as outperformers
Fit/holdout method (50/50 split, never re-used): mean `owners_mid` per (primary-genre × price-band) cell fit on one half, evaluated on the unseen half. **Validation: Pearson r=0.114, Spearman-rank≈0.297, n=57,522 holdout titles** — genre+price alone are weak predictors, stated plainly. Within that model, publisher residuals (≥5 holdout titles, to exclude single-hit noise):

| Publisher | n (holdout) | Median residual (×expectation) |
|---|---|---|
| Xbox Game Studios | 32 | 5.80× |
| Bethesda Softworks | 25 | 6.23× |
| 2K | 31 | 5.12× |
| Focus Entertainment | 34 | 4.15× |

*Caveat:* residuals inherit the owners_mid proxy's coarseness and the model's weak overall fit — read as "cleared a noisy bar consistently," not a precise multiplier. This is Steam/PC performance of Xbox's existing first-party slate, not a console/Game Pass measurement. `sql/15_developer_outperformance.sql`, `sql/16_publisher_outperformance.sql`

## F5 — Distinctly-published titles outperform self-published titles, controlling for segment
Same holdout model: mean residual 1.610 (distinct publisher, n=12,594) vs 0.904 (self-published proxy, n=29,148); median 0.307 vs 0.250. *Caveat:* `is_self_published` (developer==publisher) is a proxy, not a real first/third-party field; reverse causality (publishers select projects already trending well) cannot be excluded. `sql/19_selfpublished_vs_backed.sql`

## F6 — A large licensable back-catalogue pool already exists per genre; Sports is thin on Steam
"Proven hit" bar (owners_low≥1M, review_total≥50, positive ratio≥0.7): Action has 198/217/117/42 titles across pre-2015/2015-19/2020-22/2023+ vintages. **Sports has only 31 across its entire history** — too thin to break out by vintage. *Caveat:* this likely **understates** the real sports opportunity because it's Steam/PC-only and Steam skews away from sports (see F8) — not evidence sports games underperform. Inventory count, not a licensability/cost estimate. `sql/20_licensing_candidate_inventory.sql`

## F7 — Price bands up to $30-60 associate with more reviews/audience (observational, not causal)
Median review_total: $12 (under $5, n=39,122) → $216 ($20-30, n=2,761) → $456 ($30-60, n=1,542), then collapses at $60+ (n=353, median 17 — flagged as needing more investigation, not yet a clean finding on its own). Price is confounded with budget/quality/marketing; no elasticity claim can be made. `sql/13_price_band_vs_audience.sql`

## F8 — Steam's shooter-vs-sports tag skew, confirmed directly
Shooter+FPS tags: 21,070 rows; Sports+eSports: 6,111 rows (~3.5x gap) — direct catalogue confirmation of the Stage 3 context claim about PC/console population differences. `sql/09_shooter_vs_sports_tags.sql`

## F9 (minor) — Discount depth is fairly uniform across genres
5-8.5% of paid titles on sale at the single Dec-2024 snapshot, 45-65% mean depth when discounted, no genre a clear outlier. Single point-in-time only — no frequency/calendar data exists. Not decision-relevant on its own. `sql/18_discount_depth_by_genre.sql`

## Interesting but not yet defensible
- Extreme residual ratios for developers at n=3-4 (e.g. Gas Powered Games 38.05x) — noisy given the model's weak overall fit; needs larger n before board use.
- 2023-2024 uptick in reviews-per-year-since-release looks like re-accelerating engagement but is plausibly a launch-week front-loading artifact for young cohorts; needs a stricter minimum-age cutoff to verify.
