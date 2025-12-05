"""
Queue Size Comparison Utility

Tests with different queue sizes (5, 10, 20, 50, 100) to understand
the relationship between queue size and blocking behavior.

Usage:
    python examples/test_queue_sizes.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.shared_queue import SharedQueue
from src.producer import Producer
from src.consumer import Consumer


def run_test(queue_size, num_items=100, num_producers=2, num_consumers=2):
    """Run a test with specified queue size"""

    # Create shared queue
    queue = SharedQueue(max_size=queue_size)

    # Create producers
    producers = []
    items_per_producer = num_items // num_producers

    for i in range(num_producers):
        source_data = [f"Item-{i*items_per_producer + j}" for j in range(items_per_producer)]
        producer = Producer(
            queue=queue,
            source_data=source_data,
            name=f"Producer-{i+1}"
        )
        producers.append(producer)

    # Create consumers
    destination = []
    consumers = []
    items_per_consumer = num_items // num_consumers

    for i in range(num_consumers):
        consumer = Consumer(
            queue=queue,
            destination=destination,
            num_items=items_per_consumer,
            name=f"Consumer-{i+1}"
        )
        consumers.append(consumer)

    # Start timing
    start_time = time.time()

    # Start all threads
    for producer in producers:
        producer.start()
    for consumer in consumers:
        consumer.start()

    # Wait for completion
    for producer in producers:
        producer.join()
    for consumer in consumers:
        consumer.join()

    total_time = time.time() - start_time

    # Get metrics
    metrics = queue.get_metrics()

    return {
        'queue_size': queue_size,
        'time': total_time,
        'producer_waits': metrics['producer_waits'],
        'consumer_waits': metrics['consumer_waits'],
        'total_puts': metrics['total_puts'],
        'total_gets': metrics['total_gets'],
        'items_verified': len(destination) == num_items
    }


def main():
    print("="*80)
    print("QUEUE SIZE COMPARISON TEST")
    print("="*80)
    print()
    print("Configuration:")
    print("  Producers:     2")
    print("  Consumers:     2")
    print("  Total items:   100")
    print("  Test purpose:  Compare blocking behavior with different queue sizes")
    print()
    print("="*80)
    print()

    # Test different queue sizes
    queue_sizes = [5, 10, 20, 50, 100]
    results = []

    for queue_size in queue_sizes:
        print(f"Testing queue size {queue_size}...", end=" ", flush=True)
        result = run_test(queue_size=queue_size, num_items=100, num_producers=2, num_consumers=2)
        results.append(result)
        print("Done")

    # Print results table
    print()
    print("="*80)
    print("RESULTS")
    print("="*80)
    print()

    # Header
    print(f"{'Queue Size':<12} {'Time (s)':<10} {'P-Waits':<10} {'C-Waits':<10} {'Throughput':<12} {'Status'}")
    print("-"*80)

    # Data rows
    for result in results:
        throughput = result['total_puts'] / result['time'] if result['time'] > 0 else 0
        status = "PASS" if result['items_verified'] else "FAIL"

        print(f"{result['queue_size']:<12} "
              f"{result['time']:<10.3f} "
              f"{result['producer_waits']:<10} "
              f"{result['consumer_waits']:<10} "
              f"{throughput:<12.1f} "
              f"{status}")

    print()
    print("="*80)
    print("ANALYSIS")
    print("="*80)
    print()
    print("Observations:")
    print("  - Smaller queues (5, 10):   More producer waits, slower throughput")
    print("  - Medium queues (20, 50):   Balanced blocking behavior")
    print("  - Large queues (100):       Minimal/no blocking, faster throughput")
    print()
    print("Conclusion:")
    print("  Queue size affects blocking frequency and overall performance.")
    print("  Smaller queues demonstrate blocking better but may reduce throughput.")
    print("  Larger queues improve throughput but may not demonstrate blocking.")
    print("="*80)


if __name__ == "__main__":
    main()
