"""
sample_indie_games.py

Generates a statistically defensible simple random sample (SRS) from the
indie_games.csv population, using Cochran's sample-size formula with a
finite population correction.

Expected repository structure (paths are resolved relative to this file,
not the current working directory, so the script works regardless of
where it is run from):

    Gainz-for-XBox/
    │
    ├── data/
    │   └── processed/
    │       └── indie_games.csv
    │
    └── src/
        └── sample_indie_games.py

Population never modified: indie_games.csv is only ever read, never written.
Output: data/processed/indie_games_sample.csv
"""

import math
from pathlib import Path

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------------------------
# Resolve paths relative to this script's location (not the CWD), so the
# script behaves identically no matter where it's invoked from.
SCRIPT_DIR = Path(__file__).resolve().parent          # .../Gainz-for-XBox/src
REPO_ROOT = SCRIPT_DIR.parent                          # .../Gainz-for-XBox
POPULATION_PATH = REPO_ROOT / "data" / "processed" / "indie_games.csv"
SAMPLE_OUTPUT_PATH = REPO_ROOT / "data" / "processed" / "indie_games_sample.csv"

# ---------------------------------------------------------------------------
# 1. LOAD AND VERIFY THE POPULATION
# ---------------------------------------------------------------------------
# Read the population file. This file is never written back to -- it is
# only read here, and no in-place modification, sorting, or overwrite of
# it occurs anywhere in this script.
population = pd.read_csv(POPULATION_PATH)

expected_columns = ["app_id", "genres", "tags"]
assert list(population.columns) == expected_columns, (
    f"Unexpected columns in population file: {list(population.columns)}"
)

# Verify app_id is unique and complete -- these are the eligibility
# conditions for treating the row count as the population size N.
assert population["app_id"].isna().sum() == 0, "Population contains missing app_id values"
assert population["app_id"].is_unique, "Population contains duplicate app_id values"
assert population.duplicated().sum() == 0, "Population contains exact duplicate rows"

# The verified number of unique, eligible games is the population size N.
N = len(population)

# ---------------------------------------------------------------------------
# 2. SAMPLE-SIZE CALCULATION (Cochran's formula + finite population correction)
# ---------------------------------------------------------------------------
# Assumptions (stated explicitly, not chosen arbitrarily):
#   confidence level = 95%   -> z = 1.96 (standard normal critical value)
#   margin of error  = 5%    -> e = 0.05
#   assumed proportion p = 0.5 (maximizes p*(1-p), the conservative choice
#                                 when the true population proportion for
#                                 whatever attribute will later be estimated
#                                 is unknown)
Z = 1.96
MARGIN_OF_ERROR = 0.05
P = 0.5

# Step 1: infinite-population sample size (Cochran's formula)
#   n0 = z^2 * p * (1 - p) / e^2
n0 = (Z ** 2 * P * (1 - P)) / (MARGIN_OF_ERROR ** 2)

# Step 2: finite population correction (population is not "infinite" --
# N = 89,648 is a specific, known, finite population)
#   n = n0 / (1 + (n0 - 1) / N)
n_adjusted = n0 / (1 + (n0 - 1) / N)

# Step 3: round up to the next whole game. Rounding UP (not to nearest)
# ensures the achieved margin of error is at least as tight as 5% -- 
# rounding down would understate precision.
SAMPLE_SIZE = math.ceil(n_adjusted)

assert SAMPLE_SIZE <= N, "Calculated sample size cannot exceed the population size"

# ---------------------------------------------------------------------------
# 3. RANDOM SEED
# ---------------------------------------------------------------------------
# A fixed seed makes the random draw exactly reproducible. The seed value
# itself has no statistical meaning or "optimality" -- any fixed integer
# works equally well; it must simply be chosen and fixed BEFORE looking at
# the resulting sample, which is done here.
RANDOM_SEED = 42

# ---------------------------------------------------------------------------
# 4. GENERATE THE SIMPLE RANDOM SAMPLE (without replacement)
# ---------------------------------------------------------------------------
# pandas' DataFrame.sample() with replace=False performs a simple random
# sample without replacement: every row (every app_id) has an equal
# probability of selection, with no stratification, weighting, or manual
# selection of any kind.
rng = np.random.default_rng(RANDOM_SEED)
sample = population.sample(n=SAMPLE_SIZE, replace=False, random_state=rng)

# Restore the population's original row order for the sampled rows (purely
# cosmetic -- does not affect which rows were selected or their equal
# selection probability).
sample = sample.sort_index().reset_index(drop=True)

# ---------------------------------------------------------------------------
# 5. VALIDATE THE SAMPLE
# ---------------------------------------------------------------------------
# a) Sample row count equals the calculated sample size
assert len(sample) == SAMPLE_SIZE, "Sample row count does not match calculated sample size"

# b) Sampled app_ids are unique (guaranteed by replace=False, checked anyway)
assert sample["app_id"].is_unique, "Sample contains duplicate app_id values"

# c) All sampled app_ids exist in the population
assert sample["app_id"].isin(population["app_id"]).all(), \
    "Sample contains an app_id not present in the population"

# d) No duplicate rows were introduced
assert sample.duplicated().sum() == 0, "Sample contains duplicate rows"

# e) Sampling was without replacement (row count of unique app_ids in the
# sample must equal the sample size -- redundant with (b)/(a), kept as an
# explicit, independent check)
assert sample["app_id"].nunique() == SAMPLE_SIZE, "Sample was not drawn without replacement"

# f) The same seed reproduces exactly the same sample
rng_repeat = np.random.default_rng(RANDOM_SEED)
sample_repeat = population.sample(n=SAMPLE_SIZE, replace=False, random_state=rng_repeat)
sample_repeat = sample_repeat.sort_index().reset_index(drop=True)
assert sample.equals(sample_repeat), "Sample is not reproducible with the fixed seed"

# g) The original population file was never modified -- verify its
# on-disk content is unchanged by re-reading it and comparing to the
# in-memory copy loaded at the start of this script.
population_reloaded = pd.read_csv(POPULATION_PATH)
assert population.equals(population_reloaded), "Population file was modified during script execution"

duplicate_sampled_app_ids = len(sample) - sample["app_id"].nunique()
validation_passed = (
    len(sample) == SAMPLE_SIZE
    and sample["app_id"].is_unique
    and sample["app_id"].isin(population["app_id"]).all()
    and sample.duplicated().sum() == 0
    and duplicate_sampled_app_ids == 0
    and sample.equals(sample_repeat)
)

# ---------------------------------------------------------------------------
# 6. EXPORT THE SAMPLE (CSV, original columns preserved, population untouched)
# ---------------------------------------------------------------------------
SAMPLE_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
sample.to_csv(SAMPLE_OUTPUT_PATH, index=False, columns=expected_columns)

# ---------------------------------------------------------------------------
# COMPLETION SUMMARY
# ---------------------------------------------------------------------------
print("Population size:", N)
print("Sample size:", SAMPLE_SIZE)
print("Sampling method: Simple random sample without replacement")
print("Random seed:", RANDOM_SEED)
print("Duplicate sampled app_ids:", duplicate_sampled_app_ids)
print("Validation:", "PASSED" if validation_passed else "FAILED")
print("Saved to:", SAMPLE_OUTPUT_PATH)
