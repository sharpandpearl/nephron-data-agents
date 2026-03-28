#!/usr/bin/env python3
"""FDA data aggregator for stock sentiment analysis."""

import requests
import sys
from datetime import datetime


def aggregate_fda_data(company_name, from_date, to_date):
    """Aggregate FDA regulatory data for a company.

    Searches for:
    - Device approvals (510k clearances)
    - Warning letters
    - Recalls

    Args:
        company_name: Company name to search for (e.g., "Revvity", "Thermo Fisher")
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format

    Returns:
        List of FDA events: [{
            'source': 'fda',
            'type': 'approval|warning|recall',
            'date': 'YYYY-MM-DD',
            'title': 'Event title',
            'description': 'Event description',
            'url': 'FDA URL',
            'sentiment_signal': 'positive|negative|neutral'
        }]
    """
    items = []

    sys.stderr.write(f"[FDA] Searching for {company_name}...\n")
    sys.stderr.flush()

    # Convert dates to FDA API format (YYYYMMDD)
    from_date_fda = from_date.replace('-', '')
    to_date_fda = to_date.replace('-', '')

    # Search 510k clearances (approvals)
    try:
        # FDA openFDA API for device 510k
        url = "https://api.fda.gov/device/510k.json"
        params = {
            'search': f'applicant:"{company_name}"',
            'limit': 100
        }

        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])

            for result in results:
                # Check if within date range
                decision_date = result.get('decision_date', '')
                if decision_date and from_date_fda <= decision_date <= to_date_fda:
                    items.append({
                        'source': 'fda',
                        'type': '510k_clearance',
                        'date': f"{decision_date[:4]}-{decision_date[4:6]}-{decision_date[6:8]}",
                        'title': f"510(k) Clearance: {result.get('device_name', 'Unknown Device')}",
                        'description': result.get('statement_or_summary', '')[:500],
                        'url': f"https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfpmn/pmn.cfm?ID={result.get('k_number', '')}",
                        'sentiment_signal': 'positive'  # Approvals are positive
                    })

            sys.stderr.write(f"[FDA] Found {len([i for i in items if i['type'] == '510k_clearance'])} 510(k) clearances\n")
        else:
            sys.stderr.write(f"[FDA] 510k API returned {response.status_code}\n")

    except Exception as e:
        sys.stderr.write(f"[FDA] Error fetching 510k data: {e}\n")

    sys.stderr.flush()
    return items
