# How to Use Your MCP Servers - Complete Guide

## What You Have Now

<<<<<<< Updated upstream
You have **2 MCP servers** configured in `.claude/.mcp.json`:

### 1. Playwright MCP - Browser Automation via MCP Protocol
**Location:** `.claude/.mcp.json` (repository root)

=======
You have **2 MCP servers** configured in your `.mcp.json` file:

### 1. Playwright MCP - Browser Automation
**Location:** `NephronSelenium/.mcp.json`
>>>>>>> Stashed changes
```json
{
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

<<<<<<< Updated upstream
**Purpose:** Allows Claude to control Playwright through the MCP protocol for natural language scraping.

=======
>>>>>>> Stashed changes
### 2. Context7 MCP - Context/Memory Management
```json
{
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp"]
}
```

<<<<<<< Updated upstream
**Purpose:** Enables Claude to remember data across sessions using Upstash Redis.

## How MCP Servers Work

MCP (Model Context Protocol) servers are **tools that AI assistants like Claude can use**.

Think of them like browser extensions, but for AI:
- **Browser** has extensions (ad blockers, password managers, etc.)
- **AI assistants** have MCP servers (Playwright, Context7, file systems, etc.)

When configured, Claude can:
1. Use **Playwright MCP** to control browsers and scrape websites
2. Use **Context7 MCP** to remember things across sessions

## Important: Understanding Playwright Usage in This Repository

### Three DIFFERENT Ways Playwright is Used:

#### 1. **NephronSelenium** - Java Scraper (Does NOT use Playwright!)

**Technology:** Selenium 4.27.0 with ChromeDriver
**NOT Playwright!**

```java
// This uses Selenium, NOT Playwright
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;

WebDriver driver = new ChromeDriver();
driver.get("https://www.fishersci.com/...");
```

**Key Points:**
- ✅ Uses Selenium WebDriver API
- ✅ Modernized to Selenium 4.27.0
- ✅ WebDriverManager for automatic ChromeDriver setup
- ❌ Does NOT use Playwright library
- ❌ Does NOT use MCP

**Status:** ✅ Fully working, production-ready
**Location:** `NephronSelenium/`
**Best for:** Production Java-based scraping with API integration

---

#### 2. **playwright-mcp-scraper** - Node.js Scraper (Uses Playwright Directly)

**Technology:** Playwright Node.js library
**Direct Playwright usage, NOT via MCP**

```javascript
// This uses Playwright library directly
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
```

**Key Points:**
- ✅ Uses Playwright JavaScript/Node.js API
- ✅ Direct library usage (npm package)
- ❌ Does NOT use MCP protocol
- ❌ Not for Claude to control

**Status:** ✅ Implemented with CSV reading and validation
**Location:** `playwright-mcp-scraper/demo_mcp_usage.js`
**Best for:** Browser-based JavaScript scraping with Playwright features

---

#### 3. **MCP Playwright Server** - For Claude (Playwright via MCP Protocol)

**Technology:** Playwright MCP Server (`@playwright/mcp`)
**Provides Playwright to Claude via MCP**

```
User → Claude → MCP Protocol → Playwright Server → Playwright → Browser
```

**Key Points:**
- ✅ Playwright controlled via MCP protocol
- ✅ Allows Claude to use Playwright through natural language
- ✅ No manual coding required
- ✅ Interactive, conversational scraping

**Status:** ✅ Configured in `.claude/.mcp.json`
**Location:** MCP configuration file
**Best for:** Asking Claude to scrape in natural language

---

### Visual Comparison:

| Project | Technology | Uses Playwright? | Uses MCP? | Best For |
|---------|-----------|------------------|-----------|----------|
| **NephronSelenium** | Selenium 4.27.0 | ❌ No (uses Selenium) | ❌ No | Production Java scraping |
| **playwright-mcp-scraper** | Playwright library | ✅ Yes (direct API) | ❌ No | Node.js browser automation |
| **MCP Playwright Server** | Playwright MCP | ✅ Yes (via MCP) | ✅ Yes | Claude natural language |

## Current Project Status

### ✅ What's Completed

#### 1. **Python Validator** - Fast HTTP-based validation
```bash
python validate_fisher_sci_catalog.py
```

**Status:** ✅ Completed full validation
- **Validated:** 8,675 catalog IDs
- **Valid:** 2,892 products (33%)
- **Invalid:** 5,782 products (66%)
- **Time:** ~24 minutes
- **Output:** `generated-data/TMO_Product_list_Validated.csv`

**Uses:** HTTP requests (no browser needed)
**Best for:** Quick validation of catalog IDs

---

#### 2. **Playwright Scraper** - Browser-based Node.js scraper
```bash
cd playwright-mcp-scraper
node demo_mcp_usage.js
```

**Status:** ✅ Implemented and tested
- **Input:** `source-data/TMO_Product_list.csv`
- **Output:** `generated-data/fisher_sci_results.json`
- **Features:** CSV reading, configurable range, validation CSV
- **Configuration:** START_INDEX, END_INDEX, TIMEOUT_MS

**Uses:** Playwright Node.js library (direct)
**Best for:** Detailed product scraping with JavaScript

---

#### 3. **Java/Selenium Scraper** - Production scraper
```bash
cd NephronSelenium
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```

**Status:** ✅ Fully modernized
- **Selenium:** 4.27.0 (latest)
- **Gson:** 2.11.0
- **WebDriverManager:** 5.9.2
- **Fixed:** URI deprecation warnings
- **API Integration:** Ready for production

**Uses:** Selenium WebDriver (NOT Playwright)
**Best for:** Production scraping, API integration

---

#### 4. **Folder Structure** - Organized and clean
```
nephron-scrapper/
├── source-data/           # Input CSV files
├── generated-data/        # All output files
├── .claude/               # MCP and settings
├── playwright-mcp-scraper/# Playwright scripts
└── NephronSelenium/       # Java/Selenium project
```

**Status:** ✅ Reorganized and refactored
**Benefits:** Clear separation, no duplicates

## How to Use MCP Servers

### Option 1: Let Claude Use Them (Easiest!)

**In Claude Desktop or MCP-enabled client:**

**Example 1: Scrape a product**
```
You: Use Playwright MCP to scrape Fisher Scientific product #010075

