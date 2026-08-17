# Dimensional Model Design

The star schema for the fair-lending warehouse: one fact table
(`core.fact_application`) surrounded by five conformed dimensions. Built in the
`core` schema from the `stg` (staging) layer. Grains and keys below are the
authoritative design; the field-level transformations live in
`source_to_target_mapping.md`.

-----------------------------------------------------------------------------------

## Design principles
- **Star schema:** facts (measurements) in the center, dimensions (descriptors) on
  the points. Chosen for query simplicity, no repetition, and native BI support.
- **Surrogate keys:** each dimension has an integer `*_key` as primary key. Facts
  reference dimensions by these keys. Natural keys (lei, tract_geoid) are kept as
  attributes for traceability.
- **Conformed dimensions:** the same dimension serves every stakeholder question at
  its own grain (markets, tracts, lenders, segments) — one model, five audiences.

-----------------------------------------------------------------------------------

## Fact table

### core.fact_application
- **Grain:** *one row per loan application per reporting year.* (Not per applicant —
  an application with co-applicant is still one row.)
- **Primary key:** `application_id` (surrogate).
- **Foreign keys:** `applicant_key`, `geography_key`, `lender_key`, `loan_key`, `date_key`.
- **Measures & flags:** `action_taken`, `is_denied`, `is_originated`, `is_decisioned`,
  `loan_amount`, `interest_rate`, `rate_spread`, `dti_bucket`.
- **Row count target:** 210,643 (MA 2023) — must equal the source after load.

-----------------------------------------------------------------------------------

## Dimension tables

### core.dim_applicant
- **Grain:** one row per distinct applicant profile (race × ethnicity × sex × income × dti_bucket).
- **Key:** `applicant_key` (surrogate).
- **Attributes:** derived_race, derived_ethnicity, derived_sex, income, dti_bucket.
- **Note:** protected-class attributes — studied, never used for predictive scoring.

### core.dim_geography
- **Grain:** one row per census tract.
- **Key:** `geography_key` (surrogate); natural key `tract_geoid` (11-digit).
- **Attributes:** county_code, state_code, msa_md, median_household_income,
  minority_share (derived), owner_occupied_rate (derived).
- **Source:** HMDA tract + ACS enrichment joined on tract_geoid.

### core.dim_lender
- **Grain:** one row per lender.
- **Key:** `lender_key` (surrogate); natural key `lei`.
- **Attributes:** institution_name, asset_size, lender_type (from FFIEC panel, joined later).

### core.dim_loan
- **Grain:** one row per distinct loan-attribute combination.
- **Key:** `loan_key` (surrogate).
- **Attributes:** loan_type, loan_purpose, occupancy_type, lien_status (all decoded from codes).

### core.dim_date
- **Grain:** one row per reporting year.
- **Key:** `date_key` (surrogate); natural key `activity_year`.

-----------------------------------------------------------------------------------

## Relationships
Each fact row points to exactly one row in each dimension:

- fact_application → dim_applicant (many-to-one)
- fact_application → dim_geography (many-to-one)
- fact_application → dim_lender (many-to-one)
- fact_application → dim_loan (many-to-one)
- fact_application → dim_date (many-to-one)

No dimension references another (that would be a snowflake — deliberately avoided
to keep queries simple).

---

## Key design decisions
1. **Fact grain = application, not applicant.** Co-applicants do not create extra
   rows. Prevents double-counting.
2. **`is_decisioned` flag on the fact.** Encodes the denial-rate denominator rule
   (action_taken IN 1,2,3) as data, so every query uses the same denominator.
3. **ACS enrichment lands in dim_geography, not the fact.** Neighborhood context is
   an attribute of place, computed once per tract.
4. **Protected class isolated in dim_applicant** and flagged non-predictive.
5. **Star, not snowflake.** Dimensions are flat; no dimension joins another. Simpler
   queries, better BI performance, at the cost of some redundancy (acceptable).

---

## Validation checks (to run when the model is built)
- fact_application row count = 210,643 (matches source).
- Every fact FK resolves to a dimension row (no orphans).
- dim_geography tract count ≈ tracts present in HMDA (subset of the 1,620 ACS tracts).
- Sum of is_decisioned ≈ count of action_taken IN (1,2,3) from profiling.