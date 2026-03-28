#!/usr/bin/env python3
"""Alpha Vantage news sentiment aggregator."""

import requests
import sys
from datetime import datetime


def aggregate_alpha_vantage_news(ticker, from_date, to_date, api_key):
    """Aggregate news sentiment from Alpha Vantage.

    Args:
        ticker: Stock ticker (e.g., "RVTY", "TMO")
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        api_key: Alpha Vantage API key

    Returns:
        List of news articles: [{
            'source': 'alpha_vantage',
            'title': 'Article title',
            'url': 'Article URL',
            'date': 'YYYY-MM-DD',
            'summary': 'Article summary',
            'sentiment_score': 0.123,  # -1 to 1
            'sentiment_label': 'Positive',
            'relevance_score': 0.456  # 0 to 1
        }]
    """
    items = []

    sys.stderr.write(f"[Alpha Vantage] Searching news sentiment for {ticker}...\n")
    sys.stderr.flush()

    try:
        # Alpha Vantage News Sentiment API
        url = "https://www.alphavantage.co/query"

        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': ticker,
            'apikey': api_key,
            'limit': 50  # Max articles to return
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # Check for API error messages
            if 'Error Message' in data:
                sys.stderr.write(f"[Alpha Vantage] API Error: {data['Error Message']}\n")
                sys.stderr.flush()
                return items

            if 'Note' in data:
                sys.stderr.write(f"[Alpha Vantage] API Note: {data['Note']}\n")
                sys.stderr.flush()
                return items

            feed = data.get('feed', [])

            from_dt = datetime.strptime(from_date, '%Y-%m-%d')
            to_dt = datetime.strptime(to_date, '%Y-%m-%d')

            for article in feed:
                # Extract publication date
                time_published = article.get('time_published', '')
                if time_published:
                    # Format: YYYYMMDDTHHMMSS
                    article_date_str = time_published[:8]  # YYYYMMDD
                    try:
                        article_date = f"{article_date_str[:4]}-{article_date_str[4:6]}-{article_date_str[6:8]}"
                        article_dt = datetime.strptime(article_date, '%Y-%m-%d')

                        # Filter by date range
                        if not (from_dt <= article_dt <= to_dt):
                            continue
                    except (ValueError, IndexError):
                        article_date = to_date
                else:
                    article_date = to_date

                # Extract ticker-specific sentiment
                ticker_sentiment = None
                ticker_sentiments = article.get('ticker_sentiment', [])
                for ts in ticker_sentiments:
                    if ts.get('ticker') == ticker:
                        ticker_sentiment = ts
                        break

                # Use overall sentiment if ticker-specific not found
                if ticker_sentiment:
                    sentiment_score = float(ticker_sentiment.get('ticker_sentiment_score', 0))
                    sentiment_label = ticker_sentiment.get('ticker_sentiment_label', 'Neutral')
                    relevance_score = float(ticker_sentiment.get('relevance_score', 0))
                else:
                    sentiment_score = float(article.get('overall_sentiment_score', 0))
                    sentiment_label = article.get('overall_sentiment_label', 'Neutral')
                    relevance_score = 0.5

                items.append({
                    'source': 'alpha_vantage',
                    'title': article.get('title', 'Untitled'),
                    'url': article.get('url', ''),
                    'date': article_date,
                    'summary': (article.get('summary', '') or '')[:500],
                    'sentiment_score': sentiment_score,
                    'sentiment_label': sentiment_label,
                    'relevance_score': relevance_score
                })

            sys.stderr.write(f"[Alpha Vantage] Found {len(items)} articles\n")
            sys.stderr.flush()

        elif response.status_code == 429:
            sys.stderr.write(f"[Alpha Vantage] Rate limit exceeded (429)\n")
            sys.stderr.flush()
        else:
            sys.stderr.write(f"[Alpha Vantage] API returned {response.status_code}\n")
            sys.stderr.flush()

    except Exception as e:
        sys.stderr.write(f"[Alpha Vantage] Error: {e}\n")
        sys.stderr.flush()

    return items
