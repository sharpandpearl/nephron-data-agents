#!/usr/bin/env python3
"""Main pipeline for generic stock sentiment analysis.

Usage:
    python main_pipeline.py <TICKER> <COMPANY_NAME> [DAYS]

Examples:
    python main_pipeline.py RVTY "Revvity" 30
    python main_pipeline.py TMO "Thermo Fisher Scientific" 30
    python main_pipeline.py A "Agilent Technologies" 30
"""

import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add src/main/python to path
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))

# Load environment variables
load_dotenv()

# Import modules
from utils import date_utils
from aggregators import (
    fda_aggregator,
    news_aggregator,
    pubmed_aggregator,
    sec_aggregator,
    social_aggregator,
    alpha_vantage_aggregator
)
from sentiment import vader_analyzer
from synthesis import gemini_synthesizer
from output import pdf_generator
from visualization import chart_generator
from concurrent.futures import ThreadPoolExecutor, as_completed


def safe_print(text):
    """Print text with safe encoding for console (removes problematic Unicode)."""
    try:
        print(text)
    except UnicodeEncodeError:
        # Remove or replace problematic Unicode characters
        safe_text = text.encode('ascii', errors='replace').decode('ascii')
        print(safe_text)


def run_sentiment_analysis(ticker, company_name, days=30):
    """Run sentiment analysis for any stock.

    Args:
        ticker: Stock ticker (e.g., "RVTY", "TMO", "A")
        company_name: Full company name (e.g., "Revvity")
        days: Number of days to analyze (default: 30)

    Returns:
        Dict with analysis results
    """
    print("=" * 60)
    print(f"Stock Sentiment Analysis - {company_name} ({ticker})")
    print("=" * 60)
    print()

    # Get date range
    from_date, to_date = date_utils.get_date_range(days)
    print(f"Period: {from_date} to {to_date} ({days} days)")
    print()

    # Load API keys
    news_api_key = os.getenv('NEWS_API_KEY')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    scrapecreators_api_key = os.getenv('SCRAPECREATORS_API_KEY')
    ncbi_api_key = os.getenv('NCBI_API_KEY')
    alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

    if not news_api_key:
        print("WARNING: NEWS_API_KEY not found in .env file")
    if not gemini_api_key:
        print("WARNING: GEMINI_API_KEY not found in .env file")
    if not scrapecreators_api_key:
        print("WARNING: SCRAPECREATORS_API_KEY not found in .env file")
    if not ncbi_api_key:
        print("INFO: NCBI_API_KEY not found (optional, but recommended for PubMed)")
    if not alpha_vantage_api_key:
        print("WARNING: ALPHA_VANTAGE_API_KEY not found in .env file")

    # Aggregate data from sources (parallel execution)
    print("Phase 1: Aggregating data from multiple sources...")
    print("-" * 60)

    all_items = []

    # Define aggregation tasks
    def aggregate_fda():
        return fda_aggregator.aggregate_fda_data(company_name, from_date, to_date)

    def aggregate_news():
        if news_api_key:
            return news_aggregator.aggregate_news(
                company_name, ticker, from_date, to_date, news_api_key
            )
        print("[WARNING] Skipping news aggregation (no API key)")
        return []

    def aggregate_sec():
        return sec_aggregator.aggregate_sec_filings(ticker, from_date, to_date)

    def aggregate_pubmed():
        if ncbi_api_key:
            return pubmed_aggregator.aggregate_pubmed(
                company_name, from_date, to_date, ncbi_api_key
            )
        return pubmed_aggregator.aggregate_pubmed(
            company_name, from_date, to_date, None
        )

    def aggregate_reddit():
        if scrapecreators_api_key:
            return social_aggregator.aggregate_reddit(
                company_name, ticker, from_date, to_date, scrapecreators_api_key
            )
        print("[WARNING] Skipping Reddit aggregation (no API key)")
        return []

    def aggregate_twitter():
        if scrapecreators_api_key:
            return social_aggregator.aggregate_twitter(
                company_name, ticker, from_date, to_date, scrapecreators_api_key
            )
        print("[WARNING] Skipping Twitter aggregation (no API key)")
        return []

    def aggregate_alpha_vantage():
        if alpha_vantage_api_key:
            return alpha_vantage_aggregator.aggregate_alpha_vantage_news(
                ticker, from_date, to_date, alpha_vantage_api_key
            )
        print("[WARNING] Skipping Alpha Vantage aggregation (no API key)")
        return []

    # Execute all aggregators in parallel
    tasks = [
        ('FDA', aggregate_fda),
        ('News', aggregate_news),
        ('SEC', aggregate_sec),
        ('PubMed', aggregate_pubmed),
        ('Reddit', aggregate_reddit),
        ('Twitter', aggregate_twitter),
        ('Alpha Vantage', aggregate_alpha_vantage)
    ]

    with ThreadPoolExecutor(max_workers=7) as executor:
        future_to_source = {executor.submit(task): name for name, task in tasks}

        for future in as_completed(future_to_source):
            source_name = future_to_source[future]
            try:
                items = future.result()
                all_items.extend(items)
            except Exception as e:
                print(f"[ERROR] {source_name} aggregation failed: {e}")

    print(f"\nTotal items collected: {len(all_items)}")
    print()

    if len(all_items) == 0:
        print("ERROR: No data collected. Check API keys and company name.")
        return None

    # Analyze sentiment
    print("Phase 2: Analyzing sentiment...")
    print("-" * 60)

    all_items = vader_analyzer.analyze_items(all_items)

    # Calculate sentiment breakdown
    positive = [i for i in all_items if i.get('sentiment', {}).get('label') == 'positive']
    negative = [i for i in all_items if i.get('sentiment', {}).get('label') == 'negative']
    neutral = [i for i in all_items if i.get('sentiment', {}).get('label') == 'neutral']

    sentiment_breakdown = {
        'positive': len(positive),
        'negative': len(negative),
        'neutral': len(neutral)
    }

    print()

    # Sort by sentiment score for top items
    positive_sorted = sorted(positive, key=lambda x: x.get('sentiment', {}).get('score', 0), reverse=True)
    negative_sorted = sorted(negative, key=lambda x: x.get('sentiment', {}).get('score', 0))

    # Prepare data for synthesis
    sentiment_data = {
        'from_date': from_date,
        'to_date': to_date,
        'total_items': len(all_items),
        'sentiment_breakdown': sentiment_breakdown,
        'top_positive': positive_sorted[:10],
        'top_negative': negative_sorted[:10],
        'all_items': all_items
    }

    # AI Synthesis
    print("Phase 3: Generating executive summary...")
    print("-" * 60)

    synthesis = None
    if gemini_api_key:
        synthesis = gemini_synthesizer.synthesize_executive_summary(
            company_name, ticker, sentiment_data, gemini_api_key
        )
    else:
        print("[WARNING] Skipping AI synthesis (no Gemini API key)")
        synthesis = {
            'executive_summary': f"Analysis complete for {company_name}.",
            'key_findings': [],
            'overall_sentiment': 'neutral'
        }

    print()

    # Compile results
    results = {
        'company': company_name,
        'ticker': ticker,
        'period': {
            'from': from_date,
            'to': to_date,
            'days': days
        },
        'sentiment_breakdown': sentiment_breakdown,
        'synthesis': synthesis,
        'top_positive': [
            {
                'title': item.get('title', ''),
                'date': item.get('date', ''),
                'source': item.get('source', ''),
                'score': item.get('sentiment', {}).get('score', 0)
            }
            for item in positive_sorted[:10]
        ],
        'top_negative': [
            {
                'title': item.get('title', ''),
                'date': item.get('date', ''),
                'source': item.get('source', ''),
                'score': item.get('sentiment', {}).get('score', 0)
            }
            for item in negative_sorted[:10]
        ],
        'raw_data': {
            'total_items': len(all_items),
            'items': all_items  # All raw data with full fields from all sources
        }
    }

    # Save output to stock-sentiment-scraper/data/output/
    output_dir = SCRIPT_DIR.parent.parent.parent / 'data' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = date_utils.format_timestamp()
    output_json = output_dir / f"{ticker}_sentiment_{timestamp}.json"
    output_pdf = output_dir / f"{ticker}_sentiment_{timestamp}.pdf"

    # Save JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"JSON report saved to: {output_json}")

    # Generate sentiment trend chart
    chart_path = None
    try:
        output_chart = output_dir / f"{ticker}_sentiment_{timestamp}_chart.png"
        chart_path = chart_generator.generate_sentiment_chart(results, output_chart)
        if chart_path:
            print(f"Sentiment chart saved to: {chart_path}")
    except Exception as e:
        print(f"WARNING: Chart generation failed: {e}")

    # Generate PDF
    try:
        pdf_generator.generate_pdf_report(results, output_pdf, chart_path=chart_path)
        print(f"PDF report saved to: {output_pdf}")
    except Exception as e:
        print(f"WARNING: PDF generation failed: {e}")

    print()

    # Print summary
    print("=" * 60)
    print("EXECUTIVE SUMMARY")
    print("=" * 60)
    print(synthesis['executive_summary'])
    print()

    print("=" * 60)
    print("SENTIMENT BREAKDOWN")
    print("=" * 60)
    print(f"Positive: {sentiment_breakdown['positive']}")
    print(f"Negative: {sentiment_breakdown['negative']}")
    print(f"Neutral:  {sentiment_breakdown['neutral']}")
    print(f"Total:    {len(all_items)}")
    print()

    print("=" * 60)
    print("TOP POSITIVE EVENTS")
    print("=" * 60)
    for i, item in enumerate(positive_sorted[:5], 1):
        safe_print(f"{i}. [{item.get('source', 'unknown')}] {item.get('title', '')}")
        safe_print(f"   Score: {item.get('sentiment', {}).get('score', 0):.3f} | Date: {item.get('date', '')}")
    print()

    print("=" * 60)
    print("TOP NEGATIVE EVENTS")
    print("=" * 60)
    for i, item in enumerate(negative_sorted[:5], 1):
        safe_print(f"{i}. [{item.get('source', 'unknown')}] {item.get('title', '')}")
        safe_print(f"   Score: {item.get('sentiment', {}).get('score', 0):.3f} | Date: {item.get('date', '')}")
    print()

    return results


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main_pipeline.py <TICKER> <COMPANY_NAME> [DAYS]")
        print()
        print("Examples:")
        print('  python main_pipeline.py RVTY "Revvity" 30')
        print('  python main_pipeline.py TMO "Thermo Fisher Scientific" 30')
        print('  python main_pipeline.py A "Agilent Technologies" 7')
        sys.exit(1)

    ticker = sys.argv[1]
    company_name = sys.argv[2]
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 30

    run_sentiment_analysis(ticker, company_name, days)
