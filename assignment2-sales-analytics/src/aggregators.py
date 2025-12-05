"""
Aggregation operations using itertools.groupby and reduce.
Demonstrates functional grouping and aggregation patterns.
"""

from itertools import groupby
from functools import reduce
from typing import Iterator, Callable, Any
import operator

from models import SalesRecord


def group_by_field(records: Iterator[SalesRecord], field_name: str) -> dict[Any, list[SalesRecord]]:
    """
    Group records by field value.

    Uses itertools.groupby for functional grouping.
    Note: Requires sorted input for groupby to work correctly.

    Args:
        records: Iterator of SalesRecord objects
        field_name: Field to group by

    Returns:
        Dictionary {field_value: [records...]}

    FP Principle: itertools.groupby
    - Functional grouping without explicit loops
    - Lambda for key extraction

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> by_region = group_by_field(records, 'region')
        >>> by_region['East']  # All records from East region
        [SalesRecord(...), SalesRecord(...), ...]
    """
    # Sort first (required for groupby)
    sorted_records = sorted(records, key=lambda r: getattr(r, field_name))

    # Group using itertools.groupby
    return {
        key: list(group)
        for key, group in groupby(sorted_records, key=lambda r: getattr(r, field_name))
    }


def aggregate_by_group(records: Iterator[SalesRecord],
                       group_field: str,
                       agg_field: str,
                       agg_fn: Callable) -> dict[Any, float]:
    """
    Generic aggregation by group.

    Higher-order function that accepts aggregation function.

    Args:
        group_field: Field to group by
        agg_field: Field to aggregate
        agg_fn: Aggregation function (sum, max, min, etc.)

    Returns:
        Dictionary {group_value: aggregated_value}

    FP Principle: Higher-Order Function
    - Takes function as parameter
    - Composes grouping + aggregation

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> revenue_by_category = aggregate_by_group(
        ...     records, 'category', 'revenue', sum
        ... )
    """
    groups = group_by_field(records, group_field)
    return {
        key: agg_fn(getattr(r, agg_field) for r in group)
        for key, group in groups.items()
    }


def sum_by_group(records: Iterator[SalesRecord], group_field: str, sum_field: str) -> dict[Any, float]:
    """
    Sum a field grouped by another field.

    Args:
        records: Iterator of SalesRecord objects
        group_field: Field to group by
        sum_field: Field to sum

    Returns:
        Dictionary {group_value: sum}

    FP Principle: Partial Application
    - Specialized version of aggregate_by_group
    - Uses built-in sum (functional)

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> profit_by_region = sum_by_group(records, 'region', 'profit')
        {'East': 5000000.0, 'West': 4500000.0, ...}
    """
    return aggregate_by_group(records, group_field, sum_field, sum)


def avg_by_group(records: Iterator[SalesRecord], group_field: str, avg_field: str) -> dict[Any, float]:
    """
    Average a field grouped by another field.

    Args:
        records: Iterator of SalesRecord objects
        group_field: Field to group by
        avg_field: Field to average

    Returns:
        Dictionary {group_value: average}

    FP Principle: Functional aggregation
    - Uses lambda for average calculation
    """
    def average(values):
        """Pure function to calculate average"""
        vals = list(values)
        return sum(vals) / len(vals) if vals else 0.0

    return aggregate_by_group(records, group_field, avg_field, average)


def count_by_group(records: Iterator[SalesRecord], group_field: str) -> dict[Any, int]:
    """
    Count records by group.

    Args:
        records: Iterator of SalesRecord objects
        group_field: Field to group by

    Returns:
        Dictionary {group_value: count}

    FP Principle: map + reduce pattern
    """
    groups = group_by_field(records, group_field)
    return {key: len(group) for key, group in groups.items()}


def top_n_by_metric(records: Iterator[SalesRecord],
                    group_field: str,
                    metric_field: str,
                    n: int = 10) -> list[tuple[Any, float]]:
    """
    Get top N groups by metric.

    Args:
        records: Iterator of SalesRecord objects
        group_field: Field to group by
        metric_field: Field to rank by
        n: Number of top results

    Returns:
        List of (group_value, metric_value) tuples, sorted descending

    FP Principle: map + sort + slice pipeline
    - Functional transformation pipeline
    - Lambda for sorting

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> top_customers = top_n_by_metric(
        ...     records, 'customer_name', 'revenue', n=10
        ... )
        [('John Smith', 45678.90), ('Sarah Johnson', 42345.67), ...]
    """
    aggregated = sum_by_group(records, group_field, metric_field)
    # Sort by value (descending) and take top N
    return sorted(aggregated.items(), key=lambda x: x[1], reverse=True)[:n]


def multi_level_grouping(records: Iterator[SalesRecord], *group_fields: str) -> dict:
    """
    Multi-dimensional grouping (e.g., by region and category).

    Args:
        records: Iterator of SalesRecord objects
        *group_fields: Fields to group by (in order)

    Returns:
        Nested dictionary structure

    FP Principle: Recursive functional grouping
    - Nested reduce pattern
    - Lambda for key extraction

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> by_region_category = multi_level_grouping(records, 'region', 'category')
        {'East': {'Electronics': [...], 'Clothing & Apparel': [...]}, ...}
    """
    if not group_fields:
        return list(records)

    first_field, *rest_fields = group_fields

    # Group by first field
    groups = group_by_field(records, first_field)

    if not rest_fields:
        # Base case: no more fields to group by
        return groups

    # Recursive case: group each sub-group by remaining fields
    return {
        key: multi_level_grouping(iter(group), *rest_fields)
        for key, group in groups.items()
    }


def find_max_by_group(records: Iterator[SalesRecord],
                      group_field: str,
                      max_field: str) -> dict[Any, float]:
    """
    Find maximum value per group.

    Args:
        records: Iterator of SalesRecord objects
        group_field: Field to group by
        max_field: Field to find max of

    Returns:
        Dictionary {group_value: max_value}

    FP Principle: Higher-order aggregation with max
    """
    return aggregate_by_group(records, group_field, max_field, max)
