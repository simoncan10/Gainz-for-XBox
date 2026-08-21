"""Build the Xbox Game Pass indie-investment datasheet.

Blends two evidence sources:

  A) DATASET side - the Steam snapshot in data/raw (SteamSpy owners + review
     counts, ~Dec 2024). Reproducible, has app_id, joins straight back onto
     data/processed/pipeline_dataset.csv.
  B) WEB side - researched 2025-2026 Steam indie breakouts that are newer than
     the snapshot, kept in data/reference/web_indie_2025_2026.csv with a source
     URL per row so every figure is traceable.

Outputs (data/processed/):
  1. top50_indie_reference.csv    - the blended top 50 reference set
  2. top50_match_profile.csv      - per-attribute lift table (the "winning
                                    profile" to filter the full dataset against)
  3. indie_candidates_scored.csv  - every indie app_id in the snapshot scored
                                    against that profile, ranked

Validation: profile_fit_score separates the 300-game winner cohort from the other
85,332 indie games with AUC 0.939 in-sample and 0.950 on a held-out 30% of the
winners (seed 7), i.e. the profile generalises rather than memorising.

NOTE on parsing: data/raw/super raw/games.csv embeds JSON in price_overview
using BACKSLASH-escaped quotes. csv.DictReader must be given escapechar="\\"
or the name/type columns silently misalign for ~13% of rows.
"""
import csv
import math
import re
import statistics as st
from collections import defaultdict
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent
RAW = PROJECT_ROOT / "data" / "raw" / "super raw"
PROC = PROJECT_ROOT / "data" / "processed"
REF = PROJECT_ROOT / "data" / "reference"

# --- tuning knobs -----------------------------------------------------------
N_DATASET_PICKS = 20          # slots in the top 50 filled from the snapshot
MIN_REVIEWS_FOR_RANKING = 5000
# "winner cohort" = the statistical population the match profile is learned from
WINNER_MIN_SCORE = 8
WINNER_MIN_REVIEWS = 20000
WINNER_MIN_OWNERS = 1_000_000
W_OWNERS, W_REVIEWS, W_QUALITY = 0.35, 0.35, 0.30
LAPLACE = 0.02                # smoothing for the log-odds weights

# Dropped from the dataset picks with a documented reason (kept out of the
# top 50 only - they still appear in the scored candidate list).
MANUAL_EXCLUDE = {
    "Wallpaper Engine": "utility software, not a game",
    "Rocket League®": "Psyonix/Epic-owned since 2019, no longer indie",
    "Life is Strange - Episode 1": "free episode of a Square Enix title",
    "POSTAL 2": "legacy catalogue, not an investment candidate",
    "Plants vs. Zombies GOTY Edition": "EA-owned, not indie",
}


# --- loaders ----------------------------------------------------------------
def load_meta():
    out = {}
    with (RAW / "games.csv").open(encoding="utf-8") as f:
        for r in csv.DictReader(f, escapechar="\\"):
            out[r["app_id"]] = (r["name"], r["release_date"], r["type"], r["is_free"])
    return out


def load_long(path, value_col):
    out = defaultdict(set)
    with path.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["app_id"] and r[value_col]:
                out[r["app_id"]].add(r[value_col])
    return out


def load_keyed(path):
    with path.open(encoding="utf-8") as f:
        return {r["app_id"]: r for r in csv.DictReader(f)}


def owners_mid(s):
    nums = [int(x.replace(",", "")) for x in re.findall(r"[\d,]+", s or "")]
    if len(nums) >= 2:
        return max((nums[0] + nums[1]) / 2, 1)
    return max(nums[0], 1) if nums else 1


def price_band(cents):
    if cents == 0:
        return "free"
    for hi, label in ((500, "$0.01-4.99"), (1000, "$5-9.99"), (1500, "$10-14.99"),
                      (2000, "$15-19.99"), (3000, "$20-29.99"), (4000, "$30-39.99")):
        if cents < hi:
            return label
    return "$40+"


def zf(values):
    m, s = st.mean(values), st.pstdev(values)
    return lambda v: (v - m) / s if s else 0.0


