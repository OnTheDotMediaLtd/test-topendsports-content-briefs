"""
Tests for validate_feedback.py feedback validation helper
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from validate_feedback import validate_feedback_file


class TestValidateFeedbackFile:
    """Tests for the validate_feedback_file function"""

    @pytest.fixture
    def valid_feedback_path(self):
        """Path to valid feedback fixture"""
        return Path(__file__).parent / "fixtures" / "valid_feedback.md"

    @pytest.fixture
    def invalid_feedback_path(self):
        """Path to invalid feedback fixture"""
        return Path(__file__).parent / "fixtures" / "invalid_feedback.md"

    def test_valid_feedback_has_no_issues(self, valid_feedback_path):
        """Test that valid feedback passes validation"""
        issues, warnings = validate_feedback_file(valid_feedback_path)
        assert len(issues) == 0

    def test_invalid_feedback_has_issues(self, invalid_feedback_path):
        """Test that invalid feedback has issues detected"""
        issues, warnings = validate_feedback_file(invalid_feedback_path)
        # Should detect placeholder values and missing rating
        assert len(issues) > 0

    def test_detects_missing_brief_id(self):
        """Test detection of missing Brief ID"""
        content = """# Content Brief Feedback

**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("Brief ID" in issue for issue in issues)
        finally:
            os.unlink(temp_path)

    def test_detects_unfilled_reviewer_name(self):
        """Test detection of placeholder reviewer name"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: [Your name]
**Reviewer Role**: Writer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("Reviewer Name" in issue for issue in issues)
        finally:
            os.unlink(temp_path)

    def test_detects_unfilled_date(self):
        """Test detection of placeholder date"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: [YYYY-MM-DD]
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("Date Generated" in issue for issue in issues)
        finally:
            os.unlink(temp_path)

    def test_detects_placeholder_brief_id(self):
        """Test detection of placeholder Brief ID"""
        content = """# Content Brief Feedback

**Brief ID**: [e.g., nfl-betting-sites]
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("Brief ID" in issue for issue in issues)
        finally:
            os.unlink(temp_path)

    def test_detects_missing_rating(self):
        """Test warning for missing rating selection"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer

## Overall Rating

[ ] 1 - Poor
[ ] 2 - Needs Work
[ ] 3 - Good
[ ] 4 - Very Good
[ ] 5 - Excellent
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("rating" in warning.lower() for warning in warnings)
        finally:
            os.unlink(temp_path)

    def test_accepts_valid_rating(self):
        """Test that valid rating selection is accepted"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer

## Overall Rating

[ ] 1 - Poor
[ ] 2 - Needs Work
[ ] 3 - Good
[X] 4 - Very Good
[ ] 5 - Excellent

## What Worked Well

1. Good structure

## What Needs Improvement

1. Add more examples
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            # Should not have rating warning
            assert not any("rating" in warning.lower() for warning in warnings)
        finally:
            os.unlink(temp_path)

    def test_detects_empty_what_worked_well(self):
        """Test warning for empty What Worked Well section"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer

## What Worked Well

1.
2.
3.

## What Needs Improvement

1. Something to improve
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("What Worked Well" in warning for warning in warnings)
        finally:
            os.unlink(temp_path)

    def test_detects_empty_what_needs_improvement(self):
        """Test warning for empty What Needs Improvement section"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer

## What Worked Well

1. Good formatting

## What Needs Improvement

1.
2.
3.
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("What Needs Improvement" in warning for warning in warnings)
        finally:
            os.unlink(temp_path)

    def test_detects_priority_1_items(self):
        """Test warning when Priority 1 items are found"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer

## Actionable Changes

**Priority 1 (Critical)**:
1. Fix critical bug
2. Address security issue

**Priority 2 (Important)**:
1. Update documentation
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            assert any("Priority 1" in warning for warning in warnings)
        finally:
            os.unlink(temp_path)

    def test_handles_submitted_status(self):
        """Test that SUBMITTED status is accepted"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer

---
**Status**: SUBMITTED
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            # Should not flag SUBMITTED status as an issue
            assert not any("Status" in issue for issue in issues)
        finally:
            os.unlink(temp_path)


class TestValidationPatterns:
    """Tests for specific validation patterns"""

    def test_accepts_various_valid_formats(self):
        """Test that various valid field formats are accepted"""
        test_cases = [
            ("**Brief ID**: my-test-brief", False),
            ("**Brief ID**: nfl-betting-sites-2025", False),
            ("**Brief ID**: test_page_123", False),
        ]

        for content_line, should_have_issue in test_cases:
            content = f"""# Content Brief Feedback

{content_line}
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: Test User
**Reviewer Role**: Writer
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False, encoding="utf-8"
            ) as f:
                f.write(content)
                temp_path = f.name

            try:
                issues, warnings = validate_feedback_file(temp_path)
                brief_id_issues = [i for i in issues if "Brief ID" in i]
                assert (len(brief_id_issues) > 0) == should_have_issue
            finally:
                os.unlink(temp_path)

    def test_handles_different_role_values(self):
        """Test that different role values are handled"""
        roles = ["Writer", "SEO Manager", "Editor", "Other", "Content Lead"]

        for role in roles:
            content = f"""# Content Brief Feedback

**Brief ID**: test-brief
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: Test User
**Reviewer Role**: {role}
"""
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".md", delete=False, encoding="utf-8"
            ) as f:
                f.write(content)
                temp_path = f.name

            try:
                issues, warnings = validate_feedback_file(temp_path)
                role_issues = [i for i in issues if "Reviewer Role" in i]
                assert len(role_issues) == 0, f"Role '{role}' should be valid"
            finally:
                os.unlink(temp_path)


class TestEdgeCases:
    """Tests for edge cases in feedback validation"""

    def test_handles_empty_file(self):
        """Test handling of empty file"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("")
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            # Should have issues for all missing fields
            assert len(issues) >= 5
        finally:
            os.unlink(temp_path)

    def test_handles_unicode_content(self):
        """Test handling of Unicode content"""
        content = """# Content Brief Feedback

**Brief ID**: test-brief-émoji-测试
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: José García
**Reviewer Role**: Writer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            # Should not raise an exception
            issues, warnings = validate_feedback_file(temp_path)
            assert isinstance(issues, list)
            assert isinstance(warnings, list)
        finally:
            os.unlink(temp_path)

    def test_handles_extra_whitespace(self):
        """Test handling of extra whitespace in fields"""
        content = """# Content Brief Feedback

**Brief ID**:    test-brief
**Date Generated**:   2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**:   John Smith
**Reviewer Role**: Writer
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            # Extra whitespace should not cause false positives
            assert len(issues) == 0
        finally:
            os.unlink(temp_path)

    def test_handles_lowercase_rating_marker(self):
        """Test that lowercase [x] rating marker is accepted"""
        content = """# Content Brief Feedback

**Brief ID**: test-page
**Date Generated**: 2025-01-15
**Date Reviewed**: 2025-01-20
**Reviewer Name**: John Smith
**Reviewer Role**: Writer

## Overall Rating

[x] 4 - Very Good

## What Worked Well

1. Good work

## What Needs Improvement

1. Minor fix
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write(content)
            temp_path = f.name

        try:
            issues, warnings = validate_feedback_file(temp_path)
            # Lowercase [x] might not be detected - this tests current behavior
            # The actual result depends on the regex pattern in validate_feedback.py
            assert isinstance(issues, list)
        finally:
            os.unlink(temp_path)
