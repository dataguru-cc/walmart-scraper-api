# Walmart Scraper API

Scrape Walmart with a JSON API. This repo has working Python examples for DataGuru's Walmart scraper APIs: Walmart Product Details and Walmart Search.

[DataGuru](https://dataguru.cc) runs the scraping, proxies, retries and parsing, and returns clean JSON. You pay only for successful requests, from $0.0018 per request, out of a prepaid balance: no subscription. New accounts get $1.00 of free credit.

## Walmart APIs

| API | What it returns | Price | Page |
| --- | --- | --- | --- |
| [Walmart Product Details](#walmart-product-details) | Scrape Walmart product details, pricing, stock, local store pickup, aisle location, and seller info. | $0.0018 | [https://dataguru.cc/apis/walmart-products-details/](https://dataguru.cc/apis/walmart-products-details/) |
| [Walmart Search](#walmart-search) | Search Walmart by keyword or search URL and get matching products, seller details, ratings and reviews. | $0.0018 | [https://dataguru.cc/apis/walmart-search/](https://dataguru.cc/apis/walmart-search/) |

## Quick start

1. Create a free account and an API key at [dashboard.dataguru.cc](https://dashboard.dataguru.cc).
2. Install and run:

```bash
git clone https://github.com/dataguru-cc/walmart-scraper-api.git
cd walmart-scraper-api
pip install -r requirements.txt
export DATAGURU_API_KEY="your key"
python examples/sdk_example.py walmart-products-details
```

## Examples

Every example covers all 2 Walmart APIs. Pass an API name to run just one; with no name each script runs them all, and each call is billed at the price above.

| File | Style | Run |
| --- | --- | --- |
| [`examples/sdk_example.py`](examples/sdk_example.py) | [DataGuru Python SDK](https://github.com/dataguru-cc/dataguru-python) (`pip install dataguru-sdk`), one function per API, saves JSON to `output/` | `python examples/sdk_example.py` |
| [`examples/requests_example.py`](examples/requests_example.py) | Plain `requests`, synchronous | `python examples/requests_example.py` |
| [`examples/async_example.py`](examples/async_example.py) | `asyncio` + `httpx`, concurrent with a limit | `python examples/async_example.py` |
| [`examples/scrapy_spider.py`](examples/scrapy_spider.py) | Scrapy spider, items to JSON/CSV | `scrapy runspider examples/scrapy_spider.py -O walmart.json` |

All requests use the header `Authorization: Api-Key YOUR_API_KEY`. Errors return `{"success": false, "error": {"code", "message", "request_id"}}`, with HTTP 402 when the balance runs out and 429 (with `Retry-After`) when rate limited. Failed requests are not charged.

## API reference

### Walmart Product Details

Scrape Walmart product details, pricing, stock, local store pickup, aisle location, and seller info.

- Endpoint: `POST https://api.dataguru.cc/api/v1/walmart/products/details`
- Price: $0.0018 per successful request ($1.80 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/walmart-products-details/
- Documentation: https://dataguru.cc/documentation/walmart-products-details/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `location` | string | no | Two-letter country code to localise results (e.g. US). Default: `US`. |
| `product_url` | string | yes | Provide the full Walmart Product URL to scrape. |
| `zip_code` | string | no | US ZIP code to check local pickup availability and aisle location (e.g. 75001). |

**Response fields:** `search_information`, `product_results`, `reviews_results`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/walmart/products/details" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"product_url": "https://www.walmart.com/ip/New-Gourmia-1700W-6-Slice-Digital-Toaster-Oven-Air-Fryer-With-19-One-Touch-Presets-Stainless-Steel/1438286796?classType=VARIANT&athbdg=L1102"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "search_information": {
    "location": {
      "postal_code": "string",
      "province_code": "string",
      "city": "string"
    }
  },
  "product_results": {
    "us_item_id": "1234567890",
    "product_id": "1234567890",
    "variants": [
      "string"
    ],
    "upc": "string",
    "title": "string",
    "short_description": "string",
    "description": "string",
    "seller_id": "1234567890",
    "seller_name": "string",
    "has_seller_badge": false,
    "brand": "string",
    "standard_delivery_date": "2026-01-01T12:00:00Z",
    "fulfillment_type": "string",
    "in_stock": false,
    "out_of_stock": false,
    "price": 0.0,
    "currency": "USD",
    "was_price": 0.0,
    "fulfillment_badge": "string",
    "fulfillment_title": "string",
    "images": [
      "https://example.com/..."
    ],
    "specifications": [
      {
        "name": "string",
        "value": "string"
      }
    ],
    "variant_categories": [
      "string"
    ],
    "selections": [
      "string"
    ]
  },
  "reviews_results": {
    "ratings": [
      {
        "stars": 0,
        "count": 0,
        "percentage": 0.0
      }
    ],
    "reviews": {
      "rating": 0.0,
      "count": 0,
      "recommended_percentage": 0,
      "top_positive": {},
      "top_negative": {},
      "top_mentions": [
        "string"
      ],
      "customer_reviews": [
        "string"
      ]
    }
  },
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Walmart Product Details",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

### Walmart Search

Search Walmart by keyword or search URL and get matching products, seller details, ratings and reviews.

- Endpoint: `POST https://api.dataguru.cc/api/v1/walmart/search`
- Price: $0.0018 per successful request ($1.80 per 1,000)
- Rate limit: 60 requests/minute
- Page and live playground: https://dataguru.cc/apis/walmart-search/
- Documentation: https://dataguru.cc/documentation/walmart-search/

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `location` | string | no | Two-letter country code to localise results (e.g. US). Default: `US`. |
| `page` | integer | no | Page number of search results. Default: `1`. |
| `query` | string | yes | Search keyword or full Walmart search URL (e.g. "air fryer" or "https://www.walmart.com/search?q=air+fryer"). |

**Response fields:** `title`, `description`, `totalItemCount`, `item`, plus `_metadata`

```bash
curl -X POST "https://api.dataguru.cc/api/v1/walmart/search" \
  -H "Authorization: Api-Key $DATAGURU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "https://www.walmart.com/search?q=air+fryer"}'
```

<details><summary>Response schema</summary>

Values are type placeholders from the API's published schema, not real data.

```json
{
  "search_results": [
    {
      "title": "string",
      "description": "string",
      "totalItemCount": 0,
      "item": [
        {
          "title": "string",
          "id": "1234567890",
          "usItemId": "1234567890",
          "type": "string",
          "thumbnail": "https://example.com/...",
          "brand": "string",
          "canonicalUrl": "https://example.com/...",
          "returnPolicy": {},
          "rating": {
            "averageRating": 0.0,
            "numberOfReviews": 0
          },
          "fulfillment": {
            "isEligibleForPickup": false,
            "isEligibleForDelivery": false
          },
          "priceInfo": {
            "linePrice": "string",
            "itemPrice": "string",
            "unitPrice": "string"
          },
          "orderLimit": 0,
          "isSponsoredFlag": false,
          "shippingOption": "string"
        }
      ]
    }
  ],
  "_metadata": {
    "request_id": "3f6c1a2e-8b4d-4c1e-9a7f-2d5e6b7c8d9e",
    "execution_time_ms": 842,
    "endpoint": "Walmart Search",
    "mode": "live",
    "format": "json",
    "timestamp": "2026-01-01T12:00:00+00:00"
  }
}
```

</details>

## More

- Python SDK and examples for all DataGuru APIs: [github.com/dataguru-cc/dataguru-python](https://github.com/dataguru-cc/dataguru-python) ([docs](https://dataguru-python.readthedocs.io/))
- Every API, with a live playground: [https://dataguru.cc/apis/](https://dataguru.cc/apis/)
- Use DataGuru from Claude, ChatGPT or Cursor through the MCP server: [https://dataguru.cc/mcp/](https://dataguru.cc/mcp/)
- Run thousands of inputs from a CSV at half price with batch jobs: [https://dataguru.cc/documentation/](https://dataguru.cc/documentation/)
- Other scraper APIs: [1688](https://github.com/dataguru-cc/1688-scraper-api), [Airbnb](https://github.com/dataguru-cc/airbnb-scraper-api), [Alibaba](https://github.com/dataguru-cc/alibaba-scraper-api), [AliExpress](https://github.com/dataguru-cc/aliexpress-scraper-api), [Amazon](https://github.com/dataguru-cc/amazon-scraper-api), [arXiv](https://github.com/dataguru-cc/arxiv-scraper-api), [ASOS](https://github.com/dataguru-cc/asos-scraper-api), [Best Buy](https://github.com/dataguru-cc/best-buy-scraper-api), [Booking.com](https://github.com/dataguru-cc/booking-scraper-api), [Brave Search](https://github.com/dataguru-cc/brave-search-scraper-api), [CA State Bar](https://github.com/dataguru-cc/california-state-bar-scraper-api), [Capterra](https://github.com/dataguru-cc/capterra-scraper-api), [CoinGecko](https://github.com/dataguru-cc/coingecko-scraper-api), [CoinMarketCap](https://github.com/dataguru-cc/coinmarketcap-scraper-api), [Companies House](https://github.com/dataguru-cc/companies-house-scraper-api), [Costco](https://github.com/dataguru-cc/costco-scraper-api), [CourtListener](https://github.com/dataguru-cc/courtlistener-scraper-api), [Crunchbase](https://github.com/dataguru-cc/crunchbase-scraper-api), [Discord](https://github.com/dataguru-cc/discord-scraper-api), [DoorDash](https://github.com/dataguru-cc/doordash-scraper-api), [eBay](https://github.com/dataguru-cc/ebay-scraper-api), [Etsy](https://github.com/dataguru-cc/etsy-scraper-api), [Expedia](https://github.com/dataguru-cc/expedia-scraper-api), [Fiverr](https://github.com/dataguru-cc/fiverr-scraper-api), [Flipkart](https://github.com/dataguru-cc/flipkart-scraper-api), [Glassdoor](https://github.com/dataguru-cc/glassdoor-scraper-api), [Google Flights](https://github.com/dataguru-cc/google-flights-scraper-api), [Google Patents](https://github.com/dataguru-cc/google-patents-scraper-api), [Google Scholar](https://github.com/dataguru-cc/google-scholar-scraper-api), [Google Search](https://github.com/dataguru-cc/google-search-scraper-api), [Grubhub](https://github.com/dataguru-cc/grubhub-scraper-api), [Home Depot](https://github.com/dataguru-cc/home-depot-scraper-api), [Instagram](https://github.com/dataguru-cc/instagram-scraper-api), [Investing.com](https://github.com/dataguru-cc/investing-com-scraper-api), [Justia](https://github.com/dataguru-cc/justia-scraper-api), [Kayak](https://github.com/dataguru-cc/kayak-scraper-api), [Kick](https://github.com/dataguru-cc/kick-scraper-api), [Lazada](https://github.com/dataguru-cc/lazada-scraper-api), [MarketWatch](https://github.com/dataguru-cc/marketwatch-scraper-api), [Mercado Libre](https://github.com/dataguru-cc/mercado-libre-scraper-api), [Monster](https://github.com/dataguru-cc/monster-scraper-api), [OpenCorporates](https://github.com/dataguru-cc/opencorporates-scraper-api), [OpenTable](https://github.com/dataguru-cc/opentable-scraper-api), [PACER](https://github.com/dataguru-cc/pacer-scraper-api), [PitchBook](https://github.com/dataguru-cc/pitchbook-scraper-api), [PubMed](https://github.com/dataguru-cc/pubmed-scraper-api), [Reddit](https://github.com/dataguru-cc/reddit-scraper-api), [Redfin](https://github.com/dataguru-cc/redfin-scraper-api), [Resy](https://github.com/dataguru-cc/resy-scraper-api), [Rightmove](https://github.com/dataguru-cc/rightmove-scraper-api), [SEC EDGAR](https://github.com/dataguru-cc/sec-edgar-scraper-api), [Seeking Alpha](https://github.com/dataguru-cc/seeking-alpha-scraper-api), [Shopee](https://github.com/dataguru-cc/shopee-scraper-api), [Skyscanner](https://github.com/dataguru-cc/skyscanner-scraper-api), [Target](https://github.com/dataguru-cc/target-scraper-api), [TikTok](https://github.com/dataguru-cc/tiktok-scraper-api), [TradingView](https://github.com/dataguru-cc/tradingview-scraper-api), [TripAdvisor](https://github.com/dataguru-cc/tripadvisor-scraper-api), [Trulia](https://github.com/dataguru-cc/trulia-scraper-api), [TrustRadius](https://github.com/dataguru-cc/trustradius-scraper-api), [Twitch](https://github.com/dataguru-cc/twitch-scraper-api), [Uber Eats](https://github.com/dataguru-cc/uber-eats-scraper-api), [Upwork](https://github.com/dataguru-cc/upwork-scraper-api), [Vrbo](https://github.com/dataguru-cc/vrbo-scraper-api), [Wayfair](https://github.com/dataguru-cc/wayfair-scraper-api), [X (Twitter)](https://github.com/dataguru-cc/twitter-scraper-api), [Yahoo Finance](https://github.com/dataguru-cc/yahoo-finance-scraper-api), [YouTube](https://github.com/dataguru-cc/youtube-scraper-api), [Zillow](https://github.com/dataguru-cc/zillow-scraper-api), [ZoomInfo](https://github.com/dataguru-cc/zoominfo-scraper-api), [Zoopla](https://github.com/dataguru-cc/zoopla-scraper-api)

## License

The example code is MIT licensed. Use of the DataGuru API is subject to the [terms of service](https://dataguru.cc/terms/).
