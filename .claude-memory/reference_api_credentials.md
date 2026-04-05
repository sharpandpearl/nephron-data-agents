---
name: API Credentials Storage
description: Location of API keys and associated accounts for Nephron project services
type: reference
---

**API Keys Storage Location**:
- Local: `stock-sentiment-scraper/.env` (gitignored, not committed)
- GitHub: Repository Secrets (for Actions workflows)

**Environment Variable Names and Associated Accounts** (all use sharpandpearl@gmail.com):

1. **Google Gemini AI**
   - Variable: `GEMINI_API_KEY`
   - Account: sharpandpearl@gmail.com
   - Usage: Executive summary synthesis

2. **NewsAPI**
   - Variable: `NEWS_API_KEY`
   - Account: sharpandpearl@gmail.com
   - Limit: 100 requests/day

3. **Alpha Vantage**
   - Variable: `ALPHA_VANTAGE_API_KEY`
   - Account: sharpandpearl@gmail.com
   - Limit: 25 requests/day

4. **ScrapeCreators (Reddit)**
   - Variable: `SCRAPECREATORS_API_KEY`
   - Account: sharpandpearl@gmail.com

5. **NCBI PubMed E-utilities**
   - Variable: `NCBI_API_KEY`
   - Account: sharpandpearl@gmail.com

6. **Cloudflare R2**
   - Variables: `NEPHRON_R2_ACCESS_KEY_ID`, `NEPHRON_R2_SECRET_ACCESS_KEY`
   - Stored as GitHub secrets only (not in .env)

**GitHub Secrets** (for Actions):
All above keys stored as secrets: GEMINI_API_KEY, NEWS_API_KEY, ALPHA_VANTAGE_API_KEY, SCRAPECREATORS_API_KEY, NCBI_API_KEY, NEPHRON_R2_ACCESS_KEY_ID, NEPHRON_R2_SECRET_ACCESS_KEY

**Note**: FDA openFDA and SEC Edgar APIs do not require API keys.
