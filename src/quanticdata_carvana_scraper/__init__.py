"""Carvana Scraper API: Carvana scraper for Python and the command line: used-car inventory by make and model with price, previous price, MSRP, Kelley Blue Book value, mileage, VIN, trim, colours and stock number, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_carvana_scraper import CarvanaScraper

    scraper = CarvanaScraper()   # saved login (`carvana-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # Carvana used-car listings for a make and model
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["CarvanaScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class CarvanaScraper:
    """Carvana Scraper API on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="carvana-scraper/0.1.0 (+https://github.com/quantumproxies/carvana-scraper)", timeout=timeout)

    def search(
        self, make: Optional[str] = None,
        *,
        model: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Carvana used-car inventory — year/make/model/trim, price, MSRP, mileage, VIN and stock number.

        Args:
            make: Vehicle make, e.g. "Toyota" or "Mercedes-Benz". Omit to browse all inventory.
            model: Vehicle model (requires make), e.g. "Camry".
            max_results: How many listings to deliver at most (1–96). You pay only for delivered listings.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 96 rows, one per listing: see ``types.CarvanaCarsRow``.
        """
        payload = {
            "make": make,
            "model": model,
            "max_results": max_results,
        }
        return self.client.run_collector("carvana_cars", payload, wait=wait, timeout=timeout)
