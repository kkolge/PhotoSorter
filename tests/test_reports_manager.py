import sys
import pytest
import os
import tempfile

from src.logger import get_logger
from src.reports_manager import ReportsManager


@pytest.fixture
def temp_report_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


def test_generate_report(temp_report_dir):
    report_path = os.path.join(temp_report_dir, "test_report.txt")
    reports_manager = ReportsManager(report_path)
    
    session_id = "12345"
    total_images = 100
    deleted_images = 25
    
    reports_manager.generate_report(session_id, total_images, deleted_images)
    
    assert os.path.exists(report_path)
    
    with open(report_path, "r") as file:
        content = file.read()
        assert "Session ID: 12345" in content
        assert "Total Images Processed: 100" in content
        assert "Total Images Deleted: 25" in content


def test_generate_report_empty(temp_report_dir):
    report_path = os.path.join(temp_report_dir, "empty_report.txt")
    reports_manager = ReportsManager(report_path)
    
    reports_manager.generate_report("", 0, 0)
    
    with open(report_path, "r") as file:
        content = file.read()
        assert "Session ID: " in content
        assert "Total Images Processed: 0" in content
        assert "Total Images Deleted: 0" in content