Claude: I'll use the Playwright MCP server to scrape that.
        [Launches browser via MCP]
        [Navigates to product page]
        [Extracts data]

        Product: Action Pump Stainless-Steel Piston Pump
        Price: LOGIN_REQUIRED
        URL: https://www.fishersci.com/shop/products/...
```

**Example 2: Store results**
```
You: Store this scraping data in Context7 for future reference

Claude: I'll save this to Context7 MCP.
        [Stores data in Upstash Redis]

        Saved! I'll remember these products in future sessions.
```

**No code needed!** Just ask in natural language.

---

### Option 2: Use Your Existing Scrapers (Recommended for Production)

Choose based on your needs:

#### For Quick Validation (Fastest):
```bash
python validate_fisher_sci_catalog.py
```
- 6.1 products/second
- HTTP-based (no browser)
- Validates all 8,675 in ~24 minutes

#### For Detailed Product Data (Browser-based):
```bash
cd playwright-mcp-scraper
node demo_mcp_usage.js
```
- Uses Playwright directly
- Extracts names, prices, availability
- Configurable ranges

#### For Production (Most Reliable):
```bash
cd NephronSelenium
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```
- Selenium 4.27.0
- API integration ready
- Proven and stable

---

### Option 3: Command Line MCP Testing

**Launch Playwright MCP server:**
```bash
npx @playwright/mcp@latest
```

**Launch Context7 MCP server:**
```bash
npx -y @upstash/context7-mcp
```

These commands start the MCP servers manually for testing.
=======
## How MCP Servers Work

Think of MCP servers like **tools that I (Claude) can use** to help you:

- **Playwright MCP** = Browser automation tool
- **Context7 MCP** = Memory/storage tool

When you're talking to me in an MCP-enabled environment (like Claude Desktop), I can:
1. Use Playwright MCP to control a browser and scrape websites
2. Use Context7 MCP to remember things across sessions

## Using MCP Servers in Your Scraper

### Option 1: Let Claude Use Them Directly (Easiest!)

If you're using Claude Desktop or another MCP-enabled client:

**You:** "Use Playwright MCP to scrape Fisher Scientific product #10000475"

**Claude (me):** I'll use the Playwright MCP server to:
1. Launch a browser
2. Navigate to Fisher Scientific
3. Extract the product data
4. Return the results to you

**No code needed!** Just ask in natural language.

### Option 2: Use via Command Line

**Playwright MCP:**
```bash
# This launches the server (already installed globally via npx)
npx @playwright/mcp@latest
```

**Context7 MCP:**
```bash
# This launches the Context7 server
npx -y @upstash/context7-mcp
```

### Option 3: Use Your Existing Scrapers

You already have **working scrapers** that don't need MCP:

#### Java/Selenium Scraper (Modernized ✅)
```bash
cd c:\GitHub_Repos\nephron-scrapper\NephronSelenium
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```

**Status:** Fully working, modernized, ready to use

#### Python Scripts
Location: `playwright-mcp-scraper/`
- `fisher_sci_scraper_simple.py`
- `demo_mcp_usage.js`

**Status:** Created but need npm packages installed
>>>>>>> Stashed changes

## What I Set Up For You

### 1. Modernized Your Java Scraper ✅

**Files Updated:**
<<<<<<< Updated upstream
- `NephronSelenium/pom.xml` - Selenium 4.27.0, Gson 2.11.0, WebDriverManager 5.9.2
- `NephronSelenium/src/main/java/tmo/FischerSciScrapper.java` - Fixed URL deprecation
- Removed hardcoded ChromeDriver paths
- Added WebDriverManager for automatic driver management

**Result:** Production-ready Java scraper using Selenium (NOT Playwright)

---

### 2. Created Playwright Scraper ✅

**Files Created:**
- `playwright-mcp-scraper/demo_mcp_usage.js` - Main scraper
- `playwright-mcp-scraper/package.json` - Node.js dependencies
- CSV reading with configurable ranges
- Output to `generated-data/` folder

**Result:** Node.js scraper using Playwright library directly

---

### 3. Created Python Validator ✅

**File:** `validate_fisher_sci_catalog.py`
- Fast HTTP-based validation
- Conservative URL pattern matching
- Concurrent requests (10 workers)
- Test mode for sampling

**Result:** Validated all 8,675 products, found 2,892 valid

---

### 4. Organized Folder Structure ✅

**Created:**
- `source-data/` - Input CSV files
- `generated-data/` - All output files
- `.claude/` - MCP configuration (moved from NephronSelenium/)
- Removed duplicate `.mcp.json`

**Result:** Clean, organized repository

---

### 5. Created Documentation ✅

**Files:**
- `playwright-mcp-scraper/MCP_USAGE_GUIDE.md` - Detailed MCP guide
- `playwright-mcp-scraper/QUICK_START.md` - Quick reference
- `HOW_TO_USE_MCP_SERVERS.md` - This file
- Updated `README.md` - Comprehensive overview

## Recommended Workflow

### Workflow 1: Validate Then Scrape (Recommended)

```bash
# Step 1: Validate all catalog IDs (24 minutes)
python validate_fisher_sci_catalog.py

