import sys
import pytest
import os
import tempfile

from src.logger import get_logger
from src.progress_manager import ProgressManager


@pytest.fixture
def progress_manager():
    with tempfile.TemporaryDirectory() as temp_dir:
        progress_file = os.path.join(temp_dir, "progress.json")
        pm = ProgressManager(progress_file)
        yield pm


def test_initialize(progress_manager):
    assert progress_manager.progress_data == {"total_images": 0, "processed_images": 0}


def test_update_progress(progress_manager):
    progress_manager.update_progress(10, 3)
    assert progress_manager.progress_data["total_images"] == 10
    assert progress_manager.progress_data["processed_images"] == 3


def test_save_and_load_progress(progress_manager):
    progress_manager.update_progress(5, 2)
    progress_manager.save_progress()
    
    # Re-load from the same file
    new_pm = ProgressManager(progress_manager.progress_file)
    assert new_pm.progress_data == {"total_images": 5, "processed_images": 2}


def test_reset(progress_manager):
    progress_manager.update_progress(8, 4)
    progress_manager.reset()
    assert progress_manager.progress_data == {"total_images": 0, "processed_images": 0}
