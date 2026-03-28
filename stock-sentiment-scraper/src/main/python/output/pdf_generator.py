#!/usr/bin/env python3
"""PDF report generator for sentiment analysis."""

import sys
from datetime import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, KeepTogether, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_pdf_report(results, output_path, chart_path=None):
    """Generate PDF report from sentiment analysis results.

    Args:
        results: Dict with analysis results
        output_path: Path to save PDF file
        chart_path: Optional path to sentiment trend chart image

    Returns:
        Path to generated PDF file
    """
    sys.stderr.write(f"[PDF] Generating report...\n")
    sys.stderr.flush()

    # Create document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch
    )

    # Container for document elements
    story = []

    # Define styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=12,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#455a64'),
        spaceAfter=24,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=12,
        spaceBefore=12
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=12
    )

    # Title Page
    story.append(Spacer(1, 1.5 * inch))
    story.append(Paragraph("Stock Sentiment Analysis Report", title_style))
    story.append(Spacer(1, 0.2 * inch))

    company_info = f"{results['company']} ({results['ticker']})"
    story.append(Paragraph(company_info, subtitle_style))

    period_info = f"Analysis Period: {results['period']['from']} to {results['period']['to']} ({results['period']['days']} days)"
    story.append(Paragraph(period_info, body_style))

    generated_date = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(generated_date, body_style))

    story.append(PageBreak())

    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))

    synthesis = results.get('synthesis', {})
    exec_summary = synthesis.get('executive_summary', 'No summary available')

    # Split summary into paragraphs
    paragraphs = exec_summary.split('\n\n')
    for para in paragraphs:
        if para.strip():
            # Remove markdown formatting for PDF
            para_clean = para.replace('**', '').replace('*', '')
            story.append(Paragraph(para_clean, body_style))

    story.append(Spacer(1, 0.3 * inch))

    # Sentiment Breakdown
    story.append(Paragraph("Sentiment Breakdown", heading_style))

    breakdown = results.get('sentiment_breakdown', {})
    total = breakdown.get('positive', 0) + breakdown.get('negative', 0) + breakdown.get('neutral', 0)

    breakdown_data = [
        ['Category', 'Count', 'Percentage'],
        ['Positive', str(breakdown.get('positive', 0)), f"{breakdown.get('positive', 0) / total * 100:.1f}%"],
        ['Negative', str(breakdown.get('negative', 0)), f"{breakdown.get('negative', 0) / total * 100:.1f}%"],
        ['Neutral', str(breakdown.get('neutral', 0)), f"{breakdown.get('neutral', 0) / total * 100:.1f}%"],
        ['Total', str(total), '100.0%']
    ]

    breakdown_table = Table(breakdown_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e3f2fd')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey])
    ]))

    story.append(breakdown_table)
    story.append(Spacer(1, 0.3 * inch))

    # Overall Sentiment
    overall_sentiment = synthesis.get('overall_sentiment', 'neutral').upper()
    sentiment_color = {
        'POSITIVE': colors.green,
        'NEGATIVE': colors.red,
        'NEUTRAL': colors.orange,
        'MIXED': colors.orange
    }.get(overall_sentiment, colors.grey)

    overall_style = ParagraphStyle(
        'OverallSentiment',
        parent=body_style,
        fontSize=14,
        textColor=sentiment_color,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    story.append(Paragraph(f"Overall Sentiment: {overall_sentiment}", overall_style))
    story.append(Spacer(1, 0.3 * inch))

    # Sentiment Trend Chart (if provided)
    if chart_path and Path(chart_path).exists():
        story.append(Paragraph("Sentiment Trend Over Time", heading_style))

        # Add chart image (centered, scaled to fit page width)
        img = Image(str(chart_path), width=6.5 * inch, height=3.25 * inch)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 0.3 * inch))

    # Key Findings
    story.append(Paragraph("Key Findings", heading_style))

    key_findings = synthesis.get('key_findings', [])
    if key_findings:
        findings_text_style = ParagraphStyle(
            'FindingsText',
            parent=body_style,
            fontSize=9,
            leading=12
        )

        findings_data = [['Finding']]
        for finding in key_findings:
            # Wrap finding in Paragraph for proper text wrapping
            finding_para = Paragraph(finding, findings_text_style)
            findings_data.append([finding_para])

        findings_table = Table(findings_data, colWidths=[6.5 * inch])
        findings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 1), (-1, -1), 12),
            ('RIGHTPADDING', (0, 1), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8)
        ]))

        story.append(findings_table)
    else:
        story.append(Paragraph("No key findings available.", body_style))

    story.append(Spacer(1, 0.3 * inch))

    # Top Positive Events
    story.append(Paragraph("Top Positive Events", heading_style))

    top_positive = results.get('top_positive', [])[:5]
    if top_positive:
        # Create table-specific style for wrapping text
        table_text_style = ParagraphStyle(
            'TableText',
            parent=body_style,
            fontSize=8,
            leading=10
        )

        positive_data = [['Title', 'Source', 'Date', 'Score']]
        for item in top_positive:
            # Wrap title in Paragraph for proper text wrapping
            title_text = item.get('title', 'Unknown')[:50] + ('...' if len(item.get('title', '')) > 50 else '')
            title_para = Paragraph(title_text, table_text_style)

            positive_data.append([
                title_para,
                item.get('source', 'unknown'),
                item.get('date', ''),
                f"{item.get('score', 0):.3f}"
            ])

        positive_table = Table(positive_data, colWidths=[3.2 * inch, 1.1 * inch, 1.0 * inch, 0.8 * inch])
        positive_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1b5e20')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgreen])
        ]))

        story.append(positive_table)
    else:
        story.append(Paragraph("No positive events found.", body_style))

    story.append(Spacer(1, 0.3 * inch))

    # Top Negative Events
    story.append(Paragraph("Top Negative Events", heading_style))

    top_negative = results.get('top_negative', [])[:5]
    if top_negative:
        negative_data = [['Title', 'Source', 'Date', 'Score']]
        for item in top_negative:
            # Wrap title in Paragraph for proper text wrapping
            title_text = item.get('title', 'Unknown')[:50] + ('...' if len(item.get('title', '')) > 50 else '')
            title_para = Paragraph(title_text, table_text_style)

            negative_data.append([
                title_para,
                item.get('source', 'unknown'),
                item.get('date', ''),
                f"{item.get('score', 0):.3f}"
            ])

        negative_table = Table(negative_data, colWidths=[3.2 * inch, 1.1 * inch, 1.0 * inch, 0.8 * inch])
        negative_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#b71c1c')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#ffcdd2')])
        ]))

        story.append(negative_table)
    else:
        story.append(Paragraph("No negative events found.", body_style))

    # Build PDF
    doc.build(story)

    sys.stderr.write(f"[PDF] Report saved to {output_path}\n")
    sys.stderr.flush()

    return output_path
