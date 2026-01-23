# Security Policy

## Supported Versions

This project is actively maintained. Security updates are provided for the latest version.

| Version | Supported          |
| ------- | ------------------ |
| 7.0.x   | :white_check_mark: |
| 6.0.x   | :x:                |
| < 6.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in the Topend Sports Content Briefs project, please report it privately:

### How to Report

1. **Email:** andre-external@strategie360consulting.com
2. **Subject:** [SECURITY] topendsports-content-briefs
3. **GitHub Security Advisory:** Use the "Security" tab to create a private security advisory (preferred)
4. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact (data exposure, compliance violation, etc.)
   - Suggested fix (if available)
   - Affected versions

### What to Expect

- **Acknowledgment:** Within 48 hours
- **Initial Assessment:** Within 1 week
- **Fix Timeline:** Depends on severity
  - **Critical:** 1-3 days (legal compliance issues: 24 hours)
  - **High:** 1-2 weeks
  - **Medium:** 2-4 weeks
  - **Low:** Next release cycle
- **Coordinated Disclosure:** After fix is released

### Legal Compliance Vulnerabilities (CRITICAL PRIORITY)

This system handles sports content compliance. If you discover:
- **Unlicensed operators being featured** (legal violation)
- **Gaming commission data errors** (compliance risk)
- **State compliance violations** (regulatory issue)
- **Age verification bypasses** (legal requirement)
- **Responsible gambling disclaimer missing** (required by law)

**Contact immediately** - these are handled within 24 hours and may require legal team notification.

## Security Best Practices

### For Contributors

#### 1. Never Commit Sensitive Data

**Absolute No-Commit List:**
```
# Credentials & Keys
.env
.env.local
.env.production
*.pem
*.key
credentials.json
secrets.yml
*_api_key*
*_token*
*_secret*
ahrefs_credentials.json
claude_api_key.txt

# Databases
*.db
*.sqlite
*.sql (with production data)
database_backup_*

# Temporary/Cache
.cache/
.tmp/
temp/
__pycache__/

# OS Files
.DS_Store
Thumbs.db

# IDE
.vscode/settings.json (if contains paths)
.idea/workspace.xml
```

#### 2. Check Before Every Commit

```bash
# Scan for secrets in staged files
git diff --cached | grep -i "api.key\|token\|secret\|password\|credential"

# Check .gitignore coverage
git status --ignored

# List files that would be committed
git diff --cached --name-only

# Use git-secrets (recommended)
git secrets --scan
```

#### 3. Validation Scripts Security

- **Review all Python scripts** for code injection vulnerabilities
- **Sanitize user inputs** in validation scripts
- **Use subprocess with proper escaping** (never shell=True with user input)
- **Validate HTML before parsing** with BeautifulSoup
- **Avoid eval()** and exec() entirely
- **Pin dependencies** with exact versions in requirements.txt
- **Audit new dependencies** before adding

#### 4. Dependencies Management

- Keep dependencies updated (check weekly)
- Review Dependabot alerts immediately
- Pin versions in requirements.txt (use ==)
- Audit new dependencies:
  - Check PyPI for maintainer reputation
  - Review recent issues/CVEs
  - Verify package hasn't been hijacked
- Use `pip-audit` for vulnerability scanning

### For Brief Generation

#### 1. Input Validation

- **Validate all external data** before processing
  - URLs: Check format, protocol (https only for external)
  - State names: Match against Configuration.csv
  - Dates: Validate format and range
  - User inputs: Sanitize for HTML/JS injection
- **Web fetch validation:**
  - Verify URLs are not internal/localhost
  - Set reasonable timeouts (30s max)
  - Validate response content type
  - Check for malicious redirects
- **Ahrefs data validation:**
  - Verify API responses are JSON
  - Validate numeric fields (volume, difficulty)
  - Check for unexpected data structures
  - Rate limit API calls

#### 2. XSS Prevention

- **Escape all user inputs** before inserting into briefs
- **Use proper HTML entity encoding** for text content
- **Validate all external URLs** before including in output
- **Sanitize rich text content** from competitors
- **Never use innerHTML** with untrusted content
- **Validate inline styles** for malicious code
- **Use Content Security Policy** in generated HTML

#### 3. Operator Data Security

- **License verification:**
  - Always cross-reference Configuration.csv
  - Never feature operators not in licensed list
  - Verify gaming commission URLs are .gov domains
  - Check age requirements match state law
