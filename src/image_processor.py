# Copyright (c) 2025 Ketan Kolge
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from PIL import Image
from logger import get_logger

logger = get_logger(__name__)


class ImageProcessor:
    def __init__(self, max_width=1000, max_height=700):
        """
        Initialize the ImageProcessor with max display dimensions.
        """
        self.max_width = max_width
        self.max_height = max_height
        logger.info(f"ImageProcessor initialized with size {self.max_width}x{self.max_height}.")

    def process_image(self, image_path):
        """
        Open and resize the image to fit within the specified dimensions while maintaining aspect ratio.

        Args:
            image_path (str): The path to the image file.

        Returns:
            Image: Resized PIL Image object.
        """
        try:
            img = Image.open(image_path)
            original_size = img.size
            img.thumbnail((self.max_width, self.max_height), Image.LANCZOS)
            logger.info(
                f"Image '{image_path}' loaded and resized from {original_size} to {img.size}."
            )
            return img
        except Exception as e:
            logger.error(f"Failed to process image '{image_path}': {e}")
            return None
