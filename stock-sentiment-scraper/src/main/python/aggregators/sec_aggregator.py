#!/usr/bin/env python3
"""SEC Edgar aggregator for company filings."""

import requests
import sys
from datetime import datetime


def aggregate_sec_filings(ticker, from_date, to_date):
    """Aggregate SEC filings for a stock ticker.

    Fetches recent filings: 10-K, 10-Q, 8-K, etc.

    Args:
        ticker: Stock ticker (e.g., "RVTY", "TMO")
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format

    Returns:
        List of filings: [{
            'source': 'sec',
            'filing_type': '10-K',
            'title': 'Filing description',
            'date': 'YYYY-MM-DD',
            'url': 'SEC EDGAR URL'
        }]
    """
    items = []

    sys.stderr.write(f"[SEC] Searching filings for {ticker}...\n")
    sys.stderr.flush()

    try:
        # SEC EDGAR company search API
        # Note: SEC requires a User-Agent header
        headers = {
            'User-Agent': 'Stock Sentiment Analyzer contact@example.com'
        }

        # Get company CIK (Central Index Key) from ticker
        ticker_url = f"https://www.sec.gov/cgi-bin/browse-edgar"

        params = {
            'action': 'getcompany',
            'CIK': ticker,
            'type': '',  # All filing types
            'dateb': to_date.replace('-', ''),  # End date (YYYYMMDD)
            'owner': 'exclude',
            'output': 'atom',  # XML format
            'count': 100
        }

        response = requests.get(ticker_url, params=params, headers=headers, timeout=15)

        if response.status_code != 200:
            sys.stderr.write(f"[SEC] API returned {response.status_code}\n")
            return items

        # Parse XML response (basic parsing)
        content = response.text

        # Extract filing entries
        import re

        # Find all entry tags
        entries = re.findall(r'<entry>(.*?)</entry>', content, re.DOTALL)

        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d')
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d')

        for entry in entries:
            # Extract filing type
            filing_type_match = re.search(r'<category[^>]*term="([^"]+)"', entry)
            filing_type = filing_type_match.group(1) if filing_type_match else 'Unknown'

            # Extract title
            title_match = re.search(r'<title>([^<]+)</title>', entry)
            title = title_match.group(1) if title_match else f"{filing_type} Filing"

            # Extract filing date
            updated_match = re.search(r'<updated>([^<]+)</updated>', entry)
            if updated_match:
                filing_date_str = updated_match.group(1).split('T')[0]
                filing_date_obj = datetime.strptime(filing_date_str, '%Y-%m-%d')

                # Check if within date range
                if not (from_date_obj <= filing_date_obj <= to_date_obj):
                    continue
            else:
                continue

            # Extract URL
            link_match = re.search(r'<link[^>]*href="([^"]+)"', entry)
            url = link_match.group(1) if link_match else ''

            # Filter for important filing types
            important_types = ['10-K', '10-Q', '8-K', '10-K/A', '10-Q/A', '8-K/A']
            if filing_type not in important_types:
                continue

            items.append({
                'source': 'sec',
                'filing_type': filing_type,
                'title': title.strip(),
                'date': filing_date_str,
                'url': url
            })

        sys.stderr.write(f"[SEC] Found {len(items)} filings\n")
        sys.stderr.flush()

    except Exception as e:
        sys.stderr.write(f"[SEC] Error: {e}\n")
        sys.stderr.flush()

    return items