# Step 2: Review valid products (2,892 found)
cat generated-data/TMO_Valid_CatalogIDs.txt

# Step 3: Scrape details for valid products only
cd playwright-mcp-scraper
# Edit demo_mcp_usage.js to use valid IDs
node demo_mcp_usage.js
```

**Benefits:** Only scrape valid products, saves time

---

### Workflow 2: Production Java Scraping

```bash
# Edit catalog range in FischerSciScrapper.java
=======
- [NephronSelenium/pom.xml](NephronSelenium/pom.xml) - Updated to Selenium 4.27.0, Gson 2.11.0
- [NephronSelenium/src/main/java/tmo/FischerSciScrapper.java](NephronSelenium/src/main/java/tmo/FischerSciScrapper.java) - Modernized with WebDriverManager

**How to use:**
```bash
>>>>>>> Stashed changes
cd NephronSelenium
mvn clean compile
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```

<<<<<<< Updated upstream
**Benefits:** Reliable, API integration, production-ready

---

### Workflow 3: Interactive with Claude

```
You: Use Playwright MCP to check if product 010075 is available

Claude: [Uses MCP Playwright Server]
        Yes, product 010075 is available!
        Name: Action Pump Stainless-Steel Piston Pump

You: Store this in Context7

Claude: [Uses MCP Context7]
        Stored! I'll remember this product.
```

**Benefits:** No coding, interactive, great for debugging

## Performance Comparison

