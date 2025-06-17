from typing import Any
import rsa
from block import Block
from raw_rsa import RawRsa

class RawRsaBlock(Block):
    """RawRsaBlock uses int to store data & tag."""
    
    def __init__(self, key: RawRsa, data: int = 1, tag: int = 1):
        """Initialize a new RawRsaBlock with data 1 and tag 1 by default."""
        self.data = data
        self.tag = tag
        self.key = key
    
    def copy(self) -> 'Block':
        """Create a copy of the current block."""
        return RawRsaBlock(self.key, self.data, self.tag)
    
    def validate(self) -> bool:
        """Check whether the encrypted data equals to the tag."""
        return self.data == self.key.raw_decrypt(self.tag)
    
    def merge(self, x: 'RawRsaBlock', y: 'RawRsaBlock') -> 'Block':
        """
        Add fields of x to the fields of y.
        m1^e * m2^e mod N == (m1*m2)^e mod N, which means 
        (data1 * data2) mod N matches (tag1 * tag2) mod N
        """
        self.data = (x.data * y.data) % self.key.n
        self.tag = (x.tag * y.tag) % self.key.n
        return self 