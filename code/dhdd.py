import random
from block import Block
from cartesian import cartesian_product

# ValuePerDimension defines how many possible values every dimension has.
VALUE_PER_DIMENSION = 3

class DHDD:
    """DHDD is a class for DHDD algorithm."""
    
    def __init__(self):
        self.dimension = 0                    # Equals the x in the paper
        self.logical_block_num = 0           # Equals the N in the paper
        self.block_index_to_logical_position = {}  # Equals the pi in the paper
        
        # Equals the buffer in the paper.
        # buffers[i][j] means the buffer of "the value of dimension i is j".
        self.buffers: list[list[Block]] = []

    @classmethod
    def new(cls, n: int, seed: int) -> 'DHDD':
        """
        Calculate dimension & logical_block_num according to the count of blocks n
        and generate block_index_to_logical_position randomly by using random.seed(seed).
        If you are not sure what seed to use, use time.time_ns().
        """
        dhdd = cls()
        dhdd._get_dimension_and_logical_block_num(n)
        dhdd._generate_block_index_to_logical_position(seed)
        return dhdd

    def _get_dimension_and_logical_block_num(self, n: int) -> None:
        self.dimension = 0
        self.logical_block_num = 1
        while self.logical_block_num < n:
            self.logical_block_num *= VALUE_PER_DIMENSION
            self.dimension += 1

    def _generate_block_index_to_logical_position(self, seed: int) -> None:
        # generate logical positions, each logical position is an int list of length x
        logical_positions = cartesian_product(self.dimension)
        
        # shuffle logical positions
        random.seed(seed)
        random.shuffle(logical_positions)
        
        # construct result
        self.block_index_to_logical_position = {
            i: logical_positions[i] 
            for i in range(self.logical_block_num)
        }

    def init_buffers(self, block: Block) -> 'DHDD':
        """Init DHDD buffers by copying the given block."""
        self.buffers = []
        for i in range(self.dimension):
            self.buffers.append([])
            for _ in range(VALUE_PER_DIMENSION):
                self.buffers[i].append(block.copy())
        return self

    def merge_block(self, index: int, block: Block) -> None:
        """Merge the given block to many buffers indicated by block_index_to_logical_position."""
        logical_position = self.block_index_to_logical_position[index]
        for i, j in enumerate(logical_position):
            self.buffers[i][j].merge(self.buffers[i][j], block)

    def check_all_buffers(self) -> bool:
        """Check all buffers whether the data field matches the tag field."""
        return all(
            buffer.validate()
            for dimension in self.buffers
            for buffer in dimension
        ) 