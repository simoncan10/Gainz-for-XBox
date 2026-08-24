# Game Pass portfolio — the board's one-pager

**17 picks + a 7-title watchlist.** Generated 2026-08-22 by `scripts/18_build_onepager.py` from `artifacts/17_portfolio_final.json`. Every figure below is joined from that file's per-title trace blocks; the build aborts if any title is missing a rank, a review count, an owners bucket or an availability verdict. Tier membership, within-tier ordering and the rationale text are **authored judgments**, not derived.

**Funnel.** 122,191 non-demo games → **802** eligible (review floor 4,000) → **275** qualifying (composite ≥ 0.60) → **30** externally availability-screened → **17** picks + **7** watchlist. 5 screened titles excluded outright.

**How the ranking works, stated correctly.** The composite is **Recognition — the percentile of ln(review_total), weight 0.50 — banded by a three-level ownership step.** It is *not* a multi-pillar blend. Within any one ownership bucket Spearman(recognition, headroom) = 1.0000 exactly, so the ranking inside a bucket is simply most-reviewed-first. Fit carries 0.10 as a tiebreaker only (in-population R² = −1.34; measured influence Spearman 0.04). Owners are **bucketed SteamSpy estimates, not sales**. There is **no engagement or playtime data** anywhere in this dataset. [`16_scoring_v3.md`]

**Two accepted properties, disclosed not patched.** *Concentration:* the 17 picks are 17.6% Action / 17.6% multiplayer / 11.8% co-op against a qualifying list of 53.8% / 33.5% / 24.4%. The tested remedy did not work and was withdrawn. *Ownership ceiling:* 15 of 17 picks sit in the top (750k) owner bucket, because a continuous 0.50-weighted Recognition term is banded only by a three-level ownership step — the ceiling defines the list more than it filters it. Full mechanism and the 200k-500k sensitivity: `17_portfolio_final.md`.

Composite and rank come from `16_candidates_v3.csv`; the availability verdict and its source count come from `13_availability.json` (screened Aug 2026).

## Tier 1 — Clean spine · 3 PICKS

**Job.** The only titles in the screened set confirmed never to have been on Game Pass, confirmed to have a native Xbox console SKU, and carrying no blocker. They open the pitch because they are the only tier with no unanswered question attached: nothing to explain about a prior run, nothing to check before a call can be made.

**Confidence:** medium-high.

| # | Title | app_id | v3 rank | Composite | Reviews | Owners (SteamSpy bucket) | MC | Availability verdict (Aug 2026) | Sources |
|---|---|---|---|---|---|---|---|---|---|
| 1 | A Hat in Time | 253230 | 3 | 0.9687 | 50,390 | 500k-1M | 79 | Never on GP · Xbox SKU confirmed | 1 (medium) |
| 2 | Return of the Obra Dinn | 653530 | 19 | 0.9129 | 26,518 | 500k-1M | 89 | Never on GP · Xbox SKU confirmed | 2 (medium) |
| 3 | Baba Is You | 736260 | 40 | 0.8729 | 20,757 | 500k-1M | 87 | Never on GP · Xbox SKU confirmed | 1 (medium) |

**REMOVAL RULE for this tier.** Remove a title here if a prior Game Pass run surfaces after all — not because a prior run disqualifies it, but because it then belongs in Tier 2 and must answer Tier 2's question first. Otherwise remove only on a refusal to license.

**Named alternate:** ANIMAL WELL (813230, v3 rank 46, 13,990 reviews, MC 91) — availability: NONE - never availability-screened.

<details><summary>Per-title rationale and removal trigger</summary>

- **A Hat in Time** (Gears for Breakfast) — 50,390 reviews, the highest volume of any title in the screened set, with Metacritic 79 and both co-op and multiplayer flags set — the one pick that cuts against the singleplayer concentration disclosed below. *Trigger:* Gears for Breakfast's console publishing partner will not grant a subscription licence separately from retail.
- **Return of the Obra Dinn** (Lucas Pope) — Metacritic 89 on 26,518 reviews, and the simplest counterparty available anywhere in the portfolio: one person (Lucas Pope) holding all rights, with the Xbox SKU already shipped. *Trigger:* Lucas Pope declines subscription placement — a solo rights holder can refuse outright and there is no second party to negotiate with.
- **Baba Is You** (Hempuli Oy) — Metacritic 87 on 20,757 reviews, and the portfolio's only pure puzzle title — the specific breadth that keeps this tier from being one narrative bet made three times. *Trigger:* Hempuli declines, or the 'Not Included' tracker verdict proves stale.

