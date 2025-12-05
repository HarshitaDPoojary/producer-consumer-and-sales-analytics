import pytest
from src.shared_queue import SharedQueue
from src.producer import Producer

def test_producer_produces_all_items():
    """Test producer enqueues all source items"""
    queue = SharedQueue(max_size=10)
    source = ["a", "b", "c"]

    producer = Producer(queue, source)
    producer.start()
    producer.join()

    assert producer.items_produced == 3
    assert queue.get() == "a"
    assert queue.get() == "b"
    assert queue.get() == "c"

def test_producer_with_large_dataset():
    """Test producer with large dataset"""
    queue = SharedQueue(max_size=100)  # Large enough to hold all items
    source = list(range(100))

    producer = Producer(queue, source)
    producer.start()
    producer.join()

    assert producer.items_produced == 100

def test_producer_thread_name():
    """Test producer thread has correct name"""
    queue = SharedQueue(max_size=10)
    source = [1, 2, 3]

    producer = Producer(queue, source, name="TestProducer")
    assert producer.name == "TestProducer"

def test_producer_with_empty_source():
    """Test producer with empty source"""
    queue = SharedQueue(max_size=10)
    source = []

    producer = Producer(queue, source)
    producer.start()
    producer.join()

    assert producer.items_produced == 0
    assert queue.size() == 0
