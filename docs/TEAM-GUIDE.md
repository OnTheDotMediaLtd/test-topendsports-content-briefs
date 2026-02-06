# Team Guide: Getting Started with GitHub & Content Briefs

This guide is for team members who are new to GitHub. It explains how to access and download content briefs.

---

## Quick Links

- **Repository:** https://github.com/OnTheDotMediaLtd/topendsports-content-briefs
- **Download Briefs:** See "How to Download Briefs" section below

---

## GitHub Basics (Simple Explanation)

### What is GitHub?
GitHub is like a shared folder in the cloud, but with superpowers:
- Everyone can see the files
- It keeps track of all changes (like Google Docs history)
- Multiple people can work on files without overwriting each other

### Key Terms (Simple Definitions)

| Term | What it means |
|------|---------------|
| **Repository (Repo)** | The project folder containing all our files |
| **Branch** | A separate copy where changes are made before adding to the main version |
| **Main** | The official/approved version of all files |
| **Pull Request (PR)** | A request to add changes from a branch into main |
| **Commit** | A saved snapshot of changes (like pressing "Save") |
| **Clone** | Download a copy of the repo to your computer |
| **Pull** | Get the latest updates from GitHub to your computer |
| **Push** | Send your changes from your computer to GitHub |

---

## How to Download Briefs

### Option 1: Download Individual Files (Easiest)

1. Go to https://github.com/OnTheDotMediaLtd/topendsports-content-briefs
2. Click on `content-briefs-skill` folder
3. Click on `output` folder
4. Click on any `.docx` or `.md` file you want
5. Click the **"Download"** button (or "Raw" then right-click > Save)

### Option 2: Download All Briefs at Once

1. Go to https://github.com/OnTheDotMediaLtd/topendsports-content-briefs
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Extract the ZIP file
5. Find briefs in: `content-briefs-skill/output/`

### Option 3: Using GitHub Desktop (Recommended for Regular Use)

1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in with your GitHub account
3. Click "Clone a repository"
4. Enter: `OnTheDotMediaLtd/topendsports-content-briefs`
5. Choose where to save it on your computer
6. Click "Clone"

**To get updates later:**
- Open GitHub Desktop
- Click "Fetch origin" then "Pull origin"

---

## Where Are the Briefs Located?

```
content-briefs-skill/
├── output/                    ← COMPLETED BRIEFS ARE HERE
│   ├── [page-name]-brief-control-sheet.md
│   ├── [page-name]-brief-control-sheet.docx
│   ├── [page-name]-writer-brief.md
│   ├── [page-name]-writer-brief.docx
│   ├── [page-name]-ai-enhancement.md
│   └── [page-name]-ai-enhancement.docx
│
├── active/                    ← Work-in-progress (JSON data files)
│   ├── [page-name]-phase1.json
│   └── [page-name]-phase2.json
│
└── feedback/                  ← Submit feedback on briefs here
    └── submitted/
```

### File Types Explained

| Extension | What it is | Who uses it |
|-----------|------------|-------------|
| `.docx` | Word document | Writers - open with Microsoft Word |
| `.md` | Markdown file | Developers - plain text with formatting |
| `.json` | Data file | System use only - contains research data |

---

## How to Submit Feedback on a Brief

1. Go to: https://github.com/OnTheDotMediaLtd/topendsports-content-briefs/issues
2. Click **"New Issue"**
3. Choose **"Brief Feedback"** template (if available)
4. Fill in:
   - Which brief you're reviewing
   - Rating (1-5)
   - What was good
   - What needs improvement
5. Click **"Submit new issue"**

---

## Getting Help

- **GitHub Help:** https://docs.github.com/en/get-started
- **Ask the Team:** Post in your team chat
- **Report Issues:** https://github.com/OnTheDotMediaLtd/topendsports-content-briefs/issues

---

## Common Questions

**Q: I can't find a brief I need?**
A: Check if it's been created yet. Look in `content-briefs-skill/output/` folder. If it's not there, it may still be in progress (check `active/` folder).

**Q: The brief is outdated?**
A: Click "Fetch origin" in GitHub Desktop, or refresh the GitHub website page to see the latest version.

**Q: I want to suggest a change to a brief?**
A: Create an Issue on GitHub (see "How to Submit Feedback" above).

**Q: What's a "Pull Request" I keep seeing?**
A: It's how we add new changes to the main version. Someone proposes changes, others review them, then they get merged in. You can ignore these unless you're reviewing changes.
