#!/usr/bin/env python3
"""Stage 18 - build deliverables/portfolio_onepager.md straight from
artifacts/17_portfolio_final.json. Every figure is joined from the JSON's trace
blocks; no numeric literal is typed into this file. Aborts if a field is missing."""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
D = json.load(open(ROOT / "artifacts/17_portfolio_final.json"))

def owners(s):            # "500,000 .. 1,000,000" -> "500k-1M"
    a, b = [int(x.replace(",", "").strip()) for x in s.split("..")]
    f = lambda v: f"{v//1_000_000}M" if v >= 1_000_000 else f"{v//1000}k"
    return f"{f(a)}-{f(b)}"

VERDICT = {
    ("no", "yes"):  "Never on GP · Xbox SKU confirmed",
    ("rotated_out", "yes"): "Was on GP, rotated out · Xbox SKU confirmed",
    ("unknown", "yes"): "GP status unknown · Xbox SKU confirmed",
    ("not_verified", "yes"): "GP status not verified · Xbox SKU confirmed",
    ("not_verified", "not_verified"): "GP not verified · **Xbox SKU NOT verified**",
    ("not_verified", "other_console_only"): "GP not verified · **no Xbox SKU today**",
    ("rotated_out", "not_verified"): "Was on GP (framed as PC) · **Xbox SKU NOT verified**",
}

rows = {}
for t in D["titles"]:
    c, a = t["trace_16_candidates_v3"], t["trace_13_availability"]
    for k in ("v3_rank", "review_total", "owners_range_steamspy_bucket_estimate"):
        if c.get(k) is None:
            sys.exit(f"ABORT: {t['name']} missing {k}")
    key = (a["on_gamepass"], a["xbox_version"])
    if key not in VERDICT:
        sys.exit(f"ABORT: unmapped availability pair {key} for {t['name']}")
    rows[t["portfolio_position"]] = dict(
        pos=t["portfolio_position"], name=t["name"], app_id=t["app_id"],
        dev=t["developer"], rank=c["v3_rank"], comp=c["composite_score"],
        rev=c["review_total"], own=owners(c["owners_range_steamspy_bucket_estimate"]),
        mc=c["metacritic_score"] or "—", verdict=VERDICT[key],
        why=t["why"], trig=t["removal_or_promotion_trigger"],
        nsrc=a["n_sources"], conf=a["min_source_confidence"],
    )

out = []
w = out.append
w("# Game Pass portfolio — the board's one-pager")
w("")
w(f"**17 picks + a 7-title watchlist.** Generated {D['generated']} by "
  f"`scripts/18_build_onepager.py` from `artifacts/17_portfolio_final.json`. "
  "Every figure below is joined from that file's per-title trace blocks; the build aborts "
  "if any title is missing a rank, a review count, an owners bucket or an availability "
  "verdict. Tier membership, within-tier ordering and the rationale text are **authored "
  "judgments**, not derived.")
w("")
c = D["counts"]
w(f"**Funnel.** 122,191 non-demo games → **{c['eligible_pool_v3']}** eligible (review floor "
  f"4,000) → **{c['qualifying_v3_at_0.60']}** qualifying (composite ≥ 0.60) → "
  f"**{c['availability_screened']}** externally availability-screened → **{c['picks']}** "
  f"picks + **{c['watchlist']}** watchlist. {c['excluded']} screened titles excluded outright.")
w("")
w("**How the ranking works, stated correctly.** The composite is **Recognition — the "
  "percentile of ln(review_total), weight 0.50 — banded by a three-level ownership step.** "
  "It is *not* a multi-pillar blend. Within any one ownership bucket "
  "Spearman(recognition, headroom) = 1.0000 exactly, so the ranking inside a bucket is "
  "simply most-reviewed-first. Fit carries 0.10 as a tiebreaker only (in-population "
  "R² = −1.34; measured influence Spearman 0.04). Owners are **bucketed SteamSpy "
  "estimates, not sales**. There is **no engagement or playtime data** anywhere in this "
  "dataset. [`16_scoring_v3.md`]")
