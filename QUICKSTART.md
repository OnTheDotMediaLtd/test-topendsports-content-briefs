# Quick Start Guide
## TopEndSports Content Briefs Generation System

Welcome! This guide will get you up and running with the content brief generation system in under 10 minutes.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Choose Your Workflow](#choose-your-workflow)
4. [Generate Your First Brief](#generate-your-first-brief)
5. [Understanding the Output](#understanding-the-output)
6. [Common Workflows](#common-workflows)
7. [Troubleshooting](#troubleshooting)
8. [Getting Help](#getting-help)

---

## Prerequisites

Before you start, make sure you have:

- ✅ **GitHub access** to this repository
- ✅ **Claude Code installed** on your computer ([Download here](https://code.claude.com))
- ✅ **Git installed** ([Download here](https://git-scm.com/downloads))
- ✅ **Python 3.x** (for document conversion) - Optional but recommended

**Check if you have Git:**
```bash
git --version
```

**Check if you have Python:**
```bash
python --version
```

---

## Installation

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
# Navigate to where you want the project
cd Documents  # or Desktop, or wherever you prefer

# Clone the repository
git clone https://github.com/OnTheDotMediaLtd/topendsports-content-briefs.git

# Enter the project folder
cd topendsports-content-briefs
```

### Step 2: Verify Files

Check that you have these folders:
```
topendsports-content-briefs/
├── content-briefs-v1/          ← Agent-based system
├── content-briefs-skill/       ← Skill-based system (recommended)
├── README.md
├── CONTRIBUTING.md
└── QUICKSTART.md               ← You are here!
```

### Step 3: Open in Claude Code

**Option A: From Terminal**
```bash
cd content-briefs-skill
claude-code .
```

**Option B: From Claude Code**
1. Open Claude Code
2. Use File → Open Folder
3. Navigate to `content-briefs-skill/` folder

---

## Choose Your Workflow

You have two options. **We recommend the Skill version** for most users.

### Option 1: Skill-Based (Recommended) 🌟

**Location:** `content-briefs-skill/`

**Best for:**
- New team members
- Streamlined workflow
- All-in-one brief generation
- Built-in quality checks

**How it works:**
- Single command generates all 3 briefs
- Automatic phase management
- Built-in feedback system

### Option 2: Agent-Based (Advanced)

**Location:** `content-briefs-v1/`

**Best for:**
- Advanced users
- Custom workflows
- Phase-by-phase control
- Experimentation

**How it works:**
- Run phases individually
- More granular control
- Requires manual phase management

---

## Generate Your First Brief

Let's create a content brief using the **Skill-based system** (recommended).

### Step 1: Open the Skill Folder

```bash
cd content-briefs-skill
```

Open this folder in Claude Code (or navigate to it if already open).

### Step 2: Choose a URL

Pick a URL from the site structure. Common examples:

- `/sport/betting/nfl/index.htm` - Best NFL Betting Sites
- `/sport/betting/nba/index.htm` - Best NBA Betting Sites
- `/sport/betting/best-apps.htm` - Best Sports Betting Apps

**Want to see all available URLs?** Open:
```
assets/data/site-structure-english.csv
```

### Step 3: Generate the Brief

In Claude Code, simply say:

```
generate brief for /sport/betting/nfl/index.htm
```

Or more casually:

```
create a content brief for NFL betting sites
```

```
I need a writer brief for /sport/betting/best-apps.htm
```

### Step 4: Watch the Magic Happen

Claude Code will:

1. **Phase 1 (Research)** - 10-15 minutes
   - Look up URL in site structure
   - Research keywords with Ahrefs
   - Find 8-15 secondary keywords
   - Analyze competitors
   - Output: Brief Control Sheet

2. **Phase 2 (Writer Brief)** - 5-10 minutes
   - Create keyword-optimized outline
   - Assign correct writer
   - Specify source requirements
   - Output: Writer Brief

3. **Phase 3 (AI Enhancement)** - 10-15 minutes
   - Build HTML components
   - Add schema markup
   - Include compliance sections
   - Output: AI Enhancement Brief

4. **Final Step (Convert to Word)**
   - Converts all markdown files to .docx
   - Ready for content writers

**Total Time:** ~30-40 minutes for complete brief package

### Step 5: Review Your Output

Find your briefs in the `output/` folder:

```
output/
├── nfl-betting-sites-brief-control-sheet.md
├── nfl-betting-sites-brief-control-sheet.docx
├── nfl-betting-sites-writer-brief.md
├── nfl-betting-sites-writer-brief.docx
├── nfl-betting-sites-ai-enhancement.md
└── nfl-betting-sites-ai-enhancement.docx
```

---

## Understanding the Output

### Brief Control Sheet (Phase 1)
**Purpose:** Research findings and strategic direction
**Audience:** SEO team, project managers
**Contains:**
- Primary keyword + 8-15 secondary keywords
- Total search volume (target: 400-900% increase)
- Competitor analysis
- Writer assignment
- Template selection

**Example:**
```
Primary Keyword: best nfl betting sites (400/mo)
Secondary Keywords:
  - nfl betting apps (1,200/mo) → H2
  - nfl parlay betting (1,500/mo) → H2
  - how to bet on nfl (600/mo) → H3
Total Cluster Volume: 3,700/mo (925% increase)
```

### Writer Brief (Phase 2)
**Purpose:** Instructions for human content writer
**Audience:** Content writers
**Contains:**
- Keyword-optimized outline (H2, H3, FAQ)
- Word count requirements
- Source guidelines (Tier 1-4)
- Brand positioning
- Compliance requirements

**Example Structure:**
```
H1: Best NFL Betting Sites - Expert Reviews & Rankings

H2: Top 7 NFL Betting Sites 2025 (nfl betting sites - 400/mo)
  - FanDuel (Position #1)
  - BetMGM (Position #2)
  - [Research-driven #3-7]

H2: How to Choose an NFL Sportsbook (how to bet on nfl - 600/mo)
H2: NFL Betting Apps Compared (nfl betting apps - 1,200/mo)
H3: Live NFL Betting Features
H3: NFL Parlay Betting Options (nfl parlay betting - 1,500/mo)

FAQ:
  - Which app is best for NFL betting?
  - Can I bet on NFL games legally?
```

### AI Enhancement Brief (Phase 3)
**Purpose:** Technical implementation with HTML/code
**Audience:** Developers, AI content systems
**Contains:**
- HTML tables (comparison, odds, bonuses)
- Schema markup (FAQPage, Review, Organization)
- Calculators and interactive elements
- Complete T&Cs for all brands
- Compliance sections (age, hotline, disclosure)

---

## Common Workflows

### Workflow 1: Generate a Single Brief

**Use case:** Creating one new page

```bash
# Open skill folder in Claude Code
cd content-briefs-skill

# In Claude Code, say:
generate brief for [URL]
```

**Time:** 30-40 minutes

---

### Workflow 2: Batch Generate Multiple Briefs

**Use case:** Creating multiple pages at once

```bash
# In Claude Code, say:
generate briefs for these URLs:
- /sport/betting/nfl/index.htm
- /sport/betting/nba/index.htm
- /sport/betting/mlb/index.htm
```

**Time:** 30-40 minutes per brief (can run sequentially)

---

### Workflow 3: Update an Existing Brief

**Use case:** Refreshing old content with new keywords

```bash
# In Claude Code, say:
update the brief for /sport/betting/nfl/index.htm with latest keyword research
```

**Time:** 20-30 minutes

---

### Workflow 4: Generate Only One Phase

**Use case:** Need just research or just writer brief

**Using Agent-based system (content-briefs-v1):**

```bash
# In Claude Code, say:
run phase 1 for /sport/betting/nfl/index.htm

# Or run just phase 2:
run phase 2 for nfl-betting-sites

# Or run just phase 3:
run phase 3 for nfl-betting-sites
```

---

### Workflow 5: Spanish Content

**Use case:** Creating Spanish content for /es/ URLs

```bash
# In Claude Code, say:
generate brief for /es/sport/betting/mejores-casas-apuestas.htm
```

**System automatically:**
- Uses Spanish site structure CSV
- Assigns to Gustavo Cantella
- Targets USA Spanish speakers (not Spain)
- Uses correct age (21+) and language ("ustedes")

---

## Troubleshooting

### Problem: URL Not Found in Site Structure

**Error message:** "URL not found in site structure CSV"

**Solution:**
1. Check the CSV file: `assets/data/site-structure-english.csv`
2. If URL is missing, Claude Code will proceed with manual assignment
3. You'll be asked to provide:
   - Target keyword
   - Writer assignment
   - Template type

---

### Problem: Ahrefs API Not Working

**Error message:** "Ahrefs unavailable" or API errors

**Solution:**
1. System will fall back to web search for keyword estimates
2. Output will be marked as "estimated" data
3. Contact admin to check Ahrefs API key configuration

**To test Ahrefs manually:**
```bash
# In Claude Code, say:
test ahrefs connection for topendsports.com
```

---

### Problem: Python Script Fails (Word Conversion)

**Error message:** "Python script error" or docx conversion fails

**Solution:**
1. Check Python is installed: `python --version`
2. Install required packages:
```bash
cd content-briefs-skill/scripts
pip install python-docx markdown
```
3. Manually convert files:
```bash
python convert_to_docx.py --all
```

**Note:** Markdown (.md) files are still generated even if .docx conversion fails.

---

### Problem: Wrong Writer Assigned

**Issue:** Brief assigned to wrong writer

**Solution:**
1. Check site structure CSV for correct writer
2. If CSV is wrong, update the CSV file
3. Regenerate the brief
4. Or manually edit the Writer Brief document

**Writer Assignment Rules:**
- Spanish URLs (/es/) → Always Gustavo Cantella
- Check CSV first
- High priority → Lewis Humphries
- Supporting content → Tom Goldsmith

---

### Problem: Not Enough Secondary Keywords

**Issue:** Only finding 3-4 secondary keywords instead of 8-15

**Solution:**
1. System will warn you: "Secondary keyword count low"
2. Ask Claude Code to research more:
```bash
find more secondary keywords for [topic]
```
3. Expand search to related topics
4. Consider parent/child topic variations

**Target:** 400-900% increase in total search volume

---

### Problem: Git Conflicts

**Error message:** "Your local changes would be overwritten by merge"

**Solution:**
```bash
# Save your work first
git status

# Stash your changes
git stash

# Pull latest changes
git pull

# Reapply your changes
git stash pop

# If conflicts, resolve them in your editor
```

---

### Problem: Can't Push to GitHub

**Error message:** "Permission denied" or "Authentication failed"

**Solution:**
1. Check you have write access to the repository
2. Configure Git credentials:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@company.com"
```
3. For authentication, use GitHub Personal Access Token:
   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Create token with "repo" permissions
   - Use token as password when pushing

---

## Getting Help

### Quick Reference

**Common Commands:**
```bash
# Generate a brief
generate brief for [URL]

# Check status
show active briefs
show completed briefs

# Test systems
test ahrefs connection
verify site structure data

# Convert to Word
python scripts/convert_to_docx.py --all
```

---

### Documentation Files

- **README.md** - Project overview
- **CONTRIBUTING.md** - Team workflow guidelines
- **QUICKSTART.md** - This guide
- **references/** - Detailed phase instructions (skill version)
- **templates/** - Content templates (v1 version)

---

### File Locations Reference

**Skill Version (content-briefs-skill/):**
```
├── SKILL.md                    ← Main configuration
├── ORCHESTRATOR.md             ← Workflow orchestration
├── references/
│   ├── phase1-research.md      ← Phase 1 instructions
│   ├── phase2-writer.md        ← Phase 2 instructions
│   ├── phase3-technical.md     ← Phase 3 instructions
│   ├── reference-library.md    ← Quick lookups
│   └── quality-checklist.md    ← Pre-delivery check
├── assets/data/
│   ├── site-structure-english.csv
│   └── site-structure-spanish.csv
├── scripts/
│   └── convert_to_docx.py
├── output/                     ← Generated briefs
└── active/                     ← Work-in-progress
```

**Agent Version (content-briefs-v1/):**
```
├── CLAUDE.md                   ← Main configuration
├── agents/
│   ├── research-agent.md       ← Phase 1
│   ├── writer-agent.md         ← Phase 2
│   └── technical-agent.md      ← Phase 3
├── data/
│   ├── site-structure-english.csv
│   └── site-structure-spanish.csv
├── templates/
│   └── reference-library.md
├── scripts/
│   └── convert_to_docx.py
├── output/                     ← Generated briefs
└── active/                     ← Work-in-progress
```

---

### Support Channels

**GitHub Issues:**
- Bug reports → Use "Bug Report" template
- Feature requests → Use "Feature Request" template
- Content brief requests → Use "Content Brief Request" template

**Internal:**
- Contact project maintainer
- Slack channel: #content-briefs (if applicable)
- Email: [your team email]

---

## Success Checklist

Before delivering a brief to writers, verify:

- ✅ Primary keyword identified from site structure
- ✅ 8-15 secondary keywords researched
- ✅ Total search volume calculated (target: 400-900% increase)
- ✅ Competitor analysis completed (affiliate sites, not brand pages)
- ✅ Correct writer assigned
- ✅ Template selected (1, 2, 3, or 4)
- ✅ Brand positioning: FanDuel #1, BetMGM #2
- ✅ Compliance sections included
- ✅ Both .md and .docx files generated
- ✅ No dated language in titles
- ✅ Tier 1 sources prioritized (real users)

---

## What's Next?

Now that you're set up:

1. **Generate your first brief** following the steps above
2. **Review the output** - familiarize yourself with the 3 deliverables
3. **Provide feedback** - use the feedback system in `feedback/` folder
4. **Share with team** - teach others using this guide
5. **Create your first PR** - commit a completed brief

**Questions?** Create an issue on GitHub or contact the team.

---

## Quick Tips

💡 **Tip 1:** Always check the site structure CSV first - it has keyword mappings
💡 **Tip 2:** Target 400-900% search volume increase with secondary keywords
💡 **Tip 3:** Save work in `active/` folder - never loses progress
💡 **Tip 4:** FanDuel always #1, BetMGM always #2 - non-negotiable
💡 **Tip 5:** Spanish content → Always Gustavo, always 21+, always USA-focused
💡 **Tip 6:** Use Tier 1 sources (App Store, Reddit, Trustpilot) for pros/cons
💡 **Tip 7:** Never use dated language in titles ("2025", "October 2025")
💡 **Tip 8:** Both .md and .docx are generated - writers prefer .docx

---

**Happy brief generating! 🚀**

*Last updated: December 2025*
