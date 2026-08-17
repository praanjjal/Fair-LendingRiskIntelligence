# Plain-Language Glossary

A quick-reference for the banking, fairness, and data terms used in this project.
Written in everyday language; the precise technical definitions live in the
metric glossary and data dictionary.

## Core mortgage / lending terms
- **Mortgage** — a loan to buy or refinance a home. The subject of this whole project.
- **Applicant / borrower** — the person requesting the mortgage. *Co-applicant* = a second person on the same application.
- **Lender** — the bank or company issuing the loan.
- **Originated** — approved AND taken by the borrower; a completed loan (`action_taken = 1`).
- **Denied** — application rejected (`action_taken = 3`).
- **Underwriting** — the process where a lender decides yes/no on an application (income, credit, property).
- **Refinance (refi)** — replacing an existing mortgage with a new one, usually for a better rate.

## Money / risk terms
- **Credit score** — a number summarizing repayment reliability. **HIDDEN in this public data** — the reason disparities can only be flagged, never proven as discrimination.
- **DTI (debt-to-income ratio)** — share of monthly income going to debt. In this data it comes as rough ranges, not exact numbers.
- **Rate spread** — extra interest charged versus a benchmark; used to spot *pricing* unfairness.
- **Interest rate** — the cost of borrowing, as a percent.
- **Loan-to-value (LTV)** — loan amount vs. home value; higher = riskier for the lender.

## Fairness / legal terms (the heart of the project)
- **Fair lending** — the laws/principle that lenders can't discriminate by race, sex, ethnicity, etc.
- **Disparity** — a measured *difference* between groups. **A signal to investigate, NOT proof of discrimination.**
- **Discrimination** — illegally treating someone worse due to a protected characteristic. This project never claims it — only flags where to look.
- **Protected class** — characteristics the law protects (race, ethnicity, sex, age). May be studied, never used to make lending decisions.
- **HMDA (Home Mortgage Disclosure Act)** — the law requiring lenders to publicly report mortgage data. The source of the main dataset.
- **CRA (Community Reinvestment Act)** — law pushing banks to lend fairly across all neighborhoods, including underserved ones.
- **Regulator** — the government body enforcing these laws; being caught is costly, so banks self-check first.

## Team roles (fictional Meridian Regional Bank)
- **Compliance** — the department ensuring the bank follows the law; this project lives here.
- **Audit** — a deep formal investigation of a specific area. Costly, so it must be prioritized.
- **Fair Lending Officer** — decides *where to audit*.
- **CRA Officer** — decides *which neighborhoods to target for outreach*.
- **Chief Risk Officer (CRO)** — decides *where the bank faces the most regulatory risk*.
- **Head of Retail Lending** — runs front-line consumer lending; decides *which parts need improvement*.
- **Compliance Analyst** — decides *which specific cases need further investigation*.
- **Retail lending** — everyday consumer loans (vs. corporate lending).
- **Second line of defense** — the oversight team that checks the people making loans (this project's team).
- **Peer benchmarking** — comparing this bank against similar lenders in the same market.

## Geography terms
- **Census tract** — a neighborhood-sized statistical area (a few thousand people). The finest "where."
- **MSA (Metropolitan Statistical Area)** — a metro region (city + commuter suburbs), e.g. Boston MSA. The natural "which market" unit.
- **ACS (American Community Survey)** — Census survey giving neighborhood facts (income, race makeup, home ownership) per tract. The second dataset.
- **Owner-occupied** — a home lived in by its owner (vs. a rental); a neighborhood trait from ACS.

## Data terms
- **LEI** — a unique ID code for each lender (a fingerprint to tell banks apart).
- **FIPS code** — government numeric codes for places (Massachusetts = 25).
- **Manifest** — the small receipt file recording row counts + a data fingerprint, proving a data pull is repeatable.
- **Warehouse** — the organized database (SQL Server) where cleaned data lives; the project's "filing system."

## The three that matter most
- **Fair lending** — what you're checking.
- **Disparity** — what you measure: a signal, not proof.
- **Hidden credit score** — why you can only flag suspicions, never accuse.