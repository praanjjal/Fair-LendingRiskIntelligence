# Mortgage Access & Fair-Lending Risk Intelligence

A decision-support system for a mid-size regional bank's second-line Risk &
Compliance function. It identifies which markets, products, and peer comparisons
show **unexplained disparities** in mortgage access, and prioritizes where limited
fair-lending review and community-lending outreach should go — with defensible,
caveated evidence.

## The ethical spine
Public HMDA data is privacy-modified, has no credit score, and reports debt-to-income
only in coarse ranges. It therefore **cannot fully control for creditworthiness.**
Every output is framed as *"a market or lender warranting further review,"* never as
proof of discrimination. That honesty is a feature of the product, not a disclaimer.

## Data sources (all public)
- HMDA Loan/Application Register (FFIEC/CFPB)
- U.S. Census ACS, tract level
- FFIEC lender/institution panel
- FRED / FHFA (benchmark rates, House Price Index)

## Stack
Python · SQL Server (Docker) · Power BI · Tableau · R/Quarto · Git

## Reproducibility
Data is pulled programmatically with logged manifests (row counts + checksums).
Raw data is never committed; manifests are. See `docs/source_register.md`.

## Status
See `PROJECT_STATE.md` for what is done, decided, and open.

*Meridian Regional Bank is a clearly-labelled fictional institution used for the
business scenario. All data is real and public.*
