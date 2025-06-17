import random
from block import Block
from cartesian import cartesian_product

# Constants
VALUE_PER_DIMENSION = 3  # Number of possible values per dimension

class DPoR:
    """DPoR is a class for Dynamic Proofs of Retrievability."""

    def __init__(self):
        self.dimension = 0  # Number of dimensions (x in the paper)
        self.logical_block_num = 0  # Total number of logical blocks (N in the paper)
        self.block_index_to_logical_position = {}  # Mapping of block indices to logical positions (pi in the paper)
        self.buffers: list[list[Block]] = []  # Buffers for storing data blocks

    @classmethod
    def new(cls, n: int, seed: int) -> 'DPoR':
        """
        Initialize a DPoR instance with the given number of blocks and seed.
        """
        dpor = cls()
        dpor._calculate_dimension_and_logical_block_num(n)
        dpor._generate_block_index_to_logical_position(seed)
        return dpor

    def _calculate_dimension_and_logical_block_num(self, n: int) -> None:
        """
        Calculate the dimension and logical block number based on the number of blocks.
        """
        self.dimension = 0
        self.logical_block_num = 1
        while self.logical_block_num < n:
            self.logical_block_num *= VALUE_PER_DIMENSION
            self.dimension += 1

    def _generate_block_index_to_logical_position(self, seed: int) -> None:
        """
        Generate a random mapping of block indices to logical positions.
        """
        logical_positions = cartesian_product(self.dimension)
        random.seed(seed)
        random.shuffle(logical_positions)
        self.block_index_to_logical_position = {
            i: logical_positions[i] for i in range(self.logical_block_num)
        }

    def init_buffers(self, block: Block) -> 'DPoR':
        """
        Initialize the buffers by copying the given block.
        """
        self.buffers = [
            [block.copy() for _ in range(VALUE_PER_DIMENSION)]
            for _ in range(self.dimension)
        ]
        return self

    def update_block(self, index: int, new_block: Block) -> None:
        """
        Update a block at the given index with a new block.
        """
        logical_position = self.block_index_to_logical_position[index]
        for i, j in enumerate(logical_position):
            self.buffers[i][j].merge(new_block)

    def verify_integrity(self) -> bool:
        """
        Verify the integrity of all buffers by checking if the data matches the tags.
        """
        return all(
            buffer.validate()
            for dimension in self.buffers
            for buffer in dimension
        )

    def retrieve_block(self, index: int) -> Block:
        """
        Retrieve a block at the given index by combining data from the buffers.
        """
        logical_position = self.block_index_to_logical_position[index]
        retrieved_block = Block()
        for i, j in enumerate(logical_position):
            retrieved_block.merge(self.buffers[i][j])
        return retrieved_block