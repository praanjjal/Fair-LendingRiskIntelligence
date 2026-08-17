# Data-Quality Report

Standing log of data-quality issues found in this project, their impact on analysis,
and the decision taken. Grows as new issues surface. Findings originate in
`notebooks/01_raw_profiling.ipynb`.

Dataset: HMDA Modified LAR, Massachusetts 2023 (210,643 rows) + ACS MA tracts 2023 (1,620).

| # | Issue | Where | Impact on analysis | Decision / mitigation |
|---|-------|-------|--------------------|-----------------------|
| 1 | Credit score is absent from the public file (only the scoring-model *name* survives) | HMDA `applicant_credit_score_type` | Cannot control for creditworthiness —the main legitimate factor behind denials | Frame all disparities as *signals for review, not proof*. This is the project's ethical spine. |
| 2 | Purchased loans (`action_taken`=6, ~27k rows) are not lender decisions | HMDA `action_taken` | Including them inflates the denominator and distorts every rate | Denial/origination rates use decisioned rows only: `action_taken` IN (1,2,3). |
| 3 | ~28% of race is "Race Not Available" (58,758 rows) | HMDA `derived_race` | Race-based disparities silently drop a quarter of data; possible reporting bias | Report race metrics as conditional on reporting; always state coverage %. Flag as a limitation in outputs. |
| 4 | DTI is a mix of buckets, exact integers, "Exempt", and blanks | HMDA `debt_to_income_ratio` | Cannot be used as a clean continuous control | Treat DTI as categorical/bucketed only; never as a precise number. Document Exempt as a category. |
| 5 | ~48% of rate_spread is blank (100,521 rows) | HMDA `rate_spread` | Pricing analysis covers only part of the data | Structural (only applies to originated priced loans). Analyze on the populated subset; never impute; state coverage. |
| 6 | "Exempt" appears across DTI, rate_spread, etc. | HMDA multiple | Easy to mistake for missing/zero | Treat "Exempt" as its own category (small-filer partial exemption), not a null. |
| 7 | Multi-slot fields (race-1..5, ethnicity-1..5, denial_reason-1..4, aus-1..5): slots 4–5 ~100% empty | HMDA | Could look like massive missingness | Expected by design (applicants rarely report 5 races). Use slot 1; ignore/collapse rest. Not an error. |
| 8 | Loan amount is rounded/binned for privacy | HMDA `loan_amount` | Reduces precision of amount-based analysis | Accept as-is; treat as approximate. Public-file privacy measure. |
| 9 | ACS estimates carry margins of error, larger on small tracts | ACS all | Tract-level neighborhood values are uncertain | Prefer larger geographies where possible; note MOE when reporting small tracts. |
| 10 | ACS is a 5-year rolling average, not point-in-time | ACS all | Neighborhood values are period averages, not 2023 snapshots | Acknowledge in methodology; acceptable for context/enrichment, not precise timing. |
| 11 | Tract boundaries shifted with 2020 redistricting | HMDA/ACS join | Cross-year joins could misalign geography | Keep within matching vintages (2023 HMDA ↔ 2023 ACS). Revisit if adding earlier years. |
| 12 | "Information not provided" demographic codes are distinct from true blanks | HMDA demographics | Treating them as null overstates missingness (or hides declined responses) | Preserve as their own category; do not collapse into null. |

-----------------------------------------------------------------------------

## How this log is used
- Every entry with an analytical impact has a corresponding rule in the metric glossary or a caveat in outputs.
- New issues found during staging, modeling, or dashboarding get appended here with the same columns.
- This log is the source for the "limitations" section of the executive brief and the model card.