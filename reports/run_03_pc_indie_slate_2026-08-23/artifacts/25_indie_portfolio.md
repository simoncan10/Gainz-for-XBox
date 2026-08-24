# Stage 25 — Indie Game Pass portfolio (PC-eligible scope)

**21 named indie titles, three role tiers, ordered by deal structure.** Two further screened
titles are named and deliberately **not** picked, with the case for each recorded so the
board can overturn the call knowingly.

Built on `23_indie_candidates_v2.csv` (201 qualifying) joined to `24_availability_indie.json`
(top 25 screened) by `scripts/25_build_indie_portfolio.py`, which aborts if a named title is
missing from either. Structured data: `artifacts/25_indie_portfolio.json`.

**Scope, as reset by the client:** Game Pass runs on Windows PC, so an Xbox **console** SKU
is no longer a gate. PC availability is confirmed for all 21 picks by construction of the
dataset. Console exists for **14 of 21** and is recorded as a **reach bonus**. The previous
run's port-gap watchlist is dissolved; Wandering Sword, SANABI, The Hungry Lamb, Path Of
Wuxia and Sanfu now compete on merit and five of them are picks.

---

## The investment argument, as it should be said aloud

> A subscription does not buy owners per title. It buys catalogue breadth against a fixed
> monthly fee — the thing that keeps a subscriber subscribed is having many reasons not to
> cancel. On that yardstick indie wins clearly: **63.47 qualifying titles per $1,000 against
> non-indie's 41.39, 1.53× more breadth per dollar.** Indie is genuinely cheaper — 30.1% on
> mean, 25.0% at median, across 48,682 titles — and that is the whole of the case. It is
> **not** an engagement argument: this dataset has no playtime data at all, so engagement is
> unmeasurable here in either direction, and we withdraw that half of the original thesis
> rather than soften it. We also concede the other yardstick outright: **per owner reached
> indie costs $92.81 per million against $61.93, 1.50× more expensive**, and indie reach per
> title is genuinely worse — hit-rate ratios run 72.2% at 150k owners down to 29.4% at 7.5M,
> and survivorship makes that gap wider, not narrower. Both numbers are true. They answer
> different questions. The per-slot one is the question a subscription actually asks.

**The honest erosion, which we bring into the room rather than concede cold.** Selecting the
*recognisable* top of the indie list costs most of the breadth advantage, because recognition
and price rise together. Measured on this portfolio:

| | titles per $1,000 | advantage over non-indie |
|---|---|---|
| Non-indie benchmark | 41.39 | — |
| **This portfolio (21 picks)** | **50.28** | **+21.5%** |
| Whole 201-title qualifying list | 58.62 | +41.6% |
| Indie pool benchmark | 63.47 | +53.3% |

**This portfolio retains 40% of the pool-level breadth edge.** [DERIVED: 21 picks, summed
retail $417.69; 1000 × 21 ÷ 417.69 = 50.28.] Cutting Temtem alone lifts it to 53.66.

**Caveat carried in full from the thesis: retail price is not licensing cost.** Every figure
above uses retail price as a directional proxy measured identically on both groups. They are
comparisons, not cost figures, and must not be spoken as if they were.

---

## Known property, disclosed before the ranking

**The composite is not a multi-factor blend. It is roughly 90% log review count** — pooled R²
against `ln(review_total)` alone is **0.775**, and in the top 20 `owners_mid` takes only
**two** distinct values (350,000 and 750,000). Recognition and Headroom are Spearman 1.0000
within every owners bucket, because `owners_mid` is constant inside a bucket. Headroom moves
a title between bands; it does not order it within one. [`23_indie_v2.md` A-5.]

**This disclosure is not decorative — it changed a pick.** See KovaaK's below.

---

## Tier 1 — Clean adds · 4 picks · **leads the pitch**

