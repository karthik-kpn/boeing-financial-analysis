-- AI capital expenditure trend analysis
-- Deliberately simple SQL: SELECT, WHERE, GROUP BY, ORDER BY, basic
-- arithmetic and a couple of self-joins. No window functions, no CTEs.
-- The insight is in the interpretation, not the query complexity.

-- Q1: Combined hyperscaler capex by year, with year-over-year dollar
-- and percent growth computed by joining the table to itself on the
-- prior year.
SELECT
    curr.fiscal_year,
    curr.combined_low_b  AS capex_low_billion,
    curr.combined_high_b AS capex_high_billion,
    prev.combined_low_b  AS prior_year_low_billion,
    ROUND(curr.combined_low_b - prev.combined_low_b, 1)              AS yoy_change_billion,
    ROUND(100.0 * (curr.combined_low_b - prev.combined_low_b)
          / prev.combined_low_b, 1)                                   AS yoy_change_pct
FROM combined_capex curr
LEFT JOIN combined_capex prev
    ON curr.fiscal_year = prev.fiscal_year + 1
ORDER BY curr.fiscal_year;

-- Result:
-- 2024 | 223.0 | 223.0 | NULL  | NULL | NULL
-- 2025 | 410.0 | 413.0 | 223.0 | 187.0 | 83.9
-- 2026 | 725.0 | 760.0 | 410.0 | 315.0 | 76.8


-- Q2: Rank companies by their 2026 guided capex, largest first.
SELECT
    company,
    capex_low_b  AS guided_2026_low_billion,
    capex_high_b AS guided_2026_high_billion,
    note
FROM company_capex
WHERE fiscal_year = 2026
ORDER BY capex_low_b DESC;

-- Result (largest to smallest):
-- Amazon    | 200.0 | 200.0
-- Microsoft | 190.0 | 190.0
-- Alphabet  | 175.0 | 190.0
-- Meta      | 115.0 | 145.0


-- Q3: For each company, compare its most recent full-year actual
-- against its 2026 guidance to see whose spending is accelerating
-- fastest in dollar and percentage terms.
SELECT
    a.company,
    a.capex_low_b AS actual_2025_low_billion,
    g.capex_low_b AS guided_2026_low_billion,
    ROUND(g.capex_low_b - a.capex_low_b, 1) AS dollar_increase_billion,
    ROUND(100.0 * (g.capex_low_b - a.capex_low_b) / a.capex_low_b, 1) AS pct_increase
FROM company_capex a
JOIN company_capex g
    ON a.company = g.company
    AND g.fiscal_year = 2026
WHERE a.fiscal_year = 2025
ORDER BY pct_increase DESC;

-- Result:
-- Microsoft | 88.7  | 190.0 | 101.3 | 114.2%   <- more than doubling
-- Amazon    | 118.5 | 200.0 | 81.5  | 68.8%
-- Alphabet  | 91.0  | 175.0 | 84.0  | 92.3%
-- Meta      | 66.0  | 115.0 | 49.0  | 74.2%


-- Q4: How much of 2026's combined guided spend does each company
-- represent, as a share of the low-end combined total.
SELECT
    c.company,
    c.capex_low_b AS company_capex_billion,
    (SELECT combined_low_b FROM combined_capex WHERE fiscal_year = 2026) AS combined_total_billion,
    ROUND(100.0 * c.capex_low_b /
        (SELECT combined_low_b FROM combined_capex WHERE fiscal_year = 2026), 1) AS pct_of_combined
FROM company_capex c
WHERE c.fiscal_year = 2026
ORDER BY pct_of_combined DESC;

-- Result:
-- Amazon    | 200.0 / 725.0 = 27.6%
-- Microsoft | 190.0 / 725.0 = 26.2%
-- Alphabet  | 175.0 / 725.0 = 24.1%
-- Meta      | 115.0 / 725.0 = 15.9%
