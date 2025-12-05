"""
Custom Configuration Runner

Runs 5 different predefined scenarios to demonstrate various configurations:
1. Balanced configuration (2P, 2C)
2. More producers (4P, 2C)
3. More consumers (2P, 4C)
4. Small queue (forces blocking)
5. Large queue (minimal blocking)

Usage:
    python examples/custom_config.py
"""

import sys
import os
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.shared_queue import SharedQueue
from src.producer import Producer
from src.consumer import Consumer


def run_scenario(scenario_name, queue_size, num_producers, num_consumers, items_per_producer):
    """Run a single scenario and return results"""

    print(f"\n{'='*70}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*70}")
    print(f"Queue size:          {queue_size}")
    print(f"Producers:           {num_producers}")
    print(f"Consumers:           {num_consumers}")
    print(f"Items per producer:  {items_per_producer}")
    print(f"Total items:         {num_producers * items_per_producer}")
    print()

    # Create shared queue
    queue = SharedQueue(max_size=queue_size)

    # Create producers
    producers = []
    for i in range(num_producers):
        source_data = [f"S{scenario_name.split()[0][-1]}-P{i+1}-Item-{j}" for j in range(items_per_producer)]
        producer = Producer(
            queue=queue,
            source_data=source_data,
            name=f"Producer-{i+1}"
        )
        producers.append(producer)

    # Create consumers
    destination = []
    consumers = []
    total_items = num_producers * items_per_producer
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
    throughput = total_items / total_time if total_time > 0 else 0

    # Print results
    print(f"Execution time:      {total_time:.3f}s")
    print(f"Throughput:          {throughput:.1f} items/sec")
    print(f"Producer waits:      {metrics['producer_waits']}")
    print(f"Consumer waits:      {metrics['consumer_waits']}")

    total_produced = sum(p.items_produced for p in producers)
    total_consumed = sum(c.items_consumed for c in consumers)

    if total_produced == total_consumed == total_items:
        print(f"Verification:        PASS ({total_items} items transferred)")
    else:
        print(f"Verification:        FAIL (Expected {total_items}, Got {total_consumed})")

    return {
        'name': scenario_name,
        'time': total_time,
        'throughput': throughput,
        'producer_waits': metrics['producer_waits'],
        'consumer_waits': metrics['consumer_waits'],
        'verified': total_produced == total_consumed == total_items
    }


def main():
    print("="*70)
    print("CUSTOM CONFIGURATION SCENARIOS")
    print("="*70)
    print()
    print("This will run 5 different scenarios to demonstrate")
    print("how different configurations affect performance and blocking.")
    print()

    scenarios = [
        {
            'name': 'Scenario 1: Balanced',
            'queue_size': 10,
            'num_producers': 2,
            'num_consumers': 2,
            'items_per_producer': 50
        },
        {
            'name': 'Scenario 2: More Producers',
            'queue_size': 15,
            'num_producers': 4,
            'num_consumers': 2,
            'items_per_producer': 30
        },
        {
            'name': 'Scenario 3: More Consumers',
            'queue_size': 15,
            'num_producers': 2,
            'num_consumers': 4,
            'items_per_producer': 40
        },
        {
            'name': 'Scenario 4: Small Queue',
            'queue_size': 3,
            'num_producers': 2,
            'num_consumers': 2,
            'items_per_producer': 50
        },
        {
            'name': 'Scenario 5: Large Queue',
            'queue_size': 100,
            'num_producers': 2,
            'num_consumers': 2,
            'items_per_producer': 50
        }
    ]

    results = []

    for scenario in scenarios:
        result = run_scenario(
            scenario_name=scenario['name'],
            queue_size=scenario['queue_size'],
            num_producers=scenario['num_producers'],
            num_consumers=scenario['num_consumers'],
            items_per_producer=scenario['items_per_producer']
        )
        results.append(result)
        time.sleep(1)  # Brief pause between scenarios

    # Summary comparison
    print(f"\n{'='*70}")
    print("SUMMARY COMPARISON")
    print(f"{'='*70}\n")

    print(f"{'Scenario':<25} {'Time (s)':<10} {'Throughput':<12} {'P-Waits':<10} {'C-Waits':<10}")
    print("-"*70)

    for result in results:
        print(f"{result['name']:<25} "
              f"{result['time']:<10.3f} "
              f"{result['throughput']:<12.1f} "
              f"{result['producer_waits']:<10} "
              f"{result['consumer_waits']:<10}")

    print()
    print(f"{'='*70}")
    print("KEY OBSERVATIONS")
    print(f"{'='*70}")
    print()
    print("1. Balanced (2P, 2C):        Even distribution of work")
    print("2. More Producers (4P, 2C):  More producer blocking expected")
    print("3. More Consumers (2P, 4C):  More consumer blocking expected")
    print("4. Small Queue (size=3):     Maximum blocking, slower throughput")
    print("5. Large Queue (size=100):   Minimal blocking, faster throughput")
    print()
    print("Conclusion:")
    print("  Configuration directly affects blocking behavior and performance.")
    print("  Adjust queue size and thread counts based on your requirements.")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