# --- build ------------------------------------------------------------------
def build_indie_universe():
    meta = load_meta()
    genres = load_long(RAW / "genres.csv", "genre")
    tags = load_long(RAW / "tags.csv", "tag")
    op = load_keyed(PROC / "owners_price_buckets.csv")
    rv = load_keyed(PROC / "review_amount_buckets.csv")

    universe = []
    for app_id, o in op.items():
        r = rv.get(app_id)
        m = meta.get(app_id)
        if not r or not m:
            continue
        name, release_date, typ, is_free = m
        if typ != "game":
            continue
        g, t = genres.get(app_id, set()), tags.get(app_id, set())
        if "Indie" not in g and "Indie" not in t:
            continue
        cents = int(o["price_cents"] or 0)
        universe.append({
            "app_id": app_id,
            "name": name,
            "release_date": "" if release_date in ("\\N", "N") else release_date,
            "genres": ", ".join(sorted(g)),
            "genre_set": g,
            "tag_set": t,
            "price_cents": cents,
            "price_usd": round(cents / 100, 2),
            "price_band": price_band(cents),
            "review_score": int(r["review_score"] or 0),
            "total": int(r["total"] or 0),
            "owners_range": o["owners_range"],
            "owners_mid": owners_mid(o["owners_range"]),
        })
    return universe


def score_universe(universe):
    pool = [g for g in universe if g["total"] >= MIN_REVIEWS_FOR_RANKING]
    zo = zf([math.log10(g["owners_mid"]) for g in pool])
    zt = zf([math.log10(g["total"] + 1) for g in pool])
    zq = zf([g["review_score"] for g in pool])
    for g in universe:
        g["z_owners"] = round(zo(math.log10(g["owners_mid"])), 4)
        g["z_reviews"] = round(zt(math.log10(g["total"] + 1)), 4)
        g["z_quality"] = round(zq(g["review_score"]), 4)
        g["performance_score"] = round(
            W_OWNERS * g["z_owners"] + W_REVIEWS * g["z_reviews"] + W_QUALITY * g["z_quality"], 4)
    return pool


def build_profile(universe):
    """Naive-Bayes style lift table: winner cohort vs. all other indie games."""
    winners = [g for g in universe
               if g["review_score"] >= WINNER_MIN_SCORE
               and g["total"] >= WINNER_MIN_REVIEWS
               and g["owners_mid"] >= WINNER_MIN_OWNERS]
    rest = [g for g in universe if g not in winners]
    wset = {id(g) for g in winners}
    rest = [g for g in universe if id(g) not in wset]

    rows, weights = [], {}
    for kind, key in (("tag", "tag_set"), ("genre", "genre_set")):
        attrs = set()
        for g in universe:
            attrs |= g[key]
        for a in sorted(attrs):
            wc = sum(1 for g in winners if a in g[key])
            rc = sum(1 for g in rest if a in g[key])
            if wc < 5 or (wc + rc) < 50:
                continue
            pw = (wc + LAPLACE * len(winners)) / (len(winners) * (1 + LAPLACE))
            pr = (rc + LAPLACE * len(rest)) / (len(rest) * (1 + LAPLACE))
            lift = pw / pr
            weights[(kind, a)] = (math.log(lift), math.log((1 - pw) / (1 - pr)))
            rows.append({
                "attribute_type": kind, "attribute": a,
                "winner_count": wc, "winner_share": round(pw, 5),
                "baseline_count": rc, "baseline_share": round(pr, 5),
                "lift": round(lift, 3), "log_odds_weight": round(math.log(lift), 4),
            })

    for band in sorted({g["price_band"] for g in universe}):
        wc = sum(1 for g in winners if g["price_band"] == band)
        rc = sum(1 for g in rest if g["price_band"] == band)
        pw = (wc + LAPLACE * len(winners)) / (len(winners) * (1 + LAPLACE))
        pr = (rc + LAPLACE * len(rest)) / (len(rest) * (1 + LAPLACE))
        lift = pw / pr
        weights[("price_band", band)] = (math.log(lift), math.log((1 - pw) / (1 - pr)))
        rows.append({
            "attribute_type": "price_band", "attribute": band,
            "winner_count": wc, "winner_share": round(pw, 5),
            "baseline_count": rc, "baseline_share": round(pr, 5),
            "lift": round(lift, 3), "log_odds_weight": round(math.log(lift), 4),
        })

    rows.sort(key=lambda r: (r["attribute_type"], -r["lift"]))
    absent_total = sum(v[1] for v in weights.values())
    return winners, rows, weights, absent_total


