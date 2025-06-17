import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import time
from dhdd import DHDD
from htrm import HTRM
from utils import DefaultBlock, default_block_generator

# Define block count
N = 10000
TIMES_FOR_HTRM = 10

def run_dhdd():
    """Run DHDD example."""
    # Init DHDD
    dhdd = DHDD.new(N, int(time.time_ns()))  # Use current time as seed
    dhdd.init_buffers(DefaultBlock())  # Use default block to init buffers

    # Merge blocks
    for i in range(N):
        dhdd.merge_block(i, default_block_generator())

    # Check
    print(dhdd.check_all_buffers())  # => True

def run_htrm():
    """Run HTRM example."""
    # Init HTRM
    htrm = HTRM(TIMES_FOR_HTRM)
    htrm.init_buffers(DefaultBlock())  # Use default block to init buffers

    # Merge blocks
    for i in range(N):
        htrm.merge_block(default_block_generator())

    # Check
    print(htrm.check_all_buffers())  # => True

def main():
    run_dhdd()
    run_htrm()

if __name__ == "__main__":
    main() 