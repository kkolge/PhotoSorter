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

import tkinter as tk
from ui import PhotoManagerUI
from file_manager import FileManager
from progress_manager import ProgressManager
from image_processor import ImageProcessor
from reports_manager import ReportsManager
from logger import get_logger

logger = get_logger(__name__)


def main():
    logger.info("Photo Manager Application started.")

    try:
        # Initialize the main window
        root = tk.Tk()
        root.title("Photo Manager")
        root.state('zoomed')  # Start maximized for better viewing

        # Initialize all managers
        file_manager = FileManager()
        progress_manager = ProgressManager()
        image_processor = ImageProcessor()
        reports_manager = ReportsManager()

        # Start the UI
        app = PhotoManagerUI(
            root,
            file_manager,
            progress_manager,
            image_processor,
            reports_manager
        )

        # Start the Tkinter main loop
        root.mainloop()

        logger.info("Application closed normally.")

    except Exception as e:
        logger.exception(f"Application encountered an error: {e}")


if __name__ == "__main__":
    main()
