#!/usr/bin/env python3
"""
Stage 17 — final portfolio, rebuilt on 16_candidates_v3.csv.

Changes from scripts/14_build_portfolio.py:
  * source of truth is 16_candidates_v3.csv (275 qualifying, R 0.50 / H 0.40 / F 0.10,
    review floor 4,000), NOT 12_candidates_v2.csv
  * B-1: ALL ranks derived from ONE method — position in the v3 CSV (which is sorted by
    composite desc). The availability JSON's `rank` field is v2 and is never used as a rank.
  * B-2: the clean spine leads; restarts follow.
  * B-3: headline is 17 PICKS + a 7-title WATCHLIST, not 24 picks.
  * B-4: concentration remedy re-derived on v3 and every flag verified in code.
  * Availability verdicts exist ONLY for the 30 app_ids screened at Stage 13 (a v2 top-30).
    Any title without one is marked availability_verdict: "NONE - not screened".
"""
import csv, json, sys
from pathlib import Path

ART = Path(__file__).resolve().parent.parent / "artifacts"

V3 = list(csv.DictReader(open(ART / "16_candidates_v3.csv")))
RANK = {int(r["app_id"]): i + 1 for i, r in enumerate(V3)}      # single rank method
BY = {int(r["app_id"]): r for r in V3}
AVAIL = {int(a["app_id"]): a for a in json.load(open(ART / "13_availability.json"))}

# sanity: CSV must be sorted by composite descending, or RANK is meaningless
sc = [float(r["composite_score"]) for r in V3]
assert sc == sorted(sc, reverse=True), "16_candidates_v3.csv is not sorted by composite desc"

