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

import csv
import os
from datetime import datetime
from logger import get_logger

logger = get_logger(__name__)


class ReportsManager:
    def __init__(self, report_folder="reports"):
        self.report_folder = report_folder
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.report_file = os.path.join(self.report_folder, f"session_{self.session_id}.csv")

        try:
            os.makedirs(self.report_folder, exist_ok=True)
            with open(self.report_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(["Timestamp", "Action", "Image Path", "Details"])
            logger.info(f"Report initialized: {self.report_file}")
        except Exception as e:
            logger.error(f"Failed to initialize report: {e}")

    def record_deletion(self, image_path):
        self._write_entry("Delete", image_path, "Image deleted.")

    def record_action(self, action, image_path="", details=""):
        self._write_entry(action, image_path, details)

    def reset(self):
        logger.info("Resetting reports manager. New session starting.")
        self.__init__(self.report_folder)

    def generate_report(self):
        """
        Finalizes the report. This is a placeholder where you could:
        - Summarize the session
        - Add a footer
        - Upload to a server
        - Or simply log the completion
        """
        try:
            with open(self.report_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([])
                writer.writerow(["Session Completed", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            logger.info(f"Report finalized: {self.report_file}")
        except Exception as e:
            logger.error(f"Error finalizing report: {e}")

    def _write_entry(self, action, image_path, details):
        try:
            with open(self.report_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    action,
                    image_path,
                    details
                ])
            logger.debug(f"Report entry recorded: {action} - {image_path} - {details}")
        except Exception as e:
            logger.error(f"Failed to write report entry: {e}")
