# Stage 24 — External Game Pass availability check (indie-focused rebuild, PC-eligible scope)

Board question, rescoped: Game Pass runs on Windows PC, so an Xbox **console** SKU is no
longer required for eligibility — only Windows PC availability matters now; console is a
reach bonus, not a gate. Candidate list rebuilt under a corrected indie definition
(`artifacts/23_indie_candidates_v2.csv`, 201 qualifying titles). Coverage: top 25 by
composite score. Today is 22 August 2026. Full structured data:
`artifacts/24_availability_indie.json`.

Fifteen of these 25 were checked in the prior (console-required) pass. Verdicts are
**reused where the underlying fact hasn't changed**, and explicitly **re-checked and
flagged** where the previous verdict turned on console availability, since that condition
no longer applies. Ten titles are new to this pass and got fresh research.

## Group A — Already in the subscription today (no deal to do)

| Rank | Title | Tier | Note |
|---|---|---|---|
| 5 | BlazBlue Entropy Effect | Premium | Ships on Xbox/PC Game Pass as "BlazBlue Entropy Effect X" (different SKU, same franchise), added Feb 2026. Unchanged. |
| 21 | Halls of Torment | Premium | Confirmed current, Aug 2026. Unchanged. |

## Group B — Rotated out (previously licensed, since removed)

| Rank | Title | Was on GP | Left | Publisher now (bloc) |
|---|---|---|---|---|
| 3 | Unpacking | — | ~late June 2026 | Humble Games (third-party, **unstable** — see below) |
| 6 | VA-11 Hall-A | Dec 1, 2020 (PC Game Pass specifically) | ~Nov 30, 2021 | Ysbryd Games/PLAYISM (third-party) |
| 9 | What Remains of Edith Finch | ≥2019 | confirmed gone | Annapurna Interactive (third-party, **unstable** — see below) |
| 12 | Library Of Ruina | Aug 2021 | confirmed gone, date not pinned | ProjectMoon (third-party) |
| 13 | Journey | July 2024 (**PC Game Pass specifically**) | confirmed gone | Annapurna Interactive (third-party, **unstable**) |

VA-11 Hall-A and Journey are worth flagging together: both are the clearest precedents in
this list for exactly the "PC Game Pass" deal type the new scope asks about — both were
added and later removed as **PC-tier-specific** inclusions, not console releases.

## Group C — Publisher instability (new finding this pass, per coordinator's flag)

Two of the recurring publishers behind this list have had serious organizational trouble
in the last two years, and it changes deal risk independent of the title's own numbers:

- **Annapurna Interactive** (publishes ranks 9 Edith Finch and 13 Journey, and lower-ranked
  Neon White/Gorogoa/Florence): the entire video-game staff (~24 people) resigned en masse
  in September 2024 after a dispute with owner Megan Ellison over a failed spin-off
  negotiation. [Bloomberg, Sept 12, 2024; Deadline, Sept 2024]. No report found that
  Annapurna's catalogue rights themselves were sold or disputed — this is an
  operating-team/counterparty-continuity risk, not a confirmed rights blocker.
- **Humble Games** (publishes ranks 3 Unpacking and 7 Temtem): laid off its entire ~36-person
  staff in July 2024, widely reported as a de facto shutdown; the company disputed "full
  shutdown," called it a "restructure," and later signaled plans to continue supporting its
  existing catalogue. [Forbes, July 23 2024; Game Developer, July 2024; PC Games Insider,
  July 2024]. Same caveat: catalogue rights not reported as lost or sold.
- **NEOWIZ** (publishes rank 8 SANABI): no evidence of comparable restructuring found in
  this pass despite checking per the coordinator's instruction — stated as absence of
  evidence, not confirmed stability.

## Group D — Scope-change verdict flips (previously blocked/pending on console, now clean)

These titles were held back or flagged incomplete in the prior pass specifically because
Xbox console availability was unconfirmed. Under the new PC-eligible scope, all five are
**native Steam (Windows PC) titles by construction of the dataset**, so PC availability is
confirmed and they are no longer blocked on that basis:

| Rank | Title | PC | Xbox console | GP status |
|---|---|---|---|---|
| 4 | The Hungry Lamb | yes | not verified | not verified |
| 8 | SANABI | yes | not verified | not verified |
| 11 | Wandering Sword | yes | **no — delayed to Jan 21, 2027** | not verified |
| 15 | Path Of Wuxia | yes | not verified | not verified |
| 23 | Sanfu | yes | not verified | not verified |