PICK_TIERS = [
    dict(
        tier=1, name="Clean spine", kind="pick", lead=True,
        role=("The only titles in the screened set confirmed never to have been on Game "
              "Pass, confirmed to have a native Xbox console SKU, and carrying no blocker. "
              "They open the pitch because they are the only tier with no unanswered "
              "question attached: nothing to explain about a prior run, nothing to check "
              "before a call can be made."),
        cost_rank=2,
        cost_basis=("A cold negotiation with a small rights holder, but zero port cost and "
                    "zero certification cost — the Xbox SKU already ships. More expensive to "
                    "execute than a restart, cheaper than anything needing a port."),
        confidence="medium-high",
        confidence_driver=("3/3 confirmed 'Not Included' on current Game Pass AND 3/3 "
                           "confirmed native Xbox release (Stage 13, dated Aug 2026). All "
                           "three carry Metacritic 79-89 — an independent press signal that "
                           "is not an input to the composite that selected them."),
        removal_rule=("Remove a title here if a prior Game Pass run surfaces after all — not "
                      "because a prior run disqualifies it, but because it then belongs in "
                      "Tier 2 and must answer Tier 2's question first. Otherwise remove only "
                      "on a refusal to license."),
        picks=[
            (253230,
             "50,390 reviews, the highest volume of any title in the screened set, with "
             "Metacritic 79 and both co-op and multiplayer flags set — the one pick that "
             "cuts against the singleplayer concentration disclosed below.",
             "Gears for Breakfast's console publishing partner will not grant a "
             "subscription licence separately from retail."),
            (653530,
             "Metacritic 89 on 26,518 reviews, and the simplest counterparty available "
             "anywhere in the portfolio: one person (Lucas Pope) holding all rights, with "
             "the Xbox SKU already shipped.",
             "Lucas Pope declines subscription placement — a solo rights holder can refuse "
             "outright and there is no second party to negotiate with."),
            (736260,
             "Metacritic 87 on 20,757 reviews, and the portfolio's only pure puzzle title — "
             "the specific breadth that keeps this tier from being one narrative bet made "
             "three times.",
             "Hempuli declines, or the 'Not Included' tracker verdict proves stale."),
        ],
        alternate=813230,
        alternate_note=("ANIMAL WELL — Metacritic 91, the highest score anywhere in the v3 "
                        "qualifying list, from a solo developer (Billy Basso), in the "
                        "200k-500k owner bucket that the B-5 sensitivity below says this "
                        "portfolio is short of. It is an alternate and not a pick for one "
                        "reason: it was never availability-screened, so no verdict exists. "
                        "Screen it and it is promotable on merit alone."),
    ),
    dict(
        tier=2, name="Restarts", kind="pick", lead=False,
        role=("Re-open licences Microsoft has already signed once: the Xbox SKU shipped and "
              "passed certification, the rights holder has said yes before, and a contract "
              "template exists. This is the cheapest tier to EXECUTE. It is deliberately "
              "second, not first, because cheap to execute is not the same as good to buy — "
              "see the disclosure below."),
        cost_rank=1,
        cost_basis=("Cheapest to execute: no port, no certification, no cold introduction, "
                    "existing contract template. The licence FEE is unknown and is not "
                    "assumed lower."),
        confidence="medium-high on executability, LOW on desirability",
        confidence_driver=("Executability is externally verified with dated sources for "
                           "every title (6/6 rotated_out, 6/6 Xbox SKU confirmed). "
                           "Desirability is low-confidence because no source establishes WHY "
                           "any of them left, and the two candidate reasons point opposite "
                           "ways."),
        removal_rule=("Remove any title here that Microsoft's own record of its prior run "
                      "places in the bottom quartile of engagement per licensing dollar "
                      "among comparable back-catalogue titles. This is a condition attached "
                      "to six named picks that stand without it — not a request to go and "
                      "measure before deciding."),
        picks=[
            (1135690,
             "Left Game Pass roughly two months ago (~late June 2026) — the freshest lapsed "
             "deal in the screened set, so the counterparty is warm and the renewal "
             "conversation is live now rather than cold. This is the one call that can be "
             "made this week.",
             "Humble Games confirms the departure was its own decision to pursue a "
             "competing-subscription exclusive."),
            (787480,
             "v3 rank 2 on 33,505 reviews with Metacritic 80; the Xbox SKU shipped Sept 26 "
             "2023, so a re-add requires no port and no re-certification.",
             "Capcom prices a re-add above a fresh licence for a comparable title, which "
             "removes the entire cost rationale for this tier."),
            (501300,
             "Metacritic 89 on 41,326 reviews — the strongest independent press signal of "
             "any rotated-out title, and press coverage is never an input to the composite.",
             "Annapurna's post-2024 restructuring has left no single counterparty able to "
             "grant a console subscription licence."),
            (1256670,
             "29,181 reviews against a 500k-1M owner bucket from a single independent studio "
             "(ProjectMoon) — one rights holder, one title, one prior yes.",
             "The departure cannot be pinned well enough to establish the prior deal lapsed "
             "rather than was terminated."),
            (413420,
             "A one-year run (May 2022 - May 2023) that reads as a fixed-term deal expiring "
             "rather than a rejection, on Metacritic 83 and 25,177 reviews.",
             "Spike Chunsoft has since granted console subscription rights elsewhere."),
            (2161700,
             "The longest and best-documented Game Pass run in the tier — day-one Feb 2 2024 "
             "to Aug 15 2025 — on Metacritic 89. Ranked last in its tier deliberately: at a "
             "$69.99 still-selling SKU from a large publisher it is the likeliest title here "
             "to price itself out.",
             "SEGA/Atlus quotes anywhere near the order of magnitude of the sourced AAA "
             "day-one figures."),
        ],
        alternate=1088850,
        alternate_note=("Marvel's Guardians of the Galaxy — v3 rank 18, rotated out March 15 "
                        "2023 after a 12-month run, 35,789 reviews, Xbox SKU confirmed. It "
                        "is the alternate rather than a pick because the counterparty "
                        "changed: Embracer Group bought Eidos-Montreal and the IP from "
                        "Square Enix in 2022, so the prior yes came from a company that no "
                        "longer holds the rights — and a licensed Marvel property adds a "
                        "second rights holder this analysis never screened."),
    ),
    dict(
        tier=3, name="Confirm-then-sign breadth", kind="pick", lead=False,
        role=("Genre breadth per licensing dollar: rhythm, metroidvania, language puzzle, "
              "horror, crafting-sim and open-world exploration, none of which Tiers 1 and 2 "
              "cover. Every title here has a CONFIRMED Xbox console SKU; the only open "
              "question is whether it is currently in the subscription, and that question "
              "has exactly two answers, both already handled by the removal rule."),
        cost_rank=3,
        cost_basis=("Same structure as Tier 1 (licence, Xbox SKU exists) plus one storefront "
                    "check per title. If a title turns out to be currently included, its "
                    "cost is zero because there is nothing to buy."),
        confidence="medium-high on executability, medium on necessity",
        confidence_driver=("8/8 have a confirmed native Xbox SKU — this tier carries NO port "
                           "risk. What is open is current subscription status: Stage 13 "
                           "found a dated addition for each and no dated departure for any, "
                           "and refused to guess. 4 of 8 carry Metacritic (75-86)."),
        removal_rule=("Remove on either branch of the status check. Currently included -> "
                      "nothing to buy. Confirmed departed -> it moves to Tier 2 and inherits "
                      "Tier 2's condition. Either way the title leaves this tier, which is "
                      "why the tier is low-risk rather than uncertain."),
        picks=[
            (1288310,
             "The highest composite in the entire 275-title v3 qualifying list (0.9740) on "
             "39,637 reviews. It sits in Tier 3 rather than Tier 1 solely because its "
             "current subscription status could not be confirmed either way.",
             "Either branch of the status check; also remove if the native Xbox SKU cannot "
             "be pinned, since Stage 13 recorded 'yes' without naming the SKU."),
            (1369630,
             "Metacritic 86 on 35,018 reviews — the highest review volume in this tier and "
             "the portfolio's only metroidvania.",
             "Either branch of the status check."),
            (960170,
             "26,951 reviews in a 500k-1M bucket. The only title in the tier whose publisher "
             "(NEOWIZ) operates at mid-size rather than indie scale, which makes it the "
             "tier's cost outlier and its first candidate for deferral.",
             "Either branch of the status check; also remove if quoted at large-publisher "
             "scale, since rhythm breadth is already served by Rhythm Doctor at a fraction "
             "of the counterparty size."),
            (1055540,
             "Metacritic 82 on 17,323 reviews in the 200k-500k owner bucket — the 'recognised "
             "but not widely owned' profile the brief asks for, at its purest, and one of "
             "only two picks below the top ownership bucket.",
             "Either branch of the status check."),
            (1210320,
             "31,904 reviews in a crafting/simulation genre no other portfolio title covers.",
             "Either branch of the status check."),
            (1931770,
             "Metacritic 86 on 17,036 reviews at $12.99, in the 200k-500k bucket, occupying "
             "a language-puzzle genre nothing else in the portfolio touches.",
             "Either branch of the status check."),
            (953490,
             "24,708 reviews with Metacritic 75 — the portfolio's only horror title, a genre "
             "Tiers 1 and 2 have none of.",
             "Either branch of the status check; Metacritic 75 is the weakest press score in "
             "the portfolio, so it is also the first cut if the tier must shrink."),
            (774181,
             "20,321 reviews with co-op and multiplayer flags set — one of only two picks in "
             "the whole portfolio that is played socially, which matters given the "
             "concentration disclosed below.",
             "Either branch of the status check; still flagged Early Access in the dataset, "
             "so remove if the console SKU is not a finished release."),
        ],
        alternate=1703340,
        alternate_note=("The Stanley Parable: Ultra Deluxe — v3 rank 33, 28,048 reviews, "
                        "500k-1M owners, Crows Crows Crows. Alternate rather than pick "
                        "because it was never availability-screened: no verdict exists on "
                        "either its Game Pass status or its Xbox SKU."),
    ),
]

