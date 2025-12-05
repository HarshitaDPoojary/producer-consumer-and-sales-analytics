"""
Tests for analysis module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from analyzers import (
    revenue_by_category, profit_by_region, top_customers_by_revenue,
    revenue_trend_by_period, product_performance, profit_margin_by_subcategory,
    category_preference_by_region, avg_order_value
)


FILEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'product_sales_dataset_final.csv'))


def test_revenue_by_category():
    """Test revenue aggregation by category"""
    results = revenue_by_category(FILEPATH)
    
    assert isinstance(results, dict)
    assert len(results) > 0
    assert all(isinstance(k, str) for k in results.keys())
    assert all(isinstance(v, float) for v in results.values())
    assert all(v > 0 for v in results.values())


def test_revenue_by_category_with_filter():
    """Test revenue by category with category filter"""
    results = revenue_by_category(FILEPATH, category='Electronics')
    
    assert isinstance(results, dict)
    # Should have Electronics data
    assert 'Electronics' in results or len(results) == 1


def test_profit_by_region():
    """Test profit aggregation by region"""
    results = profit_by_region(FILEPATH)
    
    assert isinstance(results, dict)
    assert len(results) > 0
    assert all(isinstance(k, str) for k in results.keys())
    assert all(isinstance(v, float) for v in results.values())


def test_top_customers_by_revenue():
    """Test top customers ranking"""
    results = top_customers_by_revenue(FILEPATH, n=10)
    
    assert isinstance(results, list)
    assert len(results) <= 10
    assert all(isinstance(item, tuple) and len(item) == 2 for item in results)
    
    # Check sorted descending
    if len(results) > 1:
        assert results[0][1] >= results[1][1]


def test_revenue_trend_by_period():
    """Test time series analysis"""
    results = revenue_trend_by_period(FILEPATH, period_type='monthly')
    
    assert isinstance(results, dict)
    assert len(results) > 0
    
    # Keys should be period strings
    keys = list(results.keys())
    assert all('-' in k for k in keys)  # Monthly format YYYY-MM


def test_revenue_trend_yearly():
    """Test yearly trend"""
    results = revenue_trend_by_period(FILEPATH, period_type='yearly')
    
    assert isinstance(results, dict)
    assert len(results) > 0


def test_product_performance():
    """Test product ranking"""
    results = product_performance(FILEPATH, top_n=10)
    
    assert isinstance(results, list)
    assert len(results) <= 10
    assert all(isinstance(item, tuple) and len(item) == 2 for item in results)


def test_profit_margin_by_subcategory():
    """Test profit margin calculation"""
    results = profit_margin_by_subcategory(FILEPATH)
    
    assert isinstance(results, dict)
    assert len(results) > 0
    assert all(isinstance(v, float) for v in results.values())
    # Profit margins should be percentages
    assert all(v >= 0 and v <= 100 for v in results.values())


def test_category_preference_by_region():
    """Test multi-level grouping"""
    results = category_preference_by_region(FILEPATH)
    
    assert isinstance(results, dict)
    assert len(results) > 0
    # Should be dict: {region: (top_category, revenue)}
    for region, top_category_tuple in results.items():
        assert isinstance(top_category_tuple, tuple)
        assert len(top_category_tuple) == 2
        assert isinstance(top_category_tuple[0], str)  # category name
        assert isinstance(top_category_tuple[1], float)  # revenue


def test_avg_order_value():
    """Test average order value calculation"""
    results = avg_order_value(FILEPATH)
    
    assert isinstance(results, dict)
    assert len(results) > 0
    # Returns average order value by category
    assert all(isinstance(v, float) for v in results.values())
    assert all(v > 0 for v in results.values())


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
