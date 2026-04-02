---
name: Nephron Data Agents Context
description: Overall project overview - Maven multi-module structure with scrapers and sentiment analyzers
type: project
---

**Nephron Data Agents** is a Maven multi-module project for pharmaceutical/biotech data collection and analysis.

**Two Main Components**:

1. **Product Scrapers** (Java/Maven modules)
   - TMO Product Scraper - Thermo Fisher Scientific catalog scraping
   - Uses Playwright for browser automation
   - Outputs CSV files to Cloudflare R2 storage
   - Future: 50+ vendor scrapers planned

2. **Stock Sentiment Analyzers** (Python standalone)
   - Multi-source sentiment analysis for pharma/biotech stocks
   - 16 tickers running nightly at 4am EDT
   - Outputs JSON + PDF reports to R2 storage
   - Located in `stock-sentiment-scraper/` directory

**Repository Structure**:
- Root contains parent POM for Maven modules
- Each scraper is a self-contained Maven module
- Stock sentiment analyzer is Python-based (not Maven integrated)
- All GitHub Actions workflows in `.github/workflows/`
- CLAUDE.md at root contains project instructions

**Data Storage**:
- Cloudflare R2 bucket: `nephron-data`
- Path structure: `nephron-data/{TICKER}/{type}/results_TIMESTAMP.{ext}`
- Examples: `nephron-data/TMO/scraper/results_20260402.csv`, `nephron-data/RVTY/sentiment/report_20260402.pdf`

**Why**: Project aims to provide comprehensive data intelligence on pharmaceutical companies through both product-level scraping and market sentiment analysis.

**How to apply**: When adding new functionality, determine if it fits the scraper pattern (Java/Maven module) or sentiment pattern (Python standalone with GitHub Actions workflow).