</details>

## Tier 2 — Restarts · 6 PICKS

**Job.** Re-open licences Microsoft has already signed once: the Xbox SKU shipped and passed certification, the rights holder has said yes before, and a contract template exists. This is the cheapest tier to EXECUTE. It is deliberately second, not first, because cheap to execute is not the same as good to buy — see the disclosure below.

**Confidence:** medium-high on executability, LOW on desirability.

| # | Title | app_id | v3 rank | Composite | Reviews | Owners (SteamSpy bucket) | MC | Availability verdict (Aug 2026) | Sources |
|---|---|---|---|---|---|---|---|---|---|
| 4 | Unpacking | 1135690 | 4 | 0.9662 | 32,385 | 500k-1M | 83 | Was on GP, rotated out · Xbox SKU confirmed | 2 (medium) |
| 5 | Phoenix Wright: Ace Attorney Trilogy | 787480 | 2 | 0.9710 | 33,505 | 500k-1M | 80 | Was on GP, rotated out · Xbox SKU confirmed | 4 (medium) |
| 6 | What Remains of Edith Finch | 501300 | 8 | 0.9316 | 41,326 | 500k-1M | 89 | Was on GP, rotated out · Xbox SKU confirmed | 2 (medium) |
| 7 | Library Of Ruina | 1256670 | 11 | 0.9240 | 29,181 | 500k-1M | — | Was on GP, rotated out · Xbox SKU confirmed | 2 (low) |
| 8 | Danganronpa 2: Goodbye Despair | 413420 | 14 | 0.9195 | 25,177 | 500k-1M | 83 | Was on GP, rotated out · Xbox SKU confirmed | 2 (medium) |
| 9 | Persona 3 Reload | 2161700 | 22 | 0.9081 | 29,312 | 500k-1M | 89 | Was on GP, rotated out · Xbox SKU confirmed | 2 (medium) |

**REMOVAL RULE for this tier.** Remove any title here that Microsoft's own record of its prior run places in the bottom quartile of engagement per licensing dollar among comparable back-catalogue titles. This is a condition attached to six named picks that stand without it — not a request to go and measure before deciding.

**Named alternate:** Marvel's Guardians of the Galaxy (1088850, v3 rank 18, 35,789 reviews, MC —) — availability: screened at Stage 13.

<details><summary>Per-title rationale and removal trigger</summary>

- **Unpacking** (Witch Beam) — Left Game Pass roughly two months ago (~late June 2026) — the freshest lapsed deal in the screened set, so the counterparty is warm and the renewal conversation is live now rather than cold. This is the one call that can be made this week. *Trigger:* Humble Games confirms the departure was its own decision to pursue a competing-subscription exclusive.
- **Phoenix Wright: Ace Attorney Trilogy** (CAPCOM Co., Ltd.) — v3 rank 2 on 33,505 reviews with Metacritic 80; the Xbox SKU shipped Sept 26 2023, so a re-add requires no port and no re-certification. *Trigger:* Capcom prices a re-add above a fresh licence for a comparable title, which removes the entire cost rationale for this tier.
- **What Remains of Edith Finch** (Giant Sparrow) — Metacritic 89 on 41,326 reviews — the strongest independent press signal of any rotated-out title, and press coverage is never an input to the composite. *Trigger:* Annapurna's post-2024 restructuring has left no single counterparty able to grant a console subscription licence.
- **Library Of Ruina** (ProjectMoon) — 29,181 reviews against a 500k-1M owner bucket from a single independent studio (ProjectMoon) — one rights holder, one title, one prior yes. *Trigger:* The departure cannot be pinned well enough to establish the prior deal lapsed rather than was terminated.
- **Danganronpa 2: Goodbye Despair** (Spike Chunsoft Co., Ltd., Abstraction Games) — A one-year run (May 2022 - May 2023) that reads as a fixed-term deal expiring rather than a rejection, on Metacritic 83 and 25,177 reviews. *Trigger:* Spike Chunsoft has since granted console subscription rights elsewhere.
- **Persona 3 Reload** (ATLUS) — The longest and best-documented Game Pass run in the tier — day-one Feb 2 2024 to Aug 15 2025 — on Metacritic 89. Ranked last in its tier deliberately: at a $69.99 still-selling SKU from a large publisher it is the likeliest title here to price itself out. *Trigger:* SEGA/Atlus quotes anywhere near the order of magnitude of the sourced AAA day-one figures.

