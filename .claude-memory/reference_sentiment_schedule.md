---
name: Sentiment Analyzer Schedule
description: Nightly run schedule for 16 pharma/biotech tickers with 3-minute staggering
type: reference
---

**Schedule**: Nightly at 4:00 AM EDT (8:00 AM UTC), staggered by 3 minutes

**16 Tickers** (in chronological order):

| Time (UTC) | Time (EDT) | Ticker | Company |
|------------|------------|--------|---------|
| 8:00 | 4:00 | A | Agilent Technologies |
| 8:03 | 4:03 | BIO | Bio-Rad Laboratories |
| 8:06 | 4:06 | DHR | Danaher Corporation |
| 8:09 | 4:09 | EXAS | Exact Sciences |
| 8:12 | 4:12 | GH | Guardant Health |
| 8:15 | 4:15 | HOLX | Hologic |
| 8:18 | 4:18 | ICLR | Icon plc |
| 8:21 | 4:21 | ILMN | Illumina |
| 8:24 | 4:24 | IQV | IQVIA Holdings |
| 8:27 | 4:27 | LH | Laboratory Corporation of America |
| 8:30 | 4:30 | NTRA | Natera |
| 8:33 | 4:33 | PACB | Pacific Biosciences |
| 8:36 | 4:36 | QDEL | Quidel Corporation |
| 8:39 | 4:39 | QGEN | Qiagen N.V. |
| 8:42 | 4:42 | RVTY | Revvity |
| 8:45 | 4:45 | TMO | Thermo Fisher Scientific |

**Workflow Files**: `.github/workflows/sentiment-{TICKER}.yml`

**Template**: All use `.github/workflows/sentiment-template.yml` (reusable workflow)

**Analysis Period**: 30 days (configurable via `analysis_days` parameter)
- Exception: TMO manually set to 365 days

**API Rate Limit Consideration**: 16 tickers × daily runs = close to Alpha Vantage's 25 requests/day limit. Staggering helps spread load and avoid simultaneous API calls.

**Manual Triggering**: All workflows include `workflow_dispatch` trigger for on-demand runs via GitHub Actions UI.
