# Nephron Data Scrapers - Multi-Module Project

## Project Overview

This is a **Maven multi-module project** for scraping pharmaceutical product data from various vendor websites. The project is designed to scale to 50+ individual scrapers, each targeting a specific company or data source.

### Current Scrapers
- **TMO Product Scraper** - Thermo Fisher Scientific (Fisher Scientific) product catalog scraper

### Tools Available
- **Java Playwright Scrapers** - Browser-based scraping with detailed product data
- **Python Validators** - Fast HTTP-based catalog ID validation

## Technology Stack

### Multi-Module Maven Structure
- **Build Tool**: Maven 3.9.12+
- **Java Version**: 21 (required for all modules)
- **Parent POM**: Manages common dependencies and build configuration
- **Module Packaging**: Individual JAR artifacts per scraper

### Java Dependencies
- **Playwright for Java 1.49.0** - Browser automation (managed by parent POM)

### Python Tools
- **Python Version**: 3.12+
- **Dependencies**: pandas, requests

## Project Structure

```
nephron-data-agents/
├── pom.xml                          # Parent POM (manages all modules)
│
├── shared-lib/                      # Shared utilities for all scrapers
│   ├── pom.xml
│   └── src/main/java/com/nephron/shared/
│       ├── browser/BrowserManager.java      # Playwright setup
│       ├── csv/CsvHandler.java              # CSV utilities
│       ├── model/BaseProduct.java           # Base product class
│       └── util/DateUtils.java              # Date formatting
│
├── tmo-product-scraper/             # TMO (Thermo Fisher) scraper module
│   ├── pom.xml                      # Module POM (depends on shared-lib)
│   ├── data/
│   │   ├── source/                  # Input CSV files
│   │   │   ├── TMO_Product_list.csv
│   │   │   └── TMO_Product_list_Valid_Only.csv
│   │   └── output/                  # Generated files (auto-created)
│   │       └── playwright_scrape_results.csv
│   ├── src/
│   │   └── main/
│   │       ├── java/com/nephron/tmo/
│   │       │   ├── FischerSciScrapper.java  # Main scraper
│   │       │   └── FischerSciProduct.java   # Data model
│   │       └── python/
│   │           └── validate_fisher_sci_catalog.py
│   └── target/                      # Maven build artifacts
│
├── .github/workflows/
│   ├── scraper-template.yml         # Reusable workflow for all scrapers
│   └── tmo-scraper-workflow.yml     # TMO scraper schedule
│
└── [future scrapers]/               # Add new scraper modules here
    └── pfe-inventory-scraper/
    └── abbvie-pricing-scraper/
```

## Maven Multi-Module Architecture

### Parent POM (`pom.xml`)
- Defines common dependencies (Playwright version)
- Sets Java 21 as compilation target
- Lists all child modules
- Manages plugin versions

### Shared Library (`shared-lib/`)
- **Purpose**: Common code used across all scrapers
- **Package**: `com.nephron.shared`
- **Contents**:
  - `BrowserManager` - Playwright browser setup
  - `CsvHandler` - CSV field escaping
  - `DateUtils` - UTC timestamp generation
  - `BaseProduct` - Base class for product models

### Individual Scraper Modules (e.g., `tmo-product-scraper/`)
- **Purpose**: Self-contained scraper for a specific company/dataset
- **Package**: `com.nephron.[ticker]` (e.g., `com.nephron.tmo`)
- **Dependencies**: Parent POM + shared-lib
- **Data Directory**: Module-specific `data/source/` and `data/output/`
- **Python Scripts**: Optional validators in `src/main/python/`

## Building & Running

### Build Everything (All Modules)

```bash
# From project root
mvn clean install
```

This builds:
1. `shared-lib` (common utilities)
2. `tmo-product-scraper` (TMO scraper)
3. Future modules...

### Build Individual Module

```bash
# Build shared library only
mvn -pl shared-lib clean install

# Build TMO scraper only (requires shared-lib to be built first)
mvn -pl tmo-product-scraper clean install
```

### Run TMO Scraper

