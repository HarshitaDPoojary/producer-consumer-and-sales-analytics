# Assignment 1: Producer-Consumer Pattern

## Overview
Implement a classic producer-consumer pattern demonstrating thread synchronization and communication.

## Requirements
- **Languages**: Python 3.11+

## Description
The program simulates concurrent data transfer between:
- A **producer thread** that reads from a source container and places items into a shared queue
- A **consumer thread** that reads from the queue and stores items in a destination container

## Testing Objectives
- Thread synchronization (Lock mechanism)
- Concurrent programming (Threading)
- Blocking queues (Bounded queue with blocking put/get)
- Wait/Notify mechanism (Condition variables)

---

## Setup Instructions

### 1. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Quick Start

### Option 1: Basic Demo (Default Settings)
```bash
python src/main.py
```

### Option 2: Command-Line Arguments
```bash
# Custom configuration
python run_with_args.py --queue-size 15 --producers 3 --consumers 2 --items 50

# Short form
python run_with_args.py -q 15 -p 3 -c 2 -i 50

# See all options
python run_with_args.py --help
```

### Option 3: Multi-Terminal (Socket-Based)
```bash
# Terminal 1: Start server
python remote/queue_server.py --queue-size 10

# Terminal 2: Add producer
python remote/remote_producer.py --items 50 --name Producer-1

# Terminal 3: Add consumer
python remote/remote_consumer.py --items 50 --name Consumer-1
```

---

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

Expected: **19 tests PASSED in ~6 seconds**

### Run Specific Test Categories
```bash
pytest tests/test_shared_queue.py -v  # Queue tests (6 tests)
pytest tests/test_producer.py -v      # Producer tests (4 tests)
pytest tests/test_consumer.py -v      # Consumer tests (4 tests)
pytest tests/test_integration.py -v   # Integration tests (5 tests)
```

---

## Available Scripts

### 1. `run_with_args.py` - Command-Line Interface
Run with custom parameters:

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--queue-size` | `-q` | 10 | Queue capacity |
| `--producers` | `-p` | 1 | Number of producers |
| `--consumers` | `-c` | 1 | Number of consumers |
| `--items` | `-i` | 100 | Items per producer |
| `--verbose` | `-v` | False | Show detailed logs |

**Examples:**
```bash
# Small queue (more blocking)
python run_with_args.py -q 5 -i 100

# Many producers
python run_with_args.py -p 5 -c 2 -q 20

# With detailed logs
python run_with_args.py -p 2 -c 2 --verbose
```

### 2. Socket-Based (Multi-Terminal)

**Server:**
```bash
python remote/queue_server.py --queue-size 10
```

**Producer Client:**
```bash
python remote/remote_producer.py --items 50 --name Producer-1 --delay 0.01
```

**Consumer Client:**
```bash
python remote/remote_consumer.py --items 50 --name Consumer-1 --delay 0.015
```

### 3. Other Examples

**Multiple Producers/Consumers:**
```bash
python examples/multi_producer_consumer.py
```

**Test Different Queue Sizes:**
```bash
python examples/test_queue_sizes.py
```

**Custom Scenarios:**
```bash
python examples/custom_config.py
```

---

## Project Structure

```
assignment1-producer-consumer/
├── README.md                      # This file - Complete documentation
├── requirements.txt               # Python dependencies (pytest)
├── run_with_args.py              # CLI with custom parameters
│
├── src/                          # Core implementation
│   ├── __init__.py               # Package marker
│   ├── shared_queue.py           # Thread-safe bounded blocking queue
│   ├── producer.py               # Producer thread class
│   ├── consumer.py               # Consumer thread class
│   └── main.py                   # Basic demonstration program
│
├── tests/                        # Unit and integration tests (19 tests)
│   ├── __init__.py               # Package marker
│   ├── test_shared_queue.py     # Queue tests (6)
│   ├── test_producer.py         # Producer tests (4)
│   ├── test_consumer.py         # Consumer tests (4)
│   └── test_integration.py      # Integration tests (5)
│
├── remote/                       # Socket-based multi-terminal
│   ├── queue_server.py           # Server hosting shared queue
│   ├── remote_producer.py        # Producer client
│   └── remote_consumer.py        # Consumer client
│
└── examples/                     # Additional examples
    ├── multi_producer_consumer.py  # 3 producers + 3 consumers
    ├── test_queue_sizes.py         # Compare different queue sizes
    └── custom_config.py            # Multiple test scenarios
