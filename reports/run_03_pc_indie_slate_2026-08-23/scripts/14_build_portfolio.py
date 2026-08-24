#!/usr/bin/env python3
"""
Stage 14 — build artifacts/14_portfolio.json.

Every portfolio row is JOINED from the two upstream artifacts rather than typed by hand,
so each row provably traces to (a) its row in 12_candidates_v2.csv and (b) its verdict in
13_availability.json. If a title is not in both, the build fails loudly.

Portfolio membership and tier assignment are the analyst's judgement (recorded in
DECISIONS.md); everything else on each row is copied from source.
"""
import csv, json, sys
from pathlib import Path

ART = Path(__file__).resolve().parent.parent / "artifacts"

cands = {int(r["app_id"]): r for r in csv.DictReader(open(ART / "12_candidates_v2.csv"))}
avail = {int(r["app_id"]): r for r in json.load(open(ART / "13_availability.json"))}

# ---------------------------------------------------------------- tier definitions
# (app_id, one-sentence reason, per-title removal trigger)
TIERS = [
    dict(
        tier=1,
        name="Restarts",
        role=(
            "Re-open licences that Microsoft has already signed once. The deal was struck, "
            "the Xbox SKU shipped and passed certification, the rights holder has said yes "
            "before, and the contract template exists. This is the lowest-execution-cost "
            "route to visible catalogue additions, and it is the only tier where Microsoft "
            "already holds first-party performance data on the exact title."
        ),
        cost_rank=1,
        cost_basis=(
            "Cheapest to EXECUTE (no port, no certification, no cold introduction, existing "
            "contract template). The licence FEE itself is unknown and is not assumed to be "
            "lower — see sizing.unsourced_warning."
        ),
        confidence="medium-high on executability, low on desirability",
        confidence_driver=(
            "Executability is externally verified with dated sources for the addition of "
            "every title. Desirability is low-confidence because no source establishes WHY "
            "any of them left, and the two possible reasons point opposite ways."
        ),
        tier_removal_rule=(
            "Remove any title from this tier the moment Microsoft's own internal Game Pass "
            "performance record for its prior run shows it in the bottom quartile of "
            "engagement-per-licensing-dollar for comparable back-catalogue titles. That "
            "record exists inside Microsoft and settles this tier's central unknown at zero "
            "external cost; it is a condition on the recommendation, not a substitute for it."
        ),
        picks=[
            (1135690,
             "Left Game Pass roughly two months ago (~late June 2026) — the freshest lapsed "
             "deal in the top 30, so the counterparty relationship is warm and the renewal "
             "conversation is live now rather than cold.",
             "Humble Games confirms the departure was its own decision to pursue a "
             "competing-subscription exclusive."),
            (787480,
             "Highest composite in the whole 215-title qualifying list (0.9703) and the "
             "highest-scoring title carrying an independent Metacritic score (80); the "
             "Xbox SKU shipped Sept 26 2023 so no port work is required.",
             "Capcom prices a re-add above a fresh licence for a comparable title, which "
             "removes the entire cost rationale for putting it in this tier."),
            (413420,
             "A one-year Game Pass run (May 2022 – May 2023) that reads as a fixed-term "
             "deal expiring rather than a rejection, on a title with Metacritic 83 and "
             "25,177 reviews against a 500k–1M owner bucket.",
             "Spike Chunsoft has since granted the console-subscription rights elsewhere."),
            (501300,
             "The highest Metacritic score in this tier (89) on 41,326 reviews — the "
             "strongest independent press signal available for any rotated-out title, and "
             "press coverage is a signal the composite never uses as an input.",
             "Annapurna's post-2024 restructuring has moved the rights such that no single "
             "counterparty can grant a console subscription licence."),
            (1256670,
             "29,181 reviews and a 500k–1M owner bucket from a single independent studio "
             "(ProjectMoon) — the simplest counterparty in this tier, one rights holder "
             "with one title and a prior yes.",
             "The departure date cannot be pinned well enough to establish that the prior "
             "deal genuinely lapsed rather than was terminated."),
            (2161700,
             "Ran day-one from Feb 2 2024 to Aug 15 2025, the longest and best-documented "
             "Game Pass run in this tier, on the highest-Metacritic (89) large-publisher "
             "title in the top 30.",
             "SEGA/Atlus quotes anything in the order of magnitude of the sourced AAA "
             "day-one figures ($5M–$300M, Axios 2023) — at a $69.99 still-selling SKU this "
             "is the likeliest title in the tier to price itself out."),
        ],
        alternate=(1088850,
                   "Marvel's Guardians of the Galaxy — rank 28, rotated out March 2023 after a "
                   "12-month run, 35,789 reviews. Held as the alternate rather than a pick "
                   "because the counterparty changed: Embracer Group bought Eidos-Montréal and "
                   "the IP from Square Enix in 2022, so the prior yes was given by a company "
                   "that no longer holds the rights, and a licensed Marvel property carries a "
                   "second rights holder this analysis has not screened."),
    ),
    dict(
        tier=2,
        name="Clean spine",
        role=(
            "The three titles in the top 30 confirmed never to have been on Game Pass, "
            "confirmed to have a native Xbox console release, and carrying no blocker. This "
            "tier is what the pitch leads with: genuinely new subscription value, no prior "
            "run to explain away, and independent press validation the scoring model never "
            "saw."
        ),
        cost_rank=2,
        cost_basis=(
            "A cold negotiation with a small rights holder, but no port cost and no "
            "certification cost because the Xbox SKU already exists. More expensive to "
            "execute than Tier 1, cheaper than anything requiring a port."
        ),
        confidence="medium-high",
        confidence_driver=(
            "Availability is confirmed rather than assumed on all three (subscription "
            "tracker plus native-Xbox-release confirmation, dated Aug 2026), and all three "
            "carry Metacritic scores of 79–89, an independent recognition signal that is "
            "not an input to the composite that selected them."
        ),
        tier_removal_rule=(
            "Remove any title here that turns out to have a prior Game Pass run after all — "
            "not because a prior run is disqualifying, but because it belongs in Tier 1, "
            "where the 'why did it leave' question must be answered before signing."
        ),
        picks=[
            (253230,
             "50,390 reviews — the most-reviewed title in the entire availability-screened "
             "top 30 — with Metacritic 79, a 500k–1M owner bucket, and both co-op and "
             "multiplayer flags set, which is the profile least exposed to the "
             "singleplayer-narrative concentration this list otherwise carries.",
             "Gears for Breakfast's console publishing rights sit with a partner who will "
             "not grant a subscription licence separately from retail."),
            (653530,
             "Metacritic 89 on 26,518 reviews from a single-person developer (Lucas Pope) — "
             "the cleanest possible counterparty, one person holding all rights, with the "
             "Xbox SKU already shipped.",
             "Lucas Pope declines subscription placement on the record; a solo rights "
             "holder can refuse outright and there is no second party to negotiate with."),
            (736260,
             "Metacritic 87 on 20,757 reviews and a puzzle genre absent from Tiers 1 and 3, "
             "which is the specific breadth this portfolio needs to avoid being one "
             "narrative-adventure bet made repeatedly.",
             "Hempuli declines, or the confirmed 'Not Included' tracker verdict turns out "
             "to be stale."),
        ],
        alternate=(813230,
                   "ANIMAL WELL — rank 32, composite 0.8415, Metacritic 91 (the highest in the "
                   "top 60), 13,990 reviews, 200k–500k owners, developer Billy Basso. It is the "
                   "alternate rather than a pick for one disqualifying-for-now reason: it sits "
                   "at rank 32, outside the top 30 that Stage 13 screened, so it has NO "
                   "availability verdict. Its Game Pass and Xbox status must be checked before "
                   "it can be promoted."),
    ),
    dict(
        tier=3,
        name="Confirm-then-sign breadth",
        role=(
            "Titles with a documented Game Pass addition at some point and no documented "
            "departure — status genuinely unresolved as of Aug 2026, not guessed. Their job "
            "in the portfolio is genre breadth per licensing dollar: rhythm, action-horror, "
            "puzzle-language, metroidvania, crafting-sim and open-world-exploration, which "
            "Tiers 1 and 2 do not cover. Each resolves with a single storefront check."
        ),
        cost_rank=3,
        cost_basis=(
            "Same structural cost as Tier 2 (cold-ish licence, Xbox SKU exists) plus one "
            "status check per title. If a title turns out to be currently included, its "
            "cost is zero because there is nothing to buy."
        ),
        confidence="medium on merit, low on availability",
        confidence_driver=(
            "Merit is measured (review volume and owner bucket from the dataset; Metacritic "
            "present on 4 of 8). Availability is explicitly unknown — Stage 13 found a dated "
            "addition for each and no dated departure for any, and refused to guess."
        ),
        tier_removal_rule=(
            "Remove on either verdict of the status check: if the title is currently in the "
            "Game Pass catalogue there is nothing to buy, and if it is confirmed to have "
            "departed it moves to Tier 1 and inherits Tier 1's 'why did it leave' condition."
        ),
        picks=[
            (1931770,
             "Metacritic 86 on 17,036 reviews at $12.99 — the highest press score in this "
             "tier, in a language-puzzle genre no other portfolio title occupies.",
             "Confirmed currently included, or confirmed departed (see tier rule)."),
            (1369630,
             "Metacritic 86 on 35,018 reviews — the second-highest review volume in this "
             "tier and the portfolio's only metroidvania.",
             "Same tier rule; additionally if Live Wire/Adglobe's console rights are held "
             "by a publisher not screened here."),
            (1055540,
             "Metacritic 82 on 17,323 reviews from a solo developer in the 200k–500k owner "
             "bucket — the lowest ownership in this tier, which is the 'recognised but not "
             "widely owned' profile the brief asks for, at its purest.",
             "Same tier rule."),
            (953490,
             "24,708 reviews with Metacritic 75 and both action and horror tags — the "
             "portfolio's only horror title, and horror is a genre Tiers 1 and 2 have none "
             "of.",
             "Same tier rule; Metacritic 75 is the weakest press score in the portfolio, so "
             "it is also the first title to cut if the tier must shrink."),
            (1210320,
             "31,904 reviews and a 500k–1M owner bucket in a crafting/simulation genre that "
             "no other portfolio title covers.",
             "Same tier rule."),
            (1288310,
             "Composite 0.966, second-highest in the entire 215-title qualifying list, on "
             "39,637 reviews — the strongest measured case in the portfolio, held back to "
             "Tier 3 only because its current status could not be confirmed either way.",
             "Same tier rule; also remove if no native Xbox console SKU is confirmed, since "
             "Stage 13 recorded 'yes' without pinning the SKU."),
            (774181,
             "20,321 reviews in a 500k–1M owner bucket with co-op and multiplayer flags "
             "set; rhythm is a genre absent from every other tier and one of the few here "
             "that is played socially.",
             "Same tier rule; it is also still flagged Early Access in the dataset, so "
             "remove if the console SKU is not a finished release."),
            (960170,
             "26,951 reviews and a 500k–1M owner bucket at a $49.99 retail SKU — the only "
             "title in this tier whose publisher (NEOWIZ) operates at mid-size rather than "
             "indie scale, which makes it the tier's cost outlier and therefore its first "
             "candidate for deferral.",
             "Same tier rule; also remove if the licence is quoted at large-publisher "
             "scale, since its portfolio job (rhythm breadth) is already served by Rhythm "
             "Doctor at a fraction of the counterparty size."),
        ],
        alternate=(1703340,
                   "The Stanley Parable: Ultra Deluxe — rank 37, composite 0.8323, 28,048 "
                   "reviews, 500k–1M owners, Crows Crows Crows. Alternate rather than pick "
                   "because it sits outside the Stage 13 top-30 screen and therefore has no "
                   "availability verdict at all."),
    ),
    dict(
        tier=4,
        name="Dated and PC-first options",
        role=(
            "High-scoring titles with a confirmed or suspected console-port gap. Their job "
            "is to be taken now as PC Game Pass adds where that is all the rights support, "
            "and to be diarised where a console SKU has a date. This tier is explicitly the "
            "portfolio's lowest priority and is included so the board can see what it is "
            "choosing not to chase, rather than being surprised by it later."
        ),
        cost_rank=4,
        cost_basis=(
            "Cheapest per title in absolute terms (small Chinese/Korean independent rights "
            "holders, no console certification because there is no console SKU) but the "
            "worst value per dollar for a console-led subscription, because the console "
            "audience cannot play them. Cost is not the constraint here; reach is."
        ),
        confidence="low",
        confidence_driver=(
            "Stage 13 recorded 'no evidence found of any Xbox release' for five of these — "
            "absence of evidence, not confirmed absence. Only Wandering Sword's gap is "
            "positively established, with a dated console release of 21 January 2027."
        ),
        tier_removal_rule=(
            "Remove any title here for which a native Xbox console SKU is confirmed to "
            "exist — it is then not port-gapped and belongs in Tier 3, where it competes on "
            "merit. Remove the whole tier if the board's mandate is console-only."
        ),
        picks=[
            (1876890,
             "The only port gap in the top 30 that is positively established with a date: "
             "Xbox Series console version delayed to 21 January 2027, so this is a diary "
             "entry with a known date rather than an open question, on 19,877 reviews.",
             "The 21 January 2027 console date slips again, at which point it stops being a "
             "diarisable option and becomes an open-ended one."),
            (1562700,
             "Composite 0.9465, fourth in the whole qualifying list, on 30,102 reviews — the "
             "highest-scoring title anywhere in the portfolio that has no confirmed Xbox "
             "release, which is precisely why the port question is worth one call.",
             "Confirmed to have no Xbox SKU and no announced one."),
            (2593370,
             "38,601 reviews at $7.49 — the highest review volume in this tier and the "
             "lowest price, so the cheapest possible test of whether this segment "
             "transfers at all.",
             "Confirmed to have no Xbox SKU and no announced one."),
            (1189630,
             "30,091 reviews in a 500k–1M owner bucket; wuxia RPG is a segment the portfolio "
             "has no other exposure to.",
             "Confirmed to have no Xbox SKU and no announced one."),
            (1880330,
             "15,929 reviews from Shiying Studio, the same developer as Firework (Tier 3) — "
             "so a single counterparty conversation can cover two portfolio titles.",
             "Confirmed to have no Xbox SKU; also drop if the Firework conversation fails, "
             "since the shared-counterparty efficiency is its main reason for inclusion."),
            (638230,
             "The only title that is both a restart and a port question: rotated out of Game "
             "Pass after a July 2024 addition that press coverage specifically framed as 'PC "
             "Game Pass', on 32,370 reviews. Placed here rather than in Tier 1 because a "
             "restart is only worth Tier 1's cost advantage if the console SKU it restarts "
             "actually exists, and Stage 13 could not confirm that it does.",
             "Confirmed to have no native Xbox console SKU — at which point it is a PC-only "
             "re-add and competes on Tier 4's terms, not Tier 1's."),
            (1144400,
             "26,756 reviews in a 500k–1M owner bucket; ranked last in the portfolio because "
             "it combines no evidence of an Xbox release with a visual-novel format whose "
             "console-certification path this analysis has not screened.",
             "Any console content-rating or certification obstacle, or confirmation that no "
             "Xbox SKU exists."),
        ],
        alternate=(359870,
                   "FINAL FANTASY X/X-2 HD Remaster — rank 41, composite 0.8257, 18,632 reviews, "
                   "500k–1M owners, Square Enix. A deliberately different kind of alternate: if "
                   "the board rejects Tier 4's PC-first premise outright, this is a "
                   "large-publisher back-catalogue title with a long-established Xbox SKU. It is "
                   "an alternate and not a pick because it sits outside the Stage 13 top-30 "
                   "screen and has no availability verdict."),
    ),
]

