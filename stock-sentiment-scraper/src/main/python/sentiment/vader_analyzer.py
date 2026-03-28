#!/usr/bin/env python3
"""VADER sentiment analysis with domain-specific rules."""

import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Domain-specific sentiment signals
POSITIVE_SIGNALS = [
    'fda approval', '510k clearance', '510(k)', 'approved', 'clearance',
    'earnings beat', 'beat expectations', 'upgrade', 'outperform',
    'strong growth', 'revenue growth', 'profit', 'acquisition',
    'partnership', 'breakthrough', 'innovation'
]

NEGATIVE_SIGNALS = [
    'warning letter', 'recall', 'downgrade', 'underperform',
    'earnings miss', 'miss expectations', 'loss', 'decline',
    'investigation', 'lawsuit', 'fraud', 'violation',
    'fine', 'penalty', 'layoffs', 'bankruptcy'
]

# Initialize VADER
_analyzer = None


def get_analyzer():
    """Get or create VADER sentiment analyzer instance."""
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer


def classify_sentiment(text, source_type='general'):
    """Classify sentiment of text using VADER with domain rules.

    Args:
        text: Text to analyze
        source_type: Type of source ('fda', 'news', 'social', etc.)

    Returns:
        Dict with:
        - label: 'positive', 'negative', or 'neutral'
        - score: Compound score from -1 to 1
        - confidence: Confidence in classification (0-1)
    """
    if not text or not isinstance(text, str):
        return {
            'label': 'neutral',
            'score': 0.0,
            'confidence': 0.0
        }

    analyzer = get_analyzer()
    text_lower = text.lower()

    # Apply domain-specific overrides
    has_positive = any(signal in text_lower for signal in POSITIVE_SIGNALS)
    has_negative = any(signal in text_lower for signal in NEGATIVE_SIGNALS)

    # FDA events with pre-classified signals
    if source_type == 'fda':
        if '510k' in text_lower or 'clearance' in text_lower or 'approval' in text_lower:
            return {'label': 'positive', 'score': 0.8, 'confidence': 0.95}
        if 'warning letter' in text_lower or 'recall' in text_lower:
            return {'label': 'negative', 'score': -0.8, 'confidence': 0.95}

    # Get VADER scores
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    # Apply domain rule boost
    if has_positive and not has_negative:
        compound = min(1.0, compound + 0.2)
    elif has_negative and not has_positive:
        compound = max(-1.0, compound - 0.2)

    # Classify based on compound score
    if compound >= 0.05:
        label = 'positive'
    elif compound <= -0.05:
        label = 'negative'
    else:
        label = 'neutral'

    # Confidence based on absolute compound score
    confidence = min(1.0, abs(compound))

    return {
        'label': label,
        'score': round(compound, 3),
        'confidence': round(confidence, 2)
    }


def analyze_items(items):
    """Analyze sentiment for a list of items.

    Args:
        items: List of dicts with 'text' or 'title' + 'description' fields

    Returns:
        Items with added 'sentiment' field
    """
    sys.stderr.write(f"[Sentiment] Analyzing {len(items)} items...\n")
    sys.stderr.flush()

    for item in items:
        # Combine title + description for analysis
        text_parts = []
        if item.get('title'):
            text_parts.append(item['title'])
        if item.get('description'):
            text_parts.append(item['description'])

        text = ' '.join(text_parts)
        source_type = item.get('source', 'general')

        item['sentiment'] = classify_sentiment(text, source_type)

    # Count by label
    positive = sum(1 for i in items if i.get('sentiment', {}).get('label') == 'positive')
    negative = sum(1 for i in items if i.get('sentiment', {}).get('label') == 'negative')
    neutral = sum(1 for i in items if i.get('sentiment', {}).get('label') == 'neutral')

    sys.stderr.write(f"[Sentiment] Positive: {positive}, Negative: {negative}, Neutral: {neutral}\n")
    sys.stderr.flush()

    return items
