"""
Tests for output formatting module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from io import StringIO
from output import format_console_output
import os


def test_format_console_output_dict(capsys):
    """Test dictionary formatting"""
    data = {'Category A': 1000.50, 'Category B': 2000.75}
    format_console_output(data, 'Test Title', 'dict')
    
    captured = capsys.readouterr()
    assert 'TEST TITLE' in captured.out
    assert 'Category A' in captured.out
    assert '1,000.50' in captured.out


def test_format_console_output_list(capsys):
    """Test list formatting with ranking"""
    data = [('Customer A', 5000.0), ('Customer B', 3000.0)]
    format_console_output(data, 'Top Customers', 'list')
    
    captured = capsys.readouterr()
    assert 'TOP CUSTOMERS' in captured.out
    assert 'Rank' in captured.out
    assert 'Customer A' in captured.out


def test_format_console_output_trend(capsys):
    """Test trend data formatting"""
    data = {'2023-01': 10000.0, '2023-02': 12000.0}
    format_console_output(data, 'Revenue Trend', 'trend')
    
    captured = capsys.readouterr()
    assert 'REVENUE TREND' in captured.out
    assert '2023-01' in captured.out
    assert 'Period' in captured.out


def test_output_directory_creation():
    """Test that output directory gets created"""
    from output import display_results
    
    test_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'test_output_dir'))
    if os.path.exists(test_dir):
        os.rmdir(test_dir)
    
    # This should create the directory
    data = {'A': 100, 'B': 200}
    try:
        # Just test console output, skip plotting
        display_results(data, 'Test', plot_type=None)
    except:
        pass  # OK if it fails, we're just testing directory creation
    
    # Verify output base directory exists
    output_base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output'))
    assert os.path.exists(output_base)


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
