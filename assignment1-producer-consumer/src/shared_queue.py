import threading
import time
import logging
from collections import deque

logger = logging.getLogger(__name__)

class SharedQueue:
    """Thread-safe bounded blocking queue with logging and metrics

    Demonstrates:
    - Thread synchronization using Lock
    - Blocking queue behavior
    - Wait/Notify mechanism using Condition variables
    - Concurrent programming patterns
    """

    def __init__(self, max_size=10):
        """Initialize bounded blocking queue

        Args:
            max_size: Maximum number of items queue can hold
        """
        self._queue = deque()  # Use deque for O(1) popleft instead of O(n) pop(0)
        self._max_size = max_size
        self._lock = threading.Lock()  # For mutual exclusion
        self._not_empty = threading.Condition(self._lock)  # Consumer waits on this
        self._not_full = threading.Condition(self._lock)   # Producer waits on this

        # Performance metrics
        self._total_puts = 0
        self._total_gets = 0
        self._producer_waits = 0
        self._consumer_waits = 0
        self._total_producer_wait_time = 0.0
        self._total_consumer_wait_time = 0.0

    def put(self, item):
        """Add item to queue, block if full

        Demonstrates:
        - Lock acquisition for thread safety
        - Wait/notify mechanism when queue is full
        - Blocking behavior

        Edge Cases:
        - Spurious wakeups: while loop re-checks queue full condition
        - Multiple threads: notify() wakes only one waiting producer

        Args:
            item: Item to add to queue
        """
        thread_name = threading.current_thread().name
        logger.info(f"[{thread_name}] Attempting PUT: {item}")

        with self._lock:  # Acquire lock for thread safety
            wait_start = None

            # Block while queue is full (use while for spurious wakeups)
            while len(self._queue) >= self._max_size:
                if wait_start is None:
                    logger.warning(f"[{thread_name}] Queue FULL ({len(self._queue)}/{self._max_size}), waiting...")
                    self._producer_waits += 1
                    wait_start = time.time()

                # Wait releases lock and blocks until notified
                self._not_full.wait()

            # Record wait time if we waited
            if wait_start:
                wait_time = time.time() - wait_start
                self._total_producer_wait_time += wait_time
                logger.info(f"[{thread_name}] Wait completed ({wait_time:.3f}s)")

            # Add item to queue
            self._queue.append(item)
            self._total_puts += 1
            logger.info(f"[{thread_name}] PUT success: {item}, size={len(self._queue)}/{self._max_size}")

            # Notify one waiting consumer
            self._not_empty.notify()

    def get(self):
        """Remove and return item, block if empty

        Demonstrates:
        - Lock acquisition for thread safety
        - Wait/notify mechanism when queue is empty
        - Blocking behavior

        Edge Cases:
        - Spurious wakeups: while loop re-checks queue empty condition
        - Multiple threads: notify() wakes only one waiting consumer

        Returns:
            Item from queue
        """
        thread_name = threading.current_thread().name
        logger.info(f"[{thread_name}] Attempting GET")

        with self._lock:  # Acquire lock for thread safety
            wait_start = None

            # Block while queue is empty (use while for spurious wakeups)
            while len(self._queue) == 0:
                if wait_start is None:
                    logger.warning(f"[{thread_name}] Queue EMPTY, waiting...")
                    self._consumer_waits += 1
                    wait_start = time.time()

                # Wait releases lock and blocks until notified
                self._not_empty.wait()

            # Record wait time if we waited
            if wait_start:
                wait_time = time.time() - wait_start
                self._total_consumer_wait_time += wait_time
                logger.info(f"[{thread_name}] Wait completed ({wait_time:.3f}s)")

            # Remove item from queue (O(1) operation with deque)
            item = self._queue.popleft()
            self._total_gets += 1
            logger.info(f"[{thread_name}] GET success: {item}, size={len(self._queue)}/{self._max_size}")

            # Notify one waiting producer
            self._not_full.notify()

            return item

    def get_metrics(self):
        """Return performance metrics

        Returns:
            dict: Metrics including total operations, wait events, and average wait times
        """
        with self._lock:
            return {
                'total_puts': self._total_puts,
                'total_gets': self._total_gets,
                'producer_waits': self._producer_waits,
                'consumer_waits': self._consumer_waits,
                'avg_producer_wait': (
                    self._total_producer_wait_time / self._producer_waits
                    if self._producer_waits > 0 else 0
                ),
                'avg_consumer_wait': (
                    self._total_consumer_wait_time / self._consumer_waits
                    if self._consumer_waits > 0 else 0
                )
            }

    def pretty_print_metrics(self):
        """Pretty print performance metrics

        Returns formatted string with all metrics for easy display
        """
        metrics = self.get_metrics()
        lines = [
            "=" * 60,
            "PERFORMANCE METRICS",
            "=" * 60,
            f"Total queue puts:         {metrics['total_puts']}",
            f"Total queue gets:         {metrics['total_gets']}",
            f"Producer wait events:     {metrics['producer_waits']}",
            f"Consumer wait events:     {metrics['consumer_waits']}",
            f"Avg producer wait time:   {metrics['avg_producer_wait']:.3f}s",
            f"Avg consumer wait time:   {metrics['avg_consumer_wait']:.3f}s"
        ]
        return "\n".join(lines)

    def size(self):
        """Return current queue size

        Returns:
            int: Number of items in queue
        """
        with self._lock:
            return len(self._queue)
