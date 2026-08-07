"""
Generate a reproducible simulated SKIMS men's retail sales dataset.

Public product information is used for the product catalog.
All transaction-level sales records are simulated for educational
and portfolio purposes and do not represent SKIMS internal data.
"""

from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
import calendar
import csv
import random


RANDOM_SEED = 20250805
ANALYSIS_YEAR = 2025
ORDER_COUNT = 860

PRODUCTS = [
    {
        "product_id": "P001",
        "product_name": "Heavyweight Cotton Men's Cropped Muscle Tank",
        "product_category": "Tanks",
        "list_price_usd": 48.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X", "5X"],
        "available_colors": ["Atmosphere", "Chalk", "Buff", "Obsidian", "Washed Red"],
        "color_weights": [0.12, 0.26, 0.13, 0.34, 0.15],
        "source_url": "https://skims.com/products/heavyweight-cotton-mens-cropped-muscle-tank-atmosphere",
        "date_accessed": "2026-08-05",
    },
    {
        "product_id": "P002",
        "product_name": "SKIMS Cotton Men's Classic T-Shirt",
        "product_category": "T-Shirts",
        "list_price_usd": 44.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X"],
        "available_colors": ["Navy", "Light Heather Grey", "Stone", "Driftwood", "Chalk", "Onyx"],
        "color_weights": [0.18, 0.16, 0.12, 0.10, 0.20, 0.24],
        "source_url": "https://skims.com/products/skims-cotton-mens-classic-t-shirt-navy",
        "date_accessed": "2026-08-05",
    },
    {
        "product_id": "P003",
        "product_name": "Heavyweight Cotton Men's Relaxed Cropped Crewneck",
        "product_category": "Crewnecks",
        "list_price_usd": 54.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X", "5X"],
        "available_colors": ["Chalk", "Obsidian", "Atmosphere", "Raven"],
        "color_weights": [0.32, 0.35, 0.18, 0.15],
        "source_url": "https://skims.com/products/heavyweight-cotton-mens-relaxed-cropped-crewneck-chalk",
        "date_accessed": "2026-08-05",
    },
    {
        "product_id": "P004",
        "product_name": "Heavyweight Cotton Men's Relaxed Long Sleeve T-Shirt",
        "product_category": "Long Sleeve T-Shirts",
        "list_price_usd": 58.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X", "5X"],
        "available_colors": ["Chalk", "Raven", "Obsidian", "Damson", "Atmosphere"],
        "color_weights": [0.24, 0.18, 0.32, 0.10, 0.16],
        "source_url": "https://skims.com/products/heavyweight-cotton-mens-relaxed-long-sleeve-t-shirt-chalk",
        "date_accessed": "2026-08-05",
    },
    {
        "product_id": "P005",
        "product_name": "SKIMS Stretch Men's 3\" Boxer Brief",
        "product_category": "Boxer Briefs",
        "list_price_usd": 20.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X", "5X"],
        "available_colors": ["Obsidian", "Chalk", "Gunmetal", "Laurel", "Loden", "Oyster", "Currant"],
        "color_weights": [0.30, 0.18, 0.16, 0.10, 0.10, 0.09, 0.07],
        "source_url": "https://skims.com/products/skims-stretch-mens-3-inch-boxer-brief-obsidian",
        "date_accessed": "2026-08-05",
    },
    {
        "product_id": "P006",
        "product_name": "Woven Men's Pull-On Pant",
        "product_category": "Pants",
        "list_price_usd": 88.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X", "5X"],
        "available_colors": ["Jungle", "Pacific", "Ash", "Stone"],
        "color_weights": [0.24, 0.16, 0.27, 0.33],
        "source_url": "https://skims.com/products/woven-mens-pull-on-pant-jungle",
        "date_accessed": "2026-08-05",
    },
    {
        "product_id": "P007",
        "product_name": "Fleece Lounge Men's Classic Straight Leg Pant",
        "product_category": "Loungewear Pants",
        "list_price_usd": 98.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X", "5X"],
        "available_colors": ["Jungle", "Navy", "Shadow", "Washed Red", "Light Heather Grey", "Washed Onyx"],
        "color_weights": [0.18, 0.19, 0.22, 0.10, 0.17, 0.14],
        "source_url": "https://skims.com/products/fleece-lounge-mens-classic-straight-leg-pant-jungle",
        "date_accessed": "2026-08-05",
    },
    {
        "product_id": "P008",
        "product_name": "SKIMS Cotton Rib Men's Brief",
        "product_category": "Briefs",
        "list_price_usd": 22.00,
        "available_sizes": ["XS", "S", "M", "L", "XL", "2X", "3X", "4X", "5X"],
        "available_colors": ["Jungle", "Onyx", "Chalk", "Light Heather Grey"],
        "color_weights": [0.16, 0.36, 0.28, 0.20],
        "source_url": "https://skims.com/products/skims-cotton-rib-mens-brief-jungle",
        "date_accessed": "2026-08-05",
    },
]