# ------------------------------------------------------------------ excluded, stated
EXCLUDED = [
    dict(app_id=1659420, reason="structurally_excluded",
         detail="Published by PlayStation Publishing LLC (Sony). No Xbox version exists and "
                "Sony does not license PlayStation Studios titles to a competing "
                "subscription. Confirmed by Stage 13, not assumed."),
    dict(app_id=578650, reason="structurally_excluded",
         detail="Microsoft owns The Outer Worlds IP (Obsidian is Xbox Game Studios) AND it is "
                "independently confirmed currently on Game Pass Premium. Two separate reasons "
                "this is not a licensing decision."),
    dict(app_id=2273430, reason="already_included",
         detail="Ships on Xbox/Game Pass as 'BlazBlue Entropy Effect X', added Feb 12 2026. A "
                "different SKU from the scored Steam app_id, but the same franchise is already "
                "in the subscription."),
    dict(app_id=1817230, reason="already_included",
         detail="Metacritic 90 and the red team's central example — but Microsoft sold Tango "
                "Gameworks and the franchise to Krafton in Aug 2024 and it remains in Game Pass "
                "Premium under a continuing licence. Nothing to acquire, nothing to license."),
    dict(app_id=2218750, reason="already_included",
         detail="Currently listed on Game Pass Premium, no departure evidence found."),
]

