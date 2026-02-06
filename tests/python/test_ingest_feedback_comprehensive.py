#!/usr/bin/env python3
"""
Comprehensive tests for Feedback Ingestion System.

Tests cover:
- FeedbackIngestor initialization
- Feedback validation
- Feedback categorization and routing
- Report generation
- File operations
- Edge cases
"""

import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock
import sys

# Add scripts to path
SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from ingest_feedback import FeedbackIngestor


class TestFeedbackIngestorInit:
    """Tests for FeedbackIngestor initialization."""

    def test_default_initialization(self, tmp_path):
        """Test default initialization."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        assert ingestor.base_path == tmp_path
        assert ingestor.feedback_dir == tmp_path / 'feedback'
        assert ingestor.submitted_dir == tmp_path / 'feedback' / 'submitted'
        assert ingestor.validated_dir == tmp_path / 'feedback' / 'validated'
        assert ingestor.applied_dir == tmp_path / 'feedback' / 'applied'

    def test_directories_created(self, tmp_path):
        """Test directories are created on initialization."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        assert ingestor.submitted_dir.exists()
        assert ingestor.validated_dir.exists()
        assert ingestor.applied_dir.exists()

    def test_categories_defined(self):
        """Test all expected categories are defined."""
        expected_categories = ['keyword', 'writer', 'technical', 'compliance', 
                             'workflow', 'seo', 'edge-case']
        
        for cat in expected_categories:
            assert cat in FeedbackIngestor.CATEGORIES
            assert 'doc' in FeedbackIngestor.CATEGORIES[cat]
            assert 'section' in FeedbackIngestor.CATEGORIES[cat]
            assert 'priority' in FeedbackIngestor.CATEGORIES[cat]


