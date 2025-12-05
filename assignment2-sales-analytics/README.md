# Assignment 2: Sales Data Analysis

## Overview
A comprehensive sales analytics application demonstrating functional programming paradigms in Python. The application performs various aggregation and grouping operations on CSV sales data using stream-like operations, lazy evaluation, and pure functions.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Available Analyses](#available-analyses)
- [Data Structure](#data-structure)
- [Testing](#testing)
- [Functional Programming Patterns](#functional-programming-patterns)
- [Sample Output](#sample-output)

## Features

### Core Capabilities
- **8 Analytical Queries** covering revenue, profit, trends, and customer insights
- **Lazy CSV Parsing** with generator-based streaming (memory efficient)
- **Interactive CLI Dashboard** with dynamic filtering
- **Batch Mode** for automated analysis runs
- **Data Visualization** using matplotlib (bar, line, pie charts)
- **Comprehensive Unit Tests** (27 tests, 100% pass rate)

### Functional Programming Patterns
- **Higher-Order Functions**: map, filter, reduce operations
- **Lambda Expressions**: Inline predicates and transformations
- **Immutability**: namedtuple-based data structures
- **Lazy Evaluation**: Generator-based data streaming
- **Function Composition**: Chaining operations
- **Pure Functions**: Deterministic, side-effect-free computations

## Project Structure

```
assignment2-sales-analytics/
├── data/
│   └── product_sales_dataset_final.csv    # Sales dataset (200,000 records)
├── src/
│   ├── analyzers.py        # 8 analytical queries using FP patterns
│   ├── parsers.py          # Lazy CSV parsing with generators
│   ├── filters.py          # Filter operations with predicates
│   ├── aggregators.py      # Grouping and aggregation functions
│   ├── transformers.py     # Data transformation utilities
│   ├── models.py           # Immutable data structures
│   ├── visualizers.py      # Plotting wrappers with decorators
│   ├── output.py           # Console formatting
│   ├── interactive.py      # CLI menu system
│   ├── main.py             # Entry point
│   └── utils.py            # Helper utilities
├── tests/
│   ├── test_analyzers.py      # Analysis function tests (10 tests)
│   ├── test_parsers.py        # CSV parsing tests (3 tests)
│   ├── test_output.py         # Output formatting tests (4 tests)
│   ├── test_visualizers.py    # Visualization tests (5 tests)
│   └── test_integration.py    # End-to-end tests (5 tests)
├── output/                 # Generated charts and visualizations
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Installation

1. **Download the Dataset**
   
   Download the sales dataset from Kaggle:
   - **Source:** [Kaggle - Product Sales Dataset (2023-2024)](https://www.kaggle.com/datasets/yashyennewar/product-sales-dataset-2023-2024)
   - **File:** Download the CSV file (200,000 records)
   - **Location:** Place it in `data/product_sales_dataset_final.csv`
   
   ```bash
   # Ensure the data directory exists
   mkdir -p data
   
   # After downloading from Kaggle, move/rename the file to:
   # data/product_sales_dataset_final.csv
   ```

2. **Clone or navigate to the project directory**
   ```bash
   cd assignment2-sales-analytics
   ```

3. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verify data file exists**
   ```bash
   # Ensure data/product_sales_dataset_final.csv is present
   dir data  # Windows
   ls data   # Linux/Mac
   ```
   
   **Important:** The application requires the dataset to run. If the file is missing, download it from the Kaggle link above.

## Usage

### Interactive Mode (Recommended)

Launch the interactive dashboard with dynamic filtering:

```bash
python src/main.py
```

**Features:**
- Select from 8 different analyses
- Apply filters (category, region, time period)
- Generate visualizations on-demand
- Export charts to `output/` directory

**Example Session:**
```
Select mode:
1. Interactive Mode (dynamic filtering, visualizations)
2. Batch Mode (run all analyses)

Choice (default: 1): 1

SALES ANALYTICS - INTERACTIVE DASHBOARD
=========================================
1. Revenue by Category
2. Profit by Region
3. Top Customers by Revenue
...

Select option: 1

Apply filters (press Enter to skip):
  Category: Electronics
  Region: 
  Period: 

Processing...
[Results displayed]

Generate visualization? (bar/pie/n): bar
[Chart displayed and saved]
```

### Batch Mode

Run all analyses automatically and output to console:

```bash
python src/main.py
# Then select option: 2
```

Or specify mode via code modification or with specific file:
```bash
python src/main.py data/product_sales_dataset_final.csv
```

### Running Tests

Execute all unit tests:

```bash
# Run all tests with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_analyzers.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

**Expected Output:**
```
27 passed in 70.23s
```

## Available Analyses

### 1. Revenue by Category
**Query:** Total revenue grouped by product category  
**FP Pattern:** filter → group_by → sum  
**Output:** `{category: total_revenue}`

### 2. Profit by Region
**Query:** Total profit grouped by geographic region  
**FP Pattern:** filter → group_by → sum  
**Output:** `{region: total_profit}`

### 3. Top Customers by Revenue
**Query:** Top N customers ranked by total revenue  
**FP Pattern:** filter → group_by → sort → limit  
**Output:** `[(customer_name, revenue), ...]`

### 4. Revenue Trends Over Time
**Query:** Time series analysis (monthly/quarterly/yearly)  
**FP Pattern:** map (extract period) → group_by → sum  
**Output:** `{period: revenue}`

### 5. Product Performance
**Query:** Top products by quantity sold  
**FP Pattern:** group_by → sum → sort → limit  
**Output:** `[(product_name, quantity), ...]`

### 6. Profit Margin by Sub-Category
**Query:** Average profit margin percentage by sub-category  
**FP Pattern:** map (calculate margin) → group_by → avg  
**Output:** `{sub_category: avg_margin_pct}`

### 7. Category Preference by Region
**Query:** Most popular category per region  
**FP Pattern:** multi-level grouping → find_max  
**Output:** `{region: (top_category, revenue)}`

### 8. Average Order Value
**Query:** Average revenue per order by category  
**FP Pattern:** filter → group_by → avg  
**Output:** `{category: avg_order_value}`

## Data Structure

### Dataset: Product Sales (200,000 records)
**Source:** [Kaggle - Product Sales Dataset (2023-2024)](https://www.kaggle.com/datasets/yashyennewar/product-sales-dataset-2023-2024)  
**Local File:** `data/product_sales_dataset_final.csv`

**About the Dataset:**
This dataset contains 200,000 synthetic sales records simulating real-world product transactions across different U.S. regions. It is designed for data analysis, business intelligence, and machine learning projects, especially in the areas of sales forecasting, customer segmentation, profitability analysis, and regional trend evaluation.

**Schema:**
```
SalesRecord (namedtuple):
├── order_id: int              # Unique order identifier
├── order_date: datetime       # Transaction date
├── customer_name: str         # Customer name
├── city: str                  # City
├── state: str                 # U.S. state
├── region: str                # Region (East/West/South/Centre)
├── country: str               # Country (United States)
├── category: str              # Product category
│   └── Values: Electronics, Clothing & Apparel, 
│                Accessories, Home & Furniture
├── sub_category: str          # Product sub-category
├── product_name: str          # Product name
├── quantity: int              # Quantity ordered
├── unit_price: float          # Price per unit
├── revenue: float             # Total revenue (quantity × unit_price)
└── profit: float              # Total profit
```

**Data Characteristics:**
- **Size:** 200,000 rows × 14 columns
- **Type:** Synthetic sales records simulating real-world transactions
- **Currency:** All transactions in USD
- **Time Period:** January 2023 to December 2024
- **Geography:** United States (4 regions: East, West, South, Centre)
- **Data Quality:** No missing or null values
- **Calculations:** Revenue = Quantity × Unit Price

**Potential Use Cases:**
- Sales analysis and performance tracking
- Customer analytics and segmentation
- Profitability insights across categories
- Time-series forecasting and trend analysis
- Data visualization and dashboard creation
- Machine learning for demand prediction

## Testing

### Test Coverage
- **27 total tests** across 5 test modules
- **100% pass rate**
- Covers parsing, analysis, output, visualization, and integration

### Test Modules

1. **test_parsers.py** (3 tests)
   - Lazy parsing verification
   - Data type validation
   - Peek functionality

2. **test_analyzers.py** (10 tests)
   - All 8 analysis functions
   - Filter combinations
   - Edge cases

3. **test_output.py** (4 tests)
   - Console formatting (dict, list, trend)
   - Directory creation

4. **test_visualizers.py** (5 tests)
   - Bar, line, pie chart generation
   - File saving
   - Decorator pattern

5. **test_integration.py** (5 tests)
   - End-to-end workflows
   - Multi-analysis pipelines
   - Data file validation

### Running Individual Tests

```bash
# Test specific function
pytest tests/test_analyzers.py::test_revenue_by_category -v

# Test with output
pytest tests/test_output.py -v -s
```

## Functional Programming Patterns

### 1. Lazy Evaluation (Generators)
```python
def parse_csv_stream(filepath: str) -> Iterator[SalesRecord]:
    """Lazy CSV parsing - reads one record at a time"""
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield SalesRecord(...)  # Memory efficient
```

### 2. Higher-Order Functions
```python
def filter_by_predicate(records: Iterator, predicate: Callable) -> Iterator:
    """Takes function as parameter"""
    return filter(predicate, records)

# Usage
high_revenue = filter_by_predicate(records, lambda r: r.revenue > 1000)
```

### 3. Function Composition
```python
# Chain operations
result = (
    parse_csv_stream(file)
    | filter_by_category(category='Electronics')
    | group_by_field('region')
    | sum_by_metric('revenue')
)
```

### 4. Pure Functions
```python
def extract_period(record: SalesRecord, period_type: str) -> str:
    """Deterministic, no side effects"""
    if period_type == 'yearly':
        return record.order_date.strftime('%Y')
    # Always returns same output for same input
```

### 5. Immutability
```python
# namedtuple creates immutable objects
SalesRecord = namedtuple('SalesRecord', ['order_id', 'revenue', ...])

record = SalesRecord(1, 100.0, ...)
record.revenue = 200  # ERROR: AttributeError: immutable
```

### 6. Decorators (Higher-Order Functions)
```python
@with_plot_styling
def plot_bar_chart(data, title):
    """Decorator adds styling automatically"""
    plt.bar(...)
```

## Sample Output

### Console Output (Batch Mode)

```
============================================================
REVENUE BY CATEGORY
============================================================
Electronics                    $42,458,620.90
Home & Furniture               $38,142,975.30
Clothing & Apparel             $26,845,120.45
Accessories                    $12,567,890.20
============================================================

============================================================
TOP 10 CUSTOMERS
============================================================
Rank   Name                           Value
------------------------------------------------------------
1      John Smith                     $125,450.80
2      Sarah Johnson                  $118,920.30
3      Michael Brown                  $112,340.50
...
============================================================

============================================================
REVENUE TRENDS (MONTHLY)
============================================================
Period          Value
------------------------------------------------------------
2023-01         $4,856,230.45
2023-02         $5,123,450.80
2023-03         $5,567,890.20
...
============================================================
```

### Visualizations

Generated charts saved to `output/`:
- `revenue_by_category.png` - Horizontal bar chart
- `revenue_trends_monthly.png` - Line chart with trend
- `profit_by_region.png` - Pie chart
- `top_customers.png` - Horizontal bar chart (top 10)

## Design Choices & Assumptions

### 1. Lazy Evaluation Choice
**Decision:** Use generators for CSV parsing  
**Rationale:** 
- Handles large datasets (200K+ records) efficiently
- Constant memory usage regardless of file size
- Enables streaming pipeline operations

### 2. Immutable Data Structures
**Decision:** Use `namedtuple` for SalesRecord  
**Rationale:**
- Functional programming best practice
- Prevents accidental data mutation
- Hashable (can be used in sets/dict keys)
- Memory efficient vs. classes

### 3. Separate Filter/Aggregator Modules
**Decision:** Modular functional components  
**Rationale:**
- Reusability across multiple analyses
- Composable pipeline building
- Easier testing and maintenance
- Follows single responsibility principle

### 4. Two Execution Modes
**Decision:** Interactive + Batch modes  
**Rationale:**
- Interactive: Data exploration, ad-hoc queries
- Batch: Automated reporting, CI/CD integration
- Flexibility for different use cases

### 5. Optional Visualization
**Decision:** Console-first, optional plots  
**Rationale:**
- Challenge requires console output
- Plots enhance understanding
- User controls when to generate (performance)

## Performance Considerations

- **Streaming:** O(n) single-pass for most analyses
- **Memory:** Constant memory usage with generators
- **Large Files:** Tested with 200K records (~50MB)
- **Optimization:** Lazy evaluation delays computation

## Future Enhancements

- Database integration (PostgreSQL, SQLite)
- Web dashboard (Flask/FastAPI)
- Real-time streaming analytics
- ML-based forecasting
- Export to Excel/PDF reports

## Author & Submission

**Assignment:** Intuit Build Challenge - Assignment 2  
**Language:** Python 3.11  
**Paradigm:** Functional Programming  
**Testing:** pytest (27 tests, 100% pass)  
**Completion Date:** December 2025

---

## Quick Start Commands

```bash
# Setup
pip install -r requirements.txt

# Run Interactive Mode
python src/main.py

# Run Tests
pytest tests/ -v

# Generate Coverage Report
pytest tests/ --cov=src --cov-report=html
```