WATCHLIST = dict(
    tier=4, name="Port-gap watchlist", kind="watchlist", lead=False,
    role=("NOT picks. Seven high-scoring titles that cannot be recommended for purchase "
          "because the thing being bought — a title playable on Xbox console — has not been "
          "shown to exist. They are named and kept visible so the board sees what it is "
          "choosing not to chase, and so a single confirmation can promote any of them."),
    cost_rank=4,
    cost_basis=("Individually the cheapest counterparties in the analysis (small Chinese and "
                "Korean independents) but the worst value per dollar for a console-led "
                "subscription, because the console audience cannot play them. Cost is not "
                "the constraint here; reach is."),
    confidence="low",
    confidence_driver=("6 of 7 have an UNVERIFIED Xbox SKU. Five of those rest on a SINGLE "
                       "source, and two (The Hungry Lamb, Senren*Banka) at "
                       "confidence:'low'. 'No evidence found' from one low-confidence search "
                       "is not a finding. Only Wandering Sword's gap is positively "
                       "established, with a date."),
    removal_rule=("This tier's discipline is a PROMOTION trigger, not a removal rule, "
                  "because the removal rule that governs the picks ('no Xbox SKU exists and "
                  "none is dated') cannot even be evaluated for six of these seven. "
                  "PROMOTION TRIGGER: a native Xbox console SKU confirmed by two independent "
                  "dated sources, or one primary source (publisher or Microsoft Store "
                  "listing). On confirmation the title moves to Tier 3 and competes on "
                  "merit. Absent that, it is never bought and never pitched."),
    picks=[
        (1876890,
         "The only positively established gap in the set: the Xbox Series version is DATED to "
         "21 January 2027. That makes it a diary entry with a known date rather than an open "
         "question, on 19,877 reviews.",
         "Promotes on 21 Jan 2027 if the console release ships; drops off if the date slips "
         "again, at which point it is open-ended rather than diarisable."),
        (2593370,
         "38,601 reviews at $7.49 — the highest review volume and the lowest price in the "
         "set, so the cheapest possible test of whether this segment transfers at all.",
         "Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source at "
         "confidence:'low'."),
        (1562700,
         "v3 rank 6, composite 0.9546 — the highest-scoring title anywhere in this document "
         "with no confirmed Xbox SKU, which is exactly why the port question is worth one "
         "call.",
         "Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source."),
        (638230,
         "The only entry that is both a restart and a port question: rotated out after a July "
         "2024 addition that press framed specifically as 'PC Game Pass', on 32,370 reviews. "
         "It is here rather than in Tier 2 because a restart only earns Tier 2's cost "
         "advantage if the console SKU it restarts exists.",
         "Promotes to Tier 2 on a confirmed native Xbox console SKU; stays here as a PC-only "
         "re-add otherwise."),
        (1189630,
         "30,091 reviews in a 500k-1M bucket; wuxia RPG is a segment the portfolio has no "
         "other exposure to.",
         "Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source."),
        (1144400,
         "26,756 reviews in a 500k-1M bucket. Ranked second-last because it combines an "
         "unverified Xbox SKU with a visual-novel format whose console certification path "
         "this analysis has not screened.",
         "Promotes on a confirmed Xbox SKU AND a confirmed console content rating. Evidence "
         "is currently a SINGLE source at confidence:'low'."),
        (1880330,
         "15,929 reviews from Shiying Studio — the same developer as Firework in Tier 3, so "
         "one counterparty conversation covers both. That efficiency is its only reason for "
         "being listed at all.",
         "Promotes on a confirmed Xbox SKU. Evidence is currently a SINGLE source. Drops off "
         "entirely if the Firework conversation fails."),
    ],
    alternate=359870,
    alternate_note=("FINAL FANTASY X/X-2 HD Remaster — a deliberately different kind of "
                    "alternate. If the board rejects this watchlist's premise outright, this "
                    "substitutes a large-publisher back-catalogue title with a "
                    "long-established Xbox SKU. It was never availability-screened, so no "
                    "verdict exists."),
)