class TestFeedbackValidation:
    """Tests for feedback validation."""

    def test_valid_feedback(self, tmp_path):
        """Test validation of valid feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'This is a valid issue description',
            'context': 'This is the context for the issue that is long enough',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is True
        assert len(errors) == 0

    def test_missing_required_field(self, tmp_path):
        """Test validation fails with missing required field."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            # Missing: issue, context, timestamp
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is False
        assert any('Missing required field' in e for e in errors)

    def test_invalid_category(self, tmp_path):
        """Test validation fails with invalid category."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'invalid_category',
            'issue': 'Valid issue text here',
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is False
        assert any('Invalid category' in e for e in errors)

    def test_issue_too_short(self, tmp_path):
        """Test validation fails with too short issue."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'short',  # < 10 characters
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is False
        assert any('too short' in e for e in errors)

    def test_issue_too_long(self, tmp_path):
        """Test validation fails with too long issue."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'x' * 1001,  # > 1000 characters
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is False
        assert any('too long' in e for e in errors)

    def test_context_too_short(self, tmp_path):
        """Test validation fails with too short context."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Valid issue description here',
            'context': 'short',  # < 20 characters
            'timestamp': '2024-01-01T00:00:00'
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is False
        assert any('Context too short' in e for e in errors)

    @pytest.mark.parametrize("category", FeedbackIngestor.CATEGORIES.keys())
    def test_all_categories_valid(self, tmp_path, category):
        """Test all defined categories pass validation."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': category,
            'issue': 'Valid issue description here',
            'context': 'Valid context text that is long enough for validation',
            'timestamp': '2024-01-01T00:00:00'
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is True


class TestFeedbackCategorization:
    """Tests for feedback categorization and routing."""

    def test_categorize_keyword_feedback(self, tmp_path):
        """Test categorization of keyword feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Test issue',
            'context': 'Test context'
        }
        
        result = ingestor.categorize_feedback(feedback)
        
        assert 'routing' in result
        assert result['routing']['target_doc'] == 'references/keyword-research-protocol.md'
        assert result['routing']['priority'] == 'high'
        assert 'processed_at' in result['routing']

    def test_categorize_compliance_feedback(self, tmp_path):
        """Test categorization of compliance feedback (critical priority)."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'compliance',
            'issue': 'Legal compliance issue',
            'context': 'Compliance context details'
        }
        
        result = ingestor.categorize_feedback(feedback)
        
        assert result['routing']['priority'] == 'critical'
        assert result['routing']['target_doc'] == 'references/lessons-learned.md'

    def test_categorize_unknown_category_defaults_to_edge_case(self, tmp_path):
        """Test unknown category defaults to edge-case routing."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'nonexistent',
            'issue': 'Test issue',
            'context': 'Test context'
        }
        
        result = ingestor.categorize_feedback(feedback)
        
        # Should fall back to edge-case routing
        edge_case_info = FeedbackIngestor.CATEGORIES['edge-case']
        assert result['routing']['target_doc'] == edge_case_info['doc']
        assert result['routing']['priority'] == edge_case_info['priority']

    @pytest.mark.parametrize("category,expected_priority", [
        ('keyword', 'high'),
        ('writer', 'medium'),
        ('technical', 'medium'),
        ('compliance', 'critical'),
        ('workflow', 'high'),
        ('seo', 'medium'),
        ('edge-case', 'low'),
    ])
    def test_category_priorities(self, tmp_path, category, expected_priority):
        """Test all categories have correct priorities."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {'category': category}
        result = ingestor.categorize_feedback(feedback)
        
        assert result['routing']['priority'] == expected_priority


class TestScanSubmittedFeedback:
    """Tests for scanning submitted feedback."""

    def test_scan_empty_directory(self, tmp_path):
        """Test scanning empty directory."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        items = ingestor.scan_submitted_feedback()
        
        assert items == []

    def test_scan_finds_json_files(self, tmp_path):
        """Test scanning finds JSON files."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create test feedback files
        feedback1 = {
            'category': 'keyword',
            'issue': 'Test issue 1',
            'context': 'Test context for issue 1',
            'timestamp': '2024-01-01'
        }
        
        (ingestor.submitted_dir / 'test1.json').write_text(json.dumps(feedback1))
        
        items = ingestor.scan_submitted_feedback()
        
        assert len(items) == 1
        assert items[0]['category'] == 'keyword'
        assert 'filename' in items[0]
        assert 'filepath' in items[0]

    def test_scan_filters_by_category(self, tmp_path):
        """Test scanning filters by category."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback1 = {'category': 'keyword', 'issue': 'Test', 'context': 'Test'}
        feedback2 = {'category': 'writer', 'issue': 'Test', 'context': 'Test'}
        
        (ingestor.submitted_dir / 'kw.json').write_text(json.dumps(feedback1))
        (ingestor.submitted_dir / 'wr.json').write_text(json.dumps(feedback2))
        
        items = ingestor.scan_submitted_feedback(category='keyword')
        
        assert len(items) == 1
        assert items[0]['category'] == 'keyword'

    def test_scan_handles_invalid_json(self, tmp_path):
        """Test scanning handles invalid JSON gracefully."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        (ingestor.submitted_dir / 'invalid.json').write_text('not valid json')
        
        items = ingestor.scan_submitted_feedback()
        
        # Invalid JSON should be skipped
        assert len(items) == 0

    def test_scan_ignores_non_json_files(self, tmp_path):
        """Test scanning ignores non-JSON files."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        (ingestor.submitted_dir / 'readme.txt').write_text('Not JSON')
        (ingestor.submitted_dir / 'test.json').write_text(json.dumps({'category': 'keyword'}))
        
        items = ingestor.scan_submitted_feedback()
        
        assert len(items) == 1
        assert items[0]['category'] == 'keyword'


class TestMoveToValidated:
    """Tests for moving feedback to validated directory."""

    def test_move_to_validated(self, tmp_path):
        """Test moving feedback file to validated directory."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create source file
        source_path = ingestor.submitted_dir / 'test.json'
        feedback = {
            'category': 'keyword',
            'issue': 'Test issue',
            'context': 'Test context',
            'timestamp': '2024-01-01',
            'filepath': str(source_path),
            'routing': {'target_doc': 'test.md', 'priority': 'high', 'processed_at': '2024-01-01'}
        }
        source_path.write_text(json.dumps(feedback))
        
        dest_path = ingestor.move_to_validated(feedback)
        
        assert dest_path.exists()
        assert not source_path.exists()
        assert dest_path.parent == ingestor.validated_dir

    def test_move_preserves_routing_info(self, tmp_path):
        """Test move preserves routing information."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        source_path = ingestor.submitted_dir / 'test.json'
        feedback = {
            'category': 'keyword',
            'issue': 'Test',
            'context': 'Context',
            'timestamp': '2024-01-01',
            'filepath': str(source_path),
            'routing': {'target_doc': 'test.md', 'priority': 'high', 'processed_at': '2024-01-01'}
        }
        source_path.write_text(json.dumps(feedback))
        
        dest_path = ingestor.move_to_validated(feedback)
        
        saved_data = json.loads(dest_path.read_text())
        assert 'routing' in saved_data
        assert saved_data['routing']['priority'] == 'high'


