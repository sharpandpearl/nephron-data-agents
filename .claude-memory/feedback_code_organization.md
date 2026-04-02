---
name: Code Organization and Documentation
description: User prefers split documentation (high-level README + technical TECHNICAL.md)
type: feedback
---

Split documentation into user-friendly README.md and developer-focused TECHNICAL.md instead of single monolithic docs.

**Why**: User requested: "let's break it into two docs. the first a high-level readme that goes through the functionality... the second readme should be in an in-depth overview of the agent (similar to the existing readme)." This followed seeing the initial detailed README which mixed user-facing "what it does" content with technical implementation details.

**How to apply**:
- **README.md** (9-10 KB): What It Does, Quick Start, Data Sources (brief), How It Works (5 steps), Sample Output, Performance, Limitations. Target audience: users/stakeholders.
- **TECHNICAL.md** (25-30 KB): Architecture, API endpoint specs, code structure, algorithms (with pseudocode), performance optimization, troubleshooting, development guide. Target audience: developers.
- Link between them: README mentions "See TECHNICAL.md for developers"

**Code Cleanup Preference**: When asked to clean up code, user expects:
- Remove debug print statements
- Fix bare except clauses to specific exceptions
- Remove unused imports
- Remove test/debug scripts that are no longer needed
- Keep only production-ready code

**File Organization**:
- Source data in `data/source/` (committed)
- Generated output in `data/output/` (gitignored)
- Use `.gitignore` files to exclude generated content (*.json, *.pdf, *.png)
