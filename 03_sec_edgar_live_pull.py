"""
Reusable SEC EDGAR XBRL puller.

Pulls a real, current XBRL financial concept (e.g. total current assets,
capital expenditure) straight from data.sec.gov for any US public
company, using its official free API. No API key or login required.

WHAT THIS SCRIPT IS
--------------------
This is the live-data mechanism behind the Boeing 10-K validation and
the AI capex research: point it at any company's CIK and any XBRL
tag, and it returns every value that company has ever reported for
that line item, straight from SEC filings.

HOW TO USE IT
-------------
    python 03_sec_edgar_live_pull.py 0000012927 AssetsCurrent
    python 03_sec_edgar_live_pull.py 0000012927 LiabilitiesCurrent
    python 03_sec_edgar_live_pull.py 0000789019 PaymentsToAcquirePropertyPlantAndEquipment

First argument: the company's CIK (Boeing = 0000012927, Microsoft =
0000789019, Amazon = 0001018724, Meta = 0001326801, Alphabet =
0001652044, Nvidia = 0001045810). Look any company up at
https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany

Second argument: the XBRL tag, e.g. Assets, AssetsCurrent,
LiabilitiesCurrent, NetIncomeLoss, Revenues, ResearchAndDevelopmentExpense,
PaymentsToAcquirePropertyPlantAndEquipment. Full tag list:
https://www.sec.gov/info/edgar/edgartaxonomies.shtml

WHY THIS WASN'T RUN LIVE END-TO-END FOR EVERY COMPANY IN THIS SESSION
------------------------------------------------------------------------
This script needs unrestricted outbound HTTPS access. The assistant
session that wrote it only had (a) a sandboxed shell with network
access limited to a handful of package registries, and (b) a web-fetch
tool that can only retrieve a URL that has already appeared verbatim in
a prior search result -- it cannot construct a new arbitrary API call
on the fly. That combination made it possible to pull SOME real,
verified figures directly (Apple's reported revenue history, Amazon's
full XBRL fact set) but not to reliably reach Boeing's or the AI
companies' specific line items on request.

The script itself is standard, correct, and does not depend on any of
that -- run it from a normal machine with internet access (your laptop,
a Colab notebook, GitHub Actions, etc.) and it will pull live data for
any company and tag the moment you run it.
"""
import sys
import time
import json
import urllib.request

HEADERS = {
    # SEC's fair-access policy requires a descriptive User-Agent with a
    # real contact. Replace this with your own name/email before using
    # this script for real work.
    "User-Agent": "Personal research script (replace-with-your-email@example.com)"
}


def get_company_concept(cik: str, tag: str, taxonomy: str = "us-gaap") -> dict:
    """Fetch every historical value a company has reported for one XBRL tag."""
    cik_padded = str(int(cik)).zfill(10)
    url = f"https://data.sec.gov/api/xbrl/companyconcept/CIK{cik_padded}/{taxonomy}/{tag}.json"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def annual_values(concept_json: dict, unit: str = "USD"):
    """Filter down to 10-K (annual) reported values, most recent first."""
    values = concept_json.get("units", {}).get(unit, [])
    annual = [v for v in values if v.get("form") == "10-K" and v.get("fp") == "FY"]
    return sorted(annual, key=lambda v: v["end"], reverse=True)


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    cik, tag = sys.argv[1], sys.argv[2]
    print(f"Fetching {tag} for CIK {cik} ...")
    data = get_company_concept(cik, tag)
    print(f"Entity: {data.get('entityName')}")
    print(f"Label:  {data.get('label')}")

    for v in annual_values(data)[:10]:
        print(f"  FY{v['fy']}  ({v['end']}):  ${v['val']:,}  [filed {v['filed']}, form {v['form']}]")

    time.sleep(0.1)  # be polite to SEC's servers if calling this in a loop


if __name__ == "__main__":
    main()
