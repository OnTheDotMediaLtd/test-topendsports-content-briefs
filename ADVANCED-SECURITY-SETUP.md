# Advanced Security Setup Guide

**Complete guide to enabling GitHub Advanced Security features for this project**

**Status:** Ready for implementation when Advanced Security license is obtained
**Required:** GitHub Team or Enterprise Cloud plan
**Last Updated:** December 10, 2025

---

## 📋 Overview

This document provides step-by-step instructions for enabling and configuring GitHub Advanced Security features to protect the USA State Betting Hubs project.

### What is GitHub Advanced Security?

GitHub Advanced Security is a suite of security features that provides:
- **Secret Scanning**: Detect exposed API keys, tokens, credentials
- **Code Scanning (CodeQL)**: Find security vulnerabilities in Python code
- **Dependency Review**: Block vulnerable dependencies in PRs
- **Push Protection**: Prevent commits containing secrets
- **Security Advisories**: Private vulnerability reporting

### Why This Project Needs It

**Gambling Industry Requirements:**
- API keys protect thousands of dollars in costs if leaked
- Compliance violations can result in $10k-$100k+ fines
- Legal requirements for secure handling of operator data
- Insurance requirements for cybersecurity measures

**Business Protection:**
- Configuration.csv contains business strategy (confidential)
- Brief generation system is competitive advantage
- API integrations require credential security
- Regulatory compliance documentation needed

---

## 🎯 Prerequisites

### License Requirements

✅ **You Need:**
- GitHub Team plan (with Advanced Security add-on), OR
- GitHub Enterprise Cloud plan (includes Advanced Security)
- **Private repository** (already configured ✅)
- **Admin access** to repository settings

❌ **Not Available For:**
- GitHub Free plan (Advanced Security free only for public repos)
- Personal accounts without Team/Enterprise

### Cost Estimation

**GitHub Advanced Security Pricing (2025):**
- Public repositories: **FREE**
- Private repositories: **$49/user/month** (GitHub Team with add-on)
- Enterprise Cloud: **Included** in plan

**For This Project:**
- Estimated users: 2-5
- Monthly cost: $98-$245
- Annual cost: $1,176-$2,940

**ROI Justification:**
- Prevents API key exposure: **$5,000-$50,000** potential loss
- Avoids compliance violations: **$10,000-$100,000** in fines
- Reduces security incident response: **$10,000+** per incident
- Insurance requirement: May reduce premiums or be mandatory

---

## 🚀 Quick Start (5 Steps)

If you have GitHub Advanced Security enabled, follow these 5 steps:

1. **Enable Features** (5 min)
2. **Configure Secret Scanning** (10 min)
3. **Activate CodeQL** (5 min)
4. **Set Up Dependency Review** (5 min)
5. **Test & Verify** (10 min)

**Total Time:** ~35 minutes
**After:** Continuous automated security monitoring

---

## 📖 Detailed Setup Instructions

### Step 1: Enable Advanced Security Features

#### 1.1 Enable Advanced Security

Navigate to: `Settings` → `Code security and analysis`

**Enable these features in order:**

```yaml
1. Dependency graph
   Status: ✅ Should already be enabled
   Free for private repos

2. Dependabot alerts
   Status: ✅ Should already be enabled
   Free for private repos

3. Dependabot security updates
   Status: ✅ Should already be enabled
   Free for private repos

4. GitHub Advanced Security
   Status: ⚠️ Requires license
   Click: "Enable GitHub Advanced Security"
   Confirm: "Enable for this repository"

   ⚠️ Important: This may affect billing
```

**After enabling Advanced Security, new options appear:**

```yaml
5. Secret scanning
   Click: "Enable"
   ✅ Automatically scans for exposed secrets

6. Push protection (recommended)
   Click: "Enable"
   ✅ Blocks commits with secrets
   ⚠️ Can be bypassed (not recommended)

7. Code scanning
   Click: "Set up" → "Advanced"
   ✅ Will configure in next step

8. Dependency review
   Status: Automatically enabled with Advanced Security
   ✅ Blocks vulnerable dependencies in PRs
```