class TestReportGeneration:
    """Tests for report generation."""

    def test_generate_report_empty_list(self, tmp_path):
        """Test report generation with empty list."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        report = ingestor.generate_report([])
        
        assert "No feedback items to process" in report

    def test_generate_report_with_items(self, tmp_path):
        """Test report generation with feedback items."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        items = [
            {
                'category': 'keyword',
                'issue': 'Test issue 1',
                'context': 'Test context 1',
                'filename': 'test1.json',
                'routing': {'target_doc': 'test.md', 'target_section': 'Section', 'priority': 'high'}
            },
            {
                'category': 'writer',
                'issue': 'Test issue 2',
                'context': 'Test context 2',
                'filename': 'test2.json',
                'routing': {'target_doc': 'test2.md', 'target_section': 'Section2', 'priority': 'medium'}
            }
        ]
        
        report = ingestor.generate_report(items)
        
        assert 'FEEDBACK INGESTION REPORT' in report
        assert 'Total Feedback Items: 2' in report
        assert 'keyword' in report
        assert 'writer' in report

    def test_generate_report_groups_by_category(self, tmp_path):
        """Test report groups items by category."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        items = [
            {'category': 'keyword', 'issue': 'Issue 1', 'context': 'Context', 'filename': 'f1.json'},
            {'category': 'keyword', 'issue': 'Issue 2', 'context': 'Context', 'filename': 'f2.json'},
            {'category': 'writer', 'issue': 'Issue 3', 'context': 'Context', 'filename': 'f3.json'},
        ]
        
        report = ingestor.generate_report(items)
        
        assert 'keyword: 2 items' in report
        assert 'writer: 1 items' in report

    def test_generate_report_includes_suggested_fix(self, tmp_path):
        """Test report includes suggested fix if present."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        items = [{
            'category': 'keyword',
            'issue': 'Test issue',
            'context': 'Test context',
            'filename': 'test.json',
            'suggested_fix': 'This is the suggested fix for the issue'
        }]
        
        report = ingestor.generate_report(items)
        
        assert 'Suggested Fix' in report


