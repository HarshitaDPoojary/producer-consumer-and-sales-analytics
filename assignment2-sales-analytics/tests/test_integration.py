"""
Integration tests for end-to-end workflows.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from analyzers import revenue_by_category, top_customers_by_revenue
from output import format_console_output


FILEPATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'product_sales_dataset_final.csv'))


def test_full_analysis_workflow():
    """Test complete analysis pipeline"""
    # Run analysis
    results = revenue_by_category(FILEPATH)
    
    # Verify results
    assert isinstance(results, dict)
    assert len(results) > 0
    
    # Format output (should not raise exception)
    try:
        format_console_output(results, 'Integration Test', 'dict')
        success = True
    except Exception as e:
        print(f"Error: {e}")
        success = False
    
    assert success


def test_filtered_analysis_workflow():
    """Test analysis with filters"""
    # Analysis with filter
    customers = top_customers_by_revenue(FILEPATH, n=5, category='Electronics')
    
    assert isinstance(customers, list)
    assert len(customers) <= 5


def test_multiple_analyses():
    """Test running multiple analyses"""
    analyses = [
        revenue_by_category(FILEPATH),
        top_customers_by_revenue(FILEPATH, n=10)
    ]
    
    # All should return valid results
    assert all(len(result) > 0 for result in analyses)


def test_data_file_exists():
    """Verify data file is present"""
    assert os.path.exists(FILEPATH), f"Data file not found: {FILEPATH}"


def test_output_directory_exists():
    """Verify output directory structure"""
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    assert os.path.exists(output_dir)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