#### 1.2 Verify Enablement

Check that all features show as "Enabled":
- ✅ Dependency graph
- ✅ Dependabot alerts
- ✅ Dependabot security updates
- ✅ GitHub Advanced Security
- ✅ Secret scanning
- ✅ Push protection
- ✅ Code scanning (after Step 2)

---

### Step 2: Configure Secret Scanning

#### 2.1 Review Default Patterns

Navigate to: `Settings` → `Code security and analysis` → `Secret scanning`

GitHub automatically scans for 200+ secret types:
- API keys (generic patterns)
- AWS credentials
- Azure keys
- Google Cloud keys
- OAuth tokens
- Private keys

#### 2.2 Add Custom Secret Patterns

**Critical for this project:** Add patterns for Ahrefs and Claude API keys

Navigate to: `Settings` → `Code security and analysis` → `Secret scanning` → `Custom patterns`

**Pattern 1: Ahrefs API Key**
```yaml
Name: Ahrefs API Key
Description: Ahrefs API authentication key for SEO data
Secret format: ahrefs_[a-zA-Z0-9]{32,}

Regular expression: ahrefs_[a-zA-Z0-9]{32,}

Test string (for validation):
ahrefs_abc123def456ghi789jkl012mno345pqr

Before secret: api_key = "
After secret: "

Match requirements:
☑ Enable push protection (blocks commits)
☑ Consider match a secret (high confidence)
```

**Pattern 2: Claude/Anthropic API Key**
```yaml
Name: Claude API Key
Description: Claude/Anthropic API key for AI features
Secret format: sk-ant-[alphanumeric and hyphens, 95+ chars]

Regular expression: sk-ant-[a-zA-Z0-9_-]{95,}

Test string (for validation):
sk-ant-api03-abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-abcdefghijkl_ABCD

Before secret: ANTHROPIC_API_KEY="
After secret: "

Match requirements:
☑ Enable push protection (blocks commits)
☑ Consider match a secret (high confidence)
```

**Pattern 3: Generic API Key (Catch-All)**
```yaml
Name: Generic API Key
Description: Generic API key pattern for various services
Secret format: api_key or apiKey followed by key value

Regular expression: api[_-]?key[\s:="']+[a-zA-Z0-9_-]{20,}

Test string:
api_key = "1234567890abcdefghij1234567890"

Before secret: (empty)
After secret: (empty)

Match requirements:
☐ Enable push protection (may have false positives)
☑ Consider match a secret (medium confidence)
```

#### 2.3 Test Custom Patterns

**Before saving, test each pattern:**

1. Enter test string in "Test string" field
2. Verify pattern matches (should highlight the key)
3. Adjust regex if needed
4. Save pattern when tests pass

#### 2.4 Configure Push Protection

Navigate to: `Settings` → `Code security and analysis` → `Push protection`

```yaml
Configuration:
☑ Enable push protection for all contributors
☑ Allow contributors to bypass (with justification - audited)
☐ Require approval from admin (strictest - optional)

Notifications:
☑ Email admins when secret detected
☑ Email contributor when secret blocked
☑ Log all bypass attempts

Allowlist:
Add false positives here (use sparingly):
- Example test keys
- Public demo credentials
- Documentation examples
```

---

### Step 3: Activate CodeQL Code Scanning

#### 3.1 Enable CodeQL

Navigate to: `Settings` → `Code security and analysis` → `Code scanning`

Click: "Set up" → **"Advanced"**

**Why Advanced setup?**
- Default setup is limited
- Advanced allows customization
- Required for custom queries
- Better control over schedule

#### 3.2 Use Template Workflow

GitHub will prompt to create `.github/workflows/codeql.yml`

**We have a pre-configured template:**

```bash
# In repository, rename the template:
cd /path/to/repo
mv .github/workflows/codeql.yml.template .github/workflows/codeql.yml

# Commit and push
git add .github/workflows/codeql.yml
git commit -m "feat: Enable CodeQL security scanning"
git push
```

**Alternatively, create via GitHub UI:**

