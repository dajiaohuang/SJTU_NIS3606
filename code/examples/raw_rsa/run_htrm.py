from htrm import HTRM
from raw_rsa_block import RawRsaBlock
from file_manager import FileManager

TIMES_FOR_HTRM = 15

def run_htrm(fm: FileManager) -> bool:
    """Run HTRM test."""
    fm.start_session()
    try:
        # Init HTRM
        print("Initializing HTRM...")
        htrm = HTRM(TIMES_FOR_HTRM)
        htrm.init_buffers(RawRsaBlock(fm.rr))
        
        # Read & merge
        print("Merging...")
        for i in range(fm.block_count):
            block = RawRsaBlock(fm.rr, fm.next_block_data(), fm.next_block_tag())
            htrm.merge_block(block)
        
        print("Checking...")
        return htrm.check_all_buffers()
    finally:
        fm.end_session()

def parallel_run_htrm(fm: FileManager) -> bool:
    """Run parallel HTRM test."""
    fm.start_session()
    try:
        # Init HTRM
        print("Parallel initializing HTRM...")
        htrm = HTRM(TIMES_FOR_HTRM)
        htrm.parallel_init_buffers(RawRsaBlock(fm.rr))
        
        # Read & merge
        print("Parallel merging...")
        for i in range(fm.block_count):
            block = RawRsaBlock(fm.rr, fm.next_block_data(), fm.next_block_tag())
            htrm.parallel_merge_block(block)
        
        print("Parallel checking...")
        return htrm.parallel_check_all_buffers()
    finally:
        fm.end_session()