```

### File Descriptions

#### Core Implementation (`src/`)

**`shared_queue.py`** - Thread-safe bounded blocking queue implementation
- Implements `SharedQueue` class with Lock and Condition variables
- Provides `put()` method that blocks when queue is full
- Provides `get()` method that blocks when queue is empty
- Tracks performance metrics (wait times, wait events)
- Uses `collections.deque` for O(1) operations
- Demonstrates: Thread synchronization, blocking queues, wait/notify mechanism

**`producer.py`** - Producer thread implementation
- Extends `threading.Thread` class
- Reads items from source list and adds to shared queue
- Simulates work with configurable delay
- Tracks number of items produced
- Demonstrates: Concurrent programming, thread lifecycle

**`consumer.py`** - Consumer thread implementation
- Extends `threading.Thread` class
- Retrieves items from shared queue and stores in destination list
- Simulates work with configurable delay
- Tracks number of items consumed
- Thread-safe writes to shared destination
- Demonstrates: Concurrent programming, thread synchronization

**`main.py`** - Basic demonstration program
- Creates queue, producer, and consumer with default settings
- Demonstrates producer-consumer pattern with 100 items
- Displays verification results and performance metrics
- Shows blocking behavior and wait statistics
- Entry point for basic demo: `python src/main.py`

#### Command-Line Interface

**`run_with_args.py`** - Customizable CLI for running simulations
- Accepts command-line arguments for all parameters
- Options: queue size, number of producers/consumers, items count
- Verbose mode for detailed logging
- Performance analysis and metrics display
- Validates inputs and provides helpful error messages
- Usage: `python run_with_args.py -q 10 -p 3 -c 2 -i 50`

#### Testing Suite (`tests/`)

**`test_shared_queue.py`** - Unit tests for SharedQueue (6 tests)
- Tests basic put/get operations
- Tests blocking when queue is full
- Tests blocking when queue is empty
- Tests thread safety with concurrent access
- Tests queue size tracking
- Tests metrics tracking accuracy

**`test_producer.py`** - Unit tests for Producer (4 tests)
- Tests producer produces all items
- Tests with large datasets
- Tests thread naming
- Tests with empty source

**`test_consumer.py`** - Unit tests for Consumer (4 tests)
- Tests consumer consumes all items
- Tests thread-safe writes with multiple consumers
- Tests thread naming
- Tests with mixed data types

**`test_integration.py`** - Integration tests (5 tests)
- Tests full producer-consumer workflow
- Tests multiple producers and consumers
- Tests concurrent execution (not sequential)
- Tests blocking behavior occurs
- Tests data order preservation (FIFO)

#### Socket-Based Multi-Terminal (`remote/`)

**`queue_server.py`** - Central server hosting shared queue
- Listens on configurable host/port (default: localhost:5555)
- Accepts connections from producer and consumer clients
- Maintains single shared queue for all clients
- Handles multiple concurrent client connections
- Displays real-time statistics every 5 seconds
- Tracks active producers/consumers
- Usage: `python remote/queue_server.py --queue-size 10`

**`remote_producer.py`** - Producer client for socket-based mode
- Connects to queue server via socket
- Produces configurable number of items
- Sends items to remote queue via network
- Configurable production rate (delay parameter)
- Independent execution in separate terminal
- Usage: `python remote/remote_producer.py --items 50 --name Producer-1`

**`remote_consumer.py`** - Consumer client for socket-based mode
- Connects to queue server via socket
- Consumes configurable number of items
- Retrieves items from remote queue via network
- Configurable consumption rate (delay parameter)
- Independent execution in separate terminal
- Usage: `python remote/remote_consumer.py --items 50 --name Consumer-1`

#### Examples and Utilities (`examples/`)

**`multi_producer_consumer.py`** - Multiple producers and consumers example
- Demonstrates 3 producers and 3 consumers working simultaneously
- Each producer generates 50 items (150 total)
- Each consumer processes 50 items
- Shows coordination with multiple threads
- Displays detailed statistics for each thread
- Usage: `python examples/multi_producer_consumer.py`

**`test_queue_sizes.py`** - Queue size comparison utility
- Tests with different queue sizes (5, 10, 20, 50, 100)
- Measures execution time for each configuration
- Counts producer/consumer wait events
- Displays results in tabular format
- Helps understand relationship between queue size and blocking
- Usage: `python examples/test_queue_sizes.py`

**`custom_config.py`** - Multiple scenario runner
- Runs 5 different predefined scenarios automatically
- Example 1: Balanced configuration (2P, 2C)
- Example 2: More producers (4P, 2C)
- Example 3: More consumers (2P, 4C)
- Example 4: Small queue (forces blocking)
- Example 5: Large queue (minimal blocking)
- Compares performance across scenarios
- Usage: `python examples/custom_config.py`

---

## Key Implementation Details

### 1. Thread Synchronization
- Uses `threading.Lock` for mutual exclusion
- Protects critical sections (queue operations)
- Prevents race conditions
- **File:** [src/shared_queue.py](src/shared_queue.py)

### 2. Blocking Queue
- Bounded queue with configurable `max_size`
- `put()` blocks when queue is full
- `get()` blocks when queue is empty
- Uses `collections.deque` for O(1) operations
- **File:** [src/shared_queue.py](src/shared_queue.py)

### 3. Wait/Notify Mechanism
- Uses `threading.Condition` variables
- `_not_full`: Producer waits when queue is full
- `_not_empty`: Consumer waits when queue is empty
- `notify()` wakes one waiting thread
- Handles spurious wakeups with `while` loops
- **File:** [src/shared_queue.py](src/shared_queue.py)

### 4. Concurrent Programming
- Producer and Consumer extend `threading.Thread`
- Threads run in parallel, not sequentially
- Proper thread lifecycle: `start()` → `run()` → `join()`
- **Files:** [src/producer.py](src/producer.py), [src/consumer.py](src/consumer.py)

---

## Performance Metrics

The implementation tracks:
- **Total puts**: Number of items added to queue
- **Total gets**: Number of items removed from queue
- **Producer wait events**: Number of times producer blocked
- **Consumer wait events**: Number of times consumer blocked
- **Average wait times**: Time spent waiting

**Interpreting Results:**
- `Producer waits > 0, Consumer waits = 0`: Producers blocking (queue too small or slow consumers)
- `Producer waits = 0, Consumer waits > 0`: Consumers blocking (slow producers)
- `Both = 0`: No blocking (queue large enough)

---

## Examples

### Example 1: Force Blocking
```bash
python run_with_args.py --queue-size 3 --items 100
```
Small queue forces frequent blocking.

### Example 2: Many Producers
```bash
python run_with_args.py -p 5 -c 2 -q 20 -i 30
```
5 producers compete for queue space.

### Example 3: Multi-Terminal Demo
```bash
# Terminal 1
python remote/queue_server.py

