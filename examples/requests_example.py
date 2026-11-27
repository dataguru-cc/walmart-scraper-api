"""Walmart scraper API: requests example.

Runs DataGuru's Walmart APIs and prints the JSON they return:
  - Walmart Product Details: $0.0018 per successful request ($1.80 per 1,000)
  - Walmart Search: $0.0018 per successful request ($1.80 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/requests_example.py
    python examples/requests_example.py walmart-products-details
"""
import json
import os
import re
import sys

import requests

API_KEY = os.environ.get("DATAGURU_API_KEY") or sys.exit("Set DATAGURU_API_KEY (https://dashboard.dataguru.cc)")

# Every Walmart API: endpoint, method and example input. Parameters go in the query string or the
# JSON body as each endpoint expects. "from" means the input URL is taken from another API's results.
# Entries marked needs_input hold a placeholder value: replace it, then run that API by name.
CALLS = {
    "walmart-products-details": {
        "name": "Walmart Product Details",
        "method": "POST",
        "url": "https://api.dataguru.cc/api/v1/walmart/products/details",
        "query": {},
        "body": {
            "product_url": "https://www.walmart.com/ip/New-Gourmia-1700W-6-Slice-Digital-Toaster-Oven-Air-Fryer-With-19-One-Touch-Presets-Stainless-Steel/1438286796?classType=VARIANT&athbdg=L1102"
        }
    },
    "walmart-search": {
        "name": "Walmart Search",
        "method": "POST",
        "url": "https://api.dataguru.cc/api/v1/walmart/search",
        "query": {},
        "body": {
            "query": "https://www.walmart.com/search?q=air+fryer"
        }
    }
}


def run(session, name, results):
    """Calls one API (and the search it depends on, if any) and returns its JSON."""
    if name in results:
        return results[name]
    call = CALLS[name]
    query, body = dict(call["query"]), dict(call["body"])
    if "from" in call:
        src = call["from"]
        match = re.search(src["match"], json.dumps(run(session, src["api"], results)))
        if not match:
            raise RuntimeError(f"No URL found in the {src['api']} results")
        (query if src["param"] in query else body)[src["param"]] = match.group(0)
    response = session.request(
        call["method"], call["url"], params=query or None,
        json=body if call["method"] != "GET" else None, timeout=300,
    )
    data = response.json()
    if response.status_code >= 400 or data.get("success") is False:
        error = data.get("error") or {}
        raise RuntimeError(f"{name}: HTTP {response.status_code} {error.get('code')}: {error.get('message')}")
    results[name] = data
    return data


def main(names):
    with requests.Session() as session:
        session.headers["Authorization"] = f"Api-Key {API_KEY}"
        results = {}
        for name in names:
            data = run(session, name, results)
            print(f"== {CALLS[name]['name']} ({name})")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or [n for n, c in CALLS.items() if not c.get("needs_input")]
    unknown = [n for n in names if n not in CALLS]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(CALLS)}")
    try:
        main(names)
    except (requests.RequestException, RuntimeError) as error:
        sys.exit(str(error))