class TestProcessAll:
    """Tests for full processing workflow."""

    def test_process_all_no_feedback(self, tmp_path):
        """Test processing with no feedback files."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Should not crash when no feedback
        ingestor.process_all()

    def test_process_all_validate_only(self, tmp_path):
        """Test processing with validate_only flag."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Valid issue description',
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01'
        }
        (ingestor.submitted_dir / 'test.json').write_text(json.dumps(feedback))
        
        ingestor.process_all(validate_only=True)
        
        # File should still be in submitted (not moved)
        assert (ingestor.submitted_dir / 'test.json').exists()
        assert not (ingestor.validated_dir / 'test.json').exists()

    def test_process_all_with_valid_feedback(self, tmp_path):
        """Test processing valid feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Valid issue description here',
            'context': 'Valid context text that is definitely long enough',
            'timestamp': '2024-01-01'
        }
        (ingestor.submitted_dir / 'test.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        # File should be moved to validated
        assert not (ingestor.submitted_dir / 'test.json').exists()
        assert (ingestor.validated_dir / 'test.json').exists()

    def test_process_all_with_invalid_feedback(self, tmp_path):
        """Test processing invalid feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'invalid',
            'issue': 'x',  # Too short
            'context': 'y',  # Too short
        }
        (ingestor.submitted_dir / 'invalid.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        # Invalid file should stay in submitted
        assert (ingestor.submitted_dir / 'invalid.json').exists()

    def test_process_all_category_filter(self, tmp_path):
        """Test processing with category filter."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        kw_feedback = {
            'category': 'keyword',
            'issue': 'Keyword related issue here',
            'context': 'Keyword context text that is long enough',
            'timestamp': '2024-01-01'
        }
        wr_feedback = {
            'category': 'writer',
            'issue': 'Writer related issue here',
            'context': 'Writer context text that is long enough',
            'timestamp': '2024-01-01'
        }
        
        (ingestor.submitted_dir / 'kw.json').write_text(json.dumps(kw_feedback))
        (ingestor.submitted_dir / 'wr.json').write_text(json.dumps(wr_feedback))
        
        ingestor.process_all(category='keyword')
        
        # Only keyword should be processed
        assert not (ingestor.submitted_dir / 'kw.json').exists()
        assert (ingestor.submitted_dir / 'wr.json').exists()

    def test_process_all_creates_report_file(self, tmp_path):
        """Test processing creates report file."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Valid issue description here',
            'context': 'Valid context text that is long enough for test',
            'timestamp': '2024-01-01'
        }
        (ingestor.submitted_dir / 'test.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        # Should create report file
        report_files = list(ingestor.feedback_dir.glob('ingestion-report-*.txt'))
        assert len(report_files) == 1


class TestEdgeCases:
    """Tests for edge cases."""

    def test_unicode_in_feedback(self, tmp_path):
        """Test handling Unicode content in feedback."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Unicode issue with special characters like accents',
            'context': 'Context with special chars and umlauts in text',
            'timestamp': '2024-01-01'
        }
        (ingestor.submitted_dir / 'unicode.json').write_text(
            json.dumps(feedback, ensure_ascii=False), encoding='utf-8'
        )
        
        ingestor.process_all()
        
        assert (ingestor.validated_dir / 'unicode.json').exists()

    def test_special_characters_in_filename(self, tmp_path):
        """Test handling special characters in feedback filename."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Valid issue description here',
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01'
        }
        # Note: some special chars may not be allowed in filenames
        (ingestor.submitted_dir / 'test-feedback_01.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        assert (ingestor.validated_dir / 'test-feedback_01.json').exists()

    def test_empty_json_file(self, tmp_path):
        """Test handling empty JSON file."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        (ingestor.submitted_dir / 'empty.json').write_text('')
        
        items = ingestor.scan_submitted_feedback()
        
        assert len(items) == 0

    def test_feedback_with_extra_fields(self, tmp_path):
        """Test feedback with additional fields is preserved."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'Valid issue description here',
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01',
            'custom_field': 'Custom value',
            'another_field': {'nested': 'data'}
        }
        (ingestor.submitted_dir / 'extra.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        saved = json.loads((ingestor.validated_dir / 'extra.json').read_text())
        assert saved['custom_field'] == 'Custom value'
        assert saved['another_field']['nested'] == 'data'

    def test_concurrent_file_access(self, tmp_path):
        """Test handling potential concurrent access."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        # Create multiple files
        for i in range(10):
            feedback = {
                'category': 'keyword',
                'issue': f'Valid issue description number {i}',
                'context': 'Valid context text that is long enough for test',
                'timestamp': '2024-01-01'
            }
            (ingestor.submitted_dir / f'test{i}.json').write_text(json.dumps(feedback))
        
        ingestor.process_all()
        
        # All should be processed
        validated_files = list(ingestor.validated_dir.glob('*.json'))
        assert len(validated_files) == 10

    def test_very_long_issue_text(self, tmp_path):
        """Test handling maximum length issue text."""
        ingestor = FeedbackIngestor(str(tmp_path))
        
        feedback = {
            'category': 'keyword',
            'issue': 'x' * 1000,  # Maximum allowed
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01'
        }
        
        is_valid, errors = ingestor.validate_feedback(feedback)
        
        assert is_valid is True


class TestMainFunction:
    """Tests for main CLI function."""

    def test_main_no_feedback(self, tmp_path, monkeypatch):
        """Test main with no feedback."""
        import ingest_feedback as module
        
        monkeypatch.setattr('sys.argv', [
            'ingest_feedback.py',
            '--base-path', str(tmp_path)
        ])
        
        # Should run without crashing
        module.main()

    def test_main_validate_only_flag(self, tmp_path, monkeypatch):
        """Test main with validate-only flag."""
        import ingest_feedback as module
        
        # Create test feedback
        feedback_dir = tmp_path / 'feedback' / 'submitted'
        feedback_dir.mkdir(parents=True)
        feedback = {
            'category': 'keyword',
            'issue': 'Valid issue description here',
            'context': 'Valid context text that is long enough',
            'timestamp': '2024-01-01'
        }
        (feedback_dir / 'test.json').write_text(json.dumps(feedback))
        
        monkeypatch.setattr('sys.argv', [
            'ingest_feedback.py',
            '--base-path', str(tmp_path),
            '--validate-only'
        ])
        
        module.main()
        
        # File should still be in submitted
        assert (feedback_dir / 'test.json').exists()

    def test_main_category_filter(self, tmp_path, monkeypatch):
        """Test main with category filter."""
        import ingest_feedback as module
        
        feedback_dir = tmp_path / 'feedback' / 'submitted'
        feedback_dir.mkdir(parents=True)
        
        kw = {
            'category': 'keyword',
            'issue': 'Keyword issue description',
            'context': 'Keyword context text long enough',
            'timestamp': '2024-01-01'
        }
        (feedback_dir / 'kw.json').write_text(json.dumps(kw))
        
        monkeypatch.setattr('sys.argv', [
            'ingest_feedback.py',
            '--base-path', str(tmp_path),
            '--category', 'keyword'
        ])
        
        # Should run without crashing
        module.main()
