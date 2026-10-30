# Carvana Scraper API

[![ci](https://github.com/quantumproxies/carvana-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/carvana-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Carvana's used-car inventory from Python or the command line: every listing for a make and model, or the whole inventory, with price, previous price, MSRP, Kelley Blue Book value, mileage, VIN, stock number, trim, colours, MPG, seats and listing tags, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/carvana-scraper
carvana-scraper login
carvana-scraper search Toyota --model Camry --max-results 96 -o camry.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=carvana-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `carvana-scraper search` | make, optional with --model | Year/make/model/trim, price, MSRP, mileage, VIN and stock number, 31 fields per row ([fields and price](https://quanticdata.io/collectors/carvana-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=carvana-scraper)) | up to 96 |

Prices are in USD and mileage in miles. Pass a make as the first argument and `--model` to narrow it (the model needs a make), or run `carvana-scraper search` alone to browse the whole inventory. `previous_price` is set when Carvana has repriced a car; `kbb_value` and `market_adjustment` put the price next to its Kelley Blue Book value and MSRP reference.

## Sample output

A real row from `carvana-scraper search Toyota --model Camry --max-results 3` (2026-10-23):

```json
{
  "mpg": 29,
  "url": "https://www.carvana.com/vehicle/4793634",
  "vin": "4T1T11AK1PU834020",
  "make": "Toyota",
  "msrp": 28955,
  "rank": 1,
  "tags": [
    "New Price",
    "Great Deal"
  ],
  "trim": "SE",
  "year": 2023,
  "image": "https://cdnblob.fastly.carvana.io/3006743294/post-large/normalized/zoomcrop/3006743294-edc-02.jpg?v=2026.10.23_9.51.11",
  "model": "Camry",
  "price": 26590,
  "mileage": 30448,
  "kbb_trim": "SE Sedan 4D",
  "condition": "Used",
  "fuel_type": "Gas",
  "kbb_value": 28306,
  "body_style": "Sedan",
  "image_hero": "https://vexgateway.fastly.carvana.io/3006743294/standardizedHero.jpg?v=1790968647.075",
  "vehicle_id": "4793634",
  "parent_model": "Camry",
  "stock_number": "3006743294",
  "purchase_type": "Purchasable",
  "shipping_cost": 0,
  "exterior_color": "White",
  "interior_color": "Black",
  "previous_price": 26990,
  "discount_amount": 0,
  "purchase_pending": false,
  "seating_capacity": 5,
  "market_adjustment": -2365
}
```

## Python

```python
from quanticdata_carvana_scraper import CarvanaScraper

carvana = CarvanaScraper()  # saved login, or QUANTICDATA_API_KEY

camrys = carvana.search("Toyota", model="Camry", max_results=96)
for car in camrys:
    print(car["year"], car["trim"], car["mileage"], car["price"], car["kbb_value"])
camrys.to_csv("camry.csv")

under_kbb = [c for c in camrys if c["price"] and c["kbb_value"] and c["price"] < c["kbb_value"]]
print(len(under_kbb), "Camrys priced under their Kelley Blue Book value")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Cars under book value**: List the cars of a make and model priced under their Kelley Blue Book value, biggest gap first, with year, trim, mileage and VIN. See [`examples/under_kbb.py`](examples/under_kbb.py).
- **Price history**: Snapshot the inventory of a few models every day and keep one history CSV, to see how the price of each car moves. See [`examples/price_history.py`](examples/price_history.py).
- **Inventory summary**: Summarise a make by model and model year: cars listed, median price, median mileage and how many are already in a purchase. See [`examples/inventory_summary.py`](examples/inventory_summary.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `carvana-scraper run <id> -o out.csv` collects it later.

### `carvana-scraper search`

Carvana used-car inventory — year/make/model/trim, price, MSRP, mileage, VIN and stock number.

```
carvana-scraper search [MAKE] [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `MAKE` | string |  | Vehicle make, e.g. "Toyota" or "Mercedes-Benz". Omit to browse all inventory. |
| `--model` | string |  | Vehicle model (requires make), e.g. "Camry". |
| `--max-results` | integer | `24` | How many listings to deliver at most (1–96). You pay only for delivered listings. |

## Output fields

<details><summary><code>carvana-scraper search</code>: 31 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `vehicle_id` | string or null | Carvana vehicle id — the key in the listing URL. |
| `stock_number` | string or null | Carvana stock number. |
| `vin` | string or null | VIN. |
| `year` | integer or null | Model year. |
| `make` | string or null | Make. |
| `model` | string or null | Model, including the variant ("Camry Hybrid"). |
| `parent_model` | string or null | Model family ("Camry" for a Camry Hybrid). |
| `trim` | string or null | Trim, e.g. "SEL". |
| `kbb_trim` | string or null | Kelley Blue Book long trim, e.g. "SEL Sport Utility 4D". |
| `condition` | string or null | Offering as Carvana states it ("Used"). |
| `price` | number or null | Carvana price in USD. |
| `msrp` | number or null | Original MSRP in USD. |
| `previous_price` | number or null | Price before the last change; null when never repriced. |
| `mileage` | integer or null | Odometer miles. |
| `body_style` | string or null | Body style, e.g. "Suv". |
| `fuel_type` | string or null | Fuel type, e.g. "Gas". |
| `exterior_color` | string or null | Exterior colour. |
| `interior_color` | string or null | Interior colour. |
| `mpg` | integer or null | Miles per gallon. |
| `seating_capacity` | integer or null | Seats. |
| `image` | string or null | Primary photo. |
| `url` | string or null | Listing URL. |
| `kbb_value` | number or null | Kelley Blue Book value Carvana shows for the car. |
| `market_adjustment` | number or null | Difference between price and MSRP reference (negative = below). |
| `shipping_cost` | number or null | Transport cost included in the offer (0 when free). |
| `discount_amount` | number or null | Total discount applied. |
| `tags` | string[] | Listing tags ("Recently Added", "Great Deal"…). |
| `purchase_pending` | boolean | True when another buyer has a purchase in progress. |
| `purchase_type` | string or null | Purchase status (Purchasable…). |
| `image_hero` | string or null | Standardized hero image URL. |

</details>

## Sign-in and API keys

- `carvana-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `carvana-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `carvana-scraper login --api-key`.
- `carvana-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=carvana-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/carvana_cars/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"make": "Toyota", "model": "Camry", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=carvana-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=carvana-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Carvana scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a make, and optionally a model, and get rows back; the requests run on QuanticData's side.

**What are kbb_value and market_adjustment?**

kbb_value is the Kelley Blue Book value Carvana shows for the car. market_adjustment is the difference between the price and the MSRP reference, negative when the car is priced below it.

**How many cars can one run return?**

Up to 96 listings per run; ask for fewer with --max-results and you pay only for what is delivered.

**Can I export to CSV or Excel?**

Add -o cars.csv (or .json, .jsonl). Each car is one row and its tags are joined with '; ', so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/price_history.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Subito Scraper API](https://github.com/quantumproxies/subito-scraper): Subito scraper for Python and the command line.
- [Kleinanzeigen Scraper](https://github.com/quantumproxies/kleinanzeigen-scraper): Kleinanzeigen scraper for Python and the command line.
- [Zillow Scraper](https://github.com/quantumproxies/zillow-scraper): Zillow scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=carvana-scraper).