</details>

## Tier 3 — Confirm-then-sign breadth · 8 PICKS

**Job.** Genre breadth per licensing dollar: rhythm, metroidvania, language puzzle, horror, crafting-sim and open-world exploration, none of which Tiers 1 and 2 cover. Every title here has a CONFIRMED Xbox console SKU; the only open question is whether it is currently in the subscription, and that question has exactly two answers, both already handled by the removal rule.

**Confidence:** medium-high on executability, medium on necessity.

| # | Title | app_id | v3 rank | Composite | Reviews | Owners (SteamSpy bucket) | MC | Availability verdict (Aug 2026) | Sources |
|---|---|---|---|---|---|---|---|---|---|
| 10 | Firework | 1288310 | 1 | 0.9740 | 39,637 | 500k-1M | — | GP status unknown · Xbox SKU confirmed | 3 (low) |
| 11 | ENDER LILIES: Quietus of the Knights | 1369630 | 9 | 0.9243 | 35,018 | 500k-1M | 86 | GP status not verified · Xbox SKU confirmed | 1 (medium) |
| 12 | DJMAX RESPECT V | 960170 | 10 | 0.9242 | 26,951 | 500k-1M | — | GP status unknown · Xbox SKU confirmed | 2 (medium) |
| 13 | A Short Hike | 1055540 | 16 | 0.9191 | 17,323 | 200k-500k | 82 | GP status unknown · Xbox SKU confirmed | 1 (high) |
| 14 | Potion Craft: Alchemist Simulator | 1210320 | 23 | 0.9070 | 31,904 | 500k-1M | — | GP status unknown · Xbox SKU confirmed | 1 (high) |
| 15 | Chants of Sennaar | 1931770 | 25 | 0.9062 | 17,036 | 200k-500k | 86 | GP status unknown · Xbox SKU confirmed | 2 (medium) |
| 16 | CARRION | 953490 | 30 | 0.9000 | 24,708 | 500k-1M | 75 | GP status unknown · Xbox SKU confirmed | 1 (high) |
| 17 | Rhythm Doctor | 774181 | 43 | 0.8679 | 20,321 | 500k-1M | — | GP status not verified · Xbox SKU confirmed | 1 (medium) |

**REMOVAL RULE for this tier.** Remove on either branch of the status check. Currently included -> nothing to buy. Confirmed departed -> it moves to Tier 2 and inherits Tier 2's condition. Either way the title leaves this tier, which is why the tier is low-risk rather than uncertain.

**Named alternate:** The Stanley Parable: Ultra Deluxe (1703340, v3 rank 33, 28,048 reviews, MC —) — availability: NONE - never availability-screened.

<details><summary>Per-title rationale and removal trigger</summary>

