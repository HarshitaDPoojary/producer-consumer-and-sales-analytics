"""
Main entry point for Sales Analytics Application.
Supports both batch and interactive modes.
"""

import sys
import os

from interactive import run_interactive_mode
from analyzers import (
    revenue_by_category, profit_by_region, top_customers_by_revenue,
    revenue_trend_by_period, product_performance, profit_margin_by_subcategory,
    category_preference_by_region, avg_order_value
)
from output import format_console_output


DEFAULT_CSV = 'data/product_sales_dataset_final.csv'


def run_batch_mode(filepath: str):
    """
    Run all analyses and print to console (non-interactive).

    Args:
        filepath: Path to CSV file
    """
    print("=" * 60)
    print("SALES ANALYTICS - BATCH MODE")
    print("=" * 60)
    print(f"Dataset: {filepath}")
    print("=" * 60)

    analyses = [
        ("Revenue by Category", lambda: revenue_by_category(filepath), 'dict'),
        ("Profit by Region", lambda: profit_by_region(filepath), 'dict'),
        ("Top 10 Customers", lambda: top_customers_by_revenue(filepath, 10), 'list'),
        ("Revenue Trends (Monthly)", lambda: revenue_trend_by_period(filepath, 'monthly'), 'trend'),
        ("Top Products by Quantity", lambda: product_performance(filepath, top_n=10), 'list'),
        ("Profit Margin by Sub-Category", lambda: profit_margin_by_subcategory(filepath), 'dict'),
        ("Category Preferences by Region", lambda: category_preference_by_region(filepath), 'dict'),
        ("Average Order Value", lambda: avg_order_value(filepath), 'dict'),
    ]

    for title, analysis_fn, data_type in analyses:
        try:
            print(f"\nExecuting: {title}...")
            results = analysis_fn()
            format_console_output(results, title, data_type)
        except Exception as e:
            print(f"Error in {title}: {e}")

    print("\n" + "=" * 60)
    print("BATCH MODE COMPLETE")
    print("=" * 60)


def main():
    """
    Entry point with mode selection.
    """
    # Determine filepath
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = DEFAULT_CSV

    # Check if file exists
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        print(f"Please provide CSV file path or ensure {DEFAULT_CSV} exists.")
        sys.exit(1)

    print("=" * 60)
    print("SALES ANALYTICS APPLICATION")
    print("=" * 60)
    print("\nSelect mode:")
    print("1. Interactive Mode (dynamic filtering, visualizations)")
    print("2. Batch Mode (run all analyses)")

    mode = input("\nChoice (default: 1): ").strip()

    if mode == '2':
        run_batch_mode(filepath)
    else:
        run_interactive_mode(filepath)


if __name__ == "__main__":
    main()
