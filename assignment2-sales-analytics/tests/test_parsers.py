"""
Tests for CSV parsing module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from datetime import datetime
from parsers import parse_csv_stream, peek_csv
from models import SalesRecord


def test_parse_csv_stream_lazy():
    """Test that parsing is lazy (doesn't load entire file)"""
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'product_sales_dataset_final.csv'))
    gen = parse_csv_stream(filepath)

    # Generator should not be a list
    assert not isinstance(gen, list)

    # Should be able to get first record
    first = next(gen)
    assert isinstance(first, SalesRecord)


def test_peek_csv():
    """Test peeking at first N records"""
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'product_sales_dataset_final.csv'))
    records = peek_csv(filepath, n=10)

    assert len(records) == 10
    assert all(isinstance(r, SalesRecord) for r in records)


def test_parse_row_data_types():
    """Test that parsed data has correct types"""
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'product_sales_dataset_final.csv'))
    record = next(parse_csv_stream(filepath))

    assert isinstance(record.order_id, int)
    assert isinstance(record.order_date, datetime)
    assert isinstance(record.customer_name, str)
    assert isinstance(record.quantity, int)
    assert isinstance(record.revenue, float)
    assert isinstance(record.profit, float)


if __name__ == '__main__':
    test_parse_csv_stream_lazy()
    print("[PASS] test_parse_csv_stream_lazy")

    test_peek_csv()
    print("[PASS] test_peek_csv")

    test_parse_row_data_types()
    print("[PASS] test_parse_row_data_types")

    print("\nAll parsers tests passed!")
