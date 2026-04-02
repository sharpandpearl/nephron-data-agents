---
name: API Credentials Storage
description: Location of API keys and associated accounts for Nephron project services
type: reference
---

**API Keys Storage Location**:
`stock-sentiment-scraper/.env` (gitignored, not committed)

**API Keys and Associated Accounts** (all use sharpandpearl@gmail.com):

1. **Google Gemini AI**
   - Key: AIzaSyBnzy2TqXBocnGz9Cm9lXTxZtLuxb4vupg
   - Account: sharpandpearl@gmail.com
   - Usage: Executive summary synthesis
   - Note in .env: "# Google Gemini API (sharpandpearl@gmail.com)"

2. **NewsAPI**
   - Key: 458df64b626a4fe48e22d9f6619d1573
   - Account: sharpandpearl@gmail.com
   - Limit: 100 requests/day

3. **Alpha Vantage**
   - Key: 10P0TL76FI2TFYWX
   - Account: sharpandpearl@gmail.com
   - Limit: 25 requests/day

4. **ScrapeCreators (Reddit)**
   - Key: XkDIHOeFUuUqwjdbRSkcW0lUt682
   - Account: sharpandpearl@gmail.com

5. **NCBI PubMed E-utilities**
   - Key: 1ad11e1fd33bcf9a636e91e3b6e117f3a309
   - Account: sharpandpearl@gmail.com

6. **Cloudflare R2**
   - Access Key ID: (stored as GitHub secret NEPHRON_R2_ACCESS_KEY_ID)
   - Secret Access Key: (stored as GitHub secret NEPHRON_R2_SECRET_ACCESS_KEY)

**GitHub Secrets** (for Actions):
All above keys stored as secrets: GEMINI_API_KEY, NEWS_API_KEY, ALPHA_VANTAGE_API_KEY, SCRAPECREATORS_API_KEY, NCBI_API_KEY, NEPHRON_R2_ACCESS_KEY_ID, NEPHRON_R2_SECRET_ACCESS_KEY

**Note**: FDA openFDA and SEC Edgar APIs do not require API keys.
