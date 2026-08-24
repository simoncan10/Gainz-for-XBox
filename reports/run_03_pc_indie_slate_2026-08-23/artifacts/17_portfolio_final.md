# Stage 17 — Final Game Pass portfolio: 17 picks + a 7-title watchlist

Supersedes `14_portfolio.md` (kept in place). Rebuilt on **`16_candidates_v3.csv`** —
Recognition 0.50 / Headroom 0.40 / Fit 0.10, review floor 4,000, pool 802, qualifying 275.
Structured data: `artifacts/17_portfolio_final.json`. Generator:
`scripts/17_build_portfolio_final.py`.

**The recommendation:** license these **17 named back-catalogue titles** into Game Pass, in
tier order. All 17 have a **confirmed native Xbox console SKU**. Three are fully clean —
never on Game Pass, no blocker of any kind — and they open the pitch. A further seven titles
are named as a **port-gap watchlist**: they are *not* a buy list, and the document says so.

No studio acquisition, no studio funding, no pricing change, no new development.

---

## Read this before reading the ranking: how the ranking actually works

**The composite is not a multi-pillar blend, and must not be described as one.**

It is **Recognition — the percentile of `ln(review_total)`, weighted 0.50 — banded by a
three-level ownership step.** Within any one ownership band the ranking is simply
**most-reviewed first**.

Why: `owners_mid` takes only 5 distinct values, and three buckets hold nearly the entire
pool. Within every bucket `owners_mid` is a constant, so
`headroom = ln(review_total) − ln(owners_mid)` is Recognition minus a constant. Measured
**Spearman(Recognition, Headroom) = 1.0000 exactly, within every bucket.** The pooled
+0.492 that looks like complementarity is *entirely* between-bucket variation — a
Simpson-shaped artifact. Headroom's only real job is moving a title between the three bands,
not ordering it inside one. This is a SteamSpy bucket-granularity limit documented since
`01_profile.md`; no reformulation from the same column fixes it. It is disclosed, not
repaired. [Source: `16_scoring_v3.md` Fix 2.]

**Fit carries 0.10, down from 0.20**, because its in-population R² is **−1.34** — worse than
predicting the mean. Its measured influence on the v3 composite is Spearman **0.04**. It is
a tiebreaker. Nothing below rests on it.

---

## Tier 1 — Clean spine · **3 picks** · leads the pitch

**The job.** The only titles in the screened set confirmed **never** on Game Pass, confirmed
to have a native Xbox SKU, and carrying no blocker. They lead because they are the only tier
with no unanswered question attached — nothing to explain about a prior run, nothing to
check before a call is made.

| # | Title | app_id | v3 rank | Composite | Reviews | Owners | MC | Developer |
|---|---|---|---|---|---|---|---|---|
| 1 | A Hat in Time | 253230 | 3 | 0.9687 | **50,390** | 500k–1M | 79 | Gears for Breakfast |
| 2 | Return of the Obra Dinn | 653530 | 19 | 0.9129 | 26,518 | 500k–1M | **89** | Lucas Pope |
| 3 | Baba Is You | 736260 | 40 | 0.8729 | 20,757 | 500k–1M | **87** | Hempuli Oy |

A Hat in Time is the highest review volume in the screened set and the one pick carrying
co-op **and** multiplayer flags. Obra Dinn is a single-person rights holder — the simplest
counterparty anywhere in this document. Baba Is You is the portfolio's only pure puzzle
title.

**Confidence: medium-high.** 3/3 confirmed "Not Included" *and* 3/3 confirmed native Xbox
release (Stage 13, dated Aug 2026). All three carry Metacritic 79–89, an independent press
signal that is never an input to the composite.

**Removal rule.** Remove a title here if a prior Game Pass run surfaces — not because that
disqualifies it, but because it then belongs in Tier 2 and must answer Tier 2's question
first. Otherwise remove only on a refusal to license.

**Alternate: ANIMAL WELL** (813230, v3 rank 46, **Metacritic 91** — highest in the whole
qualifying list, 13,990 reviews, 200k–500k owners). Alternate for one reason only: **never
availability-screened, so no verdict exists.**

---

## Tier 2 — Restarts · **6 picks** · cheapest to execute, pending one internal check

**The job.** Re-open licences Microsoft has already signed once: the Xbox SKU shipped and
passed certification, the rights holder has said yes before, a contract template exists.

**This tier is deliberately second, not first.** Cheap to execute is not the same as good to
buy. Eight of the screened set left Game Pass, and either **the publisher declined renewal**
(the price is above what Microsoft would pay) or **Microsoft declined renewal** (its own
engagement data already returned a verdict of no). **No source establishes which, for any of
them.** Leading with these titles would present executability as desirability and hand a
hostile board its best opening question. It costs nothing to put them second.

