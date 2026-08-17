# Project State

_Updated at the end of every task._

## Done
- **Week 1 complete.**
- Task 1: Repository scaffolded and pushed (GitHub).
- Task 2: Source register with 4 verified public sources; HMDA credit-score-vs-model-name distinction documented.
- Task 3: SQL Server 2022 running in Docker (Apple Silicon, Rosetta); `fair_lending` DB with 7 schemas (raw, stg, core, mart, audit, ml, ai). Bootstrap script in `sql/00_admin/create_schemas.sql`.
- Task 4: Reproducible ingestion, HMDA MA 2023 (210,643 rows, checksum-verified) and ACS MA tracts 2023 (1,620 tracts). Manifests committed; raw CSVs gitignored.
- Task 5: Raw profiling notebook + data dictionary v0.

## Key findings from profiling
- Denial-rate denominator must exclude purchased loans (action_taken=6) and use decisioned rows (1,2,3).
- ~28% of `derived_race` is "Race Not Available", disparity estimates conditional on reporting.
- `debt_to_income_ratio` is mixed buckets + exact values + Exempt + blanks, not a clean creditworthiness control.
- `rate_spread` ~48% blank (structural, only for originated priced loans).
- Join key confirmed: HMDA `census_tract` = ACS `tract_geoid`, both 11-digit (e.g. 25005985600).

## Decided
- Scope: Massachusetts (all MSAs), year 2023, as the starting slice.
- Fictional sponsor: Meridian Regional Bank.
- SQL client: VS Code MSSQL extension.


## Done
- **Week 2 complete.**
- Business questions: 5 decision-focused headline questions + supporting sub-questions, one per stakeholder.
- Metric glossary v1: formulas, grains, caveats; denial-rate denominator rule codified (exclude action=6).
- Stakeholder map: decisions, two-sided cost of error, metric mapping per role.
- Data-quality log: 12 issues with impact and mitigation.

## Open / Next (Week 3)
- Source-to-target mapping (which raw field → which warehouse column).
- Dimensional model design: fact_application + dimensions (geography, lender, loan, applicant, date), grain documented.
- First raw-disparity exploration (uncaveated), labelled as signals only.