**Role.** Confirmed never on Game Pass, PC confirmed, no blocker, and no counterparty
carrying reported instability. They open because they are the only titles with nothing to
explain: no prior run to account for, no publisher mid-crisis, no status to check first.

| # | Title | app_id | rank | Composite | Reviews | Owners | MC | $ | Console |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A Hat in Time | 253230 | 2 | 0.9699 | **50,390** | 500k–1M | 79 | 29.99 | yes |
| 2 | Return of the Obra Dinn | 653530 | 18 | 0.9045 | 26,518 | 500k–1M | **89** | 13.39 | yes |
| 3 | Rogue Legacy | 241600 | 20 | 0.8949 | 18,349 | **200k–500k** | 85 | 14.99 | yes |
| 4 | The Stanley Parable: Ultra Deluxe | 1703340 | 24 | 0.8920 | 28,048 | 500k–1M | — | 24.99 | yes |

A Hat in Time is the highest review volume in the entire 201-title list. Obra Dinn is Lucas
Pope — a 2-title developer who develops *and* publishes, the simplest counterparty here, and
one of the canonical indies the retracted `is_self_published` rule wrongly excluded because
his label is called "3909."

**Confidence: medium-high.** 4/4 confirmed "Not Included," 4/4 PC, 4/4 console. 3 of 4 carry
Metacritic 79–89 — an independent press signal the composite never uses.

**Removal rule.** Remove if evidence of a **prior** Game Pass run surfaces — the title then
belongs in Tier 2 and must answer Tier 2's question first. **Named exposure: Rogue Legacy.**
Its "never included" verdict rests on absence of dated evidence, and its sequel Rogue Legacy
2 (a different app) has a well-documented Game Pass history that repeatedly contaminated the
search.

**Alternate: Baba Is You** (736260, rank 35, MC 87, 20,757 reviews). Alternate for one reason
only — rank 35 falls outside the Stage 24 top-25 screen, so **no availability verdict
exists.**

---

## Tier 2 — Precedent restarts · 5 picks · cheapest to execute

**Role.** Licences Microsoft has already signed once: deal struck, PC build shipped into the
service, rights holder has said yes before. **Second, not first, deliberately** — cheap to
execute is not the same as good to buy, and three of the five sit behind a publisher whose
entire staff has left.

Ordered **stable counterparty first**, so the tier can be worked in order and stopped.

| # | Title | app_id | rank | Reviews | MC | Was on GP → left | Counterparty |
|---|---|---|---|---|---|---|---|
| 5 | VA-11 Hall-A | 447530 | 6 | 34,897 | 77 | Dec 1 2020 → ~Nov 30 2021 (**PC tier**) | Ysbryd/PLAYISM — stable |
| 6 | Library Of Ruina | 1256670 | 12 | 29,181 | — | Aug 2021 → confirmed gone | ProjectMoon — stable |
| 7 | Unpacking | 1135690 | 3 | 32,385 | 83 | → **~late June 2026** | **Humble Games — distressed** |
| 8 | What Remains of Edith Finch | 501300 | 9 | 41,326 | **89** | ≥2019 → confirmed gone | **Annapurna — distressed** |
| 9 | Journey | 638230 | 13 | 32,370 | — | July 2024 (**PC tier**) → gone | **Annapurna — distressed** |

**VA-11 Hall-A and Journey are the two clearest precedents in the entire list for exactly the
PC-Game-Pass deal type this rescope asks about** — both were added and later removed as
PC-tier-specific inclusions. This exact deal shape has been done twice. Unpacking left ~two
months ago: the freshest lapsed deal and the open renewal window.

**Confidence: medium-high on executability, LOW on desirability, lower still on reachability
for three of five.** 5/5 rotated out with dated sources, 5/5 PC. Desirability is low because
no source establishes *why* any left — either the publisher declined renewal (price above
what Microsoft would pay) or Microsoft declined (its own data already said no), and nothing
external distinguishes these.