MONTH_WEIGHTS = [0.070, 0.065, 0.072, 0.078, 0.082, 0.087,
                 0.090, 0.083, 0.077, 0.083, 0.102, 0.111]

BASE_PRODUCT_WEIGHTS = {
    "P001": 0.12,
    "P002": 0.20,
    "P003": 0.10,
    "P004": 0.10,
    "P005": 0.19,
    "P006": 0.08,
    "P007": 0.08,
    "P008": 0.13,
}

SEASONAL_MULTIPLIERS = {
    "winter": {"P001": 0.70, "P002": 0.95, "P003": 1.20, "P004": 1.20,
               "P005": 1.00, "P006": 0.90, "P007": 1.35, "P008": 1.00},
    "spring": {"P001": 1.15, "P002": 1.10, "P003": 0.90, "P004": 0.90,
               "P005": 1.05, "P006": 1.05, "P007": 0.80, "P008": 1.05},
    "summer": {"P001": 1.40, "P002": 1.20, "P003": 0.65, "P004": 0.65,
               "P005": 1.12, "P006": 1.15, "P007": 0.55, "P008": 1.12},
    "fall": {"P001": 0.85, "P002": 1.00, "P003": 1.15, "P004": 1.18,
             "P005": 1.00, "P006": 1.00, "P007": 1.20, "P008": 1.00},
}

SIZE_WEIGHTS = {
    "XS": 0.04,
    "S": 0.10,
    "M": 0.23,
    "L": 0.27,
    "XL": 0.20,
    "2X": 0.09,
    "3X": 0.04,
    "4X": 0.02,
    "5X": 0.01,
}


def get_season(month: int) -> str:
    if month in (12, 1, 2):
        return "winter"
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    return "fall"


def weighted_sample_without_replacement(items, weights, count, rng):
    """Select unique items while preserving weighted probabilities."""
    remaining_items = list(items)
    remaining_weights = list(weights)
    selections = []

    for _ in range(count):
        selected = rng.choices(remaining_items, weights=remaining_weights, k=1)[0]
        selected_index = remaining_items.index(selected)
        selections.append(selected)
        remaining_items.pop(selected_index)
        remaining_weights.pop(selected_index)

    return selections


def generate_transactions(seed: int = RANDOM_SEED):
    """
    Create exactly 1,200 line items across 860 orders.

    Order structure:
    - 560 orders with one line item
    - 260 orders with two line items
    - 40 orders with three line items
    """
    rng = random.Random(seed)
    product_lookup = {product["product_id"]: product for product in PRODUCTS}

    line_counts = ([1] * 560) + ([2] * 260) + ([3] * 40)
    rng.shuffle(line_counts)

    order_specs = []
    for line_count in line_counts:
        month = rng.choices(range(1, 13), weights=MONTH_WEIGHTS, k=1)[0]
        day = rng.randint(1, calendar.monthrange(ANALYSIS_YEAR, month)[1])
        order_specs.append((date(ANALYSIS_YEAR, month, day), line_count))

    # Chronological order IDs make the finished dataset easier to read.
    order_specs.sort(key=lambda item: item[0])

    transactions = []

    for order_index, (order_date, line_count) in enumerate(order_specs):
        order_id = f"O{1001 + order_index:04d}"
        season = get_season(order_date.month)

        product_ids = [product["product_id"] for product in PRODUCTS]
        product_weights = [
            BASE_PRODUCT_WEIGHTS[product_id]
            * SEASONAL_MULTIPLIERS[season][product_id]
            for product_id in product_ids
        ]

        selected_products = weighted_sample_without_replacement(
            product_ids,
            product_weights,
            line_count,
            rng,
        )

        for product_id in selected_products:
            product = product_lookup[product_id]

            selected_color = rng.choices(
                product["available_colors"],
                weights=product["color_weights"],
                k=1,
            )[0]

            available_size_weights = [
                SIZE_WEIGHTS[size] for size in product["available_sizes"]
            ]
            selected_size = rng.choices(
                product["available_sizes"],
                weights=available_size_weights,
                k=1,
            )[0]

            quantity = rng.choices(
                [1, 2, 3],
                weights=[0.86, 0.12, 0.02],
                k=1,
            )[0]

            transactions.append(
                {
                    "line_item_id": "",
                    "order_id": order_id,
                    "order_date": order_date.isoformat(),
                    "product_id": product_id,
                    "color": selected_color,
                    "size": selected_size,
                    "quantity": quantity,
                    "unit_price": product["list_price_usd"],
                }
            )

    for line_number, transaction in enumerate(transactions, start=1):
        transaction["line_item_id"] = f"L{line_number:04d}"

    return transactions


