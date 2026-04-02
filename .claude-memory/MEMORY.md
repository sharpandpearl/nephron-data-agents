# Nephron Data Agents - Memory Index

## User
- [User Profile](user_profile.md) — Technical background and preferred email accounts for API services

## Project
- [Nephron Data Agents Context](nephron_data_agents_context.md) — Multi-module Maven project with scrapers and sentiment analyzers
- [Stock Sentiment Analyzer](project_stock_sentiment_analyzer.md) — 16-ticker sentiment analysis system with 6 data sources and AI synthesis
- [TMO Product Scraper](project_tmo_scraper.md) — First Maven scraper module, serves as template for future vendor scrapers

## Feedback
- [GitHub Actions Workflow Preferences](feedback_github_actions.md) — Detailed step-by-step logging with reusable templates and staggered scheduling
- [API Integration Lessons](feedback_api_integration.md) — Authentication patterns, rate limiting, and proper error handling for external APIs
- [Code Organization and Documentation](feedback_code_organization.md) — Split docs into README (user) + TECHNICAL (developer)
- [Error Handling and Debugging](feedback_error_handling.md) — Fix root causes: null checks, specific exceptions, Unicode handling

## Reference
- [API Credentials Storage](reference_api_credentials.md) — .env file location and GitHub secrets for all API keys
- [Cloudflare R2 Storage Structure](reference_r2_storage.md) — Bucket organization and naming conventions for outputs
- [Sentiment Analyzer Schedule](reference_sentiment_schedule.md) — Nightly 4am EDT runs for 16 tickers with 3-minute staggering
