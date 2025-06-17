from threading import Event, Thread
from typing import List
from queue import Queue

def notify_all(stoppers: List[Event]) -> None:
    """Notify all threads to stop."""
    for stopper in stoppers:
        stopper.set()

def waiter(done_event: Event, done_queue: Queue) -> None:
    """Wait until all work is done."""
    done_event.wait()
    done_queue.put(True) 