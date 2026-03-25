# Fisher Scientific Scraper - Complete Project

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
Web scraper and catalog validator for extracting product data from Fisher Scientific's website.

## 🎯 Project Overview

This repository contains multiple implementations for scraping and validating Fisher Scientific product catalogs:

1. **Python Validator** - Fast HTTP-based catalog ID validation (Recommended for validation)
2. **Playwright Scraper** - Browser-based scraping with detailed product data
3. **Java/Selenium** - Legacy production scraper (modernized)
4. **MCP Integration** - Model Context Protocol integration
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
Web scraper for extracting product data from Fisher Scientific's website.

## 🎯 Project Overview

This repository contains multiple implementations of a Fisher Scientific product scraper:

1. **Java/Selenium** - Production-ready, modernized scraper
2. **MCP Integration** - Modern approach using Model Context Protocol
3. **Documentation** - Comprehensive guides and examples
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

## 📁 Project Structure

```
nephron-scrapper/
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
├── source-data/                        # Input data files
│   └── TMO_Product_list.csv           # Source catalog IDs (8,675 products)
│
├── generated-data/                     # All output files
│   ├── TMO_Product_list_Validated.csv # Full validation results
│   ├── TMO_Product_list_Valid_Only.csv # Valid products only
│   ├── TMO_Valid_CatalogIDs.txt       # Valid IDs (text file)
│   ├── fisher_sci_results.json        # Playwright scrape results
│   └── fisher_sci_validation.csv      # Playwright validation output
│
├── playwright-mcp-scraper/             # Browser-based scraper
│   ├── demo_mcp_usage.js              # Main Playwright scraper
│   ├── MCP_USAGE_GUIDE.md             # MCP integration guide
│   ├── QUICK_START.md                  # Quick reference
│   ├── package.json                    # Node.js dependencies
│   └── node_modules/                   # Installed packages
│
├── NephronSelenium/                    # Java/Maven scraper (legacy)
│   ├── src/main/java/tmo/
│   │   ├── FischerSciScrapper.java    # Main Java scraper
│   │   └── FischerSciProduct.java      # Data model
│   └── pom.xml                         # Maven dependencies (updated)
│
├── .claude/                            # Claude Code configuration
│   ├── .mcp.json                       # MCP server configuration
│   └── settings.local.json             # Local settings
│
├── validate_fisher_sci_catalog.py      # Fast HTTP-based validator ⭐
├── HOW_TO_USE_MCP_SERVERS.md          # Complete MCP guide
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
├── NephronSelenium/                    # Main Java scraper
│   ├── src/main/java/tmo/
│   │   ├── FischerSciScrapper.java    # Main scraper (modernized)
│   │   └── FischerSciProduct.java      # Data model
│   ├── pom.xml                         # Maven dependencies (updated)
│   └── .mcp.json                       # MCP server configuration
│
├── playwright-mcp-scraper/             # MCP-based scraper examples
│   ├── MCP_USAGE_GUIDE.md             # How to use MCP servers
│   ├── QUICK_START.md                  # Quick reference
<<<<<<< Updated upstream
│   └── demo_mcp_usage.js              # Node.js demo
│
├── HOW_TO_USE_MCP_SERVERS.md          # Complete MCP guide
├── MIGRATION_SUMMARY.md                # What was changed
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
│   ├── demo_mcp_usage.js              # Node.js demo
│   └── fisher_sci_scraper_simple.py   # Python wrapper
│
├── HOW_TO_USE_MCP_SERVERS.md          # Complete MCP guide
├── MIGRATION_SUMMARY.md                # What was changed
>>>>>>> Stashed changes
└── README.md                           # This file
```

## 🚀 Quick Start

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
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
python3 validate_fisher_sci_catalog.py

# Test mode (first 1,000 products)
# Edit validate_fisher_sci_catalog.py: TEST_MODE = True
python3 validate_fisher_sci_catalog.py
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
- ✅ JSON and CSV output
- ⚠️ Slower (~15s per product with timeout)

**Usage:**

```bash
cd playwright-mcp-scraper
node demo_mcp_usage.js
```

**Configuration:**

```javascript
// In demo_mcp_usage.js
const START_INDEX = 0;      // Start at first product
const END_INDEX = 10;       // End at 10th product (-1 for all)
const TIMEOUT_MS = 15000;   // Page load timeout
```

