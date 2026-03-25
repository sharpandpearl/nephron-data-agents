# How to Use MCP Servers - Optional Guide

## Overview

This project includes MCP (Model Context Protocol) server configuration as an **optional feature**. The primary tools for this project are:

1. **Python Validator** - HTTP-based catalog validation (recommended)
2. **Java Playwright Scraper** - Browser-based product scraping

MCP servers are configured but **not required** for normal operation.

## What You Have

You have **2 MCP servers** configured in `.claude/.mcp.json`:

### 1. Playwright MCP - Browser Automation
**Location:** `.claude/.mcp.json`

```json
{
  "command": "npx",
  "args": ["@playwright/mcp@latest"]
}
```

**Purpose:** Allows Claude to control Playwright through the MCP protocol for natural language scraping.

### 2. Context7 MCP - Context/Memory Management
```json
{
  "command": "npx",
  "args": ["-y", "@upstash/context7-mcp"]
}
```

**Purpose:** Enables Claude to remember data across sessions using Upstash Redis.

## How MCP Servers Work

MCP (Model Context Protocol) servers are **tools that AI assistants like Claude can use**.

Think of them like browser extensions, but for AI:
- **Browser** has extensions (ad blockers, password managers, etc.)
- **AI assistants** have MCP servers (Playwright, Context7, file systems, etc.)

When configured, Claude can:
1. Use **Playwright MCP** to control browsers and scrape websites
2. Use **Context7 MCP** to remember things across sessions

## Main Project Workflow (Recommended)

For normal usage, **you don't need to use MCP servers**. Instead, use the direct tools:

### Option 1: Python Validator (Fast)
```bash
python validate_fisher_sci_catalog.py
```

**Status:** ✅ Fully functional
- **Input:** `source-data/TMO_Product_list.csv`
- **Output:** `generated-data/TMO_Product_list_Validated.csv`
- **Speed:** ~6.1 IDs/second
- **Purpose:** Validate which catalog IDs exist

### Option 2: Java Playwright Scraper (Detailed)
```bash
cd java-playwright-scrapper
mvn clean compile
mvn exec:java -Dexec.mainClass="nephrontools.FischerSciScrapper"
```

**Status:** ✅ Fully functional
- **Input:** `source-data/TMO_Product_list.csv`
- **Output:** `generated-data/playwright_scrape_results.csv`
- **Features:** CSV reading, configurable range, product details
- **Configuration:** START_INDEX, END_INDEX

**Uses:** Playwright for Java (direct library, not MCP)

## MCP-Based Scraping (Optional Advanced Feature)

If you want to use Claude to scrape via natural language commands through MCP:

### Prerequisites
- Node.js installed
- Claude Desktop or MCP-enabled client

### Example Usage

Instead of running the Java scraper directly, you could ask Claude:

```
Use Playwright MCP to:
1. Navigate to Fisher Scientific product page for catalog #010075
2. Extract the product name and price
3. Save to a CSV file
```

Claude would then use the Playwright MCP server to perform these actions.

### When to Use MCP vs Direct Tools

**Use Direct Tools (Recommended):**
- ✅ Validating large batches of catalog IDs (Python validator)
- ✅ Scraping many products systematically (Java scraper)
- ✅ Automated, repeatable workflows
- ✅ Production use

**Use MCP (Optional):**
- ✅ One-off scraping tasks
- ✅ Exploratory data collection
- ✅ Natural language interactions with Claude
- ✅ Learning/experimentation

## Configuration Files

### `.claude/.mcp.json`
Main MCP server configuration file. Claude Code automatically loads this.

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

## Troubleshooting MCP

### MCP Server Won't Start
```bash
# Verify Node.js is installed
node --version

# Test Playwright MCP manually
npx @playwright/mcp@latest

# Check Claude Code settings
cat .claude/.mcp.json
```

### Node.js Not Found
```bash
# Add Node.js to PATH (Windows Git Bash)
export PATH="/c/Program Files/nodejs:$PATH"
```

## Resources

- [Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Context7 MCP](https://github.com/upstash/context7-mcp)

## Summary

- **MCP servers are optional** for this project
- Use **Python validator** and **Java scraper** for normal workflows
- Use **MCP** only if you want natural language scraping with Claude
- All MCP configuration is in `.claude/.mcp.json`
