import logging
import time
from shared_queue import SharedQueue
from producer import Producer
from consumer import Consumer

def configure_logging():
    """Configure logging for the application

    Only configures if not already configured to avoid side effects during testing
    """
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(threadName)-12s] %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S'
        )

def main():
    """Demonstrate producer-consumer pattern with logging and metrics

    Demonstrates:
    - Thread synchronization
    - Concurrent programming
    - Blocking queues
    - Wait/Notify mechanism
    """

    # Configure logging (guarded to avoid side effects)
    configure_logging()

    print("=" * 60)
    print("PRODUCER-CONSUMER PATTERN DEMONSTRATION")
    print("=" * 60)

    # Setup
    queue = SharedQueue(max_size=10)  # Bounded queue forces blocking
    source = [f"Item-{i}" for i in range(100)]  # 100 items to transfer
    destination = []

    # Create threads
    producer = Producer(queue, source, name="Producer-1")
    consumer = Consumer(queue, destination, len(source), name="Consumer-1")

    # Start concurrent execution
    print("\nStarting producer and consumer threads...")
    print("Queue max size: 10")
    print("Items to transfer: 100\n")

    start_time = time.time()

    producer.start()  # Start producer thread
    consumer.start()  # Start consumer thread

    # Wait for completion
    producer.join()  # Block until producer finishes
    consumer.join()  # Block until consumer finishes

    total_time = time.time() - start_time

    # Display results
    print("\n" + "=" * 60)
    print("VERIFICATION")
    print("=" * 60)
    print(f"Items produced:   {producer.items_produced}")
    print(f"Items consumed:   {consumer.items_consumed}")
    print(f"Destination size: {len(destination)}")
    print(f"Data integrity:   {'PASS' if len(destination) == len(source) else 'FAIL'}")

    # Display performance metrics using pretty print
    print(f"\nTotal execution time:     {total_time:.3f}s")
    print(queue.pretty_print_metrics())

    # Check if blocking occurred
    metrics = queue.get_metrics()
    if metrics['producer_waits'] > 0 or metrics['consumer_waits'] > 0:
        print("\n[PASS] Blocking behavior demonstrated (threads waited)")
    print("=" * 60)

if __name__ == "__main__":
    main()
