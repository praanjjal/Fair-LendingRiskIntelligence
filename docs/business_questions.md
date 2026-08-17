# Business Questions

Decision-focused questions this project answers. Each names a stakeholder, the
decision they own, the disparity signal that ranks the answer, and the constraint
that forces a choice.

**Ethical guardrail:** every question is answerable as *"where to look / what to
prioritize,"* never *"who is guilty."* Because the public data lacks credit score,
findings are signals for review, not proof of discrimination.

-----------------------------------------------------------------------------------------

## 1. Fair Lending Officer ==> where to audit
**Headline:** Which 3–5 markets should we prioritize for fair-lending audit next
quarter, ranked by the size of unexplained denial-rate gaps between demographic
groups, given limited review capacity?

Supporting:
- Which markets have the largest denial-rate gaps between demographic groups?
- Do those gaps shrink when we account for available legitimate factors (loan purpose, income, loan type)? (Signal strength.)
- Which gaps are backed by enough volume to be worth an audit vs. noise?

## 2. CRA Officer ==> where to do community outreach
**Headline:** Which counties/tracts should we prioritize for community outreach,
ranked by gaps in mortgage access in underserved neighborhoods, given a limited
outreach budget?

Supporting:
- Which tracts have low lending relative to their population/demand?
- How do lower-income and higher-minority tracts compare on access?
- Where would outreach close the largest access gap per dollar?

## 3. Chief Risk Officer ==> where the regulatory risk is greatest
**Headline:** Where does the bank face the greatest regulatory exposure, weighing
both the size of the disparity and our lending volume in that market?

Supporting:
- Which markets combine a large disparity with high lending volume? (Exposure = severity × scale.)
- Where are we an outlier versus peers in the same market?
- Which disparities are large enough and public enough to attract scrutiny?

## 4. Head of Retail Lending ==> which operations need improvement
**Headline:** Which of our lending operations underperform their peers, ranked by
how much our denial or pricing patterns differ from comparable lenders in the same
market?

Supporting:
- Where do our denial rates exceed the peer benchmark for the same market/product?
- Where do our rate spreads (pricing) exceed peers for similar borrowers?
- Which operations show the widest peer gap and are operationally fixable?

## 5. Compliance Analyst ==> which cases to investigate
**Headline:** Which specific lender–product–demographic segments look most
anomalous and warrant a closer manual review?

Supporting:
- Which fine-grained segments are statistical outliers on denial or pricing?
- Are anomalies concentrated in particular products or channels?
- Which segments have enough records to justify a manual case pull?

-----------------------------------------------------------------------------------------

## Note on grain
Each stakeholder needs the same underlying data at a different level of detail:
- CRO → **markets** (MSA level)
- Fair Lending Officer → **markets**, gap-ranked
- CRA Officer → **counties / tracts**
- Head of Retail Lending → **lender vs. peer set**
- Compliance Analyst → **lender × product × demographic segments** (finest grain)

This is why the warehouse is built around conformed dimensions (geography, lender,
loan, applicant) — so one model can answer all five at their own grain.