# Assignment 1: Producer-Consumer Pattern

## Table of Contents
1. [Overview](#overview)
2. [What This Project Demonstrates](#what-this-project-demonstrates)
3. [How It Works](#how-it-works)
4. [Project Structure](#project-structure)
5. [Setup Instructions](#setup-instructions)
6. [How to Run](#how-to-run)
7. [Sample Outputs](#sample-outputs)
8. [Testing](#testing)
9. [Performance Metrics](#performance-metrics)
10. [Troubleshooting](#troubleshooting)

---

## Overview

This project implements a **classic producer-consumer pattern** in Python demonstrating thread synchronization and communication.

**Requirements:**
- Python 3.11+
- pytest (for testing)

**The Problem:**
Transfer data concurrently from a source container to a destination container using:
- A **producer thread** that reads from source and places items into a shared queue
- A **consumer thread** that reads from the queue and stores items in destination

---

## What This Project Demonstrates

Every execution demonstrates all 4 key concurrency mechanisms:

### 1. Thread Synchronization
- Uses `threading.Lock` for mutual exclusion
- Protects critical sections (queue operations)
- Prevents race conditions
- **Implementation:** [src/shared_queue.py](src/shared_queue.py)

### 2. Blocking Queues
- Bounded queue with configurable `max_size`
- `put()` blocks when queue is full
- `get()` blocks when queue is empty
- Uses `collections.deque` for O(1) operations
- **Implementation:** [src/shared_queue.py](src/shared_queue.py)

### 3. Wait/Notify Mechanism
- Uses `threading.Condition` variables
- `_not_full`: Producer waits when queue is full
- `_not_empty`: Consumer waits when queue is empty
- `notify()` wakes one waiting thread
- Handles spurious wakeups with `while` loops
- **Implementation:** [src/shared_queue.py](src/shared_queue.py)

### 4. Concurrent Programming
- Producer and Consumer extend `threading.Thread`
- Threads run in parallel, not sequentially
- Proper thread lifecycle: `start()` → `run()` → `join()`
- **Implementation:** [src/producer.py](src/producer.py), [src/consumer.py](src/consumer.py)


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

## Setup Instructions

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pytest` - For running unit tests

---

## How to Run

### Option 1: Basic Demo (Default Settings)

**Command:**
```bash
python src/main.py
```

**What it does:**
- Creates queue with size 10
- 1 producer, 1 consumer
- Transfers 100 items
- Shows verification and performance metrics

**Use this for:**
- Quick demonstration
- Understanding basic behavior
- Seeing default configuration

---

### Option 2: Command-Line Arguments (Custom Configuration)

**Command:**
```bash
python run_with_args.py --queue-size 15 --producers 3 --consumers 2 --items 50
```

**Short form:**
```bash
python run_with_args.py -q 15 -p 3 -c 2 -i 50
```

**Available Options:**

| Option | Short | Default | Description |
|--------|-------|---------|-------------|
| `--queue-size` | `-q` | 10 | Queue capacity |
| `--producers` | `-p` | 1 | Number of producers |
| `--consumers` | `-c` | 1 | Number of consumers |
| `--items` | `-i` | 100 | Items per producer |
| `--verbose` | `-v` | False | Show detailed logs |

**Common Examples:**

**Force blocking (small queue):**
```bash
python run_with_args.py -q 3 -i 100
```
Small queue forces frequent producer blocking.

**Many producers:**
```bash
python run_with_args.py -p 5 -c 2 -q 20 -i 30
```
5 producers compete for queue space.

**Verbose logging:**
```bash
python run_with_args.py -p 2 -c 2 --verbose
```
Shows detailed thread-level logs of every put/get operation.

**See all options:**
```bash
python run_with_args.py --help
```

**Use this for:**
- Testing different configurations
- Understanding how queue size affects blocking
- Experimenting with multiple producers/consumers

---

### Option 3: Multi-Terminal (Socket-Based)

This mode lets you run producers and consumers in **separate terminal windows**, demonstrating distributed coordination.

**Step 1: Start the server (Terminal 1)**
```bash
python remote/queue_server.py --queue-size 10
```
Server starts and waits for producer/consumer clients.

**Step 2: Add producer (Terminal 2)**
```bash
python remote/remote_producer.py --items 50 --name Producer-1 --delay 0.01
```
Producer connects and starts producing items.

**Step 3: Add consumer (Terminal 3)**
```bash
python remote/remote_consumer.py --items 50 --name Consumer-1 --delay 0.015
```
Consumer connects and starts consuming items.

**Advanced Example (Fast Producer, Slow Consumer):**

Terminal 1:
```bash
python remote/queue_server.py
```

Terminal 2:
```bash
python remote/remote_producer.py --items 30 --name FastProducer --delay 0.005
```

Terminal 3:
```bash
python remote/remote_consumer.py --items 30 --name SlowConsumer --delay 0.02
```
Producer is faster → queue fills up and blocks!

**Use this for:**
- Visual demonstration of distributed systems
- Understanding network-based coordination
- Demonstrating blocking with different production/consumption rates

---

### Option 4: Example Scripts

**Multiple producers and consumers:**
```bash
python examples/multi_producer_consumer.py
```
Runs 3 producers + 3 consumers simultaneously.

**Test different queue sizes:**
```bash
python examples/test_queue_sizes.py
```
Compares performance with queue sizes: 5, 10, 20, 50, 100.

**Custom scenarios:**
```bash
python examples/custom_config.py
```
Runs 5 predefined scenarios with different configurations.

---

## Sample Outputs

### Output 1: Command-Line Arguments Example

**Command:**
```bash
python run_with_args.py -q 15 -p 3 -c 2 -i 50
```

**Output:**
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

**Interpretation:**
- 3 producers created 150 items total (50 each)
- 2 consumers consumed 75 items each
- Producers blocked 123 times (queue filled up frequently)
- Consumers never blocked (producers kept queue populated)
- All items transferred successfully

---

### Output 2: Basic Demo Example

**Command:**
```bash
python src/main.py
```

**Output:**
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

**Interpretation:**
- Single producer created 100 items
- Single consumer consumed all 100 items
- Producer blocked 45 times (small queue size of 10)
- Consumer never blocked (producer kept up)
- Data integrity verified: all items transferred

---

### Output 3: Test Suite Example

**Command:**
```bash
pytest tests/ -v
```

**Output:**
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

**Interpretation:**
- All 19 unit and integration tests passed
- Tests cover: queue operations, producer behavior, consumer behavior, integration
- Execution time: ~6 seconds

---

### Output 4: Verbose Logging Example

**Command:**
```bash
python run_with_args.py -q 5 -p 1 -c 1 -i 20 --verbose
```

**Output (partial):**
```
12:34:56 [Producer-1 ] INFO     Attempting PUT: Item-0
12:34:56 [Producer-1 ] INFO     PUT success: Item-0, size=1/5
12:34:56 [Producer-1 ] INFO     Attempting PUT: Item-1
12:34:56 [Producer-1 ] INFO     PUT success: Item-1, size=2/5
12:34:56 [Consumer-1 ] INFO     Attempting GET
12:34:56 [Consumer-1 ] INFO     GET success: Item-0, size=1/5
12:34:56 [Producer-1 ] INFO     Attempting PUT: Item-2
12:34:56 [Producer-1 ] INFO     PUT success: Item-2, size=2/5
12:34:56 [Producer-1 ] INFO     Attempting PUT: Item-3
12:34:56 [Producer-1 ] INFO     PUT success: Item-3, size=3/5
12:34:56 [Producer-1 ] INFO     Attempting PUT: Item-4
12:34:56 [Producer-1 ] INFO     PUT success: Item-4, size=4/5
12:34:56 [Producer-1 ] INFO     Attempting PUT: Item-5
12:34:56 [Producer-1 ] INFO     PUT success: Item-5, size=5/5
12:34:56 [Producer-1 ] WARNING  Queue FULL (5/5), waiting...
12:34:57 [Consumer-1 ] INFO     GET success: Item-1, size=4/5
12:34:57 [Producer-1 ] INFO     Wait completed (0.015s)
12:34:57 [Producer-1 ] INFO     PUT success: Item-6, size=5/5
...
```

**Interpretation:**
- Detailed logs show every put/get operation
- Timestamps show concurrent execution
- See exact moments when blocking occurs
- Useful for debugging and understanding flow

---

### Output 5: Multi-Terminal Example

**Terminal 1 (Server):**
```bash
$ python remote/queue_server.py

Queue Server Started
Host: localhost
Port: 5555
Queue Size: 10

Waiting for clients...

[12:34:56] Producer-1 connected
[12:34:58] Consumer-1 connected

--- Statistics (t=5s) ---
Queue size: 7/10
Active producers: 1
Active consumers: 1
Total puts: 45
Total gets: 38
```

**Terminal 2 (Producer):**
```bash
$ python remote/remote_producer.py --items 50 --name Producer-1

Connecting to queue server at localhost:5555...
Connected successfully!

Producer-1 starting (50 items)...

Producer-1 finished: produced 50 items
```

**Terminal 3 (Consumer):**
```bash
$ python remote/remote_consumer.py --items 50 --name Consumer-1

Connecting to queue server at localhost:5555...
Connected successfully!

Consumer-1 starting (50 items)...

Consumer-1 finished: consumed 50 items
```

**Interpretation:**
- Server coordinates all clients
- Real-time statistics show queue state
- Producers and consumers run independently
- Demonstrates distributed coordination

---

## Testing

### Run All Tests

**Command:**
```bash
pytest tests/ -v
```

**Expected:** 19 tests PASSED in ~6 seconds

### Run Specific Test Categories

**Queue tests only (6 tests):**
```bash
pytest tests/test_shared_queue.py -v
```

**Producer tests only (4 tests):**
```bash
pytest tests/test_producer.py -v
```

**Consumer tests only (4 tests):**
```bash
pytest tests/test_consumer.py -v
```

**Integration tests only (5 tests):**
```bash
pytest tests/test_integration.py -v
```

### What Tests Cover

**SharedQueue Tests:**
- Basic put/get operations
- Blocking when queue is full
- Blocking when queue is empty
- Thread safety with concurrent access
- Queue size tracking
- Metrics tracking accuracy

**Producer Tests:**
- Produces all source items
- Handles large datasets
- Thread naming correctness
- Handles empty source

**Consumer Tests:**
- Consumes all items
- Thread-safe writes with multiple consumers
- Thread naming correctness
- Handles mixed data types

**Integration Tests:**
- Full end-to-end workflow
- Multiple producers and consumers
- Concurrent execution (not sequential)
- Blocking behavior occurs
- Data order preserved (FIFO)

---

## Performance Metrics

The implementation tracks and displays:

### Metrics Tracked

- **Total puts**: Number of items added to queue
- **Total gets**: Number of items removed from queue
- **Producer wait events**: Number of times producer blocked (queue full)
- **Consumer wait events**: Number of times consumer blocked (queue empty)
- **Average wait times**: Time spent waiting (seconds)
- **Execution time**: Total time from start to finish
- **Throughput**: Items processed per second

### Interpreting Results

**Scenario 1: Producer waits > 0, Consumer waits = 0**
```
Producer wait events:     123
Consumer wait events:     0
```
**Meaning:** Producers blocking frequently
**Causes:**
- Queue too small
- Consumers too slow
- Too many producers

**Scenario 2: Producer waits = 0, Consumer waits > 0**
```
Producer wait events:     0
Consumer wait events:     87
```
**Meaning:** Consumers blocking frequently
**Causes:**
- Producers too slow
- Too many consumers
- Not enough data

**Scenario 3: Both = 0**
```
Producer wait events:     0
Consumer wait events:     0
```
**Meaning:** No blocking occurred
**Causes:**
- Queue large enough to hold all items
- Perfect balance between production/consumption
- May not demonstrate blocking behavior

**Scenario 4: Both > 0**
```
Producer wait events:     45
Consumer wait events:     38
```
**Meaning:** Dynamic balance, both blocking at different times
**This is ideal** - demonstrates full wait/notify mechanism

---

## Troubleshooting

### Issue: Tests hang or timeout

**Symptoms:**
- Test runs indefinitely
- No output after several seconds
- Process must be killed manually

**Cause:**
Queue size too small for items being added without consumers running.

**Solution:**
Ensure `max_size` ≥ number of items when pre-populating queue, OR start consumers before filling.

**Example:**
```python
# BAD: Will hang
queue = SharedQueue(max_size=10)
for i in range(100):  # Trying to add 100 items to size-10 queue
    queue.put(i)      # Blocks at item 11 with no consumer

# GOOD: Use larger queue or start consumer first
queue = SharedQueue(max_size=100)  # Can hold all items
for i in range(100):
    queue.put(i)
```

---

### Issue: No blocking behavior

**Symptoms:**
```
Producer wait events:     0
Consumer wait events:     0
```

**Cause:**
Queue size too large relative to items.

**Solution:**
Use smaller queue (e.g., `max_size=5`) with many items (e.g., 100).

**Example:**
```bash
# Force blocking
python run_with_args.py -q 3 -i 100
```

---

### Issue: "Could not connect to server" (Socket mode)

**Symptoms:**
```
Connecting to queue server at localhost:5555...
Error: [Errno 111] Connection refused
```

**Cause:**
Queue server not running.

**Solution:**
Start `queue_server.py` first before starting clients.

**Correct order:**
```bash
# Terminal 1 - Start this FIRST
python remote/queue_server.py

# Terminal 2 - Then start producer
python remote/remote_producer.py

# Terminal 3 - Then start consumer
python remote/remote_consumer.py
```

---

## Deliverables

This project includes:

- Complete source code with all components
- Thread-safe SharedQueue with Lock and Condition variables
- Producer and Consumer thread classes
- 19 comprehensive unit tests (all passing)
- Sample output demonstrating concurrent execution
- Performance metrics and logging
- Code documentation with docstrings and comments
- Command-line interface for custom configurations
- Socket-based multi-terminal demonstration
- Comprehensive README with step-by-step instructions

---

## Quick Reference Card

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

**Force blocking:**
```bash
python run_with_args.py -q 3 -i 100
```

**Verbose logs:**
```bash
python run_with_args.py --verbose
```

**See all options:**
```bash
python run_with_args.py --help
```
