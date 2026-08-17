# Source-to-Target Mapping

For every HMDA/ACS field used, where it lands in the star schema and how it is
transformed. This is the contract between raw data and warehouse, transformations
are decided here once, then implemented consistently in the staging layer.

Source: `hmda_MA_2023.csv` (210,643 rows) and `acs_25_2023.csv` (1,620 tracts).

**Convention:** "decode" = translate a numeric code to a readable label using the
HMDA schema. "bucket" = keep as a category, not a number. Surrogate keys (`*_key`)
are integer IDs generated when the dimension tables are built.

-------------------------------------------------------------------------------

## fact_application
**Grain:** one row per loan application per reporting year.

| Target column | Source field | Transformation |
|---------------|--------------|----------------|
| `application_id` | (row number) | Surrogate integer, one per source row. |
| `applicant_key` | → dim_applicant | FK to dim_applicant. |
| `geography_key` | `census_tract` | FK to dim_geography (via tract_geoid). |
| `lender_key` | `lei` | FK to dim_lender. |
| `loan_key` | → dim_loan | FK to dim_loan. |
| `date_key` | `activity_year` | FK to dim_date. |
| `action_taken` | `action_taken` | Keep raw code (1–8). |
| `is_denied` | `action_taken` | Derived flag: 1 if action_taken=3, else 0. |
| `is_originated` | `action_taken` | Derived flag: 1 if action_taken=1, else 0. |
| `is_decisioned` | `action_taken` | Derived flag: 1 if action_taken IN (1,2,3), else 0. **Denominator gate.** |
| `loan_amount` | `loan_amount` | Numeric (already binned for privacy). |
| `interest_rate` | `interest_rate` | Numeric; may be blank/Exempt. |
| `rate_spread` | `rate_spread` | Numeric; ~48% blank (structural). |
| `dti_bucket` | `debt_to_income_ratio` | Bucket/category only — never numeric. |

## dim_applicant
**Grain:** one row per distinct applicant profile. **Natural key:** combination of demographic + income fields.

| Target column | Source field | Transformation |
|---------------|--------------|----------------|
| `applicant_key` | (generated) | Surrogate integer. |
| `derived_race` | `derived_race` | Keep label; preserve "Race Not Available" as its own category. |
| `derived_ethnicity` | `derived_ethnicity` | Keep label; preserve "not available". |
| `derived_sex` | `derived_sex` | Keep label. |
| `income` | `income` | Numeric (as reported). |
| `dti_bucket` | `debt_to_income_ratio` | Bucketed category. |

> Protected-class fields (race, ethnicity, sex) live here. They may be **studied**
> in disparity analysis but must **never** feed a predictive model that drives a
> lending decision.

## dim_geography
**Grain:** one row per census tract. **Natural key:** `tract_geoid` (11-digit).

| Target column | Source field | Transformation |
|---------------|--------------|----------------|
| `geography_key` | (generated) | Surrogate integer. |
| `tract_geoid` | `census_tract` (HMDA) / `tract_geoid` (ACS) | 11-digit join key. |
| `county_code`, `state_code` | HMDA | FIPS codes. |
| `msa_md` | `derived_msa-md` | Metro/division code. |
| `median_household_income` | ACS `median_household_income` | From ACS join. |
| `minority_share` | ACS race counts | Derived: 1 − (white_nonhispanic / race_total). |
| `owner_occupied_rate` | ACS tenure | Derived: owner_occupied / tenure_total. |

## dim_lender
**Grain:** one row per lender. **Natural key:** `lei`.

| Target column | Source field | Transformation |
|---------------|--------------|----------------|
| `lender_key` | (generated) | Surrogate integer. |
| `lei` | `lei` | Legal Entity Identifier. |
| `institution_name` | FFIEC panel (later) | Joined from institution panel. |
| `asset_size`, `lender_type` | FFIEC panel (later) | Joined from institution panel. |

## dim_loan
**Grain:** one row per distinct loan-attribute combination. **Natural key:** the combination of the fields below.

| Target column | Source field | Transformation |
|---------------|--------------|----------------|
| `loan_key` | (generated) | Surrogate integer. |
| `loan_type` | `loan_type` | Decode: 1=Conventional, 2=FHA, 3=VA, 4=RHS/FSA. |
| `loan_purpose` | `loan_purpose` | Decode: 1=Purchase, 2=Home improvement, 31/32=Refi, etc. |
| `occupancy_type` | `occupancy_type` | Decode: 1=Principal, 2=Second, 3=Investment. |
| `lien_status` | `lien_status` | Decode: 1=First lien, 2=Subordinate. |

## dim_date
**Grain:** one row per year. **Natural key:** `activity_year`.

| Target column | Source field | Transformation |
|---------------|--------------|----------------|
| `date_key` | (generated) | Surrogate integer. |
| `activity_year` | `activity_year` | Reporting year (2023). |

-------------------------------------------------------------------------------

## Decisions locked here
- Denial-rate denominator gate = `is_decisioned` flag (action_taken IN 1,2,3). One rule, applied everywhere.
- DTI is categorical only, never numeric ==> enforced by mapping it to `dti_bucket`.
- Protected-class fields isolated in dim_applicant, flagged non-predictive.
- Geography derived metrics (minority_share, owner_occupied_rate) computed once, in the dimension. 