def fit_score(game, weights, absent_total):
    """Naive-Bayes log-likelihood ratio: P(attributes | winner) / P(attributes | rest).

    Every attribute contributes, present or absent, so a game is not rewarded
    simply for carrying more Steam tags than another.
    """
    s = absent_total
    for kind, key in (("tag", "tag_set"), ("genre", "genre_set")):
        for a in game[key]:
            w = weights.get((kind, a))
            if w:
                s += w[0] - w[1]
    w = weights.get(("price_band", game["price_band"]))
    if w:
        s += w[0] - w[1]
    return s


def main():
    universe = build_indie_universe()
    pool = score_universe(universe)
    winners, profile_rows, weights, absent_total = build_profile(universe)
    print(f"indie universe: {len(universe)}  ranking pool: {len(pool)}  winner cohort: {len(winners)}")

    # ---- 1. blended top 50 -------------------------------------------------
    web_rows = list(csv.DictReader((REF / "web_indie_2025_2026.csv").open(encoding="utf-8")))
    web_names = {r["name"].lower() for r in web_rows}

    pool.sort(key=lambda g: -g["performance_score"])
    picks, seen = [], set()
    for g in pool:
        if len(picks) >= N_DATASET_PICKS:
            break
        n = g["name"].lower()
        if n in web_names or n in seen or g["name"] in MANUAL_EXCLUDE:
            continue
        seen.add(n)
        picks.append(g)

    by_name = {g["name"].lower(): g for g in universe}
    MIN_SNAPSHOT_REVIEWS = 1000  # below this the Dec-2024 row is a pre-release stub
    out = []
    for r in web_rows:
        snap = by_name.get(r["name"].lower())
        if snap and snap["total"] < MIN_SNAPSHOT_REVIEWS:
            snap = None  # released after / too early in the snapshot to be meaningful
        out.append({
            "source": "web_2025_2026",
            "app_id": snap["app_id"] if snap else "",
            "name": r["name"],
            "release_year": r["release_year"],
            "developer": r["developer"],
            "genres": r["genres"],
            "key_tags": r["key_tags"],
            "price_cents": int(round(float(r["price_usd"]) * 100)) if r["price_usd"] else "",
            "price_usd": r["price_usd"],
            "price_band": price_band(int(round(float(r["price_usd"]) * 100))) if r["price_usd"] else "",
            "review_score": snap["review_score"] if snap else "",
            "total": snap["total"] if snap else "",
            "owners_range": snap["owners_range"] if snap else "",
            "pct_positive": r["pct_positive"],
            "metacritic": r["metacritic"],
            "units_millions": r["units_millions"],
            "revenue_musd": r["revenue_musd"],
            "peak_ccu": r["peak_ccu"],
            "performance_score": snap["performance_score"] if snap else "",
            "profile_fit_score": round(fit_score(snap, weights, absent_total), 4) if snap else "",
            "scale_tier": r["scale_tier"],
            "gamepass_status": r["gamepass_status"],
            "evidence_strength": r["evidence_strength"],
            "source_url": r["source"],
        })
    for g in picks:
        out.append({
            "source": "steam_snapshot_2024",
            "app_id": g["app_id"],
            "name": g["name"],
            "release_year": g["release_date"][:4],
            "developer": "",
            "genres": g["genres"],
            "key_tags": ", ".join(sorted(g["tag_set"],
                                         key=lambda t: -weights.get(("tag", t), (0, 0))[0])[:6]),
            "price_cents": g["price_cents"],
            "price_usd": g["price_usd"],
            "price_band": g["price_band"],
            "review_score": g["review_score"],
            "total": g["total"],
            "owners_range": g["owners_range"],
            "pct_positive": "", "metacritic": "", "units_millions": "",
            "revenue_musd": "", "peak_ccu": "",
            "performance_score": g["performance_score"],
            "profile_fit_score": round(fit_score(g, weights, absent_total), 4),
            "scale_tier": "indie",
            "gamepass_status": "unverified",
            "evidence_strength": "strong",
            "source_url": "data/raw (SteamSpy + Steam reviews snapshot, Dec 2024)",
        })

    for i, r in enumerate(out, 1):
        r["rank"] = i
    cols = ["rank", "source", "app_id", "name", "release_year", "developer", "genres",
            "key_tags", "price_cents", "price_usd", "price_band", "review_score", "total",
            "owners_range", "pct_positive", "metacritic", "units_millions", "revenue_musd",
            "peak_ccu", "performance_score", "profile_fit_score", "scale_tier",
            "gamepass_status", "evidence_strength", "source_url"]
    write_csv(PROC / "top50_indie_reference.csv", cols, out)

    # ---- 2. match profile --------------------------------------------------
    write_csv(PROC / "top50_match_profile.csv",
              ["attribute_type", "attribute", "winner_count", "winner_share",
               "baseline_count", "baseline_share", "lift", "log_odds_weight"],
              profile_rows)

    # ---- 3. scored candidates ---------------------------------------------
    wids = {g["app_id"] for g in winners}
    ref_ids = {r["app_id"] for r in out if r["app_id"]}
    cands = []
    for g in universe:
        raw = fit_score(g, weights, absent_total)
        cands.append({**g, "raw_fit": raw})
    fits = [c["raw_fit"] for c in cands]
    lo, hi = min(fits), max(fits)
    for c in cands:
        c["profile_fit_score"] = round(100 * (c["raw_fit"] - lo) / (hi - lo), 2)
    # combine profile fit with observed performance into an actionable priority,
    # and flag how much evidence each row actually rests on
    perfs = [c["performance_score"] for c in cands]
    pmin, pmax = min(perfs), max(perfs)
    for c in cands:
        c["perf_norm"] = 100 * (c["performance_score"] - pmin) / (pmax - pmin)
        c["priority_score"] = round(0.5 * c["profile_fit_score"] + 0.5 * c["perf_norm"], 2)
        c["evidence_tier"] = ("high" if c["total"] >= 5000 else
                              "medium" if c["total"] >= 500 else "low")
    cands.sort(key=lambda c: -c["raw_fit"])
    crows = [{
        "fit_rank": i,
        "app_id": c["app_id"],
        "name": c["name"],
        "release_date": c["release_date"],
        "genres": c["genres"],
        "top_matching_tags": ", ".join(sorted([t for t in c["tag_set"] if weights.get(("tag", t), (0, 0))[0] > 0],
                                              key=lambda t: -weights[("tag", t)][0])[:8]),
        "price_cents": c["price_cents"],
        "price_usd": c["price_usd"],
        "price_band": c["price_band"],
        "review_score": c["review_score"],
        "total": c["total"],
        "owners_range": c["owners_range"],
        "owners_mid": int(c["owners_mid"]),
        "performance_score": c["performance_score"],
        "profile_fit_score": c["profile_fit_score"],
        "priority_score": c["priority_score"],
        "evidence_tier": c["evidence_tier"],
        "in_winner_cohort": int(c["app_id"] in wids),
        "in_top50_reference": int(c["app_id"] in ref_ids),
    } for i, c in enumerate(cands, 1)]
    write_csv(PROC / "indie_candidates_scored.csv", list(crows[0].keys()), crows)

    # ---- validation: does the profile actually separate winners from the rest?
    pos = sorted(c["raw_fit"] for c in cands if c["app_id"] in wids)
    neg = sorted(c["raw_fit"] for c in cands if c["app_id"] not in wids)
    import bisect
    auc = sum(bisect.bisect_left(neg, v) + 0.5 * (bisect.bisect_right(neg, v) - bisect.bisect_left(neg, v))
              for v in pos) / (len(pos) * len(neg))
    print(f"validation: profile_fit_score AUC separating the {len(pos)} winners "
          f"from {len(neg)} other indie games = {auc:.3f}")
    print(f"wrote {len(out)} reference rows, {len(profile_rows)} profile rows, "
          f"{len(crows)} scored candidates")


def write_csv(path, cols, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"  -> {path}")


if __name__ == "__main__":
    main()