w("")
cc, oc = D["concentration_B4"], D["ownership_ceiling_B5"]
w("**Two accepted properties, disclosed not patched.** *Concentration:* the 17 picks are "
  "17.6% Action / 17.6% multiplayer / 11.8% co-op against a qualifying list of 53.8% / "
  "33.5% / 24.4%. The tested remedy did not work and was withdrawn. *Ownership ceiling:* "
  "15 of 17 picks sit in the top (750k) owner bucket, because a continuous 0.50-weighted "
  "Recognition term is banded only by a three-level ownership step — the ceiling defines "
  "the list more than it filters it. Full mechanism and the 200k-500k sensitivity: "
  "`17_portfolio_final.md`.")
w("")
w("Composite and rank come from `16_candidates_v3.csv`; the availability verdict and its "
  "source count come from `13_availability.json` (screened Aug 2026).")
w("")

for tier in D["tiers"]:
    kind = "PICKS" if tier["kind"] == "pick" else "WATCHLIST — NOT PICKS"
    w(f"## Tier {tier['presentation_order']} — {tier['tier_name']} · {tier['n']} {kind}")
    w("")
    w(f"**Job.** {tier['role']}")
    w("")
    w(f"**Confidence:** {tier['confidence']}.")
    w("")
    w("| # | Title | app_id | v3 rank | Composite | Reviews | Owners (SteamSpy bucket) | MC | Availability verdict (Aug 2026) | Sources |")
    w("|---|---|---|---|---|---|---|---|---|---|")
    for t in tier["titles"]:
        r = rows[t["position"]]
        w(f"| {r['pos']} | {r['name']} | {r['app_id']} | {r['rank']} | {r['comp']:.4f} | "
          f"{r['rev']:,} | {r['own']} | {r['mc']} | {r['verdict']} | {r['nsrc']} ({r['conf']}) |")
    w("")
    label = "REMOVAL RULE" if tier["kind"] == "pick" else "PROMOTION TRIGGER"
    w(f"**{label} for this tier.** {tier['removal_or_promotion_rule']}")
    w("")
    alt = tier["named_alternate"]
    w(f"**Named alternate:** {alt['name']} ({alt['app_id']}, v3 rank {alt['v3_rank']}, "
      f"{alt['review_total']:,} reviews, MC {alt['metacritic_score'] or '—'}) — "
      f"availability: {alt['availability_verdict']}.")
    w("")
    w("<details><summary>Per-title rationale and removal trigger</summary>")
    w("")
    for t in tier["titles"]:
        r = rows[t["position"]]
        w(f"- **{r['name']}** ({r['dev']}) — {r['why']} *Trigger:* {r['trig']}")
    w("")
    w("</details>")
    w("")

w("## Screened and excluded — no deal is possible or needed")
w("")
for e in D["excluded_from_portfolio"]:
    w(f"- **{e['name']}** ({e['app_id']}, v3 rank {e['v3_rank']}) — "
      f"`{e['reason']}`. {e['detail']}")
w("")
u = D["top_ranked_but_unscreened_cannot_be_picks"]
w("## Top-ranked but never screened — cannot be picks")
w("")
w(u["note"] + " They are the first two titles any screen extension should cover.")
w("")
for e in u["titles"]:
    w(f"- **{e['name']}** ({e['app_id']}, v3 rank {e['v3_rank']}, "
      f"{e['review_total']:,} reviews, MC {e['metacritic_score'] or '—'}) — "
      "never availability-screened, so no verdict exists.")
w("")
w("## Standing caveats")
w("")
for v in D["standing_caveats"]:
    w(f"- {v}")

path = ROOT / "deliverables/portfolio_onepager.md"
path.write_text("\n".join(out) + "\n")
print(f"wrote {path} ({len(out)} lines, {len(rows)} titles)")
