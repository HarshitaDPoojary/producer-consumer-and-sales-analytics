import pytest
import threading
from src.shared_queue import SharedQueue
from src.consumer import Consumer

def test_consumer_consumes_all_items():
    """Test consumer retrieves all items"""
    queue = SharedQueue(max_size=10)
    destination = []

    # Pre-populate queue
    for i in range(5):
        queue.put(f"item-{i}")

    consumer = Consumer(queue, destination, 5)
    consumer.start()
    consumer.join()

    assert consumer.items_consumed == 5
    assert len(destination) == 5

def test_consumer_thread_safe_writes():
    """Test multiple consumers write safely to destination"""
    queue = SharedQueue(max_size=100)  # Large enough to hold all items
    destination = []

    # Populate queue
    for i in range(100):
        queue.put(i)

    # Multiple consumers
    consumers = [Consumer(queue, destination, 50) for _ in range(2)]
    for c in consumers:
        c.start()
    for c in consumers:
        c.join()

    # All items should be in destination
    assert len(destination) == 100
    # No duplicates
    assert len(set(destination)) == 100

def test_consumer_thread_name():
    """Test consumer thread has correct name"""
    queue = SharedQueue(max_size=10)
    destination = []

    consumer = Consumer(queue, destination, 0, name="TestConsumer")
    assert consumer.name == "TestConsumer"

def test_consumer_with_mixed_data_types():
    """Test consumer handles different data types"""
    queue = SharedQueue(max_size=10)
    destination = []

    # Add different types
    items = [1, "string", 3.14, True, None]
    for item in items:
        queue.put(item)

    consumer = Consumer(queue, destination, len(items))
    consumer.start()
    consumer.join()

    assert len(destination) == len(items)
    assert destination == items