| # | Title | app_id | v3 rank | Composite | Reviews | MC | Left Game Pass |
|---|---|---|---|---|---|---|---|
| 4 | Unpacking | 1135690 | 4 | 0.9662 | 32,385 | 83 | ~late June 2026 |
| 5 | Phoenix Wright: Ace Attorney Trilogy | 787480 | 2 | 0.9710 | 33,505 | 80 | after a Sept 2023 run |
| 6 | What Remains of Edith Finch | 501300 | 8 | 0.9316 | 41,326 | **89** | confirmed gone |
| 7 | Library Of Ruina | 1256670 | 11 | 0.9240 | 29,181 | — | confirmed gone |
| 8 | Danganronpa 2: Goodbye Despair | 413420 | 14 | 0.9195 | 25,177 | 83 | May 2023 |
| 9 | Persona 3 Reload | 2161700 | 22 | 0.9081 | 29,312 | **89** | Aug 15 2025 |

Ordered by executability, not composite. Unpacking leads despite ranking behind Phoenix
Wright because it left roughly **two months ago** — the warmest counterparty in the set, and
the one call that can be made this week. Persona 3 Reload is last on purpose: a $69.99
still-selling SKU from a large publisher is the likeliest title here to price itself out.

**Confidence: medium-high on executability, LOW on desirability.** 6/6 `rotated_out`, 6/6
Xbox SKU confirmed, every claim dated. Desirability is low because the reason for departure
is unknown in every case.

**Removal rule.** Remove any title Microsoft's own record of its prior run places in the
bottom quartile of engagement per licensing dollar among comparable back-catalogue titles.
**This is a condition attached to six named picks that stand without it** — not a request to
measure before deciding.

**Alternate: Marvel's Guardians of the Galaxy** (1088850, v3 rank 18, 35,789 reviews, Xbox
SKU confirmed). Alternate because **the counterparty changed** — Embracer bought
Eidos-Montréal and the IP from Square Enix in 2022, so the prior yes came from a company
that no longer holds the rights, and the licensed Marvel property adds a second rights
holder never screened here.

---

## Tier 3 — Confirm-then-sign breadth · **8 picks**

**The job.** Genre breadth per licensing dollar — rhythm, metroidvania, language puzzle,
horror, crafting-sim, open-world exploration — none of which Tiers 1 and 2 cover.

**This tier carries no port risk. 8/8 have a confirmed native Xbox SKU.** The only open
question is whether each is *currently* in the subscription, and that question has exactly
two answers, both already resolved by the removal rule. It is a low-risk tier, not an
uncertain one.

| # | Title | app_id | v3 rank | Composite | Reviews | Owners | MC | Genre job |
|---|---|---|---|---|---|---|---|---|
| 10 | Firework | 1288310 | **1** | **0.9740** | 39,637 | 500k–1M | — | horror-adventure |
| 11 | ENDER LILIES | 1369630 | 9 | 0.9243 | 35,018 | 500k–1M | 86 | metroidvania |
| 12 | DJMAX RESPECT V | 960170 | 10 | 0.9242 | 26,951 | 500k–1M | — | rhythm, multiplayer |
| 13 | A Short Hike | 1055540 | 16 | 0.9191 | 17,323 | **200k–500k** | 82 | open-world exploration |
| 14 | Potion Craft | 1210320 | 23 | 0.9070 | 31,904 | 500k–1M | — | crafting sim |
| 15 | Chants of Sennaar | 1931770 | 25 | 0.9062 | 17,036 | **200k–500k** | 86 | language puzzle |
| 16 | CARRION | 953490 | 30 | 0.9000 | 24,708 | 500k–1M | 75 | horror |
| 17 | Rhythm Doctor | 774181 | 43 | 0.8679 | 20,321 | 500k–1M | — | rhythm, co-op |

Firework holds the **highest composite in the entire 275-title qualifying list** and sits
here only because its current status could not be confirmed. A Short Hike and Chants of
Sennaar are the portfolio's only two picks below the top ownership bucket.

**Confidence: medium-high on executability, medium on necessity.** 4 of 8 carry Metacritic
(75–86).

**Removal rule.** Remove on either branch of the status check: currently included → nothing
to buy; confirmed departed → it moves to Tier 2 and inherits Tier 2's condition. Either way
it leaves this tier — which is exactly why the tier is low-risk.

**Alternate: The Stanley Parable: Ultra Deluxe** (1703340, v3 rank 33, 28,048 reviews).
Never availability-screened; no verdict on either its Game Pass status or its Xbox SKU.

---

