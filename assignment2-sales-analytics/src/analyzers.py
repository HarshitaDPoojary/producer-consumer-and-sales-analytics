"""
Sales analysis methods composing functional modules.
Each analysis demonstrates different functional programming patterns.
"""

from typing import Optional
from parsers import parse_csv_stream
from filters import filter_by_category, filter_by_region, filter_by_period
from aggregators import sum_by_group, avg_by_group, top_n_by_metric, group_by_field, multi_level_grouping, find_max_by_group
from models import extract_period


def revenue_by_category(filepath: str, category: Optional[str] = None) -> dict[str, float]:
    """
    Analysis 1: Total revenue by product category.

    FP Pattern: filter + groupby + sum

    Args:
        filepath: Path to CSV file
        category: Optional category filter

    Returns:
        Dictionary {category: total_revenue}
    """
    records = parse_csv_stream(filepath)

    # Apply optional filter
    if category:
        records = filter_by_category(records, category)

    # Group by category and sum revenue
    return sum_by_group(records, 'category', 'revenue')


def profit_by_region(filepath: str, region: Optional[str] = None) -> dict[str, float]:
    """
    Analysis 2: Total profit by geographic region.

    FP Pattern: filter + groupby + sum

    Args:
        filepath: Path to CSV file
        region: Optional region filter

    Returns:
        Dictionary {region: total_profit}
    """
    records = parse_csv_stream(filepath)

    if region:
        records = filter_by_region(records, region)

    return sum_by_group(records, 'region', 'profit')


def top_customers_by_revenue(filepath: str, n: int = 10, category: Optional[str] = None) -> list[tuple[str, float]]:
    """
    Analysis 3: Top N customers by total revenue.

    FP Pattern: filter + groupby + sort + limit

    Args:
        filepath: Path to CSV file
        n: Number of top customers
        category: Optional category filter

    Returns:
        List of (customer_name, revenue) tuples, sorted descending
    """
    records = parse_csv_stream(filepath)

    if category:
        records = filter_by_category(records, category)

    return top_n_by_metric(records, 'customer_name', 'revenue', n)


def revenue_trend_by_period(filepath: str,
                             period_type: str = 'monthly',
                             category: Optional[str] = None) -> dict[str, float]:
    """
    Analysis 4: Revenue trends over time (monthly/quarterly/yearly).

    FP Pattern: map (extract period) + groupby + sum

    Args:
        filepath: Path to CSV file
        period_type: 'monthly', 'quarterly', or 'yearly'
        category: Optional category filter

    Returns:
        Dictionary {period: revenue}, sorted by period
    """
    records = parse_csv_stream(filepath)

    if category:
        records = filter_by_category(records, category)

    # Convert to list to add period field (map operation)
    records_list = list(records)

    # Create temporary records with period as a field for grouping
    # This demonstrates map transformation
    records_with_period = []
    for r in records_list:
        period = extract_period(r, period_type)
        # Create a simple object with period and revenue
        records_with_period.append({'period': period, 'revenue': r.revenue})

    # Group by period and sum
    from itertools import groupby
    records_with_period.sort(key=lambda x: x['period'])

    result = {}
    for period, group in groupby(records_with_period, key=lambda x: x['period']):
        result[period] = sum(item['revenue'] for item in group)

    # Return sorted by period
    return dict(sorted(result.items()))


def product_performance(filepath: str,
                        region: Optional[str] = None,
                        top_n: int = 10) -> list[tuple[str, int]]:
    """
    Analysis 5: Top products by quantity sold.

    FP Pattern: filter + groupby + sum (quantity) + sort

    Args:
        filepath: Path to CSV file
        region: Optional region filter
        top_n: Number of top products

    Returns:
        List of (product_name, total_quantity) tuples
    """
    records = parse_csv_stream(filepath)

    if region:
        records = filter_by_region(records, region)

    return top_n_by_metric(records, 'product_name', 'quantity', top_n)


def profit_margin_by_subcategory(filepath: str, category: Optional[str] = None) -> dict[str, float]:
    """
    Analysis 6: Profit margin % by sub-category.

    FP Pattern: map (calculate margin) + groupby + avg

    Args:
        filepath: Path to CSV file
        category: Optional category filter

    Returns:
        Dictionary {sub_category: avg_profit_margin_pct}
    """
    records = parse_csv_stream(filepath)

    if category:
        records = filter_by_category(records, category)

    # Convert to list to calculate margins
    records_list = list(records)

    # Group by sub_category
    groups = group_by_field(iter(records_list), 'sub_category')

    # Calculate average margin per sub-category
    result = {}
    for sub_cat, group_records in groups.items():
        # Calculate margin for each record in group
        margins = [
            (r.profit / r.revenue * 100) if r.revenue > 0 else 0.0
            for r in group_records
        ]
        # Average the margins
        result[sub_cat] = sum(margins) / len(margins) if margins else 0.0

    return result


def category_preference_by_region(filepath: str) -> dict[str, tuple[str, float]]:
    """
    Analysis 7: Top category per region by revenue.

    FP Pattern: multi-level grouping (region x category)

    Args:
        filepath: Path to CSV file

    Returns:
        Dictionary {region: (top_category, revenue)}
    """
    records = parse_csv_stream(filepath)

    # Multi-level grouping by region and category
    by_region_category = multi_level_grouping(records, 'region', 'category')

    # Find top category per region
    result = {}
    for region, categories in by_region_category.items():
        # Sum revenue for each category in this region
        category_revenues = {
            cat: sum(r.revenue for r in records_list)
            for cat, records_list in categories.items()
        }
        # Find max
        top_category = max(category_revenues.items(), key=lambda x: x[1])
        result[region] = top_category

    return result


def avg_order_value(filepath: str,
                    category: Optional[str] = None,
                    region: Optional[str] = None) -> dict[str, float]:
    """
    Analysis 8: Average order value by various dimensions.

    FP Pattern: filter + groupby + avg

    Args:
        filepath: Path to CSV file
        category: Optional category filter
        region: Optional region filter

    Returns:
        Dictionary with average order values by category
    """
    records = parse_csv_stream(filepath)

    # Apply filters
    if category:
        records = filter_by_category(records, category)
    if region:
        records = filter_by_region(records, region)

    # Calculate average revenue per category
    avg_revenue_by_cat = avg_by_group(records, 'category', 'revenue')

    return avg_revenue_by_cat