```bash
# From project root
cd tmo-product-scraper
mvn exec:java -Dexec.mainClass="com.nephron.tmo.FischerSciScrapper"

# Or from project root (without cd)
mvn -pl tmo-product-scraper exec:java -Dexec.mainClass="com.nephron.tmo.FischerSciScrapper"
```

**Configuration** (in [FischerSciScrapper.java](tmo-product-scraper/src/main/java/com/nephron/tmo/FischerSciScrapper.java)):
- `CSV_FILE_PATH` - Input CSV (default: `data/source/TMO_Product_list_Valid_Only.csv`)
- `OUTPUT_CSV_FILE` - Output CSV (default: `data/output/playwright_scrape_results.csv`)
- `START_INDEX` - Starting position (default: 0)
- `END_INDEX` - Ending position (default: 25, use -1 for all)

### Run Python Validator

```bash
# From TMO scraper module directory
cd tmo-product-scraper
python src/main/python/validate_fisher_sci_catalog.py
```

**Configuration** (in validator script):
- `INPUT_CSV` - Input catalog IDs (default: `data/source/TMO_Product_list.csv`)
- `OUTPUT_CSV` - Validation results (default: `data/output/TMO_Product_list_Validated.csv`)
- `TEST_MODE` - Enable test mode (default: False)
- `MAX_WORKERS` - Concurrent requests (default: 10)

## Code Conventions

### Package Naming
- **Root Package**: `com.nephron`
- **Shared Code**: `com.nephron.shared.[component]`
- **Scraper Modules**: `com.nephron.[ticker].[component]`

Examples:
- `com.nephron.shared.browser.BrowserManager`
- `com.nephron.tmo.FischerSciScrapper`
- `com.nephron.pfe.InventoryScraper` (future)

### Java Naming Conventions
- **Classes**: PascalCase (`FischerSciProduct`, `BrowserManager`)
- **Methods**: camelCase (`scrapeFischerSciPricesFromList`, `launchBrowser`)
- **Constants**: UPPER_SNAKE_CASE (`START_INDEX`, `OUTPUT_CSV_FILE`)
- **Packages**: lowercase (`com.nephron.tmo`)

### Data Model Conventions
- Use descriptive field names: `catalogNumber`, `productName`, `price`, `scrapeDate`
- Extend `BaseProduct` for common fields (when applicable)
- CSV output format: `CatalogNo,ProductName,Price,ScrapeDate`

### File Organization
- **Source Data**: `[module]/data/source/` (committed to git)
- **Generated Data**: `[module]/data/output/` (gitignored)
- **Java Code**: `[module]/src/main/java/com/nephron/[ticker]/`
- **Python Scripts**: `[module]/src/main/python/`

## Adding a New Scraper

To add a new scraper module (e.g., Pfizer inventory scraper):

### 1. Create Module Directory

```bash
mkdir -p pfizer-inventory-scraper/src/main/java/com/nephron/pfizer
mkdir -p pfizer-inventory-scraper/data/source
mkdir -p pfizer-inventory-scraper/data/output
```

### 2. Create Module POM

**`pfizer-inventory-scraper/pom.xml`:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project>
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.nephron</groupId>
        <artifactId>data-scrapers</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>pfizer-inventory-scraper</artifactId>
    <name>Pfizer Inventory Scraper</name>

    <dependencies>
        <dependency>
            <groupId>com.nephron</groupId>
            <artifactId>shared-lib</artifactId>
            <version>${project.version}</version>
        </dependency>
        <dependency>
            <groupId>com.microsoft.playwright</groupId>
            <artifactId>playwright</artifactId>
        </dependency>
    </dependencies>
</project>
```

### 3. Update Parent POM

Add to `pom.xml` (root):
```xml
<modules>
    <module>shared-lib</module>
    <module>tmo-product-scraper</module>
    <module>pfizer-inventory-scraper</module>  <!-- ADD THIS -->
</modules>
```

### 4. Create Scraper Class

**`pfizer-inventory-scraper/src/main/java/com/nephron/pfizer/PfizerScraper.java`:**
```java
package com.nephron.pfizer;

import com.nephron.shared.browser.BrowserManager;
import com.nephron.shared.util.DateUtils;
import com.microsoft.playwright.*;

