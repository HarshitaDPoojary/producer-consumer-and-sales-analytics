"""
Interactive CLI menu system with dynamic filtering.
Demonstrates partial application and map-based dispatch.
"""

from functools import partial
from typing import Optional

from analyzers import (
    revenue_by_category, profit_by_region, top_customers_by_revenue,
    revenue_trend_by_period, product_performance, profit_margin_by_subcategory,
    category_preference_by_region, avg_order_value
)
from output import display_results


MENU_OPTIONS = {
    '1': 'Revenue by Category',
    '2': 'Profit by Region',
    '3': 'Top Customers by Revenue',
    '4': 'Revenue Trends Over Time',
    '5': 'Product Performance',
    '6': 'Profit Margin by Sub-Category',
    '7': 'Category Preferences by Region',
    '8': 'Average Order Value Analysis',
    '0': 'Exit'
}


def display_menu():
    """Display main menu"""
    print("\n" + "=" * 60)
    print("SALES ANALYTICS - INTERACTIVE DASHBOARD")
    print("=" * 60)
    for key, value in MENU_OPTIONS.items():
        print(f"{key}. {value}")
    print("=" * 60)


def get_filters():
    """
    Interactive filter selection.

    Returns:
        Dictionary of filter parameters
    """
    print("\nApply filters (press Enter to skip):")
    category_input = input("  Category (Electronics/Clothing & Apparel/Accessories/Home & Furniture): ").strip()
    region_input = input("  Region (East/West/South/Centre): ").strip()
    period_input = input("  Period (monthly/quarterly/yearly): ").strip()

    return {
        'category': category_input if category_input else None,
        'region': region_input if region_input else None,
        'period': period_input if period_input else 'monthly'
    }


def execute_analysis(choice: str, filepath: str):
    """
    Execute selected analysis with user filters.

    FP Principle: Partial Application + Map-based Dispatch
    - Uses partial to bind parameters
    - Map structure avoids if/else chains

    Args:
        choice: User's menu choice
        filepath: Path to CSV file
    """
    filters = get_filters()

    # Map choice to analysis function with partial application
    # This demonstrates functional composition
    analysis_map = {
        '1': lambda: revenue_by_category(filepath, filters['category']),
        '2': lambda: profit_by_region(filepath, filters['region']),
        '3': lambda: top_customers_by_revenue(filepath, n=10, category=filters['category']),
        '4': lambda: revenue_trend_by_period(filepath, filters['period'], filters['category']),
        '5': lambda: product_performance(filepath, filters['region'], top_n=10),
        '6': lambda: profit_margin_by_subcategory(filepath, filters['category']),
        '7': lambda: category_preference_by_region(filepath),
        '8': lambda: avg_order_value(filepath, filters['category'], filters['region'])
    }

    if choice not in analysis_map:
        print("Invalid option!")
        return

    # Execute analysis
    print("\nProcessing...")
    try:
        results = analysis_map[choice]()

        # Determine output type and plot type
        title = MENU_OPTIONS[choice]

        if choice in ['3', '5']:
            # Rankings (list of tuples)
            display_results(results, title)
        elif choice == '4':
            # Time series
            display_results(results, title, plot_type='line')
        else:
            # Regular aggregations
            display_results(results, title)

        # Ask if user wants visualization
        if choice not in ['4']:  # Skip if already plotted
            vis_choice = input("\nGenerate visualization? (bar/pie/n): ").strip().lower()
            if vis_choice in ['bar', 'pie']:
                display_results(results, title, plot_type=vis_choice)

    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()


def run_interactive_mode(filepath: str):
    """
    Main interactive loop.

    Args:
        filepath: Path to CSV file
    """
    print("\nWelcome to Sales Analytics!")
    print(f"Dataset: {filepath}")

    while True:
        display_menu()
        choice = input("\nSelect option: ").strip()

        if choice == '0':
            print("\nExiting... Thank you!")
            break
        elif choice in MENU_OPTIONS:
            execute_analysis(choice, filepath)
        else:
            print("Invalid option! Please try again.")
