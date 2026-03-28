#!/usr/bin/env python3
"""News aggregator for stock sentiment analysis."""

import os
import requests
import sys
from datetime import datetime


def aggregate_news(company_name, ticker, from_date, to_date, api_key):
    """Aggregate news articles about a company/stock.

    Uses NewsAPI to search for mentions of company name or ticker.

    Args:
        company_name: Company name (e.g., "Revvity")
        ticker: Stock ticker (e.g., "RVTY")
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        api_key: NewsAPI key

    Returns:
        List of news articles: [{
            'source': 'news',
            'source_name': 'Reuters',
            'title': 'Article title',
            'description': 'Article description',
            'url': 'Article URL',
            'date': 'YYYY-MM-DD',
            'published_at': 'ISO timestamp'
        }]
    """
    items = []

    sys.stderr.write(f"[News] Searching for {company_name} OR {ticker}...\n")
    sys.stderr.flush()

    try:
        # NewsAPI endpoint
        url = "https://newsapi.org/v2/everything"

        # Search query: company name OR ticker
        query = f'"{company_name}" OR "{ticker}"'

        params = {
            'q': query,
            'from': from_date,
            'to': to_date,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': 100,  # Max results
            'apiKey': api_key
        }

        response = requests.get(url, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])

            for article in articles:
                # Skip articles without key fields
                if not article.get('title') or not article.get('url'):
                    continue

                # Extract date from publishedAt
                published_at = article.get('publishedAt', '')
                article_date = published_at.split('T')[0] if published_at else to_date

                source_obj = article.get('source')
                source_name = 'Unknown'
                if source_obj and isinstance(source_obj, dict):
                    source_name = source_obj.get('name', 'Unknown')

                items.append({
                    'source': 'news',
                    'source_name': source_name,
                    'title': article.get('title', ''),
                    'description': (article.get('description') or '')[:500],
                    'url': article.get('url', ''),
                    'date': article_date,
                    'published_at': published_at
                })

            sys.stderr.write(f"[News] Found {len(items)} articles\n")
            sys.stderr.flush()

        elif response.status_code == 429:
            sys.stderr.write(f"[News] Rate limit exceeded (429)\n")
            sys.stderr.flush()
        else:
            sys.stderr.write(f"[News] API returned {response.status_code}: {response.text[:200]}\n")
            sys.stderr.flush()

    except Exception as e:
        sys.stderr.write(f"[News] Error: {e}\n")
        sys.stderr.flush()

    return items
