#!/usr/bin/env python3
"""Social media aggregator using ScrapeCreators API."""

import requests
import sys
from datetime import datetime


def aggregate_reddit(company_name, ticker, from_date, to_date, api_key):
    """Aggregate Reddit discussions about a company/stock.

    Args:
        company_name: Company name
        ticker: Stock ticker (e.g., "RVTY")
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        api_key: ScrapeCreators API key

    Returns:
        List of Reddit posts: [{
            'source': 'reddit',
            'subreddit': 'r/stocks',
            'title': 'Post title',
            'text': 'Post content',
            'author': 'username',
            'score': 123,
            'num_comments': 45,
            'date': 'YYYY-MM-DD',
            'url': 'Reddit URL'
        }]
    """
    items = []

    sys.stderr.write(f"[Reddit] Searching for {company_name}...\n")
    sys.stderr.flush()

    try:
        # ScrapeCreators Reddit search API (corrected implementation)
        url = "https://api.scrapecreators.com/v1/reddit/search"

        # Search query: company name OR ticker
        query = f'{company_name} OR {ticker}'

        # Correct authentication header format
        headers = {
            'x-api-key': api_key
        }

        # Calculate timeframe (day, week, month, year, all)
        from_dt = datetime.strptime(from_date, '%Y-%m-%d')
        to_dt = datetime.strptime(to_date, '%Y-%m-%d')
        days_diff = (to_dt - from_dt).days

        # Map days to Reddit timeframe
        if days_diff <= 1:
            timeframe = 'day'
        elif days_diff <= 7:
            timeframe = 'week'
        elif days_diff <= 30:
            timeframe = 'month'
        elif days_diff <= 365:
            timeframe = 'year'
        else:
            timeframe = 'all'

        # Query parameters (GET not POST)
        params = {
            'query': query,
            'sort': 'relevance',
            'timeframe': timeframe
        }

        response = requests.get(url, headers=headers, params=params, timeout=30)

        if response.status_code == 200:
            data = response.json()

            # ScrapeCreators returns posts directly in 'posts' array
            posts = data.get('posts', [])

            for post in posts:
                # Extract timestamp (ScrapeCreators uses 'created' or 'created_utc')
                created = post.get('created', post.get('created_utc', 0))
                if created:
                    try:
                        post_date = datetime.utcfromtimestamp(created).strftime('%Y-%m-%d')
                        post_dt = datetime.strptime(post_date, '%Y-%m-%d')

                        # Filter by date range
                        if not (from_dt <= post_dt <= to_dt):
                            continue
                    except (ValueError, TypeError):
                        post_date = to_date
                else:
                    post_date = to_date

                # Build Reddit URL
                permalink = post.get('permalink', '')
                if permalink and not permalink.startswith('http'):
                    url = f"https://reddit.com{permalink}"
                else:
                    url = permalink or ''

                items.append({
                    'source': 'reddit',
                    'subreddit': post.get('subreddit', post.get('subreddit_name', 'unknown')),
                    'title': post.get('title', ''),
                    'text': (post.get('selftext', post.get('body', '')) or '')[:500],
                    'author': post.get('author', 'unknown'),
                    'score': post.get('score', post.get('ups', 0)),
                    'num_comments': post.get('num_comments', post.get('comment_count', 0)),
                    'date': post_date,
                    'url': url
                })

            sys.stderr.write(f"[Reddit] Found {len(items)} posts\n")
            sys.stderr.flush()

        elif response.status_code == 429:
            sys.stderr.write(f"[Reddit] Rate limit exceeded (429)\n")
            sys.stderr.flush()
        elif response.status_code == 401:
            sys.stderr.write(f"[Reddit] Authentication failed (401) - check API key\n")
            sys.stderr.flush()
        else:
            sys.stderr.write(f"[Reddit] API returned {response.status_code}: {response.text[:200]}\n")
            sys.stderr.flush()

    except Exception as e:
        sys.stderr.write(f"[Reddit] Error: {e}\n")
        sys.stderr.flush()

    return items


def aggregate_twitter(company_name, ticker, from_date, to_date, api_key):
    """Aggregate Twitter/X mentions about a company/stock.

    NOTE: ScrapeCreators does NOT support Twitter keyword/cashtag search.
    They only provide /v1/twitter/user-tweets which requires a specific username.
    This function is disabled until an alternative Twitter API is found.

    Args:
        company_name: Company name
        ticker: Stock ticker (e.g., "RVTY")
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        api_key: ScrapeCreators API key (unused)

    Returns:
        Empty list (Twitter search not supported)
    """
    sys.stderr.write(f"[Twitter] Skipped - ScrapeCreators does not support keyword/cashtag search\n")
    sys.stderr.flush()
    return []
