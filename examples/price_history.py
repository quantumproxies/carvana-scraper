"""Daily price history of Carvana listings.

Reads the listings of each make/model pair and appends one row per car to
carvana_history.csv with a UTC timestamp, its price, previous price and
mileage. Run it once a day from cron; a car's rows over time show how its
price moves:

    0 7 * * *  cd /path/to/here && python price_history.py "Toyota/Camry" "Mercedes-Benz/GLA" Honda

Needs a login (`carvana-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_carvana_scraper import CarvanaScraper

FIELDS = ["checked_at", "vehicle_id", "vin", "year", "make", "model", "trim", "mileage", "price",
          "previous_price", "kbb_value", "purchase_pending", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("pairs", nargs="+", help='"Make/Model" pairs, or just "Make"')
    parser.add_argument("--max-results", type=int, default=96, help="listings per pair (max 96)")
    parser.add_argument("--out", default="carvana_history.csv")
    args = parser.parse_args()

    carvana = CarvanaScraper()
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        for pair in args.pairs:
            make, _, model = pair.partition("/")
            run = carvana.search(make.strip(), model=model.strip() or None, max_results=args.max_results)
            repriced = sum(1 for car in run if car.get("previous_price"))
            for car in run:
                writer.writerow({"checked_at": checked_at, **car})
                written += 1
            print(f"{pair}: {len(run)} cars, {repriced} repriced")
    print(f"{written} rows appended to {args.out}")


if __name__ == "__main__":
    main()
