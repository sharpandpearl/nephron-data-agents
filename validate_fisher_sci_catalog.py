#!/usr/bin/env python3
"""
Fisher Scientific Catalog ID Validator
Fast validation using HTTP HEAD requests instead of browser automation.
Estimated time: ~20-30 minutes for 8,675 products (vs 30+ hours with Playwright)
"""

import pandas as pd
import requests
import concurrent.futures
import time
from datetime import datetime

# Configuration
INPUT_CSV = 'source-data/TMO_Product_list.csv'
OUTPUT_CSV = 'generated-data/TMO_Product_list_Validated.csv'
MAX_WORKERS = 10  # Number of concurrent requests
TIMEOUT = 5  # Timeout in seconds for each request
PROGRESS_INTERVAL = 100  # Print progress every N products
TEST_MODE = False  # Set to False to validate all products
TEST_LIMIT = 1000  # Number of products to validate in test mode

# Fisher Scientific URL pattern - using search URL (same as Playwright scraper)
BASE_URL = 'https://www.fishersci.com/us/en/catalog/search/products?keyword={id}'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def check_product_id(product_id):
    """
    Check if a Fisher Scientific product ID is valid by searching for it.
    Uses GET request to search page and checks for valid product results.

    Args:
        product_id: The catalog number to validate

    Returns:
        tuple: (product_id, status, response_time)
    """
    url = BASE_URL.format(id=product_id)
    start_time = time.time()

    try:
        # Use GET request to check the search results
        response = requests.get(url, headers=HEADERS, allow_redirects=True, timeout=TIMEOUT)
        response_time = round(time.time() - start_time, 2)

        if response.status_code == 200:
            # Check if the response indicates a valid product
            content_lower = response.text.lower()
            final_url = response.url
            final_url_lower = final_url.lower()

            # Check if product doesn't exist at all (search results page with no matches)
            if ('no results found' in content_lower or
                '0 results' in content_lower):
                return product_id, "Invalid (Not Found)", response_time

            # Check if we landed on an actual product page
            # Valid URL format: https://www.fishersci.com/shop/products/{product-slug}/{catalog-id}
            is_product_page = '/shop/products/' in final_url_lower

            # Check if the URL ends with the catalog ID (with optional query parameters)
            # Split by '?' to remove query params, then check if path ends with catalog ID
            url_path = final_url.split('?')[0]  # Remove query parameters
            url_ends_with_id = url_path.endswith(f'/{product_id}') or url_path.endswith(f'/{product_id}/')

            # Conservative validation: Only mark as VALID if:
            # 1. We landed on a product page (/shop/products/) AND
            # 2. The URL path ends with the catalog ID
            if is_product_page and url_ends_with_id:
                return product_id, "Valid", response_time

            # If we're still on a search page or URL doesn't end with catalog ID, it's invalid
            else:
                return product_id, "Invalid (Not Found)", response_time

        elif response.status_code == 404:
            return product_id, "Invalid (404)", response_time
        elif response.status_code == 403:
            return product_id, "Forbidden (403)", response_time
        else:
            return product_id, f"Unknown ({response.status_code})", response_time

    except requests.Timeout:
        response_time = TIMEOUT
        return product_id, "Timeout", response_time
    except requests.RequestException as e:
        response_time = round(time.time() - start_time, 2)
        return product_id, f"Error: {str(e)[:50]}", response_time