**Removal rule — two independent conditions, either sufficient.**
1. Microsoft's own record of the prior run puts the title in the bottom quartile of
   engagement per licensing dollar among comparable back-catalogue titles. *A condition on
   five named picks that stand without it — not a request to measure before deciding.*
2. **No counterparty with clear authority to grant the licence can be identified within 30
   days.**

**Alternate: ABZU** (384190, rank 40, MC 83), with an honest qualification: **no alternate
from ranks 26+ can be confirmed to *be* a restart**, because rotated-out status is only
knowable from the availability check and that check stopped at rank 25. Whether ABZU is a
restart or a clean add is precisely what screening it would determine — which is why it is
the first title to screen if a restart falls over.

---

## Tier 3 — Breadth block · 12 picks · **this tier is the investment case**

**Role.** The argument for an indie-weighted portfolio is breadth per dollar, and breadth is
delivered by title count at a quality bar, not by any single name. Twelve titles spanning
horror, metroidvania, wuxia RPG, language puzzle, crafting-sim, platformer, monster-collector
and open-world exploration — genres Tiers 1 and 2 do not cover between them.

| # | Title | app_id | rank | Reviews | Owners | MC | $ | GP status |
|---|---|---|---|---|---|---|---|---|
| 10 | Firework | 1288310 | **1** | 39,637 | 500k–1M | — | 9.99 | added Jun 2024, no dated exit |
| 11 | The Hungry Lamb | 2593370 | 4 | 38,601 | 500k–1M | — | 7.49 | no evidence either way |
| 12 | SANABI | 1562700 | 8 | 30,102 | 500k–1M | — | 14.99 | no evidence either way |
| 13 | ENDER LILIES | 1369630 | 10 | 35,018 | 500k–1M | **86** | 24.99 | no evidence either way |
| 14 | Wandering Sword | 1876890 | 11 | 19,877 | 200k–500k | — | 24.99 | no evidence either way |
| 15 | A Short Hike | 1055540 | 14 | 17,323 | 200k–500k | 82 | 7.99 | added, no dated exit |
| 16 | Path Of Wuxia | 1189630 | 15 | 30,091 | 500k–1M | — | 34.99 | no evidence either way |
| 17 | Potion Craft | 1210320 | 16 | 31,904 | 500k–1M | — | 19.99 | added, no dated exit |
| 18 | Chants of Sennaar | 1931770 | 19 | 17,036 | 200k–500k | **86** | 12.99 | added, no dated exit |
| 19 | Sanfu | 1880330 | 23 | 15,929 | 200k–500k | — | 10.99 | no evidence either way |
| 20 | CARRION | 953490 | 25 | 24,708 | 500k–1M | 75 | 19.99 | added, no dated exit |
| 21 | Temtem | 745920 | 7 | 38,583 | 500k–1M | 79 | **44.99** | none found; **Humble — distressed** |

**Wandering Sword is the clearest single illustration of what the rescope bought.** Under the
console-required scope it was the portfolio's hardest blocker — no Xbox SKU until 21 January
2027. Under PC eligibility it is available today, with console reach arriving in five months
if the date holds. The Jan 2027 slip risk is explicitly **not** a removal condition here; it
only defers the bonus.

**Temtem is ranked last on purpose and is the designated first cut for the whole portfolio.**
At $44.99 it is by a wide margin the worst titles-per-dollar contribution, and it carries the
Humble instability flag. Dropping it alone raises realised breadth from 50.28 to 53.66 per
$1,000.

Sanfu shares a developer with Firework (Shiying Studio) — one counterparty conversation
covers two picks.

**Confidence: medium on executability, medium-high on merit.** PC confirmed 12/12. 5 were
confirmed added at some point with no dated departure; 7 have no Game Pass evidence either
way. 4 of 12 carry Metacritic (75–86).