## Watchlist — Port gap · **7 named titles · NOT picks**

**The job.** To be visible. These cannot be recommended for purchase because **the thing
being bought — a title playable on Xbox console — has not been shown to exist.**

**6 of 7 have an unverified Xbox SKU. Five rest on a single source. Two (The Hungry Lamb,
Senren＊Banka) carry `confidence: low`.** "No evidence found" from one low-confidence search
is not a finding. The picks' removal rule ("no Xbox SKU exists and none is dated") **cannot
be evaluated** for six of these seven — which is precisely why they are not picks.

| Title | app_id | v3 rank | Reviews | Xbox SKU evidence |
|---|---|---|---|---|
| Wandering Sword | 1876890 | 13 | 19,877 | **DATED: 21 Jan 2027** |
| The Hungry Lamb | 2593370 | 5 | 38,601 | single source, confidence low |
| SANABI | 1562700 | 6 | 30,102 | single source |
| Journey | 638230 | 15 | 32,370 | rotated out; press framed the 2024 add as *PC* Game Pass |
| Path Of Wuxia | 1189630 | 17 | 30,091 | single source |
| Senren＊Banka | 1144400 | 26 | 26,756 | single source, confidence low |
| Sanfu | 1880330 | 28 | 15,929 | single source |

**Confidence: low**, and stated as such.

**PROMOTION TRIGGER** (this tier is disciplined by promotion, not removal): a native Xbox
console SKU confirmed by **two independent dated sources, or one primary source** (publisher
or Microsoft Store listing). On confirmation the title moves to Tier 3 and competes on
merit. Absent that, it is never bought and never pitched. Wandering Sword promotes on 21 Jan
2027 if the console release ships; Journey promotes to Tier 2 if a native console SKU is
confirmed. Sanfu shares a developer with Firework (Shiying Studio), so one conversation
covers both — that efficiency is its only reason for being listed.

**Alternate: FINAL FANTASY X/X-2 HD Remaster** (359870) — a different kind of alternate: if
the board rejects the watchlist premise outright, this substitutes a large-publisher
back-catalogue title with a long-established Xbox SKU. Never screened; no verdict.

---

## Excluded, and titles that cannot be picks

**Excluded from the screened set, reason stated:** UNCHARTED: Legacy of Thieves Collection
(Sony-owned, no Xbox version — confirmed); The Outer Worlds (Microsoft owns the IP *and* it
is already on Game Pass Premium); BlazBlue Entropy Effect, Hi-Fi RUSH, Halls of Torment (all
already in the subscription).

**Top-ranked but never screened — no availability claim is made, and neither is a pick:**
**Dead Space** (v3 rank 20, 43,575 reviews, Metacritic 87) and **Lies of P** (v3 rank 21,
41,414 reviews). Both entered the v3 top 30 after the review floor moved to 4,000 and the
weights changed; Stage 13 screened the *v2* top 30 and never touched them. They are the
first two titles any screen extension should cover.

---

## Concentration — stated as an accepted property, not patched

**[MEASURED]** Picks (n=17): Action **17.6%**, multiplayer **17.6%**, co-op **11.8%**.
v3 qualifying list (n=275): Action **53.8%**, multiplayer **33.5%**, co-op **24.4%**.
The gap is real and it is not closing by itself.

**[MEASURED] By rank band (v3):**

| band | n | Action | multiplayer | co-op |
|---|---|---|---|---|
| ranks 1–30 | 30 | 33.3% | 13.3% | 10.0% |
| ranks 31–60 | 30 | 43.3% | 23.3% | 16.7% |
| ranks 61–120 | 60 | 58.3% | **38.3%** | 28.3% |
| ranks 121–275 | 155 | 58.1% | 37.4% | 27.1% |

**What changed from v2, and it is a real improvement.** In v2, ranks 31–60 were *identical*
to ranks 1–30 on multiplayer and co-op (16.7% / 13.3% in both) — which is why v2's remedy
("extend the screen to rank 60") did nothing at all. Cutting Fit from 0.20 to 0.10 reduced
the tilt: **v3 ranks 31–60 are 23.3% multiplayer against 13.3% in ranks 1–30.** The
coordinator's hypothesis is confirmed. But the gradient is still monotone and density only
**doubles past rank 60**.

**Mechanism.** Two causes. (1) Recognition carries 0.50 and review volume is highest for
singleplayer narrative titles in this pool. (2) v2's Fit model, retargeted onto
`review_positive_ratio`, became a *sentiment* proxy and penalised `genre_Massively
Multiplayer` (−0.0851), `genre_Action` (−0.0247) and `has_multiplayer` (−0.0095), because
multiplayer titles carry systematically lower positive ratios. At 0.10 weight that
distortion is much reduced, not eliminated.

