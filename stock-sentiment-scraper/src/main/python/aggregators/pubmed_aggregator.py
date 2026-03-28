#!/usr/bin/env python3
"""PubMed aggregator for medical journal citations."""

import requests
import sys
import time
from datetime import datetime


def aggregate_pubmed(company_name, from_date, to_date, api_key=None):
    """Aggregate PubMed citations mentioning a company.

    Args:
        company_name: Company name to search for
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        api_key: NCBI API key (optional, increases rate limit)

    Returns:
        List of publications: [{
            'source': 'pubmed',
            'pmid': 'PubMed ID',
            'title': 'Article title',
            'authors': 'First author et al.',
            'journal': 'Journal name',
            'date': 'YYYY-MM-DD',
            'url': 'PubMed URL'
        }]
    """
    items = []

    sys.stderr.write(f"[PubMed] Searching for {company_name}...\n")
    sys.stderr.flush()

    try:
        # Step 1: Search for PMIDs
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

        # Convert dates to PubMed format (YYYY/MM/DD)
        from_date_pm = from_date.replace('-', '/')
        to_date_pm = to_date.replace('-', '/')

        search_params = {
            'db': 'pubmed',
            'term': f'"{company_name}"[Affiliation] OR "{company_name}"[All Fields]',
            'datetype': 'pdat',
            'mindate': from_date_pm,
            'maxdate': to_date_pm,
            'retmax': 50,  # Limit to 50 results
            'retmode': 'json'
        }

        if api_key:
            search_params['api_key'] = api_key

        response = requests.get(search_url, params=search_params, timeout=15)

        if response.status_code != 200:
            sys.stderr.write(f"[PubMed] Search API returned {response.status_code}\n")
            return items

        data = response.json()
        pmids = data.get('esearchresult', {}).get('idlist', [])

        if not pmids:
            sys.stderr.write(f"[PubMed] No publications found\n")
            return items

        sys.stderr.write(f"[PubMed] Found {len(pmids)} publications, fetching details...\n")
        sys.stderr.flush()

        # Step 2: Fetch details for each PMID
        summary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

        # Batch fetch (up to 200 IDs at once)
        pmid_str = ','.join(pmids)

        summary_params = {
            'db': 'pubmed',
            'id': pmid_str,
            'retmode': 'json'
        }

        if api_key:
            summary_params['api_key'] = api_key

        # Rate limiting: 3 req/sec without key, 10 req/sec with key
        if not api_key:
            time.sleep(0.34)  # ~3 requests per second

        response = requests.get(summary_url, params=summary_params, timeout=15)

        if response.status_code != 200:
            sys.stderr.write(f"[PubMed] Summary API returned {response.status_code}\n")
            return items

        summary_data = response.json()
        results = summary_data.get('result', {})

        for pmid in pmids:
            if pmid not in results:
                continue

            article = results[pmid]

            # Extract authors
            authors = article.get('authors', [])
            author_str = 'Unknown'
            if authors:
                first_author = authors[0].get('name', 'Unknown')
                if len(authors) > 1:
                    author_str = f"{first_author} et al."
                else:
                    author_str = first_author

            # Extract publication date
            pubdate = article.get('pubdate', '')
            pub_year = article.get('pubyear', '')

            # Try to construct date (PubMed dates can be partial)
            article_date = to_date  # Fallback to end date
            if pubdate:
                try:
                    # Try to parse full date
                    if len(pubdate) >= 10:
                        article_date = pubdate[:10]
                    elif pub_year:
                        article_date = f"{pub_year}-01-01"
                except (KeyError, IndexError, TypeError):
                    pass

            items.append({
                'source': 'pubmed',
                'pmid': pmid,
                'title': article.get('title', 'Untitled'),
                'authors': author_str,
                'journal': article.get('fulljournalname', article.get('source', 'Unknown')),
                'date': article_date,
                'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
            })

        sys.stderr.write(f"[PubMed] Retrieved {len(items)} publication details\n")
        sys.stderr.flush()

    except Exception as e:
        sys.stderr.write(f"[PubMed] Error: {e}\n")
        sys.stderr.flush()

    return items
