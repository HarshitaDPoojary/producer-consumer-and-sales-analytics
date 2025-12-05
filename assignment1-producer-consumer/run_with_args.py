"""
Producer-Consumer with Command-Line Arguments

Usage:
    python run_with_args.py --queue-size 10 --producers 3 --consumers 2 --items 50

Arguments:
    --queue-size: Maximum size of the queue (default: 10)
    --producers: Number of producer threads (default: 1)
    --consumers: Number of consumer threads (default: 1)
    --items: Number of items per producer (default: 100)
    --verbose: Show detailed logging (default: False)
"""

import sys
import time
import argparse
import logging
sys.path.insert(0, 'src')

from shared_queue import SharedQueue
from producer import Producer
from consumer import Consumer

def configure_logging(verbose=False):
    """Configure logging based on verbosity"""
    if verbose:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(threadName)-12s] %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S'
        )
    else:
        # Disable logging for clean output
        logging.basicConfig(level=logging.CRITICAL)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Run producer-consumer simulation with custom parameters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic: 1 producer, 1 consumer, queue size 10, 100 items
  python run_with_args.py

  # Custom: 3 producers, 2 consumers, queue size 15, 50 items each
  python run_with_args.py --queue-size 15 --producers 3 --consumers 2 --items 50

  # With verbose logging
  python run_with_args.py --producers 2 --consumers 2 --verbose

  # Small queue to force blocking
  python run_with_args.py --queue-size 5 --items 100
        """
    )

    parser.add_argument('--queue-size', '-q', type=int, default=10,
                        help='Maximum size of the queue (default: 10)')
    parser.add_argument('--producers', '-p', type=int, default=1,
                        help='Number of producer threads (default: 1)')
    parser.add_argument('--consumers', '-c', type=int, default=1,
                        help='Number of consumer threads (default: 1)')
    parser.add_argument('--items', '-i', type=int, default=100,
                        help='Number of items per producer (default: 100)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed logging output')

    args = parser.parse_args()

    # Configure logging
    configure_logging(args.verbose)

    # Validate inputs
    if args.queue_size < 1:
        print("Error: Queue size must be at least 1")
        return
    if args.producers < 1:
        print("Error: Number of producers must be at least 1")
        return
    if args.consumers < 1:
        print("Error: Number of consumers must be at least 1")
        return
    if args.items < 1:
        print("Error: Items per producer must be at least 1")
        return

    # Calculate totals
    total_items = args.producers * args.items
    items_per_consumer = total_items // args.consumers

    # Print configuration
    print("="*70)
    print("PRODUCER-CONSUMER SIMULATION")
    print("="*70)
    print(f"\nConfiguration:")
    print(f"  Queue size:          {args.queue_size}")
    print(f"  Producers:           {args.producers}")
    print(f"  Consumers:           {args.consumers}")
    print(f"  Items per producer:  {args.items}")
    print(f"  Items per consumer:  {items_per_consumer}")
    print(f"  Total items:         {total_items}")
    print(f"  Verbose logging:     {args.verbose}")
    print()

    # Create shared queue and destination
    queue = SharedQueue(max_size=args.queue_size)
    destination = []

    # Create producers
    producers = []
    for i in range(args.producers):
        source = [f"P{i+1}-Item-{j}" for j in range(args.items)]
        p = Producer(queue, source, name=f"Producer-{i+1}")
        producers.append(p)

    # Create consumers
    consumers = []
    for i in range(args.consumers):
        c = Consumer(queue, destination, items_per_consumer, name=f"Consumer-{i+1}")
        consumers.append(c)

    # Start simulation
    print("Starting simulation...")
    if not args.verbose:
        print("(Run with --verbose to see detailed thread logs)\n")

    start_time = time.time()

    # Start all threads
    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    # Wait for completion
    for p in producers:
        p.join()
    for c in consumers:
        c.join()

    total_time = time.time() - start_time

    # Print results
    print("\n" + "="*70)
    print("RESULTS")
    print("="*70)

    # Producer stats
    print(f"\nProducers ({args.producers} threads):")
    total_produced = 0
    for p in producers:
        print(f"  {p.name:12} produced {p.items_produced:4} items")
        total_produced += p.items_produced
    print(f"  {'Total':12} produced {total_produced:4} items")

    # Consumer stats
    print(f"\nConsumers ({args.consumers} threads):")
    total_consumed = 0
    for c in consumers:
        print(f"  {c.name:12} consumed {c.items_consumed:4} items")
        total_consumed += c.items_consumed
    print(f"  {'Total':12} consumed {total_consumed:4} items")

    # Metrics
    metrics = queue.get_metrics()
    print(f"\nPerformance:")
    print(f"  Execution time:      {total_time:.3f}s")
    print(f"  Throughput:          {total_items/total_time:.1f} items/sec")
    print(f"  Queue puts:          {metrics['total_puts']}")
    print(f"  Queue gets:          {metrics['total_gets']}")
    print(f"  Producer waits:      {metrics['producer_waits']}")
    print(f"  Consumer waits:      {metrics['consumer_waits']}")
    print(f"  Avg producer wait:   {metrics['avg_producer_wait']:.4f}s")
    print(f"  Avg consumer wait:   {metrics['avg_consumer_wait']:.4f}s")

    # Verification
    success = len(destination) == total_items
    print(f"\nVerification:")
    print(f"  Expected:            {total_items} items")
    print(f"  Actual:              {len(destination)} items")
    print(f"  Status:              {'PASS' if success else 'FAIL'}")

    # Blocking analysis
    if metrics['producer_waits'] > 0 and metrics['consumer_waits'] > 0:
        print(f"\n  Note: Both producers and consumers blocked (balanced workload)")
    elif metrics['producer_waits'] > 0:
        print(f"\n  Note: Producers blocked {metrics['producer_waits']} times (queue too small or consumers too slow)")
    elif metrics['consumer_waits'] > 0:
        print(f"\n  Note: Consumers blocked {metrics['consumer_waits']} times (producers too slow)")
    else:
        print(f"\n  Note: No blocking occurred (queue size sufficient)")

    print("="*70)

if __name__ == "__main__":
    main()