| Method | Speed | Technology | Best For |
|--------|-------|-----------|----------|
| **Python Validator** | ⚡ 6.1/s | HTTP requests | Bulk validation |
| **Playwright Scraper** | 🐌 ~0.07/s | Browser (Playwright) | Detailed data |
| **Java/Selenium** | 🐌 ~0.2/s | Browser (Selenium) | Production |
| **MCP via Claude** | 🐌 ~0.3/s | Browser (Playwright MCP) | Interactive |

## Files Overview

| File/Directory | Purpose | Technology | Status |
|----------------|---------|-----------|--------|
| `NephronSelenium/` | Java scraper | Selenium 4.27.0 | ✅ Working |
| `playwright-mcp-scraper/` | Node.js scraper | Playwright (direct) | ✅ Working |
| `validate_fisher_sci_catalog.py` | Fast validator | HTTP/Requests | ✅ Completed |
| `.claude/.mcp.json` | MCP configuration | MCP protocol | ✅ Configured |
| `source-data/` | Input CSV files | Data | ✅ Organized |
| `generated-data/` | Output files | Data | ✅ Organized |

## What Are MCP Servers Really?

MCP servers are **standardized tools for AI assistants**:

```
Traditional Approach:
You → Write Code → Run Code → Get Results

MCP Approach:
You → Ask Claude → Claude uses MCP servers → Get Results
```

**Examples:**
- **Playwright MCP** = Browser automation tool for AI
- **Context7 MCP** = Memory/storage tool for AI
- **File System MCP** = File operations tool for AI

Your `.mcp.json` tells Claude which servers are available.

## Troubleshooting

### Issue: "Which scraper should I use?"

**Answer:**
- **Validation only** → `validate_fisher_sci_catalog.py`
- **Detailed scraping** → `demo_mcp_usage.js` (Playwright)
- **Production** → NephronSelenium (Selenium)
- **Interactive** → Ask Claude (MCP)

### Issue: "Does NephronSelenium use Playwright?"

**Answer:** No! It uses Selenium 4.27.0, NOT Playwright.
- Selenium and Playwright are different browser automation libraries
- NephronSelenium = Selenium WebDriver
- playwright-mcp-scraper = Playwright library

### Issue: "How do I enable MCP?"

**Answer:**
1. Use Claude Desktop (or compatible MCP client)
2. Configure it to load `.claude/.mcp.json`
3. Servers auto-install via `npx` when needed

### Issue: "MCP vs Direct Usage?"

**Answer:**
- **MCP** = Let Claude control Playwright through natural language
- **Direct** = You write code using Playwright API
- Both use Playwright, different interfaces

## Next Steps

### To Use Scraper Right Now:

**Option A: Validate catalog IDs**
```bash
python validate_fisher_sci_catalog.py
```

**Option B: Scrape with Playwright**
```bash
cd playwright-mcp-scraper
node demo_mcp_usage.js
```

**Option C: Java production scraper**
=======
### 2. Created MCP Configuration ✅

**File:** [NephronSelenium/.mcp.json](NephronSelenium/.mcp.json)

This tells MCP-enabled clients (like Claude Desktop) which servers to load.

### 3. Created Documentation ✅

**Files Created:**
- `playwright-mcp-scraper/MCP_USAGE_GUIDE.md` - Full MCP documentation
- `playwright-mcp-scraper/QUICK_START.md` - Quick reference
- `playwright-mcp-scraper/demo_mcp_usage.js` - Node.js demo script
- `playwright-mcp-scraper/fisher_sci_scraper_simple.py` - Python wrapper
- `MIGRATION_SUMMARY.md` - What was changed

## How MCP Servers Help Your Scraping

### Without MCP (Traditional):
```
You → Write Code → Run Code → Get Results
```

### With MCP (Modern):
```
You → Ask Claude → Claude uses MCP servers → Get Results
```

## Practical Examples

### Example 1: Scrape Using Claude + Playwright MCP

**In Claude Desktop (with MCP enabled):**

```
You: Use Playwright MCP to scrape Fisher Scientific product #10000475
     and show me the product name and price.

Claude: I'll use the Playwright MCP server to scrape that for you.
        [Uses Playwright MCP server]

        Product: Stoelting™ Halstead Mosquito Forceps
        Price: Login Required
```

### Example 2: Remember Scraping History with Context7

**In Claude Desktop:**

