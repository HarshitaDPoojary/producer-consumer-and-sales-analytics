import pytest
import threading
import time
from src.shared_queue import SharedQueue

def test_queue_put_and_get():
    """Test basic put and get operations"""
    queue = SharedQueue(max_size=5)
    queue.put("item1")
    queue.put("item2")
    assert queue.get() == "item1"
    assert queue.get() == "item2"

def test_queue_blocking_when_full():
    """Test that put blocks when queue is full"""
    queue = SharedQueue(max_size=2)
    queue.put("item1")
    queue.put("item2")

    # Try to add third item - should block
    blocked = []
    def blocking_put():
        queue.put("item3")
        blocked.append(True)

    thread = threading.Thread(target=blocking_put)
    thread.start()
    time.sleep(0.1)  # Let thread start blocking

    # Should be blocked
    assert len(blocked) == 0

    # Unblock by consuming
    queue.get()
    thread.join(timeout=1)

    # Should have completed
    assert len(blocked) == 1

def test_queue_blocking_when_empty():
    """Test that get blocks when queue is empty"""
    queue = SharedQueue(max_size=5)

    result = []
    def blocking_get():
        item = queue.get()
        result.append(item)

    thread = threading.Thread(target=blocking_get)
    thread.start()
    time.sleep(0.1)

    # Should be blocked
    assert len(result) == 0

    # Unblock by producing
    queue.put("test-item")
    thread.join(timeout=1)

    # Should have item
    assert result[0] == "test-item"

def test_thread_safety():
    """Test concurrent access by multiple threads"""
    queue = SharedQueue(max_size=50)
    num_items = 100

    def producer_work():
        for i in range(num_items):
            queue.put(i)

    def consumer_work():
        items = []
        for _ in range(num_items):
            items.append(queue.get())
        return items

    results = []

    # Start multiple producers and consumers
    producers = [threading.Thread(target=producer_work) for _ in range(2)]
    consumers = [threading.Thread(target=lambda: results.extend(consumer_work())) for _ in range(2)]

    for t in producers + consumers:
        t.start()
    for t in producers + consumers:
        t.join()

    # Verify all items transferred
    assert len(results) == num_items * 2

def test_queue_size():
    """Test size method returns correct queue size"""
    queue = SharedQueue(max_size=5)
    assert queue.size() == 0
    queue.put("item1")
    assert queue.size() == 1
    queue.put("item2")
    assert queue.size() == 2
    queue.get()
    assert queue.size() == 1

def test_metrics_tracking():
    """Test that metrics are tracked correctly"""
    queue = SharedQueue(max_size=3)

    # Put 3 items (fill queue)
    queue.put("item1")
    queue.put("item2")
    queue.put("item3")

    # Try to put 4th item in separate thread (will wait)
    def blocking_put():
        queue.put("item4")

    thread = threading.Thread(target=blocking_put)
    thread.start()
    time.sleep(0.1)

    # Get metrics
    metrics = queue.get_metrics()
    assert metrics['total_puts'] == 3
    assert metrics['producer_waits'] == 1

    # Consume and let producer finish
    queue.get()
    queue.get()
    thread.join(timeout=1)

    # Check final metrics
    metrics = queue.get_metrics()
    assert metrics['total_puts'] == 4
    assert metrics['total_gets'] == 2
    assert metrics['producer_waits'] == 1
