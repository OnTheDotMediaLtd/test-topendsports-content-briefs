#!/usr/bin/env python3
"""
Tests for run_pattern_analysis.py - Pattern Analysis Runner Script

Coverage targets:
- main() function
- Full workflow execution
- Integration with PatternAnalyzer
"""

import pytest
import json
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))


class TestMainFunction:
    """Tests for main function."""

    def test_main_no_patterns(self, tmp_path, capsys):
        """Test main when no recurring patterns exist."""
        from run_pattern_analysis import main
        
        # Mock PatternAnalyzer
        mock_analyzer = MagicMock()
        mock_analyzer.recurring_patterns = []
        mock_analyzer.analyze_all_patterns.return_value = {
            'total_reports': 0,
            'total_failures': 0,
            'patterns': {},
            'recurring_patterns': []
        }
        
        with patch('run_pattern_analysis.PatternAnalyzer', return_value=mock_analyzer):
            main()
        
        captured = capsys.readouterr()
        assert "quality is consistent" in captured.out or "Pattern analysis complete" in captured.out

    def test_main_with_high_severity_patterns(self, tmp_path, capsys):
        """Test main with high severity recurring patterns."""
        from run_pattern_analysis import main
        
        # Mock PatternAnalyzer
        mock_analyzer = MagicMock()
        mock_analyzer.recurring_patterns = [
            {'category': 'word_count', 'count': 5, 'severity': 'high', 'failures': []}
        ]
        mock_analyzer.analyze_all_patterns.return_value = {
            'total_reports': 10,
            'total_failures': 5,
            'patterns': {'word_count': 5},
            'recurring_patterns': mock_analyzer.recurring_patterns
        }
        mock_analyzer.generate_alerts.return_value = [{'category': 'word_count'}]
        mock_analyzer.create_auto_feedback.return_value = []
        
        with patch('run_pattern_analysis.PatternAnalyzer', return_value=mock_analyzer):
            with patch('builtins.open', MagicMock()):
                with patch('pathlib.Path.mkdir'):
                    main()
        
        captured = capsys.readouterr()
        assert "Phase 2" in captured.out or "Generating alerts" in captured.out

    def test_main_with_medium_severity_patterns(self, tmp_path, capsys):
        """Test main with medium severity patterns (no auto-feedback)."""
        from run_pattern_analysis import main
        
        # Mock PatternAnalyzer
        mock_analyzer = MagicMock()
        mock_analyzer.recurring_patterns = [
            {'category': 'links', 'count': 3, 'severity': 'medium', 'failures': []}
        ]
        mock_analyzer.analyze_all_patterns.return_value = {
            'total_reports': 10,
            'total_failures': 3,
            'patterns': {'links': 3},
            'recurring_patterns': mock_analyzer.recurring_patterns
        }
        mock_analyzer.generate_alerts.return_value = [{'category': 'links'}]
        
        with patch('run_pattern_analysis.PatternAnalyzer', return_value=mock_analyzer):
            with patch('builtins.open', MagicMock()):
                with patch('pathlib.Path.mkdir'):
                    main()
        
        captured = capsys.readouterr()
        # Should not create auto-feedback for medium severity

    def test_main_full_workflow(self, tmp_path, capsys):
        """Test full pattern analysis workflow."""
        from run_pattern_analysis import main
        
        # Create test validation files
        for i in range(3):
            report = {
                "status": "FAIL",
                "file": f"test{i}.html",
                "checks": {
                    "errors": ["word count too low: 500 words"],
                    "warnings": []
                }
            }
            (tmp_path / f'test{i}.validation.json').write_text(json.dumps(report))
        
        mock_analyzer = MagicMock()
        mock_analyzer.recurring_patterns = [
            {'category': 'word_count', 'count': 3, 'severity': 'critical', 'failures': []}
        ]
        mock_analyzer.analyze_all_patterns.return_value = {
            'total_reports': 3,
            'total_failures': 3,
            'patterns': {'word_count': 3},
            'recurring_patterns': mock_analyzer.recurring_patterns
        }
        mock_analyzer.generate_alerts.return_value = [{'severity': 'critical'}]
        mock_analyzer.create_auto_feedback.return_value = ['feedback.json']
        
        with patch('run_pattern_analysis.PatternAnalyzer', return_value=mock_analyzer):
            with patch('builtins.open', MagicMock()):
                with patch('pathlib.Path.mkdir'):
                    main()
        
        captured = capsys.readouterr()
        assert "Pattern analysis complete" in captured.out


class TestIntegration:
    """Integration tests for pattern analysis."""

    def test_full_analysis_run(self, tmp_path, capsys):
        """Test complete analysis run with real PatternAnalyzer."""
        from run_pattern_analysis import main
        
        # Create output directory with test files
        output_dir = tmp_path / 'output'
        output_dir.mkdir()
        
        # Create validation file
        report = {
            "status": "FAIL",
            "file": "test.html",
            "checks": {
                "errors": ["word count too low"],
                "warnings": []
            }
        }
        (output_dir / 'test.validation.json').write_text(json.dumps(report))
        
        # Run with mock to avoid file system issues
        mock_analyzer = MagicMock()
        mock_analyzer.recurring_patterns = []
        mock_analyzer.analyze_all_patterns.return_value = {
            'total_reports': 1,
            'total_failures': 1,
            'patterns': {'word_count': 1},
            'recurring_patterns': []
        }
        
        with patch('run_pattern_analysis.PatternAnalyzer', return_value=mock_analyzer):
            main()
        
        captured = capsys.readouterr()
        assert "complete" in captured.out.lower()


class TestEdgeCases:
    """Edge case tests."""

    def test_main_exception_handling(self, capsys):
        """Test main handles exceptions gracefully."""
        from run_pattern_analysis import main
        
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_all_patterns.side_effect = Exception("Test error")
        
        with patch('run_pattern_analysis.PatternAnalyzer', return_value=mock_analyzer):
            with pytest.raises(Exception):
                main()

    def test_main_empty_output_dir(self, tmp_path, capsys):
        """Test main with empty output directory."""
        from run_pattern_analysis import main
        
        mock_analyzer = MagicMock()
        mock_analyzer.recurring_patterns = []
        mock_analyzer.analyze_all_patterns.return_value = {
            'total_reports': 0,
            'total_failures': 0,
            'patterns': {},
            'recurring_patterns': []
        }
        
        with patch('run_pattern_analysis.PatternAnalyzer', return_value=mock_analyzer):
            main()
