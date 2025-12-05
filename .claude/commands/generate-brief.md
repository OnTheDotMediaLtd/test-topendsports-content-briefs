# Generate Content Brief

Generate a complete 3-phase content brief for: $ARGUMENTS

## MANDATORY WORKFLOW

You MUST execute ALL 3 phases in order. Skipping any phase makes the brief INCOMPLETE.

### Pre-Flight Checklist
- [ ] Read `content-briefs-skill/ORCHESTRATOR.md`
- [ ] Lookup URL in site structure (use MCP tool: `mcp__topendsports-briefs__get_page_info`)
- [ ] Test Ahrefs connectivity

### Phase 1: Research & Discovery
**Reference:** `content-briefs-skill/references/phase1-research.md`

Execute Phase 1 to create:
- `content-briefs-skill/active/[page-name]-phase1.json`
- `content-briefs-skill/output/[page-name]-brief-control-sheet.md`

**Requirements:**
- Use Ahrefs MCP for keyword data
- If MCP fails with 403: `python3 .claude/scripts/ahrefs-api.py [endpoint] [params]`
- Find 8-15 secondary keywords with REAL volume data
- Analyze 3-5 affiliate competitors (NOT brand sites)
- Document brand selection with rationale

### Phase 2: Writer Brief
**Reference:** `content-briefs-skill/references/phase2-writer.md`

Execute Phase 2 using Phase 1 JSON to create:
- `content-briefs-skill/active/[page-name]-phase2.json`
- `content-briefs-skill/output/[page-name]-writer-brief.md`

**Requirements:**
- Map ALL keywords to H2/H3/FAQ sections
- Create 8-10 optimized FAQs
- Specify source requirements (Tier 1 priority)
- Include brand sections with word counts

### Phase 3: AI Enhancement
**Reference:** `content-briefs-skill/references/phase3-technical.md`

Execute Phase 3 using Phase 1 + Phase 2 JSON to create:
- `content-briefs-skill/output/[page-name]-ai-enhancement.md`

**Requirements:**
- Complete HTML/CSS/JS code for all components
- Interactive comparison table
- Schema markup (Article, FAQ, Breadcrumb)
- Complete T&Cs for ALL brands (not just top 3)
- Compliance sections (affiliate disclosure, responsible gambling)

### Final: Convert to DOCX
Use MCP tool: `mcp__topendsports-briefs__convert_to_docx`

Convert all 3 markdown files to Word documents.

## VERIFICATION

Before finishing, confirm ALL 6 files exist:
1. `[page-name]-phase1.json`
2. `[page-name]-phase2.json`
3. `[page-name]-brief-control-sheet.md` + `.docx`
4. `[page-name]-writer-brief.md` + `.docx`
5. `[page-name]-ai-enhancement.md` + `.docx`

## ANTI-PATTERNS (NEVER DO)

- ❌ Skip Phase 1 and go straight to writer brief
- ❌ Use estimated/guessed keyword data instead of Ahrefs
- ❌ Create only 1 file instead of 6
- ❌ Skip Phase 3 AI Enhancement
- ❌ Give up when Ahrefs MCP returns 403 (use Python fallback!)

## AHREFS PYTHON FALLBACK

When MCP fails:
```bash
python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview \
  '{"select":"keyword,volume,difficulty,traffic_potential","country":"us","keywords":"YOUR_KEYWORDS"}'
```

---

Now execute all 3 phases for the URL provided above. Start by reading the ORCHESTRATOR.md file.
