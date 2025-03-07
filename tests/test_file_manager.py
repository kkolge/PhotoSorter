import sys
import os
import shutil
import tempfile
import pytest

from src.logger import get_logger
from src.file_manager import FileManager

@pytest.fixture
def temp_folder_with_images():
    # Setup
    temp_dir = tempfile.mkdtemp()
    image_paths = []
    for i in range(3):
        path = os.path.join(temp_dir, f"image_{i}.jpg")
        with open(path, 'wb') as f:
            f.write(b"Test image content")
        image_paths.append(path)
    
    yield temp_dir, image_paths

    # Teardown
    shutil.rmtree(temp_dir)


def test_load_images(temp_folder_with_images):
    temp_dir, image_paths = temp_folder_with_images
    fm = FileManager()
    fm.load_images(temp_dir)
    
    assert len(fm.images) == 3
    assert all(img in fm.images for img in image_paths)


def test_get_current_image(temp_folder_with_images):
    temp_dir, image_paths = temp_folder_with_images
    fm = FileManager()
    fm.load_images(temp_dir)
    
    assert fm.get_current_image() == image_paths[0]


def test_next_image(temp_folder_with_images):
    temp_dir, image_paths = temp_folder_with_images
    fm = FileManager()
    fm.load_images(temp_dir)
    
    fm.next_image()
    assert fm.get_current_image() == image_paths[1]


def test_previous_image(temp_folder_with_images):
    temp_dir, image_paths = temp_folder_with_images
    fm = FileManager()
    fm.load_images(temp_dir)
    
    fm.previous_image()
    assert fm.get_current_image() == image_paths[-1]


def test_delete_image(temp_folder_with_images):
    temp_dir, image_paths = temp_folder_with_images
    fm = FileManager()
    fm.load_images(temp_dir)
    
    first_image = fm.get_current_image()
    fm.delete_image()
    
    assert first_image not in fm.images
    assert len(fm.images) == 2
    assert not os.path.exists(first_image)


def test_reset(temp_folder_with_images):
    temp_dir, image_paths = temp_folder_with_images
    fm = FileManager()
    fm.load_images(temp_dir)
    fm.next_image()
    
    fm.reset()
    assert fm.index == 0