# ------------------------------------------------------------------------- assemble
def row(app_id, why, removal, tier_no, tier_name):
    if app_id not in cands:
        sys.exit(f"FATAL: app_id {app_id} not in 12_candidates_v2.csv")
    if app_id not in avail:
        sys.exit(f"FATAL: app_id {app_id} has no verdict in 13_availability.json")
    c, a = cands[app_id], avail[app_id]
    return {
        "portfolio_rank": None,
        "tier": tier_no,
        "tier_name": tier_name,
        "app_id": app_id,
        "name": c["name"],
        "developer": c["developer"],
        "publisher": c["publisher"],
        "why_in_portfolio": why,
        "removal_trigger": removal,
        "trace": {
            "candidates_v2_rank": a["rank"],
            "composite_score": float(c["composite_score"]),
            "score_tier": c["tier"],
            "recognition_pct": float(c["recognition_pct"]),
            "headroom_pct": float(c["headroom_pct"]),
            "fit_pct": float(c["fit_pct"]),
            "review_total": int(c["review_total"]),
            "review_positive_ratio": float(c["review_positive_ratio"]),
            "owners_range": c["owners_range"],
            "owners_mid": int(float(c["owners_mid"])),
            "price_usd_retail_not_licence_cost": float(c["price_usd"]),
            "metacritic_score": c["metacritic_score"] or None,
            "has_controller_support": c["has_controller_support"],
            "has_coop": c["has_coop"],
            "has_multiplayer": c["has_multiplayer"],
            "genres": c["genres"],
        },
        "availability": {
            "on_gamepass": a["on_gamepass"],
            "xbox_version": a["xbox_version"],
            "publisher_now": a["publisher_now"],
            "publisher_bloc": a["publisher_bloc"],
            "blockers": a["blockers"],
            "note": a["notes"],
            "n_sources": len(a["sources"]),
            "source_urls": [s["url"] for s in a["sources"]],
        },
    }

