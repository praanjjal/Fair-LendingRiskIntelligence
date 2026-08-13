




# Data Dictionary

Fields used from the HMDA Modified LAR (MA, 2023) and the ACS tract enrichment.
This is not the full 99-field schema, only fields the project uses, with the
data-quality issues found during raw profiling (see `notebooks/01_raw_profiling.ipynb`).

Dataset: `data/sample/hmda_MA_2023.csv`  ==> 210,643 rows × 99 columns.

## HMDA - core analytical fields

| Field | Type | Meaning | Known issue found in profiling |
|-------|------|---------|-------------------------------|
| `action_taken` | code (1–8) | Outcome of the application | 1=originated (111,655), 3=denied (33,902), 6=purchased (27,403), 4=withdrawn (22,534), 5=incomplete (10,134), 2=approved-not-accepted (4,092), 8/7=preapproval. **Denial rate must use decisioned rows only (1,2,3); code 6 = purchased loans, NOT this lender's decision - exclude.** |
| `derived_race` | text label | Applicant race (derived) | ~28% (58,758 rows) are **"Race Not Available"** - disparity estimates are conditional on race being reported; possible reporting bias. |
| `derived_ethnicity` | text label | Hispanic/Latino origin (derived) | Similar "not available" category; treat like `derived_race`. |
| `derived_sex` | text label | Applicant sex (derived) | Has "Not Available" / "Joint" categories. |
| `debt_to_income_ratio` | mixed | DTI at decision | **Not a clean number.** Mix of buckets (`<20%`, `20%-<30%`, `30%-<36%`, `50%-60%`, `>60%`) AND exact integers (36–49); 63,981 blank; 11,087 "Exempt". Cannot be used as a continuous creditworthiness control. |
| `rate_spread` | numeric (mixed) | Spread over APOR on originated loans | ~48% blank (100,521 NaN) - structural: only meaningful for originated priced loans; 11,076 "Exempt". |
| `loan_amount` | numeric | Loan amount | Rounded/binned for privacy in the public file. |
| `loan_purpose` | code | Purpose (purchase, refi, etc.) | Numeric code; decode against schema. |
| `loan_type` | code | Conventional / FHA / VA / RHS | Numeric code. |
| `occupancy_type` | code | Principal residence / second / investment | Numeric code. |
| `census_tract` | 11-digit string | Tract of the property | Join key to ACS `tract_geoid`. Confirmed 11-digit format (e.g. `25005985600`). |
| `county_code`, `state_code` | code | Geography | Numeric FIPS codes. |
| `lei` | string | Legal Entity Identifier of the lender | Join key to the FFIEC institution panel. |

## HMDA - structural notes

- **Multi-slot fields** (`applicant_race-1..5`, `applicant_ethnicity-1..5`, `denial_reason-1..4`, `aus-1..5`): slots 4–5 are ~100% empty **by design** (applicants rarely report 5 races). Use slot 1; ignore or collapse the rest. Not a data error.
- **"Exempt"** appears across DTI, rate_spread, and other fields: small-filer **partial exemption** under HMDA - a category, not a null.

## ACS - tract enrichment fields

Dataset: `data/sample/acs_25_2023.csv` ==> 1,620 MA tracts.

| Field | Type | Meaning | Known issue |
|-------|------|---------|-------------|
| `tract_geoid` | 11-digit string | state+county+tract | Join key to HMDA `census_tract`. |
| `median_household_income` | numeric | ACS B19013 | ACS estimate with margin of error; larger error on small tracts. |
| `white_nonhispanic`, `black_nonhispanic`, `asian_nonhispanic`, `hispanic_any_race` | numeric | Counts from B03002 | Derive shares by dividing by `race_total`. |
| `owner_occupied`, `renter_occupied`, `tenure_total` | numeric | B25003 tenure | Derive owner-occupancy rate. |