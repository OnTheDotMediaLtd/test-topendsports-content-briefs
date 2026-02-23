"""
Tests for content-briefs-skill/scripts/validate_feedback.py

Tests feedback validation functionality including:
- Complete feedback file validation
- Missing required fields detection
- Unfilled placeholder detection
- Warning detection for incomplete sections
- Edge cases and special scenarios
"""

import pytest
import sys
import importlib.util
from pathlib import Path
from unittest.mock import Mock, patch

# Load validate_feedback from content-briefs-skill/scripts/ explicitly
# to avoid collision with scripts/validate_feedback.py (different module)
SCRIPT_DIR = Path(__file__).parent.parent.parent / "content-briefs-skill" / "scripts"
_spec = importlib.util.spec_from_file_location(
    "cbs_validate_feedback",
    SCRIPT_DIR / "validate_feedback.py"
)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
validate_feedback_file = _mod.validate_feedback_file


class TestValidateFeedbackFile:
    """Test feedback file validation."""

    def test_validate_complete_feedback(self, feedback_file):
        """Test validation of complete feedback file."""
        issues, warnings = validate_feedback_file(feedback_file)

        assert len(issues) == 0
        # May have some warnings about priority items
        assert isinstance(warnings, list)

    def test_validate_incomplete_feedback(self, temp_dir, incomplete_feedback):
        """Test validation of incomplete feedback file."""
        feedback_file = temp_dir / "incomplete.md"
        feedback_file.write_text(incomplete_feedback)

        issues, warnings = validate_feedback_file(feedback_file)

        # Should have issues for missing Brief ID field
        assert len(issues) > 0
        assert any("Brief ID" in issue for issue in issues)

    def test_missing_brief_id(self, temp_dir):
        """Test detection of missing Brief ID."""
        content = """# Content Brief Feedback

**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("Brief ID" in issue for issue in issues)

    def test_missing_date_generated(self, temp_dir):
        """Test detection of missing Date Generated."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("Date Generated" in issue for issue in issues)

    def test_unfilled_placeholder_brief_id(self, temp_dir):
        """Test detection of unfilled Brief ID placeholder."""
        content = """# Content Brief Feedback

**Brief ID**: [e.g., nfl-betting-sites]
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("Brief ID" in issue for issue in issues)

    def test_unfilled_placeholder_date(self, temp_dir):
        """Test detection of unfilled date placeholder."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: [YYYY-MM-DD]
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("Date Generated" in issue for issue in issues)

    def test_unfilled_reviewer_name(self, temp_dir):
        """Test detection of unfilled reviewer name."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: [Your name]
**Reviewer Role**: Writer
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("Reviewer Name" in issue for issue in issues)

    def test_unfilled_reviewer_role(self, temp_dir):
        """Test detection of unfilled reviewer role."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: [Writer / SEO Manager / Editor / Other]
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("Reviewer Role" in issue for issue in issues)


class TestOverallRating:
    """Test overall rating validation."""

    def test_no_rating_selected(self, temp_dir):
        """Test warning when no rating is selected."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## Overall Rating

- [ ] 1 - Poor
- [ ] 2 - Needs Work
- [ ] 3 - Good
- [ ] 4 - Very Good
- [ ] 5 - Excellent
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("rating not selected" in warning.lower() for warning in warnings)

    def test_rating_selected(self, temp_dir):
        """Test no warning when rating is selected."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## Overall Rating

- [ ] 1 - Poor
- [ ] 2 - Needs Work
- [X] 3 - Good
- [ ] 4 - Very Good
- [ ] 5 - Excellent
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert not any("rating not selected" in warning.lower() for warning in warnings)

    def test_rating_case_insensitive(self, temp_dir):
        """Test rating detection is case insensitive."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## Overall Rating

- [ ] 1 - poor
- [x] 2 - needs work
- [ ] 3 - good
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert not any("rating not selected" in warning.lower() for warning in warnings)


class TestWhatWorkedWell:
    """Test 'What Worked Well' section validation."""

    def test_empty_what_worked_well(self, temp_dir):
        """Test warning when 'What Worked Well' is empty."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## What Worked Well

## What Needs Improvement
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("What Worked Well" in warning for warning in warnings)

    def test_filled_what_worked_well(self, temp_dir):
        """Test no warning when 'What Worked Well' has items."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## What Worked Well

1. Great keyword research
2. Clear structure

## What Needs Improvement
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert not any("What Worked Well" in warning for warning in warnings)


class TestWhatNeedsImprovement:
    """Test 'What Needs Improvement' section validation."""

    def test_empty_what_needs_improvement(self, temp_dir):
        """Test warning when 'What Needs Improvement' is empty."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## What Worked Well

1. Good keywords

## What Needs Improvement

## Actionable Changes
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("What Needs Improvement" in warning for warning in warnings)

    def test_filled_what_needs_improvement(self, temp_dir):
        """Test no warning when 'What Needs Improvement' has items."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## What Worked Well

1. Good keywords

## What Needs Improvement

1. Fix H3 structure
2. Add more FAQs
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert not any("What Needs Improvement" in warning for warning in warnings)


class TestPriorityItems:
    """Test priority items detection."""

    def test_priority1_items_warning(self, temp_dir):
        """Test warning when Priority 1 items exist."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## Actionable Changes