def validate_transactions(transactions):
    """Run portfolio-friendly data quality checks."""
    product_lookup = {product["product_id"]: product for product in PRODUCTS}
    required_columns = [
        "line_item_id",
        "order_id",
        "order_date",
        "product_id",
        "color",
        "size",
        "quantity",
        "unit_price",
    ]

    duplicate_full_rows = len(transactions) - len(
        {
            tuple(transaction[column] for column in required_columns)
            for transaction in transactions
        }
    )

    checks = {
        "transaction_line_items": len(transactions),
        "unique_orders": len({row["order_id"] for row in transactions}),
        "unique_line_item_ids": len({row["line_item_id"] for row in transactions}),
        "missing_required_values": sum(
            1
            for row in transactions
            for column in required_columns
            if row[column] in ("", None)
        ),
        "invalid_product_ids": sum(
            1 for row in transactions if row["product_id"] not in product_lookup
        ),
        "dates_outside_2025": sum(
            1 for row in transactions if not row["order_date"].startswith("2025-")
        ),
        "invalid_quantities": sum(
            1 for row in transactions if row["quantity"] not in (1, 2, 3)
        ),
        "invalid_sizes": sum(
            1
            for row in transactions
            if row["size"] not in product_lookup[row["product_id"]]["available_sizes"]
        ),
        "invalid_colors": sum(
            1
            for row in transactions
            if row["color"] not in product_lookup[row["product_id"]]["available_colors"]
        ),
        "price_mismatches": sum(
            1
            for row in transactions
            if row["unit_price"] != product_lookup[row["product_id"]]["list_price_usd"]
        ),
        "duplicate_full_rows": duplicate_full_rows,
    }

    return checks


def export_csv_files(output_dir: Path, transactions, quality_checks):
    output_dir.mkdir(parents=True, exist_ok=True)

    product_path = output_dir / "skims_product_catalog.csv"
    transaction_path = output_dir / "skims_sales_transactions_simulated.csv"
    quality_path = output_dir / "skims_data_quality_summary.csv"

    product_headers = [
        "product_id",
        "product_name",
        "product_category",
        "list_price_usd",
        "available_sizes",
        "available_colors",
        "source_url",
        "date_accessed",
    ]

    with product_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=product_headers)
        writer.writeheader()
        for product in PRODUCTS:
            writer.writerow(
                {
                    "product_id": product["product_id"],
                    "product_name": product["product_name"],
                    "product_category": product["product_category"],
                    "list_price_usd": f'{product["list_price_usd"]:.2f}',
                    "available_sizes": ", ".join(product["available_sizes"]),
                    "available_colors": ", ".join(product["available_colors"]),
                    "source_url": product["source_url"],
                    "date_accessed": product["date_accessed"],
                }
            )

    transaction_headers = [
        "line_item_id",
        "order_id",
        "order_date",
        "product_id",
        "color",
        "size",
        "quantity",
        "unit_price",
    ]

    with transaction_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=transaction_headers)
        writer.writeheader()
        writer.writerows(transactions)

    with quality_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["quality_metric", "result"])
        for metric, value in quality_checks.items():
            writer.writerow([metric, value])

    return product_path, transaction_path, quality_path


def main(output_dir="."):
    output_dir = Path(output_dir)
    transactions = generate_transactions()
    quality_checks = validate_transactions(transactions)
    paths = export_csv_files(output_dir, transactions, quality_checks)

    total_units = sum(row["quantity"] for row in transactions)
    total_revenue = sum(
        row["quantity"] * row["unit_price"] for row in transactions
    )

    print("SKIMS simulated sales dataset generated successfully.")
    print(f"Random seed: {RANDOM_SEED}")
    print(f"Transaction line items: {len(transactions):,}")
    print(f"Unique orders: {quality_checks['unique_orders']:,}")
    print(f"Total simulated units: {total_units:,}")
    print(f"Total simulated revenue: ${total_revenue:,.2f}")
    print("Quality checks:", quality_checks)

    return transactions, quality_checks, paths


if __name__ == "__main__":
    main(Path(__file__).resolve().parent)