- **Bonus data handling:**
  - Don't commit live bonus amounts to git
  - Use placeholders for example briefs
  - Verify operator promo codes with brands
  - Never store affiliate tracking parameters in repo

#### 4. API Key Management

**Critical: Never expose API keys**

```python
# ✅ CORRECT: Use environment variables
import os
api_key = os.environ.get('AHREFS_API_KEY')

# ❌ WRONG: Hardcoded key
api_key = "ahrefs_abc123def456"  # NEVER DO THIS

# ✅ CORRECT: Verify key exists before use
if not api_key:
    raise ValueError("AHREFS_API_KEY not set in environment")

# ❌ WRONG: Print API key in logs
print(f"Using API key: {api_key}")  # NEVER LOG KEYS
```

## Security Features

### Implemented ✅

- ✅ Comprehensive .gitignore with API key patterns
- ✅ Proprietary LICENSE file (prevents unauthorized use)
- ✅ Licensed operator validation (prevents legal violations)
- ✅ Gaming commission verification (.gov domain check)
- ✅ Age requirement validation by state
- ✅ Responsible gambling disclaimer checks
- ✅ 23-point automated validation system
- ✅ Private repository with access controls
- ✅ Input validation in Python scripts
- ✅ BeautifulSoup4 for safe HTML parsing
- ✅ No eval() or unsafe code execution
- ✅ GitHub Actions for automated checks (4 workflows)
- ✅ HTML structure validation before output

### Advanced Security (GitHub Advanced Security Required) 🔒

#### Dependency Graph & Dependabot
- ✅ **Enabled:** Automatic dependency tracking
- ✅ **Dependabot Alerts:** Notifies of vulnerable dependencies
- ✅ **Dependabot Security Updates:** Auto-creates PRs for security fixes
- ✅ **Frequency:** Check daily for critical, weekly for others

#### Secret Scanning
- ⚠️ **Status:** Requires GitHub Advanced Security license
- **When Enabled:**
  - Scans all commits for exposed secrets
  - Alerts on API keys, tokens, credentials
  - Blocks pushes with detected secrets (push protection)
  - Custom patterns for Ahrefs, Claude API keys

**Custom Secret Patterns (when Advanced Security enabled):**
```
Pattern Name: Ahrefs API Key
Regex: ahrefs_[a-zA-Z0-9]{32,}
Description: Ahrefs API authentication key

Pattern Name: Claude API Key
Regex: sk-ant-[a-zA-Z0-9_-]{95,}
Description: Claude/Anthropic API key

Pattern Name: Generic API Key
Regex: api[_-]?key["\s:=]+[a-zA-Z0-9]{20,}
Description: Generic API key pattern
```

#### Code Scanning (CodeQL)
- ⚠️ **Status:** Requires GitHub Advanced Security license
- **When Enabled:**
  - Scans Python code for security vulnerabilities
  - Detects SQL injection, XSS, command injection
  - Identifies hardcoded credentials
  - Analyzes data flow for security issues
  - Runs on: Push, Pull Request, Schedule (weekly)

**Languages Analyzed:**
- Python (validation scripts, automation)
- JavaScript (if added to project)

#### Dependency Review
- ⚠️ **Status:** Requires GitHub Advanced Security license
- **When Enabled:**
  - Blocks PRs with vulnerable dependencies
  - Shows security impact of dependency changes
  - Enforces license policy compliance
  - Alerts on deprecated packages

### Planned Security Enhancements 🔄

- [ ] Pre-commit hooks for secret detection (git-secrets)
- [ ] Automated license compliance checking
- [ ] Signed commits requirement for production
- [ ] Branch protection with required reviewers
- [ ] Automated vulnerability scanning in CI/CD
- [ ] Security incident response playbook
- [ ] Quarterly security audits
- [ ] Penetration testing for brief generation system

## GitHub Advanced Security Setup

### Requirements

- **GitHub Team or Enterprise Cloud** plan
- **Private repository** (already configured)
- **Admin access** to repository settings

### Enabling Advanced Security

#### Step 1: Enable Advanced Security (Admin Only)

Navigate to: `Settings` → `Code security and analysis`