**Output Files:**
- `generated-data/fisher_sci_results.json` - Full product data
- `generated-data/fisher_sci_validation.csv` - Validation status

### Option 3: Java/Selenium (Legacy)

**Purpose:** Production-ready scraper using Java and Selenium.
=======
### Option 1: Java/Selenium (Recommended for Production)
>>>>>>> Stashed changes
=======
### Option 1: Java/Selenium (Recommended for Production)
>>>>>>> Stashed changes
=======
### Option 1: Java/Selenium (Recommended for Production)
>>>>>>> Stashed changes

```bash
cd NephronSelenium
mvn clean compile
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
**Status:** ✅ Fully working, modernized (Selenium 4.27.0)

## 📊 Validation Logic

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
- ❌ Not available / Not web orderable

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

## 🔧 Requirements

### Python Validator (Recommended)
- Python 3.12+
- Dependencies: `pandas`, `requests`

```bash
pip install pandas requests
```

### Playwright Scraper
- Node.js 24.13.1+
- Playwright installed

```bash
cd playwright-mcp-scraper
npm install
```

### Java Scraper (Optional)
- Java 21+
- Maven 3.9.12+

## ✨ Features Comparison

| Tool | Speed | Data Depth | Browser | Use Case |
|------|-------|------------|---------|----------|
| **Python Validator** | ⚡ 6.1/s | Basic (exists?) | ❌ No | Validate catalog IDs |
| **Playwright Scraper** | 🐌 ~0.07/s | Detailed | ✅ Yes | Product details |
| **Java/Selenium** | 🐌 ~0.2/s | Detailed | ✅ Yes | Legacy production |
| **MCP Integration** | 🐌 ~0.3/s | Detailed | ✅ Yes | Claude integration |

## 📚 Documentation

- **[validate_fisher_sci_catalog.py](validate_fisher_sci_catalog.py)** - Main validator script
- **[demo_mcp_usage.js](playwright-mcp-scraper/demo_mcp_usage.js)** - Playwright scraper
- **[HOW_TO_USE_MCP_SERVERS.md](HOW_TO_USE_MCP_SERVERS.md)** - MCP integration guide
- **[MCP_USAGE_GUIDE.md](playwright-mcp-scraper/MCP_USAGE_GUIDE.md)** - Detailed MCP guide
- **[QUICK_START.md](playwright-mcp-scraper/QUICK_START.md)** - Quick reference

## 🎓 Workflows

### Workflow 1: Validate & Filter (Recommended)

```bash
# Step 1: Validate all catalog IDs (24 minutes)
python3 validate_fisher_sci_catalog.py

# Step 2: Review results
cat generated-data/TMO_Product_list_Validated.csv

# Step 3: Extract valid IDs only
grep ",Valid," generated-data/TMO_Product_list_Validated.csv | cut -d',' -f1 > generated-data/TMO_Valid_CatalogIDs.txt

# Result: 2,892 valid catalog IDs ready for scraping
```

### Workflow 2: Scrape Product Details

```bash
# Use the 2,892 valid catalog IDs as input
cd playwright-mcp-scraper

# Configure range in demo_mcp_usage.js
# START_INDEX = 0
# END_INDEX = 100  # Or -1 for all 2,892 valid products

node demo_mcp_usage.js
```

### Workflow 3: Test Before Production

```bash
# Test validation on first 100 products
# Edit validate_fisher_sci_catalog.py: TEST_MODE = True, TEST_LIMIT = 100
python3 validate_fisher_sci_catalog.py

