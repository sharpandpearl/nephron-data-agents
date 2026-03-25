# Fisher Scientific Product Scraper

Web scraper and catalog validator for extracting product data from Fisher Scientific's website.

## Project Overview

This repository contains tools for validating and scraping Fisher Scientific product catalogs:

1. **Python Validator** - Fast HTTP-based catalog ID validation (~6 IDs/sec)
2. **Java Playwright Scraper** - Browser-based scraping with detailed product data
3. **CSV Data Processing** - Input/output handling for catalog numbers and results

## Project Structure

```
nephron-data-agents/
├── source-data/                        # Input data files (never modify)
│   └── TMO_Product_list.csv           # Source catalog IDs (8,675 products)
│
├── generated-data/                     # All output files (auto-generated)
│   ├── TMO_Product_list_Validated.csv # Full validation results
│   ├── TMO_Product_list_Valid_Only.csv # Valid products only
│   ├── TMO_Valid_CatalogIDs.txt       # Valid IDs (text file)
│   └── playwright_scrape_results.csv  # Java Playwright scrape results
│
├── java-playwright-scrapper/           # Java browser automation
│   ├── src/main/java/nephrontools/
│   │   ├── FischerSciScrapper.java    # Main scraper
│   │   └── FischerSciProduct.java     # Data model
│   ├── pom.xml                         # Maven config
│   └── target/                         # Build artifacts
│
└── validate_fisher_sci_catalog.py     # Fast HTTP-based validator
```

## Quick Start

### Option 1: Validate Catalog IDs (Fastest - Recommended)

**Purpose:** Quickly validate which catalog IDs exist on Fisher Scientific's website.

**Features:**
- ✅ Validates 8,675 products in ~24 minutes
- ✅ HTTP-based (no browser needed)
- ✅ Concurrent requests (10 workers)
- ✅ Conservative validation (checks URL patterns)
- ✅ Test mode for trying samples

**Usage:**

```bash
# Validate all catalog IDs (production mode)
python validate_fisher_sci_catalog.py

# Test mode (first 1,000 products)
# Edit validate_fisher_sci_catalog.py: TEST_MODE = True
python validate_fisher_sci_catalog.py
```

**Configuration:**

```python
# In validate_fisher_sci_catalog.py
INPUT_CSV = 'source-data/TMO_Product_list.csv'
OUTPUT_CSV = 'generated-data/TMO_Product_list_Validated.csv'
MAX_WORKERS = 10        # Concurrent requests
TIMEOUT = 5             # Timeout per request (seconds)
TEST_MODE = False       # Set True for testing
TEST_LIMIT = 1000       # Test mode limit
```

**Validation Results (from 8,675 products):**
- ✅ Valid: 2,892 products (33%)
- ❌ Invalid: 5,782 products (66%)
- ⚠️ Errors: 1 timeout (0%)
- ⚡ Throughput: 6.1 IDs/second

**Output Files:**
- `generated-data/TMO_Product_list_Validated.csv` - All results with status
- `generated-data/TMO_Product_list_Valid_Only.csv` - Valid products only
- `generated-data/TMO_Valid_CatalogIDs.txt` - Valid IDs (one per line)

### Option 2: Scrape Product Details (Slower, More Data)

**Purpose:** Extract detailed product information (name, price, etc.) using a browser.

**Features:**
- ✅ Extracts product name, price, availability
- ✅ Detects login requirements
- ✅ Configurable range (for testing)
- ✅ CSV output format

**Usage:**

```bash
cd java-playwright-scrapper
mvn clean compile
mvn exec:java -Dexec.mainClass="nephrontools.FischerSciScrapper"
```

**Configuration:**

```java
// In FischerSciScrapper.java
static String CSV_FILE_PATH = "../generated-data/TMO_Product_list_Valid_Only.csv";
static String OUTPUT_CSV_FILE = "../generated-data/playwright_scrape_results.csv";
static int START_INDEX = 0;      // Start at first product
static int END_INDEX = 10;       // End at 10th product (-1 for all)
```

**Output Files:**
- `generated-data/playwright_scrape_results.csv` - Full product data and prices

## Requirements

### Python Validator
- Python 3.12+
- Dependencies: `pandas`, `requests`

```bash
pip install pandas requests
```

### Java Playwright Scraper
- Java 21+
- Maven 3.9.12+

## Validation Logic

The validator uses a **conservative validation approach** to ensure accuracy:

### Valid Product Criteria:
1. ✅ HTTP 200 response
2. ✅ Redirects to product page: `/shop/products/{slug}/{catalog-id}`
3. ✅ URL path ends with the catalog ID

### Invalid Product Detection:
- ❌ "No results found" or "0 results" in content
- ❌ Stays on search results page
- ❌ URL doesn't end with catalog ID
- ❌ HTTP 404 or 403 errors

### Example URLs:

**Valid:**
```
https://www.fishersci.com/shop/products/stainless-steel-piston-pump/010075
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^ ^^^^^^
                                       product-slug              catalog-id
```

**Invalid:**
```
https://www.fishersci.com/us/en/catalog/search/products?keyword=011890102
(Stays on search page - product not available)
```

## Features Comparison

| Tool | Speed | Data Depth | Browser | Use Case |
|------|-------|------------|---------|----------|
| **Python Validator** | ⚡ 6.1/s | Basic (exists?) | ❌ No | Validate catalog IDs |
| **Java Playwright** | 🐌 ~0.2/s | Detailed | ✅ Yes | Product details + prices |

## Recommended Workflows

### Workflow 1: Validate & Filter (Recommended)

