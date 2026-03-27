# Nephron Data Scrapers

**Scalable multi-module web scraping framework for pharmaceutical product data**

## Overview

This project provides automated data collection tools for pharmaceutical and life sciences product catalogs. Built as a Maven multi-module project, it's designed to scale from a single scraper to 50+ independent data collection modules.

### Current Capabilities
- ✅ **TMO (Thermo Fisher Scientific)** - Product catalog scraper with 2,891 validated products
- ✅ **Fast HTTP validation** - Validate thousands of catalog IDs in minutes
- ✅ **Browser automation** - Extract detailed product data with Playwright
- ✅ **Cloud storage** - Automatic upload to Cloudflare R2
- ✅ **GitHub Actions** - Scheduled scraping with parallel execution support

## Quick Start

### Prerequisites
- **Java 21+** ([Download](https://adoptium.net/))
- **Maven 3.9.12+** ([Download](https://maven.apache.org/download.cgi))
- **Python 3.12+** (optional, for validators)

### Build & Run

```bash
# Clone repository
git clone https://github.com/sharpandpearl/nephron-data-agents.git
cd nephron-data-agents

# Build all modules
mvn clean install

# Run TMO scraper (first 25 products)
cd tmo-product-scraper
mvn exec:java -Dexec.mainClass="com.nephron.tmo.FischerSciScrapper"
```

**Output**: Results saved to `tmo-product-scraper/data/output/playwright_scrape_results.csv`

## Project Structure

```
nephron-data-agents/
├── pom.xml                      # Parent POM - manages all modules
├── shared-lib/                  # Common utilities (browser, CSV, dates)
├── tmo-product-scraper/         # Thermo Fisher scraper
│   ├── data/
│   │   ├── source/              # Input catalog IDs
│   │   └── output/              # Generated results
│   └── src/main/
│       ├── java/                # Java scraper
│       └── python/              # Python validator
└── .github/workflows/           # CI/CD automation
```

## Features

### Multi-Module Maven Architecture
- **Shared Library**: Reusable browser automation, CSV handling, and date utilities
- **Independent Modules**: Each scraper is self-contained with its own data and configuration
- **Scalable**: Add new scrapers without modifying existing code

### Data Collection Tools

#### 1. Python Validator (Fast)
Quickly validate which catalog IDs exist on a website using HTTP requests.

```bash
cd tmo-product-scraper
python src/main/python/validate_fisher_sci_catalog.py
```

**Performance**: ~6 IDs/second | 8,675 products validated in 24 minutes

#### 2. Java Playwright Scraper (Detailed)
Extract complete product information using browser automation.

```bash
cd tmo-product-scraper
mvn exec:java -Dexec.mainClass="com.nephron.tmo.FischerSciScrapper"
```

**Performance**: ~0.3-0.5 products/second | Full details: name, price, availability

### GitHub Actions Automation

Automated scraping runs nightly with:
- ✅ Scheduled execution (configurable cron)
- ✅ Manual triggers with custom parameters
- ✅ Parallel execution (4+ concurrent jobs)
- ✅ Automatic upload to Cloudflare R2
- ✅ GitHub artifact backups

## Usage

### Scraping TMO Products

**Configuration** (in `FischerSciScrapper.java`):
```java
static int START_INDEX = 0;      // First product
static int END_INDEX = 25;       // Last product (-1 for all)
```

**Run locally**:
```bash
cd tmo-product-scraper
mvn clean compile
mvn exec:java -Dexec.mainClass="com.nephron.tmo.FischerSciScrapper"
```

**Trigger via GitHub Actions**:
1. Go to repository → Actions tab
2. Select "TMO Product Scraper"
3. Click "Run workflow"
4. Set parameters (start_index, end_index)

### Validating Catalog IDs

**Configuration** (in `validate_fisher_sci_catalog.py`):
```python
INPUT_CSV = 'data/source/TMO_Product_list.csv'
OUTPUT_CSV = 'data/output/TMO_Product_list_Validated.csv'
TEST_MODE = False  # Set True for testing first 1,000 IDs
```

**Run**:
```bash
cd tmo-product-scraper
python src/main/python/validate_fisher_sci_catalog.py
```

## Adding a New Scraper

To add a scraper for another company (e.g., Pfizer):

### 1. Create Module Structure
```bash
mkdir -p pfizer-inventory-scraper/src/main/java/com/nephron/pfizer
mkdir -p pfizer-inventory-scraper/data/{source,output}
```

### 2. Create Module POM
```xml
<!-- pfizer-inventory-scraper/pom.xml -->
<project>
    <parent>
        <groupId>com.nephron</groupId>
        <artifactId>data-scrapers</artifactId>
        <version>1.0.0</version>
    </parent>

    <artifactId>pfizer-inventory-scraper</artifactId>

    <dependencies>
        <dependency>
            <groupId>com.nephron</groupId>
            <artifactId>shared-lib</artifactId>
            <version>${project.version}</version>
        </dependency>
    </dependencies>
</project>
```

### 3. Update Parent POM
Add module to root `pom.xml`:
```xml
<modules>
    <module>shared-lib</module>
    <module>tmo-product-scraper</module>
    <module>pfizer-inventory-scraper</module>  <!-- NEW -->
</modules>
```

### 4. Create Scraper Class
```java
package com.nephron.pfizer;

import com.nephron.shared.browser.BrowserManager;
import com.microsoft.playwright.*;

public class PfizerScraper {
    public static void main(String[] args) {
        Playwright playwright = Playwright.create();
        Browser browser = BrowserManager.launchBrowser(playwright, true);
        // Your scraping logic here
    }
}
```

### 5. Build & Test
```bash
mvn clean install
cd pfizer-inventory-scraper
mvn exec:java -Dexec.mainClass="com.nephron.pfizer.PfizerScraper"
```

See [CLAUDE.md](CLAUDE.md) for complete developer documentation.

## Data Output

### CSV Format
All scrapers output CSV files with standardized columns:

```csv
CatalogNo,ProductName,Price,ScrapeDate
010075,Action Pump Stainless-Steel Piston Pump,398.50,2026-03-26T14:30:00Z
01060A,Thermo Scientific™ Nalgene™ Vacuum Chamber,602.00,2026-03-26T14:30:15Z
```

### Cloud Storage (Cloudflare R2)
GitHub Actions automatically uploads results to:
```
nephron-data/
└── TMO/
    ├── playwright_scrape_results_2026-03-26_143000.csv
    ├── playwright_scrape_results_2026-03-27_143000.csv
    └── ...
```

## Performance

| Tool | Speed | Use Case | Time for 2,891 Products |
|------|-------|----------|------------------------|
| **Python Validator** | 6.1 IDs/sec | Validate which IDs exist | ~8 minutes |
| **Java Scraper (Single)** | 0.3-0.5 products/sec | Full product details | ~2-3 hours |
| **Java Scraper (Parallel)** | 1.2-2.0 products/sec | Full details (4 workers) | ~30-45 minutes |

## Technology Stack

- **Java 21** - Modern LTS with pattern matching and records
- **Maven** - Multi-module build system
- **Playwright for Java 1.49.0** - Browser automation
- **Python 3.12** - Fast HTTP validation scripts
- **GitHub Actions** - CI/CD and scheduled scraping
- **Cloudflare R2** - S3-compatible cloud storage

## Project Metrics

### TMO Product Scraper
- **Total Catalog IDs**: 8,675
- **Valid Products**: 2,892 (33%)
- **Invalid/Discontinued**: 5,782 (67%)
- **Validation Time**: 24 minutes (full dataset)
- **Scraping Time**: ~2 hours (all valid products)

## Development

### Build Commands
```bash
# Build everything
mvn clean install

# Build shared library only
mvn -pl shared-lib clean install

# Build specific module
mvn -pl tmo-product-scraper clean install

# Run tests
mvn test

# Clean all build artifacts
mvn clean
```

### Testing
```bash
# Test with first 10 products
cd tmo-product-scraper
# Edit FischerSciScrapper.java: END_INDEX = 10
mvn exec:java -Dexec.mainClass="com.nephron.tmo.FischerSciScrapper"
```

## Troubleshooting

### Maven Build Fails
```bash
# Verify Java version
java -version  # Should be 21+

# Clean and rebuild
mvn clean install

# Build with debug output
mvn clean install -X
```

### Module Not Found
- Check parent POM lists module in `<modules>` section
- Ensure module POM has correct `<parent>` reference
- Build shared-lib first: `mvn -pl shared-lib install`

### Scraper Can't Find CSV
- Verify files exist in `data/source/`
- Check you're running from correct directory
- Review console output for resolved file paths

## Contributing

When adding new scrapers:
1. ✅ Follow package naming: `com.nephron.[ticker]`
2. ✅ Use shared-lib utilities where possible
3. ✅ Add data files to `[module]/data/source/`
4. ✅ Output to `[module]/data/output/`
5. ✅ Create GitHub Actions workflow

## License

Same as original project.

## Resources

- **Repository**: https://github.com/sharpandpearl/nephron-data-agents
- **Issues**: https://github.com/sharpandpearl/nephron-data-agents/issues
- **Playwright Docs**: https://playwright.dev/java/
- **Maven Multi-Module**: https://maven.apache.org/guides/mini/guide-multiple-modules.html

---

**Maintained by**: Nephron Team
**Last Updated**: 2026-03-26