EXCLUDED = [
    (1659420, "structurally_excluded",
     "Published by PlayStation Publishing LLC (Sony); no Xbox version exists and Sony does "
     "not license PlayStation Studios titles to a competing subscription. Confirmed, not "
     "assumed."),
    (578650, "structurally_excluded",
     "Microsoft owns The Outer Worlds IP (Obsidian is Xbox Game Studios) AND it is "
     "independently confirmed currently on Game Pass Premium. Two separate reasons this is "
     "not a licensing decision."),
    (2273430, "already_included",
     "Ships on Xbox/Game Pass as 'BlazBlue Entropy Effect X', added Feb 12 2026 — a different "
     "SKU from the scored Steam app_id, but the franchise is already in the subscription."),
    (1817230, "already_included",
     "Metacritic 90 and the red team's original example. Microsoft sold Tango Gameworks and "
     "the franchise to Krafton in Aug 2024, but it remains in Game Pass Premium under a "
     "continuing licence. Nothing to acquire, nothing to license."),
    (2218750, "already_included",
     "Currently listed on Game Pass Premium; no departure evidence found."),
]


def build_row(app_id, why, trigger, tier, tier_name, kind):
    if app_id not in BY:
        sys.exit(f"FATAL: app_id {app_id} is not in the v3 qualifying list")
    if app_id not in AVAIL:
        sys.exit(f"FATAL: app_id {app_id} has no Stage 13 availability verdict "
                 f"and therefore cannot be a pick or watchlist entry")
    c, a = BY[app_id], AVAIL[app_id]
    return {
        "portfolio_position": None, "kind": kind, "tier": tier, "tier_name": tier_name,
        "app_id": app_id, "name": c["name"], "developer": c["developer"],
        "publisher": c["publisher"],
        "why": why, "removal_or_promotion_trigger": trigger,
        "trace_16_candidates_v3": {
            "v3_rank": RANK[app_id], "composite_score": float(c["composite_score"]),
            "score_tier": c["tier"],
            "recognition_pct": float(c["recognition_pct"]),
            "headroom_pct_NOT_independent_see_disclosure": float(c["headroom_pct"]),
            "fit_pct_tiebreaker_only_10pct_weight": float(c["fit_pct"]),
            "review_total": int(c["review_total"]),
            "review_positive_ratio": float(c["review_positive_ratio"]),
            "owners_range_steamspy_bucket_estimate": c["owners_range"],
            "owners_mid": int(float(c["owners_mid"])),
            "price_usd_retail_NOT_licence_cost": float(c["price_usd"]),
            "metacritic_score": c["metacritic_score"] or None,
            "has_controller_support": c["has_controller_support"],
            "has_coop": c["has_coop"], "has_multiplayer": c["has_multiplayer"],
            "genres": c["genres"],
        },
        "trace_13_availability": {
            "screened": True, "on_gamepass": a["on_gamepass"],
            "xbox_version": a["xbox_version"], "publisher_now": a["publisher_now"],
            "blockers": a["blockers"], "note": a["notes"],
            "n_sources": len(a["sources"]),
            "min_source_confidence": min(
                (s.get("confidence", "unknown") for s in a["sources"]),
                key=lambda x: {"low": 0, "medium": 1, "high": 2}.get(x, 3)),
            "source_urls": [s["url"] for s in a["sources"]],
        },
    }