1. Go to: `Actions` → `New workflow`
2. Search: "CodeQL Analysis"
3. Click: "Configure"
4. Review and commit the workflow file

#### 3.3 CodeQL Configuration

**Default configuration (recommended):**

```yaml
name: "CodeQL"
on:
  push:
    branches: [ "master", "main" ]
  pull_request:
    branches: [ "master", "main" ]
  schedule:
    - cron: '0 12 * * 1'  # Every Monday at noon

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
      contents: read
      actions: read
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: python
          queries: security-extended  # More thorough
      - uses: github/codeql-action/autobuild@v3
      - uses: github/codeql-action/analyze@v3
```

**Custom queries (optional):**

Create `.github/codeql/codeql-config.yml`:

```yaml
name: "Custom CodeQL Config"
disable-default-queries: false

queries:
  - uses: security-extended
  - uses: security-and-quality

paths-ignore:
  - tests/**
  - .venv/**
  - __pycache__/**

paths:
  - scripts/**
```

#### 3.4 First CodeQL Scan

**Trigger first scan:**

```bash
# Option 1: Push a commit
git commit --allow-empty -m "trigger: Initial CodeQL scan"
git push

# Option 2: Manual workflow dispatch
# Go to: Actions → CodeQL → Run workflow
```

**Monitor scan:**
- Go to: `Actions` tab
- Find: "CodeQL" workflow
- Watch progress: ~2-5 minutes for Python
- View results: `Security` → `Code scanning`

**Expected Results:**
- ✅ Zero critical/high issues (our code follows best practices)
- ⚠️ Possible medium/low warnings (review and address)
- 📊 Security score visible in Security tab

---

### Step 4: Configure Dependency Review

#### 4.1 Verify Dependency Review is Active

Navigate to: `Settings` → `Code security and analysis` → `Dependency review`

**Should show:**
```yaml
Status: ✅ Enabled (automatic with Advanced Security)

Configuration:
- Blocks PRs with critical vulnerabilities
- Shows security impact of dependency changes
- Enforces license policy
```

#### 4.2 Configure Policy (Optional)

GitHub Enterprise Cloud allows custom policies:

Navigate to: `Settings` → `Code security and analysis` → `Dependency review` → `Policy`

```yaml
Block pull requests:
☑ Critical vulnerabilities (required)
☑ High vulnerabilities (recommended)
☐ Medium vulnerabilities (optional - may be too strict)
☐ Low vulnerabilities (not recommended)

License policy:
☑ Block copyleft licenses (GPL, LGPL, AGPL)
☑ Allow permissive licenses (MIT, Apache, BSD)
☐ Require manual review for new licenses

Exceptions:
Add specific packages that can bypass policy:
- Example: test-only dependencies
- Example: development tools
```

#### 4.3 Test Dependency Review

**Create test PR with vulnerable dependency:**

```bash
# On a test branch
git checkout -b test-dependency-review

# Add a known vulnerable package (for testing only)
echo "requests==2.0.0  # Known CVE" >> requirements.txt

git add requirements.txt
git commit -m "test: Add vulnerable dependency"
git push -u origin test-dependency-review

# Create PR via GitHub UI
```

**Expected Behavior:**
- ❌ PR shows dependency review warning
- 🛑 PR is blocked from merging
- 📊 Shows security advisory details
- ✅ Must update to safe version to merge

**Clean up:**
```bash
git checkout master
git branch -D test-dependency-review
git push origin --delete test-dependency-review
```

---

### Step 5: Test & Verify

#### 5.1 Test Secret Scanning

**Test push protection:**

```bash
# Create test file with fake API key
echo 'api_key = "ahrefs_test123456789012345678901234567890"' > test_secret.py

git add test_secret.py
git commit -m "test: secret detection"
git push
```

**Expected Result:**
```
❌ Push blocked by secret scanning!

Secret detected:
- Type: Ahrefs API Key
- File: test_secret.py
- Pattern: Custom pattern "Ahrefs API Key"

Options:
1. Remove secret and commit again
2. Bypass (requires justification - audited)
3. Add to allowlist (not recommended)

Recommendation: Remove secret and use environment variables
```

