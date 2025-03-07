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

import os
import shutil
import json
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)

SESSION_FILE = "session.json"
DELETED_FOLDER = "deleted"

class FileManager:
    def __init__(self):
        self.folder = ""
        self.images = []
        self.index = 0

    def load_images(self, folder):
        """Load image files from the selected folder and prepare session tracking."""
        try:
            self.folder = folder
            self.index = 0
            self.images = [os.path.join(folder, f) for f in os.listdir(folder)
                           if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.images.sort()
            logger.info(f"{len(self.images)} images loaded from folder: {folder}")

            # Load session if exists
            self.load_session()
        except Exception as e:
            logger.error(f"Error loading images: {e}")

    def get_current_image(self):
        """Return the current image path."""
        if self.images:
            try:
                return self.images[self.index]
            except IndexError:
                logger.error("Index out of range while fetching current image.")
        else:
            logger.warning("No images loaded.")
        return None

    def next_image(self):
        """Move to the next image."""
        if self.images:
            self.index = (self.index + 1) % len(self.images)
            self.save_session()
        else:
            logger.warning("No images available to navigate.")

    def previous_image(self):
        """Move to the previous image."""
        if self.images:
            self.index = (self.index - 1) % len(self.images)
            self.save_session()
        else:
            logger.warning("No images available to navigate.")

    def delete_image(self):
        """Move the current image to a 'deleted' folder."""
        if self.images:
            try:
                image_path = self.images[self.index]
                deleted_path = os.path.join(self.folder, DELETED_FOLDER)
                os.makedirs(deleted_path, exist_ok=True)
                shutil.move(image_path, deleted_path)
                logger.info(f"Deleted image moved to: {deleted_path}")

                del self.images[self.index]
                if self.index >= len(self.images):
                    self.index = 0
                self.save_session()
            except Exception as e:
                logger.error(f"Error deleting image: {e}")
        else:
            logger.warning("No images to delete.")

    def reset(self):
        """Reset session to start over from the beginning."""
        self.index = 0
        self.save_session()
        logger.info("Session reset to start over.")

    def save_session(self):
        """Save the current session progress to a file."""
        try:
            session_data = {
                "folder": self.folder,
                "index": self.index,
                "timestamp": datetime.now().isoformat()
            }
            with open(SESSION_FILE, "w") as f:
                json.dump(session_data, f)
            logger.info("Session saved successfully.")
        except Exception as e:
            logger.error(f"Error saving session: {e}")

    def load_session(self):
        """Load previous session if it matches the current folder."""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r") as f:
                    session_data = json.load(f)
                if session_data.get("folder") == self.folder:
                    self.index = session_data.get("index", 0)
                    logger.info(f"Resuming session from index {self.index}.")
                else:
                    logger.info("Different folder detected. Starting fresh session.")
            except Exception as e:
                logger.error(f"Error loading session: {e}")
        else:
            logger.info("No previous session found. Starting fresh.")
