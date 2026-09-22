"""Reviewable preprocessing pipeline reconstructed from the recovered Olist notebook.

The original notebook merged order-level payments directly and could expand rows
when an order had multiple payment records. This refactor aggregates payment
value at order level before merging so order/item analysis remains interpretable.

Raw Olist CSV files are intentionally not included.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd


DATA_FILES = {
    "customers": "olist_customers_dataset.csv",
    "items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}


def load_tables(data_dir: str | Path = "data") -> dict[str, pd.DataFrame]:
    data_dir = Path(data_dir)
    tables = {}
    for name, file_name in DATA_FILES.items():
        kwargs = {"low_memory": False}
        if name == "reviews":
            kwargs["encoding"] = "ISO-8859-1"
        tables[name] = pd.read_csv(data_dir / file_name, **kwargs)
    return tables


def clean_source_tables(tables: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    data = {name: df.copy() for name, df in tables.items()}

    data["customers"].drop(
        columns=["customer_zip_code_prefix"],
        errors="ignore",
        inplace=True,
    )
    data["payments"].drop(
        columns=["payment_sequential", "payment_type", "payment_installments"],
        errors="ignore",
        inplace=True,
    )
    data["reviews"].drop(
        columns=["review_id", "review_comment_title", "review_creation_date"],
        errors="ignore",
        inplace=True,
    )
    data["orders"].drop(columns=["order_approved_at"], errors="ignore", inplace=True)
    data["products"].drop(
        columns=[
            "product_name_lenght",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
        errors="ignore",
        inplace=True,
    )

    data["products"] = data["products"].dropna(subset=["product_category_name"])
    data["reviews"]["review_comment_message"] = (
        data["reviews"]["review_comment_message"].fillna("")
    )

    return data


def build_analysis_table(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    data = clean_source_tables(tables)

    # Prevent payment rows from multiplying order-item rows.
    payment_by_order = (
        data["payments"]
        .groupby("order_id", as_index=False)["payment_value"]
        .sum()
    )

    merged = (
        data["items"]
        .merge(data["orders"], on="order_id", how="left")
        .merge(data["customers"], on="customer_id", how="left")
        .merge(data["reviews"], on="order_id", how="left")
        .merge(payment_by_order, on="order_id", how="left")
        .merge(data["products"], on="product_id", how="left")
        .merge(
            data["sellers"],
            on="seller_id",
            how="left",
            suffixes=("", "_seller"),
        )
    )

    merged = merged.dropna(subset=["review_score", "product_category_name"])

    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    for col in date_columns:
        if col in merged.columns:
            merged[col] = pd.to_datetime(merged[col], errors="coerce")

    merged["delivery_days"] = (
        merged["order_delivered_customer_date"]
        - merged["order_purchase_timestamp"]
    ).dt.days

    merged["delivery_vs_estimate_days"] = (
        merged["order_delivered_customer_date"]
        - merged["order_estimated_delivery_date"]
    ).dt.days

    return merged


if __name__ == "__main__":
    tables = load_tables()
    analysis_df = build_analysis_table(tables)
    print(analysis_df.shape)
    print(analysis_df.head())
