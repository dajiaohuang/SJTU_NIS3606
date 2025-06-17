from abc import ABC, abstractmethod

class Block(ABC):
    """
    Block defines the interface of a block. Usually a block consists of a data field and a tag field.
    Use DefaultBlock for the default block definition.
    """
    
    @abstractmethod
    def validate(self) -> bool:
        """Validate check whether a block is valid."""
        pass
    
    @abstractmethod
    def merge(self, x: 'Block', y: 'Block') -> 'Block':
        """Merge sets the current block to the result of merging block x & y."""
        pass
    
    @abstractmethod
    def copy(self) -> 'Block':
        """Copy creates a copy of the current block."""
        pass 