# Stage 13 — External Game Pass availability check

Board question: which of the ranked candidates (`12_candidates_v2.csv`, 215 qualifying
titles) could actually be ADDED to Game Pass. Today is 22 August 2026. Coverage: top 30
by composite score (ranks 1-30), the required minimum. Every determination below carries
a source and a date; where none could be found, the title is marked **not_verified** or
**unknown** rather than guessed.

Full structured data: `artifacts/13_availability.json`.

## Group A — Structurally excluded (no deal is possible or needed)

| Rank | Title | Reason |
|---|---|---|
| 11 | UNCHARTED: Legacy of Thieves Collection | Published by PlayStation Publishing LLC (Naughty Dog / Sony). No Xbox version exists (PC port only, via Steam). Sony does not license PlayStation Studios titles to a competing subscription. **Confirmed, not assumed.** |
| 26 | The Outer Worlds | Developer Obsidian Entertainment is Xbox Game Studios; Private Division (Take-Two) publicly clarified **Microsoft owns The Outer Worlds IP** even though Take-Two retained legacy distribution duties. Also independently confirmed **currently on Xbox Game Pass Premium tier**. Two separate reasons this is not a licensing decision. |

## Group B — Already in the subscription today (verified current, Aug 2026)

| Rank | Title | Tier | Note |
|---|---|---|---|
| 6 | BlazBlue Entropy Effect | Premium | Ships on Xbox/Game Pass under the edition name **"BlazBlue Entropy Effect X"** — same franchise, different SKU from the Steam app_id scored in the dataset. Added Feb 12, 2026. |
| 19 | Hi-Fi RUSH | Premium | **The flagged case.** Ownership moved: Microsoft **sold** Tango Gameworks and the Hi-Fi RUSH franchise to **Krafton** in Aug 2024, after the studio's closure. It is third-party-owned now, not Microsoft's — but Microsoft still has it in Game Pass under an apparent continuing licence with Krafton. Net effect for the board: nothing to acquire, nothing to license; it's already there. |
| 22 | Halls of Torment | Premium | Currently listed, no departure evidence found. |

## Group C — Rotated out (previously licensed, since removed — the cheaper "bring-back" case)

| Rank | Title | Was on GP | Left | Publisher now (bloc) |
|---|---|---|---|---|
| 1 | Phoenix Wright: Ace Attorney Trilogy | Sept 2023 | confirmed gone, exact date not pinned | Capcom (third-party) |
| 3 | Unpacking | — | ~late June 2026 (very recent) | Humble Games (third-party) |
| 8 | Danganronpa 2: Goodbye Despair | May 2022 | May 2023 | Spike Chunsoft (third-party) |
| 12 | Library Of Ruina | Aug 2021 | confirmed gone (player reports), date not pinned | ProjectMoon (third-party) |
| 16 | What Remains of Edith Finch | ≥2019 (upgraded July 2022) | confirmed gone (VGC rotation article) | Annapurna Interactive (third-party) |
| 25 | Journey | July 2024 (PC Game Pass specifically) | confirmed gone | Annapurna Interactive (third-party) |
| 28 | Marvel's Guardians of the Galaxy | March 2022 | March 15, 2023 | Eidos-Montréal, now **Embracer Group**-owned (Square Enix sold the studio+IP for ~$300M in 2022 — deal counterpart has changed) |
| 29 | Persona 3 Reload | Feb 2, 2024 (day one) | Aug 15, 2025 | SEGA/Atlus (third-party) |

## Group D — Never confirmed on Game Pass, but has a native Xbox release (clean licensing candidates)

Ranks 5 (A Hat in Time), 17 (Return of the Obra Dinn), 18 (Baba Is You) — all confirmed
**"Not Included"** on current Game Pass by a subscription tracker, all confirmed to have
native Xbox console releases, and no evidence found of prior inclusion. These are the
closest things in the top 30 to a genuinely fresh, uncomplicated licensing opportunity.

## Group E — Xbox version exists, current Game Pass status not reconfirmed either way

Ranks 9 (A Short Hike), 10 (DJMAX RESPECT V), 15 (Chants of Sennaar), 20 (ENDER LILIES),
21 (Rhythm Doctor), 24 (CARRION), 30 (Potion Craft). All were added to Game Pass at some
point (dated sources for each in the JSON); none has a dated departure article, and none
was confirmed present in the current Aug 2026 lineup either. Marked **unknown** —
plausible either way, needs a direct storefront check before costing.

## Group F — Console-port and platform-coverage gaps (cost multiplier, not a blocker)

