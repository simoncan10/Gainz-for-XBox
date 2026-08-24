# Game Pass portfolio — spoken pitch

**Audience:** Microsoft / Xbox board · **Date:** 22 August 2026
**Spoken word count: 439** (body only — headings, stage directions and the traceability
table are not spoken)
**Runtime: 3:23 at 130 wpm · 2:56 at 150 wpm.** Plan for **~3:10**. If you are running long,
the cuttable line is marked **[CUT IF LONG]** — dropping it takes you to 430 words (3:18 /
2:52). It is the only line in the script that says nothing the board did not already assume.

**Two delivery rules.** Slow down on the six restart titles — they are a list and lists get
rushed. And pause a full beat after "Seventeen survived" before you move on; that is the
number the room should be holding.

---

## 0:00 — 0:20 · HOOK (45 words)

> **One hundred and twenty-two thousand games in the data. Seventeen names on the table.**
>
> The first three: **A Hat in Time.** *(beat)* **Return of the Obra Dinn.** *(beat)* **Baba
> Is You.**
>
> Never on Game Pass, Xbox versions confirmed, no blocker. You could make those calls
> tomorrow morning.

*Delivery: land "one hundred and twenty-two thousand" and "seventeen" as a pair — the whole
pitch is the gap between them. Name the three games slowly, one beat each. Do not explain
them. Do not say what they are. Just name them.*

---

## 0:20 — 0:40 · TENSION (45 words)

> Since July, the studio door is closed. Breadth in Game Pass has to be **licensed** now,
> not built.
>
> The usual answer is a list somebody assembled by taste. **This is not that list.** Every
> title traces to a row in the data and a score.

*Delivery: "This is not that list" is the pivot of the pitch. Stop dead before it and after
it.*

---

## 0:40 — 1:40 · EVIDENCE — three findings (105 words)

**Finding 1 — the funnel (47 words)**

> Start with the funnel. It is the whole argument.
>
> That hundred and twenty-two thousand comes down to **eight hundred** that pass the
> screens, then **two hundred and seventy-five** that clear the bar. **Thirty** were checked
> externally for Game Pass status and for an Xbox version. **Seventeen survived.**

*Delivery: this is the slide the board reads. Let the funnel graphic do the work — say the
four numbers, then hold a full beat on "Seventeen survived."*

**Finding 2 — no port risk (18 words)**

> Second. All seventeen have a confirmed Xbox console release. There is **no port risk**
> anywhere on this list.

*Delivery: flat, fast, factual. This is the cheapest sentence in the pitch and the most
reassuring one. Do not decorate it.*

**Finding 3 — the restarts (40 words)**

> Third, the cheap ones. Six titles were on Game Pass and rotated out. **Unpacking. Phoenix
> Wright. Edith Finch. Library of Ruina. Danganronpa 2. Persona 3 Reload.**
>
> The port shipped, certification passed, and the rights holder has already said yes once.

*Delivery: SLOW. Six names is a lot of ear-work. One beat between each. Some of these are
titles people in the room personally signed off on — the recognition is the point.*

---

## 1:40 — 2:30 · RECOMMENDATION (114 words)

> So. **Approve seventeen back-catalogue licences, in tier order.**
>
> The clean three first: no prior run to explain. Then the six restarts — **Unpacking left
> two months ago**, the warmest call in the set. Then eight breadth titles, led by
> **Firework, ENDER LILIES and DJMAX RESPECT V**. One storefront check each, then sign.
>
> Seven more sit on a watchlist, explicitly **not** a buy: no Xbox version verified.
>
> **[CUT IF LONG]** No studio purchase. No price change. No new development.
>
> I am **not** giving you a per-title number. None is defensible at this tier, and the only
> public range spans a thousandfold. What I have is an **order**: commit tier by tier, and
> stop when the quotes stop making sense.

*Delivery: "I am not giving you a per-title number" will make someone sit forward. Say it
without apology and go straight into what replaces it. The refusal is the credibility move —
if you hedge it, it reads as a gap instead of a decision.*

---

## 2:30 — 3:20 · RISK AND ASK (130 words)

> The strongest objection is mine to raise. **Six of these we already had, and gave up.**
> Either the publisher declined to renew — or **we** did, on engagement data this analysis
> has never seen. I cannot tell from outside. **You can, from inside, in a day.** That is why
> those six are second and not first.
>
> Two caveats. This is **Steam PC data behind an Xbox console decision.** And the list leans
> single-player: under a fifth Action, against more than half the qualifying pool. We tested
> a fix. It did not work, so it is disclosed, not patched.
>
> **I am asking you to approve the seventeen, in tier order, plus one internal lookup on
> those six prior runs.** It costs nothing, and it closes the only open question on the list.

*Delivery: look at the CFO on "or we did." Own it completely — the sentence only works if
you are not defending. Land the ask on two fingers: (1) the seventeen, (2) the lookup. Then
stop talking. Do not add a closing thought.*

---

## Traceability — every spoken figure

Types per `GOAL_STATEMENT.md`: **[M]** Measured (dataset query), **[S]** Sourced (external
publication), **[D]** Derived (arithmetic on the above).

