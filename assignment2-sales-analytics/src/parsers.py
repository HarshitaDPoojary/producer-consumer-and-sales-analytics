"""
CSV parsing with lazy evaluation using generators.
Demonstrates stream-like processing without loading entire file into memory.
"""

import csv
from datetime import datetime
from itertools import islice
from typing import Generator, Iterator

from models import SalesRecord
from utils import setup_logger


logger = setup_logger(__name__)


def parse_csv_stream(filepath: str) -> Generator[SalesRecord, None, None]:
    """
    Generator that yields SalesRecord objects one at a time.

    This is the core of the functional "stream" approach - records are
    yielded lazily, never loading the entire 200K records into memory.

    Args:
        filepath: Path to CSV file

    Yields:
        SalesRecord objects one at a time

    FP Principle: Lazy Evaluation (Generator Expression)
    - Only computes values when requested
    - Memory efficient for large datasets
    - Similar to Java Streams or Haskell lazy lists

    Example:
        >>> records = parse_csv_stream('data.csv')  # No file I/O yet
        >>> first = next(records)  # Only now does it read first row
        >>> for record in records:  # Reads one row at a time
        ...     process(record)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Yield parsed record - lazy evaluation in action
                yield _parse_row(row)
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise
    except Exception as e:
        logger.error(f"Error reading CSV: {e}")
        raise


def _parse_row(row: dict) -> SalesRecord:
    """
    Parse single CSV row into SalesRecord.

    Pure function that transforms raw CSV dict into typed namedtuple.
    Handles data cleaning (space trimming) and type conversion.

    Args:
        row: Dictionary from csv.DictReader

    Returns:
        SalesRecord namedtuple

    FP Principle: Pure Function
    - Same input always produces same output
    - No side effects
    - Deterministic transformation

    Data Cleaning:
    - Trims spaces from numeric fields (e.g., " Unit_Price " → "Unit_Price")
    - Parses dates from MM-DD-YY format
    - Converts strings to appropriate types
    """
    # Helper to safely parse numeric fields with spaces
    def safe_float(value: str) -> float:
        """Pure function to parse float, trimming spaces"""
        return float(value.strip()) if value else 0.0

    def safe_int(value: str) -> int:
        """Pure function to parse int, trimming spaces"""
        return int(value.strip()) if value else 0

    # Parse date from MM-DD-YY format to datetime object
    def parse_date(date_str: str) -> datetime:
        """Pure function to parse MM-DD-YY date format"""
        try:
            return datetime.strptime(date_str.strip(), '%m-%d-%y')
        except ValueError:
            # Try alternate format if first fails
            return datetime.strptime(date_str.strip(), '%m/%d/%Y')

    # Create immutable SalesRecord from parsed values
    return SalesRecord(
        order_id=safe_int(row['Order_ID']),
        order_date=parse_date(row['Order_Date']),
        customer_name=row['Customer_Name'].strip(),
        city=row['City'].strip(),
        state=row['State'].strip(),
        region=row['Region'].strip(),
        country=row['Country'].strip(),
        category=row['Category'].strip(),
        sub_category=row['Sub_Category'].strip(),
        product_name=row['Product_Name'].strip(),
        quantity=safe_int(row['Quantity']),
        unit_price=safe_float(row[' Unit_Price ']),  # Note: has spaces in header
        revenue=safe_float(row[' Revenue ']),         # Note: has spaces
        profit=safe_float(row[' Profit '])            # Note: has spaces
    )


def parse_csv_batch(filepath: str, batch_size: int = 1000) -> Generator[list[SalesRecord], None, None]:
    """
    Generator that yields batches of records.

    Useful for operations that benefit from batching while maintaining
    lazy evaluation. Uses itertools.islice for efficient batching.

    Args:
        filepath: Path to CSV file
        batch_size: Number of records per batch

    Yields:
        Lists of SalesRecord objects (batch_size records each)

    FP Principle: Lazy Evaluation + Higher-Order Function
    - Uses itertools.islice (functional tool for lazy slicing)
    - Maintains memory efficiency while allowing batch processing

    Example:
        >>> batches = parse_csv_batch('data.csv', batch_size=100)
        >>> first_batch = next(batches)  # List of 100 records
        >>> len(first_batch)
        100
    """
    stream = parse_csv_stream(filepath)

    while True:
        # Use islice to take next batch_size records lazily
        batch = list(islice(stream, batch_size))
        if not batch:
            break
        yield batch


def peek_csv(filepath: str, n: int = 5) -> list[SalesRecord]:
    """
    Peek at first N records without consuming the stream.

    Useful for data exploration and testing.

    Args:
        filepath: Path to CSV file
        n: Number of records to peek

    Returns:
        List of first N records

    FP Principle: Partial Evaluation
    - Uses islice to take only needed records
    - Demonstrates lazy evaluation benefits
    """
    stream = parse_csv_stream(filepath)
    return list(islice(stream, n))