# Terminal 2
python remote/remote_producer.py --items 30 --name FastProducer --delay 0.005

# Terminal 3
python remote/remote_consumer.py --items 30 --name SlowConsumer --delay 0.02
```
Producer faster than consumer → queue fills up!

---

## Troubleshooting

### Issue: Tests hang or timeout
**Cause:** Queue size too small for items being added without consumers running.

**Solution:** Ensure `max_size` ≥ number of items when pre-populating queue, OR start consumers before filling.

### Issue: No blocking behavior
**Cause:** Queue size too large relative to items.

**Solution:** Use smaller queue (e.g., `max_size=5`) with many items (e.g., 100).

### Issue: "Could not connect to server" (Socket mode)
**Cause:** Queue server not running.

**Solution:** Start `queue_server.py` first before starting clients.

---

## Sample Output

### Command-Line Arguments Example

Running this command:
```bash
python run_with_args.py -q 15 -p 3 -c 2 -i 50
```

Produces this output:
```
======================================================================
PRODUCER-CONSUMER SIMULATION
======================================================================

Configuration:
  Queue size:          15
  Producers:           3
  Consumers:           2
  Items per producer:  50
  Total items:         150

Starting simulation...

Producer-1 finished: produced 50 items
Producer-2 finished: produced 50 items
Producer-3 finished: produced 50 items
Consumer-1 finished: consumed 75 items
Consumer-2 finished: consumed 75 items

