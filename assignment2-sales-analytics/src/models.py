"""
Data models for Sales Analytics Application.
Immutable data structures using namedtuple (functional programming principle).
"""

from collections import namedtuple
from datetime import datetime
from typing import Literal


# Immutable sales record structure
# FP Principle: Immutability - namedtuple creates immutable objects
SalesRecord = namedtuple('SalesRecord', [
    'order_id',        # int: Unique order identifier (1-200,000)
    'order_date',      # datetime: Date of order
    'customer_name',   # str: Customer name
    'city',            # str: City name
    'state',           # str: U.S. state
    'region',          # str: Region (East/West/South/Centre)
    'country',         # str: Country (all United States)
    'category',        # str: Product category
    'sub_category',    # str: Product sub-category
    'product_name',    # str: Product name
    'quantity',        # int: Quantity ordered
    'unit_price',      # float: Price per unit
    'revenue',         # float: Total revenue
    'profit'           # float: Total profit
])


PeriodType = Literal['yearly', 'quarterly', 'monthly']


def extract_period(record: SalesRecord, period_type: PeriodType = 'monthly') -> str:
    """
    Extract time period from sales record.

    Pure function that derives period string from order date.

    Args:
        record: Sales record with order_date
        period_type: Type of period ('yearly', 'quarterly', 'monthly')

    Returns:
        Period string in format:
        - yearly: 'YYYY' (e.g., '2023')
        - quarterly: 'YYYY-Q1' (e.g., '2023-Q1')
        - monthly: 'YYYY-MM' (e.g., '2023-01')

    FP Principle: Pure function (deterministic, no side effects)

    Examples:
        >>> from datetime import datetime
        >>> record = SalesRecord(1, datetime(2023, 3, 15), 'John', 'NYC', 'NY',
        ...                      'East', 'US', 'Electronics', 'Phone', 'iPhone',
        ...                      1, 999.0, 999.0, 299.0)
        >>> extract_period(record, 'yearly')
        '2023'
        >>> extract_period(record, 'quarterly')
        '2023-Q1'
        >>> extract_period(record, 'monthly')
        '2023-03'
    """
    date = record.order_date

    if period_type == 'yearly':
        return f"{date.year}"
    elif period_type == 'quarterly':
        quarter = (date.month - 1) // 3 + 1
        return f"{date.year}-Q{quarter}"
    elif period_type == 'monthly':
        return f"{date.year}-{date.month:02d}"
    else:
        raise ValueError(f"Invalid period_type: {period_type}. Must be 'yearly', 'quarterly', or 'monthly'")


def get_profit_margin(record: SalesRecord) -> float:
    """
    Calculate profit margin percentage.

    Pure function to compute profit margin from revenue and profit.

    Args:
        record: Sales record with revenue and profit

    Returns:
        Profit margin as percentage (0-100)

    FP Principle: Pure function (no side effects, deterministic)

    Example:
        >>> record = SalesRecord(1, datetime(2023, 1, 1), 'John', 'NYC', 'NY',
        ...                      'East', 'US', 'Electronics', 'Phone', 'iPhone',
        ...                      1, 1000.0, 1000.0, 300.0)
        >>> get_profit_margin(record)
        30.0
    """
    if record.revenue == 0:
        return 0.0
    return (record.profit / record.revenue) * 100
