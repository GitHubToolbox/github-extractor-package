"""
This module defines default constants used for configuring GitHub API requests and concurrent execution.

Constants:
- DEFAULT_TIMEOUT: The default timeout for API requests in seconds.
- DEFAULT_CPU_COUNT: A sensible default number of CPU cores if os.cpu_count() returns None.
- DEFAULT_THREADS: The default number of threads for concurrent execution, set to twice the number of CPU cores.

These constants can be imported and used in other modules to ensure consistent configuration values across the application.

Example usage:
    from .constants import DEFAULT_TIMEOUT, DEFAULT_THREADS

    timeout = DEFAULT_TIMEOUT
    max_threads = DEFAULT_THREADS
"""

import os

DEFAULT_TIMEOUT: int = 10  # Default timeout for API requests in seconds
DEFAULT_CPU_COUNT = 4  # Sensible default if os.cpu_count() returns None
DEFAULT_THREADS: int = (os.cpu_count() or DEFAULT_CPU_COUNT) * 2
