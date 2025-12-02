# MULTI-AGENT ORCHESTRATOR

**Purpose:** Coordinate multiple specialized agents to generate content briefs efficiently with fresh context per phase.

## Architecture

```
Main Orchestrator (You are here)
    ↓
    ├─> [AGENT 1] Phase 1: Research & Discovery (10-15 min)
    │   - Spawns with research-agent context
    │   - Outputs: phase1.json + brief-control-sheet.md
    │
    ├─> [AGENT 2] Phase 2: Writer Brief Creation (5-10 min)
    │   - Spawns with writer-agent context + phase1.json
    │   - Outputs: phase2.json + writer-brief.md
    │
    ├─> [AGENT 3] Phase 3: Technical Implementation (10-15 min)
    │   - Spawns with technical-agent context + phase1.json + phase2.json
    │   - Outputs: ai-enhancement.md
    │
    └─> [FINAL] Convert to Word (auto)
        - Runs convert_to_docx.py --all
```

## When User Requests Brief

**Input:** URL like `/sport/betting/nfl-betting-sites.htm`

**Orchestration Steps:**

### Step 1: Extract Page Name
```python
url = "/sport/betting/nfl-betting-sites.htm"
page_name = url.split('/')[-1].replace('.htm', '')  # "nfl-betting-sites"
```

### Step 2: Spawn Phase 1 Agent
```
Use Task tool with:
- subagent_type: "general-purpose"
- description: "Research & keyword analysis for [page_name]"
- prompt: """
You are executing Phase 1 (Research & Discovery) for the TES betting content brief system.

**Your task:** Generate a Brief Control Sheet for [URL]

**Instructions to follow:**
[Read and follow: references/phase1-research.md]

**Critical steps:**
1. Search site structure: grep -i "[page_name]" assets/data/site-structure-english.csv
2. Research primary keyword + 8-15 secondary keywords
3. Analyze top 3 affiliate competitors (actionnetwork.com, covers.com, thelines.com)
4. Identify competitor gaps
5. Select brands (FanDuel #1, BetMGM #2, research-driven #3-7)

**Output requirements:**
- Save JSON: active/[page-name]-phase1.json
- Save Markdown: output/[page-name]-brief-control-sheet.md

**Data files available:**
- assets/data/site-structure-english.csv
- assets/data/site-structure-spanish.csv

**Reference docs available:**
- references/phase1-research.md (YOUR MAIN INSTRUCTIONS)
- references/reference-library.md (quick lookups)
- references/lessons-learned.md (mistakes to avoid)

Execute Phase 1 now and report back when complete.
"""
```

**Wait for Agent 1 to complete.**

### Step 3: Spawn Phase 2 Agent
```
Use Task tool with:
- subagent_type: "general-purpose"
- description: "Create writer brief for [page_name]"
- prompt: """
You are executing Phase 2 (Writer Brief Creation) for the TES betting content brief system.

**Your task:** Generate a Writer Brief for [page_name]

**Instructions to follow:**
[Read and follow: references/phase2-writer.md]

**Input data:**
[Read: active/[page-name]-phase1.json]

**Critical steps:**
1. Load Phase 1 keyword cluster and brand selection
2. Build keyword-optimized content outline (map secondary keywords to H2/H3/FAQ)
3. Create 7 FAQ questions targeting high-volume keywords
4. Specify source requirements (TIER 1: App Store, Reddit)
5. Format writer brief with all optimization details

**Output requirements:**
- Save JSON: active/[page-name]-phase2.json
- Save Markdown: output/[page-name]-writer-brief.md

**Reference docs available:**
- references/phase2-writer.md (YOUR MAIN INSTRUCTIONS)
- references/reference-library.md (quick lookups)
- references/content-templates.md (outline structures)

Execute Phase 2 now and report back when complete.
"""
```

**Wait for Agent 2 to complete.**

### Step 4: Spawn Phase 3 Agent
```
Use Task tool with:
- subagent_type: "general-purpose"
- description: "Build technical implementation for [page_name]"
- prompt: """
You are executing Phase 3 (Technical Implementation) for the TES betting content brief system.

**Your task:** Generate an AI Enhancement Brief with complete HTML/code for [page_name]

**Instructions to follow:**
[Read and follow: references/phase3-technical.md]

**Input data:**
[Read: active/[page-name]-phase1.json]
[Read: active/[page-name]-phase2.json]

**Critical steps:**
1. Build meta tags with ALL keywords from Phase 2
2. Create comparison table with researched brands from Phase 1
3. Build interactive elements based on competitor gaps from Phase 1
4. Generate complete T&Cs sections for all featured brands
5. Create schema markup (Article, FAQ with Phase 2 questions, Breadcrumb)
6. Add compliance sections (affiliate disclosure, responsible gambling)

**Output requirements:**
- Save Markdown with HTML: output/[page-name]-ai-enhancement.md

**Reference docs available:**
- references/phase3-technical.md (YOUR MAIN INSTRUCTIONS)
- references/reference-library.md (quick lookups)
- references/verification-standards.md (T&Cs standards)

Execute Phase 3 now and report back when complete.
"""
```

**Wait for Agent 3 to complete.**

### Step 5: Convert to Word
```bash
python scripts/convert_to_docx.py --all
```

### Step 6: Report Completion
```
All 3 phases complete. Brief package delivered:
- Phase 1: Brief Control Sheet (research findings, keyword cluster)
- Phase 2: Writer Brief (content outline, optimization)
- Phase 3: AI Enhancement Brief (HTML, schema, code)
- All converted to .docx format

Files located in: output/[page-name]-*
```

## Benefits of Multi-Agent Approach

1. **Fresh Context:** Each agent starts with clean context, preventing token overflow
2. **Focused Expertise:** Each agent only loads instructions for their phase
3. **Better Error Recovery:** If one phase fails, can retry that agent without redoing all
4. **Parallel Potential:** Future enhancement could parallelize independent research tasks
5. **Quality Control:** Each agent can be tested independently

## Quality Checks

After each agent completes:
- ✅ Verify output files exist
- ✅ Check file sizes are reasonable (not empty)
- ✅ Validate JSON structure (for phase1.json and phase2.json)
- ✅ Confirm keyword counts match requirements

## Error Handling

If agent fails:
1. Check error message from agent
2. Verify input files exist (for Phase 2/3)
3. Retry agent with clarified instructions
4. If repeated failures, fall back to single-agent mode

## Usage

When user says: `generate brief for /sport/betting/[page].htm`

Execute this orchestration automatically:
1. Spawn Agent 1 (Phase 1)
2. Wait for completion
3. Spawn Agent 2 (Phase 2)
4. Wait for completion
5. Spawn Agent 3 (Phase 3)
6. Wait for completion
7. Convert to Word
8. Report success

Total time: ~25-40 minutes for complete brief package
