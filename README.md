# Boeing Financial Analysis & Facility Location Recommendation

**[→ Interactive Dashboard](https://karthik-kpn.github.io/boeing-financial-analysis/dashboard.html)**

Two-part financial analysis of The Boeing Company (NYSE: BA), built for M&IE-ENG 645 (Project Budgeting & Finance), UMass Amherst, Spring 2025, under Prof. Doug Eddy.

## The Question

Boeing has run at a net loss for most years since 2019 — the 737 MAX groundings, COVID-19 demand collapse, and ongoing supply chain disruption all landed on the same balance sheet. Two questions followed from that: **how bad is it, exactly**, and **if Boeing were to invest in a new US production facility today, where should it go and does the math actually work?**

## Project 1 — Financial Ratio Analysis

Full ratio analysis using Boeing's own 10-K filings for fiscal years 2015–2024, pulled directly from SEC EDGAR / Boeing's investor relations site (every year individually cited — see the `SEC links` sheet in the Excel workbook).

**Method:** standard profitability, solvency, liquidity, and efficiency ratios (ROA, ROI, ROE, Debt Ratio, Debt-to-Equity, Current Ratio, Quick Ratio, Inventory Turnover, DSO), computed from the raw 10-K figures, not pulled from a pre-aggregated source like Macrotrends.

**What it found:**
- ROA peaked at 9.11% in 2018, then went negative from 2019 onward, bottoming at -8.31% in 2024
- ROE swung from a strong 25.49% in 2018 to erratic single digits post-2019 — the volatility itself is a signal of unstable equity
- Days Sales Outstanding rose from 33.89 days in 2015 to a peak of 66.67 days in 2021, meaning Boeing was waiting nearly twice as long to collect on receivables during its worst operational years
- The Debt Ratio jumped from ~0.09 (2015–2018) to 0.41 (2020–2021) as Boeing borrowed heavily to survive the MAX grounding and pandemic demand shock, and has only partially unwound since

## Project 2 — Facility Location Recommendation

Builds on Project 1's findings: since Boeing's core problem is capital discipline under financial strain, any new facility investment needs to clear a high bar. Evaluated five candidate cities (Everett WA, Charleston SC, Wichita KS, Huntsville AL, Fort Worth TX) on labor cost, logistics access, supplier proximity, and risk diversification, narrowing to a head-to-head between Charleston, SC and Wichita, KS.

**Method:** a 30-year cash-flow-after-tax (CFAT) model for each location, with revenue projected conservatively at 0.9% of Boeing's $77.8B annual revenue ($693M/year — deliberately below Boeing's historical 5–10% margin contribution, given the company's current financial strain). MACRS 39-year depreciation (IRS standard for non-residential real property), region-specific labor costs and tax rates, evaluated against IRR, NPV, Annual Worth, and Payback Period at a 10% MARR.

**Result — Wichita, KS recommended:**

| Metric | Charleston, SC | Wichita, KS |
|---|---|---|
| IRR | 4.48% | **23.04%** |
| NPV | -$67.2M | **$185.0M** |
| Annual Worth | -$7.13M | **$19.6M** |
| Payback Period | 16 years | **5 years** |

Charleston has the existing Boeing footprint and stronger port logistics, but loses on nearly every financial metric — lower labor cost, a stronger tax climate, and lower risk-of-overconcentration make Wichita the financially superior choice, despite Boeing having no existing presence there. "Air Capital of the World" branding aside, the numbers are what carried the recommendation.

## Sources

- Boeing 10-K filings, 2015–2024 (SEC EDGAR / Boeing Investor Relations)
- IRS MACRS Depreciation Tables (39-Year), irs.gov/publications/p946
- U.S. Bureau of Labor Statistics, Occupational Employment and Wage Statistics, bls.gov/oes
- U.S. Department of Commerce, Quadrennial Supply Chain Review (2021–2024)

## Files

- `Karthik_Krishnagiri_Pachiyappan_Project1.pdf` — full financial ratio analysis report
- `Karthik_Krishnagiri_Pachiyappan_Project2.pdf` — full facility location report
- `Karthik_Project_Budgeting_for_Engineers_Project1.xlsx` — ratio calculations, with a dedicated sheet linking every figure to its source 10-K
- `Karthik_Project_Budgeting_for_Engineers_Project2.xlsx` — CFAT model, assumptions, MACRS schedule, and full financials for both candidate locations
- `dashboard.html` — interactive Chart.js dashboard summarizing both projects (open directly, or view it live at the link above)

## Author

Karthik Krishnagiri Pachiyappan — M.S. Engineering Management, University of Massachusetts Amherst
