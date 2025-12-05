"""
Functional transformation utilities.
Demonstrates map/reduce/compose patterns from functional programming.
"""

from functools import reduce
from typing import Callable, Iterator, Any
import operator


def compose(*functions: Callable) -> Callable:
    """
    Compose multiple functions (f ∘ g ∘ h).

    Composes functions right-to-left, like mathematical composition.

    Args:
        *functions: Variable number of functions to compose

    Returns:
        Composed function

    FP Principle: Function Composition
    - Combines simple functions into complex ones
    - Pure functional pattern from mathematics

    Example:
        >>> add_one = lambda x: x + 1
        >>> double = lambda x: x * 2
        >>> f = compose(double, add_one)
        >>> f(5)  # double(add_one(5)) = double(6) = 12
        12
    """
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)


def extract_field(records: Iterator, field_name: str) -> Iterator:
    """
    Extract single field from record stream.

    Uses map with lambda for field extraction.

    Args:
        records: Iterator of SalesRecord objects
        field_name: Name of field to extract

    Returns:
        Iterator of field values

    FP Principle: map + lambda
    - map applies function to each element
    - Lambda creates inline function
    - Lazy evaluation (returns iterator, not list)

    Example:
        >>> records = [SalesRecord(...), SalesRecord(...)]
        >>> revenues = extract_field(records, 'revenue')
        >>> list(revenues)
        [1000.0, 2000.0, ...]
    """
    return map(lambda r: getattr(r, field_name), records)


def transform_field(records: Iterator, field_name: str, transform_fn: Callable) -> Iterator:
    """
    Apply transformation to specific field.

    Higher-order function that takes transformation function.

    Args:
        records: Iterator of SalesRecord objects
        field_name: Name of field to transform
        transform_fn: Function to apply to field

    Returns:
        Iterator of transformed values

    FP Principle: Higher-Order Function + map
    - Takes function as parameter
    - Returns transformed iterator

    Example:
        >>> records = [record1, record2]
        >>> # Get profit margins (profit / revenue)
        >>> margins = transform_field(records, 'profit',
        ...                          lambda p, r: (p / r.revenue) * 100)
    """
    return map(lambda r: transform_fn(getattr(r, field_name)), records)


def sum_field(records: Iterator, field_name: str) -> float:
    """
    Sum numeric field across all records.

    Uses reduce with operator.add for aggregation.

    Args:
        records: Iterator of SalesRecord objects
        field_name: Name of numeric field to sum

    Returns:
        Sum of field values

    FP Principle: reduce + operator
    - reduce collapses sequence to single value
    - operator.add is functional addition
    - No loops, pure functional approach

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> total_revenue = sum_field(records, 'revenue')
        27604926.40
    """
    return reduce(
        operator.add,
        map(lambda r: getattr(r, field_name), records),
        0.0
    )


def avg_field(records: Iterator, field_name: str) -> float:
    """
    Average numeric field across records.

    Args:
        records: Iterator of SalesRecord objects
        field_name: Name of numeric field

    Returns:
        Average of field values

    FP Principle: reduce for aggregation
    - Uses reduce to compute sum and count simultaneously
    - Pure function (no side effects)
    """
    # Convert to list once (need to traverse twice)
    records_list = list(records)
    if not records_list:
        return 0.0

    total = sum_field(iter(records_list), field_name)
    count = len(records_list)
    return total / count if count > 0 else 0.0


def calculate_metric(records: Iterator, numerator_field: str, denominator_field: str) -> Iterator[float]:
    """
    Calculate ratio metrics (e.g., profit margin = profit / revenue).

    Args:
        records: Iterator of SalesRecord objects
        numerator_field: Field for numerator
        denominator_field: Field for denominator

    Returns:
        Iterator of ratio values

    FP Principle: map with lambda
    - Computes derived metrics functionally
    - Lazy evaluation

    Example:
        >>> records = parse_csv_stream('data.csv')
        >>> margins = calculate_metric(records, 'profit', 'revenue')
        >>> list(islice(margins, 5))
        [0.367, 0.327, 0.374, ...]
    """
    return map(
        lambda r: (getattr(r, numerator_field) / getattr(r, denominator_field))
                  if getattr(r, denominator_field) != 0 else 0.0,
        records
    )


def count_records(records: Iterator) -> int:
    """
    Count number of records in iterator.

    Args:
        records: Iterator of SalesRecord objects

    Returns:
        Count of records

    FP Principle: reduce for aggregation
    - Counts without explicit loop
    """
    return reduce(lambda count, _: count + 1, records, 0)
