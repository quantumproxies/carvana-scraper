"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class CarvanaCarsRow(TypedDict, total=False):
    """One row of `carvana-scraper search` (carvana_cars v1.1.2)."""

    rank: int
    """1-based position."""
    vehicle_id: Optional[str]
    """Carvana vehicle id — the key in the listing URL."""
    stock_number: Optional[str]
    """Carvana stock number."""
    vin: Optional[str]
    """VIN."""
    year: Optional[int]
    """Model year."""
    make: Optional[str]
    """Make."""
    model: Optional[str]
    """Model, including the variant ("Camry Hybrid")."""
    parent_model: Optional[str]
    """Model family ("Camry" for a Camry Hybrid)."""
    trim: Optional[str]
    """Trim, e.g. "SEL"."""
    kbb_trim: Optional[str]
    """Kelley Blue Book long trim, e.g. "SEL Sport Utility 4D"."""
    condition: Optional[str]
    """Offering as Carvana states it ("Used")."""
    price: Optional[float]
    """Carvana price in USD."""
    msrp: Optional[float]
    """Original MSRP in USD."""
    previous_price: Optional[float]
    """Price before the last change; null when never repriced."""
    mileage: Optional[int]
    """Odometer miles."""
    body_style: Optional[str]
    """Body style, e.g. "Suv"."""
    fuel_type: Optional[str]
    """Fuel type, e.g. "Gas"."""
    exterior_color: Optional[str]
    """Exterior colour."""
    interior_color: Optional[str]
    """Interior colour."""
    mpg: Optional[int]
    """Miles per gallon."""
    seating_capacity: Optional[int]
    """Seats."""
    image: Optional[str]
    """Primary photo."""
    url: Optional[str]
    """Listing URL."""
    kbb_value: Optional[float]
    """Kelley Blue Book value Carvana shows for the car."""
    market_adjustment: Optional[float]
    """Difference between price and MSRP reference (negative = below)."""
    shipping_cost: Optional[float]
    """Transport cost included in the offer (0 when free)."""
    discount_amount: Optional[float]
    """Total discount applied."""
    tags: List[str]
    """Listing tags ("Recently Added", "Great Deal"…)."""
    purchase_pending: bool
    """True when another buyer has a purchase in progress."""
    purchase_type: Optional[str]
    """Purchase status (Purchasable…)."""
    image_hero: Optional[str]
    """Standardized hero image URL."""
