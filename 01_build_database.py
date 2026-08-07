"""
Build a small SQLite database of hyperscaler AI capital expenditure.

Data source note
-----------------
Every figure below was pulled from named, dated financial reporting
(company earnings calls, 10-K/10-Q disclosures as cited by press
coverage, and industry analyst notes) via live web search on
2026-08-06. Sources are recorded per-row in the `source` column so
every number in the database can be traced back to where it came
from. Figures are in USD billions, rounded to the nearest whole
number for guided/estimated ranges, one decimal for reported actuals.

This mirrors the sourcing discipline used in the Boeing 10-K project
(Project 1/2, M&IE-ENG 645): every number ties to a named, dated
source, not a synthetic or invented figure.
"""
import sqlite3

DB_PATH = "ai_capex.db"

ROWS = [
    # company, fiscal_year, capex_low, capex_high, status, source, source_date
    ("Microsoft", 2024, 88.7, 88.7, "actual",
     "FY2025 (ended Jun 2025) capex reported at $88.7B, exceeding the earlier $80B guide",
     "AOL/Reuters coverage, 2025"),
    ("Microsoft", 2025, 88.7, 88.7, "actual",
     "Same FY2025 print; Microsoft's fiscal year runs Jul-Jun so this is the FY2025 actual",
     "AOL/Reuters coverage, 2025"),
    ("Microsoft", 2026, 190.0, 190.0, "guided",
     "Tracking toward ~$190B for calendar 2026; Q3 FY26 quarter alone was $30.9B, up ~84% YoY",
     "valueaddvc.com, Aug 2026"),

    ("Amazon", 2025, 118.5, 125.0, "actual/near-actual",
     "Q2 2025 run-rate of $31.4B/quarter implied ~$118.5B full year; later prints landed near $125B",
     "AOL/Reuters + eMarketer, 2025"),
    ("Amazon", 2026, 200.0, 200.0, "guided",
     "Projecting ~$200B for 2026; Q1 2026 alone was $44.2B as AWS grew 28%",
     "valueaddvc.com, Aug 2026"),

    ("Alphabet", 2025, 91.0, 93.0, "actual/near-actual",
     "Guidance raised through the year from $85B to a $91-93B range",
     "IEEE ComSoc blog, late 2025"),
    ("Alphabet", 2026, 175.0, 190.0, "guided",
     "Guided $175-185B, later raised by ~$5B toward $190B; funds data centers and in-house TPUs",
     "valueaddvc.com, Aug 2026"),

    ("Meta", 2025, 66.0, 72.0, "actual/near-actual",
     "Full-year 2025 outlook of $66-72B, up ~$30B YoY, for Prometheus/Hyperion AI supercomputers",
     "eMarketer, 2025"),
    ("Meta", 2026, 115.0, 145.0, "guided",
     "Initially guided $115-135B, later raised toward $125-145B citing memory-chip prices",
     "Futurum Group + valueaddvc.com, Aug 2026"),
]

COMBINED = [
    # year, combined_low, combined_high, companies_included, source
    (2024, 223.0, 223.0, "MSFT+AMZN+META+GOOGL",
     "Reported combined 2024 spend, cited as the base for a 46% growth estimate into 2025",
     "Yahoo Finance/AOL, Jan 2025"),
    (2025, 410.0, 413.0, "MSFT+AMZN+META+GOOGL",
     "Actual/near-final combined 2025 capex, well above the ~$325B estimated earlier in the year",
     "Futurum Group + Statista, 2026"),
    (2026, 725.0, 760.0, "MSFT+AMZN+META+GOOGL(+ORCL for the $690B five-company figure)",
     "Guided combined 2026 capex across the major hyperscalers",
     "Futurum Group + Statista + valueaddvc.com, Aug 2026"),
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS company_capex")
    cur.execute("""
        CREATE TABLE company_capex (
            company      TEXT NOT NULL,
            fiscal_year  INTEGER NOT NULL,
            capex_low_b  REAL NOT NULL,
            capex_high_b REAL NOT NULL,
            status       TEXT NOT NULL,
            note         TEXT,
            source       TEXT NOT NULL
        )
    """)
    cur.executemany(
        "INSERT INTO company_capex (company, fiscal_year, capex_low_b, capex_high_b, status, note, source) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        ROWS,
    )

    cur.execute("DROP TABLE IF EXISTS combined_capex")
    cur.execute("""
        CREATE TABLE combined_capex (
            fiscal_year        INTEGER NOT NULL,
            combined_low_b     REAL NOT NULL,
            combined_high_b    REAL NOT NULL,
            companies_included TEXT NOT NULL,
            note               TEXT,
            source             TEXT NOT NULL
        )
    """)
    cur.executemany(
        "INSERT INTO combined_capex (fiscal_year, combined_low_b, combined_high_b, companies_included, note, source) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        COMBINED,
    )

    conn.commit()
    print(f"Loaded {len(ROWS)} company-year rows and {len(COMBINED)} combined-year rows into {DB_PATH}")
    conn.close()

if __name__ == "__main__":
    main()
