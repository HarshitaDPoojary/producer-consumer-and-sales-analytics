"""
Visualization wrappers for matplotlib.
Functional approach to plotting with reusable templates.
"""

import matplotlib.pyplot as plt
from functools import wraps
from typing import Callable, Optional
import os


def with_plot_styling(plot_fn: Callable) -> Callable:
    """
    Decorator to apply consistent styling to plots.

    FP Principle: Decorator Pattern (Higher-Order Function)
    - Wraps plot function with styling
    - Pure functional decoration

    Args:
        plot_fn: Plot function to wrap

    Returns:
        Wrapped function with styling applied
    """
    @wraps(plot_fn)
    def wrapper(*args, **kwargs):
        # Apply theme
        plt.style.use('default')
        result = plot_fn(*args, **kwargs)
        plt.tight_layout()
        return result
    return wrapper


@with_plot_styling
def plot_bar_chart(data: dict, title: str, xlabel: str, ylabel: str, top_n: Optional[int] = None, save_path: Optional[str] = None):
    """
    Generic bar chart visualization.

    Args:
        data: Dictionary or list of tuples
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        top_n: Limit to top N items
        save_path: Path to save plot (optional)
    """
    # Convert to sorted list if dict
    if isinstance(data, dict):
        items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    else:
        items = data

    # Limit to top N
    if top_n:
        items = items[:top_n]

    keys, values = zip(*items) if items else ([], [])

    # Create horizontal bar chart
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(keys)), values, color='skyblue')
    plt.yticks(range(len(keys)), keys)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.gca().invert_yaxis()  # Highest at top

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved: {save_path}")

    plt.show()


@with_plot_styling
def plot_line_chart(data: dict, title: str, xlabel: str, ylabel: str, save_path: Optional[str] = None):
    """
    Line chart for time series (trends).

    Args:
        data: Dictionary {period: value}
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label
        save_path: Path to save plot
    """
    # Sort by period
    items = sorted(data.items())
    periods, values = zip(*items) if items else ([], [])

    plt.figure(figsize=(12, 6))
    plt.plot(periods, values, marker='o', linewidth=2, markersize=6)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved: {save_path}")

    plt.show()


@with_plot_styling
def plot_pie_chart(data: dict, title: str, top_n: int = 10, save_path: Optional[str] = None):
    """
    Pie chart for categorical breakdown.

    Args:
        data: Dictionary {category: value}
        title: Chart title
        top_n: Limit to top N slices
        save_path: Path to save plot
    """
    # Sort and limit
    items = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    labels, values = zip(*items) if items else ([], [])

    plt.figure(figsize=(10, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Chart saved: {save_path}")

    plt.show()
