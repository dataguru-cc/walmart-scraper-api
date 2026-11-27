"""Walmart scraper API: Scrapy spider example.

Runs DataGuru's Walmart APIs and prints the JSON they return:
  - Walmart Product Details: $0.0018 per successful request ($1.80 per 1,000)
  - Walmart Search: $0.0018 per successful request ($1.80 per 1,000)

Setup:
    pip install -r requirements.txt
    export DATAGURU_API_KEY="your key"   # free credit at https://dashboard.dataguru.cc

Run:
    scrapy runspider examples/scrapy_spider.py -O walmart.json
    scrapy runspider examples/scrapy_spider.py -a apis=walmart-products-details -O walmart.json
"""
import json
import os
import re
from urllib.parse import urlencode

import scrapy

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


class WalmartSpider(scrapy.Spider):
    """Each DataGuru call is one Scrapy request; detail APIs are requested from the search callback."""

    name = "walmart"
    custom_settings = {
        "CONCURRENT_REQUESTS": 4,
        "DOWNLOAD_TIMEOUT": 300,      # some sites take a while to scrape
        "RETRY_ENABLED": False,       # a retried request could be billed twice
        "HTTPERROR_ALLOW_ALL": True,  # errors come back as JSON; parse() reports them
        "ROBOTSTXT_OBEY": False,      # requests go to api.dataguru.cc, not the website itself
    }

    def __init__(self, apis=None, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.environ.get("DATAGURU_API_KEY")
        if not self.api_key:
            raise ValueError("Set DATAGURU_API_KEY (https://dashboard.dataguru.cc)")
        self.wanted = apis.split(",") if apis else [n for n, c in CALLS.items() if not c.get("needs_input")]
        unknown = [n for n in self.wanted if n not in CALLS]
        if unknown:
            raise ValueError(f"Unknown API {unknown}. Choose from: {', '.join(CALLS)}")

    def request_for(self, name, value=None):
        call = CALLS[name]
        query, body = dict(call["query"]), dict(call["body"])
        if value is not None:
            param = call["from"]["param"]
            (query if param in query else body)[param] = value
        url = call["url"] + ("?" + urlencode(query) if query else "")
        headers = {"Authorization": f"Api-Key {self.api_key}"}
        if call["method"] == "GET":
            return scrapy.Request(url, headers=headers, callback=self.parse, cb_kwargs={"name": name})
        return scrapy.http.JsonRequest(url, data=body, method=call["method"], headers=headers,
                                       callback=self.parse, cb_kwargs={"name": name})

    async def start(self):  # Scrapy 2.13+
        for request in self.start_requests():
            yield request

    def start_requests(self):  # older Scrapy
        # Detail APIs need a URL from their search first; request the search instead.
        needed = dict.fromkeys(CALLS[n]["from"]["api"] if "from" in CALLS[n] else n for n in self.wanted)
        for name in needed:
            yield self.request_for(name)

    def parse(self, response, name):
        data = json.loads(response.text)
        if response.status >= 400 or data.get("success") is False:
            self.logger.error("%s failed: %s", name, data.get("error"))
            return
        if name in self.wanted:
            yield {"api": name, "data": data}
        # Feed the first matching URL into each detail API that depends on this one.
        for detail, call in CALLS.items():
            if call.get("from", {}).get("api") == name and detail in self.wanted:
                match = re.search(call["from"]["match"], json.dumps(data))
                if match:
                    yield self.request_for(detail, match.group(0))
                else:
                    self.logger.warning("No URL for %s in the %s results", detail, name)
