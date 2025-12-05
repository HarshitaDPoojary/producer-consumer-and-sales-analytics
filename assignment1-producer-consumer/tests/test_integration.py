import pytest
import time
from src.shared_queue import SharedQueue
from src.producer import Producer
from src.consumer import Consumer

def test_full_producer_consumer_workflow():
    """Test complete producer-consumer workflow"""
    queue = SharedQueue(max_size=10)
    source = [f"Item-{i}" for i in range(50)]
    destination = []

    producer = Producer(queue, source)
    consumer = Consumer(queue, destination, len(source))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    # Verify data integrity
    assert producer.items_produced == 50
    assert consumer.items_consumed == 50
    assert len(destination) == 50
    assert all(source[i] == destination[i] for i in range(50))

def test_multiple_producers_and_consumers():
    """Test with multiple producers and consumers"""
    queue = SharedQueue(max_size=20)

    source1 = [f"P1-{i}" for i in range(50)]
    source2 = [f"P2-{i}" for i in range(50)]
    destination = []

    producers = [
        Producer(queue, source1, name="Producer-1"),
        Producer(queue, source2, name="Producer-2")
    ]

    consumers = [
        Consumer(queue, destination, 50, name="Consumer-1"),
        Consumer(queue, destination, 50, name="Consumer-2")
    ]

    for t in producers + consumers:
        t.start()
    for t in producers + consumers:
        t.join()

    # Verify all items transferred
    assert len(destination) == 100

def test_concurrent_execution():
    """Test that producer and consumer run concurrently (not sequentially)"""
    queue = SharedQueue(max_size=10)
    source = list(range(50))
    destination = []

    start = time.time()

    producer = Producer(queue, source)
    consumer = Consumer(queue, destination, len(source))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    duration = time.time() - start

    # Concurrent execution should be faster than sequential
    # (producer + consumer sleep times would be ~1.25s if sequential)
    assert duration < 1.0  # Should complete faster due to overlapping

def test_blocking_behavior_occurs():
    """Test that blocking actually occurs with small queue"""
    queue = SharedQueue(max_size=5)  # Small queue to force blocking
    source = list(range(50))
    destination = []

    producer = Producer(queue, source)
    consumer = Consumer(queue, destination, len(source))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    # Get metrics
    metrics = queue.get_metrics()

    # With small queue, blocking should occur
    assert metrics['producer_waits'] > 0 or metrics['consumer_waits'] > 0
    assert metrics['total_puts'] == 50
    assert metrics['total_gets'] == 50

def test_data_order_preserved():
    """Test that FIFO order is preserved"""
    queue = SharedQueue(max_size=10)
    source = list(range(20))
    destination = []

    producer = Producer(queue, source)
    consumer = Consumer(queue, destination, len(source))

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    # Verify FIFO order
    assert destination == source