**Priority 1 (Critical)**:

1. Fix broken links
2. Update outdated information

**Priority 2 (Important)**:

1. Add more examples
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert any("Priority 1" in warning for warning in warnings)
        assert any("2" in warning or "items" in warning for warning in warnings)

    def test_no_priority1_items(self, temp_dir):
        """Test no warning when no Priority 1 items."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## Actionable Changes

**Priority 1 (Critical)**:

**Priority 2 (Important)**:

1. Add more examples
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert not any("Priority 1" in warning and "items found" in warning
                      for warning in warnings)


class TestStatusField:
    """Test status field handling."""

    def test_submitted_status_accepted(self, temp_dir):
        """Test that SUBMITTED status is accepted for new submissions."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer
**Status**: SUBMITTED
"""
        feedback_file = temp_dir / "test.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        # SUBMITTED status should not generate errors
        assert not any("Status" in issue for issue in issues)


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_file(self, temp_dir):
        """Test validation of empty file."""
        feedback_file = temp_dir / "empty.md"
        feedback_file.write_text("")

        issues, warnings = validate_feedback_file(feedback_file)

        # Should have issues for all missing fields
        assert len(issues) >= 5

    def test_minimal_valid_feedback(self, temp_dir):
        """Test minimal valid feedback file."""
        content = """# Content Brief Feedback

**Brief ID**: test-brief
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: Test User
**Reviewer Role**: Writer

## Overall Rating

- [X] 3 - Good

## What Worked Well

1. Something worked

## What Needs Improvement

1. Something to improve
"""
        feedback_file = temp_dir / "minimal.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        assert len(issues) == 0

    def test_multiple_sections(self, temp_dir):
        """Test feedback with multiple sections."""
        content = """# Content Brief Feedback

**Brief ID**: test-brief
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: Test User
**Reviewer Role**: Writer

## Overall Rating

- [X] 4 - Very Good

## What Worked Well

1. Item 1
2. Item 2
3. Item 3

## What Needs Improvement

1. Issue 1
2. Issue 2

## Additional Comments

Some additional notes here.

## Actionable Changes

**Priority 1 (Critical)**:

1. Critical fix

**Priority 2 (Important)**:

1. Important update
2. Another update

**Priority 3 (Nice to Have)**:

1. Enhancement
"""
        feedback_file = temp_dir / "multiple.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        # Should have warning about Priority 1 items
        assert any("Priority 1" in warning for warning in warnings)
        # But no issues
        assert len(issues) == 0

    def test_special_characters_in_fields(self, temp_dir):
        """Test fields with special characters."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites-2025
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: O'Connor & Smith
**Reviewer Role**: Writer / Editor
"""
        feedback_file = temp_dir / "special.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        # Should be valid despite special characters
        assert not any("Brief ID" in issue for issue in issues)
        assert not any("Reviewer Name" in issue for issue in issues)

    def test_markdown_links_in_content(self, temp_dir):
        """Test content with markdown links."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## What Worked Well

1. Good reference to [Ahrefs](https://ahrefs.com)
2. Used proper [markdown formatting](https://example.com)
"""
        feedback_file = temp_dir / "links.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        # Should handle markdown links fine
        assert not any("What Worked Well" in warning for warning in warnings)

    def test_unicode_in_feedback(self, temp_dir):
        """Test feedback with Unicode characters."""
        content = """# Content Brief Feedback

**Brief ID**: café-review
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: José García
**Reviewer Role**: Writer

## What Worked Well

1. Good use of Unicode: café, naïve, résumé
"""
        feedback_file = temp_dir / "unicode.md"
        feedback_file.write_text(content, encoding='utf-8')

        issues, warnings = validate_feedback_file(feedback_file)

        # Should handle Unicode properly
        assert not any("Brief ID" in issue for issue in issues)
        assert not any("Reviewer Name" in issue for issue in issues)

    def test_multiline_values(self, temp_dir):
        """Test fields that might span multiple lines."""
        content = """# Content Brief Feedback

**Brief ID**: nfl-betting-sites
**Date Generated**: 2025-12-01
**Date Reviewed**: 2025-12-08
**Reviewer Name**: John Doe
**Reviewer Role**: Writer

## What Worked Well

1. This is a very long item that describes
   something that worked well in detail
   across multiple lines

## What Needs Improvement

1. Short item
"""
        feedback_file = temp_dir / "multiline.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        # Should handle multiline items
        assert not any("What Worked Well" in warning for warning in warnings)

    def test_extra_whitespace(self, temp_dir):
        """Test handling of extra whitespace in fields."""
        content = """# Content Brief Feedback

**Brief ID**:    nfl-betting-sites
**Date Generated**:   2025-12-01
**Date Reviewed**:  2025-12-08
**Reviewer Name**:  John Doe
**Reviewer Role**:   Writer
"""
        feedback_file = temp_dir / "whitespace.md"
        feedback_file.write_text(content)

        issues, warnings = validate_feedback_file(feedback_file)

        # Should handle extra whitespace
        assert not any("Brief ID" in issue for issue in issues)
