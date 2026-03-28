#!/usr/bin/env python3
"""Sentiment trend chart generator using Matplotlib."""

import sys
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle


def generate_sentiment_chart(results, output_path):
    """Generate sentiment trend chart over time.

    Args:
        results: Dict with analysis results containing raw_data
        output_path: Path to save PNG chart

    Returns:
        Path to generated chart file
    """
    sys.stderr.write(f"[Chart] Generating sentiment trend visualization...\n")
    sys.stderr.flush()

    # Extract raw items
    raw_items = results.get('raw_data', {}).get('items', [])
    if not raw_items:
        sys.stderr.write(f"[Chart] No data to visualize\n")
        sys.stderr.flush()
        return None

    # Group items by date and calculate daily average sentiment
    daily_sentiment = defaultdict(list)

    for item in raw_items:
        date_str = item.get('date', '')
        sentiment = item.get('sentiment', {})
        score = sentiment.get('score', 0)

        if date_str and score is not None:
            # Parse date (handle different formats)
            try:
                # Try YYYY-MM-DD format
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                try:
                    # Try "YYYY MMM D" format (PubMed)
                    date_obj = datetime.strptime(date_str, '%Y %b %d')
                except ValueError:
                    # Skip if can't parse
                    continue

            daily_sentiment[date_obj].append(score)

    if not daily_sentiment:
        sys.stderr.write(f"[Chart] No valid date/sentiment data found\n")
        sys.stderr.flush()
        return None

    # Calculate daily averages
    dates = sorted(daily_sentiment.keys())
    avg_scores = [sum(daily_sentiment[date]) / len(daily_sentiment[date]) for date in dates]
    item_counts = [len(daily_sentiment[date]) for date in dates]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Set style
    ax.set_facecolor('#f5f5f5')
    fig.patch.set_facecolor('white')

    # Add horizontal reference zones
    ax.axhspan(-1.0, 0, facecolor='#ffcdd2', alpha=0.3, zorder=0)  # Negative zone (light red)
    ax.axhspan(0, 1.0, facecolor='#c8e6c9', alpha=0.3, zorder=0)   # Positive zone (light green)
    ax.axhline(0, color='#666666', linewidth=1, linestyle='--', alpha=0.5, zorder=1)  # Zero line

    # Plot sentiment trend
    ax.plot(dates, avg_scores, color='#1a237e', linewidth=2.5, marker='o',
            markersize=6, markerfacecolor='#1a237e', markeredgewidth=0,
            label='Daily Avg Sentiment', zorder=3)

    # Add subtle grid
    ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.3, zorder=2)

    # Format x-axis (dates)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates) // 10)))
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Set y-axis limits and labels
    ax.set_ylim(-1.0, 1.0)
    ax.set_ylabel('Sentiment Score', fontsize=11, fontweight='bold', color='#333333')
    ax.set_xlabel('Date', fontsize=11, fontweight='bold', color='#333333')

    # Title
    company = results.get('company', 'Company')
    ticker = results.get('ticker', '')
    period = results.get('period', {})
    days = period.get('days', 30)

    title = f"{company} ({ticker}) - Sentiment Trend ({days} Days)"
    ax.set_title(title, fontsize=14, fontweight='bold', color='#1a237e', pad=15)

    # Add legend
    ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True, fontsize=9)

    # Add summary text box
    total_items = len(raw_items)
    avg_sentiment = sum(avg_scores) / len(avg_scores) if avg_scores else 0

    textstr = f'Total Items: {total_items}\nAvg Sentiment: {avg_sentiment:.3f}'
    props = dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='#1a237e')
    ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    # Tight layout
    plt.tight_layout()

    # Save figure
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    sys.stderr.write(f"[Chart] Saved to {output_path}\n")
    sys.stderr.flush()

    return output_path


def generate_sentiment_distribution_chart(results, output_path):
    """Generate sentiment distribution bar chart.

    Args:
        results: Dict with analysis results
        output_path: Path to save PNG chart

    Returns:
        Path to generated chart file
    """
    sys.stderr.write(f"[Chart] Generating sentiment distribution chart...\n")
    sys.stderr.flush()

    breakdown = results.get('sentiment_breakdown', {})

    categories = ['Positive', 'Negative', 'Neutral']
    counts = [
        breakdown.get('positive', 0),
        breakdown.get('negative', 0),
        breakdown.get('neutral', 0)
    ]
    colors = ['#4caf50', '#f44336', '#9e9e9e']

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 5))

    # Create bar chart
    bars = ax.bar(categories, counts, color=colors, alpha=0.8, edgecolor='#333333', linewidth=1.5)

    # Add value labels on bars
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Styling
    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
    ax.set_title(f"Sentiment Distribution - {results.get('company', 'Company')} ({results.get('ticker', '')})",
                 fontsize=14, fontweight='bold', color='#1a237e', pad=15)
    ax.set_facecolor('#f5f5f5')
    fig.patch.set_facecolor('white')

    # Grid
    ax.grid(True, axis='y', linestyle=':', linewidth=0.5, alpha=0.3, zorder=0)
    ax.set_axisbelow(True)

    # Tight layout
    plt.tight_layout()

    # Save
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)

    sys.stderr.write(f"[Chart] Saved distribution chart to {output_path}\n")
    sys.stderr.flush()

    return output_path