Wandering Sword is the one to flag hardest: it genuinely has no Xbox console SKU at all
today (console launch, across PS5/Switch/Xbox Series, is delayed to 21 January 2027), but
it is fully available on PC right now — under this scope that is sufficient for a PC Game
Pass deal, with console reach arriving five months from now if the current date holds.

## Group E — Never confirmed on Game Pass, native platforms confirmed

| Rank | Title | PC | Xbox console |
|---|---|---|---|
| 2 | A Hat in Time | yes | yes |
| 18 | Return of the Obra Dinn | yes | yes |
| 20 | Rogue Legacy | yes | yes |
| 24 | The Stanley Parable: Ultra Deluxe | yes | yes |

All four confirmed "Not Included" on current Game Pass (three via subscription-tracker
check, Rogue Legacy via absence of any dated evidence despite extensive searching) with no
evidence of prior inclusion. Rogue Legacy 2 (a different game/app) has its own,
well-documented Game Pass history that repeatedly surfaced in searches and must not be
confused with the original Rogue Legacy scored here.

## Group F — Xbox/PC version exists, GP status inconclusive either way

Ranks 1 (Firework), 14 (A Short Hike), 16 (Potion Craft), 19 (Chants of Sennaar), 25
(CARRION) — all confirmed added to Game Pass (PC and/or console) at some point, none with
a confirmed current-day status. Unchanged from the prior pass.

## Group G — New, PC-confirmed, no Game Pass or console evidence found

- **Rank 17, Milk inside a bag of milk inside a bag of milk**: PC (Steam) and Switch
  confirmed; no Xbox release or Game Pass listing found anywhere.
- **Rank 22, KovaaK's**: PC-only in every source checked (a mouse-driven aim trainer,
  consistent with `has_controller_support=False` in the dataset itself); no Xbox release or
  Game Pass listing found. Not disqualified under the new scope, but its genre is a poor
  console-reach fit even though that's not formally a blocker.
- **Rank 7, Temtem**: has a native Xbox Series X|S release (Sept 2022, after PS4/Xbox One
  versions were cancelled in 2020) and PC/Steam release, but no Game Pass listing found in
  any source despite extensive searching.

## What could not be verified

- Current-day Game Pass status for 8 titles with confirmed past-but-unreconfirmed-present
  inclusion (Firework, A Short Hike, Potion Craft, Chants of Sennaar, CARRION, plus SANABI/
  Hungry Lamb/Path of Wuxia/Sanfu, which were never confirmed added at all).
- Whether Journey's PC Game Pass release ever had, or has, an Xbox console counterpart.
- Any Xbox console release for The Hungry Lamb, SANABI, Path Of Wuxia, Sanfu, Milk inside a
  bag of milk, KovaaK's, VA-11 Hall-A — absence of evidence found, not confirmed absence.
- Exact departure dates for Library Of Ruina and Edith Finch.
- Whether the original Rogue Legacy was ever on Game Pass (heavily obscured in search
  results by its sequel's separate, well-documented Game Pass history).
- Ranks 26+ not checked (out of scope for this pass).

## Deal-cost picture — update

**The gap flagged in the previous pass is unchanged: no sourced figure for indie or
back-catalogue-tier Game Pass minimum guarantees was found in this pass either**, despite
searching specifically for it again. The only dated, sourced figures remain AAA-scale
(Axios, Sept 19 2023: $5M-$300M day-one deals) and the GTA V back-catalogue figure
(~$12-15M/month) — neither representative of a sub-750k-owner indie title. State this
plainly to the sizing stage, as instructed: **order the recommendation on deal structure
(rotated-out vs. never-included vs. already-in-service vs. publisher-risk-adjusted), not
on a price point that does not exist in the public record for this tier.**

**New, relevant to sizing though not a price figure:** the discovery that two of this
list's most frequent publishers (Annapurna Interactive, Humble Games) went through
significant organizational upheaval in 2024 is a **deal-risk multiplier** the sizing stage
should weight explicitly — a licence renegotiation with a publisher that laid off its
entire staff eight months prior carries execution risk a stable, well-capitalized
publisher (e.g., NEOWIZ, Devolver Digital, tinyBuild) does not, independent of what the
licence would cost.
