import os
import random
from typing import BinaryIO, TextIO
from raw_rsa import RawRsa

class FileManager:
    """FileManager will manage data files & tag files."""
    
    def __init__(self, rr: RawRsa, data_filename: str, tag_filename: str, 
                 chunk_size: int, block_count: int):
        self.rr = rr
        self.data_filename = data_filename
        self.tag_filename = tag_filename
        self.chunk_size = chunk_size
        self.block_count = block_count
        self.data_file: BinaryIO | None = None
        self.tag_file: TextIO | None = None
    
    @classmethod
    def new_files(cls, key_filename: str, rsa_key_bits: int, 
                  data_filename: str, tag_filename: str, 
                  chunk_size: int, block_count: int) -> 'FileManager':
        """Create new files and return FileManager."""
        # Create key file and save
        rr = RawRsa.new(rsa_key_bits)
        rr.save(key_filename)
        
        # Create and write files
        with open(data_filename, 'wb') as data_file, \
             open(tag_filename, 'w') as tag_file:
            
            for _ in range(block_count):
                # Data file consists of random bytes
                data = random.randbytes(chunk_size)
                data_file.write(data)
                
                # Each line in tag file is a tag
                data_int = int.from_bytes(data, 'big')
                tag = rr.raw_encrypt(data_int)
                tag_file.write(f"{tag}\n")
        
        return cls(rr, data_filename, tag_filename, chunk_size, block_count)
    
    @classmethod
    def load_files(cls, key_filename: str, data_filename: str, 
                   tag_filename: str, chunk_size: int, 
                   block_count: int) -> 'FileManager':
        """Use existing files and return FileManager."""
        rr = RawRsa.load(key_filename)
        return cls(rr, data_filename, tag_filename, chunk_size, block_count)
    
    def start_session(self):
        """Open files for reading operations."""
        self.data_file = open(self.data_filename, 'rb')
        self.tag_file = open(self.tag_filename, 'r')
    
    def end_session(self):
        """Close files."""
        if self.data_file:
            self.data_file.close()
        if self.tag_file:
            self.tag_file.close()
        self.data_file = None
        self.tag_file = None
    
    def next_block_data(self) -> int:
        """Read from data file and return int of a block size."""
        data = self.data_file.read(self.chunk_size)
        return int.from_bytes(data, 'big')
    
    def next_block_tag(self) -> int:
        """Read from tag file and return the tag."""
        return int(self.tag_file.readline().strip()) 