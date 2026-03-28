#!/usr/bin/env python3
"""Date utility functions for sentiment analysis."""

from datetime import datetime, timedelta


def get_date_range(days_back=30):
    """Calculate date range for analysis.

    Args:
        days_back: Number of days to look back (default: 30)

    Returns:
        Tuple of (from_date, to_date) as ISO format strings (YYYY-MM-DD)
    """
    to_date = datetime.utcnow()
    from_date = to_date - timedelta(days=days_back)

    return (
        from_date.strftime('%Y-%m-%d'),
        to_date.strftime('%Y-%m-%d')
    )


def format_timestamp():
    """Get current UTC timestamp for filenames.

    Returns:
        String in format YYYY-MM-DD_HHMMSS
    """
    return datetime.utcnow().strftime('%Y-%m-%d_%H%M%S')
