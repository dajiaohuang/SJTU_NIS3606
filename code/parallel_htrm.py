from threading import Thread, Event, Lock
from queue import Queue
from typing import List
from block import Block
import random
from parallel_utils import notify_all, waiter
from htrm import HTRM, VALUE_PER_TIMES

class ParallelHTRM(HTRM):
    """Parallel version of HTRM using threads."""
    
    def __init__(self, times: int):
        """Initialize ParallelHTRM with given times."""
        super().__init__(times)
    
    def parallel_init_buffers(self, block: Block) -> 'HTRM':
        """Initialize HTRM buffers by copying the given block in parallel."""
        self.buffers = [[] for _ in range(self.times)]
        threads = []
        
        for i in range(self.times):
            thread = Thread(target=self._init_single_time_buffers, 
                          args=(i, block))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
        return self
    
    def _init_single_time_buffers(self, i: int, block: Block) -> None:
        """Init buffers of time i."""
        self.buffers[i] = [block.copy() for _ in range(VALUE_PER_TIMES)]
    
    def parallel_merge_block(self, block: Block) -> None:
        """Merge the given block to buffers in parallel."""
        threads = []
        
        for i in range(self.times):
            thread = Thread(target=self._merge_single_block,
                          args=(i, block))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
    
    def _merge_single_block(self, i: int, block: Block) -> None:
        """Merge single block to a buffer."""
        j = random.randint(0, VALUE_PER_TIMES - 1)
        self.buffers[i][j].merge(self.buffers[i][j], block)
    
    def parallel_check_all_buffers(self) -> bool:
        """Check all buffers in parallel whether the data field matches the tag field."""
        mismatch_queue = Queue()
        done_event = Event()
        stoppers = [Event() for _ in range(self.times)]
        threads = []
        
        for i in range(self.times):
            thread = Thread(target=self._check_single_time,
                          args=(i, mismatch_queue, stoppers[i]))
            threads.append(thread)
            thread.start()
        
        done_queue = Queue()
        Thread(target=waiter, args=(done_event, done_queue)).start()
        
        # Wait for either a mismatch or completion
        if not mismatch_queue.empty():
            notify_all(stoppers)
            return False
        
        done_event.set()
        return done_queue.get()
    
    def _check_single_time(self, i: int, mismatch_queue: Queue, 
                          stopper: Event) -> None:
        """Check whether a single time's buffers are valid."""
        for j in range(VALUE_PER_TIMES):
            if stopper.is_set():
                return
            if not self.buffers[i][j].validate():
                mismatch_queue.put(False)
                return 