```yaml
Security Features:

✅ Dependency graph: Enabled (free for private repos)
✅ Dependabot alerts: Enabled (free for private repos)
✅ Dependabot security updates: Enabled (free)

# Requires GitHub Advanced Security license:
☐ Code scanning: Enable
  → Choose: GitHub Actions
  → Language: Python
  → Schedule: Weekly + on push

☐ Secret scanning: Enable
  → Enable push protection (blocks commits with secrets)
  → Configure custom patterns (see above)

☐ Dependency review: Enable
  → Blocks PRs with vulnerable dependencies
```

#### Step 2: Configure CodeQL Workflow

When enabled, GitHub creates `.github/workflows/codeql.yml` automatically.

**Verify configuration:**
```yaml
name: "CodeQL"
on:
  push:
    branches: [ "master", "main" ]
  pull_request:
    branches: [ "master", "main" ]
  schedule:
    - cron: '0 12 * * 1'  # Every Monday at noon UTC

jobs:
  analyze:
    name: Analyze Python
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: python
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

#### Step 3: Add Custom Secret Patterns

Navigate to: `Settings` → `Code security and analysis` → `Secret scanning` → `Custom patterns`

**Add each pattern:**
1. Click "New pattern"
2. Enter pattern name, regex, and test strings
3. Set as "Push protection" (blocks commits)
4. Save pattern

**Test Patterns:**
```
Test String for Ahrefs: ahrefs_abc123def456ghi789jkl012mno345p
Test String for Claude: sk-ant-api03-abcdefghijklmnopqrstuvwxyz...
```

#### Step 4: Configure Dependency Review

Navigate to: `Settings` → `Code security and analysis` → `Dependency review`

```yaml
Policy Configuration:

☑ Block on critical vulnerabilities (required)
☑ Block on high vulnerabilities (recommended)
☐ Block on medium vulnerabilities (optional)

License Policy:
☑ Block copyleft licenses (GPL, LGPL) if proprietary
☑ Allow MIT, Apache 2.0, BSD licenses
☐ Require manual review for new dependencies

Scope:
☑ Check all dependencies (direct + transitive)
☑ Alert on deprecated packages
☑ Enforce dependency pinning
```

#### Step 5: Set Up Security Alerts

Navigate to: `Settings` → `Notifications` → `Security alerts`

```yaml
Email Notifications:

☑ Dependabot alerts (critical & high)
☑ Secret scanning alerts (all)
☑ Code scanning alerts (medium & above)

Webhook:
☐ Optional: Configure Slack webhook for team alerts
```

### Costs & Considerations

**GitHub Advanced Security Pricing (as of 2025):**
- Free for public repositories
- Paid for private repositories:
  - GitHub Team: Add-on required
  - GitHub Enterprise Cloud: Included

**ROI Justification:**
- Prevents API key exposure ($$$$ in costs if leaked)
- Avoids legal compliance violations (regulatory fines)
- Catches vulnerabilities before production
- Reduces security incident response costs
- Insurance requirement for gambling industry compliance

### Alternative: Open-Source Security Tools

If GitHub Advanced Security is not available:

```bash
# Install security tools
pip install bandit safety pip-audit git-secrets

# Run security scans locally
bandit -r scripts/          # Python security linter
safety check                # Dependency vulnerabilities
pip-audit                   # Alternative vulnerability scanner
git secrets --scan          # Secret detection