public class PfizerScraper {
    public static void main(String[] args) {
        Playwright playwright = Playwright.create();
        Browser browser = BrowserManager.launchBrowser(playwright, true);
        // ... scraping logic
    }
}
```

### 5. Create GitHub Workflow

**`.github/workflows/pfizer-scraper-workflow.yml`:**
```yaml
name: Pfizer Inventory Scraper

on:
  workflow_dispatch:
  schedule:
    - cron: '0 3 * * *'

jobs:
  scrape:
    uses: ./.github/workflows/scraper-template.yml
    with:
      scraper_name: 'Pfizer Inventory Scraper'
      company_ticker: 'pfizer'
      module_path: 'pfizer-inventory-scraper'
      java_main_class: 'com.nephron.pfizer.PfizerScraper'
    secrets:
      R2_ACCESS_KEY_ID: ${{ secrets.NEPHRON_R2_ACCESS_KEY_ID }}
      R2_SECRET_ACCESS_KEY: ${{ secrets.NEPHRON_R2_SECRET_ACCESS_KEY }}
```

### 6. Build and Test

```bash
mvn clean install
cd pfizer-inventory-scraper
mvn exec:java -Dexec.mainClass="com.nephron.pfizer.PfizerScraper"
```

## GitHub Actions Integration

### Reusable Workflow Template

All scrapers use `.github/workflows/scraper-template.yml`:
- Builds shared-lib first
- Compiles and runs specified scraper module
- Uploads results to Cloudflare R2
- Backs up to GitHub Actions artifacts

### Scraper-Specific Workflows

Each scraper has its own workflow file (e.g., `tmo-scraper-workflow.yml`):
- Calls the reusable template
- Specifies module path and main class
- Sets schedule (cron)
- Provides company ticker for R2 organization

## Data Flow

1. **Input**: Source CSV in `[module]/data/source/`
2. **Processing**: Scraper reads input, navigates websites, extracts data
3. **Output**: Results saved to `[module]/data/output/`
4. **Upload**: GitHub Actions uploads to R2: `nephron-data/[TICKER]/results_TIMESTAMP.csv`

## File Locations

### Never Modify
- `[module]/data/source/` - Source data files (committed)

### Auto-Generated (Safe to Delete)
- `[module]/data/output/` - Scraper output files
- `[module]/target/` - Maven build artifacts
- Legacy: `source-data/`, `generated-data/` (deprecated, will be removed)

### Configuration Files
- `pom.xml` (root) - Parent POM
- `[module]/pom.xml` - Module POM
- `.github/workflows/*.yml` - CI/CD workflows

## Performance Benchmarks

| Scraper | Speed | Products | Time Estimate |
|---------|-------|----------|---------------|
| **TMO Validator** (Python) | ~6.1 IDs/sec | 8,675 | ~24 minutes |
| **TMO Scraper** (Java) | ~0.3-0.5/sec | 2,891 valid | ~2-3 hours |

## Common Workflows

### Test New Scraper Locally
```bash
cd [scraper-module]
mvn clean compile
mvn exec:java -Dexec.mainClass="com.nephron.[ticker].MainClass"
```

### Test GitHub Actions Workflow
- Commit workflow file
- Push to `main` branch
- Go to Actions tab → Run workflow manually

### Update Shared Library
```bash
# Make changes to shared-lib
mvn -pl shared-lib clean install

# Rebuild dependent scrapers
mvn -pl tmo-product-scraper clean install
```

## Troubleshooting

### Maven Build Issues
- Ensure Java 21 is installed: `java -version`
- Clean install from root: `mvn clean install`
- Build shared-lib first if module fails

### Module Not Found
- Check parent POM lists module in `<modules>` section
- Verify module POM has correct `<parent>` reference

### Path Issues
- Scraper code detects if running from module dir or root
- Data files: `data/source/` and `data/output/` relative to module
- Run from module directory for simplest paths

## Security & Best Practices

- **Rate Limiting**: 2-second delays between requests in scrapers
- **Respectful Scraping**: Conservative concurrent requests
- **No Credentials**: Never store vendor login credentials in code
- **R2 Secrets**: Stored as GitHub repository secrets
- **CSV Only**: All scrapers output CSV format for consistency

---

**Last Updated**: 2026-03-26 (Multi-module refactoring)