**Removal rule.** Either branch of the status check (currently included → nothing to buy;
confirmed departed → moves to Tier 2 and inherits its conditions). **Plus an aggregate
test:** remove any title whose quote pushes the tier's realised titles-per-$1,000 below
**41.39**, the non-indie benchmark. That number is what the entire investment case rests on;
a tier that fails it is not delivering the thesis.

**Alternate: Verdun** (242860, rank 26, 37,045 reviews, MC 70, `has_multiplayer=True`
verified) — the highest-composite title with no verdict, one place outside the screen, and
the top of the concentration-remedy band below.

---

## Named and deliberately NOT picked

Both sit inside the screened 25 and both would rank as picks on the composite alone. Both are
excluded on **positioning**, which the red team explicitly framed as a decision to be made
rather than a scoring by-product (`22_redteam_indie.md` A-3).

**KovaaK's** (824270, rank 22, 32,859 reviews — 4th-highest volume in the screened set,
$9.99). *For:* on composite it outranks Sanfu, The Stanley Parable and CARRION, all picks; a
cheap slot under a pure titles-per-dollar reading. *Against:* **the composite is ~90% log
review count.** A training utility accumulates review volume through a mechanism that does
not convert into what a catalogue slot is for — bought once by a large, highly motivated
competitive-FPS population and reviewed at a rate no narrative title matches. This is the
clearest case in the list where the composite's *disclosed* degeneracy produces a title the
metric likes for a reason the strategy does not share. **Excluded.**

**Milk inside a bag of milk inside a bag of milk** (1392820, rank 17, 26,566 reviews, $1.49).
*For — and this is a real tension, stated not hidden:* it is the **best titles-per-dollar
entry anywhere in the screened set**, the breadth-per-dollar thesis taken to its logical
limit. Excluding it is in genuine tension with the argument this portfolio rests on.
*Against:* (1) positioning — the opening tiers set the perceived quality of the whole
addition, and a $1.49 novelty is what a hostile board quotes back; (2) series duplication —
Milk inside (rank 17) and Milk outside (rank 28) are one licensable property contributing two
rows, so the slot contribution is smaller than the ranking implies. **Note:** the dataset has
**no playtime data**, so this document does not assert a runtime — "very short novelty" is
the client's characterisation, not a measured finding here. **Excluded, reversibly.**

**Nothing to license** (in the subscription today): BlazBlue Entropy Effect (rank 5, ships as
"Entropy Effect X"), Halls of Torment (rank 21).

*21 picks + 2 named-not-picked + 2 excluded = all 25 screened titles. Verified in code.*

---

## Counterparty instability — reasoned, not listed

Four of the strongest candidates sit behind two publishers that lost their entire staff in
2024: **Annapurna Interactive** (Edith Finch, Journey — ~24 staff resigned en masse Sept
2024, Bloomberg 2024-09-12) and **Humble Games** (Unpacking, Temtem — entire ~36-person staff
laid off July 2024, Forbes 2024-07-23; the company disputed "shutdown" and later signalled it
would keep supporting its catalogue).

**It cuts both ways, and the honest answer turns on something no source establishes.** A
distressed rights holder with a dormant catalogue and no staff may license **cheaply** — a
back-catalogue licence is close to free money against an asset nobody is working. Or it may
be **impossible to transact with at all**, because no one with signing authority is left to
answer. Crucially these are not two ends of a price range: one is cheap and one is binary,
and a binary failure cannot be priced into a bid.

**What this portfolio does about it.** It does not withdraw the four — their measured cases
are among the strongest here, and no source reports that any catalogue rights were lost, sold
or disputed. Instead: (1) the two **stable** restarts are ordered ahead of the three
distressed ones, so Tier 2 can be executed in order and stopped; (2) a **30-day
counterparty-identification condition** is written into Tier 2's removal rule, converting an
unpriceable risk into a dated go/no-go; (3) Tiers 1 and 3 are populated independently of these
publishers, so **the portfolio does not fail if all four fall over** — 17 of 21 picks are
untouched.

