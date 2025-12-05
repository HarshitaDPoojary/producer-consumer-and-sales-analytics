import threading
import time

class Producer(threading.Thread):
    """Producer thread that puts items into shared queue

    Demonstrates:
    - Thread lifecycle (start, run, join)
    - Concurrent programming patterns
    - Producer role in producer-consumer pattern
    """

    def __init__(self, queue, source_data, name="Producer"):
        """Initialize producer thread

        Args:
            queue: SharedQueue instance to put items into
            source_data: List of items to produce
            name: Thread name for identification
        """
        super().__init__(name=name)
        self.queue = queue
        self.source_data = source_data
        self.items_produced = 0

    def run(self):
        """Thread execution - iterates source and enqueues items

        This method is called when start() is invoked.
        Demonstrates thread concurrent execution.
        """
        for item in self.source_data:
            self.queue.put(item)  # May block if queue is full
            self.items_produced += 1
            time.sleep(0.01)  # Simulate work
        print(f"{self.name} finished: produced {self.items_produced} items")