**Clean up:**
```bash
git reset HEAD~1
rm test_secret.py
```

#### 5.2 Verify CodeQL Results

Navigate to: `Security` → `Code scanning`

**Should show:**
- ✅ Latest scan date (within last week)
- 📊 Number of alerts (aim for 0 critical/high)
- 🔍 Scan details (languages, queries used)

**If alerts exist:**
1. Click alert to view details
2. Review code context
3. Fix legitimate issues
4. Dismiss false positives with justification

#### 5.3 Check Dependabot Alerts

Navigate to: `Security` → `Dependabot`

**Should show:**
- ✅ No critical vulnerabilities
- ⚠️ Any known issues with dependencies
- 📦 Auto-generated PRs for security updates

**If vulnerabilities exist:**
1. Review Dependabot PR
2. Test changes locally
3. Merge PR to apply fix
4. Update `requirements.txt` with pinned versions

#### 5.4 Review Security Overview

Navigate to: `Security` → `Security overview`

**Dashboard should show:**
```
Security Features:
✅ Secret scanning: Active
✅ Code scanning: Active
✅ Dependabot: Active
✅ Dependency review: Active

Recent Activity:
- X secrets detected (0 unresolved)
- X code scanning alerts (0 critical)
- X dependency alerts (0 critical)
- Last scan: [timestamp]

Security Score: [Grade]
```

---

## 🔧 Ongoing Maintenance

### Daily
- [ ] Review new secret scanning alerts (if any)
- [ ] Check for high/critical code scanning alerts

### Weekly
- [ ] Review all Dependabot PRs
- [ ] Check CodeQL scan results (Monday scan)
- [ ] Address medium-severity code alerts
- [ ] Update dependencies with security fixes

### Monthly
- [ ] Review security overview dashboard
- [ ] Audit secret scanning allowlist
- [ ] Update custom secret patterns if needed
- [ ] Review and update security policies

### Quarterly
- [ ] Full security audit of all features
- [ ] Review dismissed alerts (re-evaluate)
- [ ] Update CodeQL custom queries
- [ ] Security training for team members

---

## 🚨 Troubleshooting

### Issue: Advanced Security Not Available

**Symptoms:**
- "Enable GitHub Advanced Security" button not visible
- Features grayed out

**Solutions:**
1. Check GitHub plan: Settings → Billing
2. Verify you're on Team or Enterprise Cloud
3. Contact GitHub sales if needed: https://github.com/enterprise/contact
4. Consider upgrading plan

**Alternative:**
Use open-source tools until license obtained:
- `git-secrets` for secret detection
- `bandit` for Python security linting
- `safety` for dependency scanning

### Issue: CodeQL Scan Failing

**Symptoms:**
- Workflow fails with error
- Scan times out
- No results appear

**Solutions:**

```bash
# Check workflow logs
Go to: Actions → Failed workflow → View logs

# Common issues:
1. Permission error:
   - Add security-events: write to workflow

2. Language detection error:
   - Explicitly specify language: python

3. Timeout (rare for our small project):
   - Add timeout-minutes: 360 to job

# Re-run failed workflow
Click: "Re-run failed jobs"
```

### Issue: Too Many False Positives

**Symptoms:**
- Secret scanning alerts for non-secrets
- CodeQL flags safe code patterns

**Solutions:**

**For Secret Scanning:**
```yaml
# Add to allowlist: Settings → Secret scanning → Allowlist
Examples:
- "example_api_key_for_docs"
- "test_token_1234567890"
- "demo_credential_in_readme"

# Or adjust custom pattern regex
Make pattern more specific to reduce false matches
```

**For CodeQL:**
```yaml
# Dismiss with justification
1. Click alert
2. Click "Dismiss alert"
3. Select reason: "False positive"
4. Add comment: "This is safe because [reason]"

# Or add to custom config
.github/codeql/codeql-config.yml:
paths-ignore:
  - path/to/false/positive
```

### Issue: Blocked Push (Push Protection)