```
You: Store this scraping data in Context7 so we remember it next time.

Claude: I'll save this to Context7 MCP.
        [Uses Context7 to store data]

        Saved! I'll remember this product data in future sessions.
```

### Example 3: Use Your Java Scraper (No MCP Needed)

```bash
cd c:\GitHub_Repos\nephron-scrapper\NephronSelenium
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```

This uses your modernized Java/Selenium code directly.

## Summary Table

| Method | Complexity | Setup Time | Best For |
|--------|------------|------------|----------|
| **Java/Selenium** | Medium | Ready now | Production scraping |
| **Claude + MCP** | Low | Need Claude Desktop | Quick one-off scrapes |
| **Node.js/Playwright** | Medium | Need npm install | Custom automation |
| **Python MCP** | High | Most setup needed | Learning MCP protocol |

## Recommended Approach

For **production scraping right now:**
>>>>>>> Stashed changes
```bash
cd NephronSelenium
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```

<<<<<<< Updated upstream
### To Experiment with MCP:

1. Install Claude Desktop
2. Point it to `.claude/.mcp.json`
3. Ask me to use Playwright MCP or Context7

### To Learn More:

- Read `playwright-mcp-scraper/MCP_USAGE_GUIDE.md`
- Read `playwright-mcp-scraper/QUICK_START.md`
- Check `README.md` for overview

## Summary

You now have a **complete scraping toolkit**:

### Three Browser Automation Approaches:
1. **Java/Selenium** - Production scraping (Selenium 4.27.0)
2. **Node.js/Playwright** - Browser scraping (Playwright library)
3. **MCP Playwright** - Natural language scraping (via Claude)

### One Fast Validator:
- **Python HTTP** - Quick validation (no browser needed)

### Organized Structure:
- **source-data/** - Inputs
- **generated-data/** - Outputs
- **.claude/** - Configuration
- Clean separation, no duplicates

### Current Results:
- ✅ 8,675 catalog IDs validated
- ✅ 2,892 valid products identified (33%)
- ✅ All tools working and tested

**Choose the right tool for your task and start scraping!** 🚀
=======
For **experimenting with MCP:**
- Use Claude Desktop with MCP enabled
- Ask me to use Playwright MCP
- I'll control the browser for you

For **custom automation:**
- Install Node.js packages
- Use the demo scripts I created

## What Are MCP Servers Really?

MCP (Model Context Protocol) servers are:
- **Tools that AI assistants like me can use**
- **Standardized way to give AI capabilities**
- **Like plugins for AI assistants**

Think of it like:
- **VSCode** has extensions
- **Chrome** has extensions
- **AI assistants** have MCP servers

Your MCP servers give me the ability to:
- **Playwright MCP** → Control browsers, scrape websites
- **Context7 MCP** → Remember things across sessions

## Files Overview

| File/Directory | Purpose | Status |
|----------------|---------|--------|
| `NephronSelenium/` | Java/Selenium scraper | ✅ Working |
| `NephronSelenium/.mcp.json` | MCP configuration | ✅ Configured |
| `playwright-mcp-scraper/` | Python/Node demos | ⚠️ Needs npm install |
| `MIGRATION_SUMMARY.md` | What was changed | ✅ Documentation |

## Next Steps

### If you want to use your scraper NOW:
```bash
cd NephronSelenium
mvn exec:java -Dexec.mainClass="tmo.FischerSciScrapper"
```

### If you want to experiment with MCP:
1. Install Claude Desktop
2. Configure it to use your `.mcp.json`
3. Ask me to scrape using Playwright MCP

### If you want to understand MCP better:
Read the documentation files I created in `playwright-mcp-scraper/`

## Questions?

**Q: Do I need MCP to use my scraper?**
A: No! Your Java scraper works independently.

**Q: What's the advantage of MCP?**
A: I (Claude) can use the tools directly through natural language.

**Q: How do I enable MCP?**
A: Use Claude Desktop and point it to your `.mcp.json` file.

**Q: Which scraper should I use?**
A: For production → Java/Selenium. For experimentation → MCP.

## The Bottom Line

You now have:
1. ✅ A working, modernized Java/Selenium scraper
2. ✅ MCP configuration for future use
3. ✅ Demo scripts showing how MCP works
4. ✅ Comprehensive documentation

**Use what works best for you!**
>>>>>>> Stashed changes
