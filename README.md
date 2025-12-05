# Intuit Build Challenge: Producer-Consumer & Sales Analytics

Python solutions for two coding challenge assignments demonstrating advanced programming competencies:
1. **Producer-Consumer Pattern** - Thread synchronization and concurrent programming
2. **Sales Analytics** - Functional programming with stream operations and data aggregation

## Repository Structure

```
producer-consumer-and-sales-analytics/
├── assignment1-producer-consumer/     # Concurrency & Thread Synchronization
│   ├── src/                          # Producer, Consumer, SharedQueue implementation
│   ├── tests/                        # 19 unit tests (100% pass)
│   ├── remote/                       # Network-based implementation bonus
│   └── README.md                     # Detailed documentation
│
├── assignment2-sales-analytics/      # Functional Programming & Data Analysis
│   ├── src/                          # Analysis modules, parsers, visualizers
│   ├── tests/                        # 27 unit tests (100% pass)
│   ├── data/                         # 200K sales records CSV
│   ├── output/                       # Generated charts
│   └── README.md                     # Comprehensive documentation
│
└── README.md                         # This file
```

## Assignment Status

| Assignment | Status | Tests | Features |
|------------|--------|-------|----------|
| **Assignment 1** | Complete | 19/19 Pass | Producer-Consumer, Thread Sync, Blocking Queue, Remote Mode |
| **Assignment 2** | Complete | 27/27 Pass | 8 Analyses, Lazy Parsing, Interactive CLI, Visualizations |

## Quick Start

### Assignment 1: Producer-Consumer Pattern

```bash
cd assignment1-producer-consumer

# Run basic demo
python main.py

# Run tests
pytest tests/ -v

# See README for advanced options
```

**Key Features:**
- Thread-safe shared queue with blocking operations
- Configurable capacity and timeout
- Multiple producer/consumer support
- Performance metrics tracking
- Network-based remote implementation

### Assignment 2: Sales Analytics

**Prerequisites:**
1. Download the dataset from [Kaggle - Product Sales Dataset (2023-2024)](https://www.kaggle.com/datasets/yashyennewar/product-sales-dataset-2023-2024)
2. Place the CSV file in `assignment2-sales-analytics/data/` as `product_sales_dataset_final.csv`

```bash
cd assignment2-sales-analytics

# Install dependencies
pip install -r requirements.txt

# Run interactive mode
python src/main.py

# Run batch mode (all analyses)
python src/main.py
# Select option 2

# Run tests
pytest tests/ -v
```

**Key Features:**
- 8 analytical queries with functional programming patterns
- Interactive dashboard with dynamic filtering
- Data visualizations (bar, line, pie charts)
- Lazy CSV parsing (memory efficient)
- Comprehensive unit test coverage
- Analysis of 200,000 synthetic sales records (2023-2024)

## Test Results

### Assignment 1: Producer-Consumer
```
19 passed in 5.77s
- Thread synchronization tests
- Blocking queue operations
- Concurrent execution validation
- Multi-producer/consumer tests
```

### Assignment 2: Sales Analytics
```
27 passed in 92.81s
- All 8 analysis functions
- CSV parsing (lazy evaluation)

## Technologies Used

### Assignment 1: Producer-Consumer Pattern
- **Python 3.11**
- **Threading** (threading.Thread, threading.Lock, threading.Condition)
- **Concurrency** (Blocking queues, wait/notify mechanisms)
- **Socket Programming** (remote implementation)
- **pytest** (testing framework)

**Core Concepts Demonstrated:**
- Thread synchronization with locks
- Blocking queue operations (bounded, thread-safe)
- Wait/Notify mechanism with condition variables
- Concurrent programming patterns
- Network-based distributed processing

### Assignment 2: Sales Analytics
- **Python 3.11**
- **Functional Programming** (generators, lambda, map/filter/reduce)
- **Data Processing** (200K records from Kaggle dataset)
## Documentation

Each assignment includes comprehensive README with:
- Detailed setup instructions
- Architecture and design patterns
- API documentation
- Usage examples with sample output
- Testing guide
- Performance considerations

### Assignment 1: Producer-Consumer Pattern
**README:** [assignment1-producer-consumer/README.md](assignment1-producer-consumer/README.md)

**What It Demonstrates:**
- Thread-safe shared queue implementation
- Producer thread reading from source container
- Consumer thread writing to destination container
- Blocking operations when queue is full/empty
- Wait/notify mechanism for thread coordination
- Performance metrics and monitoring
- Remote/distributed variant using sockets

**Key Sections:**
- Step-by-step execution flow
- Concurrency mechanisms explained
- Sample outputs with timing
- Testing guide (19 tests)
- Performance analysis

### Assignment 2: Sales Analytics  
**README:** [assignment2-sales-analytics/README.md](assignment2-sales-analytics/README.md)

**What It Demonstrates:**
- 8 analytical queries on 200K sales records
- Lazy CSV parsing with generators
- Functional programming patterns
- Interactive CLI dashboard
- Data visualizations (bar, line, pie charts)
- Dynamic filtering capabilities

**Key Sections:**
- Dataset information (Kaggle source)
- All 8 analyses with FP patterns
- Interactive and batch modes
- Functional programming examples
- Testing guide (27 tests)
- Sample outputs and visualizations

## Challenge Objectives Met

### Assignment 1: Producer-Consumer Pattern
- Thread synchronization implemented
- Concurrent programming demonstrated
- Blocking queue operations
- Wait/Notify mechanism
- Comprehensive unit tests
- Code documentation
- Bonus: Remote/network implementation

### Assignment 2: Sales Analytics
- Functional programming patterns
- Stream operations (lazy evaluation)
- Data aggregation (8 analyses)
- Lambda expressions
- CSV data parsing
- Unit tests for all methods
- Console output with formatting
- Documentation of assumptions
- Bonus: Interactive mode + visualizations

## Running All Tests

```bash
# Test both assignments
cd assignment1-producer-consumer
pytest tests/ -v

cd ../assignment2-sales-analytics
pytest tests/ -v
```

**Combined Results:**
- Total Tests: **46**
- Passed: **46/46**
- Coverage: Comprehensive (all core functionality)

## Key Highlights

### Code Quality
- Clean, modular architecture
- Comprehensive documentation
- Extensive test coverage
- Best practices followed
- Type hints and docstrings

### Functional Programming (Assignment 2)
- Generator-based streaming
- Immutable data structures
- Pure functions
- Higher-order functions
- Function composition
- Lazy evaluation

### Concurrency (Assignment 1)
- Thread-safe operations
- Proper synchronization
- Deadlock prevention
- Resource management
- Performance monitoring

## Summary

Both assignments successfully implemented with:
- **46/46 tests passing**
- **Complete documentation**
- **Working demo applications**
- **Clean, maintainable code**
- **Best practices throughout**

