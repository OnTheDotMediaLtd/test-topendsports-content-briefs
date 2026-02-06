#!/usr/bin/env python3
"""
Tests for ingest_feedback.py - Feedback Ingestion System

Coverage targets:
- FeedbackIngestor class initialization
- scan_submitted_feedback() method
- validate_feedback() method
- categorize_feedback() method
- move_to_validated() method
- generate_report() method
- process_all() method
- main() function
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from ingest_feedback import FeedbackIngestor, main


class TestFeedbackIngestorInit:
    """Tests for FeedbackIngestor initialization."""

    def test_init_creates_directories(self, tmp_path):
        """Test that initialization creates required directories."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        assert (tmp_path / 'feedback' / 'submitted').exists()
        assert (tmp_path / 'feedback' / 'validated').exists()
        assert (tmp_path / 'feedback' / 'applied').exists()

    def test_init_with_existing_directories(self, tmp_path):
        """Test initialization with pre-existing directories."""
        (tmp_path / 'feedback' / 'submitted').mkdir(parents=True)
        
        ingestor = FeedbackIngestor(str(tmp_path))
        assert ingestor.submitted_dir.exists()

    def test_categories_defined(self, tmp_path):
        """Test that all expected categories are defined."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        expected_categories = [
            'keyword', 'writer', 'technical', 'compliance',
            'workflow', 'seo', 'edge-case'
        ]
        for cat in expected_categories:
            assert cat in FeedbackIngestor.CATEGORIES


class TestScanSubmittedFeedback:
    """Tests for scan_submitted_feedback method."""

    def test_scan_empty_directory(self, tmp_path):
        """Test scanning empty submitted directory."""
        ingestor = FeedbackIngestor(str(tmp_path))
        result = ingestor.scan_submitted_feedback()
        assert result == []

    def test_scan_with_valid_feedback(self, tmp_path):
        """Test scanning with valid feedback files."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create test feedback file
        feedback = {
            "category": "keyword",
            "issue": "Test issue description",
            "context": "Test context for the feedback",
            "timestamp": datetime.now().isoformat()
        }
        feedback_file = ingestor.submitted_dir / 'test-feedback.json'
        feedback_file.write_text(json.dumps(feedback))
        
        result = ingestor.scan_submitted_feedback()
        assert len(result) == 1
        assert result[0]['category'] == 'keyword'

    def test_scan_with_category_filter(self, tmp_path):
        """Test scanning with category filter."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create feedback files with different categories
        for i, cat in enumerate(['keyword', 'writer', 'technical']):
            feedback = {
                "category": cat,
                "issue": f"Issue {i}",
                "context": f"Context {i}" * 5,
                "timestamp": datetime.now().isoformat()
            }
            (ingestor.submitted_dir / f'feedback-{i}.json').write_text(json.dumps(feedback))
        
        result = ingestor.scan_submitted_feedback(category='keyword')
        assert len(result) == 1
        assert result[0]['category'] == 'keyword'

    def test_scan_handles_invalid_json(self, tmp_path):
        """Test scanning handles invalid JSON files gracefully."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create invalid JSON file
        (ingestor.submitted_dir / 'invalid.json').write_text('not valid json')
        
        # Create valid file
        valid_feedback = {
            "category": "keyword",
            "issue": "Valid issue",
            "context": "Valid context here",
            "timestamp": datetime.now().isoformat()
        }
        (ingestor.submitted_dir / 'valid.json').write_text(json.dumps(valid_feedback))
        
        result = ingestor.scan_submitted_feedback()
        assert len(result) == 1  # Only valid file