**When you see:**
```
❌ Push blocked! Secret detected in commit.
```

**Solutions:**

**Option 1: Remove Secret (Recommended)**
```bash
# Remove the file with secret
git reset HEAD~1
# Edit file to remove secret
# Use environment variable instead
# Commit again without secret
```

**Option 2: Bypass with Justification (Use Sparingly)**
```bash
# GitHub UI will show bypass option
# You must provide justification
# All bypasses are logged and audited

Justification examples:
✅ "Test data for unit tests - not a real key"
✅ "Example in documentation - publicly known"
❌ "It's fine" - not acceptable
❌ "Temporary" - still not safe
```

**Option 3: Add to Allowlist (Rare)**
```
Only for known false positives:
- Example keys in documentation
- Public test credentials
- Non-sensitive identifiers
```

---

## 📊 Security Metrics

### KPIs to Track

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| Unresolved secret alerts | 0 | - | - |
| Critical code alerts | 0 | - | - |
| High code alerts | < 5 | - | - |
| Critical dependency vulns | 0 | - | - |
| Scan failure rate | < 5% | - | - |
| Mean time to remediate | < 48h | - | - |

### Reporting

**Weekly Security Report Template:**

```markdown
# Security Report - Week of [Date]

## Overview
- Secret Scanning: X new alerts, X resolved
- Code Scanning: X new alerts, X resolved
- Dependencies: X updates needed, X applied

## Critical Items
1. [Alert description] - Status: [In Progress/Resolved]
2. [Alert description] - Status: [In Progress/Resolved]

## Actions Taken
- Updated dependency X to version Y
- Dismissed false positive in file Z
- Resolved secret exposure in commit ABC

## Upcoming
- Plan to address [issue]
- Schedule security training
- Update custom patterns
```

---

## 🎓 Team Training

### For Developers

**Security Awareness Training Topics:**
1. Never commit API keys or secrets
2. Use environment variables for credentials
3. Review Dependabot PRs promptly
4. Understand CodeQL alerts before dismissing
5. Follow secure coding practices

**Resources:**
- SECURITY.md (this repository)
- GitHub Security Docs: https://docs.github.com/en/code-security
- OWASP Top 10: https://owasp.org/www-project-top-ten/

### For Admins

**Admin Responsibilities:**
1. Monitor security dashboard daily
2. Review and approve bypass requests
3. Update security policies
4. Respond to critical alerts within 4 hours
5. Coordinate incident response

**Checklist:**
- [ ] Completed security admin training
- [ ] Have admin access to repository
- [ ] Know how to rotate API keys
- [ ] Understand incident response process
- [ ] Contact info for security team

---

## 📞 Support & Resources

### GitHub Support

**For Advanced Security Issues:**
- Support Portal: https://support.github.com
- Email: support@github.com
- Phone: Available for Enterprise customers

**Documentation:**
- Advanced Security: https://docs.github.com/en/code-security
- CodeQL: https://codeql.github.com/docs
- Secret Scanning: https://docs.github.com/en/code-security/secret-scanning

### Internal Support

**Security Questions:**
- Email: andre-external@strategie360consulting.com
- GitHub: Create issue with "security" label

**Emergency Contact (Critical):**
- Email: andre-external@strategie360consulting.com
- Subject: [URGENT SECURITY] [Brief description]
- Response Time: Within 4 hours

---

## ✅ Post-Setup Checklist

After completing all steps, verify:

- [ ] GitHub Advanced Security enabled
- [ ] Secret scanning active with custom patterns
- [ ] Push protection enabled
- [ ] CodeQL scanning running weekly
- [ ] Dependency review blocking vulnerable PRs
- [ ] Dependabot creating security update PRs
- [ ] Security tab shows all features active
- [ ] Team trained on security features
- [ ] Incident response plan documented
- [ ] Security metrics tracking configured

**Congratulations! Your repository now has enterprise-grade security! 🎉**

---

**Document Version:** 1.0
**Last Updated:** December 10, 2025
**Status:** Production Ready (Pending License)
**Maintained By:** andre-external@strategie360consulting.com
