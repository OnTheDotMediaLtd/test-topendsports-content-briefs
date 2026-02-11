# MULTI-AGENT ORCHESTRATOR

**Purpose:** Coordinate multiple specialized agents to generate content briefs efficiently with fresh context per phase.

**Last Updated:** December 8, 2025

---

## CRITICAL CONTENT OUTPUT RULES (Team Feedback - December 2024)

> **ALL agents MUST follow these rules:**

1. **NEVER shorten, compress, or skip content** - Output ALL content in full
2. **Do NOT include max-width CSS** - Site handles maximum content size
3. **No placeholders** - Deliver complete, working code always
4. **ESPN BET is now theScore BET** - Rebranded December 1, 2025
5. **Use Gold Standard Templates** - See `references/gold-standard-templates.md`
6. **Use Letter Badges** - No image logos (FD, DK, MGM, CZR, 365, FAN, SCR, BRV, HRB, BOR)

---

## CRITICAL CONTENT DEPTH RULES (Added December 8, 2025)

> **From SERP analysis feedback:**

1. **Match or exceed #1 ranking page** - Analyze competitor content structure FIRST
2. **Brand count by keyword volume:**
   - 10K+/mo keywords: 8-10 brands
   - 5K-10K/mo: 7-8 brands
   - <5K/mo: 5-7 brands
3. **Per-brand sections (3 required):**
   - Key Features (150-200 words)
   - Mobile Experience (100-150 words) ← NEW
   - Pros/Cons with citations (100-150 words)
4. **Mandatory sections:**
   - Payment methods comparison ← NEW
   - Calculator tool links ← NEW
5. **Word count follows brand depth** - Don't set arbitrary targets; add brands + depth

---

## Architecture

```
Main Orchestrator (You are here)
    ↓
    ├─> [AGENT 1] Phase 1: Research & Discovery (15-20 min)
    │   - Spawns with research-agent context
    │   - MUST analyze #1 ranking page structure
    │   - Outputs: phase1.json + brief-control-sheet.md
    │
    ├─> [AGENT 2] Phase 2: Writer Brief Creation (5-10 min)
    │   - Spawns with writer-agent context + phase1.json
    │   - Outputs: phase2.json + writer-brief.md
    │
    ├─> [AGENTS 3A-3G] Phase 3: Technical Implementation (10-15 min)
    │   - SPLIT INTO 7 PARALLEL SUB-AGENTS (see below)
    │   - Outputs: ai-enhancement.md (concatenated)
    │
    └─> [FINAL] Convert to Word (auto)
        - Runs convert_to_docx.py --all
```

---

## Phase 3: Multi-Agent Execution (REQUIRED)

**Problem:** Phase 3 output exceeds 32,000 token limit for single agent.

**Solution:** Split into 7 parallel sub-agents, then concatenate.

### Phase 3 Sub-Agent Architecture

```
Phase 3 Orchestration:
    │
    ├─> [3A] Meta, badges, disclosure, quick answer (haiku)
    ├─> [3B] Comparison table (haiku)
    ├─> [3C] Brand cards (haiku)
    ├─> [3D] T&Cs (brands 1-5) (haiku)
    ├─> [3E] T&Cs (brands 6-10) (haiku)
    ├─> [3F] Schema markup (haiku)
    └─> [3G] Interactive elements + responsible gambling (haiku)

    ↓ All complete

    Concatenate: cat output/*-phase3[a-g].md > output/[page]-ai-enhancement.md
    Cleanup: rm output/*-phase3[a-g].md
    Fix headings: Convert H1 → H2 for sections 3B-3G
```

### Phase 3 Sub-Agent Prompts