class TestValidateFeedback:
    """Tests for validate_feedback method."""

    def test_validate_valid_feedback(self, tmp_path):
        """Test validation of valid feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "keyword",
            "issue": "This is a valid issue description",
            "context": "This is valid context that is long enough",
            "timestamp": datetime.now().isoformat()
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is True
        assert len(errors) == 0

    def test_validate_missing_required_fields(self, tmp_path):
        """Test validation with missing required fields."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {"category": "keyword"}  # Missing other fields
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is False
        assert any("Missing required field" in e for e in errors)

    def test_validate_invalid_category(self, tmp_path):
        """Test validation with invalid category."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "invalid_category",
            "issue": "Valid issue description",
            "context": "Valid context description here",
            "timestamp": datetime.now().isoformat()
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is False
        assert any("Invalid category" in e for e in errors)

    def test_validate_issue_too_short(self, tmp_path):
        """Test validation with issue description too short."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "keyword",
            "issue": "Short",  # Less than 10 chars
            "context": "Valid context description here",
            "timestamp": datetime.now().isoformat()
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is False
        assert any("too short" in e for e in errors)

    def test_validate_issue_too_long(self, tmp_path):
        """Test validation with issue description too long."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "keyword",
            "issue": "x" * 1001,  # Over 1000 chars
            "context": "Valid context description here",
            "timestamp": datetime.now().isoformat()
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is False
        assert any("too long" in e for e in errors)

    def test_validate_context_too_short(self, tmp_path):
        """Test validation with context too short."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "keyword",
            "issue": "Valid issue description",
            "context": "Short",  # Less than 20 chars
            "timestamp": datetime.now().isoformat()
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is False
        assert any("Context too short" in e for e in errors)


class TestCategorizeFeedback:
    """Tests for categorize_feedback method."""

    def test_categorize_known_category(self, tmp_path):
        """Test categorizing feedback with known category."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {"category": "keyword"}
        result = ingestor.categorize_feedback(feedback)
        
        assert 'routing' in result
        assert result['routing']['target_doc'] == 'references/keyword-research-protocol.md'
        assert result['routing']['priority'] == 'high'

    def test_categorize_edge_case_category(self, tmp_path):
        """Test categorizing edge-case feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {"category": "edge-case"}
        result = ingestor.categorize_feedback(feedback)
        
        assert result['routing']['priority'] == 'low'

    def test_categorize_unknown_category(self, tmp_path):
        """Test categorizing feedback with unknown category."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {"category": "unknown"}
        result = ingestor.categorize_feedback(feedback)
        
        # Should default to edge-case
        assert 'routing' in result

    def test_categorize_adds_timestamp(self, tmp_path):
        """Test that categorization adds processed_at timestamp."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {"category": "writer"}
        result = ingestor.categorize_feedback(feedback)
        
        assert 'processed_at' in result['routing']


class TestMoveToValidated:
    """Tests for move_to_validated method."""

    def test_move_valid_feedback(self, tmp_path):
        """Test moving feedback to validated directory."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create feedback file
        feedback = {
            "category": "keyword",
            "issue": "Test issue",
            "filepath": str(ingestor.submitted_dir / 'test.json')
        }
        (ingestor.submitted_dir / 'test.json').write_text('{}')
        
        # Add routing info
        feedback['routing'] = {
            'target_doc': 'test.md',
            'target_section': 'Test',
            'priority': 'high',
            'processed_at': datetime.now().isoformat()
        }
        
        dest_path = ingestor.move_to_validated(feedback)
        
        assert dest_path.exists()
        assert not (ingestor.submitted_dir / 'test.json').exists()


class TestGenerateReport:
    """Tests for generate_report method."""

    def test_generate_report_empty(self, tmp_path):
        """Test generating report with no items."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        result = ingestor.generate_report([])
        assert "No feedback items" in result

    def test_generate_report_with_items(self, tmp_path):
        """Test generating report with feedback items."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback_items = [
            {
                "category": "keyword",
                "issue": "Test issue 1",
                "context": "Test context 1",
                "filename": "test1.json",
                "routing": {
                    "target_doc": "test.md",
                    "target_section": "Test",
                    "priority": "high",
                    "processed_at": datetime.now().isoformat()
                }
            }
        ]
        
        result = ingestor.generate_report(feedback_items)
        
        assert "FEEDBACK INGESTION REPORT" in result
        assert "keyword" in result
        assert "Total Feedback Items: 1" in result

    def test_generate_report_with_suggested_fix(self, tmp_path):
        """Test report includes suggested fixes."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback_items = [
            {
                "category": "technical",
                "issue": "Test issue",
                "context": "Test context",
                "suggested_fix": "This is the suggested fix for the issue",
                "filename": "test.json"
            }
        ]
        
        result = ingestor.generate_report(feedback_items)
        assert "Suggested Fix" in result