# Add to pre-commit hooks
# See .pre-commit-config.yaml
```

## Secure Development Guidelines

### When Adding New Features

#### 1. Brief Generation Code

- **HTML Generation:**
  - Validate all inputs before HTML generation
  - Use template libraries (Jinja2) with auto-escaping
  - Never concatenate untrusted data into HTML
  - Test with malicious input samples (XSS payloads)
  - Validate generated HTML with linter

- **Data Processing:**
  - Validate Ahrefs API responses
  - Sanitize competitor scraped content
  - Check for malicious redirects in URLs
  - Limit response sizes (prevent DoS)
  - Handle API errors gracefully (don't leak keys in errors)

#### 2. File Processing

- **Validation:**
  - Verify file paths before operations (no directory traversal)
  - Check file sizes before reading (max 10MB)
  - Validate file types (only expected extensions)
  - Use secure temp directories (mkdtemp)
  - Clean up temporary files (try/finally)

- **CSV Processing:**
  - Validate Configuration.csv schema
  - Check for CSV injection attacks
  - Sanitize cell contents before use
  - Limit row count (prevent memory exhaustion)
  - Use pandas with dtype validation

#### 3. API Integrations

- **Ahrefs API:**
  - Store API key in environment only
  - Use HTTPS for all requests
  - Validate API responses before parsing
  - Implement rate limiting (client-side)
  - Log API usage (not keys or responses)
  - Handle 429 errors gracefully

- **Claude/MCP:**
  - Store API keys securely
  - Validate prompt inputs
  - Sanitize responses before use
  - Monitor token usage
  - Implement timeouts (30s default)

#### 4. Code Review Requirements

Before merging any PR:

- [ ] Run all validation scripts
- [ ] Check for XSS vulnerabilities
- [ ] Review HTML injection risks
- [ ] Validate external inputs
- [ ] Check dependencies for CVEs
- [ ] Verify .gitignore coverage
- [ ] Test with malicious inputs
- [ ] Review error handling (no info leakage)
- [ ] Confirm logging doesn't expose secrets
- [ ] Validate compliance with gambling regulations

## Known Security Considerations

### 1. Tracking Codes (Public & Intentional)

The following identifiers are public and intentionally included:
- **Analytics:** Various Google Analytics / Tag Manager IDs
- **Domain Names:** All 27 betting hub domains are public

These are not considered sensitive as they're public-facing website identifiers.

### 2. Library References

The system references external library files:
- `/Library/all-header.lbi`
- Various CMS library includes

These are validated during brief generation and are internal CMS references.

### 3. Configuration Data (SENSITIVE)

**content-config.csv contains:**
- ✅ Licensed operators per state (business-sensitive)
- ✅ Gaming commission URLs (public information)
- ✅ Age requirements (public regulatory data)
- ✅ Local team mappings (public sports data)

**Security Level:** CONFIDENTIAL (private repo only)
**Why:** Reveals business strategy, coverage plans, and competitive analysis

### 4. External Links in Briefs

Generated briefs contain external links (competitors, gaming commissions):

**Security measures:**
- Use `target="_blank"` for external links
- Include `rel="noopener noreferrer"` (prevents tabnabbing)
- Validate URLs before inclusion (https only)
- Check against malware databases (optional)
- No automatic redirects without validation

### 5. Gambling Industry Compliance

**Regulatory Requirements:**
- Only feature licensed operators (per state)
- Include responsible gambling disclaimers (1-800-GAMBLER)
- Verify age requirements (18+ or 21+ by state)
- Link to official gaming commission websites
- Never bypass compliance validation

**Legal Risks:**
- Featuring unlicensed operators = regulatory violation
- Missing disclaimers = liability exposure
- Wrong age requirements = legal non-compliance
- Broken gaming commission links = loss of authority

## Incident Response

### If Security Issue Discovered

#### 1. Containment (Immediate - Within 1 hour)

```bash
# If API key exposed:
1. Rotate compromised credentials immediately
   - Generate new Ahrefs API key
   - Update environment variables on all systems
   - Revoke old key

2. Remove sensitive data from git history
   # WARNING: This rewrites history
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/sensitive/file" \
     --prune-empty --tag-name-filter cat -- --all

   # Or use BFG Repo-Cleaner (faster)
   bfg --delete-files sensitive_file.txt

3. Force push cleaned history (after backup)
   git push --force --all
   git push --force --tags

