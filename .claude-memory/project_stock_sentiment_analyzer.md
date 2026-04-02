---
name: Stock Sentiment Analyzer
description: Multi-source sentiment analysis system for 16 pharma/biotech stocks with nightly automation
type: project
---

**Stock Sentiment Analyzer** is a Python-based system that aggregates data from 6 sources, performs VADER sentiment analysis, and generates AI-synthesized PDF reports.

**Architecture**:
- **Data Aggregation**: ThreadPoolExecutor parallelizes 6 API sources
- **Sentiment Analysis**: VADER with pharma/biotech domain-specific rules
- **AI Synthesis**: Google Gemini 2.5-flash for executive summaries (4000 token limit)
- **Visualization**: Matplotlib for sentiment trend charts
- **Report Generation**: ReportLab for PDF output with embedded charts

**6 Data Sources**:
1. FDA openFDA 510k clearances
2. SEC Edgar filings (10-K, 10-Q, 8-K)
3. NewsAPI - financial news articles
4. Alpha Vantage News Sentiment - pre-scored articles
5. PubMed E-utilities - medical journal citations
6. ScrapeCreators Reddit API - social media posts
   - Note: Twitter disabled (no keyword search endpoint)

**16 Automated Tickers**:
A (Agilent), BIO (Bio-Rad), DHR (Danaher), EXAS (Exact Sciences), GH (Guardant Health), HOLX (Hologic), ICLR (Icon plc), ILMN (Illumina), IQV (IQVIA), LH (LabCorp), NTRA (Natera), PACB (Pacific Biosciences), QDEL (Quidel), QGEN (Qiagen), RVTY (Revvity), TMO (Thermo Fisher)

**Location**: `stock-sentiment-scraper/` directory
**Output**: `stock-sentiment-scraper/data/output/` (JSON + PDF + PNG chart)
**Analysis Period**: Typically 30 days (configurable via workflow parameter)

**Why**: Built to provide actionable sentiment intelligence on pharma/biotech stocks by synthesizing diverse data sources that traditional financial analysis might miss.

**How to apply**: When adding new tickers or data sources, follow the template pattern in `.github/workflows/sentiment-template.yml` and ensure API rate limits are considered.