class TestProcessAll:
    """Tests for process_all method."""

    def test_process_all_no_feedback(self, tmp_path, capsys):
        """Test processing when no feedback exists."""
        ingestor = FeedbackIngestor(str(tmp_path))
        ingestor.process_all()
        
        captured = capsys.readouterr()
        assert "No feedback to process" in captured.out

    def test_process_all_with_valid_feedback(self, tmp_path, capsys):
        """Test processing valid feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create valid feedback
        feedback = {
            "category": "keyword",
            "issue": "This is a test issue description",
            "context": "This is the context for the test issue",
            "timestamp": datetime.now().isoformat()
        }
        (ingestor.submitted_dir / 'test.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        captured = capsys.readouterr()
        assert "Valid" in captured.out or "valid" in captured.out

    def test_process_all_validate_only(self, tmp_path, capsys):
        """Test process_all with validate_only flag."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create feedback
        feedback = {
            "category": "keyword",
            "issue": "This is a test issue description",
            "context": "This is the context for the test issue",
            "timestamp": datetime.now().isoformat()
        }
        (ingestor.submitted_dir / 'test.json').write_text(json.dumps(feedback))
        
        ingestor.process_all(validate_only=True)
        
        # File should still be in submitted (not moved)
        assert (ingestor.submitted_dir / 'test.json').exists()

    def test_process_all_with_invalid_feedback(self, tmp_path, capsys):
        """Test processing invalid feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create invalid feedback
        feedback = {"category": "invalid"}
        (ingestor.submitted_dir / 'invalid.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        captured = capsys.readouterr()
        assert "failed validation" in captured.out.lower() or "invalid" in captured.out.lower()


class TestMainFunction:
    """Tests for main function."""

    def test_main_with_category_filter(self, tmp_path):
        """Test main with category filter argument."""
        with patch('sys.argv', ['ingest_feedback.py', '--category', 'keyword', '--base-path', str(tmp_path)]):
            main()

    def test_main_with_validate_only(self, tmp_path):
        """Test main with validate-only flag."""
        with patch('sys.argv', ['ingest_feedback.py', '--validate-only', '--base-path', str(tmp_path)]):
            main()


class TestEdgeCases:
    """Edge case tests."""

    def test_unicode_feedback(self, tmp_path):
        """Test handling unicode in feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "keyword",
            "issue": "Issue with émojis 🎉 and 日本語",
            "context": "Context with special chars: àéïõü",
            "timestamp": datetime.now().isoformat()
        }
        (ingestor.submitted_dir / 'unicode.json').write_text(
            json.dumps(feedback, ensure_ascii=False),
            encoding='utf-8'
        )
        
        result = ingestor.scan_submitted_feedback()
        assert len(result) == 1

    def test_empty_strings_in_feedback(self, tmp_path):
        """Test validation with empty strings."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "keyword",
            "issue": "",
            "context": "",
            "timestamp": ""
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is False

    def test_whitespace_only_fields(self, tmp_path):
        """Test validation with whitespace-only fields."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "keyword",
            "issue": "   ",
            "context": "   ",
            "timestamp": datetime.now().isoformat()
        }
        
        # The validator checks for strip(), so whitespace should fail
        is_valid, errors = ingestor.validate_feedback(feedback)
        # Issue is too short after stripping
        assert is_valid is False

    def test_multiple_categories_same_priority(self, tmp_path):
        """Test processing multiple feedback items with same priority."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        for i in range(3):
            feedback = {
                "category": "writer",  # All same category
                "issue": f"Issue number {i} description",
                "context": f"Context for issue {i} here",
                "timestamp": datetime.now().isoformat()
            }
            (ingestor.submitted_dir / f'feedback-{i}.json').write_text(json.dumps(feedback))
        
        items = ingestor.scan_submitted_feedback()
        assert len(items) == 3

    def test_large_feedback_file(self, tmp_path):
        """Test handling large feedback content."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            "category": "technical",
            "issue": "A" * 500,  # 500 chars (under 1000 limit)
            "context": "B" * 500,  # 500 chars
            "timestamp": datetime.now().isoformat()
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        assert is_valid is True
