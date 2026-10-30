"""Carvana inventory of one make, summarised by model and model year.

    python inventory_summary.py Toyota
    python inventory_summary.py Mercedes-Benz --model GLA

For each model and model year: cars listed, median price, median mileage,
median Kelley Blue Book value and how many cars already have a purchase in
progress. Writes inventory_summary.csv.
"""

import argparse
from collections import defaultdict
from statistics import median

from quanticdata_carvana_scraper import CarvanaScraper, write


def med(values):
    values = [v for v in values if v is not None]
    return round(median(values)) if values else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("make", help='e.g. "Toyota"')
    parser.add_argument("--model", help="narrow to one model")
    parser.add_argument("--max-results", type=int, default=96, help="listings to read (max 96)")
    parser.add_argument("--out", default="inventory_summary.csv")
    args = parser.parse_args()

    carvana = CarvanaScraper()
    groups = defaultdict(list)
    for car in carvana.search(args.make, model=args.model, max_results=args.max_results):
        groups[(car.get("parent_model") or car.get("model"), car.get("year"))].append(car)

    summary = []
    for (model, year), cars in sorted(groups.items(), key=lambda g: (str(g[0][0]), g[0][1] or 0)):
        summary.append({
            "model": model,
            "year": year,
            "cars": len(cars),
            "median_price": med(c.get("price") for c in cars),
            "median_mileage": med(c.get("mileage") for c in cars),
            "median_kbb_value": med(c.get("kbb_value") for c in cars),
            "purchase_pending": sum(1 for c in cars if c.get("purchase_pending")),
        })
        s = summary[-1]
        print(f"{model} {year}: {s['cars']} cars, median ${s['median_price']:,} at {s['median_mileage']:,} mi"
              if s["median_price"] and s["median_mileage"] else f"{model} {year}: {s['cars']} cars")

    write(summary, args.out)
    print(f"{len(summary)} model/year groups written to {args.out}")


if __name__ == "__main__":
    main()
