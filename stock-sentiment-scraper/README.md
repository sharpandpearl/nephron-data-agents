# Stock Sentiment Analyzer

**AI-powered sentiment analysis for pharmaceutical and life sciences stocks**

Analyze market sentiment for any biotech/pharma stock by aggregating data from 6+ sources, applying domain-specific sentiment analysis, and generating professional PDF reports with trend visualizations.

---

## What It Does

The Stock Sentiment Analyzer monitors public sentiment about pharmaceutical companies by:

1. **Collecting data** from regulatory agencies, financial news, medical journals, and social media
2. **Analyzing sentiment** using AI and domain-specific rules for pharma/biotech industry
3. **Synthesizing insights** with Google Gemini AI
4. **Generating reports** as PDF documents with charts and JSON data

**Works with any stock ticker**: RVTY, TMO, A, JNJ, PFE, ABBV, etc.

---

## Quick Start

### Installation

```bash
cd stock-sentiment-scraper
pip install -r requirements.txt
```

### Set Up API Keys

Create `.env` file in project root:

```bash
GEMINI_API_KEY=your_key_here            # Required - AI synthesis
NEWS_API_KEY=your_key_here              # Required - News articles
ALPHA_VANTAGE_API_KEY=your_key_here     # Required - Financial news
SCRAPECREATORS_API_KEY=your_key_here    # Required - Reddit data
NCBI_API_KEY=your_key_here              # Optional - PubMed rate limit boost
```