- **Firework** (Shiying Studio) — The highest composite in the entire 275-title v3 qualifying list (0.9740) on 39,637 reviews. It sits in Tier 3 rather than Tier 1 solely because its current subscription status could not be confirmed either way. *Trigger:* Either branch of the status check; also remove if the native Xbox SKU cannot be pinned, since Stage 13 recorded 'yes' without naming the SKU.
- **ENDER LILIES: Quietus of the Knights** (Live Wire, Adglobe) — Metacritic 86 on 35,018 reviews — the highest review volume in this tier and the portfolio's only metroidvania. *Trigger:* Either branch of the status check.
- **DJMAX RESPECT V** (NEOWIZ) — 26,951 reviews in a 500k-1M bucket. The only title in the tier whose publisher (NEOWIZ) operates at mid-size rather than indie scale, which makes it the tier's cost outlier and its first candidate for deferral. *Trigger:* Either branch of the status check; also remove if quoted at large-publisher scale, since rhythm breadth is already served by Rhythm Doctor at a fraction of the counterparty size.
- **A Short Hike** (adamgryu) — Metacritic 82 on 17,323 reviews in the 200k-500k owner bucket — the 'recognised but not widely owned' profile the brief asks for, at its purest, and one of only two picks below the top ownership bucket. *Trigger:* Either branch of the status check.
- **Potion Craft: Alchemist Simulator** (niceplay games) — 31,904 reviews in a crafting/simulation genre no other portfolio title covers. *Trigger:* Either branch of the status check.
- **Chants of Sennaar** (Rundisc) — Metacritic 86 on 17,036 reviews at $12.99, in the 200k-500k bucket, occupying a language-puzzle genre nothing else in the portfolio touches. *Trigger:* Either branch of the status check.
- **CARRION** (Phobia Game Studio) — 24,708 reviews with Metacritic 75 — the portfolio's only horror title, a genre Tiers 1 and 2 have none of. *Trigger:* Either branch of the status check; Metacritic 75 is the weakest press score in the portfolio, so it is also the first cut if the tier must shrink.
- **Rhythm Doctor** (7th Beat Games) — 20,321 reviews with co-op and multiplayer flags set — one of only two picks in the whole portfolio that is played socially, which matters given the concentration disclosed below. *Trigger:* Either branch of the status check; still flagged Early Access in the dataset, so remove if the console SKU is not a finished release.

</details>

## Tier 4 — Port-gap watchlist · 7 WATCHLIST — NOT PICKS

**Job.** NOT picks. Seven high-scoring titles that cannot be recommended for purchase because the thing being bought — a title playable on Xbox console — has not been shown to exist. They are named and kept visible so the board sees what it is choosing not to chase, and so a single confirmation can promote any of them.

**Confidence:** low.

| # | Title | app_id | v3 rank | Composite | Reviews | Owners (SteamSpy bucket) | MC | Availability verdict (Aug 2026) | Sources |
|---|---|---|---|---|---|---|---|---|---|
| 18 | Wandering Sword | 1876890 | 13 | 0.9221 | 19,877 | 200k-500k | — | GP not verified · **no Xbox SKU today** | 2 (medium) |
| 19 | The Hungry Lamb: Traveling in the Late Ming Dynasty | 2593370 | 5 | 0.9556 | 38,601 | 500k-1M | — | GP not verified · **Xbox SKU NOT verified** | 1 (low) |
| 20 | SANABI | 1562700 | 6 | 0.9546 | 30,102 | 500k-1M | — | GP not verified · **Xbox SKU NOT verified** | 1 (medium) |
| 21 | Journey | 638230 | 15 | 0.9192 | 32,370 | 500k-1M | — | Was on GP (framed as PC) · **Xbox SKU NOT verified** | 2 (medium) |
| 22 | Path Of Wuxia | 1189630 | 17 | 0.9179 | 30,091 | 500k-1M | — | GP not verified · **Xbox SKU NOT verified** | 1 (medium) |
| 23 | Senren＊Banka | 1144400 | 26 | 0.9047 | 26,756 | 500k-1M | — | GP not verified · **Xbox SKU NOT verified** | 1 (low) |
| 24 | Sanfu | 1880330 | 28 | 0.9018 | 15,929 | 200k-500k | — | GP not verified · **Xbox SKU NOT verified** | 1 (medium) |

**PROMOTION TRIGGER for this tier.** This tier's discipline is a PROMOTION trigger, not a removal rule, because the removal rule that governs the picks ('no Xbox SKU exists and none is dated') cannot even be evaluated for six of these seven. PROMOTION TRIGGER: a native Xbox console SKU confirmed by two independent dated sources, or one primary source (publisher or Microsoft Store listing). On confirmation the title moves to Tier 3 and competes on merit. Absent that, it is never bought and never pitched.

**Named alternate:** FINAL FANTASY X/X-2 HD Remaster (359870, v3 rank 62, 18,632 reviews, MC —) — availability: NONE - never availability-screened.

<details><summary>Per-title rationale and removal trigger</summary>

