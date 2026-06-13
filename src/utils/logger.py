"""
Central Logging Configuration for the Document Assistant.
Provides clean terminal logging with timestamps and severity levels.
"""

import logging
import sys

def get_logger(module_name):
    """
    Creates or retrieves a formatted logger instance for a given module.
    """
    logger = logging.getLogger(module_name)
    
    # Prevent duplicate handlers if the logger is fetched multiple times
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create a professional format: Timestamp | Level | Module | Message
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Output directly to the standard console stream
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger