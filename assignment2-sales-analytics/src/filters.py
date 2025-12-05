"""
Filtering operations with predicates.
Demonstrates filter with lambda expressions (functional programming).
"""

from datetime import datetime
from typing import Iterator, Callable, Any

from models import SalesRecord


def filter_by_predicate(records: Iterator[SalesRecord], predicate: Callable[[SalesRecord], bool]) -> Iterator[SalesRecord]:
    """
    Generic filter using predicate function.

    Args:
        records: Iterator of SalesRecord objects
        predicate: Function that returns True/False for each record

    Returns:
        Filtered iterator

    FP Principle: Higher-Order Function + filter
    - Takes function (predicate) as parameter
    - Uses built-in filter (functional approach)
    - Lazy evaluation (returns iterator)

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> high_revenue = filter_by_predicate(
        ...     records,
        ...     lambda r: r.revenue > 1000
        ... )
    """
    return filter(predicate, records)


def filter_by_field(records: Iterator[SalesRecord], field_name: str, value: Any) -> Iterator[SalesRecord]:
    """
    Filter records where field equals value.

    Args:
        records: Iterator of SalesRecord objects
        field_name: Name of field to check
        value: Value to match

    Returns:
        Filtered iterator

    FP Principle: filter + lambda
    - Lambda creates inline predicate
    - Lazy evaluation

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> electronics = filter_by_field(records, 'category', 'Electronics')
    """
    return filter(lambda r: getattr(r, field_name) == value, records)


def filter_by_category(records: Iterator[SalesRecord], category: str) -> Iterator[SalesRecord]:
    """
    Filter by product category.

    Args:
        records: Iterator of SalesRecord objects
        category: Category to filter ('Electronics', 'Clothing & Apparel', etc.)

    Returns:
        Filtered iterator

    FP Principle: Partial Application (specialized filter)
    """
    return filter_by_field(records, 'category', category)


def filter_by_region(records: Iterator[SalesRecord], region: str) -> Iterator[SalesRecord]:
    """
    Filter by geographic region.

    Args:
        records: Iterator of SalesRecord objects
        region: Region to filter ('East', 'West', 'South', 'Centre')

    Returns:
        Filtered iterator

    FP Principle: Partial Application
    """
    return filter_by_field(records, 'region', region)


def filter_by_date_range(records: Iterator[SalesRecord],
                          start_date: datetime,
                          end_date: datetime) -> Iterator[SalesRecord]:
    """
    Filter by date range.

    Args:
        records: Iterator of SalesRecord objects
        start_date: Start date (inclusive)
        end_date: End date (inclusive)

    Returns:
        Filtered iterator

    FP Principle: filter + lambda with complex predicate
    """
    return filter(
        lambda r: start_date <= r.order_date <= end_date,
        records
    )


def filter_by_period(records: Iterator[SalesRecord],
                     year: int = None,
                     month: int = None,
                     quarter: int = None) -> Iterator[SalesRecord]:
    """
    Filter by time period (yearly/quarterly/monthly).

    Args:
        records: Iterator of SalesRecord objects
        year: Year to filter (e.g., 2023)
        month: Month to filter (1-12)
        quarter: Quarter to filter (1-4)

    Returns:
        Filtered iterator

    FP Principle: Composable predicates
    - Builds predicate based on parameters
    - Combines multiple conditions functionally

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> q4_2023 = filter_by_period(records, year=2023, quarter=4)
    """
    def build_predicate():
        """Build predicate based on provided parameters"""
        predicates = []

        if year is not None:
            predicates.append(lambda r: r.order_date.year == year)

        if month is not None:
            predicates.append(lambda r: r.order_date.month == month)

        if quarter is not None:
            # Q1: Jan-Mar (1-3), Q2: Apr-Jun (4-6), Q3: Jul-Sep (7-9), Q4: Oct-Dec (10-12)
            q_start = (quarter - 1) * 3 + 1
            q_end = quarter * 3
            predicates.append(lambda r: q_start <= r.order_date.month <= q_end)

        # Combine all predicates with AND
        return lambda r: all(pred(r) for pred in predicates)

    if not any([year, month, quarter]):
        # No filters, return all
        return records

    predicate = build_predicate()
    return filter(predicate, records)


def filter_by_revenue_range(records: Iterator[SalesRecord],
                             min_revenue: float = 0.0,
                             max_revenue: float = float('inf')) -> Iterator[SalesRecord]:
    """
    Filter by revenue range.

    Args:
        records: Iterator of SalesRecord objects
        min_revenue: Minimum revenue (inclusive)
        max_revenue: Maximum revenue (inclusive)

    Returns:
        Filtered iterator

    FP Principle: filter + lambda
    """
    return filter(
        lambda r: min_revenue <= r.revenue <= max_revenue,
        records
    )


def filter_by_profit_margin(records: Iterator[SalesRecord],
                            min_margin_pct: float = 0.0) -> Iterator[SalesRecord]:
    """
    Filter by minimum profit margin percentage.

    Args:
        records: Iterator of SalesRecord objects
        min_margin_pct: Minimum profit margin % (e.g., 20.0 for 20%)

    Returns:
        Filtered iterator

    FP Principle: filter + lambda with derived metric
    """
    return filter(
        lambda r: (r.profit / r.revenue * 100) >= min_margin_pct if r.revenue > 0 else False,
        records
    )