- **Wandering Sword** (The Swordman Studio) — The only positively established gap in the set: the Xbox Series version is DATED to 21 January 2027. That makes it a diary entry with a known date rather than an open question, on 19,877 reviews. *Trigger:* Promotes on 21 Jan 2027 if the console release ships; drops off if the date slips again, at which point it is open-ended rather than diarisable.
- **The Hungry Lamb: Traveling in the Late Ming Dynasty** (零创游戏(ZerocreationGame)) — 38,601 reviews at $7.49 — the highest review volume and the lowest price in the set, so the cheapest possible test of whether this segment transfers at all. *Trigger:* Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source at confidence:'low'.
- **SANABI** (WONDER POTION) — v3 rank 6, composite 0.9546 — the highest-scoring title anywhere in this document with no confirmed Xbox SKU, which is exactly why the port question is worth one call. *Trigger:* Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source.
- **Journey** (thatgamecompany) — The only entry that is both a restart and a port question: rotated out after a July 2024 addition that press framed specifically as 'PC Game Pass', on 32,370 reviews. It is here rather than in Tier 2 because a restart only earns Tier 2's cost advantage if the console SKU it restarts exists. *Trigger:* Promotes to Tier 2 on a confirmed native Xbox console SKU; stays here as a PC-only re-add otherwise.
- **Path Of Wuxia** (香港商河洛互動娛樂股份有限公司) — 30,091 reviews in a 500k-1M bucket; wuxia RPG is a segment the portfolio has no other exposure to. *Trigger:* Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source.
- **Senren＊Banka** (YUZUSOFT) — 26,756 reviews in a 500k-1M bucket. Ranked second-last because it combines an unverified Xbox SKU with a visual-novel format whose console certification path this analysis has not screened. *Trigger:* Promotes on a confirmed Xbox SKU AND a confirmed console content rating. Evidence is currently a SINGLE source at confidence:'low'.
- **Sanfu** (Shiying Studio) — 15,929 reviews from Shiying Studio — the same developer as Firework in Tier 3, so one counterparty conversation covers both. That efficiency is its only reason for being listed at all. *Trigger:* Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source. Drops off entirely if the Firework conversation fails.

</details>

## Screened and excluded — no deal is possible or needed

- **UNCHARTED™: Legacy of Thieves Collection** (1659420, v3 rank 24) — `structurally_excluded`. Published by PlayStation Publishing LLC (Sony); no Xbox version exists and Sony does not license PlayStation Studios titles to a competing subscription. Confirmed, not assumed.
- **The Outer Worlds** (578650, v3 rank 29) — `structurally_excluded`. Microsoft owns The Outer Worlds IP (Obsidian is Xbox Game Studios) AND it is independently confirmed currently on Game Pass Premium. Two separate reasons this is not a licensing decision.
- **BlazBlue Entropy Effect** (2273430, v3 rank 7) — `already_included`. Ships on Xbox/Game Pass as 'BlazBlue Entropy Effect X', added Feb 12 2026 — a different SKU from the scored Steam app_id, but the franchise is already in the subscription.
- **Hi-Fi RUSH** (1817230, v3 rank 12) — `already_included`. Metacritic 90 and the red team's original example. Microsoft sold Tango Gameworks and the franchise to Krafton in Aug 2024, but it remains in Game Pass Premium under a continuing licence. Nothing to acquire, nothing to license.
- **Halls of Torment** (2218750, v3 rank 27) — `already_included`. Currently listed on Game Pass Premium; no departure evidence found.

## Top-ranked but never screened — cannot be picks

Availability was screened on the v2 top 30. These titles rank inside the v3 top 30 but were never screened, so no verdict exists for them. They are NOT picks and no availability claim is made about them. They are the first two titles any screen extension should cover.

- **Dead Space** (1693980, v3 rank 20, 43,575 reviews, MC 87) — never availability-screened, so no verdict exists.
- **Lies of P** (1627720, v3 rank 21, 41,414 reviews, MC —) — never availability-screened, so no verdict exists.

## Standing caveats

- No engagement or playtime data exists in this dataset — every playtime column is zero. Nothing here claims anything about retention or session length for any title.
- Owners are bucketed SteamSpy ESTIMATES, not measured sales.
- Review counts are self-selected and vary by genre, price and audience size.
- The data is Steam PC; the decision is Xbox console. Console ARPPU is +47.3% ($81.68 / $55.47 - 1 = 0.4725; inputs are MIDiA Research 2024 estimates via Plarium). The has_controller_support gate addresses control scheme only.
- release_date is right-truncated (nothing after Oct 2024) and 20.4% missing.
- Availability was screened on the v2 top 30 only. Every title in this document with no verdict is labelled as such and none is a pick.
