from file_manager import FileManager

def run_one_by_one(fm: FileManager) -> bool:
    """Check every block one by one."""
    fm.start_session()
    try:
        # Check each block
        for i in range(fm.block_count):
            data = fm.next_block_data()
            tag = fm.next_block_tag()
            if data != fm.rr.raw_decrypt(tag):
                return False
        return True
    finally:
        fm.end_session() 