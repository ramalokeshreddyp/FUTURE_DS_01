"""
Generate a realistic Superstore-style Business Sales Dataset (2021-2024)
~5,000 rows covering products, categories, sub-categories, regions, and more.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

random.seed(42)
np.random.seed(42)

# ── Configuration ─────────────────────────────────────────────────────────────
START_DATE = datetime(2021, 1, 1)
END_DATE   = datetime(2024, 12, 31)
N_ORDERS   = 5000

REGIONS     = ["East", "West", "South", "Central"]
REGION_BIAS = [0.30, 0.28, 0.22, 0.20]          # relative order frequency

CATEGORIES = {
    "Technology": {
        "Electronics":    ["Laptop", "Tablet", "Monitor", "Wireless Mouse", "USB-C Hub",
                           "Keyboard", "Webcam", "Headphones", "Smart Speaker", "SSD Drive"],
        "Phones":         ["Smartphone Pro", "Smartphone Lite", "Feature Phone",
                           "Bluetooth Earbuds", "Phone Case"],
        "Accessories":    ["Charging Pad", "Power Bank", "Screen Protector",
                           "Laptop Stand", "Cable Organizer"],
    },
    "Furniture": {
        "Office Chairs":  ["Ergonomic Chair", "Executive Chair", "Mesh Chair",
                           "Stool", "Gaming Chair"],
        "Desks":          ["Standing Desk", "Corner Desk", "Writing Desk",
                           "Foldable Desk", "L-Shaped Desk"],
        "Storage":        ["Bookshelf", "Filing Cabinet", "Drawer Unit",
                           "Storage Box", "Display Rack"],
    },
    "Office Supplies": {
        "Stationery":     ["Pen Set", "Notebook", "Sticky Notes", "Highlighter Pack",
                           "Stapler", "Paper Clips", "Binder"],
        "Paper":          ["A4 Paper Ream", "Cardstock", "Labels Sheet",
                           "Envelope Pack", "Poster Paper"],
        "Binders":        ["Ring Binder", "Lever Arch File", "Document Wallet",
                           "Presentation Folder", "Clear Sleeve"],
    },
}

# price ranges per sub-category (min, max in USD)
PRICE_RANGES = {
    "Electronics":   (80, 1800),
    "Phones":        (30, 1200),
    "Accessories":   (10, 120),
    "Office Chairs": (150, 900),
    "Desks":         (200, 1200),
    "Storage":       (40, 350),
    "Stationery":    (3, 40),
    "Paper":         (5, 60),
    "Binders":       (4, 35),
}

DISCOUNT_RATES = [0.0, 0.0, 0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30]

CUSTOMER_SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_BIAS      = [0.52, 0.30, 0.18]

STATES = {
    "East":    ["New York", "Pennsylvania", "New Jersey", "Massachusetts", "Connecticut",
                "Virginia", "Maryland", "Ohio", "Michigan"],
    "West":    ["California", "Washington", "Oregon", "Nevada", "Arizona",
                "Colorado", "Utah", "Idaho"],
    "South":   ["Texas", "Florida", "Georgia", "North Carolina", "Louisiana",
                "Tennessee", "Alabama", "South Carolina"],
    "Central": ["Illinois", "Minnesota", "Missouri", "Wisconsin", "Indiana",
                "Kansas", "Arkansas", "Iowa"],
}

SHIP_MODES      = ["Standard Class", "Second Class", "First Class", "Same Day"]
SHIP_MODE_BIAS  = [0.60, 0.20, 0.15, 0.05]

# ── Helper ────────────────────────────────────────────────────────────────────
def random_date(start: datetime, end: datetime) -> datetime:
    delta = (end - start).days
    # add seasonal bias – Q4 gets ~40 % more orders
    month = random.randint(1, 12)
    day   = random.randint(1, 28)
    year  = random.choices([2021, 2022, 2023, 2024], weights=[0.20, 0.24, 0.26, 0.30])[0]
    month_weights = [1,1,1,1,1,1,1,1,1.2,1.3,1.5,1.6]
    month = random.choices(range(1,13), weights=month_weights)[0]
    return datetime(year, month, day)

# ── Generate Orders ────────────────────────────────────────────────────────────
rows = []
order_id_counter = 10000

for i in range(N_ORDERS):
    region   = random.choices(REGIONS, weights=REGION_BIAS)[0]
    state    = random.choice(STATES[region])
    category = random.choices(list(CATEGORIES.keys()), weights=[0.35, 0.30, 0.35])[0]
    sub_cat  = random.choice(list(CATEGORIES[category].keys()))
    product  = random.choice(CATEGORIES[category][sub_cat])
    segment  = random.choices(CUSTOMER_SEGMENTS, weights=SEGMENT_BIAS)[0]
    ship     = random.choices(SHIP_MODES, weights=SHIP_MODE_BIAS)[0]

    order_date = random_date(START_DATE, END_DATE)
    ship_days  = {"Standard Class": 5, "Second Class": 3, "First Class": 2, "Same Day": 0}[ship]
    ship_date  = order_date + timedelta(days=ship_days + random.randint(0, 2))

    low, high = PRICE_RANGES[sub_cat]
    unit_price = round(random.uniform(low, high), 2)
    quantity   = random.choices([1,2,3,4,5,6], weights=[0.45,0.25,0.15,0.08,0.05,0.02])[0]
    discount   = random.choice(DISCOUNT_RATES)

    sales   = round(unit_price * quantity * (1 - discount), 2)
    # profit margin varies by category
    margin_ranges = {"Technology": (0.12, 0.28), "Furniture": (0.05, 0.20), "Office Supplies": (0.15, 0.35)}
    lo_m, hi_m = margin_ranges[category]
    profit  = round(sales * random.uniform(lo_m, hi_m) * (1 - discount * 0.5), 2)

    customer_id = f"CUST-{random.randint(1000,9999)}"

    order_id_counter += random.randint(1, 5)
    rows.append({
        "Order_ID":       f"ORD-{order_id_counter}",
        "Order_Date":     order_date.strftime("%Y-%m-%d"),
        "Ship_Date":      ship_date.strftime("%Y-%m-%d"),
        "Ship_Mode":      ship,
        "Customer_ID":    customer_id,
        "Segment":        segment,
        "Region":         region,
        "State":          state,
        "Category":       category,
        "Sub_Category":   sub_cat,
        "Product_Name":   product,
        "Unit_Price":     unit_price,
        "Quantity":       quantity,
        "Discount":       discount,
        "Sales":          sales,
        "Profit":         profit,
    })

df = pd.DataFrame(rows)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Ship_Date"]  = pd.to_datetime(df["Ship_Date"])

# ── Save ───────────────────────────────────────────────────────────────────────
out_path = r"C:\Users\lokes\Desktop\DS1\data\superstore_sales.csv"
df.to_csv(out_path, index=False)
print(f"✅ Dataset saved to {out_path}")
print(f"   Rows: {len(df):,}  |  Columns: {df.columns.tolist()}")
print(df.head(3))
