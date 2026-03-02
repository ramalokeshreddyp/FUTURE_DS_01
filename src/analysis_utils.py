from __future__ import annotations

from pathlib import Path
import pandas as pd


def load_sales_data(path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])

    numeric_cols = [
        "quantity",
        "unit_price",
        "revenue",
        "profit",
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if "is_return" in df.columns:
        df["is_return"] = df["is_return"].astype(str).str.lower().isin(["true", "1"])
    else:
        df["is_return"] = False

    df = df.dropna(subset=["order_id", "order_date", "product_name", "category", "region", "revenue", "profit"])
    return df


def build_kpis(df: pd.DataFrame) -> dict[str, float]:
    total_revenue = float(df["revenue"].sum())
    total_profit = float(df["profit"].sum())
    total_orders = int(df["order_id"].nunique())
    avg_order_value = total_revenue / total_orders if total_orders else 0.0
    profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0.0
    return_rate = (float(df["is_return"].mean()) * 100) if len(df) else 0.0

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "profit_margin_pct": profit_margin,
        "return_rate_pct": return_rate,
    }


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.assign(month_start=df["order_date"].dt.to_period("M").dt.to_timestamp())
        .groupby("month_start", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
        .sort_values("month_start")
    )
    return out


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return (
        df.groupby(["product_name", "category"], as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("quantity", "sum"))
        .sort_values("revenue", ascending=False)
        .head(n)
    )


def category_performance(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category", as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), units=("quantity", "sum"))
        .sort_values("revenue", ascending=False)
    )


def regional_performance(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["country", "region"], as_index=False)
        .agg(revenue=("revenue", "sum"), profit=("profit", "sum"), orders=("order_id", "nunique"))
        .sort_values("revenue", ascending=False)
    )
