from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import random

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class ProductSpec:
    name: str
    category: str
    unit_price: float
    cost_ratio: float


def generate_sales_data(seed: int = 42, n_orders: int = 5000) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)

    products = [
        ProductSpec("Laptop Pro 14", "Electronics", 1200, 0.68),
        ProductSpec("Wireless Mouse", "Electronics", 45, 0.42),
        ProductSpec("Noise-Cancel Headphones", "Electronics", 180, 0.55),
        ProductSpec("Office Chair", "Furniture", 260, 0.60),
        ProductSpec("Standing Desk", "Furniture", 420, 0.63),
        ProductSpec("Notebook Set", "Office Supplies", 18, 0.35),
        ProductSpec("Printer Paper Box", "Office Supplies", 32, 0.58),
        ProductSpec("Water Bottle", "Lifestyle", 24, 0.40),
        ProductSpec("Fitness Band", "Lifestyle", 95, 0.52),
        ProductSpec("Coffee Machine", "Appliances", 210, 0.57),
        ProductSpec("Air Purifier", "Appliances", 330, 0.62),
        ProductSpec("Blender", "Appliances", 120, 0.54),
    ]

    regions = ["North", "South", "East", "West", "Central"]
    segments = ["Consumer", "Corporate", "Home Office"]
    channels = ["Online", "Retail", "Distributor"]
    countries = ["India", "UAE", "Singapore"]

    date_range = pd.date_range("2024-01-01", "2025-12-31", freq="D")

    rows = []
    for i in range(1, n_orders + 1):
        product = random.choice(products)

        date = random.choice(date_range)

        month_seasonality = 1.0
        if date.month in [10, 11, 12]:
            month_seasonality = 1.22
        elif date.month in [6, 7]:
            month_seasonality = 0.92

        region = random.choices(regions, weights=[0.22, 0.18, 0.20, 0.24, 0.16])[0]
        segment = random.choices(segments, weights=[0.50, 0.33, 0.17])[0]
        channel = random.choices(channels, weights=[0.58, 0.27, 0.15])[0]
        country = random.choices(countries, weights=[0.62, 0.22, 0.16])[0]

        quantity = max(1, int(np.random.poisson(3) + 1))

        base_discount = np.clip(np.random.normal(0.08, 0.05), 0, 0.35)
        if segment == "Corporate":
            base_discount = min(base_discount + 0.03, 0.40)

        gross_sales = product.unit_price * quantity * month_seasonality
        discount_amount = gross_sales * base_discount
        net_sales = gross_sales - discount_amount

        shipping_cost = max(4, np.random.normal(12, 4)) * (1 + quantity / 10)
        cogs = net_sales * product.cost_ratio
        profit = net_sales - cogs - shipping_cost

        rows.append(
            {
                "order_id": f"ORD-{100000 + i}",
                "order_date": pd.Timestamp(date),
                "year": int(date.year),
                "month": int(date.month),
                "month_name": date.strftime("%b"),
                "quarter": f"Q{((date.month - 1) // 3) + 1}",
                "country": country,
                "region": region,
                "segment": segment,
                "channel": channel,
                "product_name": product.name,
                "category": product.category,
                "quantity": quantity,
                "unit_price": round(product.unit_price, 2),
                "discount_pct": round(base_discount, 4),
                "gross_sales": round(gross_sales, 2),
                "discount_amount": round(discount_amount, 2),
                "net_sales": round(net_sales, 2),
                "shipping_cost": round(shipping_cost, 2),
                "cogs": round(cogs, 2),
                "profit": round(profit, 2),
            }
        )

    df = pd.DataFrame(rows).sort_values("order_date").reset_index(drop=True)
    return df


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "data"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = generate_sales_data(seed=42, n_orders=5000)
    output_path = output_dir / "business_sales_data.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved {len(df):,} rows to {output_path}")


if __name__ == "__main__":
    main()