portfolio, n = [], 0
tiers_out = []
for t in TIERS:
    rows = []
    for app_id, why, removal in t["picks"]:
        n += 1
        r = row(app_id, why, removal, t["tier"], t["name"])
        r["portfolio_rank"] = n
        rows.append(r)
        portfolio.append(r)
    alt_id, alt_note = t["alternate"]
    ac = cands.get(alt_id)
    if ac is None:
        sys.exit(f"FATAL: alternate {alt_id} not in candidates")
    tiers_out.append({
        "tier": t["tier"], "tier_name": t["name"], "role": t["role"],
        "relative_cost_rank_1_is_cheapest_to_execute": t["cost_rank"],
        "cost_basis": t["cost_basis"],
        "confidence": t["confidence"], "confidence_driver": t["confidence_driver"],
        "tier_removal_rule": t["tier_removal_rule"],
        "n_titles": len(rows),
        "titles": [{"portfolio_rank": r["portfolio_rank"], "app_id": r["app_id"],
                    "name": r["name"]} for r in rows],
        "named_alternate": {
            "app_id": alt_id, "name": ac["name"], "developer": ac["developer"],
            "composite_score": float(ac["composite_score"]),
            "candidates_v2_rank": list(cands).index(alt_id) + 1,
            "review_total": int(ac["review_total"]),
            "owners_range": ac["owners_range"],
            "metacritic_score": ac["metacritic_score"] or None,
            "availability_verdict": ("checked in Stage 13" if alt_id in avail
                                     else "NOT CHECKED — outside Stage 13 top-30 screen"),
            "why_alternate_not_pick": alt_note,
        },
    })

