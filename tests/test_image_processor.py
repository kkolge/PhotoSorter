import sys
import pytest
import tempfile
import os
from PIL import Image

from src.logger import get_logger
from src.image_processor import ImageProcessor


@pytest.fixture
def sample_image():
    # Create a temporary image for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        image_path = os.path.join(temp_dir, "test_image.jpg")
        img = Image.new('RGB', (1600, 1200), color='red')
        img.save(image_path)
        yield image_path


@pytest.fixture
def image_processor():
    return ImageProcessor()


def test_process_image(sample_image, image_processor):
    processed_img = image_processor.process_image(sample_image, 800, 600)
    
    assert processed_img is not None
    assert processed_img.width <= 800
    assert processed_img.height <= 600


def test_process_image_invalid_path(image_processor):
    with pytest.raises(FileNotFoundError):
        image_processor.process_image("invalid_path.jpg", 800, 600)
