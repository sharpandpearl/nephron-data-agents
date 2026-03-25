# Fisher Scientific Data Scraper Project

## Project Overview

This project validates and scrapes product data from Fisher Scientific's website. It contains two main tools optimized for different use cases:

- **Python Validator** - Fast HTTP-based catalog ID validation (6.1 IDs/sec)
- **Java Playwright Scraper** - Browser-based scraping with detailed product data

## Technology Stack

### Java Module (`java-playwright-scrapper/`)
- **Java Version**: 21 (required)
- **Build Tool**: Maven 3.9.12+
- **Key Dependencies**:
  - Playwright for Java 1.49.0 (browser automation)

### Python Module
- **Python Version**: 3.12+
- **Key Dependencies**:
  - pandas (CSV processing)
  - requests (HTTP validation)

## Project Structure

```
nephron-data-agents/
├── source-data/              # Input CSV files (never modify)
│   └── TMO_Product_list.csv  # Source catalog IDs (8,675 products)
│
├── generated-data/           # All output files (auto-generated, safe to delete)
│   ├── TMO_Product_list_Validated.csv    # Python validator output (all products)
│   ├── TMO_Product_list_Valid_Only.csv   # Filtered valid products only
│   ├── TMO_Valid_CatalogIDs.txt          # Valid IDs (text format)
│   └── playwright_scrape_results.csv     # Java scraper output
│
├── java-playwright-scrapper/ # Java browser automation
│   ├── src/main/java/nephrontools/
│   │   ├── FischerSciScrapper.java    # Main scraper
│   │   └── FischerSciProduct.java     # Data model
│   ├── pom.xml                         # Maven config
│   └── target/                         # Build artifacts (auto-generated)
│
└── validate_fisher_sci_catalog.py     # Python validator
```

## Data Flow

1. **Input**: `source-data/TMO_Product_list.csv` - Single-line CSV with 8,675 catalog IDs
2. **Validation**: Python validator checks which IDs exist on Fisher Scientific → outputs validated CSV
3. **Scraping**: Java scraper extracts detailed product data (name, price, etc.) → outputs CSV
4. **Output**: CSV files in `generated-data/`

## Building & Running

### Java Playwright Scraper

```bash
# Build
cd java-playwright-scrapper
mvn clean compile

# Run (scrapes products based on START_INDEX and END_INDEX)
mvn exec:java -Dexec.mainClass="nephrontools.FischerSciScrapper"
```

**Configuration** (in [FischerSciScrapper.java](java-playwright-scrapper/src/main/java/nephrontools/FischerSciScrapper.java)):
- `CSV_FILE_PATH` - Input CSV location (default: `../generated-data/TMO_Product_list_Valid_Only.csv`)
- `OUTPUT_CSV_FILE` - Output CSV location (default: `../generated-data/playwright_scrape_results.csv`)
- `START_INDEX` - Starting position in CSV (default: 0)
- `END_INDEX` - Ending position in CSV (default: 10, use -1 for all)

### Python Validator

```bash
# Run full validation (~24 minutes for all 8,675 products)
python validate_fisher_sci_catalog.py
```

**Configuration** (in [validate_fisher_sci_catalog.py](validate_fisher_sci_catalog.py)):
- `TEST_MODE` - Set `True` for testing first N products (default: False)
- `TEST_LIMIT` - Number of products in test mode (default: 1000)
- `MAX_WORKERS` - Concurrent HTTP requests (default: 10, max 20 recommended)
- `TIMEOUT` - Request timeout in seconds (default: 5)

## Code Conventions

### Java Conventions
- **Package**: `nephrontools`
- **Naming**:
  - Classes: PascalCase (`FischerSciProduct`, `FischerSciScrapper`)
  - Methods: camelCase (`scrapeFischerSciPricesFromList`, `loadCatalogNumbersFromCSV`)
  - Static fields: camelCase with descriptive names
- **Data Model Fields**: Use `Product_` prefix (e.g., `Product_CatalogNo`, `Product_Name`, `Product_Price`, `Product_ScrapeDate`)
- **Path Handling**: Use relative paths from project root (`../generated-data/`)
- **Output Format**: CSV only (no JSON)

### Python Conventions
- **Style**: Follow standard Python conventions
- **Concurrency**: ThreadPoolExecutor for HTTP requests
- **CSV Handling**: Support both single-line comma-separated and multi-line formats

## Important Implementation Details

### CSV Input Format
The source CSV (`TMO_Product_list.csv`) uses a **single-line, comma-separated format**:
```csv
003002,010075,0102322A,01060A,011045A,011045H,...
```

Both Java and Python code handle:
- Single-line comma-separated format
- Multi-line format (with optional headers)
- Range filtering (START_INDEX to END_INDEX)