# Test scraping on first 10 products
# demo_mcp_usage.js already defaults to END_INDEX = 10
cd playwright-mcp-scraper
node demo_mcp_usage.js
```

## 📈 Performance Statistics

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

| Task | Products | Python Validator | Playwright | Java/Selenium |
|------|----------|------------------|------------|---------------|
| Validate 8,675 | Full dataset | 24 min | 36 hours | 12 hours |
| Scrape 2,892 | Valid only | N/A | 12 hours | 4 hours |
| Test 100 | Sample | 16 sec | 25 min | 8 min |

## 🔐 Best Practices

### Rate Limiting
- ✅ Validator: Uses concurrent requests with timeout
- ✅ Scraper: 2-second delay between requests
- ✅ Respects website policies

### Error Handling
- ✅ Timeout handling (5s for validator, 15s for scraper)
- ✅ Connection error recovery
- ✅ Invalid product detection
- ✅ Progress tracking with ETA

### Data Quality
- ✅ Conservative validation (only mark valid if URL confirms)
- ✅ Checks actual product page URLs
- ✅ Detects "not available" and "not web orderable" products
- ✅ Filters out search results pages

## 🐛 Troubleshooting

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

### Playwright Scraper Issues

**Module not found:**
```bash
cd playwright-mcp-scraper
npm install
```

**Timeout errors:**
```javascript
// Increase timeout in demo_mcp_usage.js
const TIMEOUT_MS = 30000;  // 30 seconds
```

**CSV file not found:**
```bash
# Verify source data location
ls -la source-data/TMO_Product_list.csv
```

### General Issues

**Output files not created:**
```bash
# Ensure output directory exists
mkdir -p generated-data

# Check write permissions
ls -ld generated-data/
```

## 📝 File Formats

### Input: TMO_Product_list.csv
```csv
003002,010075,0102322A,01060A,011045A,011045H,...
```
- Format: Single-line, comma-separated
- Total: 8,675 catalog IDs
- Location: `source-data/TMO_Product_list.csv`

### Output: Validation Results
```csv
ProductID,Status,ResponseTime_s
003002,Invalid (Not Found),1.23
010075,Valid,0.87
011890102,Invalid (Not Found),1.45
```

### Output: Valid IDs Only
```
010075
0102322A
01060A
011045H
...
```

## 🔌 MCP Integration

MCP servers configured in `.claude/.mcp.json`:

### Playwright MCP
- **Purpose:** Browser automation for Claude
- **Command:** `npx @playwright/mcp@latest`
- **Use case:** Ask Claude to scrape products

### Context7 MCP
- **Purpose:** Context/memory management
- **Command:** `npx -y @upstash/context7-mcp`
- **Use case:** Store scraping history

=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
**Status:** ✅ Fully working, modernized, ready to use

**Features:**
- Automated ChromeDriver management via WebDriverManager
- Latest Selenium 4.27.0 and Gson 2.11.0
- Scrapes product names, prices, catalog numbers
- Exports to JSON
- API integration ready

### Option 2: MCP-Based Scraping (Modern Approach)

If using Claude Desktop or MCP-enabled client:

```
Ask Claude: "Use Playwright MCP to scrape Fisher Scientific product #10000475"
```

**Status:** ✅ Configured, ready for MCP clients

## 📚 Documentation

- **[HOW_TO_USE_MCP_SERVERS.md](HOW_TO_USE_MCP_SERVERS.md)** - Complete guide to using MCP servers
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** - Details of modernization changes
- **[MCP_USAGE_GUIDE.md](playwright-mcp-scraper/MCP_USAGE_GUIDE.md)** - MCP integration patterns
- **[QUICK_START.md](playwright-mcp-scraper/QUICK_START.md)** - Quick reference guide

## 🔧 Requirements

### Java Scraper
- Java 21+ (OpenJDK 21.0.4 installed ✅)
- Maven 3.9.12+ (installed ✅)

### MCP Scraper (Optional)
- Node.js 24.13.1+ (installed ✅)
- Python 3.12+ (installed ✅)
- Claude Desktop or MCP-enabled client

## ✨ Features

### Java/Selenium Scraper
- ✅ Automatic ChromeDriver management
- ✅ Headless browser support
- ✅ Product name extraction
- ✅ Price extraction with login detection
- ✅ JSON export
- ✅ API integration (configurable)
- ✅ Error handling and recovery
- ✅ Catalog range iteration

### MCP Integration
- ✅ Playwright MCP server configured
- ✅ Context7 MCP server configured
- ✅ Natural language scraping via Claude
- ✅ Session memory and context
- ✅ Demo scripts provided

## 📊 Recent Updates

### ✅ Modernization (Completed)
- Updated Selenium: 4.1.2 → 4.27.0
- Updated Gson: 2.8.9 → 2.11.0
- Added WebDriverManager 5.9.2
- Removed hardcoded ChromeDriver paths
- Improved error handling
- Modern Chrome options

### ✅ MCP Setup (Completed)
- Installed Node.js v24.13.1
- Configured Playwright MCP server
- Configured Context7 MCP server
- Created demo scripts
- Comprehensive documentation

## 🎓 How It Works

### Java/Selenium Flow

```
1. Configure catalog range (e.g., 10000-10010)
2. WebDriverManager downloads ChromeDriver
3. For each catalog number:
   - Navigate to Fisher Scientific search page
   - Extract product name from h1 tag
   - Extract price (or detect login requirement)
   - Store in FischerSciProduct object
