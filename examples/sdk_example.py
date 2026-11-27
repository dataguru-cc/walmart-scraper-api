"""Walmart scraper API: DataGuru Python SDK example.

Runs DataGuru's Walmart APIs and prints the JSON they return:
  - Walmart Product Details: $0.0018 per successful request ($1.80 per 1,000)
  - Walmart Search: $0.0018 per successful request ($1.80 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    python examples/sdk_example.py            # every API below
    python examples/sdk_example.py walmart-products-details
"""
import json
import sys
from pathlib import Path

from dataguru import DataGuru, DataGuruError

def walmart_products_details(dg):
    """Walmart Product Details: Scrape Walmart product details, pricing, stock, local store pickup, aisle location, and seller info."""
    return dg.call(
        "walmart-products-details",
        product_url="https://www.walmart.com/ip/New-Gourmia-1700W-6-Slice-Digital-Toaster-Oven-Air-Fryer-With-19-One-Touch-Presets-Stainless-Steel/1438286796?classType=VARIANT&athbdg=L1102",
    )


def walmart_search(dg):
    """Walmart Search: Search Walmart by keyword or search URL and get matching products, seller details, ratings and reviews."""
    return dg.call(
        "walmart-search",
        query="https://www.walmart.com/search?q=air+fryer",
    )


EXAMPLES = {
    "walmart-products-details": walmart_products_details,
    "walmart-search": walmart_search,
}
DEFAULT = ['walmart-products-details', 'walmart-search']


def main(names):
    out = Path("output")
    out.mkdir(exist_ok=True)
    with DataGuru() as dg:  # reads DATAGURU_API_KEY
        for name in names:
            data = EXAMPLES[name](dg)
            (out / f"{name}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{name}: saved output/{name}.json")
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1500])


if __name__ == "__main__":
    names = sys.argv[1:] or DEFAULT
    unknown = [n for n in names if n not in EXAMPLES]
    if unknown:
        sys.exit(f"Unknown API {unknown}. Choose from: {', '.join(EXAMPLES)}")
    try:
        main(names)
    except DataGuruError as error:
        sys.exit(f"DataGuru error: {error}")