def alt_block(app_id, note):
    c = BY.get(app_id)
    if c is None:
        sys.exit(f"FATAL: alternate {app_id} not in v3 qualifying list")
    return {
        "app_id": app_id, "name": c["name"], "developer": c["developer"],
        "v3_rank": RANK[app_id], "composite_score": float(c["composite_score"]),
        "review_total": int(c["review_total"]),
        "owners_range": c["owners_range"],
        "metacritic_score": c["metacritic_score"] or None,
        "availability_verdict": ("screened at Stage 13" if app_id in AVAIL
                                 else "NONE - never availability-screened"),
        "why_alternate_not_pick": note,
    }


rows, tiers_out, pos = [], [], 0
for t in PICK_TIERS + [WATCHLIST]:
    trs = []
    for app_id, why, trig in t["picks"]:
        pos += 1
        r = build_row(app_id, why, trig, t["tier"], t["name"], t["kind"])
        r["portfolio_position"] = pos
        rows.append(r); trs.append(r)
    tiers_out.append({
        "presentation_order": t["tier"], "tier_name": t["name"], "kind": t["kind"],
        "leads_the_pitch": t["lead"], "role": t["role"],
        "execution_cost_rank_1_cheapest": t["cost_rank"], "cost_basis": t["cost_basis"],
        "confidence": t["confidence"], "confidence_driver": t["confidence_driver"],
        "removal_or_promotion_rule": t["removal_rule"], "n": len(trs),
        "titles": [{"position": r["portfolio_position"], "app_id": r["app_id"],
                    "name": r["name"], "v3_rank": r["trace_16_candidates_v3"]["v3_rank"]}
                   for r in trs],
        "named_alternate": alt_block(t["alternate"], t["alternate_note"]),
    })

