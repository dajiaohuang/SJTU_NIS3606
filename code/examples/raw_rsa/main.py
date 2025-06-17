import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import time
from raw_rsa_block import RawRsaBlock
from file_manager import FileManager
from dhdd import DHDD
from htrm import HTRM
from parallel_dhdd import ParallelDHDD
from parallel_htrm import ParallelHTRM

# Constants
RSA_KEY_BITS = 4096
CHUNK_SIZE = 256  # Byte count of a block's data field
BLOCK_COUNT = 1024
DATA_FILENAME = "data.bin"
TAG_FILENAME = "tag.txt"
KEY_FILENAME = "key.pem"
TIMES_FOR_HTRM = 15

def track_duration(name: str, func, fm: FileManager) -> None:
    """Call f and track duration."""
    print(f"Running {name}:")
    start = time.time()
    print(f"Result: {func(fm)}")
    print(f"{name}: {time.time() - start:.2f}s")

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

def run_parallel_dhdd(fm: FileManager) -> bool:
    """Run parallel DHDD test."""
    fm.start_session()
    try:
        print("Parallel initializing DHDD...")
        dhdd = ParallelDHDD.new(fm.block_count, int(time.time_ns()))
        dhdd.parallel_init_buffers(RawRsaBlock(fm.rr))
        
        print("Parallel merging...")
        for i in range(fm.block_count):
            block = RawRsaBlock(fm.rr, fm.next_block_data(), fm.next_block_tag())
            dhdd.parallel_merge_block(i, block)
        
        print("Parallel checking...")
        return dhdd.parallel_check_all_buffers()
    finally:
        fm.end_session()

def run_htrm(fm: FileManager) -> bool:
    """Run HTRM test."""
    fm.start_session()
    try:
        print("Initializing HTRM...")
        htrm = HTRM(TIMES_FOR_HTRM)
        htrm.init_buffers(RawRsaBlock(fm.rr))
        
        print("Merging...")
        for i in range(fm.block_count):
            block = RawRsaBlock(fm.rr, fm.next_block_data(), fm.next_block_tag())
            htrm.merge_block(block)
        
        print("Checking...")
        return htrm.check_all_buffers()
    finally:
        fm.end_session()

def run_parallel_htrm(fm: FileManager) -> bool:
    """Run parallel HTRM test."""
    fm.start_session()
    try:
        print("Parallel initializing HTRM...")
        htrm = ParallelHTRM(TIMES_FOR_HTRM)
        htrm.parallel_init_buffers(RawRsaBlock(fm.rr))
        
        print("Parallel merging...")
        for i in range(fm.block_count):
            block = RawRsaBlock(fm.rr, fm.next_block_data(), fm.next_block_tag())
            htrm.parallel_merge_block(block)
        
        print("Parallel checking...")
        return htrm.parallel_check_all_buffers()
    finally:
        fm.end_session()

def run_one_by_one(fm: FileManager) -> bool:
    """Check every block one by one."""
    fm.start_session()
    try:
        for i in range(fm.block_count):
            data = fm.next_block_data()
            tag = fm.next_block_tag()
            if data != fm.rr.raw_decrypt(tag):
                return False
        return True
    finally:
        fm.end_session()

def main():
    # Generate key files and test data
    print("Generating files...")
    fm = FileManager.new_files(KEY_FILENAME, RSA_KEY_BITS, DATA_FILENAME, 
                              TAG_FILENAME, CHUNK_SIZE, BLOCK_COUNT)
    
    # Or you can load existing files
    # print("Using existing files.")
    # fm = FileManager.load_files(KEY_FILENAME, DATA_FILENAME, TAG_FILENAME, 
    #                            CHUNK_SIZE, BLOCK_COUNT)
    
    # Performance test
    track_duration("DHDD", run_dhdd, fm)
    track_duration("HTRM", run_htrm, fm)
    track_duration("Parallel DHDD", run_parallel_dhdd, fm)
    track_duration("Parallel HTRM", run_parallel_htrm, fm)
    track_duration("One by one", run_one_by_one, fm)

if __name__ == "__main__":
    main() 