**Correction carried forward.** `14_portfolio.md` named **Deep Rock Galactic: Survivor** as a
co-op alternate. Its flags are `has_coop=False` and `has_multiplayer=False`, and Stage 16
confirmed **the flags are correct** — it is a genuine single-player roguelite spin-off,
distinct from Deep Rock Galactic (548430). **The label was our error.** It is withdrawn and
appears nowhere in this portfolio.

**The position.** The concentration is an **accepted, explained property of a
Recognition-led ranking**, not a defect with a cheap fix. The only intervention that would
work is extending the availability screen to **v3 rank 120**, which is where multiplayer
density doubles; it would surface **22 titles with verified co-op *and* multiplayer flags**
(SnowRunner #35, Streets of Rogue #51, Children of Morta #60 MC 82, TMNT: Shredder's
Revenge #63, My Time at Sandrock #65 MC 80, Streets of Rage 4 #114 MC 84, Shovel Knight:
Treasure Trove #120 MC 85, and 15 more — all listed in the JSON, every flag verified in
code). **None can be a pick today because none has been availability-screened.** That is
stated as the cost of closing the gap, not offered as a gap already closed.

---

## The ownership ceiling defines the list — a known design property

**[MEASURED]** 60.0% of the v3 qualifying list sits in the top (750k) owner bucket, against
48.1% of the eligible pool. **15 of 17 picks** are in that bucket.

**Mechanism, complete.** Recognition is continuous and weighted 0.50; ownership acts only as
a **three-level step** (see the disclosure at the top), far too coarse to offset it. The
model therefore selects **the most-owned titles that still clear the ceiling** — the ceiling
*defines* the list more than it filters it. And `owners_mid ≤ 750,000` is bucket-identical
to `≤ 1,499,999`, so "not already widely owned" is being enforced at a granularity the data
cannot support.

**Sensitivity, one bucket down** (`owners_mid ≤ 500,000`): **110 of 275 titles (40.0%)**.
The top of that view is ANIMAL WELL (MC 91), Neon White (MC 89), Rogue Legacy (MC 85),
Sonic Frontiers, Refunct — **and 11 of its top 15 were never availability-screened**, so it
cannot be turned into a portfolio without extending the screen. That is the honest answer to
"did you pick these games, or did the threshold pick them?": largely the threshold, and here
is exactly what it excluded.

---

## Sizing

**There is no defensible per-title price for this tier and none is offered.** What is
offered is an **execution ordering**: commit tier by tier and stop when the quotes stop
making sense. Tier 1 needs no port. Tier 2 needs no port, no certification and no cold
introduction. Tier 3 needs one status check. The watchlist needs a port that may not exist.

The ordering basis is **deal structure** — prior deal exists / port exists / status known /
counterparty scale — **never retail price**. Stage 11 (RT-04) established that price in this
catalogue is a monotone proxy for production budget and press coverage, so ordering cost by
sticker price would resurrect the error the rebuild removed. Price appears in the JSON only
as `price_usd_retail_NOT_licence_cost` and does no ordering work.

*Q&A context, not a sizing anchor:* $50K to over $50M across 500+ deals [MacIntyre via
TweakTown, 2025-07-13]. A 1,000× span with no published breakdown excludes no possibility
and supports no budget approval, so it is not presented as one. The AAA figures ($5M–$300M
day-one; $12–15M/month for GTA V back-catalogue, Axios 2023-09-19) are the wrong order of
magnitude to extrapolate from.

---

## Standing caveats

- **No engagement or playtime data exists** — every playtime column is zero. Nothing here
  claims anything about retention or session length for any title.
- **Owners are bucketed SteamSpy estimates**, not measured sales. Review counts are
  self-selected.
- **[DERIVED] Steam PC data, Xbox console decision.** Console ARPPU is **+47.3%**
  ($81.68 ÷ $55.47 − 1 = 0.4725; inputs are MIDiA Research 2024 estimates via Plarium). The
  `has_controller_support` gate addresses control scheme only — not certification history or
  store discovery.
- `release_date` is right-truncated (nothing after Oct 2024) and 20.4% missing.
- **Availability was screened on the v2 top 30 only.** Every title here without a verdict is
  labelled as such, and none is a pick.
- **On traceability:** every *figure* in the JSON is joined from `16_candidates_v3.csv` and
  `13_availability.json` and the build aborts if a title is missing from either. All ranks
  derive from one method (position in the v3 CSV, asserted sorted). **Tier membership,
  within-tier ordering and rationale text are authored judgments**, not derived — corrected
  from `14_portfolio.md`'s overstated "no row was typed by hand."