4. Export all products to JSON
5. Optional: POST to API endpoint
```

### MCP Flow (via Claude)

```
1. You ask Claude to scrape a product
2. Claude uses Playwright MCP server
3. Server launches browser and navigates
4. Data extracted and returned to Claude
5. Claude presents results to you
6. Optional: Store in Context7 for memory
```

## 🔌 MCP Servers

Configured in `NephronSelenium/.mcp.json`:

### Playwright MCP
**Purpose:** Browser automation
**Command:** `npx @playwright/mcp@latest`
**Use for:** Scraping, navigation, screenshots

### Context7 MCP
**Purpose:** Context/memory management
**Command:** `npx -y @upstash/context7-mcp`
**Use for:** Storing scraping history, tracking changes

## 📝 Configuration

### Customize Catalog Range

**Java version:**
```java
// In FischerSciScrapper.java
static int fsProductID_start = 10000;
static int fsProductID_end = 10010;
```

### Update API Endpoint

```java
// In FischerSciScrapper.java
public static String postScrapedData(String jsonString) throws IOException {
    URL url = new URL("http://your-api-endpoint.com/api/store-data");
    // ...
}
```

## 🐛 Troubleshooting

### Java Issues

**Maven not found:**
```bash
export PATH="/c/Tools/Maven/apache-maven-3.9.12/bin:$PATH"
```

**Compilation errors:**
```bash
cd NephronSelenium
mvn clean install
```

### MCP Issues

**Node.js not found:**
```bash
export PATH="/c/Program Files/nodejs:$PATH"
```

**MCP server won't start:**
- Verify `npx @playwright/mcp@latest` works
- Check `.mcp.json` configuration
- Ensure Claude Desktop is MCP-enabled

## 📈 Performance

| Implementation | Speed | Setup Time | Maintenance |
|----------------|-------|------------|-------------|
| Java/Selenium | ~5s/product | 2 min | Low |
| MCP (via Claude) | ~3s/product | 0 min | None |

## 🔐 Security Notes

- Scraper respects robots.txt
- Includes delays between requests
- Detects and handles login requirements
- No credentials stored in code
- API endpoint configurable

## 🛠️ Development

### Build Java Scraper

```bash
cd NephronSelenium
mvn clean compile package
```

### Run Tests

```bash
# Test MCP setup
cd playwright-mcp-scraper
python3 test_mcp.py

# Test Java scraper
cd NephronSelenium
mvn test
```

<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
## 📄 License

Same as original project.

<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
## 👤 Contributors

- Original Author: andri
- Modernization & Validation: Claude (Anthropic)
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
## 👤 Author

Original: andri
Modernization: Claude (Anthropic)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

## 🔗 Resources

- [Fisher Scientific](https://www.fishersci.com/)
<<<<<<< Updated upstream
<<<<<<< Updated upstream
<<<<<<< Updated upstream
- [Python Requests](https://requests.readthedocs.io/)
- [Playwright](https://playwright.dev/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

---

## 🎯 Recommended Workflow

**For most users, we recommend:**

1. **Start with validation** (24 minutes):
   ```bash
   python3 validate_fisher_sci_catalog.py
   ```

2. **Review valid products** (2,892 found):
   ```bash
   head generated-data/TMO_Valid_CatalogIDs.txt
   ```

3. **Scrape details only for valid products** (optional):
   ```bash
   cd playwright-mcp-scraper
   # Configure range in demo_mcp_usage.js
   node demo_mcp_usage.js
   ```

This approach saves time by validating first, then scraping only valid products! 🚀
=======
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
- [Selenium Documentation](https://www.selenium.dev/)
- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [WebDriverManager](https://github.com/bonigarcia/webdrivermanager)

---

**Ready to scrape?** Start with the Java scraper for immediate results!

```bash
cd NephronSelenium
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```
<<<<<<< Updated upstream
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes
