import time
from dhdd import DHDD
from raw_rsa_block import RawRsaBlock
from file_manager import FileManager

def run_dhdd(fm: FileManager) -> bool:
    """Run DHDD test."""
    fm.start_session()
    try:
        # Init DHDD
        print("Initializing DHDD...")
        dhdd = DHDD.new(fm.block_count, int(time.time_ns()))
        dhdd.init_buffers(RawRsaBlock(fm.rr))
        
        # Read & merge
        print("Merging...")
        for i in range(fm.block_count):
            block = RawRsaBlock(fm.rr, fm.next_block_data(), fm.next_block_tag())
            dhdd.merge_block(i, block)
        
        print("Checking...")
        return dhdd.check_all_buffers()
    finally:
        fm.end_session()

def parallel_run_dhdd(fm: FileManager) -> bool:
    """Run parallel DHDD test."""
    fm.start_session()
    try:
        # Init DHDD
        print("Parallel initializing DHDD...")
        dhdd = DHDD.new(fm.block_count, int(time.time_ns()))
        dhdd.parallel_init_buffers(RawRsaBlock(fm.rr))
        
        # Read & merge
        print("Parallel merging...")
        for i in range(fm.block_count):
            block = RawRsaBlock(fm.rr, fm.next_block_data(), fm.next_block_tag())
            dhdd.parallel_merge_block(i, block)
        
        print("Parallel checking...")
        return dhdd.parallel_check_all_buffers()
    finally:
        fm.end_session()