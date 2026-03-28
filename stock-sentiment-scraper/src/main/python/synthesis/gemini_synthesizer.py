#!/usr/bin/env python3
"""Gemini AI synthesis for sentiment reports."""

import json
import sys
from google import genai
from google.genai import types


def synthesize_executive_summary(company_name, ticker, sentiment_data, api_key):
    """Generate AI-powered executive summary using Gemini.

    Args:
        company_name: Company name (e.g., "Revvity")
        ticker: Stock ticker (e.g., "RVTY")
        sentiment_data: Dict with sentiment analysis results
        api_key: Gemini API key

    Returns:
        Dict with:
        - executive_summary: String (2-3 paragraphs)
        - key_findings: List of strings
        - overall_sentiment: String ('positive', 'negative', 'neutral')
    """
    sys.stderr.write(f"[Gemini] Generating executive summary...\n")
    sys.stderr.flush()

    try:
        # Configure Gemini client
        client = genai.Client(api_key=api_key)

        # Prepare data for AI
        prompt_data = {
            "company": company_name,
            "ticker": ticker,
            "period": f"{sentiment_data['from_date']} to {sentiment_data['to_date']}",
            "total_items": sentiment_data['total_items'],
            "sentiment_breakdown": sentiment_data['sentiment_breakdown'],
            "top_positive": sentiment_data.get('top_positive', [])[:5],
            "top_negative": sentiment_data.get('top_negative', [])[:5]
        }

        # Create prompt
        prompt = f"""You are a financial analyst writing an executive summary for a sentiment analysis report.

Based on this sentiment data for {company_name} ({ticker}):

{json.dumps(prompt_data, indent=2)}

Write a professional 2-paragraph executive summary (150-200 words) that:
1. States the overall sentiment and key drivers
2. Highlights the most significant positive and negative events
3. Uses clear, concise financial language

Be direct and data-driven. Do not speculate beyond the data provided.
"""

        # Call Gemini API
        # Note: gemini-2.5-flash uses extended thinking, which consumes output tokens
        # Set max_output_tokens high enough to account for thinking + output
        # For larger datasets, thinking tokens can be substantial
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,  # Deterministic output
                max_output_tokens=4000  # High limit to account for thinking tokens on large datasets
            )
        )

        executive_summary = response.text

        sys.stderr.write(f"[Gemini] Generated {len(executive_summary)} character summary\n")
        sys.stderr.flush()

        # Extract key findings from top positive/negative
        key_findings = []
        for item in sentiment_data.get('top_positive', [])[:3]:
            key_findings.append(f"✓ {item.get('title', 'Positive event')}")
        for item in sentiment_data.get('top_negative', [])[:3]:
            key_findings.append(f"✗ {item.get('title', 'Negative event')}")

        # Determine overall sentiment
        breakdown = sentiment_data['sentiment_breakdown']
        if breakdown['positive'] > breakdown['negative'] * 1.5:
            overall = 'positive'
        elif breakdown['negative'] > breakdown['positive'] * 1.5:
            overall = 'negative'
        else:
            overall = 'mixed'

        return {
            'executive_summary': executive_summary,
            'key_findings': key_findings,
            'overall_sentiment': overall
        }

    except Exception as e:
        sys.stderr.write(f"[Gemini] Error: {e}\n")
        sys.stderr.flush()

        # Fallback: return basic summary without AI
        return {
            'executive_summary': f"Sentiment analysis for {company_name} ({ticker}) from {sentiment_data['from_date']} to {sentiment_data['to_date']}. Analyzed {sentiment_data['total_items']} items across FDA and news sources.",
            'key_findings': [],
            'overall_sentiment': 'neutral'
        }
