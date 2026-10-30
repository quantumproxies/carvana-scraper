"""Carvana cars priced under their Kelley Blue Book value, biggest gap first.

    python under_kbb.py Toyota --model Camry
    python under_kbb.py Honda --max-mileage 60000 --out honda_under_kbb.csv

Reads the listings of one make (and model), keeps the cars whose Carvana
price is below the Kelley Blue Book value Carvana shows, and writes them to
under_kbb.csv with the gap in dollars and in percent.
"""

import argparse

from quanticdata_carvana_scraper import CarvanaScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("make", help='e.g. "Toyota", "Mercedes-Benz"')
    parser.add_argument("--model", help='e.g. "Camry"')
    parser.add_argument("--max-mileage", type=int, help="skip cars above this many miles")
    parser.add_argument("--max-results", type=int, default=96, help="listings to read (max 96)")
    parser.add_argument("--out", default="under_kbb.csv")
    args = parser.parse_args()

    carvana = CarvanaScraper()
    rows = []
    for car in carvana.search(args.make, model=args.model, max_results=args.max_results):
        price, kbb = car.get("price"), car.get("kbb_value")
        if not price or not kbb or price >= kbb:
            continue
        if args.max_mileage is not None and (car.get("mileage") or 0) > args.max_mileage:
            continue
        rows.append({
            "gap_usd": round(kbb - price),
            "gap_percent": round(100 * (kbb - price) / kbb, 1),
            "year": car.get("year"), "make": car.get("make"), "model": car.get("model"), "trim": car.get("trim"),
            "mileage": car.get("mileage"), "price": price, "kbb_value": kbb, "vin": car.get("vin"),
            "url": car.get("url"),
        })

    rows.sort(key=lambda r: r["gap_usd"], reverse=True)
    for r in rows[:15]:
        print(f"${r['gap_usd']:>6,} under KBB  {r['year']} {r['model']} {r['trim'] or ''}  "
              f"{r['mileage'] or 0:,} mi  ${r['price']:,}")
    write(rows, args.out)
    print(f"{len(rows)} cars written to {args.out}")


if __name__ == "__main__":
    main()