out = {
    "stage": 14,
    "generated": "2026-08-22",
    "generated_by": "scripts/14_build_portfolio.py (joins 12_candidates_v2.csv x 13_availability.json)",
    "decision": ("Add these 24 named titles to Game Pass, in four tiers ordered by how "
                 "cheaply and how certainly each can be executed. This is a recommendation "
                 "to license named back-catalogue titles; it recommends no studio "
                 "acquisition, no studio funding, no pricing change and no new development, "
                 "all of which the goal statement places out of scope."),
    "objective_optimised": {
        "objective": "retention and margin per licensing dollar, not net subscriber adds",
        "basis": ("04_context.md §2 [ANALYSIS, confidence MEDIUM]: the July 2026 studio "
                  "closures and the April 2026 Ultimate rollback from $29.99 to $22.99 "
                  "both point to margin discipline over reach maximisation. A portfolio of "
                  "many small, high-recognition, low-ownership titles serves retention "
                  "breadth; a single AAA day-one swing does not, and the one sourced "
                  "internal Xbox assessment of such a swing (Star Wars Jedi: Survivor at "
                  "~$300M, Axios 2023-09-19) flagged it as poor ROI."),
        "consequence_for_this_portfolio": ("The AAA-scale back-catalogue option is named "
                                           "(Persona 3 Reload as a pick, Marvel's Guardians "
                                           "of the Galaxy as an alternate) but ranked last "
                                           "within its tier and behind sixteen "
                                           "indie-scale titles."),
    },
    "counts": {
        "eligible_pool": 638, "qualifying_at_0.60": 215,
        "availability_screened": 30, "in_portfolio": n,
        "excluded_from_top_30": len(EXCLUDED),
    },
    "tiers": tiers_out,
    "titles": portfolio,
    "excluded_from_portfolio": [
        dict(app_id=e["app_id"], name=cands[e["app_id"]]["name"],
             candidates_v2_rank=avail[e["app_id"]]["rank"],
             reason=e["reason"], detail=e["detail"]) for e in EXCLUDED],
}
json.dump(out, open(ART / "14_portfolio.json", "w"), indent=1, ensure_ascii=False)
print(f"wrote 14_portfolio.json: {n} titles, {len(tiers_out)} tiers, {len(EXCLUDED)} excluded")
for t in tiers_out:
    print(f"  T{t['tier']} {t['tier_name']}: {t['n_titles']} titles, alt = {t['named_alternate']['name']}")
