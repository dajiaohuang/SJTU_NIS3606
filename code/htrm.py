import random
from block import Block

# ValuePerTimes defines how many possible values every random-merging has.
VALUE_PER_TIMES = 3

class HTRM:
    """HTRM is a class for HTRM algorithm."""
    
    def __init__(self, times: int):
        """Return a new HTRM object with the given times."""
        self.times = times
        # Equals the buffer in the paper.
        # buffers[i][j] means the buffer of "the i-th test of random value j".
        self.buffers: list[list[Block]] = []

    def init_buffers(self, block: Block) -> 'HTRM':
        """Init HTRM buffers by copying the given block."""
        self.buffers = []
        for _ in range(self.times):
            dimension = []
            for _ in range(VALUE_PER_TIMES):
                dimension.append(block.copy())
            self.buffers.append(dimension)
        return self

    def merge_block(self, block: Block) -> None:
        """Merge the given block to buffers many times."""
        # merge `times` times
        for i in range(self.times):
            # each time, generate a random number from 0 to ValuePerTimes-1
            j = random.randint(0, VALUE_PER_TIMES - 1)
            self.buffers[i][j].merge(self.buffers[i][j], block)

    def check_all_buffers(self) -> bool:
        """Check all buffers whether the data field matches the tag field."""
        return all(
            buffer.validate()
            for dimension in self.buffers
            for buffer in dimension
        ) 