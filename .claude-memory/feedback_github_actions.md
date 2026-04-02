---
name: GitHub Actions Workflow Preferences
description: User wants detailed step-by-step logging and reusable templates with proper scheduling
type: feedback
---

Use reusable workflow templates with detailed step-by-step logging that shows each phase of processing (not just final results).

**Why**: User specifically requested "I'd also like to make sure the workflows show each step of the sentiment analysis process (i.e. pulling from reddit, pulling from fda, performing sentiment analysis with VADER etc.)" This helps with debugging and understanding what's happening during automated runs.

**How to apply**:
- For any GitHub Actions workflow, create a reusable template (`.yml` with `workflow_call` trigger)
- Add explicit echo statements for each major phase: "Phase 1: Data Aggregation", "Phase 2: Sentiment Analysis", etc.
- Show progress for each data source individually
- Include summary output at the end with key metrics
- Use workflow_dispatch to enable manual testing

**Additional Pattern**: When scheduling multiple similar jobs, stagger them by 3 minutes to avoid API rate limiting issues (e.g., 8:00, 8:03, 8:06, 8:09...). User approved this approach for the 16 sentiment analyzer workflows.

**Case Sensitivity**: Java package names must be lowercase, but tickers are uppercase for display. Use `tr '[:upper:]' '[:lower:]'` in workflows when building file paths that include package names.
