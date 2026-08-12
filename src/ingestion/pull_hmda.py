"""
Pull one state-year of HMDA Modified LAR data and write a reproducibility manifest.
Source: FFIEC HMDA Data Browser API (no key required).
Starting with all of Massachusetts to confirm the pipeline; will narrow to Boston MSA next.
"""
import hashlib
import json
import datetime as dt
from pathlib import Path
import requests

# --- Parameters for this pull ---
STATE = "MA"         # Massachusetts
YEAR = "2023"
URL = (
    "https://ffiec.cfpb.gov/v2/data-browser-api/view/csv"
    f"?years={YEAR}&states={STATE}&actions_taken=1,2,3,4,5,6,7,8"
)

# --- Output paths ---
SAMPLE_DIR = Path("data/sample")
MANIFEST_DIR = Path("data/manifests")
OUT_CSV = SAMPLE_DIR / f"hmda_{STATE}_{YEAR}.csv"
OUT_MANIFEST = MANIFEST_DIR / f"hmda_{STATE}_{YEAR}.json"


def pull() -> None:
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Pulling HMDA {STATE} {YEAR} ...")
    with requests.get(URL, stream=True, timeout=600) as resp:
        resp.raise_for_status()
        with open(OUT_CSV, "wb") as f:
            for chunk in resp.iter_content(chunk_size=1 << 20):
                f.write(chunk)

    data = OUT_CSV.read_bytes()
    row_count = data.count(b"\n") - 1
    checksum = hashlib.sha256(data).hexdigest()

    manifest = {
        "source": "HMDA Modified LAR (FFIEC Data Browser API)",
        "url": URL,
        "state": STATE,
        "year": YEAR,
        "rows": row_count,
        "bytes": len(data),
        "sha256": checksum,
        "pulled_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2))

    print(f"Saved {row_count:,} rows to {OUT_CSV}")
    print(f"Manifest written to {OUT_MANIFEST}")


if __name__ == "__main__":
    pull()