# ---- B-4: concentration, re-derived on v3, every flag read from the CSV --------------
def share(rs, f):
    return round(100.0 * sum(1 for r in rs if f(r)) / len(rs), 1)
is_action = lambda r: "Action" in r["genres"].split("|")
is_mp = lambda r: r["has_multiplayer"] == "True"
is_co = lambda r: r["has_coop"] == "True"
pick_rows = [BY[r["app_id"]] for r in rows if r["kind"] == "pick"]
bands = {f"ranks {a+1}-{b}": V3[a:b] for a, b in [(0, 30), (30, 60), (60, 120), (120, 275)]}
# verified co-op AND multiplayer titles in the band where density actually rises
remedy = [{"v3_rank": RANK[int(r["app_id"])], "app_id": int(r["app_id"]), "name": r["name"],
           "has_coop": r["has_coop"], "has_multiplayer": r["has_multiplayer"],
           "review_total": int(r["review_total"]),
           "metacritic_score": r["metacritic_score"] or None,
           "availability_verdict": ("screened" if int(r["app_id"]) in AVAIL
                                    else "NONE - never availability-screened")}
          for r in V3[30:120] if r["has_coop"] == "True" and r["has_multiplayer"] == "True"]
for m in remedy:                      # verify in code, do not trust the label
    assert m["has_coop"] == "True" and m["has_multiplayer"] == "True"

top30_unscreened = [{"v3_rank": i, "app_id": int(r["app_id"]), "name": r["name"],
                     "review_total": int(r["review_total"]),
                     "metacritic_score": r["metacritic_score"] or None}
                    for i, r in enumerate(V3[:30], 1) if int(r["app_id"]) not in AVAIL]

sub500 = [r for r in V3 if float(r["owners_mid"]) <= 500000]