4. Notify all collaborators to re-clone
```

#### 2. Investigation (24-48 hours)

- [ ] Determine what was exposed (API key, credentials, data?)
- [ ] Identify affected systems (where was key used?)
- [ ] Review git history for exposure duration
- [ ] Check if exposed key was used maliciously (audit logs)
- [ ] Document timeline of exposure

#### 3. Recovery (48-72 hours)

- [ ] Deploy rotated credentials to all systems
- [ ] Verify all systems secure (key rotation complete)
- [ ] Test all systems functional with new keys
- [ ] Update documentation with new security measures
- [ ] Review and update .gitignore if needed

#### 4. Prevention (1 week)

- [ ] Add exposed pattern to .gitignore
- [ ] Install git-secrets pre-commit hook
- [ ] Add custom secret patterns to GitHub
- [ ] Document lesson learned in LESSONS-LEARNED.md
- [ ] Train team on secure practices
- [ ] Update this security policy

### Legal Compliance Incidents

For compliance violations (unlicensed operators, gaming commission errors):

#### Immediate Action (Within 24 hours)

1. **Identify Scope:**
   - Which state(s) affected?
   - Which operator(s) improperly featured?
   - How many generated briefs affected?
   - Was content already published?

2. **Containment:**
   - Remove affected briefs from output/ immediately
   - Update Configuration.csv with correct data
   - Notify legal team if content was published
   - Document violation in compliance log

3. **Correction:**
   - Regenerate affected briefs with correct data
   - Validate with scripts/validate_compliance.py
   - Double-check against gaming commission sources
   - Get legal team approval before republishing

4. **Prevention:**
   - Add validation check for this specific issue
   - Update CRITICAL-EXECUTION-CHECKLIST
   - Document in LESSONS-LEARNED.md
   - Train team on proper operator verification

#### Notification Requirements

**Must notify within 24 hours:**
- Legal team (all compliance violations)
- Management (critical violations)
- Gaming commission (if legally required)

## Security Audit Log

| Date | Issue Type | Severity | Action Taken | Status |
|------|------------|----------|--------------|--------|
| 2025-12-10 | Initial security review | N/A | Created comprehensive SECURITY.md | ✅ Complete |
| 2025-12-10 | .gitignore gaps | HIGH | Enhanced .gitignore with API key patterns | ✅ Complete |
| 2025-12-10 | Missing LICENSE | HIGH | Added proprietary LICENSE | ✅ Complete |
| 2025-12-10 | Validation scripts | MEDIUM | Created compliance validation scripts | ✅ Complete |
| 2025-12-10 | GitHub workflows | LOW | Added 4 automated check workflows | ✅ Complete |
| 2025-12-10 | Security enhancement | HIGH | Updated to TES standards + Advanced Security docs | ✅ Complete |

## Security Updates & Announcements

Security updates will be announced through:
1. **GitHub Security Advisories** (preferred)
2. **Release notes** (for all updates)
3. **Repository README** (for critical updates)
4. **Email notification** (for team members on critical issues)

**Subscribe to security updates:**
- Watch repository → Custom → Security alerts

## Compliance & Data Handling

### What This Project Handles

- ❌ **No personal data** (PII)
- ❌ **No user health information** (not medical advice)
- ❌ **No financial transactions** (payment processing)
- ❌ **No direct user tracking** (analytics is external)
- ✅ **Business strategy data** (confidential but not regulated)
- ✅ **Public regulatory information** (gaming commissions)
- ✅ **Licensed operator lists** (business-sensitive)
- ✅ **Generated content** (HTML/text briefs)

### Regulatory Context

**Gambling Industry Regulations:**
- Must comply with state gaming regulations
- Required to feature only licensed operators
- Must include responsible gambling disclaimers
- Subject to gaming commission oversight
- Potential fines for non-compliance: $10k-$100k+ per violation

**Data Privacy:**
- No GDPR applicability (no EU user data)
- No CCPA applicability (no consumer data collection)
- No HIPAA applicability (not health-related)
- Business data protection (trade secrets)

## Pre-Commit Hooks (Recommended)

### Installation

```bash
# Install pre-commit framework
pip install pre-commit

# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files
```

### Configuration (.pre-commit-config.yaml)

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=500']
      - id: check-merge-conflict
      - id: detect-private-key
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']

  - repo: https://github.com/PyCQA/bandit
    rev: '1.7.5'
    hooks:
      - id: bandit
        args: ['-c', 'pyproject.toml']

  - repo: local
    hooks:
      - id: check-api-keys
        name: Check for API keys
        entry: scripts/check_secrets.sh
        language: script
        pass_filenames: false
```

## Questions & Support

**Security Questions:**
- Email: andre-external@strategie360consulting.com
- GitHub Security Advisory: Use "Security" tab

**General Questions:**
- See: CONTRIBUTING.md
- Create issue: Use appropriate template

**Emergency Contact (Critical Issues):**
- Email: andre-external@strategie360consulting.com
- Subject: [URGENT SECURITY] [Brief description]
- Response Time: Within 4 hours for critical issues

---

**Last Updated:** December 10, 2025
**Version:** 2.0 (Enhanced with TES standards + GitHub Advanced Security)
**Responsible Disclosure:** We appreciate responsible disclosure and will acknowledge security researchers who report issues through proper channels.
**Organization:** On The Dot Media Ltd
**Repository:** https://github.com/OnTheDotMediaLtd/topendsports-content-briefs
