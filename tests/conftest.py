"""
Pytest configuration and fixtures for ΛΕΩΝΙΔΑΣ-AI PHALANX tests.
"""
import multiprocessing
import pytest


# Fix multiprocessing fork warnings in Python 3.12+
# This fixture runs before all tests to set the spawn method
@pytest.fixture(scope="session", autouse=True)
def setup_multiprocessing():
    """
    Configure multiprocessing to use 'spawn' method instead of 'fork'.
    This prevents DeprecationWarnings in Python 3.12+ about fork() deadlocks.
    """
    try:
        # Set spawn method globally for all tests
        multiprocessing.set_start_method('spawn', force=True)
    except RuntimeError:
        # Method already set, ignore
        pass
    
    yield
    
    # Cleanup (if needed)
    pass
