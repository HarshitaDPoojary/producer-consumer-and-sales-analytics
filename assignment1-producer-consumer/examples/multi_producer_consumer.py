"""
Multi-Producer Multi-Consumer Example

Demonstrates 3 producers and 3 consumers working simultaneously.
Shows coordination with multiple threads and detailed statistics.

Usage:
    python examples/multi_producer_consumer.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.shared_queue import SharedQueue
from src.producer import Producer
from src.consumer import Consumer


def main():
    print("="*70)
    print("MULTI-PRODUCER MULTI-CONSUMER DEMONSTRATION")
    print("="*70)
    print()

    # Configuration
    queue_size = 15
    items_per_producer = 50
    num_producers = 3
    num_consumers = 3
    total_items = items_per_producer * num_producers

    print("Configuration:")
    print(f"  Queue size:          {queue_size}")
    print(f"  Producers:           {num_producers}")
    print(f"  Consumers:           {num_consumers}")
    print(f"  Items per producer:  {items_per_producer}")
    print(f"  Total items:         {total_items}")
    print()

    # Create shared queue
    queue = SharedQueue(max_size=queue_size)

    # Create producers
    producers = []
    for i in range(num_producers):
        source_data = [f"P{i+1}-Item-{j}" for j in range(items_per_producer)]
        producer = Producer(
            queue=queue,
            source_data=source_data,
            name=f"Producer-{i+1}"
        )
        producers.append(producer)

    # Create consumers
    destination = []
    consumers = []
    items_per_consumer = total_items // num_consumers

    for i in range(num_consumers):
        consumer = Consumer(
            queue=queue,
            destination=destination,
            num_items=items_per_consumer,
            name=f"Consumer-{i+1}"
        )
        consumers.append(consumer)

    # Start timing
    print("Starting simulation...")
    print()
    start_time = time.time()

    # Start all producers
    for producer in producers:
        producer.start()

    # Start all consumers
    for consumer in consumers:
        consumer.start()

    # Wait for all producers to finish
    for producer in producers:
        producer.join()

    # Wait for all consumers to finish
    for consumer in consumers:
        consumer.join()

    # Calculate total time
    total_time = time.time() - start_time

    # Print thread statistics
    print()
    print("="*70)
    print("THREAD STATISTICS")
    print("="*70)
    print()
    print("Producers:")
    for producer in producers:
        print(f"  {producer.name:12s} - Produced: {producer.items_produced:3d} items")

    print()
    print("Consumers:")
    for consumer in consumers:
        print(f"  {consumer.name:12s} - Consumed: {consumer.items_consumed:3d} items")

    # Verification
    print()
    print("="*70)
    print("VERIFICATION")
    print("="*70)
    total_produced = sum(p.items_produced for p in producers)
    total_consumed = sum(c.items_consumed for c in consumers)

    print(f"Total produced:      {total_produced}")
    print(f"Total consumed:      {total_consumed}")
    print(f"Destination size:    {len(destination)}")
    print(f"Expected total:      {total_items}")

    if total_produced == total_consumed == len(destination) == total_items:
        print(f"Status:              PASS")
    else:
        print(f"Status:              FAIL")

    # Performance metrics
    print()
    print("="*70)
    print("PERFORMANCE METRICS")
    print("="*70)

    metrics = queue.get_metrics()
    throughput = total_items / total_time if total_time > 0 else 0

    print(f"Total execution time:     {total_time:.3f}s")
    print(f"Throughput:               {throughput:.1f} items/sec")
    print(f"Queue capacity:           {queue._max_size}")
    print(f"Total queue puts:         {metrics['total_puts']}")
    print(f"Total queue gets:         {metrics['total_gets']}")
    print(f"Producer wait events:     {metrics['producer_waits']}")
    print(f"Consumer wait events:     {metrics['consumer_waits']}")
    print(f"Avg producer wait time:   {metrics['avg_producer_wait']:.3f}s")
    print(f"Avg consumer wait time:   {metrics['avg_consumer_wait']:.3f}s")

    print()
    if metrics['producer_waits'] > 0 or metrics['consumer_waits'] > 0:
        print("[PASS] Blocking behavior demonstrated")
    else:
        print("[INFO] No blocking occurred (queue may be too large)")

    print("="*70)


if __name__ == "__main__":
    main()
