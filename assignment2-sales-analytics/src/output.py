"""
Output formatting and visualization coordination.
Centralized output handling for console and plots.
"""

from typing import Any, Optional
import os


def format_console_output(data: Any, title: str, data_type: str = 'dict') -> None:
    """
    Pretty-print results to console.

    Args:
        data: Analysis results (dict or list of tuples)
        title: Title for output
        data_type: Type of data ('dict', 'list', 'trend')
    """
    print("\n" + "=" * 60)
    print(title.upper())
    print("=" * 60)

    if data_type == 'dict':
        # Dictionary output
        for key, value in data.items():
            if isinstance(value, float):
                print(f"{str(key):<30} ${value:>15,.2f}")
            elif isinstance(value, tuple):
                # Handle tuple values (e.g., category preferences)
                print(f"{str(key):<30} {str(value[0]):<20} ${value[1]:>15,.2f}")
            else:
                print(f"{str(key):<30} {value:>15}")

    elif data_type == 'list':
        # List of tuples (ranking)
        print(f"{'Rank':<6} {'Name':<30} {'Value':>15}")
        print("-" * 60)
        for rank, (name, value) in enumerate(data, 1):
            if isinstance(value, float):
                print(f"{rank:<6} {str(name):<30} ${value:>15,.2f}")
            else:
                print(f"{rank:<6} {str(name):<30} {value:>15}")

    elif data_type == 'trend':
        # Time series data
        print(f"{'Period':<15} {'Value':>20}")
        print("-" * 60)
        for period, value in sorted(data.items()):
            print(f"{period:<15} ${value:>20,.2f}")

    print("=" * 60)


def display_results(data: Any, title: str, plot_type: Optional[str] = None, save_dir: str = 'output') -> None:
    """
    Combined console + plot output.

    Args:
        data: Analysis results
        title: Title for output
        plot_type: Type of plot ('bar', 'line', 'pie', None)
        save_dir: Directory to save plots
    """
    # Determine data type for formatting
    if isinstance(data, dict):
        if any(isinstance(k, str) and '-' in k for k in data.keys()):
            data_type = 'trend'
        else:
            data_type = 'dict'
    elif isinstance(data, list):
        data_type = 'list'
    else:
        data_type = 'dict'

    # Console output
    format_console_output(data, title, data_type)

    # Optional visualization
    if plot_type:
        # Ensure output directory exists
        os.makedirs(save_dir, exist_ok=True)

        # Generate filename from title
        filename = title.lower().replace(' ', '_').replace('/', '_') + '.png'
        save_path = os.path.join(save_dir, filename)

        # Import visualizers here to avoid circular import
        from visualizers import plot_bar_chart, plot_line_chart, plot_pie_chart

        if plot_type == 'bar':
            plot_bar_chart(data, title, 'Value', 'Category', save_path=save_path)
        elif plot_type == 'line':
            plot_line_chart(data, title, 'Period', 'Value', save_path=save_path)
        elif plot_type == 'pie':
            plot_pie_chart(data, title, save_path=save_path)
