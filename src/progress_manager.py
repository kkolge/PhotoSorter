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

import json
import os
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)

class ProgressManager:
    def __init__(self):
        self.progress_file = "progress.json"
        self.progress_data = {
            "session_start": datetime.now().isoformat(),
            "last_index": 0,
            "total_images": 0,
            "processed_images": 0,
            "deleted_images": 0,
            "paused": False
        }
        self.load_progress()

    def load_progress(self):
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, "r") as f:
                    self.progress_data = json.load(f)
                logger.info(f"Progress loaded from {self.progress_file}.")
            except Exception as e:
                logger.error(f"Failed to load progress: {e}")
        else:
            logger.info("No previous progress found. Starting new session.")

    def save_progress(self):
        try:
            with open(self.progress_file, "w") as f:
                json.dump(self.progress_data, f, indent=4)
            logger.info(f"Progress saved to {self.progress_file}.")
        except Exception as e:
            logger.error(f"Failed to save progress: {e}")

    def update_progress(self, current_index, total_images):
        self.progress_data["last_index"] = current_index
        self.progress_data["total_images"] = total_images
        self.progress_data["processed_images"] = current_index
        self.save_progress()
        logger.info(
            f"Progress updated: {current_index}/{total_images} images processed."
        )

    def increment_deleted(self):
        self.progress_data["deleted_images"] += 1
        self.save_progress()
        logger.info(f"Deleted images count updated to {self.progress_data['deleted_images']}.")

    def pause(self):
        self.progress_data["paused"] = True
        self.save_progress()
        logger.info("Processing paused.")

    def resume(self):
        self.progress_data["paused"] = False
        self.save_progress()
        logger.info("Processing resumed.")

    def reset(self):
        self.progress_data = {
            "session_start": datetime.now().isoformat(),
            "last_index": 0,
            "total_images": 0,
            "processed_images": 0,
            "deleted_images": 0,
            "paused": False
        }
        self.save_progress()
        logger.info("Progress reset for a new session.")
