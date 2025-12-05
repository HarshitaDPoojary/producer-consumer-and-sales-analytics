import threading
import time

class Consumer(threading.Thread):
    """Consumer thread that gets items from shared queue

    Demonstrates:
    - Thread lifecycle (start, run, join)
    - Concurrent programming patterns
    - Consumer role in producer-consumer pattern
    - Thread-safe writes to shared destination
    """

    def __init__(self, queue, destination, num_items, name="Consumer"):
        """Initialize consumer thread

        Args:
            queue: SharedQueue instance to get items from
            destination: List to store consumed items
            num_items: Number of items to consume
            name: Thread name for identification
        """
        super().__init__(name=name)
        self.queue = queue
        self.destination = destination
        self.num_items = num_items
        self.items_consumed = 0
        self._lock = threading.Lock()  # For thread-safe destination writes

    def run(self):
        """Thread execution - dequeues items and stores in destination

        This method is called when start() is invoked.
        Demonstrates thread concurrent execution and synchronization.
        """
        while self.items_consumed < self.num_items:
            item = self.queue.get()  # May block if queue is empty
            with self._lock:  # Thread-safe write to destination
                self.destination.append(item)
                self.items_consumed += 1
            time.sleep(0.015)  # Simulate work (slightly slower than producer)
        print(f"{self.name} finished: consumed {self.items_consumed} items")
