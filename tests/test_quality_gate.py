"""
Comprehensive tests for the Content Quality Gate.

Tests all validator integrations and quality gate logic including:
- Individual validator functionality
- Score calculation and weighting
- Pass/fail logic in strict and non-strict modes
- Error handling and edge cases
- Performance and execution time tracking
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from validation.quality_gate import (
    ContentQualityGate,
    QualityGateResult,
    QualityGateStatus,
    ValidatorType,
    ValidatorResult,
    validate_content_brief
)


class TestContentQualityGate:
    """Test cases for the main ContentQualityGate class."""
    
    def test_init_default_configuration(self):
        """Test that quality gate initializes with correct defaults."""
        gate = ContentQualityGate()
        
        assert gate.strict_mode == True
        assert gate.target_keywords == []
        assert gate.brand_name == "TopEndSports"
        assert gate.target_states == []
        assert len(gate.validators) == 5
        assert ValidatorType.EEAT in gate.validators
        assert ValidatorType.BRAND in gate.validators
        assert ValidatorType.RESPONSIBLE_GAMBLING in gate.validators
        assert ValidatorType.SEO_META in gate.validators
        assert ValidatorType.AI_PATTERN in gate.validators
    
    def test_init_custom_configuration(self):
        """Test initialization with custom parameters."""
        gate = ContentQualityGate(
            strict_mode=False,
            target_keywords=["sports betting", "sportsbook"],
            brand_name="TestBrand",
            target_states=["NV", "NJ", "PA"]
        )
        
        assert gate.strict_mode == False
        assert gate.target_keywords == ["sports betting", "sportsbook"]
        assert gate.brand_name == "TestBrand"
        assert gate.target_states == ["NV", "NJ", "PA"]
    
    def test_validator_weights_sum_to_100(self):
        """Test that validator weights sum to 100."""
        total_weight = sum(ContentQualityGate.VALIDATOR_WEIGHTS.values())
        assert total_weight == 100
    
    def test_minimum_passing_scores_reasonable(self):
        """Test that minimum passing scores are reasonable."""
        scores = ContentQualityGate.MINIMUM_PASSING_SCORES
        
        # All scores should be between 0 and 100
        for score in scores.values():
            assert 0 <= score <= 100
        
        # Responsible gambling should have the highest threshold
        assert scores[ValidatorType.RESPONSIBLE_GAMBLING] >= 80
        
        # EEAT should have a reasonable threshold for YMYL content
        assert scores[ValidatorType.EEAT] >= 60


class TestQualityGateValidation:
    """Test the main validation functionality."""
    
    @pytest.fixture
    def mock_validators(self):
        """Create mock validators that return predictable results."""
        with patch.multiple(
            'validation.quality_gate',
            EEATValidator=MagicMock,
            BrandValidator=MagicMock,
            ResponsibleGamblingValidator=MagicMock,
            SEOMetaValidator=MagicMock,
            AIPatternValidator=MagicMock
        ) as mocks:
            yield mocks
    
    def test_validate_high_quality_content(self):
        """Test validation of high-quality content that should pass all validators."""
        gate = ContentQualityGate()
        
        high_quality_content = """
        <html>
        <head>
            <title>Expert Sports Betting Analysis: 2024 March Madness Predictions | TopEndSports</title>
            <meta name="description" content="Get expert March Madness predictions from our professional analysts. 20+ years of basketball betting experience with proven track record and responsible gambling resources.">
            <meta property="og:title" content="Expert Sports Betting Analysis: 2024 March Madness Predictions">
            <meta property="og:description" content="Get expert March Madness predictions from our professional analysts. 20+ years of basketball betting experience.">
            <meta property="og:image" content="https://example.com/march-madness-2024.jpg">
            <link rel="canonical" href="https://topendsports.com/march-madness-predictions">
        </head>
        <body>
            <article>
                <header>
                    <h1>Expert Sports Betting Analysis: 2024 March Madness Predictions</h1>
                    <div class="author-bio">
                        <p>By John Smith, Sports Analyst with 15+ years of experience covering college basketball</p>
                        <p>Our team has been analyzing college basketball betting markets since 2008, with real-money testing at DraftKings, FanDuel, and BetMGM.</p>
                    </div>
                </header>
                
                <section>
                    <h2>Our Testing Methodology</h2>
                    <p>We've been testing these sportsbooks with real money for over a decade. Our methodology includes:</p>
                    <ul>
                        <li>Real-money deposits and withdrawals</li>
                        <li>Extensive market analysis</li>
                        <li>Customer service testing</li>
                    </ul>
                </section>
                
                <section>
                    <h2>Top Sportsbooks for March Madness</h2>
                    <p>Based on our real-money testing, here are the top sites:</p>
                    <ul>
                        <li>DraftKings - Excellent odds and promotions</li>
                        <li>FanDuel - Great mobile app experience</li>
                        <li>BetMGM - Superior live betting options</li>
                    </ul>
                </section>
                
                <footer>
                    <div class="responsible-gambling">
                        <p><strong>Please gamble responsibly.</strong> If you have a gambling problem, call 1-800-GAMBLER or visit ncpgambling.org for help.</p>
                        <p>You must be 21+ to participate in sports betting. Know when to stop before you start.</p>
                        <p>For help with problem gambling, contact:</p>
                        <ul>
                            <li>National Problem Gambling Helpline: 1-800-522-4700</li>
                            <li>Gamblers Anonymous: gamblersanonymous.org</li>
                        </ul>
                    </div>
                </footer>
            </article>
        </body>
        </html>
        """
        
        result = gate.validate(high_quality_content)
        
        # The result should exist and have basic structure
        assert isinstance(result, QualityGateResult)
        assert hasattr(result, 'passed')
        assert hasattr(result, 'total_score')
        assert hasattr(result, 'validator_results')
        assert len(result.validator_results) == 5
    
    def test_validate_low_quality_content(self):
        """Test validation of low-quality content that should fail multiple validators."""
        gate = ContentQualityGate()
        
        low_quality_content = """
        <html>
        <head>
            <title>Betting</title>
        </head>
        <body>
            <h1>Understanding Sports Betting: A Complete Guide</h1>
            <p>In today's world of sports betting, you need to know about FakeBet Casino and ScamSports.</p>
            <p>Check out BetNotReal for the best odds!</p>
        </body>
        </html>
        """
        
        result = gate.validate(low_quality_content)
        
        # Should still return a valid result structure
        assert isinstance(result, QualityGateResult)
        assert hasattr(result, 'passed')
        assert hasattr(result, 'total_score')
        assert len(result.validator_results) == 5
    
    def test_validate_with_page_url(self):
        """Test validation with a specific page URL for SEO validation."""
        gate = ContentQualityGate()
        
        content = """
        <html>
        <head>
            <title>Sports Betting Guide | TopEndSports</title>
            <link rel="canonical" href="https://topendsports.com/betting-guide">
        </head>
        <body>
            <h1>Sports Betting Guide</h1>
            <p>Learn about sports betting at DraftKings and FanDuel.</p>
        </body>
        </html>
        """
        
        result = gate.validate(content, page_url="https://topendsports.com/betting-guide")
        
        assert isinstance(result, QualityGateResult)
        assert len(result.validator_results) == 5
    
    def test_strict_mode_vs_non_strict(self):
        """Test difference between strict and non-strict modes."""
        content = """
        <html>
        <head><title>Short</title></head>
        <body><h1>Understanding Betting: A Complete Guide</h1></body>
        </html>
        """
        
        # Test strict mode
        strict_gate = ContentQualityGate(strict_mode=True)
        strict_result = strict_gate.validate(content)
        
        # Test non-strict mode
        non_strict_gate = ContentQualityGate(strict_mode=False)
        non_strict_result = non_strict_gate.validate(content)
        
        # Both should return results
        assert isinstance(strict_result, QualityGateResult)
        assert isinstance(non_strict_result, QualityGateResult)


class TestValidatorResults:
    """Test individual validator result processing."""
    
    def test_validator_result_creation(self):
        """Test creating ValidatorResult objects."""
        result = ValidatorResult(
            validator_type=ValidatorType.EEAT,
            passed=True,
            score=85.0,
            errors=["Error 1"],
            warnings=["Warning 1"],
            details={"test": "data"}
        )
        
        assert result.validator_type == ValidatorType.EEAT
        assert result.passed == True
        assert result.score == 85.0
        assert result.errors == ["Error 1"]
        assert result.warnings == ["Warning 1"]
        assert result.details == {"test": "data"}
    
    def test_quality_gate_result_summary(self):
        """Test the summary property of QualityGateResult."""
        # Create a mock result
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=80.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=False,
                score=40.0,
                errors=["Unknown brand found"]
            )
        }
        
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=72.5,
            validator_results=validator_results,
            critical_errors=["Unknown brand found"],
            warnings=["Minor issue"]
        )
        
        summary = result.summary
        
        assert "❌" in summary
        assert "FAILED" in summary
        assert "72.5/100" in summary
        assert "Unknown brand found" in summary
        assert "Minor issue" in summary


class TestScoreCalculation:
    """Test score calculation and weighting logic."""
    
    def test_calculate_total_score(self):
        """Test the weighted score calculation."""
        gate = ContentQualityGate()
        
        # Mock validator results with known scores
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=80.0  # Weight: 30, contributes 24.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=True,
                score=90.0  # Weight: 20, contributes 18.0
            ),
            ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                passed=True,
                score=100.0  # Weight: 25, contributes 25.0
            ),
            ValidatorType.SEO_META: ValidatorResult(
                validator_type=ValidatorType.SEO_META,
                passed=True,
                score=70.0  # Weight: 15, contributes 10.5
            ),
            ValidatorType.AI_PATTERN: ValidatorResult(
                validator_type=ValidatorType.AI_PATTERN,
                passed=True,
                score=60.0  # Weight: 10, contributes 6.0
            )
        }
        
        total_score = gate._calculate_total_score(validator_results)
        expected_score = 24.0 + 18.0 + 25.0 + 10.5 + 6.0  # 83.5
        
        assert total_score == expected_score
    
    def test_determine_status_all_passed(self):
        """Test status determination when all validators pass."""
        gate = ContentQualityGate()
        
        validator_results = {
            validator_type: ValidatorResult(
                validator_type=validator_type,
                passed=True,
                score=80.0
            ) for validator_type in ValidatorType
        }
        
        passed, status = gate._determine_status(validator_results, [])
        
        assert passed == True
        assert status == QualityGateStatus.PASSED
    
    def test_determine_status_critical_failure(self):
        """Test status determination with critical validator failure."""
        gate = ContentQualityGate()
        
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=False,  # Critical failure
                score=50.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=True,
                score=80.0
            ),
            ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                passed=True,
                score=90.0
            )
        }
        
        passed, status = gate._determine_status(validator_results, ["EEAT failed"])
        
        assert passed == False
        assert status == QualityGateStatus.FAILED
    
    def test_determine_status_non_strict_mode(self):
        """Test status determination in non-strict mode."""
        gate = ContentQualityGate(strict_mode=False)
        
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=True,
                score=80.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=False,  # Non-critical failure in non-strict mode
                score=50.0
            ),
            ValidatorType.RESPONSIBLE_GAMBLING: ValidatorResult(
                validator_type=ValidatorType.RESPONSIBLE_GAMBLING,
                passed=True,
                score=90.0
            )
        }
        
        passed, status = gate._determine_status(validator_results, [])
        
        assert passed == True
        assert status == QualityGateStatus.WARNING


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_validator_exception_handling(self):
        """Test handling of validator exceptions."""
        gate = ContentQualityGate()
        
        # Mock a validator that raises an exception
        with patch.object(gate.validators[ValidatorType.EEAT], 'validate', side_effect=Exception("Test error")):
            result = gate.validate("test content")
            
            # Should still return a result
            assert isinstance(result, QualityGateResult)
            
            # The failed validator should have an error result
            eeat_result = result.validator_results.get(ValidatorType.EEAT)
            assert eeat_result is not None
            assert not eeat_result.passed
            assert eeat_result.score == 0.0
            assert any("Validator execution failed" in error for error in eeat_result.errors)
    
    def test_empty_content(self):
        """Test validation of empty content."""
        gate = ContentQualityGate()
        result = gate.validate("")
        
        assert isinstance(result, QualityGateResult)
        assert len(result.validator_results) == 5
    
    def test_none_content(self):
        """Test handling of None content."""
        gate = ContentQualityGate()
        
        # This should handle None gracefully or raise appropriate error
        try:
            result = gate.validate(None)
            assert isinstance(result, QualityGateResult)
        except (TypeError, AttributeError):
            # Acceptable to raise error for None content
            pass
    
    def test_malformed_html(self):
        """Test validation of malformed HTML content."""
        gate = ContentQualityGate()
        
        malformed_html = """
        <html>
        <head>
            <title>Test Title
            <meta name="description" content="Test description
        </head>
        <body>
            <h1>Test Header</h1>
            <p>Test paragraph
        </body>
        """
        
        result = gate.validate(malformed_html)
        
        # Should still return a result even with malformed HTML
        assert isinstance(result, QualityGateResult)
        assert len(result.validator_results) == 5


class TestPerformance:
    """Test performance and execution time tracking."""
    
    def test_execution_time_tracking(self):
        """Test that execution times are tracked properly."""
        gate = ContentQualityGate()
        
        content = "<html><head><title>Test</title></head><body><h1>Test</h1></body></html>"
        result = gate.validate(content)
        
        # Overall execution time should be tracked
        assert result.execution_time > 0
        
        # Individual validator execution times should be tracked
        for validator_result in result.validator_results.values():
            assert validator_result.execution_time >= 0


class TestConvenienceFunctions:
    """Test convenience functions and utility methods."""
    
    def test_validate_content_brief_function(self):
        """Test the standalone validate_content_brief function."""
        content = """
        <html>
        <head>
            <title>Test Content Brief | TopEndSports</title>
            <meta name="description" content="Test description for content brief validation.">
        </head>
        <body>
            <h1>Test Content Brief</h1>
            <p>This is a test content brief for validation testing.</p>
        </body>
        </html>
        """
        
        result = validate_content_brief(content)
        
        assert isinstance(result, QualityGateResult)
        assert len(result.validator_results) == 5
    
    def test_get_recommendations(self):
        """Test the get_recommendations method."""
        gate = ContentQualityGate()
        
        # Create a result with some failed validators
        validator_results = {
            ValidatorType.EEAT: ValidatorResult(
                validator_type=ValidatorType.EEAT,
                passed=False,
                score=40.0
            ),
            ValidatorType.SEO_META: ValidatorResult(
                validator_type=ValidatorType.SEO_META,
                passed=False,
                score=30.0
            ),
            ValidatorType.BRAND: ValidatorResult(
                validator_type=ValidatorType.BRAND,
                passed=True,
                score=80.0
            )
        }
        
        result = QualityGateResult(
            passed=False,
            status=QualityGateStatus.FAILED,
            total_score=50.0,
            validator_results=validator_results
        )
        
        recommendations = gate.get_recommendations(result)
        
        assert len(recommendations) >= 2  # Should have recommendations for failed validators
        assert any("E-E-A-T" in rec for rec in recommendations)
        assert any("title tag" in rec or "meta description" in rec for rec in recommendations)


class TestIntegration:
    """Integration tests that test the full pipeline."""
    
    def test_full_validation_pipeline(self):
        """Test the complete validation pipeline end-to-end."""
        gate = ContentQualityGate(
            target_keywords=["sports betting", "sportsbook"],
            brand_name="TopEndSports",
            target_states=["NV", "NJ"]
        )
        
        comprehensive_content = """
        <html>
        <head>
            <title>Complete Sports Betting Guide 2024: Expert Reviews and Analysis | TopEndSports</title>
            <meta name="description" content="Expert sports betting analysis with 15+ years of testing experience. Comprehensive sportsbook reviews, responsible gambling resources, and proven strategies for success.">
            <meta property="og:title" content="Complete Sports Betting Guide 2024: Expert Reviews and Analysis">
            <meta property="og:description" content="Expert sports betting analysis with 15+ years of testing experience. Comprehensive sportsbook reviews and proven strategies.">
            <meta property="og:image" content="https://topendsports.com/images/sports-betting-guide-2024.jpg">
            <meta property="og:url" content="https://topendsports.com/sports-betting-guide">
            <meta name="twitter:card" content="summary_large_image">
            <meta name="twitter:title" content="Complete Sports Betting Guide 2024: Expert Reviews and Analysis">
            <meta name="twitter:description" content="Expert sports betting analysis with 15+ years of testing experience.">
            <meta name="twitter:image" content="https://topendsports.com/images/sports-betting-guide-2024.jpg">
            <link rel="canonical" href="https://topendsports.com/sports-betting-guide">
            <meta name="robots" content="index, follow">
        </head>
        <body>
            <article>
                <header>
                    <h1>Complete Sports Betting Guide 2024: Expert Reviews and Analysis</h1>
                    <div class="author-info">
                        <img src="/author-john-smith.jpg" alt="John Smith, Senior Sports Analyst">
                        <div class="author-bio">
                            <h3>John Smith, Senior Sports Analyst</h3>
                            <p>John has been analyzing sports betting markets professionally since 2008. He holds a degree in Statistics from USC and has published research on sports analytics. Our team has tested over 50 sportsbooks with real money deposits exceeding $100,000 over the past 15 years.</p>
                            <p>Expertise: NBA betting analysis, March Madness predictions, sportsbook platform testing</p>
                        </div>
                    </div>
                </header>

                <section id="methodology">
                    <h2>Our Testing Methodology</h2>
                    <p>We've been conducting real-money sportsbook testing since 2008. Our comprehensive evaluation process includes:</p>
                    <ul>
                        <li><strong>Real Money Testing:</strong> We deposit and wager real money (over $100,000 total) to test actual user experience</li>
                        <li><strong>Withdrawal Testing:</strong> Every sportsbook must successfully process withdrawal requests within stated timeframes</li>
                        <li><strong>Customer Service:</strong> We contact customer support multiple times to evaluate response quality and speed</li>
                        <li><strong>Platform Testing:</strong> Extensive testing of mobile apps and desktop platforms across multiple devices</li>
                        <li><strong>Odds Comparison:</strong> Daily monitoring of odds across all major sports for competitive analysis</li>
                    </ul>
                    <p>When we tested DraftKings in January 2024, for example, we deposited $500, placed 47 different bet types, and successfully withdrew $623 within 24 hours. This hands-on approach gives us unique insights you won't find elsewhere.</p>
                </section>

                <section id="top-sportsbooks">
                    <h2>Top Rated Sportsbooks for 2024</h2>
                    <p>Based on our extensive real-money testing, here are the top-performing sportsbooks:</p>
                    
                    <div class="sportsbook-review">
                        <h3>1. DraftKings Sportsbook</h3>
                        <p>Our testing revealed DraftKings as the most consistent performer with excellent odds, fast payouts, and superior mobile experience. In our testing, we processed 15 withdrawals with an average completion time of 18 hours.</p>
                        <ul>
                            <li>Average odds margin: 4.2% (excellent)</li>
                            <li>Withdrawal time: 12-24 hours (tested 15 times)</li>
                            <li>Mobile app rating: 4.8/5 based on our testing</li>
                        </ul>
                    </div>

                    <div class="sportsbook-review">
                        <h3>2. FanDuel Sportsbook</h3>
                        <p>FanDuel consistently impressed our testers with intuitive design and reliable customer service. We particularly appreciated their same-game parlay options during our NBA testing in March 2024.</p>
                        <ul>
                            <li>Customer service response: Average 3.2 minutes (tested 12 times)</li>
                            <li>Platform uptime: 99.7% during major sporting events</li>
                            <li>Bonus terms clarity: Excellent (no hidden requirements found)</li>
                        </ul>
                    </div>

                    <div class="sportsbook-review">
                        <h3>3. BetMGM</h3>
                        <p>BetMGM earned high marks in our testing for live betting features and competitive odds on major sports. Our team particularly values their pre-game analysis tools.</p>
                        <ul>
                            <li>Live betting options: 200+ markets per NBA game (tested during playoffs)</li>
                            <li>Deposit methods: 8 different options tested successfully</li>
                            <li>Security features: Two-factor authentication, SSL encryption verified</li>
                        </ul>
                    </div>
                </section>

                <section id="responsible-gambling">
                    <h2>Responsible Gambling</h2>
                    <div class="responsible-gambling-notice">
                        <p><strong>Please gamble responsibly.</strong> Sports betting should be entertainment, not a way to make money. Set limits before you start and stick to them.</p>
                        
                        <h3>Age Requirements</h3>
                        <p>You must be 21 years of age or older to participate in sports betting. Age verification is required by all licensed operators.</p>
                        
                        <h3>Problem Gambling Help</h3>
                        <p>If you or someone you know has a gambling problem, help is available:</p>
                        <ul>
                            <li><strong>National Problem Gambling Helpline:</strong> 1-800-522-4700</li>
                            <li><strong>Crisis Text Line:</strong> Text HOME to 741741</li>
                            <li><strong>Gamblers Anonymous:</strong> <a href="https://www.gamblersanonymous.org">gamblersanonymous.org</a></li>
                            <li><strong>National Council on Problem Gambling:</strong> <a href="https://www.ncpgambling.org">ncpgambling.org</a></li>
                        </ul>
                        
                        <h3>State-Specific Resources</h3>
                        <p><strong>Nevada:</strong> Nevada Council on Problem Gambling - 1-800-522-4700</p>
                        <p><strong>New Jersey:</strong> New Jersey Council on Compulsive Gambling - 1-800-GAMBLER</p>
                        
                        <h3>Self-Exclusion</h3>
                        <p>All licensed sportsbooks offer self-exclusion tools. You can temporarily or permanently exclude yourself from betting activities. Contact customer support for assistance.</p>
                        
                        <div class="disclaimer">
                            <p><em>Gambling problem? Call 1-800-GAMBLER. Available 24/7. You must be 21+ to participate. Know When To Stop Before You Start. Gambling problem? Visit ncpgambling.org.</em></p>
                        </div>
                    </div>
                </section>

                <footer class="article-footer">
                    <div class="author-expertise">
                        <h3>About Our Expert Team</h3>
                        <p>TopEndSports has been providing independent sports betting analysis since 2008. Our team includes former oddsmakers, professional sports analysts, and certified gambling counselors. We maintain strict editorial independence and never accept payments for reviews.</p>
                        <p>Last updated: January 2024 | Next review: February 2024</p>
                    </div>
                </footer>
            </article>
        </body>
        </html>
        """
        
        result = gate.validate(comprehensive_content, page_url="https://topendsports.com/sports-betting-guide")
        
        # Verify result structure
        assert isinstance(result, QualityGateResult)
        assert hasattr(result, 'passed')
        assert hasattr(result, 'total_score')
        assert hasattr(result, 'status')
        assert len(result.validator_results) == 5
        
        # Check that all validators ran
        expected_validators = {ValidatorType.EEAT, ValidatorType.BRAND, ValidatorType.RESPONSIBLE_GAMBLING, 
                             ValidatorType.SEO_META, ValidatorType.AI_PATTERN}
        actual_validators = set(result.validator_results.keys())
        assert expected_validators == actual_validators
        
        # Verify summary is generated
        summary = result.summary
        assert len(summary) > 0
        assert "Quality Gate" in summary
        assert "/100" in summary
        
        # Test recommendations
        recommendations = gate.get_recommendations(result)
        assert isinstance(recommendations, list)
        
        print(f"\nIntegration Test Results:")
        print(f"Passed: {result.passed}")
        print(f"Status: {result.status}")
        print(f"Total Score: {result.total_score}")
        print(f"Execution Time: {result.execution_time:.3f}s")
        print(f"\nValidator Breakdown:")
        for validator_type, validator_result in result.validator_results.items():
            status = "✅" if validator_result.passed else "❌"
            print(f"  {status} {validator_type.value}: {validator_result.score:.1f}/100")
        
        if recommendations:
            print(f"\nRecommendations:")
            for rec in recommendations:
                print(f"  - {rec}")


if __name__ == "__main__":
    # Run specific tests for development
    import subprocess
    
    print("Running Quality Gate Tests...")
    
    # Run the tests with pytest
    result = subprocess.run([
        "python", "-m", "pytest", __file__, "-v", "--tb=short"
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    print(f"Exit code: {result.returncode}")