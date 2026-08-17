# Metric Glossary (v1)

Every metric with an exact formula, the grain it's computed at, and its caveats.
Purpose: so each metric is calculated the same way every time, and any reviewer
can audit the logic. Where a definition prevents a common error, that is noted.

**Overarching caveat:** the public HMDA data lacks credit score and gives DTI only
in ranges, so no metric here controls fully for creditworthiness. All disparity
metrics are *signals for review*, never proof of discrimination.

---

## Decision universe (used by most metrics)
"Decisioned applications" = rows where `action_taken` IN (1, 2, 3):
- 1 = loan originated
- 2 = approved but not accepted
- 3 = denied

**Excluded** and why:
- 6 = purchased loan → not a decision this lender made (bought from another lender)
- 4 = withdrawn by applicant → applicant's choice, not a lender denial
- 5 = file closed incomplete → never decisioned
- 7, 8 = preapproval outcomes → separate process

> This exclusion is the most important calculation rule in the project. Including
> code 6 would inflate the denominator with ~27k non-decisions and distort every rate.

---

## Core metrics

### Denial rate
- **Formula:** count(`action_taken` = 3) ÷ count(`action_taken` IN (1,2,3))
- **Grain:** computed per group × geography × year (e.g. race × MSA × 2023)
- **Caveat:** denominator is decisioned apps only. Excludes withdrawn/incomplete/purchased.

### Origination rate
- **Formula:** count(`action_taken` = 1) ÷ count(`action_taken` IN (1,2,3))
- **Grain:** group × geography × year
- **Note:** the "success" mirror of denial rate.

### Rate spread (pricing)
- **Definition:** reported `rate_spread` on originated loans (spread over the market benchmark APOR).
- **Grain:** distribution (median + spread) per group × geography, on originated loans only.
- **Caveat:** ~48% of rows are blank —structural, because rate_spread only applies to originated priced loans. Never impute; report on the populated subset and state coverage.

### Disparity (gap)
- **Formula:** metric(group A) −metric(reference group), e.g. denial_rate(Black) − denial_rate(White).
- **Grain:** per geography × year.
- **Required with it:**
  - a **confidence interval** (a gap from few applications may be noise);
  - a **minimum-volume threshold** (see below) before a gap is reported;
  - the standing caveat: uncontrolled for creditworthiness → signal, not proof.

### Exposure (for the CRO question)
- **Definition:** disparity size combined with lending volume in that market.
- **Rationale:** a large gap in a 5-loan market is low risk; a moderate gap in a 5,000-loan market is high risk. Exposure = severity × scale.
- **Grain:** market (MSA) × year.

### Peer benchmark gap (for Retail Lending)
- **Definition:** our metric (denial or rate spread) minus the peer-set metric for the same market/product.
- **Peer set:** lenders active in the same MSA above a minimum volume threshold (threshold TBD, documented when set).
- **Caveat:** peer sets shift year to year as lenders enter/exit.

### Access gap (for CRA outreach)
- **Definition:** difference between mortgage demand/population and actual lending in a tract, focused on underserved tracts.
- **Grain:** tract × year, joined to ACS income/minority share.

---

## Supporting definitions
- **Group:** a demographic category from `derived_race` / `derived_ethnicity` / `derived_sex`. Note: ~28% of race is "Race Not Available" — every race-based metric is conditional on race being reported, and that coverage % must be stated.
- **Reference group:** the comparison baseline (commonly non-Hispanic White) — stated explicitly wherever a disparity is reported.
- **Minimum volume threshold:** a metric is not reported for a cell below N decisioned applications (N TBD, e.g. 30–50) to avoid noise. Documented when finalized.
- **Underserved tract:** defined via ACS (e.g. below-median income and/or high minority share) — exact definition documented when the geography dimension is built.

---

## Open definitions to finalize later
- Minimum volume threshold N (Week 2–3).
- Peer-set volume threshold (Week 5+).
- Exact "underserved tract" cutoffs (Week 6, with ACS).
- Which controls are applied in "unexplained" gaps (Week 5+, staging).