| Spoken as | Exact figure | Type | Backing |
|---|---|---|---|
| "one hundred and twenty-two thousand games" | 122,191 non-demo games | **[M]** | `sql/09_review_bucket_check.sql`, n=122,191; `02_cleaning_report.md` (122,191 `game` / 17,891 `demo`) |
| "eight hundred that pass the screens" | 802 eligible | **[M]** | `16_scoring_v3.md` §Cheap fix — review floor 4,000, 47.3% Metacritic presence |
| "two hundred and seventy-five that clear the bar" | 275 qualifying at composite ≥ 0.60 | **[M]** | `16_scoring_v3.md` §Result; `16_candidates_v3.csv` |
| "thirty were checked externally" | 30 titles availability-screened | **[M]** (external screen, per-title **[S]**) | `13_availability.md` — v2 top 30, every verdict dated Aug 2026, sources in `13_availability.json` |
| "seventeen survived" | 17 picks | **[D]** | `17_portfolio_final.json` `counts.picks` = 3 + 6 + 8; built by `scripts/17_build_portfolio_final.py`, which aborts on any app_id missing from the CSV or the availability JSON |
| "the first three… never on Game Pass, Xbox versions confirmed" | 3/3 `on_gamepass: no`, 3/3 `xbox_version: yes` | **[S]** | `13_availability.md` Group D — A Hat in Time (253230), Return of the Obra Dinn (653530), Baba Is You (736260) |
| "all seventeen have a confirmed Xbox console release" | 17/17 `xbox_version: yes` | **[S]** | `13_availability.json`; verified independently in `15_redteam_portfolio.md` B-3, which counts them under its own pre-reorder tier labels (restarts 6/6, clean spine 3/3, breadth 8/8) |
| "six titles were on Game Pass and rotated out" | 6/6 `rotated_out` | **[S]** | `13_availability.md` Group C (dated departures) |
| "Unpacking left two months ago" | Left ~late June 2026; today 22 Aug 2026 → ~2 months | **[D]** | `13_availability.md` Group C. Departure month is the sourced input; "two months" is arithmetic on it. Say "about two months" — the exact day is not pinned |
| "the only public range spans a thousandfold" | $50K to over $50M across 500+ deals = 1,000× | **[S]** → **[D]** | Iain MacIntyre (ex-Xbox BD lead) via TweakTown, 2025-07-13. **Context only, never a sizing anchor** (`15_redteam_portfolio.md` B-6). The 1,000× ratio is arithmetic on the two endpoints |
| "under a fifth Action" | 17.6% of the 17 picks | **[M]** | `17_portfolio_final.md` §Concentration, n=17 |
| "more than half the qualifying pool" | 53.8% of the 275 qualifying titles | **[M]** | `17_portfolio_final.md` §Concentration, n=275 |
| "Steam PC data behind an Xbox console decision" | Console ARPPU +47.3% ($81.68 ÷ $55.47 − 1) | **[D]** on **[S]** estimates | MIDiA Research 2024 estimates via Plarium, in `04_context.md` §5. Stated qualitatively in the pitch; the figure is in Q&A |
| "seven more sit on a watchlist" | 7 watchlist titles, 6/7 unverified Xbox SKU | **[S]** | `17_portfolio_final.md` §Watchlist; `15_redteam_portfolio.md` B-3 |
| "since July, the studio door is closed" | Ninja Theory, Double Fine, Compulsion closed/divested 2026-07-06 | **[S]** | Tech Times, 2026-07-06, via `04_context.md` §1 |

**On the slides but not spoken** (same rule applies — every slide figure traces):

| On the slide | Exact figure | Type | Backing |
|---|---|---|---|
| Slide 2 · "0.014%" | 17 ÷ 122,191 = 0.0139% | **[D]** | Arithmetic on two Measured figures above (picks; non-demo games). Shown to three significant figures because rounding to "0.01%" would understate by a third |
| Slide 1 · review counts and Metacritic for the lead three | 50,390 / MC 79 · 26,518 / MC 89 · 20,757 / MC 87 | **[M]** | `16_candidates_v3.csv` via `17_portfolio_final.json` trace blocks. Metacritic is an independent press signal and is **never** an input to the composite |
| Slide 3 · tier sizes 3 / 6 / 8 / 7 | — | **[D]** | `17_portfolio_final.json` tier `n` fields |
| Slide 4 · review counts for the six restarts | 41,326 / 33,505 / 32,385 / 29,312 / 29,181 / 25,177 | **[M]** | `16_candidates_v3.csv` via `17_portfolio_final.json`. Chart title states these are recognition, **not sales and not engagement** |

**Figures deliberately NOT spoken**, and why:

- **Any per-title licence cost.** No sourced figure exists for this tier
  (`13_availability.md` §Deal structures; `15_redteam_portfolio.md` B-6). The AAA anchors
  ($5M–$300M day-one; $12–15M/month GTA V back-catalogue, Axios 2023-09-19) are the wrong
  order of magnitude and are not extrapolated downward.
- **Any engagement, retention or playtime claim.** Every playtime column in the dataset is
  zero (`GOAL_STATEMENT.md` §Constraints on honesty).
- **Subscriber counts.** ~30–34M is a third-party aggregator estimate Microsoft has not
  disclosed (`04_context.md` §1). Not needed for the ask.
- **The model's internals** (Recognition 0.50 / three-level ownership step / Fit at 0.10).
  Correct and disclosed in `16_scoring_v3.md` and on the Q&A sheet; too much for the ear. If
  asked, describe it as **"recognition, banded by a coarse three-level ownership step"** —
  never as a multi-pillar blend.
- **"Owners" as sales.** Owners are bucketed SteamSpy estimates. The pitch never says sales.