- **Rank 13, Wandering Sword**: has **no Xbox release at all** as of Aug 2026. Console
  versions (PS5, Switch/Switch 2, Xbox Series) were delayed to **21 January 2027**. Any
  deal today is PC Game Pass only, or must wait ~5 months for the console SKU to exist.
- Ranks 4 (SANABI), 7 (The Hungry Lamb), 14 (Sanfu), 23 (Path Of Wuxia), 27 (Senren＊Banka):
  no evidence found of any Xbox console release — coverage is Steam/Switch/PC only in every
  source checked. These should be treated as **PC-only pending direct confirmation**, which
  changes the cost of a deal by the order of magnitude the brief anticipated.

## What could not be verified

- Exact departure dates for Phoenix Wright, Library of Ruina, and What Remains of Edith
  Finch (confirmed gone, date not pinned to a single dated article).
- Current-day Game Pass status for A Short Hike, DJMAX RESPECT V, Chants of Sennaar, ENDER
  LILIES, Rhythm Doctor, CARRION, Potion Craft, and Firework — all had confirmed additions
  at some point but no confirmed current status either way.
- Any Xbox console release for SANABI, The Hungry Lamb, Sanfu, Path Of Wuxia, Senren＊Banka
  — absence of evidence, not confirmed absence of a port.
- Whether Journey has a native Xbox Series console release versus a PC-only 2024 port —
  press coverage specifically frames the 2024 addition as "PC Game Pass," which is a signal,
  not a confirmation.
- Ranks 31+ were not checked at all (out of scope for this pass; task required top 30 minimum).

## Deal structures and cost ranges (for the sizing stage)

**Fact, dated:** A May 2023 internal Xbox email (Sarah Bond, CVP), reported by Axios
(Sept 19, 2023, based on a legal-discovery leak), assessed 18 third-party titles under
consideration for Game Pass and put estimated day-one licensing costs at wildly different
levels by title prominence: Assassin's Creed Mirage ≈ **$100M**, Star Wars Jedi: Survivor
≈ **$300M** (flagged internally as poor ROI despite being a "crown jewel"), Baldur's Gate
3 ≈ **$5M**. Back-catalogue ongoing licensing for GTA V was estimated at **$12-15M/month**.
[Axios, "Microsoft leak reveals cost estimates of bringing big releases to Game Pass," Sept 19, 2023]

**Fact, dated:** Microsoft has paid "hundreds of millions of dollars" in aggregate Game
Pass licensing fees to developers/publishers since the service's 2017 launch, but has never
disclosed whether payments are structured as upfront minimum guarantees, per-player-hour
payouts, or a hybrid — GameSpot explicitly notes this remains undisclosed. [GameSpot,
March 25, 2022]

**Analyst/practitioner observation, dated:** Red Hook Studios co-founder Chris Bourassa
(quoted in Game World Observer, March 29, 2024) says indie-scale minimum-guarantee deals
have shrunk markedly since the 2019 "gold rush" era (when Epic Games alone spent $210M in
minimum guarantees in one wave of exclusivity deals) — "the scale of the deals I'm hearing
about is significantly diminished." No comparable specific dollar figures for current
indie-tier deals were found; this is a directional signal, not a number to build a model on.

**What this means for sizing an indie/back-catalogue add:** none of the sourced figures
above are indie-scale — they are all AAA or established-franchise numbers ($5M-$300M, or
$12-15M/month for one of the best-selling games ever made). No dated, sourced figure for
a genuinely small-scale indie or back-catalogue minimum guarantee (the tier most of this
top-30 list sits in) was found in this pass. **Flag this explicitly to the next stage as
an unquantified input** — extrapolating from the Baldur's Gate 3 ($5M) or GTA V
($12-15M/month) numbers downward to a sub-750k-owner indie title would be speculation, not
evidence.

**Day-one vs back-catalogue:** the pattern across every dated example found in this pass
(Firework, A Short Hike, Potion Craft, Library of Ruina, Persona 3 Reload, DJMAX Respect V,
Danganronpa 2, Chants of Sennaar, Phoenix Wright, Unpacking) is that **almost every title
Microsoft licenses into Game Pass at all arrives day-and-date with its console/PC launch**,
not as a later back-catalogue pickup — of the top-30, only Phoenix Wright, Unpacking,
Baba Is You-class "already released, added later" pattern shows up rarely by comparison.
No source gave an explicit price differential between day-one and back-catalogue
placement; the Axios GTA V figure ($12-15M/month) is the only clean back-catalogue data
point found, and it is not comparable in scale to anything in this list.