**IMPORTANT:** Each sub-agent MUST output H2 headings (##), not H1 (#), to prevent markdown lint errors after concatenation.

| Agent | Output File | Content |
|-------|-------------|---------|
| 3A | phase3a.md | Meta tags, Last Updated badge, Affiliate disclosure, Quick answer box |
| 3B | phase3b.md | Comparison table (all brands) |
| 3C | phase3c.md | Brand cards (all brands) |
| 3D | phase3d.md | T&Cs for brands 1-5 |
| 3E | phase3e.md | T&Cs for brands 6-10 |
| 3F | phase3f.md | Schema markup (Article, FAQ, Breadcrumb) |
| 3G | phase3g.md | Interactive elements, Responsible gambling |

---

## When User Requests Brief

**Input:** URL like `/sport/betting/nfl-betting-sites.htm` or `/generate-brief [URL]`

**CRITICAL:** Execute IMMEDIATELY when user provides `/generate-brief [URL]`. Do NOT ask for clarification.

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
[Read: references/competitor-content-analysis.md]

**Critical steps:**
1. Search site structure: grep -i "[page_name]" assets/data/site-structure-english.csv
2. **ANALYZE #1 RANKING PAGE** - Count brands, estimate word count, identify sections
3. Research primary keyword + 8-15 secondary keywords + branded keywords
4. Analyze top 3 affiliate competitors
5. Select brands (8-10 for high-volume keywords):
   - FanDuel #1, BetMGM #2 (locked)
   - Research-driven #3-10 (Bet365, DraftKings, theScore BET, Caesars, Fanatics, BetRivers, Hard Rock, Borgata)

**Output requirements:**
- Save JSON: active/[page-name]-phase1.json
- Save Markdown: output/[page-name]-brief-control-sheet.md

**NEW REQUIREMENTS:**
- Match or exceed #1 ranking page brand count
- Plan 3 sections per brand (Key Features, Mobile Experience, Pros/Cons)
- Include payment methods comparison section
- Include calculator tool links

Execute Phase 1 now and report back when complete.
"""
```

**Wait for Agent 1 to complete. Validate with: `bash scripts/validate-phase.sh 1 [page-name]`**

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
3. Create 8-10 FAQ questions targeting high-volume keywords
4. Specify source requirements (TIER 1: App Store, Reddit)
5. **Include Mobile Experience section per brand**
6. **Include Payment methods comparison section**
7. **Include Calculator tool links**

**Output requirements:**
- Save JSON: active/[page-name]-phase2.json
- Save Markdown: output/[page-name]-writer-brief.md

Execute Phase 2 now and report back when complete.
"""
```

**Wait for Agent 2 to complete. Validate with: `bash scripts/validate-phase.sh 2 [page-name]`**

### Step 3.5: MANDATORY Brand Validation Gate

**CRITICAL:** After Phase 2 completes, MUST validate all brand names before proceeding to Phase 3.

```bash
python scripts/validate_brands_gate.py output/[page-name]-writer-brief.md
```

**This validation:**
- ✅ Accepts verified sportsbook brands (FanDuel, BetMGM, DraftKings, etc.)
- ❌ BLOCKS suspicious/fake brands (Treasure Spins, Royalistplay, etc.)
- 💡 Suggests corrections for typos (Wyns → WynnBET)

**Exit codes:**
- 0 = Validation passed, proceed to Phase 3
- 1 = BLOCKED - fake brands detected, FIX BEFORE PROCEEDING
- 2 = Validation error (file missing, etc.)

**If validation FAILS:**
1. Review the unknown/suspicious brands listed in the output
2. Edit `output/[page-name]-writer-brief.md` to replace with verified brands
3. Re-run validation until it passes
4. DO NOT proceed to Phase 3 until validation passes

**Why this matters:** Prevents hallucinated brand names like "Treasure Spins Sport" from being delivered to production. This gate caught 3 fake brands in recent briefs that would have otherwise been published.

### Step 4: Spawn Phase 3 Sub-Agents (PARALLEL)

**CRITICAL:** Spawn all 7 sub-agents in a SINGLE message with multiple Task tool calls.

```
// Agent 3A - Meta, badges, disclosure
Task(subagent_type="general-purpose", model="haiku",
     description="Phase 3A: Meta and badges",
     prompt="Create phase3a.md with: Meta tags, Last Updated badge, Affiliate disclosure, Quick answer box...")

// Agent 3B - Comparison table
Task(subagent_type="general-purpose", model="haiku",
     description="Phase 3B: Comparison table",
     prompt="Create phase3b.md with comparison table for ALL brands. Use H2 headings...")

// Agent 3C - Brand cards
Task(subagent_type="general-purpose", model="haiku",
     description="Phase 3C: Brand cards",
     prompt="Create phase3c.md with brand cards for ALL brands. Use H2 headings...")

// Agent 3D - T&Cs (brands 1-5)
Task(subagent_type="general-purpose", model="haiku",
     description="Phase 3D: T&Cs brands 1-5",
     prompt="Create phase3d.md with T&Cs for brands 1-5. Use H2 headings...")

// Agent 3E - T&Cs (brands 6-10)
Task(subagent_type="general-purpose", model="haiku",
     description="Phase 3E: T&Cs brands 6-10",
     prompt="Create phase3e.md with T&Cs for brands 6-10. Use H2 headings...")

// Agent 3F - Schema markup
Task(subagent_type="general-purpose", model="haiku",
     description="Phase 3F: Schema markup",
     prompt="Create phase3f.md with Article, FAQ (all questions), Breadcrumb schema...")

// Agent 3G - Interactive + Responsible gambling
Task(subagent_type="general-purpose", model="haiku",
     description="Phase 3G: Interactive elements",
     prompt="Create phase3g.md with bonus calculator, state checker, responsible gambling...")
```

**Wait for ALL sub-agents to complete.**

### Step 5: Concatenate Phase 3 Outputs
```bash
cd output
cat [page]-phase3a.md [page]-phase3b.md [page]-phase3c.md [page]-phase3d.md [page]-phase3e.md [page]-phase3f.md [page]-phase3g.md > [page]-ai-enhancement.md
rm [page]-phase3[a-g].md
```

### Step 6: Validate Phase 3
```bash
bash scripts/validate-phase.sh 3 [page-name]
```

### Step 7: Convert to Word
```bash
mcp__topendsports-briefs__convert_to_docx with files=["--all"]
```

### Step 8: Report Completion
```
All 3 phases complete. Brief package delivered:
- Phase 1: Brief Control Sheet (research findings, keyword cluster)
- Phase 2: Writer Brief (content outline, optimization)
- Phase 3: AI Enhancement Brief (HTML, schema, code)
- All converted to .docx format

Files located in: output/[page-name]-*
```

---

## Brand Badge Reference

| Brand | Badge | Color |
|-------|-------|-------|
| FanDuel | FD | #1493FF |
| BetMGM | MGM | #C4A137 |
| Bet365 | 365 | #027B5B |
| DraftKings | DK | #53D337 |
| theScore BET | SCR | #6B2D5B |
| Caesars | CZR | #0A2240 |
| Fanatics | FAN | #004C91 |
| BetRivers | BRV | #1E5AA8 |
| Hard Rock Bet | HRB | #000000 |
| Borgata | BOR | #8B0000 |

---

## Quality Checks

After each agent completes:
- ✅ Verify output files exist
- ✅ Check file sizes are reasonable (not empty)
- ✅ Validate JSON structure (for phase1.json and phase2.json)
- ✅ Confirm keyword counts match requirements
- ✅ Confirm brand count matches #1 competitor (8-10 for high-volume)
- ✅ Run validation script: `bash scripts/validate-phase.sh [phase] [page-name]`
- 🚨 **MANDATORY after Phase 2:** Run brand validation gate: `python scripts/validate_brands_gate.py output/[page-name]-writer-brief.md`

---

## Error Handling

### Phase 3 Token Limit Error
If single Phase 3 agent fails with token limit error:
- Use the 7 sub-agent pattern described above
- Each sub-agent uses `model="haiku"` for efficiency

### Markdown Lint Failures
Common issues and fixes:
- **MD025 (multiple H1):** Ensure sub-agents use H2 headings
- **MD042 (empty links):** Use real URLs, not `[text](#)`
- **MD046 (code block style):** Disabled in .markdownlint.json

### Agent Failure
1. Check error message from agent
2. Verify input files exist (for Phase 2/3)
3. Retry agent with clarified instructions
4. If repeated failures, check token limits

---

## Usage

When user says: `/generate-brief [URL]`

**Execute IMMEDIATELY:**
1. Spawn Agent 1 (Phase 1) - Research
2. Wait + Validate
3. Spawn Agent 2 (Phase 2) - Writer
4. Wait + Validate
5. Spawn Agents 3A-3G (Phase 3) - Technical (PARALLEL)
6. Wait + Concatenate + Validate
7. Convert to Word
8. Commit + Push
9. Report success

**Total time:** ~15-25 minutes for complete brief package

---

## Lessons Learned (December 8, 2025)

1. **Don't wait for clarification** - Execute /generate-brief immediately
2. **Phase 3 needs splitting** - Single agent exceeds token limits
3. **Match competitor depth** - Analyze #1 ranking page first
4. **8-10 brands for high-volume** - Not 5-7
5. **Mobile Experience section** - Per brand, currently missing
6. **Payment methods section** - Competitors have this
7. **Calculator links** - Leverage existing site tools