out = {
    "stage": 17, "generated": "2026-08-22", "supersedes": "artifacts/14_portfolio.json",
    "built_from": {"candidates": "16_candidates_v3.csv (275 qualifying, composite >= 0.60)",
                   "availability": "13_availability.json (30 titles, screened on the v2 top 30)",
                   "script": "scripts/17_build_portfolio_final.py"},
    "headline": ("17 named picks in three tiers, plus a 7-title port-gap watchlist that is "
                 "explicitly NOT a buy list. All 17 picks have a confirmed native Xbox "
                 "console SKU; 3 are fully clean (never on Game Pass, no blocker). This "
                 "recommends licensing named back-catalogue titles only — no studio "
                 "acquisition, no studio funding, no pricing change, no new development."),
    "how_the_ranking_actually_works_DISCLOSURE": {
        "statement": ("The composite is NOT a multi-pillar blend. It is Recognition "
                      "(percentile of ln review_total, weight 0.50) banded by a three-level "
                      "ownership step. Within any ownership tier the ranking is simply "
                      "most-reviewed first."),
        "evidence": ("owners_mid takes 5 distinct values and 3 buckets hold nearly the whole "
                     "pool, so within every bucket Spearman(recognition, headroom) = 1.0000 "
                     "exactly — Headroom is Recognition minus a constant. The pooled +0.492 "
                     "(v3) is entirely between-bucket variation, a Simpson-shaped artifact. "
                     "Headroom's only real job is moving a title between the three bands, "
                     "not ordering it within one. Source: 16_scoring_v3.md Fix 2."),
        "why_not_fixed": ("This is a SteamSpy bucket-granularity limit, documented since "
                          "01_profile.md. No reformulation of Headroom from the same column "
                          "changes it. It is disclosed, not repaired."),
        "fit": ("Weight cut 0.20 -> 0.10 because its in-population R2 is -1.34, worse than "
                "predicting the mean. Measured influence on the v3 composite: Spearman 0.04. "
                "It is a tiebreaker; nothing in this portfolio rests on it."),
    },
    "counts": {"eligible_pool_v3": 802, "qualifying_v3_at_0.60": 275,
               "availability_screened": 30,
               "picks": sum(1 for r in rows if r["kind"] == "pick"),
               "watchlist": sum(1 for r in rows if r["kind"] == "watchlist"),
               "excluded": len(EXCLUDED)},
    "tiers": tiers_out, "titles": rows,
    "excluded_from_portfolio": [
        {"app_id": i, "name": BY[i]["name"] if i in BY else AVAIL[i]["name"],
         "v3_rank": RANK.get(i), "reason": why, "detail": d} for i, why, d in EXCLUDED],
    "top_ranked_but_unscreened_cannot_be_picks": {
        "note": ("Availability was screened on the v2 top 30. These titles rank inside the "
                 "v3 top 30 but were never screened, so no verdict exists for them. They are "
                 "NOT picks and no availability claim is made about them."),
        "titles": top30_unscreened,
    },
    "concentration_B4": {
        "position": ("Stated as an accepted, explained property of the ranking — not "
                     "papered over, and not patched with a remedy that does not remedy it."),
        "portfolio_picks": {"n": len(pick_rows), "action_pct": share(pick_rows, is_action),
                            "multiplayer_pct": share(pick_rows, is_mp),
                            "coop_pct": share(pick_rows, is_co)},
        "v3_qualifying_list": {"n": len(V3), "action_pct": share(V3, is_action),
                               "multiplayer_pct": share(V3, is_mp),
                               "coop_pct": share(V3, is_co)},
        "by_rank_band_v3": {k: {"n": len(v), "action_pct": share(v, is_action),
                                "multiplayer_pct": share(v, is_mp),
                                "coop_pct": share(v, is_co)} for k, v in bands.items()},
        "what_changed_from_v2": ("v2 ranks 31-60 were IDENTICAL to ranks 1-30 on multiplayer "
                                 "and co-op (16.7% / 13.3% in both), which is why the v2 "
                                 "remedy 'extend the screen to rank 60' did nothing. Cutting "
                                 "Fit to 10% reduced the sentiment tilt: v3 ranks 31-60 are "
                                 "23.3% multiplayer against 13.3% in ranks 1-30. The tilt is "
                                 "smaller but the gradient is still monotone, and density "
                                 "only doubles past rank 60."),
        "mechanism": ("Two causes. (1) Recognition carries 0.50 and review volume is highest "
                      "for singleplayer narrative titles in this pool. (2) v2's Fit model, "
                      "retargeted onto review_positive_ratio, became a sentiment proxy and "
                      "penalised genre_Massively Multiplayer (-0.0851), genre_Action "
                      "(-0.0247) and has_multiplayer (-0.0095), because multiplayer titles "
                      "carry systematically lower positive ratios. At 0.10 weight that "
                      "distortion is much reduced but not eliminated."),
        "correction_carried_from_v2": ("The v2 artifact named Deep Rock Galactic: Survivor "
                                       "(app_id 2321470) as a co-op alternate. Its flags are "
                                       "has_coop=False and has_multiplayer=False, and Stage "
                                       "16 confirmed the flags are CORRECT — it is a genuine "
                                       "single-player roguelite spin-off, distinct from Deep "
                                       "Rock Galactic (548430). The label was the error. It "
                                       "is withdrawn and appears nowhere in this portfolio."),
        "what_a_working_remedy_would_cost": (
            "Extending the availability screen to v3 rank 120 is the only intervention that "
            "reaches the band where multiplayer density actually doubles. It would surface "
            f"{len(remedy)} titles with VERIFIED co-op AND multiplayer flags. None of them "
            "can be a pick today because none has been availability-screened. This is stated "
            "as the cost of closing the gap, not offered as a closed gap."),
        "verified_coop_and_multiplayer_titles_v3_ranks_31_120": remedy,
    },
    "ownership_ceiling_B5": {
        "position": "Known design property, stated plainly, not a defect being hidden.",
        "measured": {"qualifying_list_in_top_bucket_pct": 60.0,
                     "eligible_pool_in_top_bucket_pct": 48.1,
                     "picks_in_top_bucket": sum(
                         1 for r in pick_rows if float(r["owners_mid"]) > 500000),
                     "picks_total": len(pick_rows)},
        "mechanism": ("Recognition is continuous and weighted 0.50 while ownership acts only "
                      "as a three-level step (see the disclosure above), far too coarse to "
                      "offset it. The model therefore selects the most-owned titles that "
                      "still clear the ceiling: the ceiling DEFINES the list more than it "
                      "filters it. And owners_mid <= 750,000 is bucket-identical to "
                      "<= 1,499,999, so 'not already widely owned' is enforced at a "
                      "granularity SteamSpy data cannot support."),
        "sensitivity_one_bucket_down": {
            "definition": "v3 qualifying titles with owners_mid <= 500,000",
            "n": len(sub500), "pct_of_qualifying": round(100.0 * len(sub500) / len(V3), 1),
            "top_10": [{"v3_rank": RANK[int(r["app_id"])], "name": r["name"],
                        "review_total": int(r["review_total"]),
                        "metacritic_score": r["metacritic_score"] or None,
                        "availability_verdict": (
                            AVAIL[int(r["app_id"])]["on_gamepass"]
                            if int(r["app_id"]) in AVAIL
                            else "NONE - never availability-screened")}
                       for r in sub500[:10]],
            "finding": ("Most of this view was never availability-screened, so it cannot be "
                        "turned into a portfolio without extending the screen. It surfaces "
                        "named titles the current picks miss — ANIMAL WELL (Metacritic 91), "
                        "Neon White (89), Rogue Legacy (85) — which is the honest answer to "
                        "'did you pick these, or did the threshold pick them?'"),
        },
    },
    "sizing": {
        "position": ("There is NO defensible per-title price for this tier and none is "
                     "offered. What is offered instead is an execution ordering: commit tier "
                     "by tier and stop when the quotes stop making sense."),
        "ordering_basis": ("Deal structure — prior deal exists / port exists / status known / "
                           "counterparty scale. NOT retail price: Stage 11 (RT-04) "
                           "established that price in this catalogue is a monotone proxy for "
                           "production budget and press coverage, so ordering cost by sticker "
                           "price would resurrect the error the rebuild removed."),
        "qa_sheet_context_not_a_sizing_anchor": (
            "$50K to over $50M across 500+ deals [Iain MacIntyre, former Xbox BD lead, via "
            "TweakTown 2025-07-13]. A 1,000x span with no published breakdown: it excludes no "
            "possibility and supports no budget approval. It belongs in Q&A as context, not "
            "in a sizing section as an anchor. The AAA figures ($5M-$300M day-one; "
            "$12-15M/month for GTA V back-catalogue, Axios 2023-09-19) are the wrong order of "
            "magnitude to extrapolate from."),
    },
    "standing_caveats": [
        "No engagement or playtime data exists in this dataset — every playtime column is "
        "zero. Nothing here claims anything about retention or session length for any title.",
        "Owners are bucketed SteamSpy ESTIMATES, not measured sales.",
        "Review counts are self-selected and vary by genre, price and audience size.",
        "The data is Steam PC; the decision is Xbox console. Console ARPPU is +47.3% "
        "($81.68 / $55.47 - 1 = 0.4725; inputs are MIDiA Research 2024 estimates via "
        "Plarium). The has_controller_support gate addresses control scheme only.",
        "release_date is right-truncated (nothing after Oct 2024) and 20.4% missing.",
        "Availability was screened on the v2 top 30 only. Every title in this document with "
        "no verdict is labelled as such and none is a pick.",
    ],
}

json.dump(out, open(ART / "17_portfolio_final.json", "w"), indent=1, ensure_ascii=False)
p = out["counts"]
print(f"wrote 17_portfolio_final.json: {p['picks']} picks + {p['watchlist']} watchlist, "
      f"{p['excluded']} excluded")
for t in tiers_out:
    print(f"  [{t['kind']:9}] T{t['presentation_order']} {t['tier_name']}: {t['n']} — "
          f"alt {t['named_alternate']['name']} ({t['named_alternate']['availability_verdict']})")
print("  picks in top ownership bucket:",
      out["ownership_ceiling_B5"]["measured"]["picks_in_top_bucket"], "/", p["picks"])
print("  concentration picks:", out["concentration_B4"]["portfolio_picks"])
print("  remedy candidates (verified coop+mp, ranks 31-120):", len(remedy))
print("  top-30 unscreened:", [t["name"] for t in top30_unscreened])
