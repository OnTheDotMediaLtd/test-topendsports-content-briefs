# TROUBLESHOOTING GUIDE

Common issues and solutions for the TopEndSports Content Briefs workflow.

## Table of Contents

1. [Ahrefs API Issues](#ahrefs-api-issues)
2. [MCP Server Issues](#mcp-server-issues)
3. [Phase 1 Issues](#phase-1-issues)
4. [Phase 2 Issues](#phase-2-issues)
5. [Phase 3 Issues](#phase-3-issues)
6. [Multi-Agent Issues](#multi-agent-issues)
7. [Data Issues](#data-issues)
8. [Output Issues](#output-issues)

---

## Ahrefs API Issues

### Problem: Rate Limit Exceeded
**Symptoms:** API returns 429 error, requests fail with "too many requests"
**Cause:** Ahrefs API has strict rate limits (typically 500 requests/day for standard plans)
**Solution:**
1. Check current usage: `mcp__ahrefs__doc` to see rate limit status
2. Implement exponential backoff in retry logic
3. Reduce parallel requests or batch keyword queries
**Prevention:** Cache API responses, use keyword lists instead of individual queries, schedule jobs to spread requests over 24 hours

### Problem: Authentication Failures
**Symptoms:** 401/403 errors, "Invalid API token" messages
**Cause:** Expired, incorrect, or missing API token in environment variables
**Solution:**
1. Verify token in `.env` file: `AHREFS_API_TOKEN=your_token`
2. Check token permissions in Ahrefs dashboard
3. Regenerate token if compromised
**Prevention:** Use secure credential management, set token expiry reminders, test authentication before bulk operations

### Problem: No Data Returned for Target
**Symptoms:** Empty results, zero keywords/backlinks for valid URLs
**Cause:** Domain not in Ahrefs index, new site, or insufficient data
**Solution:**
1. Check domain age and authority using `site-explorer-metrics`
2. Verify URL format (include protocol: https://)
3. Try parent domain if subdomain has no data
**Prevention:** Pre-validate targets against Ahrefs index, maintain minimum DR threshold (e.g., DR > 5)

### Problem: Wrong Country Data
**Symptoms:** Keywords/volumes don't match target region (US vs global)
**Cause:** Incorrect `country` parameter in API calls
**Solution:**
1. Set `country: "us"` explicitly in all keyword/SERP calls
2. Verify country codes match Ahrefs format (ISO 2-letter)
3. Check `volume_mode` parameter for local vs global volumes
**Prevention:** Standardize country parameter in configuration file, validate before API calls

### Problem: Incomplete Keyword Data
**Symptoms:** Missing search volume, CPC, or difficulty scores
**Cause:** API response doesn't include all requested fields
**Solution:**
1. Add `select` parameter with all required fields: `select: "keyword,volume,cpc,difficulty"`
2. Check if premium fields require higher API tier
3. Use `keywords-explorer-overview` for comprehensive data
**Prevention:** Document required fields per endpoint, validate response schemas

### Problem: Competitor Analysis Fails
**Symptoms:** No competitors returned or low-quality matches
**Cause:** Insufficient common keywords, target too niche, or wrong mode parameter
**Solution:**
1. Lower minimum common keyword threshold
2. Use `organic-competitors` with `mode: "domain"` for broader matches
3. Increase `limit` parameter to get more results
**Prevention:** Set realistic competitor thresholds based on niche (5-10 common keywords minimum)

### Problem: Historical Data Gaps
**Symptoms:** Missing data points in date ranges, incomplete trends
**Cause:** Ahrefs doesn't crawl all sites daily, data aggregation delays
**Solution:**
1. Use `history_grouping: "monthly"` instead of daily for more complete data
2. Extend `date_from` range to capture more history
3. Check if target domain has consistent crawl coverage
**Prevention:** Request weekly/monthly aggregations, avoid relying on daily granularity

### Problem: Timeout Errors
**Symptoms:** Requests hang or return 504 gateway timeout
**Cause:** Complex queries (large domains, broad filters) exceed default timeout
**Solution:**
1. Add `timeout: 600000` (10 minutes) to API calls
2. Narrow query scope with `where` filters
3. Reduce `limit` parameter for initial testing
**Prevention:** Start with small limits, progressively increase, use pagination for large datasets

### Problem: Invalid Target Format
**Symptoms:** "Invalid target" or parsing errors from API
**Cause:** Malformed URLs, missing protocols, invalid characters
**Solution:**
1. Normalize URLs: lowercase, remove trailing slashes
2. Ensure protocol is included: `https://example.com`
3. URL-encode special characters in paths
**Prevention:** Implement URL validation function, sanitize inputs from CSV before API calls

### Problem: SERP Data Mismatch
**Symptoms:** SERP results don't match manual Google searches
**Cause:** Ahrefs SERP data is point-in-time, may differ from live results
**Solution:**
1. Check `date` parameter matches intended timeframe
2. Note Ahrefs updates SERP data every few days
3. Use `top_positions: 10` to see full first page
**Prevention:** Accept lag between live SERPs and Ahrefs data, use most recent available date

---

## MCP Server Issues

### Problem: MCP Connection Refused
**Symptoms:** "Cannot connect to MCP server", ECONNREFUSED errors
**Cause:** MCP server not running, wrong port, or firewall blocking
**Solution:**
1. Start MCP server: `npm run mcp:start` or check process manager
2. Verify port in config matches server: default 3000
3. Check firewall rules allow localhost connections
**Prevention:** Add MCP server to startup scripts, use health check endpoint before workflows

### Problem: CSV Parsing Failures
**Symptoms:** "Invalid CSV format", missing columns, encoding errors
**Cause:** Wrong delimiter, BOM characters, or unexpected column structure
**Solution:**
1. Verify CSV encoding is UTF-8 without BOM
2. Check delimiter matches expected (comma vs semicolon)
3. Validate required columns exist: URL, Section, Writer, Priority
**Prevention:** Use CSV linting tool, standardize export format, add schema validation step

### Problem: DOCX Conversion Errors
**Symptoms:** Generated DOCX files are corrupted or won't open
**Cause:** Invalid XML in document structure, image embedding issues
**Solution:**
1. Check markdown input for malformed HTML tags
2. Verify image URLs are accessible before embedding
3. Use `docx` library's debug mode to see XML errors
**Prevention:** Sanitize markdown before conversion, validate images exist, use error boundaries

### Problem: Resource Not Found
**Symptoms:** MCP server returns 404 for CSV/template resources
**Cause:** File paths incorrect, resources not mounted in server config
**Solution:**
1. Check MCP server resource configuration in `mcp.json`
2. Verify file paths are absolute or relative to server root
3. Test resource access: `ListMcpResourcesTool` to see available resources
**Prevention:** Document resource URIs, use constants for paths, add startup validation

### Problem: Memory Exhaustion
**Symptoms:** MCP server crashes with OOM errors during large operations
**Cause:** Processing entire site structure CSV in memory, large DOCX files
**Solution:**
1. Increase Node.js heap: `NODE_OPTIONS=--max-old-space-size=4096`
2. Implement streaming for large CSV files
3. Process site structure in batches (e.g., 100 rows at a time)
**Prevention:** Profile memory usage, add pagination to CSV endpoints, limit concurrent DOCX conversions

### Problem: MCP Request Timeout
**Symptoms:** Long-running MCP operations timeout before completion
**Cause:** Default timeout too short for complex operations (DOCX generation, full CSV parse)
**Solution:**
1. Increase timeout in MCP client config: `timeout: 300000` (5 minutes)
2. Add progress callbacks for long operations
3. Break large operations into smaller chunks
**Prevention:** Set realistic timeouts per operation type, implement streaming responses

### Problem: Encoding Issues in Output
**Symptoms:** Special characters appear as �, accented letters broken
**Cause:** Charset mismatch between MCP server and output files
**Solution:**
1. Set explicit UTF-8 encoding in all file operations
2. Add BOM to DOCX XML if needed for Office compatibility
3. Test with special characters: é, ñ, —, "smart quotes"
**Prevention:** Standardize on UTF-8 everywhere, add encoding tests to CI pipeline

### Problem: Stale Cache Data
**Symptoms:** MCP returns outdated CSV data after file updates
**Cause:** Server caching resource reads without invalidation
**Solution:**
1. Restart MCP server to clear cache
2. Add cache-busting query params or timestamp checks
3. Implement file watcher to invalidate cache on changes
**Prevention:** Use shorter cache TTL (5-10 minutes), add manual cache clear endpoint

---

## Phase 1 Issues

### Problem: URL Not in Site Structure CSV
**Symptoms:** Cannot find target URL when searching site structure
**Cause:** URL not added to CSV yet, typo in URL, or CSV not updated
**Solution:**
1. Search CSV with normalized URL (lowercase, no trailing slash)
2. Add missing URL to appropriate section in site structure
3. Verify CSV has been reloaded by MCP server
**Prevention:** Maintain URL inventory, validate against live sitemap, automate CSV updates

### Problem: Insufficient Keyword Volume
**Symptoms:** Found keywords but need 8-15, only have 3-5
**Cause:** Topic too niche, overly restrictive filters, or wrong seed keywords
**Solution:**
1. Expand seed keywords: use `related-terms` and `search-suggestions`
2. Lower volume threshold (e.g., 10+ instead of 50+)
3. Include long-tail variations and question keywords
**Prevention:** Start with broad seed terms, use multiple keyword discovery methods, accept lower volumes for niche topics

### Problem: No Competitor Data Available
**Symptoms:** Competitor analysis returns empty or only 1-2 competitors
**Cause:** Target domain too unique, new domain, or overly narrow niche
**Solution:**
1. Use parent domain instead of specific page for competitor discovery
2. Expand to related topics with `matching-terms` keyword research
3. Manually identify 2-3 competitors and analyze their keywords
**Prevention:** Accept that some niches have few direct competitors, focus on keyword opportunities instead

### Problem: Brand Selection Conflicts
**Symptoms:** Multiple brand affiliates available, unclear which to prioritize
**Cause:** Product available from multiple partners (Amazon, SportsDirect, etc.)
**Solution:**
1. Check commission rates: prioritize higher-paying affiliates
2. Consider availability: Amazon for US, SportsDirect for UK
3. Use brand preference order: 1) Specialized brands, 2) Amazon, 3) General retailers
**Prevention:** Document brand priority matrix per product category, standardize in configuration

### Problem: Wrong Topical Authority Score
**Symptoms:** Ahrefs shows high authority but content is thin or off-topic
**Cause:** Domain has general authority but weak topical clusters
**Solution:**
1. Filter to specific subfolder/section: `mode: "prefix"`
2. Analyze keyword clustering: are ranking keywords actually on-topic?
3. Check DR vs topic relevance separately
**Prevention:** Use subfolder-level analysis, validate keyword relevance manually for new topics

### Problem: SERP Intent Mismatch
**Symptoms:** Top ranking pages don't match intended content type (e.g., products vs info)
**Cause:** Keyword has mixed or transactional intent, SERP dominated by different format
**Solution:**
1. Analyze `intent` field in SERP overview: informational vs commercial
2. Check top 3 results: are they similar to planned content?
3. Adjust content angle or choose different primary keyword
**Prevention:** Always review top 10 SERP results before finalizing keyword selection

### Problem: Duplicate Keyword Clusters
**Symptoms:** Multiple similar keywords selected (e.g., "best basketball shoes", "top basketball shoes")
**Cause:** Keyword tools return variations that target same SERP
**Solution:**
1. Check if keywords share top 5 ranking URLs using SERP overlap
2. Group near-duplicates and pick highest volume variant
3. Use others as secondary/LSI keywords
**Prevention:** Run SERP similarity check, merge clusters with >70% URL overlap

### Problem: Seasonal Keyword Issues
**Symptoms:** Keyword has high volume but only during specific months
**Cause:** Topic is seasonal (e.g., "super bowl predictions", "olympic events")
**Solution:**
1. Check `volume-history` endpoint for monthly trends
2. Note seasonality in brief, plan publish date accordingly
3. Consider year-round alternative keywords
**Prevention:** Always check 12-month volume history, flag seasonal topics in brief

### Problem: Missing Content Gap Analysis
**Symptoms:** Brief lacks competitive advantage angle, unclear differentiation
**Cause:** Insufficient analysis of what competitors are missing
**Solution:**
1. Compare top 5 competitor outlines: note common sections
2. Identify gaps: topics mentioned in 0-1 competitor articles
3. Highlight these gaps as "unique angle" in brief
**Prevention:** Standardize gap analysis template, require minimum 3 gap opportunities per brief

### Problem: Keyword Difficulty Miscalculation
**Symptoms:** Target keyword marked as "easy" but dominated by DR 80+ domains
**Cause:** Ahrefs KD score doesn't account for content quality or user intent match
**Solution:**
1. Manually review top 10: check DR, content depth, brand strength
2. Adjust internal difficulty rating based on realistic competitiveness
3. Note if top results are weak content (thin, outdated)
**Prevention:** Use hybrid scoring: Ahrefs KD + manual SERP review, document realistic targets

---

## Phase 2 Issues

### Problem: Writer Assignment Mismatch
**Symptoms:** Brief assigned to writer unfamiliar with topic
**Cause:** CSV has wrong writer name or writer availability not checked
**Solution:**
1. Verify writer name matches exactly in site structure CSV
2. Check writer specialty: sports vs fitness vs nutrition
3. Reassign in CSV if needed, regenerate brief
**Prevention:** Maintain writer expertise matrix, validate assignments during CSV updates

### Problem: Section Mapping Failures
**Symptoms:** Cannot determine correct site section for URL
**Cause:** URL structure doesn't match expected patterns in site structure
**Solution:**
1. Check URL path matches section prefix in CSV
2. For new sections, add pattern to site structure mapping
3. Default to closest parent section if no exact match
**Prevention:** Document URL structure conventions, update patterns when adding new sections

### Problem: Insufficient FAQ Count
**Symptoms:** Only 2-3 FAQs generated, need 5-8 minimum
**Cause:** Limited "People Also Ask" data from Ahrefs or narrow topic
**Solution:**
1. Query multiple related keywords for FAQ data
2. Use `search-suggestions` for question variations
3. Manually craft FAQs from competitor content if needed
**Prevention:** Set minimum FAQ threshold (5), use multiple PAA sources, validate before finalizing

### Problem: Source Quality Issues
**Symptoms:** Brief cites low-authority or off-topic sources
**Cause:** Automated source gathering doesn't validate relevance/authority
**Solution:**
1. Filter sources by DR > 50 or trusted domain list
2. Manually review top 5 sources for topical relevance
3. Prioritize .edu, .gov, sports associations, peer-reviewed studies
**Prevention:** Maintain trusted domain whitelist, require human source review for technical topics

### Problem: Missing Content Angles
**Symptoms:** Brief is generic, lacks unique perspective or hook
**Cause:** Template filled mechanically without strategic thinking
**Solution:**
1. Review content gap analysis from Phase 1
2. Add specific angles: beginner vs pro, budget options, injury prevention
3. Include 2-3 unique insights competitors don't cover
**Prevention:** Require "unique angle" field in brief template, validate during QA

### Problem: Inconsistent Tone Guidelines
**Symptoms:** Tone description vague or contradicts site style
**Cause:** Generic tone instructions not tailored to TopEndSports voice
**Solution:**
1. Reference style guide: conversational, authoritative, encouraging
2. Add specific examples: "Use 2nd person (you), avoid jargon"
3. Note any topic-specific tone adjustments (serious for injuries, energetic for training)
**Prevention:** Standardize tone template per content type, include example sentences

### Problem: Word Count Unrealistic
**Symptoms:** Brief specifies 3000 words for simple "how-to" or 800 words for comprehensive guide
**Cause:** Word count set by formula without considering content complexity
**Solution:**
1. Review top 3 competitor lengths, aim for 20% longer
2. Adjust based on section count: 150-250 words per section
3. Set realistic range: 1500-2500 for most articles
**Prevention:** Use competitor average + 20% as baseline, validate against section outline

### Problem: Metadata Incomplete
**Symptoms:** Missing meta description, title tag, or slug
**Cause:** Metadata generation step skipped or failed
**Solution:**
1. Generate title tag: 50-60 chars, include primary keyword
2. Write meta description: 140-160 chars, include CTA
3. Create slug: lowercase, hyphens, primary keyword
**Prevention:** Add metadata validation step, use templates for consistency

---

## Phase 3 Issues

### Problem: Token Limit Exceeded
**Symptoms:** Content generation fails with "context too long" error
**Cause:** Full brief + instructions + examples exceed model's context window (200k tokens)
**Solution:**
1. Split into 7 sub-agents: Intro, 5 main sections, Conclusion
2. Pass only relevant section brief to each agent
3. Use parallel execution to speed up generation
**Prevention:** Always use multi-agent approach for articles >2000 words, monitor token usage

### Problem: HTML Formatting Missing
**Symptoms:** Output is plain text or markdown, missing semantic HTML
**Cause:** Agent prompt doesn't specify HTML output format
**Solution:**
1. Add explicit instruction: "Return as semantic HTML5"
2. Specify required tags: `<article>`, `<h2>`, `<p>`, `<ul>`, `<strong>`
3. Validate HTML structure before concatenation
**Prevention:** Include HTML template in prompt, show examples of expected output

### Problem: Schema Markup Incomplete
**Symptoms:** Missing schema.org JSON-LD for FAQPage, Article, or Product
**Cause:** Schema generation agent not invoked or missing required fields
**Solution:**
1. Generate FAQPage schema for FAQ section
2. Add Article schema with author, datePublished, description
3. Include Product schema if reviewing specific items
**Prevention:** Checklist required schemas per content type, validate JSON-LD syntax

### Problem: Terms & Conditions Missing
**Symptoms:** Affiliate disclosure or site T&Cs not included in output
**Cause:** Boilerplate insertion step skipped
**Solution:**
1. Add affiliate disclosure before first product mention
2. Include standard disclaimer at article end
3. Verify T&C text matches current legal requirements
**Prevention:** Automate T&C insertion, maintain versioned boilerplate templates

### Problem: Sub-Agent Spawn Failures
**Symptoms:** Not all 7 agents launch, some sections missing
**Cause:** Resource limits, rate limiting, or orchestration errors
**Solution:**
1. Check system resources: memory, CPU, API quotas
2. Implement retry logic for failed spawns
3. Validate all agents complete before concatenation
**Prevention:** Add health checks before spawning, limit concurrent agents if needed

### Problem: Section Concatenation Errors
**Symptoms:** Sections out of order, duplicate content, or missing transitions
**Cause:** Improper merging of sub-agent outputs
**Solution:**
1. Enforce strict ordering: Intro → Section 1-5 → Conclusion → FAQ
2. Remove duplicate headers or paragraphs during merge
3. Add transition sentences between major sections
**Prevention:** Use section markers in prompts, validate structure after concatenation

### Problem: Inconsistent Voice Across Sections
**Symptoms:** Tone shifts noticeably between sections (formal → casual)
**Cause:** Different sub-agents interpret tone guidelines differently
**Solution:**
1. Use identical tone instructions for all agents
2. Add specific examples of voice in each section prompt
3. Run consistency check agent to harmonize tone post-generation
**Prevention:** Standardize tone examples, use same temperature/model settings for all agents

### Problem: Missing Internal Links
**Symptoms:** No links to other TopEndSports pages, missed SEO opportunity
**Cause:** Agents don't have access to site structure for link opportunities
**Solution:**
1. Pass relevant CSV rows to each agent: related pages in same section
2. Instruct to include 3-5 internal links per 1000 words
3. Format as HTML anchor tags with descriptive text
**Prevention:** Provide link suggestions in section brief, validate minimum link count

### Problem: Image Placeholders Not Resolved
**Symptoms:** Output contains `[Image: description]` instead of actual images
**Cause:** Image sourcing/embedding not implemented in workflow
**Solution:**
1. Generate image descriptions during content creation
2. Use separate process to source/generate images
3. Insert image HTML with alt text and captions
**Prevention:** Document image workflow, assign image sourcing to specific team member

### Problem: Fact-Checking Errors
**Symptoms:** Statistics, names, or facts are incorrect or outdated
**Cause:** AI generates plausible but inaccurate information
**Solution:**
1. Require citation for all statistics and claims
2. Add verification step: validate facts against sources
3. Flag uncertain information for human review
**Prevention:** Emphasize accuracy in prompts, use RAG with trusted sources, mandatory human fact-check

---

## Multi-Agent Issues

### Problem: Agent Spawn Race Conditions
**Symptoms:** Agents overwrite each other's outputs or access shared resources simultaneously
**Cause:** Lack of synchronization in parallel execution
**Solution:**
1. Use unique output files per agent: `section_1.html`, `section_2.html`
2. Implement file locking if writing to shared database
3. Coordinate with orchestrator: spawn → execute → collect pattern
**Prevention:** Isolate agent workspaces, use message queues for coordination

### Problem: Concatenation Order Errors
**Symptoms:** Sections appear in wrong order in final document
**Cause:** Async execution completes out of order, improper sorting
**Solution:**
1. Use explicit section numbers in filenames: `01_intro.html`, `02_section1.html`
2. Sort outputs by filename before concatenation
3. Validate section headers match expected order
**Prevention:** Enforce naming convention, add order validation step

### Problem: Markdown Linting Failures (MD025)
**Symptoms:** Markdown lint error "Multiple top-level headings in same document"
**Cause:** Each section has H1, concatenation creates multiple H1s
**Solution:**
1. Use H2 for section titles, reserve H1 for article title only
2. Strip H1 from section outputs before concatenation
3. Add article title H1 during final assembly
**Prevention:** Instruct section agents to start with H2, validate heading hierarchy

### Problem: Encoding Corruption in Merge
**Symptoms:** Special characters broken when combining section outputs
**Cause:** Inconsistent encoding across section files
**Solution:**
1. Force UTF-8 encoding when reading/writing all section files
2. Add BOM stripping to avoid duplication
3. Test merge with special characters: em dash, curly quotes, accented letters
**Prevention:** Standardize encoding in all file operations, add encoding tests

### Problem: Timeout in Orchestration
**Symptoms:** Orchestrator gives up before all agents complete
**Cause:** Some agents take longer than expected, timeout too aggressive
**Solution:**
1. Increase orchestrator timeout: 15-20 minutes for 7 agents
2. Add progress monitoring: log when each agent completes
3. Implement partial success: complete sections even if one agent fails
**Prevention:** Profile agent execution times, set realistic timeouts, add fallback logic

### Problem: Memory Leaks in Long-Running Orchestrator
**Symptoms:** Orchestrator process memory grows unbounded, eventual crash
**Cause:** Section outputs held in memory, not released after processing
**Solution:**
1. Write section outputs to disk immediately, clear from memory
2. Stream final concatenation instead of building entire document in memory
3. Add garbage collection hints after major operations
**Prevention:** Profile memory usage, use streaming wherever possible, limit in-memory buffering

### Problem: Error Propagation Failures
**Symptoms:** Individual agent errors not reported, workflow appears to succeed but output is incomplete
**Cause:** Try-catch blocks swallow errors without proper logging
**Solution:**
1. Log all errors with context: which agent, which section, stack trace
2. Fail fast: halt orchestration if any critical agent fails
3. Return error summary in final output metadata
**Prevention:** Implement structured error handling, add error aggregation in orchestrator

### Problem: Inconsistent Formatting Across Agents
**Symptoms:** Some sections use bullet lists, others use numbered lists for similar content
**Cause:** Agents interpret formatting instructions differently
**Solution:**
1. Provide explicit formatting rules per section type: use bullets for features, numbers for steps
2. Add formatting examples in prompts
3. Run formatting normalization pass after concatenation
**Prevention:** Standardize formatting guide, validate consistency in QA

---

## Data Issues

### Problem: Duplicate URLs in Site Structure
**Symptoms:** Same URL appears multiple times in CSV with different metadata
**Cause:** Manual CSV updates without deduplication, data import errors
**Solution:**
1. Run deduplication script: `csvtool dedupe -k url site_structure.csv`
2. Merge metadata: keep most recent writer assignment, highest priority
3. Validate no duplicates remain before loading into MCP
**Prevention:** Add unique constraint on URL column, validate on CSV import, automate deduplication

### Problem: Wrong Writer Assignment
**Symptoms:** Content doesn't match writer's expertise (fitness writer gets nutrition topic)
**Cause:** CSV not updated after writer specialization changes
**Solution:**
1. Review writer expertise matrix, update assignments
2. Bulk update CSV for similar topics: all "basketball" → Writer A
3. Validate writer-topic match during brief generation
**Prevention:** Maintain writer profiles with topic tags, automate assignment suggestions

### Problem: Spanish Translation Errors (Vosotros vs Ustedes)
**Symptoms:** Spanish content uses vosotros (Spain) instead of ustedes (Latin America) or vice versa
**Cause:** Translation model defaults to European Spanish, inconsistent dialect settings
**Solution:**
1. Specify target dialect in translation prompt: "Latin American Spanish (ustedes form)"
2. Find/replace: vosotros → ustedes, os → les
3. Validate with native speaker or dialect-specific grammar checker
**Prevention:** Set default dialect in configuration, add dialect validation step

### Problem: Inconsistent URL Schemes
**Symptoms:** Some URLs have www., others don't; http vs https mixed
**Cause:** URLs added manually without normalization
**Solution:**
1. Normalize all URLs: force https://, strip www. (or add consistently)
2. Update CSV with normalized versions
3. Add URL normalization function called before any operations
**Prevention:** Implement URL normalization at data entry point, validate format on import

### Problem: Missing Required Fields
**Symptoms:** CSV rows have empty Writer, Priority, or Section columns
**Cause:** Incomplete data entry, import from partial source
**Solution:**
1. Identify rows with missing fields: `csvtool filter -e writer,priority,section`
2. Fill defaults: Priority=3, Section=infer from URL path
3. Flag for manual review if Writer cannot be determined
**Prevention:** Add field validation on CSV import, require all fields or explicit null value

### Problem: Encoding Issues in CSV
**Symptoms:** Special characters corrupted when opening CSV in Excel
**Cause:** CSV saved without UTF-8 BOM, Excel defaults to ANSI
**Solution:**
1. Re-save CSV as "UTF-8 with BOM" in text editor
2. Verify special characters display correctly: é, ñ, —
3. Document encoding requirement in CSV guidelines
**Prevention:** Always use UTF-8 with BOM for Excel compatibility, add encoding check to validation

### Problem: Outdated Competitor Data
**Symptoms:** Competitor analysis references sites that no longer rank or are offline
**Cause:** Competitor data cached from months ago, not refreshed
**Solution:**
1. Re-run competitor analysis from Phase 1
2. Update site structure CSV with current competitors
3. Validate competitor URLs are still live (return 200)
**Prevention:** Add competitor data timestamp, refresh quarterly, validate URLs before use

### Problem: Inconsistent Brand Names
**Symptoms:** Same brand spelled differently: "Nike" vs "NIKE" vs "Nike, Inc."
**Cause:** Manual entry without standardization
**Solution:**
1. Create brand name authority list with canonical forms
2. Find/replace variants with canonical name
3. Validate brand names against authority list
**Prevention:** Use dropdown/autocomplete for brand entry, maintain brand database

---

## Output Issues

### Problem: DOCX File Corruption
**Symptoms:** Generated DOCX won't open in Word or Google Docs
**Cause:** Invalid XML structure, improper image embedding, or encoding issues
**Solution:**
1. Validate HTML input before DOCX conversion: check for unclosed tags
2. Test with minimal content to isolate issue (text only, then add images)
3. Use `docx` library's validation mode to identify XML errors
**Prevention:** Sanitize HTML before conversion, validate DOCX with automated test, limit image sizes

### Problem: Missing Output Files
**Symptoms:** Workflow completes but expected files (brief, DOCX, HTML) not generated
**Cause:** File write failures, path errors, or premature process termination
**Solution:**
1. Check file permissions on output directory
2. Verify output paths are absolute, not relative
3. Add error handling to catch write failures and log details
**Prevention:** Validate output directory exists and is writable before starting, add file existence checks

### Problem: Brand Badge Images Broken
**Symptoms:** Affiliate brand logos don't display or show broken image icons
**Cause:** Image URLs invalid, images not accessible, or HTML img tags malformed
**Solution:**
1. Validate image URLs return 200 before embedding
2. Use data URIs for small badges to avoid external dependencies
3. Add fallback alt text if image fails to load
**Prevention:** Host badge images locally or on CDN, validate images during brief creation

### Problem: Formatting Lost in DOCX
**Symptoms:** Bullet lists, bold, italics render as plain text in Word
**Cause:** HTML to DOCX conversion doesn't handle all formatting tags
**Solution:**
1. Use supported HTML tags: `<strong>`, `<em>`, `<ul>`, `<ol>`, avoid `<div>`
2. Test conversion with sample formatted content
3. Add custom styling in DOCX template for unsupported elements
**Prevention:** Document supported HTML subset, validate formatting after conversion

### Problem: Incorrect File Naming
**Symptoms:** Output files have generic names (brief_1.docx) instead of descriptive names
**Cause:** Filename generation doesn't use article title or URL slug
**Solution:**
1. Generate filename from title: `basketball-training-tips-brief.docx`
2. Sanitize: lowercase, replace spaces with hyphens, remove special chars
3. Add date prefix if needed: `2025-01-15_basketball-training-tips.docx`
**Prevention:** Implement filename generation function, validate uniqueness

### Problem: Oversized DOCX Files
**Symptoms:** DOCX files are 10+ MB for articles with few images
**Cause:** Embedded images not compressed, high-resolution originals included
**Solution:**
1. Compress images before embedding: max 1920px width, 80% JPEG quality
2. Use web-optimized formats: WebP or optimized JPEG
3. Consider linking to images instead of embedding
**Prevention:** Add image optimization step to workflow, set max file size limits

---

## Quick Reference

### Phase 1 Checklist
- [ ] URL exists in site structure CSV
- [ ] 8-15 target keywords identified with volumes
- [ ] 3-5 competitors analyzed
- [ ] Brand affiliates selected per product category
- [ ] Content gaps documented

### Phase 2 Checklist
- [ ] Writer assigned matches expertise
- [ ] Section mapped to site structure
- [ ] 5-8 FAQs from PAA data
- [ ] Sources validated (DR >50, topically relevant)
- [ ] Metadata complete (title, description, slug)

### Phase 3 Checklist
- [ ] 7 sub-agents spawned successfully
- [ ] HTML formatting semantic and valid
- [ ] Schema markup included (Article, FAQPage)
- [ ] Terms & conditions inserted
- [ ] Internal links added (3-5 per 1000 words)

### Common Commands

```bash
# Validate CSV format
csvtool validate -s site_structure_schema.json site_structure.csv

# Deduplicate URLs
csvtool dedupe -k url site_structure.csv -o site_structure_clean.csv

# Normalize URLs in CSV
csvtool transform -f url -t normalize site_structure.csv

# Test Ahrefs API connection
curl -H "Authorization: Bearer $AHREFS_API_TOKEN" https://api.ahrefs.com/v3/site-explorer/metrics

# Restart MCP server
npm run mcp:restart

# Validate DOCX file
docx-validator output.docx

# Check HTML formatting
html-validator --format=html5 output.html

# Test multi-agent orchestration
npm run test:orchestrator -- --sections=7 --timeout=20m
```

### Contact & Escalation

For issues not resolved by this guide:
1. Check project GitHub issues for similar problems
2. Review recent commits for related changes
3. Contact technical lead with error logs and reproduction steps
4. Escalate critical blockers (API outages, data corruption) immediately

---

**Document Version:** 1.0
**Last Updated:** 2025-12-09
**Maintained By:** TopEndSports Technical Team
