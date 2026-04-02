---
name: Cloudflare R2 Storage Structure
description: R2 bucket organization and naming conventions for Nephron data outputs
type: reference
---

**Bucket Name**: `nephron-data`

**Path Structure**:
```
nephron-data/
├── {TICKER}/
│   ├── scraper/
│   │   └── results_{TIMESTAMP}.csv
│   └── sentiment/
│       ├── report_{TIMESTAMP}.pdf
│       └── raw_{TIMESTAMP}.json
```

**Ticker Format**: Uppercase (A, TMO, RVTY, etc.)

**Examples**:
- `nephron-data/TMO/scraper/results_20260402_143022.csv`
- `nephron-data/RVTY/sentiment/report_20260402_080015.pdf`
- `nephron-data/A/sentiment/raw_20260402_080000.json`

**Timestamp Format**: `YYYYMMDD_HHMMSS` (UTC)

**Workflow Integration**:
- GitHub Actions uses AWS CLI v2 with S3-compatible endpoint
- Upload command: `aws s3 cp --endpoint-url https://[account-id].r2.cloudflarestorage.com`
- Both R2 and GitHub Actions artifacts (30-day retention) receive copies

**Access**:
- Credentials stored as GitHub secrets (NEPHRON_R2_ACCESS_KEY_ID, NEPHRON_R2_SECRET_ACCESS_KEY)
- S3-compatible API for programmatic access

**File Types by Module**:
- Product scrapers (TMO, etc.): CSV only
- Sentiment analyzers: JSON (raw data) + PDF (report) + PNG (chart, not uploaded to R2)
