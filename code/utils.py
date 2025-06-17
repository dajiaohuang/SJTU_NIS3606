import random
from block import Block

# DefaultBlockFieldSize is the default size of the data & tag fields of a block.
DEFAULT_BLOCK_FIELD_SIZE = 1024

class DefaultBlock(Block):
    """DefaultBlock consists of a data field and a tag field."""
    
    def __init__(self):
        """
        Initialize the data & tag fields of DefaultBlock
        with an empty byte list of the length DEFAULT_BLOCK_FIELD_SIZE.
        """
        self.data = bytearray(DEFAULT_BLOCK_FIELD_SIZE)
        self.tag = bytearray(DEFAULT_BLOCK_FIELD_SIZE)
    
    def merge(self, x: 'DefaultBlock', y: 'DefaultBlock') -> 'Block':
        """Merge will add fields of x to the fields of y."""
        # In Python we don't need type assertion as we're using type hints
        for i in range(DEFAULT_BLOCK_FIELD_SIZE):
            self.data[i] = (x.data[i] + y.data[i]) % 256  # Use modulo to keep within byte range
            self.tag[i] = (x.tag[i] + y.tag[i]) % 256
        return self
    
    def copy(self) -> 'Block':
        """Return a copy of the current block."""
        copied = DefaultBlock()
        copied.data = bytearray(self.data)
        copied.tag = bytearray(self.tag)
        return copied
    
    def validate(self) -> bool:
        """Check whether each byte of the data field is identical to the tag field."""
        return self.data == self.tag

def default_block_generator() -> DefaultBlock:
    """
    Generate a DefaultBlock whose data & tag fields are identical with the length DEFAULT_BLOCK_FIELD_SIZE
    and the content is random.
    """
    block = DefaultBlock()
    # Generate random bytes
    block.data = bytearray(random.getrandbits(8) for _ in range(DEFAULT_BLOCK_FIELD_SIZE))
    block.tag = bytearray(block.data)  # copy value
    return block 