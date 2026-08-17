# Stakeholder Map

The five decision-makers this project serves. For each: the decision they own, what
being wrong costs them (in both directions), and the metrics that serve them.

**The two-sided cost of error (applies to all):** missing a real disparity risks
regulatory enforcement and reputational harm; flagging a false one wastes scarce
audit resources and can wrongly implicate loan officers. Every stakeholder balances
these two failure modes.

-----------------------------------------------------------------------------

## Chief Risk Officer (CRO)
- **Owns the decision:** where the bank concentrates its fair-lending risk attention overall.
- **Fear of being wrong:**
  - *Miss:* a large, high-volume disparity becomes a public enforcement action.
  - *False alarm:* over-escalating diverts the whole compliance program to a non-issue.
- **Served by:** Exposure metric (disparity × volume), peer-benchmark gap.
- **Grain:** market (MSA).
- **Business question:** #3 (regulatory exposure).

## Fair Lending Officer
- **Owns the decision:** which markets to audit next quarter.
- **Fear of being wrong:**
  - *Miss:* a genuine access gap goes un-audited and surfaces in a regulator's exam.
  - *False alarm:* burns limited audit hours on noise.
- **Served by:** denial-rate disparity + confidence interval + minimum-volume threshold.
- **Grain:** market (MSA), gap-ranked.
- **Business question:** #1 (where to audit).

## CRA Officer
- **Owns the decision:** which neighborhoods get community-lending outreach.
- **Fear of being wrong:**
  - *Miss:* underserved tracts stay underserved; CRA goals unmet.
  - *False alarm:* outreach budget spent where access was already fine.
- **Served by:** access gap (lending vs. demand), joined to ACS income/minority share.
- **Grain:** county / tract.
- **Business question:** #2 (where to do outreach).

## Head of Retail Lending
- **Owns the decision:** which lending operations need operational fixes.
- **Fear of being wrong:**
  - *Miss:* an operation quietly underperforms peers and invites scrutiny.
  - *False alarm:* front-line staff wrongly flagged, morale and trust damaged.
- **Served by:** peer-benchmark gap (our denial/pricing vs. comparable lenders).
- **Grain:** lender vs. peer set.
- **Business question:** #4 (which operations to improve).

## Compliance Analyst
- **Owns the decision:** which specific cases to pull for manual investigation.
- **Fear of being wrong:**
  - *Miss:* a genuinely anomalous segment never gets a human look.
  - *False alarm:* wastes hours on statistical noise from tiny segments.
- **Served by:** fine-grained outlier detection on denial/pricing, with volume floors.
- **Grain:** lender × product × demographic segment (finest).
- **Business question:** #5 (which cases to investigate).

-----------------------------------------------------------------------------

## Why this map matters
Every metric in the glossary traces to at least one stakeholder here. If a metric
serves no one on this map, it should not be built. This is the guard against
analysis that looks impressive but drives no decision.