```bash
# Step 1: Validate all catalog IDs (24 minutes)
python validate_fisher_sci_catalog.py

# Step 2: Review results
cat generated-data/TMO_Product_list_Validated.csv

# Step 3: Extract valid IDs only (already done by validator)
# File: generated-data/TMO_Product_list_Valid_Only.csv

# Result: 2,892 valid catalog IDs ready for scraping
```

### Workflow 2: Scrape Product Details

```bash
# Use the 2,892 valid catalog IDs as input
cd java-playwright-scrapper

# Configure range in FischerSciScrapper.java
# START_INDEX = 0
# END_INDEX = 100  # Or -1 for all 2,892 valid products

mvn clean compile exec:java -Dexec.mainClass="nephrontools.FischerSciScrapper"
```

### Workflow 3: Test Before Production

```bash
# Test validation on first 100 products
# Edit validate_fisher_sci_catalog.py: TEST_MODE = True, TEST_LIMIT = 100
python validate_fisher_sci_catalog.py

# Test scraping on first 10 products
# FischerSciScrapper.java already defaults to END_INDEX = 10
cd java-playwright-scrapper
mvn exec:java -Dexec.mainClass="nephrontools.FischerSciScrapper"
```

## Performance Statistics

### Full Validation Run (8,675 products)
```
Total Processed:    8,675
Valid Products:     2,892 (33%)
Invalid Products:   5,782 (66%)
Errors/Timeouts:    1 (0%)
Total Time:         23m 51s
Average Time/ID:    0.16s
Throughput:         6.1 IDs/second
```

### Estimated Time Comparisons

| Task | Products | Python Validator | Java Playwright |
|------|----------|------------------|-----------------|
| Validate 8,675 | Full dataset | 24 min | N/A |
| Scrape 2,892 | Valid only | N/A | ~4 hours |
| Test 100 | Sample | 16 sec | ~8 min |

## Best Practices

### Rate Limiting
- ✅ Validator: Uses concurrent requests with timeout
- ✅ Scraper: 2-second delay between requests
- ✅ Respects website policies

### Error Handling
- ✅ Timeout handling (5s for validator, 3s page wait for scraper)
- ✅ Connection error recovery
- ✅ Invalid product detection
- ✅ Progress tracking with ETA

### Data Quality
- ✅ Conservative validation (only mark valid if URL confirms)
- ✅ Checks actual product page URLs
- ✅ Detects "LOGIN_REQUIRED" for restricted products
- ✅ Filters out search results pages

## Troubleshooting

### Python Validator Issues

**FileNotFoundError:**
```bash
# Ensure source data exists
ls -la source-data/TMO_Product_list.csv

# Check file path in script
grep INPUT_CSV validate_fisher_sci_catalog.py
```

**Slow validation:**
```python
# Increase workers (max 20 recommended)
MAX_WORKERS = 15

# Decrease timeout (min 3s recommended)
TIMEOUT = 3
```

### Java Scraper Issues

**Maven not found:**
```bash
mvn --version
# If not found, ensure Maven is installed and on PATH
```

**Compilation errors:**
```bash
cd java-playwright-scrapper
mvn clean install
```

**CSV file not found:**
```bash
# Verify source data location
ls -la generated-data/TMO_Product_list_Valid_Only.csv
```

### General Issues

**Output files not created:**
```bash
# Ensure output directory exists
mkdir -p generated-data

# Check write permissions
ls -ld generated-data/
```

## File Formats

### Input: TMO_Product_list.csv
```csv
003002,010075,0102322A,01060A,011045A,011045H,...
```
- Format: Single-line, comma-separated
- Total: 8,675 catalog IDs
- Location: `source-data/TMO_Product_list.csv`

### Output: Validation Results (CSV)
```csv
ProductID,Status,ResponseTime_s
003002,Invalid (Not Found),1.23
010075,Valid,0.87
011890102,Invalid (Not Found),1.45
```

### Output: Scrape Results (CSV)
```csv
CatalogNo,ProductName,Price,ScrapeDate
01060A,Thermo Scientific™ Nalgene™ Vacuum Chamber,602.00,2026-03-25T19:33:35Z
010075,Action Pump Stainless-Steel Piston Pump,398.50,2026-03-25T19:33:52Z
```

### Output: Valid IDs Only (TXT)
```
010075
0102322A
01060A
011045H
...
```

## Technology Stack

### Java Module
- **Java Version**: 21
- **Build Tool**: Maven 3.9.12
- **Dependencies**:
  - Playwright for Java 1.49.0 (browser automation)

### Python Module
- **Python Version**: 3.12+
- **Dependencies**:
  - pandas (CSV processing)
  - requests (HTTP validation)

## License

Same as original project.

## Contributors

- Original Author: andri
- Modernization & Updates: Claude (Anthropic)

## Resources

- [Fisher Scientific](https://www.fishersci.com/)
- [Python Requests](https://requests.readthedocs.io/)
- [Playwright](https://playwright.dev/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## Recommended Approach

**For most users:**

1. **Start with validation** (24 minutes):
   ```bash
   python validate_fisher_sci_catalog.py
   ```

2. **Review valid products** (2,892 found):
   ```bash
   head generated-data/TMO_Valid_CatalogIDs.txt
   ```

3. **Scrape details only for valid products**:
   ```bash
   cd java-playwright-scrapper
   # Configure range in FischerSciScrapper.java
   mvn exec:java -Dexec.mainClass="nephrontools.FischerSciScrapper"
   ```

This approach saves time by validating first, then scraping only valid products! 🚀