======================================================================
RESULTS
======================================================================

Performance:
  Execution time:      1.158s
  Throughput:          129.6 items/sec
  Producer waits:      123
  Consumer waits:      0

Verification:
  Expected:            150 items
  Actual:              150 items
  Status:              PASS

  Note: Producers blocked 123 times (queue too small or consumers too slow)
======================================================================
```

### Basic Demo Example

Running this command:
```bash
python src/main.py
```

Produces output similar to:
```
============================================================
PRODUCER-CONSUMER PATTERN DEMONSTRATION
============================================================

Starting producer and consumer threads...
Queue max size: 10
Items to transfer: 100

Producer-1 finished: produced 100 items
Consumer-1 finished: consumed 100 items

============================================================
VERIFICATION
============================================================
Items produced:   100
Items consumed:   100
Destination size: 100
Data integrity:   [PASS]

============================================================
PERFORMANCE METRICS
============================================================
Total execution time:     1.234s
Total queue puts:         100
Total queue gets:         100
Producer wait events:     45
Consumer wait events:     0
Avg producer wait time:   0.012s
Avg consumer wait time:   0.000s

[PASS] Blocking behavior demonstrated (threads waited)
============================================================
```

### Test Suite Example

Running this command:
```bash
pytest tests/ -v
```

Produces output like:
```
tests/test_consumer.py::test_consumer_consumes_all_items PASSED
tests/test_consumer.py::test_consumer_thread_safe_writes PASSED
tests/test_consumer.py::test_consumer_thread_naming PASSED
tests/test_consumer.py::test_consumer_with_mixed_types PASSED
tests/test_integration.py::test_full_producer_consumer_workflow PASSED
tests/test_integration.py::test_multiple_producers_and_consumers PASSED
tests/test_integration.py::test_concurrent_execution PASSED
tests/test_integration.py::test_blocking_behavior_occurs PASSED
tests/test_integration.py::test_data_order_preserved PASSED
tests/test_producer.py::test_producer_produces_all_items PASSED
tests/test_producer.py::test_producer_with_large_dataset PASSED
tests/test_producer.py::test_producer_thread_naming PASSED
tests/test_producer.py::test_producer_with_empty_source PASSED
tests/test_shared_queue.py::test_queue_put_and_get PASSED
tests/test_shared_queue.py::test_queue_blocking_when_full PASSED
tests/test_shared_queue.py::test_queue_blocking_when_empty PASSED
tests/test_shared_queue.py::test_thread_safety PASSED
tests/test_shared_queue.py::test_queue_size_tracking PASSED
tests/test_shared_queue.py::test_metrics_tracking PASSED

===================== 19 passed in 5.76s ======================
```

---

## Deliverables

- Complete source code with all components
- Thread-safe SharedQueue with Lock and Condition variables
- Producer and Consumer thread classes
- 19 comprehensive unit tests (all passing)
- Sample output demonstrating concurrent execution
- Performance metrics and logging
- Code documentation with docstrings and comments
- Command-line interface for custom configurations
- Socket-based multi-terminal demonstration

---

## What This Demonstrates

Every execution shows all 4 key mechanisms:

1. **Thread Synchronization** - Locks protect shared queue
2. **Blocking Queues** - `put()` blocks when full, `get()` blocks when empty
3. **Wait/Notify Mechanism** - Threads coordinate via condition variables
4. **Concurrent Programming** - Multiple threads run in parallel

---

## Quick Reference

**Basic demo:**
```bash
python src/main.py
```

**Custom configuration:**
```bash
python run_with_args.py -q 10 -p 3 -c 2 -i 50
```

**Run tests:**
```bash
pytest tests/ -v
```

**Multi-terminal setup:**
```bash
# Terminal 1
python remote/queue_server.py

# Terminal 2
python remote/remote_producer.py

# Terminal 3
python remote/remote_consumer.py
```

**See all options:**
```bash
python run_with_args.py --help
```

**Force blocking:**
```bash
python run_with_args.py -q 3 -i 100
```

**Verbose logs:**
```bash
python run_with_args.py --verbose
```