**Get free API keys**:
- [Gemini API](https://aistudio.google.com/apikey)
- [NewsAPI](https://newsapi.org/register)
- [Alpha Vantage](https://www.alphavantage.co/support/#api-key)
- [ScrapeCreators](https://scrapecreators.com/)
- [NCBI E-utilities](https://www.ncbi.nlm.nih.gov/account/settings/) (optional)

### Run Analysis

```bash
python src/main/python/main_pipeline.py <TICKER> "<COMPANY_NAME>" [DAYS]
```

**Examples**:

```bash
# Analyze Revvity over last 30 days (default)
python src/main/python/main_pipeline.py RVTY "Revvity"

# Analyze Thermo Fisher over last 7 days
python src/main/python/main_pipeline.py TMO "Thermo Fisher Scientific" 7

# Analyze Agilent over last 14 days
python src/main/python/main_pipeline.py A "Agilent Technologies" 14
```

### View Results

Reports are saved to `data/output/`:
- `{TICKER}_sentiment_{timestamp}.pdf` - Professional report with charts
- `{TICKER}_sentiment_{timestamp}.json` - Raw data + analysis results
- `{TICKER}_sentiment_{timestamp}_chart.png` - Sentiment trend chart

---

## Data Sources

The analyzer collects information from **6 independent sources**:

### 1. 🏛️ FDA (Regulatory)
**What**: Medical device clearances and approvals
**Why**: FDA approvals are strong positive sentiment signals
**Coverage**: Device-focused companies (Revvity, Agilent, Thermo Fisher)

### 2. 📋 SEC Edgar (Financial Filings)
**What**: 10-K, 10-Q, 8-K corporate filings
**Why**: Required disclosures reveal material events
**Coverage**: All public companies

### 3. 📰 NewsAPI (General News)
**What**: News articles from 80,000+ sources
**Why**: Broad media coverage and breaking news
**Coverage**: Up to 100 articles per query

### 4. 💹 Alpha Vantage (Financial News)
**What**: Financial news with **pre-computed sentiment scores**
**Why**: Fast, reliable sentiment from financial sources
**Coverage**: Up to 50 articles per query with relevance scores

### 5. 🔬 PubMed (Medical Research)
**What**: Scientific publications from NCBI database
**Why**: R&D developments and clinical trial results
**Coverage**: 35+ million medical journal citations

### 6. 💬 Reddit (Social Sentiment)
**What**: Reddit posts and discussions
**Why**: Retail investor sentiment and grassroots opinions
**Coverage**: Real-time social media monitoring

---

## How Sentiment Analysis Works

### Step 1: Data Collection (Parallel)
All 6 sources are queried simultaneously using Python's `ThreadPoolExecutor` for maximum speed (~30-60 seconds for 30 days of data).

### Step 2: VADER Sentiment Analysis
Uses **VADER** (Valence Aware Dictionary and sEntiment Reasoner) enhanced with **domain-specific pharma/biotech rules**:

**Positive Signals** (boost score):
- `fda approval`, `510k clearance`, `breakthrough designation`
- `earnings beat`, `upgrade`, `clinical trial success`
- `patent approval`, `revenue growth`

**Negative Signals** (lower score):
- `warning letter`, `recall`, `black box warning`
- `downgrade`, `lawsuit`, `bankruptcy`
- `earnings miss`, `layoffs`

Each item receives:
- **Label**: positive, negative, or neutral
- **Score**: -1.0 (very negative) to +1.0 (very positive)
- **Confidence**: 0.0 to 1.0

### Step 3: AI Synthesis
Google Gemini AI (gemini-2.5-flash model) analyzes all sentiment data and generates:
- 2-paragraph executive summary (150-200 words)
- Key findings list (top positive/negative events)
- Overall sentiment assessment (positive/negative/mixed)

### Step 4: Visualization
Matplotlib generates a **sentiment trend chart** showing:
- Daily average sentiment over time
- Positive/negative zones (green/red backgrounds)
- Reference zero line
- Summary statistics

### Step 5: Report Generation
Professional PDF report includes:
- Executive summary
- Sentiment breakdown table
- **Sentiment trend chart** (embedded)
- Key findings
- Top 5 positive events
- Top 5 negative events

---

## Sample Output

### Console Output
```
============================================================
Stock Sentiment Analysis - Thermo Fisher Scientific (TMO)
============================================================

Period: 2026-03-21 to 2026-03-28 (7 days)

Phase 1: Aggregating data from multiple sources...
[Alpha Vantage] Found 50 articles
[News] Found 50 articles
[PubMed] Retrieved 16 publication details
[Reddit] Found 21 posts
[SEC] Found 1 filings
[FDA] Found 0 510(k) clearances

Total items collected: 138

Phase 2: Analyzing sentiment...
[Sentiment] Positive: 53, Negative: 40, Neutral: 45

Phase 3: Generating executive summary...
[Gemini] Generated 1593 character summary

JSON report saved to: data/output/TMO_sentiment_2026-03-28_055201.json
Sentiment chart saved to: data/output/TMO_sentiment_2026-03-28_055201_chart.png
PDF report saved to: data/output/TMO_sentiment_2026-03-28_055201.pdf

============================================================
EXECUTIVE SUMMARY
============================================================
Sentiment surrounding Thermo Fisher Scientific (TMO) was largely mixed,
exhibiting a slight positive bias. Of 138 analyzed items, positive mentions
accounted for 38.4% (53 items), neutral for 32.6% (45 items), and negative
for 29.0% (40 items)...
```

### PDF Report Sections
1. **Title Page** - Company, ticker, date range
2. **Executive Summary** - AI-generated analysis
3. **Sentiment Breakdown** - Counts and percentages
4. **Sentiment Trend Chart** - Visual timeline
5. **Key Findings** - Bulleted highlights
6. **Top Positive Events** - 5 most positive items
7. **Top Negative Events** - 5 most negative items

### JSON Output Structure
```json
{
  "company": "Thermo Fisher Scientific",
  "ticker": "TMO",
  "period": {"from": "2026-03-21", "to": "2026-03-28", "days": 7},
  "sentiment_breakdown": {"positive": 53, "negative": 40, "neutral": 45},
  "synthesis": {
    "executive_summary": "...",
    "key_findings": [...],
    "overall_sentiment": "positive"
  },
  "top_positive": [...],
  "top_negative": [...],
  "raw_data": {
    "total_items": 138,
    "items": [...]  // All collected data with full fields
  }
}
```

---

## Performance

**Typical Results** (7-day analysis):

| Ticker | Items | Sources | Runtime | PDF Size |
|--------|-------|---------|---------|----------|
| RVTY   | 31    | 6       | ~45 sec | 98 KB    |
| TMO    | 138   | 6       | ~55 sec | 104 KB   |
| A      | 175   | 6       | ~60 sec | 107 KB   |

**Speed**: Parallel data collection makes it fast
**Scale**: Handles 100+ items easily
**Quality**: Domain-specific rules improve accuracy

---

## Limitations

### API Rate Limits (Free Tier)
- **NewsAPI**: 100 requests/day, 30 days back only
- **Alpha Vantage**: 25 requests/day
- **PubMed**: 3 req/sec (10 with API key)

### Data Availability
- **FDA**: Only device/diagnostic companies (not all pharma)
- **Reddit**: May have low volume for smaller stocks
- **Twitter**: Not available (ScrapeCreators doesn't support keyword search)

### Sentiment Analysis
- VADER is rule-based (not deep learning)
- Medical research often misclassified as negative (disease terminology)
- No sarcasm/irony detection

---

## Key Features

✅ **Generic Design** - Works with any stock ticker
✅ **6 Data Sources** - FDA, SEC, News, Alpha Vantage, PubMed, Reddit
✅ **Parallel Execution** - Fast concurrent API calls
✅ **Domain-Specific** - Pharma/biotech sentiment rules
✅ **AI Synthesis** - Google Gemini executive summaries
✅ **Professional Reports** - PDF with charts + JSON raw data
✅ **Trend Visualization** - Matplotlib sentiment timeline
✅ **Production-Ready** - Clean code, proper error handling

---

## Technical Documentation

For developers and advanced users, see [TECHNICAL.md](TECHNICAL.md) for:
- Detailed API endpoints and parameters
- Code architecture and module structure
- Advanced configuration options
- Performance benchmarks and optimization
- Troubleshooting guide
- Development workflow

---

## Support

**Issues**: Check [TECHNICAL.md](TECHNICAL.md) troubleshooting section
**API Status**: Verify API service availability at provider websites
**Questions**: Review README and technical documentation first

---

## License

Internal tool for Nephron Research. Not licensed for external use.

---

**Version**: 1.0.0
**Python**: 3.12+
**Status**: Production-ready
**Last Updated**: 2026-03-28