def main():
    """Main validation function"""
    print("=" * 70)
    print("Fisher Scientific Catalog ID Validator")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Load product IDs from CSV
    print(f"Loading catalog IDs from: {INPUT_CSV}")
    try:
        # Read the file and handle both formats: one-line comma-separated or multi-line
        with open(INPUT_CSV, 'r', encoding='utf-8-sig') as f:  # utf-8-sig to handle BOM
            content = f.read().strip()

        # Check if it's a single line with commas or multiple lines
        if ',' in content and '\n' not in content:
            # Single line, comma-separated format
            product_ids = [pid.strip() for pid in content.split(',') if pid.strip()]
        else:
            # Multi-line format (fallback to pandas)
            df = pd.read_csv(INPUT_CSV, header=None, names=['ProductID'])
            product_ids = df['ProductID'].astype(str).tolist()

        # Apply test mode limit if enabled
        if TEST_MODE and len(product_ids) > TEST_LIMIT:
            product_ids = product_ids[:TEST_LIMIT]
            print(f"[OK] Loaded {len(product_ids)} catalog IDs (TEST MODE: limited to first {TEST_LIMIT})")
        else:
            print(f"[OK] Loaded {len(product_ids)} catalog IDs")

    except FileNotFoundError:
        print(f"[ERROR] File '{INPUT_CSV}' not found!")
        return
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        return

    print()
    print("Configuration:")
    print(f"  - Test mode: {'ENABLED (first ' + str(TEST_LIMIT) + ' IDs)' if TEST_MODE else 'DISABLED (all IDs)'}")
    print(f"  - Max concurrent workers: {MAX_WORKERS}")
    print(f"  - Timeout per request: {TIMEOUT}s")
    print(f"  - Base URL: {BASE_URL}")
    print()

    # Estimate time
    estimated_time = (len(product_ids) / MAX_WORKERS) * 1.5  # Rough estimate
    estimated_minutes = int(estimated_time / 60)
    print(f"Estimated completion time: ~{estimated_minutes} minutes")
    print()

    print("=" * 70)
    print("Starting validation...")
    print("=" * 70)

    results = []
    valid_count = 0
    invalid_count = 0
    error_count = 0
    start_time = time.time()

    # Use ThreadPoolExecutor for concurrent validation
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_id = {executor.submit(check_product_id, pid): pid for pid in product_ids}

        # Process results as they complete
        count = 0
        for future in concurrent.futures.as_completed(future_to_id):
            count += 1
            pid, status, response_time = future.result()
            results.append((pid, status, response_time))

            # Update statistics
            if status == "Valid":
                valid_count += 1
            elif "Invalid" in status or "404" in status:
                invalid_count += 1
            else:
                error_count += 1

            # Progress reporting
            if count % PROGRESS_INTERVAL == 0 or count == len(product_ids):
                elapsed = time.time() - start_time
                rate = count / elapsed if elapsed > 0 else 0
                remaining = (len(product_ids) - count) / rate if rate > 0 else 0

                print(f"Progress: {count}/{len(product_ids)} ({count*100//len(product_ids)}%) | "
                      f"Valid: {valid_count} | Invalid: {invalid_count} | Errors: {error_count} | "
                      f"Rate: {rate:.1f}/s | ETA: {int(remaining/60)}m {int(remaining%60)}s")

    # Calculate final statistics
    total_time = time.time() - start_time
    avg_time = total_time / len(product_ids)

    print()
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total Processed:    {len(product_ids)}")
    print(f"Valid Products:     {valid_count} ({valid_count*100//len(product_ids)}%)")
    print(f"Invalid Products:   {invalid_count} ({invalid_count*100//len(product_ids)}%)")
    print(f"Errors/Timeouts:    {error_count} ({error_count*100//len(product_ids)}%)")
    print(f"Total Time:         {int(total_time//60)}m {int(total_time%60)}s")
    print(f"Average Time/ID:    {avg_time:.2f}s")
    print(f"Throughput:         {len(product_ids)/total_time:.1f} IDs/second")
    print("=" * 70)
    print()

    # Save results to CSV
    print(f"Saving results to: {OUTPUT_CSV}")
    results_df = pd.DataFrame(results, columns=['ProductID', 'Status', 'ResponseTime_s'])
    results_df.to_csv(OUTPUT_CSV, index=False)
    print(f"[OK] Results saved successfully!")

    print()
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == '__main__':
    main()