### Fisher Scientific URL Patterns

**Search URL** (used for initial lookup):
```
https://www.fishersci.com/us/en/catalog/search/products?keyword={catalog-id}
```

**Valid Product URL** (after redirect):
```
https://www.fishersci.com/shop/products/{product-slug}/{catalog-id}
```

### Validation Logic

**Valid Product Criteria**:
- HTTP 200 response
- Redirects to product page: `/shop/products/{slug}/{catalog-id}`
- URL path ends with the catalog ID

**Invalid Product Detection**:
- "No results found" or "0 results" in content
- Stays on search results page
- URL doesn't end with catalog ID
- HTTP 404/403 errors

### Browser Automation
- **Headless Mode**: Default is `true` (can be toggled in `launchBrowser()`)
- **Wait Strategy**: 3-second timeout after page load for JavaScript execution
- **Rate Limiting**: 2-second delay between requests
- **Price Extraction**: Multiple selectors tried (`[class*='price']`, `[data-testid*='price']`, etc.)
- **Login Detection**: Checks for "Sign In to purchase" text when price not found (sets price to "LOGIN_REQUIRED")

## File Locations

### Never Modify
- `source-data/` - Original input data

### Auto-Generated (Safe to Delete)
- `generated-data/` - All output files
- `java-playwright-scrapper/target/` - Maven build artifacts

### Configuration Files
- `java-playwright-scrapper/pom.xml` - Maven dependencies
- `.vscode/settings.json` - VSCode settings
- `.claude/` - Claude Code configuration

## Performance Benchmarks

| Tool | Speed | Use Case |
|------|-------|----------|
| Python Validator | ~6.1 IDs/sec | Validate which catalog IDs exist |
| Java Playwright | ~0.3-0.5 products/sec | Extract detailed product data |

**Time Estimates**:
- Validate 8,675 products: ~24 minutes (Python)
- Scrape 100 products: ~5-8 minutes (Java)
- Scrape 2,892 valid products: ~2-3 hours (Java)

## Common Workflows

### Workflow 1: Validate Then Scrape (Recommended)
1. Run Python validator to identify valid catalog IDs
2. Validator automatically creates `TMO_Product_list_Valid_Only.csv`
3. Run Java scraper on valid IDs only

### Workflow 2: Test Before Production
1. Set `TEST_MODE = True` in Python validator
2. Set `END_INDEX = 10` in Java scraper
3. Run both tools on small sample

## Troubleshooting

### Maven Build Issues
- Ensure Java 21+ is installed and on PATH
- Run `mvn clean compile` to rebuild from scratch
- Check Maven is 3.9.12+ with `mvn --version`

### Python Issues
- Install dependencies: `pip install pandas requests`
- Check file paths are relative to project root
- Verify source CSV exists at `source-data/TMO_Product_list.csv`

### Scraping Issues
- **Timeout errors**: Increase page wait time (line 201 in FischerSciScrapper.java)
- **No price found**: May require login (check for "LOGIN_REQUIRED" in output)
- **CSV not found**: Verify paths are relative to `java-playwright-scrapper/` directory

## Testing

### Test Java Scraper
```bash
# Edit FischerSciScrapper.java:
# START_INDEX = 0
# END_INDEX = 5  # Test on first 5 products only

cd java-playwright-scrapper
mvn clean compile exec:java -Dexec.mainClass="nephrontools.FischerSciScrapper"
```

### Test Python Validator
```python
# Edit validate_fisher_sci_catalog.py:
# TEST_MODE = True
# TEST_LIMIT = 100

python validate_fisher_sci_catalog.py
```

## Domain Knowledge

### Fisher Scientific
- Online scientific equipment and supplies retailer
- Product catalog uses alphanumeric IDs (e.g., "010075", "0102322A")
- Some products require login to view pricing
- Website uses JavaScript-heavy single-page application

### Product Data Model
```java
FischerSciProduct {
    Product_CatalogNo: String   // Catalog ID (e.g., "010075")
    Product_Name: String        // Product title
    Product_Price: String       // Price or "LOGIN_REQUIRED" or "0.0"
    Product_ScrapeDate: String  // UTC timestamp (ISO 8601 format + Z)
}
```

### CSV Output Format
All tools output CSV files with proper escaping:
- Fields with commas are quoted
- Quotes within fields are escaped as `""`
- Newlines within fields are preserved within quotes

## Security & Best Practices

- **Rate Limiting**: Built-in delays between requests (2 seconds for scraper)
- **Respectful Scraping**: Conservative concurrent request limits (10 workers)
- **Error Handling**: Timeouts and retries implemented
- **No Credentials**: Never store Fisher Scientific login credentials in code
- **User Agent**: Uses realistic browser user agent strings
- **Output Format**: CSV only for consistency and compatibility
