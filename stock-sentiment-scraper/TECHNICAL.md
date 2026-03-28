# Stock Sentiment Analyzer - Technical Documentation

Comprehensive technical documentation for developers, data scientists, and advanced users.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Data Source APIs](#data-source-apis)
3. [Code Structure](#code-structure)
4. [Sentiment Analysis Engine](#sentiment-analysis-engine)
5. [AI Synthesis](#ai-synthesis)
6. [Report Generation](#report-generation)
7. [Configuration](#configuration)
8. [Performance & Optimization](#performance--optimization)
9. [Troubleshooting](#troubleshooting)
10. [Development Guide](#development-guide)

---

## Architecture Overview

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Main Pipeline                            │
│  (main_pipeline.py - Orchestration)                         │
└──────────────┬──────────────────────────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐        ┌──────────────┐
│  Load   │        │   Calculate  │
│ API Keys│        │  Date Range  │
└────┬────┘        └──────┬───────┘
     │                    │
     └─────────┬──────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│   Phase 1: Parallel Data Aggregation     │
│   (ThreadPoolExecutor - 6 workers)       │
├──────────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌────────┐ ┌─────┐    │
│  │ FDA │ │ SEC │ │  News  │ │Alpha│    │
│  └─────┘ └─────┘ └────────┘ └─────┘    │
│  ┌────────┐ ┌────────┐                  │
│  │PubMed  │ │ Reddit │                  │
│  └────────┘ └────────┘                  │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Phase 2: Sentiment Analysis (VADER)     │
│  - Domain-specific rules                 │
│  - Score calculation                     │
│  - Confidence estimation                 │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Phase 3: AI Synthesis (Gemini)          │
│  - Executive summary generation          │
│  - Key findings extraction               │
│  - Overall sentiment determination       │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Phase 4: Visualization (Matplotlib)     │
│  - Sentiment trend chart                 │
│  - Daily average calculation             │
│  - PNG export                            │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Phase 5: Report Generation              │
│  - JSON output (raw data)                │
│  - PDF report (ReportLab + embedded PNG) │
└──────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Language** | Python 3.12+ | Core implementation |
| **Concurrency** | ThreadPoolExecutor | Parallel API calls |
| **HTTP** | requests | API communication |
| **Sentiment** | vaderSentiment | Rule-based analysis |
| **AI** | google-genai | Executive summary |
| **Visualization** | matplotlib | Trend charts |
| **PDF** | reportlab | Report generation |
| **Data** | pandas (optional) | Data manipulation |
| **Config** | python-dotenv | Environment variables |

---

## Data Source APIs

### 1. FDA openFDA API

**Endpoint**: `https://api.fda.gov/device/510k.json`

**Authentication**: None required (public API)

**Request Parameters**:
```python
params = {
    'search': f'applicant:"{company_name}"',
    'limit': 100
}
```

**Rate Limits**:
- 240 requests per minute
- 120,000 requests per day

**Response Structure**:
```json
{
  "results": [
    {
      "k_number": "K123456",
      "applicant": "Company Name",
      "device_name": "Product Name",
      "decision_code": "SESE",  // Substantially Equivalent
      "decision_date": "20260315",
      "date_received": "20260101"
    }
  ]
}
```

**Implementation**: [`aggregators/fda_aggregator.py`](src/main/python/aggregators/fda_aggregator.py)

---

### 2. SEC Edgar API

**Endpoint**: `https://www.sec.gov/cgi-bin/browse-edgar`

**Authentication**: None required (User-Agent header mandatory)

**Request Parameters**:
```python
params = {
    'action': 'getcompany',
    'CIK': ticker,
    'type': '',
    'dateb': '',
    'owner': 'exclude',
    'count': 100,
    'output': 'xml'
}
headers = {
    'User-Agent': 'Nephron Data Agents contact@example.com'
}
```

**Rate Limits**:
- 10 requests per second per IP
- Violators may be blocked

**Important Filing Types**:
- **10-K**: Annual report
- **10-Q**: Quarterly report
- **8-K**: Material events
- **S-1**: IPO registration
- **DEF 14A**: Proxy statement

**Implementation**: [`aggregators/sec_aggregator.py`](src/main/python/aggregators/sec_aggregator.py)

---

### 3. NewsAPI

**Endpoint**: `https://newsapi.org/v2/everything`

**Authentication**: API key required

**Request Parameters**:
```python
params = {
    'q': f'{company_name} OR {ticker}',
    'from': from_date,  # YYYY-MM-DD
    'to': to_date,
    'language': 'en',
    'sortBy': 'relevancy',
    'pageSize': 100
}
headers = {
    'X-Api-Key': api_key
}
```

**Rate Limits** (Free Tier):
- 100 requests per day
- 30 days historical data only
- 500 requests per day (paid)

**Response Structure**:
```json
{
  "articles": [
    {
      "source": {"name": "Bloomberg"},
      "title": "Article headline",
      "description": "Article summary",
      "url": "https://...",
      "publishedAt": "2026-03-26T10:30:00Z"
    }
  ]
}
```

**Implementation**: [`aggregators/news_aggregator.py`](src/main/python/aggregators/news_aggregator.py)

---

### 4. Alpha Vantage News Sentiment API

**Endpoint**: `https://www.alphavantage.co/query`

**Authentication**: API key required

**Request Parameters**:
```python
params = {
    'function': 'NEWS_SENTIMENT',
    'tickers': ticker,
    'apikey': api_key,
    'limit': 50
}
```

**Rate Limits** (Free Tier):
- 25 requests per day
- 500 requests per day (premium)

**Unique Features**:
- **Pre-computed sentiment scores** (-1 to +1)
- **Ticker-specific sentiment** (vs overall article sentiment)
- **Relevance scores** (0 to 1)

**Response Structure**:
```json
{
  "feed": [
    {
      "title": "Article title",
      "url": "https://...",
      "time_published": "20260326T103000",
      "overall_sentiment_score": 0.234,
      "overall_sentiment_label": "Somewhat-Bullish",
      "ticker_sentiment": [
        {
          "ticker": "TMO",
          "relevance_score": "0.876",
          "ticker_sentiment_score": "0.456",
          "ticker_sentiment_label": "Bullish"
        }
      ]
    }
  ]
}
```

**Implementation**: [`aggregators/alpha_vantage_aggregator.py`](src/main/python/aggregators/alpha_vantage_aggregator.py)

---

### 5. PubMed E-utilities API

**Endpoints**:
1. **Search**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
2. **Summary**: `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`

**Authentication**: API key optional (increases rate limit)

**Two-Step Process**:

**Step 1 - Search for PMIDs**:
```python
params = {
    'db': 'pubmed',
    'term': company_name,
    'retmax': 50,
    'retmode': 'json',
    'api_key': api_key  # optional
}
```

**Step 2 - Fetch Article Details**:
```python
params = {
    'db': 'pubmed',
    'id': ','.join(pmids),
    'retmode': 'json',
    'api_key': api_key  # optional
}
```

**Rate Limits**:
- **Without API key**: 3 requests/second
- **With API key**: 10 requests/second

**Response Structure**:
```json
{
  "result": {
    "12345678": {
      "uid": "12345678",
      "title": "Research article title",
      "authors": [{"name": "Smith J"}, {"name": "Doe A"}],
      "fulljournalname": "Nature Medicine",
      "pubdate": "2026 Mar 15"
    }
  }
}
```

**Implementation**: [`aggregators/pubmed_aggregator.py`](src/main/python/aggregators/pubmed_aggregator.py)

---

### 6. ScrapeCreators Reddit API

**Endpoint**: `https://api.scrapecreators.com/v1/reddit/search`

**Authentication**: `x-api-key` header required

**Request Parameters**:
```python
params = {
    'query': f'{company_name} OR {ticker}',
    'sort': 'relevance',  # or 'new', 'top', 'comment_count'
    'timeframe': 'month'  # 'day', 'week', 'month', 'year', 'all'
}
headers = {
    'x-api-key': api_key
}
```

**Rate Limits**: Depends on ScrapeCreators plan

**Response Structure**:
```json
{
  "success": true,
  "credits_remaining": 9500,
  "posts": [
    {
      "title": "Post title",
      "selftext": "Post body",
      "subreddit": "stocks",
      "author": "username",
      "score": 42,
      "num_comments": 15,
      "created": 1711234567,
      "permalink": "/r/stocks/comments/..."
    }
  ],
  "after": "t3_abc123"  // Pagination cursor
}
```

**Implementation**: [`aggregators/social_aggregator.py`](src/main/python/aggregators/social_aggregator.py)

---

### 7. Twitter/X (Disabled)

**Status**: ❌ Not available

**Reason**: ScrapeCreators API does not support keyword/cashtag search. Only supports fetching tweets from specific user handles via `/v1/twitter/user-tweets`.

**Alternative**: Could implement with Twitter API v2 (requires enterprise access) or alternative social media APIs.

**Implementation**: [`aggregators/social_aggregator.py`](src/main/python/aggregators/social_aggregator.py) - Returns empty list

---

## Code Structure

### Project Layout

```
stock-sentiment-scraper/
├── README.md                          # High-level user guide
├── TECHNICAL.md                       # This file
├── requirements.txt                   # Python dependencies
├── data/
│   ├── source/                        # Input data (future use)
│   │   └── .gitignore
│   └── output/                        # Generated reports
│       └── .gitignore
└── src/main/python/
    ├── main_pipeline.py               # Main orchestration script
    ├── utils/
    │   ├── __init__.py
    │   └── date_utils.py              # Date range utilities
    ├── aggregators/
    │   ├── __init__.py
    │   ├── fda_aggregator.py          # FDA 510k data
    │   ├── sec_aggregator.py          # SEC filings
    │   ├── news_aggregator.py         # NewsAPI articles
    │   ├── alpha_vantage_aggregator.py # Alpha Vantage news sentiment
    │   ├── pubmed_aggregator.py       # PubMed citations
    │   └── social_aggregator.py       # Reddit + Twitter (disabled)
    ├── sentiment/
    │   ├── __init__.py
    │   └── vader_analyzer.py          # VADER sentiment analysis
    ├── synthesis/
    │   ├── __init__.py
    │   └── gemini_synthesizer.py      # Google Gemini AI summary
    ├── visualization/
    │   ├── __init__.py
    │   └── chart_generator.py         # Matplotlib charts
    └── output/
        ├── __init__.py
        └── pdf_generator.py           # ReportLab PDF generation
```

### Module Responsibilities

#### **main_pipeline.py**
- Command-line argument parsing
- API key loading from `.env`
- Orchestrates 5 phases (aggregate, analyze, synthesize, visualize, report)
- Parallel execution of aggregators
- Console output formatting
- Error handling and graceful degradation

#### **aggregators/**
All aggregators follow the same pattern:
```python
def aggregate_<source>(company_name, ticker, from_date, to_date, api_key=None):
    """
    Returns: List[Dict] with standardized fields:
    - source: str (identifier)
    - title: str
    - date: str (YYYY-MM-DD)
    - ... source-specific fields
    """
```

#### **sentiment/vader_analyzer.py**
- VADER initialization with domain lexicon
- Positive/negative signal detection
- Sentiment classification (positive/negative/neutral)
- Score calculation (-1.0 to 1.0)
- Confidence estimation

#### **synthesis/gemini_synthesizer.py**
- Gemini client configuration
- Prompt engineering for financial summaries
- API call with temperature=0 (deterministic)
- Response parsing and validation
- Fallback handling

#### **visualization/chart_generator.py**
- Daily sentiment aggregation
- Matplotlib figure creation
- Trend line plotting
- Positive/negative zone shading
- PNG export

#### **output/pdf_generator.py**
- ReportLab document setup
- Page layout and styling
- Table generation (sentiment breakdown, top events)
- Chart embedding
- Text wrapping for long titles
- PDF export

---

## Sentiment Analysis Engine

### VADER Configuration

**Base Model**: vaderSentiment 3.3.2

**Domain-Specific Lexicon** (added to VADER):

```python
POSITIVE_SIGNALS = [
    # Regulatory
    'fda approval', '510k clearance', 'breakthrough designation',
    'fast track', 'orphan drug', 'priority review',

    # Financial
    'earnings beat', 'revenue growth', 'upgrade',
    'outperform', 'strong quarter', 'raised guidance',

    # Clinical
    'clinical trial success', 'positive results', 'efficacy',
    'patent approval', 'patent granted',

    # Market
    'market leader', 'competitive advantage', 'innovation'
]

NEGATIVE_SIGNALS = [
    # Regulatory
    'warning letter', 'recall', 'black box warning',
    'fda rejection', 'clinical hold', 'complete response letter',

    # Financial
    'earnings miss', 'downgrade', 'lawsuit',
    'investigation', 'bankruptcy', 'layoffs',

    # Clinical
    'trial failure', 'adverse events', 'safety concerns',

    # Market
    'competition', 'market share loss', 'obsolete'
]
```

### Sentiment Classification Algorithm

```python
def classify_sentiment(text, source_type):
    # 1. Check for domain-specific signals
    for signal in POSITIVE_SIGNALS:
        if signal in text.lower():
            score_boost += 0.2

    for signal in NEGATIVE_SIGNALS:
        if signal in text.lower():
            score_reduction -= 0.2

    # 2. Apply VADER analysis
    vader_scores = analyzer.polarity_scores(text)
    compound_score = vader_scores['compound']

    # 3. Combine domain signals with VADER
    final_score = compound_score + score_boost + score_reduction
    final_score = max(-1.0, min(1.0, final_score))  # Clamp

    # 4. Classify based on threshold
    if final_score >= 0.05:
        label = 'positive'
        confidence = abs(final_score)
    elif final_score <= -0.05:
        label = 'negative'
        confidence = abs(final_score)
    else:
        label = 'neutral'
        confidence = 1.0 - abs(final_score)

    return {
        'label': label,
        'score': final_score,
        'confidence': confidence
    }
```

### Known Limitations

1. **Medical Research Misclassification**
   - Problem: Disease terminology (cancer, death, failure) triggers negative
   - Impact: PubMed articles often false negatives
   - Mitigation: Source-specific rules could be added

2. **Context Independence**
   - Problem: "Not a failure" is classified negative (sees "failure")
   - Impact: Nuanced statements may be wrong
   - Mitigation: Future: Use context-aware models (BERT, RoBERTa)

3. **Sarcasm/Irony**
   - Problem: "Great, another lawsuit" is classified positive
   - Impact: Social media may have accuracy issues
   - Mitigation: Limited - requires deep learning

---

## AI Synthesis

### Gemini Configuration

**Model**: `gemini-2.5-flash`
- Latest Gemini model (as of March 2026)
- Extended thinking mode (uses extra tokens for reasoning)
- Fast inference (~2-3 seconds)

**Parameters**:
```python
config = types.GenerateContentConfig(
    temperature=0,          # Deterministic output
    max_output_tokens=4000  # Accounts for thinking tokens
)
```

### Prompt Engineering

**Structure**:
```python
prompt = f"""You are a financial analyst writing an executive summary.

Based on this sentiment data for {company_name} ({ticker}):

{json.dumps(prompt_data, indent=2)}

Write a professional 2-paragraph executive summary (150-200 words) that:
1. States the overall sentiment and key drivers
2. Highlights the most significant positive and negative events
3. Uses clear, concise financial language

Be direct and data-driven. Do not speculate beyond the data provided.
"""
```

**Input Data** (sent to Gemini):
- Company name and ticker
- Date range
- Total items analyzed
- Sentiment breakdown (counts)
- Top 5 positive items
- Top 5 negative items

**Output** (from Gemini):
- Executive summary (2 paragraphs)
- Extracted key findings
- Overall sentiment assessment

### Token Usage

**Typical Usage** (TMO 30-day analysis):
- Prompt: ~400 tokens
- Thinking: ~380 tokens (internal reasoning)
- Output: ~300 tokens (visible text)
- **Total**: ~1,080 tokens

**Cost** (gemini-2.5-flash free tier):
- Free up to 15 requests/minute
- 1,500 requests/day
- More than sufficient for sentiment analysis

---

## Report Generation

### PDF Layout

**Page Size**: US Letter (8.5" × 11")
**Margins**: 0.75" all sides
**Font**: Helvetica (built-in, no embedding needed)

**Color Scheme**:
- Primary: Navy Blue (#1a237e)
- Positive: Green (#1b5e20, #c8e6c9)
- Negative: Red (#b71c1c, #ffcdd2)
- Neutral: Orange (#ff9800)
- Accent: Light Blue (#e3f2fd)

**Sections**:
1. Title Page (centered)
2. Executive Summary (full width)
3. Sentiment Breakdown Table
4. Overall Sentiment Indicator (color-coded)
5. **Sentiment Trend Chart** (embedded PNG)
6. Key Findings Table
7. Top Positive Events Table
8. Top Negative Events Table

### Chart Specifications

**Dimensions**: 10" × 5" (150 DPI PNG)

**Elements**:
- X-axis: Dates (auto-formatted)
- Y-axis: Sentiment score (-1.0 to 1.0)
- Trend line: Navy blue, 2.5pt, with markers
- Background zones:
  - Positive (0 to 1.0): Light green (#c8e6c9)
  - Negative (-1.0 to 0): Light red (#ffcdd2)
- Zero line: Dashed gray
- Grid: Subtle dotted lines
- Legend: Top-left corner
- Info box: Top-right (total items, avg sentiment)

### JSON Output

**Structure**:
```json
{
  "company": "Company Name",
  "ticker": "TICKER",
  "period": {
    "from": "YYYY-MM-DD",
    "to": "YYYY-MM-DD",
    "days": 30
  },
  "sentiment_breakdown": {
    "positive": 50,
    "negative": 25,
    "neutral": 25
  },
  "synthesis": {
    "executive_summary": "AI-generated summary...",
    "key_findings": ["✓ Finding 1", "✗ Finding 2"],
    "overall_sentiment": "positive|negative|mixed"
  },
  "top_positive": [
    {
      "title": "Event title",
      "date": "YYYY-MM-DD",
      "source": "source_name",
      "score": 0.789
    }
  ],
  "top_negative": [...],
  "raw_data": {
    "total_items": 100,
    "items": [
      {
        "source": "source_name",
        "title": "Full title",
        "date": "YYYY-MM-DD",
        "url": "https://...",
        "description": "...",
        "sentiment": {
          "label": "positive",
          "score": 0.789,
          "confidence": 0.85
        },
        // ... source-specific fields
      }
    ]
  }
}
```

---

## Configuration

### Environment Variables

**Required**:
```bash
GEMINI_API_KEY=              # Google Gemini AI
NEWS_API_KEY=                # NewsAPI.org
ALPHA_VANTAGE_API_KEY=       # Alpha Vantage
SCRAPECREATORS_API_KEY=      # ScrapeCreators (Reddit)
```

**Optional**:
```bash
NCBI_API_KEY=                # PubMed (boosts rate limit 3/s → 10/s)
```

### Code Configuration

**Date Range** (in `main_pipeline.py`):
```python
days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
```

**Parallel Workers** (in `main_pipeline.py`):
```python
with ThreadPoolExecutor(max_workers=6) as executor:
```

**Gemini Token Limit** (in `gemini_synthesizer.py`):
```python
max_output_tokens=4000  # Increase if summaries truncate
```

**Chart DPI** (in `chart_generator.py`):
```python
plt.savefig(output_path, dpi=150, ...)  # Higher = better quality
```

**PDF Margins** (in `pdf_generator.py`):
```python
rightMargin=0.75 * inch,
leftMargin=0.75 * inch,
topMargin=0.75 * inch,
bottomMargin=0.75 * inch
```

---

## Performance & Optimization

### Benchmarks

**Hardware**: Standard GitHub Actions runner (2-core CPU)

| Metric | 7 Days | 30 Days |
|--------|--------|---------|
| Aggregation | ~30s | ~45s |
| Sentiment Analysis | ~2s | ~5s |
| AI Synthesis | ~3s | ~3s |
| Chart Generation | ~1s | ~2s |
| PDF Generation | ~1s | ~1s |
| **Total** | **~37s** | **~56s** |

### Optimization Strategies

**1. Parallel Aggregation**
```python
# Sequential: 6 sources × 5s = 30s
# Parallel:   max(5s) = 5s
with ThreadPoolExecutor(max_workers=6) as executor:
    futures = [executor.submit(task) for task in tasks]
```

**2. Connection Pooling** (requests library auto-handles)

**3. API Result Caching** (not implemented, could add)
```python
# Cache API responses for X minutes
@lru_cache(maxsize=128)
def fetch_with_cache(url, params):
    ...
```

**4. Reduce API Calls**
- Use date filters to limit results
- Request only needed fields
- Batch operations where possible

**5. Async I/O** (future enhancement)
```python
# Could replace ThreadPoolExecutor with asyncio
import aiohttp
async def aggregate_all():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_fda(session), fetch_sec(session), ...]
        return await asyncio.gather(*tasks)
```

---

## Troubleshooting

### Common Issues

#### 1. "No data collected"

**Symptoms**: `Total items collected: 0`

**Causes**:
- API keys missing or invalid
- Company name misspelled
- Date range has no data
- All APIs rate-limited

**Solutions**:
```bash
# Check API keys
cat .env | grep -v '^#'

# Try well-known ticker
python src/main/python/main_pipeline.py JNJ "Johnson & Johnson" 7

# Check API key validity
curl -H "X-Api-Key: YOUR_KEY" "https://newsapi.org/v2/top-headlines?country=us"
```

#### 2. "Rate limit exceeded"

**Symptoms**: `[Source] Rate limit exceeded (429)`

**Solutions**:
- Wait 24 hours (free tier resets)
- Reduce date range (fewer API calls)
- Upgrade to paid API tier
- Use NCBI_API_KEY for PubMed

#### 3. "Chart generation failed"

**Symptoms**: PDF created but no chart

**Causes**:
- No valid date/sentiment data
- matplotlib backend issues

**Solutions**:
```bash
# Check matplotlib backend
python -c "import matplotlib; print(matplotlib.get_backend())"

# Should be 'Agg' (non-interactive)

# If wrong, set in chart_generator.py:
matplotlib.use('Agg')
```

#### 4. "PDF generation failed"

**Symptoms**: JSON created, PDF missing

**Causes**:
- ReportLab not installed
- File permissions issue
- Unicode encoding errors

**Solutions**:
```bash
# Reinstall ReportLab
pip install --upgrade reportlab

# Check permissions
ls -la stock-sentiment-scraper/data/output/

# Fix permissions
chmod 755 stock-sentiment-scraper/data/output/
```

#### 5. "Gemini response truncated"

**Symptoms**: Executive summary incomplete

**Causes**:
- max_output_tokens too low
- Thinking tokens consume limit

**Solution**:
```python
# In gemini_synthesizer.py, increase:
max_output_tokens=8000  # Was 4000
```

#### 6. "UnicodeEncodeError"

**Symptoms**: Console crashes with Unicode error

**Causes**:
- Windows console encoding (cp1252)
- Emoji or special characters in titles

**Solution**:
Already handled via `safe_print()` function in `main_pipeline.py`

---

## Development Guide

### Adding a New Data Source

**1. Create aggregator file**:
```bash
touch src/main/python/aggregators/newsource_aggregator.py
```

**2. Implement aggregator function**:
```python
def aggregate_newsource(company_name, ticker, from_date, to_date, api_key):
    items = []

    # Make API call
    response = requests.get(url, params=params, headers=headers)

    # Parse response
    for item in response.json()['data']:
        items.append({
            'source': 'newsource',
            'title': item['title'],
            'date': item['date'],  # YYYY-MM-DD format
            # ... other fields
        })

    return items
```

**3. Add to main pipeline**:
```python
# In main_pipeline.py imports:
from aggregators import newsource_aggregator

# In aggregation tasks:
def aggregate_newsource():
    if newsource_api_key:
        return newsource_aggregator.aggregate_newsource(...)
    return []

tasks = [
    ...,
    ('NewSource', aggregate_newsource)
]
```

**4. Update .env**:
```bash
NEWSOURCE_API_KEY=your_key_here
```

**5. Update README**:
- Add to data sources table
- Document API details in TECHNICAL.md

### Testing

**Unit Test Template**:
```python
# test_aggregators.py
import unittest
from aggregators import newsource_aggregator

class TestNewsourceAggregator(unittest.TestCase):
    def test_aggregation(self):
        results = newsource_aggregator.aggregate_newsource(
            company_name="Test Company",
            ticker="TEST",
            from_date="2026-03-01",
            to_date="2026-03-31",
            api_key="test_key"
        )
        self.assertIsInstance(results, list)
        if results:
            self.assertIn('source', results[0])
            self.assertEqual(results[0]['source'], 'newsource')
```

**Integration Test**:
```bash
# Test full pipeline with real APIs
python src/main/python/main_pipeline.py TEST "Test Company" 1

# Verify output
ls -lh stock-sentiment-scraper/data/output/ | grep TEST
```

### Code Style

**Follow existing patterns**:
- PEP 8 style guide
- Type hints optional but encouraged
- Docstrings for all public functions
- stderr for logging, stdout for user output
- Specific exception handling (no bare `except:`)

**Example**:
```python
def aggregate_data(company_name: str, ticker: str,
                  from_date: str, to_date: str,
                  api_key: str = None) -> list:
    """Aggregate data from source.

    Args:
        company_name: Full company name
        ticker: Stock ticker symbol
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        api_key: Optional API key

    Returns:
        List of dict items with standardized fields
    """
    items = []

    try:
        # Implementation
        pass
    except (ValueError, KeyError) as e:
        sys.stderr.write(f"[Source] Error: {e}\n")
        sys.stderr.flush()

    return items
```

---

## Future Enhancements

### Planned

1. **Source Weighting**
   - FDA: 40% (high signal)
   - News: 25%
   - Medical: 20%
   - Social: 10%
   - Other: 5%

2. **Historical Comparison**
   - Month-over-month trends
   - Year-over-year comparison
   - Seasonal patterns

3. **Alerts**
   - Email notifications for sentiment changes
   - Slack integration
   - Threshold-based triggers

4. **Multi-ticker Reports**
   - Compare multiple stocks side-by-side
   - Sector analysis
   - Correlation detection

### Under Consideration

1. **Deep Learning Models**
   - Replace VADER with FinBERT or similar
   - Context-aware sentiment
   - Better accuracy on complex text

2. **Real-time Streaming**
   - WebSocket connections
   - Live sentiment dashboard
   - Continuous monitoring

3. **Database Storage**
   - PostgreSQL for historical data
   - Time-series optimization
   - Query capabilities

---

## Appendix

### Dependencies

```
requests==2.31.0
python-dotenv==1.0.0
vaderSentiment==3.3.2
google-genai==1.0.0
reportlab==4.0.7
matplotlib==3.8.2
pandas==2.1.4
```

### File Sizes

**Typical Output** (30-day analysis):

| File | Size Range |
|------|------------|
| JSON | 50-150 KB |
| PDF | 100-120 KB |
| Chart PNG | 80-100 KB |
| **Total** | **230-370 KB** |

### API Response Times

| Source | Avg Response | Max Observed |
|--------|-------------|--------------|
| FDA | 1.2s | 3.5s |
| SEC | 0.8s | 2.1s |
| NewsAPI | 1.5s | 4.2s |
| Alpha Vantage | 1.1s | 3.8s |
| PubMed | 2.3s | 6.1s |
| Reddit | 1.8s | 5.2s |

---

**Last Updated**: 2026-03-28
**Version**: 1.0.0
**Maintainer**: Nephron Data Agents Team
