from __future__ import annotations

from pathlib import Path
import pandas as pd


COUNTRY_REGION_MAP = {
    "United Kingdom": "Europe",
    "EIRE": "Europe",
    "France": "Europe",
    "Germany": "Europe",
    "Spain": "Europe",
    "Netherlands": "Europe",
    "Belgium": "Europe",
    "Switzerland": "Europe",
    "Portugal": "Europe",
    "Italy": "Europe",
    "Norway": "Europe",
    "Sweden": "Europe",
    "Denmark": "Europe",
    "Finland": "Europe",
    "Poland": "Europe",
    "Austria": "Europe",
    "Iceland": "Europe",
    "Cyprus": "Europe",
    "Greece": "Europe",
    "USA": "North America",
    "Canada": "North America",
    "Australia": "APAC",
    "Japan": "APAC",
    "Singapore": "APAC",
    "Hong Kong": "APAC",
    "Israel": "Middle East",
    "United Arab Emirates": "Middle East",
}


def infer_category(description: str) -> str:
    text = str(description).upper()
    if any(keyword in text for keyword in ["BAG", "BOX", "CASE", "BOTTLE", "BOWL", "MUG", "JAR", "CUP"]):
        return "Kitchen & Storage"
    if any(keyword in text for keyword in ["LIGHT", "LANTERN", "CANDLE", "HOLDER", "LAMPS", "LAMP"]):
        return "Lighting & Decor"
    if any(keyword in text for keyword in ["CHRISTMAS", "PARTY", "GIFT", "RIBBON", "CARD", "WRAP"]):
        return "Seasonal & Gifts"
    if any(keyword in text for keyword in ["TOY", "GAME", "JIGSAW", "DOLL", "SKITTLES", "BALLOON"]):
        return "Toys & Kids"
    if any(keyword in text for keyword in ["DOORMAT", "CUSHION", "CLOCK", "FRAME", "HEART", "HOOK", "SIGN"]):
        return "Home Furnishing"
    return "General Merchandise"


def preprocess_data(input_path: Path, output_path: Path) -> pd.DataFrame:
    df = pd.read_csv(input_path, encoding="latin1")

    df = df.rename(
        columns={
            "InvoiceNo": "order_id",
            "StockCode": "stock_code",
            "Description": "product_name",
            "Quantity": "quantity",
            "InvoiceDate": "order_date",
            "UnitPrice": "unit_price",
            "CustomerID": "customer_id",
            "Country": "country",
        }
    )

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["country"] = df["country"].astype(str).str.strip()
    df["is_return"] = df["order_id"].astype(str).str.startswith("C") | (pd.to_numeric(df["quantity"], errors="coerce") < 0)

    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["order_id", "order_date", "product_name", "quantity", "unit_price", "country"])
    df = df[(df["unit_price"] > 0) & (df["product_name"] != "")]

    df["revenue"] = df["quantity"] * df["unit_price"]
    df["category"] = df["product_name"].apply(infer_category)
    df["region"] = df["country"].map(COUNTRY_REGION_MAP).fillna("Other")

    margin_map = {
        "Kitchen & Storage": 0.32,
        "Lighting & Decor": 0.35,
        "Seasonal & Gifts": 0.30,
        "Toys & Kids": 0.28,
        "Home Furnishing": 0.33,
        "General Merchandise": 0.26,
    }
    df["estimated_margin_pct"] = df["category"].map(margin_map).fillna(0.28)
    df["profit"] = df["revenue"] * df["estimated_margin_pct"]

    curated = df[
        [
            "order_id",
            "order_date",
            "country",
            "region",
            "customer_id",
            "stock_code",
            "product_name",
            "category",
            "quantity",
            "unit_price",
            "revenue",
            "profit",
            "is_return",
        ]
    ].sort_values("order_date")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    curated.to_csv(output_path, index=False)
    return curated


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / "data" / "raw" / "online_retail.csv"
    output_path = project_root / "data" / "processed" / "business_sales_curated.csv"

    curated = preprocess_data(input_path=input_path, output_path=output_path)
    print(f"Saved {len(curated):,} cleaned rows to {output_path}")


if __name__ == "__main__":
    main()