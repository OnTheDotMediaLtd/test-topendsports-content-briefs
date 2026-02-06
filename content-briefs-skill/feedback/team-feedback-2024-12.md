# Team Feedback Collection - December 2024

**Collected by:** Andre Borg
**Date:** December 3, 2024
**Purpose:** Identify pain points, improvements, and project ideas

---

## Summary of Key Issues

### 1. Content Shortening/Skipping (CRITICAL - Multiple Reports)
**Reported by:** Gustavo, Lewis, Daniel
- Claude tends to shorten responses recently
- Skips key points that were mentioned to be kept in mind
- Skips information when formatting new content
- Sometimes refuses to break up extra long text into artifacts

### 2. Long Conversation Limits
**Reported by:** Lewis, Daniel
- Chat resets mid-conversation
- "Conversation too long" message prevents continuing work
- Compacting problem causes loss of context

### 3. Response Wait Times
**Reported by:** [Team member]
- Long waits before getting output
- Claude can't handle big requests lately

### 4. CSS Conflict Issue (RESOLVED)
**Status:** Fixed by devs
**Issue:** AI-generated content included hardcoded CSS (e.g., `max-width: 1200px`) that conflicted with site styling, causing mobile display issues.
**Solution:** Instruct AI: "Do not include max-width CSS on its elements in the content"
**Action:** Add this rule to content generation instructions.

---

## Individual Feedback

### Gustavo
**Pain Points:**
- Claude can't handle big requests lately
- Claude and Gemini skip information when formatting

**Current Projects Used:**
- TES - Article Formatting & Optimizations
- TES - Calculator Pages
- Uses Gemini with published page code as example

**Workflow Improvement Needed:**
- Fix AI skipping content while formatting

---

### [Team Member 2]
**Pain Points:**
- Long wait times for output
- Sometimes needs to tweak input for correct output

**Current Projects Used:**
- TES - Article Formatting and Optimization

**Workflow Improvement Needed:**
- Getting the right references, quotes, and information in text

---

### Lewis
**Pain Points:**
- Claude shortens responses
- Skips key points mentioned
- "Conversation too long" message is frustrating

**Current Projects Used:**
- TES Content Brief Generator for ES Sports Betting Structure
- Internal Linking strategy project (custom, in development)

**Workflow Improvement Needed:**
- Fix conversation length limits
- Stop Claude from skipping important information

**Project Ideas:**
- Internal Linking process automation

---

### Daniel
**Pain Points:**
- Chat resets issue (previously reported)
- AI refuses to break up long text into artifacts (sporadic)

**Current Projects Used:**
- TES - Betting Content Generation
- TES - Article Formatting and Optimization

**Project Ideas:**
- Automatic bonus editing/updating project for when bonuses change across pages

---

## Actionable Improvements

### Immediate Actions
1. **Add CSS Rule:** Include in all content generation instructions:
   > "Do not include max-width CSS on elements. Maximum content size is handled by site CSS."

2. **Anti-Skipping Instructions:** Add explicit rules to prevent content shortening:
   > "NEVER shorten, compress, or skip content. Output ALL content in full."

3. **Chunking Strategy:** For long content, implement explicit chunking:
   > "Break content into artifacts/sections. Never combine sections to save space."

### Project Ideas to Develop
1. **Bonus Update Automation** - Auto-edit bonuses across multiple pages
2. **Internal Linking Assistant** - Help with on-page internal linking strategy

### Systemic Issues (Claude Platform)
- Long conversation limits (platform limitation)
- Response time slowness (platform issue)
- Artifact generation inconsistency

---

### [Additional Team Member - Quality Feedback]
**Date Added:** December 3, 2024

**Quality Issues Reported:**
1. **Literal Interpretation Problem:**
   - When user says "add 5 major sportsbooks in the US", AI literally uses that phrase as an H2
   - Should convert to keyword-optimized heading instead
   - Example: "5 major sportsbooks in the US" → "Best US Sportsbooks for [Sport] Betting"

2. **Duplicate Content Problem:**
   - Quick answer box and affiliate disclosure formatted correctly at top
   - But the paragraphs used to generate the info appear right below it
   - Same content appears twice (easy fix to delete, but shouldn't happen)

**Action Taken:** Added to Content Output Rules and Common Mistakes sections

---

### Remi Helgheim
**Date Added:** December 3, 2024

**Pain Points:**
- Running out of resources (context limits)
- Chat resets when window is not on top (browser tab loses focus)

**Current Projects Used:**
- Prototype 3 for optis/replacement
- Norwegian content casino reviews
- US Remi things for new pages
- Looker Studio

**Workflow Improvement Needed:**
- Article formatting
- Research keyword cannibalization
- Stop hallucinations

**Project Ideas:**
- Implement a specified self-check rubric for projects before output

**Action Taken:** Added Pre-Output Verification Rubric to PROJECT-INSTRUCTIONS.md

---

## Notes

All feedback collected from team has been incorporated into project documentation.
See PROJECT-INSTRUCTIONS.md for implemented rules and self-check rubric.

---

*Last Updated: December 3, 2024*
