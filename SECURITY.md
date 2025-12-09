# Security Policy

## Supported Versions

This project is actively maintained. Security updates are provided for the latest version.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability in the TopEndSports Content Briefs project, please report it privately:

### How to Report

1. **Email:** andre-external@strategie360consulting.com
2. **GitHub Security Advisory:** Use the "Security" tab to create a private security advisory
3. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to Expect

- **Acknowledgment:** Within 48 hours
- **Assessment:** Within 1 week
- **Fix Timeline:** Depends on severity
  - Critical: 1-3 days
  - High: 1-2 weeks
  - Medium: 2-4 weeks
  - Low: Next release cycle
- **Disclosure:** Coordinated disclosure after fix is released

## Security Best Practices

### For Contributors

1. **Never commit:**
   - API keys or tokens (especially Ahrefs API key)
   - Passwords or credentials
   - Personal identifiable information (PII)
   - Internal URLs or IP addresses

2. **API Security:**
   - Ahrefs API key must be in environment variables only
   - Never hardcode API keys in Python scripts
   - Use .env files (excluded from git via .gitignore)
   - Rotate API keys if accidentally exposed

3. **Python Scripts:**
   - Review all scripts for code injection vulnerabilities
   - Sanitize user inputs in validation scripts
   - Use subprocess with proper escaping
   - Validate file paths before file operations

4. **MCP Server Security:**
   - Validate all inputs to MCP server endpoints
   - Sanitize CSV data before processing
   - Use secure file handling for DOCX conversion
   - Prevent path traversal attacks

5. **Dependencies:**
   - Keep dependencies updated
   - Review dependency security advisories
   - Use `pip install -r requirements.txt` with pinned versions
   - Audit new dependencies before adding

### For Content Brief Generation

1. **Input Validation:**
   - Validate URLs before processing
   - Sanitize keywords and search terms
   - Validate CSV data structure
   - Check for malicious content in source data

2. **Data Handling:**
   - Site structure CSVs contain sensitive business data
   - Competitor analysis data should not be publicly exposed
   - Brand positioning rules are confidential
   - Writer assignments may contain PII

3. **Output Security:**
   - Generated briefs may contain proprietary research
   - Keyword data reveals SEO strategy
   - HTML/JavaScript code should be validated for XSS
   - Schema markup should not leak sensitive data

## Security Features

### Implemented

- ✅ API key in environment variables (not hardcoded)
- ✅ Private repository with access controls
- ✅ GitHub Actions for automated checks
- ✅ Python scripts with input validation
- ✅ MCP server with request validation
- ✅ .gitignore prevents committing sensitive files

### Planned

- [ ] Dependency vulnerability scanning (Dependabot configured)
- [ ] Code scanning with CodeQL
- [ ] Secret scanning alerts
- [ ] Branch protection rules

## Security Updates

Security updates will be announced through:
- GitHub Security Advisories
- Release notes
- Repository README

## Compliance

This project handles:
- ❌ No personal data
- ❌ No health information
- ❌ No financial information
- ✅ Proprietary business data (SEO research, brand positioning)
- ✅ API credentials (Ahrefs)

**Data Classification:**
- Site structure CSVs: Confidential
- Keyword research: Confidential
- Competitor analysis: Confidential
- Generated briefs: Internal use only
- Code and documentation: Private repository

## Secure Development Guidelines

### When Adding New Features

1. **API Integration:**
   - Use environment variables for credentials
   - Implement rate limiting
   - Handle API errors gracefully
   - Log security-relevant events

2. **File Processing:**
   - Validate file paths
   - Check file sizes
   - Scan for malicious content
   - Use secure temp directories

3. **Data Processing:**
   - Validate CSV structure before parsing
   - Sanitize inputs from external sources
   - Use parameterized queries if adding database
   - Implement proper error handling

4. **Code Review:**
   - Review for injection vulnerabilities
   - Check authentication/authorization logic
   - Validate input handling
   - Review dependencies for known issues

## Incident Response

In case of security incident:

1. **Containment:**
   - Rotate compromised API keys immediately
   - Revoke access if unauthorized access detected
   - Take affected systems offline if necessary

2. **Investigation:**
   - Document timeline of events
   - Identify scope of compromise
   - Determine root cause
   - Assess data exposure

3. **Recovery:**
   - Apply security patches
   - Restore from clean backups if needed
   - Verify system integrity
   - Update security controls

4. **Notification:**
   - Notify affected parties
   - Report to appropriate authorities if required
   - Document lessons learned
   - Update security procedures

---

Last updated: December 2025
