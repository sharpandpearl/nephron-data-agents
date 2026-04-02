---
name: API Integration Lessons
description: Authentication methods, rate limiting strategies, and error handling for external APIs
type: feedback
---

When integrating external APIs, verify documentation carefully and implement proper error handling from the start.

**Why**: During ScrapeCreators Reddit API integration, initial implementation used wrong HTTP method (POST instead of GET) and wrong auth header (Authorization: Bearer instead of x-api-key). This caused all requests to fail with 404 errors. Similarly, Gemini API response truncation issue was caused by not accounting for "thinking tokens" consuming output budget.

**How to apply**:
- Always verify API documentation via WebSearch/WebFetch before implementing
- Check HTTP method (GET vs POST), authentication header format, and request/response structure
- For AI APIs with extended thinking (like Gemini 2.5-flash), set high token limits (4000+) to account for internal reasoning tokens
- Implement proper null checking: verify objects exist before accessing nested properties
- Add specific exception handling instead of bare `except:` clauses
- For rate-limited APIs (NewsAPI: 100/day, Alpha Vantage: 25/day), calculate total daily usage and stagger requests

**Disabled Features**: Don't force integration when API doesn't support required functionality. Example: ScrapeCreators Twitter API only supports user-specific queries, not keyword/cashtag search, so Twitter aggregator was disabled with clear documentation explaining why.

**Authentication Patterns Observed**:
- NewsAPI: `?apiKey=` query parameter
- Alpha Vantage: `&apikey=` query parameter
- ScrapeCreators: `x-api-key` header
- Gemini: API key in client initialization
- PubMed: `&api_key=` query parameter (optional but recommended)
- SEC Edgar: User-Agent header (required per SEC rules)
