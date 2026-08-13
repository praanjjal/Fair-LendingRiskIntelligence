"""
Pull tract-level ACS 5-Year data for Massachusetts (2023) and write a manifest.
Source: U.S. Census Bureau ACS API (requires free API key in .env).
Tables: median household income (B19013), race/ethnicity (B03002), tenure (B25003).
"""
import hashlib
import json
import os
import datetime as dt
from pathlib import Path
import requests
import pandas as pd
from dotenv import load_dotenv

# --- Load the Census key from .env ---
load_dotenv()
API_KEY = os.environ["CENSUS_API_KEY"]

# --- Parameters ---
STATE_FIPS = "25"    # Massachusetts
YEAR = "2023"

# Variables we want. Census codes end in E for "Estimate".
# B19013_001E = median household income
# B03002 table = Hispanic origin by race (we take the pieces we need)
# B25003_001E total occupied, _002E owner-occupied, _003E renter-occupied
VARIABLES = {
    "B19013_001E": "median_household_income",
    "B03002_001E": "race_total",
    "B03002_003E": "white_nonhispanic",
    "B03002_004E": "black_nonhispanic",
    "B03002_006E": "asian_nonhispanic",
    "B03002_012E": "hispanic_any_race",
    "B25003_001E": "tenure_total",
    "B25003_002E": "owner_occupied",
    "B25003_003E": "renter_occupied",
}

BASE = f"https://api.census.gov/data/{YEAR}/acs/acs5"
get_fields = ",".join(["NAME", *VARIABLES.keys()])
URL = f"{BASE}?get={get_fields}&for=tract:*&in=state:{STATE_FIPS}&key={API_KEY}"

# --- Output paths ---
SAMPLE_DIR = Path("data/sample")
MANIFEST_DIR = Path("data/manifests")
OUT_CSV = SAMPLE_DIR / f"acs_{STATE_FIPS}_{YEAR}.csv"
OUT_MANIFEST = MANIFEST_DIR / f"acs_{STATE_FIPS}_{YEAR}.json"


def pull() -> None:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Pulling ACS tracts for state {STATE_FIPS} {YEAR} ...")
    resp = requests.get(URL, timeout=120)
    resp.raise_for_status()
    rows = resp.json()  # first row is headers, rest are data

    # Convert to a DataFrame and rename the variable codes to readable names
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df = df.rename(columns=VARIABLES)

    # Build an 11-digit tract GEOID = state(2) + county(3) + tract(6) to join with HMDA
    df["tract_geoid"] = df["state"] + df["county"] + df["tract"]

    df.to_csv(OUT_CSV, index=False)

    data = OUT_CSV.read_bytes()
    manifest = {
        "source": "U.S. Census ACS 5-Year (API)",
        "url": URL.replace(API_KEY, "REDACTED"),   # never log the key
        "state_fips": STATE_FIPS,
        "year": YEAR,
        "rows": len(df),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "variables": VARIABLES,
        "pulled_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2))

    print(f"Saved {len(df):,} tracts to {OUT_CSV}")
    print(f"Manifest written to {OUT_MANIFEST}")


if __name__ == "__main__":
    pull()