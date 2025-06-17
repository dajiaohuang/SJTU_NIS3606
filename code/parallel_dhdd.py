from threading import Thread, Event, Lock
from queue import Queue
from typing import List
from block import Block
import random
from parallel_utils import notify_all, waiter
from dhdd import DHDD, VALUE_PER_DIMENSION

class ParallelDHDD(DHDD):
    """Parallel version of DHDD using threads."""
    
    def parallel_init_buffers(self, block: Block) -> 'DHDD':
        """Initialize DHDD buffers by copying the given block in parallel."""
        self.buffers = [[] for _ in range(self.dimension)]
        threads = []
        
        for i in range(self.dimension):
            thread = Thread(target=self._init_single_dimension_buffers, 
                          args=(i, block))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
        return self
    
    def _init_single_dimension_buffers(self, i: int, block: Block) -> None:
        """Init buffers of dimension i."""
        self.buffers[i] = [block.copy() for _ in range(VALUE_PER_DIMENSION)]
    
    def parallel_merge_block(self, index: int, block: Block) -> None:
        """
        Merge the given block to many buffers indicated by block_index_to_logical_position 
        in parallel.
        """
        logical_position = self.block_index_to_logical_position[index]
        threads = []
        
        for i, j in enumerate(logical_position):
            thread = Thread(target=self._merge_single_block,
                          args=(i, j, block))
            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()
    
    def _merge_single_block(self, i: int, j: int, block: Block) -> None:
        """Merge single block to a buffer."""
        self.buffers[i][j].merge(self.buffers[i][j], block)
    
    def parallel_check_all_buffers(self) -> bool:
        """Check all buffers in parallel whether the data field matches the tag field."""
        mismatch_queue = Queue()
        done_event = Event()
        stoppers = [Event() for _ in range(self.dimension)]
        threads = []
        
        for i in range(self.dimension):
            thread = Thread(target=self._check_single_dimension,
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
    
    def _check_single_dimension(self, i: int, mismatch_queue: Queue, 
                              stopper: Event) -> None:
        """Check whether a single dimension's buffers are valid."""
        for j in range(VALUE_PER_DIMENSION):
            if stopper.is_set():
                return
            if not self.buffers[i][j].validate():
                mismatch_queue.put(False)
                return 