---

## Concentration — and this time the remedy actually works

**[MEASURED]** Picks (n=21): Action 19.0%, multiplayer 9.5%, co-op 9.5%. Qualifying list
(n=201): Action 47.3%, multiplayer 27.4%, co-op 23.4%. The gap is real.

| band | n | Action | multiplayer | co-op |
|---|---|---|---|---|
| ranks 1–25 (screened) | 25 | 28.0% | 12.0% | 12.0% |
| **ranks 26–60** | 35 | 45.7% | **40.0%** | **34.3%** |
| ranks 61–120 | 60 | 56.7% | 28.3% | 20.0% |
| ranks 121–201 | 81 | 46.9% | 25.9% | 24.7% |

**Unlike the previous run** — where the adjacent band was *identical* to the screened one on
multiplayer (16.7% in both) and the proposed remedy therefore did nothing — **the band
immediately below this screen is the multiplayer peak of the entire list.** Extending the
availability screen from rank 25 to rank 60 is a bounded ask (35 titles) that lands exactly
where the gap closes.

**14 titles with verified co-op or multiplayer flags sit in ranks 26–60**, every flag
asserted in the build script rather than trusted from a label: Verdun (#26), Deadside (#33),
Rhythm Doctor (#36), Your Only Move Is HUSTLE (#39), Streets of Rogue (#43), Children of
Morta (#47, MC 82), Crab Champions (#48), TerraTech (#50), My Time at Sandrock (#52, MC 80),
Contagion (#54), TMNT: Shredder's Revenge (#55), Trailmakers (#56), LIZARDS MUST DIE (#58),
Wobbly Life (#60). **None can be a pick today** — all sit outside the Stage 24 screen with no
availability verdict. That is the cost of closing the gap, not a gap already closed.

---

## Composition and standing caveats

**[MEASURED]** 11 of 21 picks carry Metacritic (75–89). 16 of 21 sit in the 500k–1M owner
bucket — against the ceiling, which is bucket-equivalent to 1,000,000. Max titles from one
developer: **2** (Shiying Studio). Mean price $19.89, median $19.99. Two picks lack controller
support (VA-11 Hall-A, Temtem) — playable on PC by construction; the cost is console reach,
which under this scope is a bonus, not a gate. Temtem's genre strings are Spanish in source
(`Aventura`/`Rol`/`Multijugador masivo`), a known non-English metadata case from
`02_cleaning_report.md`, which slightly understates the Action/RPG share above.

- **No engagement or playtime data exists** — every playtime column is constant zero across
  all 140,077 rows. No claim about retention or session length is made for any title.
- **Owners are bucketed SteamSpy estimates**, not measured sales. Review counts are
  self-selected.
- **Availability was screened on the top 25 only.** Every title named outside that set is
  labelled unscreened and none is a pick.
- The platform-transfer risk that dominated earlier stages is **largely dissolved by the
  rescope** — Steam PC data now targets PC Game Pass. Console ARPPU remains +47.3%
  ($81.68 ÷ $55.47 − 1; MIDiA 2024 estimates via Plarium), which is why console SKUs are
  tracked as a reach bonus.
- `release_date` is right-truncated (nothing after Oct 2024) and 20.4% missing.
- **Sizing:** no sourced indie or back-catalogue Game Pass licensing figure exists in the
  public record; none is invented and nothing is extrapolated from the AAA numbers ($5M–$300M
  day-one, $12–15M/month for GTA V; Axios 2023-09-19). The ordering is by **deal structure**,
  never by retail price — price is used only in the aggregate breadth comparison, measured
  identically on both groups, carrying that comparison's caveat.
- **Traceability:** every *figure* is joined from the two source artifacts and the build
  aborts on a missing title. Tier membership, ordering and rationale text are **authored
  judgments**.
