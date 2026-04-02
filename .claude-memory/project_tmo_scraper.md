---
name: TMO Product Scraper
description: Thermo Fisher Scientific product catalog scraper - first Maven module in the project
type: project
---

**TMO Product Scraper** is a Java/Playwright-based scraper for Thermo Fisher Scientific (Fisher Scientific) product catalog.

**Key Details**:
- **Package**: `com.nephron.tmo`
- **Main Class**: `FischerSciScrapper.java`
- **Input**: CSV list of catalog IDs (8,675 total, 2,891 valid)
- **Output**: Product details with pricing (CSV format)
- **Performance**: ~0.3-0.5 products/second (~2-3 hours for full run)

**Two-Phase Approach**:
1. **Python Validator** - Fast HTTP requests to validate catalog IDs (~6.1 IDs/sec, ~24 min)
2. **Java Scraper** - Playwright browser automation for detailed scraping (slow but thorough)

**Configuration**:
- START_INDEX / END_INDEX for partial runs
- GitHub Actions dynamically sets these via sed during CI/CD
- Data files in `tmo-product-scraper/data/source/` and `data/output/`

**Important Lesson**: Java package must be lowercase (`com.nephron.tmo`) but ticker can be uppercase (TMO) for display. GitHub Actions workflow uses `tr '[:upper:]' '[:lower:]'` to convert.

**Why**: First implementation of the multi-module scraper pattern, serves as template for future vendor scrapers.

**How to apply**: Use TMO scraper as reference when building new product scrapers. Follow the same Maven module structure and GitHub Actions workflow pattern.
