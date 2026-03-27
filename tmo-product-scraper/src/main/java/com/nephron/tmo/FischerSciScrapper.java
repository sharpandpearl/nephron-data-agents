package com.nephron.tmo;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.ElementHandle;
import com.microsoft.playwright.Page;
import com.microsoft.playwright.Playwright;

public class FischerSciScrapper {

	static Browser browser = null;
	static Page page = null;
	static String CSV_FILE_PATH = "data/source/TMO_Product_list_Valid_Only.csv";
	static String OUTPUT_CSV_FILE = "data/output/playwright_scrape_results.csv";
	static int START_INDEX = 0;      // Start at first product (0-based index)
	static int END_INDEX = 25;       // Test on first 25 products

	public static void main(String[] args) {

		System.out.println("Starting Fisher Scientific Playwright scraper...");

		// Load catalog numbers from CSV
		ArrayList<String> catalogNumbers = loadCatalogNumbersFromCSV();

		if (catalogNumbers.isEmpty()) {
			System.err.println("No catalog numbers to scrape. Check your START_INDEX and END_INDEX configuration.");
			System.exit(1);
		}

		System.out.println("Loaded " + catalogNumbers.size() + " catalog numbers to scrape");
		System.out.println("First catalog: " + catalogNumbers.get(0));
		System.out.println("Last catalog: " + catalogNumbers.get(catalogNumbers.size() - 1));

		// Initialize Playwright
		Playwright playwright = Playwright.create();

		try {
			// Launch browser in headless mode
			browser = launchBrowser(playwright, true);
			page = browser.newPage();

			ArrayList<FischerSciProduct> myProducts = scrapeFischerSciPricesFromList(page, catalogNumbers);

			// Save to CSV file
			try {
				saveToCsvFile(myProducts, OUTPUT_CSV_FILE);
				System.out.println("\n[OK] Results saved to: " + OUTPUT_CSV_FILE);
			} catch (IOException e) {
				System.err.println("Error saving results to file: " + e.getMessage());
				e.printStackTrace();
			}

		} finally {
			if (page != null) {
				page.close();
			}
			if (browser != null) {
				browser.close();
			}
			if (playwright != null) {
				playwright.close();
			}
			System.out.println("\nBrowser closed successfully.");
		}
	}

	/**
	 * Launch browser with Playwright
	 */
	public static Browser launchBrowser(Playwright playwright, boolean headless) {
		BrowserType.LaunchOptions options = new BrowserType.LaunchOptions()
			.setHeadless(headless)
			.setArgs(List.of(
				"--disable-blink-features=AutomationControlled",
				"--no-sandbox",
				"--disable-dev-shm-usage"
			));

		System.out.println("Launching browser in " + (headless ? "headless" : "headed") + " mode...");
		return playwright.chromium().launch(options);
	}

	/**
	 * Load catalog numbers from CSV file
	 */
	public static ArrayList<String> loadCatalogNumbersFromCSV() {
		ArrayList<String> catalogNumbers = new ArrayList<>();

		try {
			// Resolve the CSV file path - handle both Maven and IDE execution
			String currentDir = System.getProperty("user.dir");
			String csvPath;

			// If running from tmo-product-scraper directory (Maven)
			if (currentDir.endsWith("tmo-product-scraper")) {
				csvPath = Paths.get(currentDir, CSV_FILE_PATH).toString();
			} else {
				// If running from project root (IDE/VSCode)
				csvPath = Paths.get(currentDir, "tmo-product-scraper", CSV_FILE_PATH).toString();
			}

			System.out.println("Current directory: " + currentDir);
			System.out.println("Reading CSV file from: " + csvPath);

			BufferedReader reader = new BufferedReader(new FileReader(csvPath));
			String line;
			ArrayList<String> allLines = new ArrayList<>();

			// Read all lines
			while ((line = reader.readLine()) != null) {
				line = line.trim();
				if (!line.isEmpty()) {
					allLines.add(line);
				}
			}
			reader.close();

			if (allLines.isEmpty()) {
				System.err.println("CSV file is empty");
				return catalogNumbers;
			}

			// Check if first line is a header
			String firstLine = allLines.get(0);
			boolean hasHeader = firstLine.toLowerCase().contains("catalog") ||
			                   firstLine.toLowerCase().contains("valid") ||
			                   !Character.isDigit(firstLine.charAt(0));

			int startLine = hasHeader ? 1 : 0;

			// Extract first column from each line
			for (int i = startLine; i < allLines.size(); i++) {
				String dataLine = allLines.get(i);
				String catalogId;

				if (dataLine.contains(",")) {
					// Extract first column
					catalogId = dataLine.split(",")[0].trim();
				} else {
					catalogId = dataLine.trim();
				}

				if (!catalogId.isEmpty()) {
					catalogNumbers.add(catalogId);
				}
			}

			// Apply range filtering
			ArrayList<String> selectedCatalogs = new ArrayList<>();
			int endIdx = (END_INDEX == -1) ? catalogNumbers.size() : Math.min(END_INDEX, catalogNumbers.size());

			for (int i = START_INDEX; i < endIdx; i++) {
				selectedCatalogs.add(catalogNumbers.get(i));
			}

			System.out.println("\n" + "=".repeat(70));
			System.out.println("CSV FILE CONFIGURATION");
			System.out.println("=".repeat(70));
			System.out.println("CSV File:            " + csvPath);
			System.out.println("Total in CSV:        " + catalogNumbers.size() + " catalog numbers");
			System.out.println("Start Index:         " + START_INDEX);
			System.out.println("End Index:           " + (END_INDEX == -1 ? "END OF FILE" : END_INDEX));
			System.out.println("Selected Range:      " + selectedCatalogs.size() + " catalog numbers");
			System.out.println("=".repeat(70));

			return selectedCatalogs;

		} catch (IOException e) {
			System.err.println("Error reading CSV file: " + e.getMessage());
			e.printStackTrace();
			return catalogNumbers;
		}
	}

	/**
	 * Scrape products from a list of catalog numbers using Playwright
	 */
	public static ArrayList<FischerSciProduct> scrapeFischerSciPricesFromList(Page page, ArrayList<String> catalogNumbers) {
		ArrayList<FischerSciProduct> fischerSciProductList = new ArrayList<FischerSciProduct>();

		long startTime = System.currentTimeMillis();

		for(int idx = 0; idx < catalogNumbers.size(); idx++) {
			String catalogNum = catalogNumbers.get(idx);
			int progress = idx + 1;
			int total = catalogNumbers.size();

			try {
				System.out.println("\n>>> Progress: " + progress + "/" + total + " (" +
				                 Math.round((progress * 100.0) / total) + "%)");
				System.out.println("Processing catalog number: " + catalogNum);

				// Navigate directly to search results URL
				String searchUrl = "https://www.fishersci.com/us/en/catalog/search/products?keyword=" + catalogNum;
				page.navigate(searchUrl);

				// Wait for page to load (Playwright auto-waits, but adding explicit wait for JS execution)
				page.waitForTimeout(1000);

				// Try multiple possible selectors for product title
				String itemName = "";
				try {
					// Try h1 tags first (common for product titles)
					List<ElementHandle> h1Elements = page.querySelectorAll("h1");
					if (!h1Elements.isEmpty()) {
						itemName = h1Elements.get(0).textContent();
					}

					// Fallback: try common product title selectors
					if (itemName.isEmpty()) {
						ElementHandle titleElement = page.querySelector("h1[class*='product'], h1[class*='title'], [data-testid*='title']");
						if (titleElement != null) {
							itemName = titleElement.textContent();
						}
					}
				} catch (Exception e) {
					System.out.println("Could not find product title for catalog #" + catalogNum);
					itemName = "Product Not Found";
				}

				// Try to extract price
				String price = "0.0";

				try {
					// First attempt: Try multiple price selectors
					String[] priceSelectors = {
						"[class*='price']",
						"[data-testid*='price']",
						".product-price",
						"[class*='Price']",
						"span[class*='amount']"
					};

					for (String selector : priceSelectors) {
						try {
							List<ElementHandle> elements = page.querySelectorAll(selector);

							for (ElementHandle priceElement : elements) {
								if (priceElement != null && priceElement.isVisible()) {
									String priceText = priceElement.textContent();

									// Use regex to extract price: $?\s*(\d+[,.]?\d*\.?\d{0,2})
									java.util.regex.Pattern pattern = java.util.regex.Pattern.compile("\\$?\\s*(\\d+[,.]?\\d*\\.?\\d{0,2})");
									java.util.regex.Matcher matcher = pattern.matcher(priceText);

									if (matcher.find()) {
										String extractedPrice = matcher.group(1).replace(",", "");
										if (!extractedPrice.isEmpty() && !extractedPrice.equals("0") && !extractedPrice.equals("0.0")) {
											price = extractedPrice;
											break; // Found valid price, stop searching
										}
									}
								}
							}
							if (!price.equals("0.0")) {
								break; // Found valid price in this selector, stop trying other selectors
							}
						} catch (Exception e) {
							// Try next selector
							continue;
						}
					}

					// If no price found, check if login is required
					if (price.equals("0.0")) {
						String pageContent = page.content();
						if (pageContent.contains("Sign In to purchase") ||
							pageContent.contains("view availability") ||
							pageContent.contains("Sign In or Register to check")) {
							System.out.println("Login required to view pricing for catalog #" + catalogNum);
							price = "LOGIN_REQUIRED";
						}
					}
				} catch (Exception e) {
					System.out.println("Could not extract price for catalog #" + catalogNum + ": " + e.getMessage());
				}

				System.out.println("Product Name: " + itemName);
				System.out.println("Price: " + price);

				FischerSciProduct scrapedProduct = new FischerSciProduct();
				scrapedProduct.setProductCatalogNo(catalogNum);
				scrapedProduct.setProductName(itemName);
				scrapedProduct.setScrapeDate(getCurrentUTCDate() + "Z");
				scrapedProduct.setProductPrice(price);

				fischerSciProductList.add(scrapedProduct);

				// Small delay between requests
				if (idx < catalogNumbers.size() - 1) {
					System.out.println("Waiting 2 seconds before next request...");
					page.waitForTimeout(2000);
				}

			} catch (Exception e) {
				System.out.println("Error processing catalog #" + catalogNum + ": " + e.getMessage());
				e.printStackTrace();

				// Add failed entry
				FischerSciProduct errorProduct = new FischerSciProduct();
				errorProduct.setProductCatalogNo(catalogNum);
				errorProduct.setProductName("ERROR: " + e.getMessage());
				errorProduct.setScrapeDate(getCurrentUTCDate() + "Z");
				errorProduct.setProductPrice("0.0");
				fischerSciProductList.add(errorProduct);
			}
		}

		long endTime = System.currentTimeMillis();
		double duration = (endTime - startTime) / 1000.0;

		System.out.println("\n" + "=".repeat(70));
		System.out.println("SCRAPING SUMMARY");
		System.out.println("=".repeat(70));
		System.out.println("Total Processed:     " + fischerSciProductList.size());
		System.out.println("Duration:            " + String.format("%.2f", duration) + " seconds");
		System.out.println("Average Time/Product: " + String.format("%.2f", duration / fischerSciProductList.size()) + " seconds");
		System.out.println("=".repeat(70));

		return fischerSciProductList;
	}

	/**
	 * Save products to CSV file
	 */
	public static void saveToCsvFile(ArrayList<FischerSciProduct> products, String filePath) throws IOException {
		// Resolve the output file path - handle both Maven and IDE execution
		String currentDir = System.getProperty("user.dir");
		String fullPath;

		// If running from tmo-product-scraper directory (Maven)
		if (currentDir.endsWith("tmo-product-scraper")) {
			fullPath = Paths.get(currentDir, filePath).toString();
		} else {
			// If running from project root (IDE/VSCode)
			fullPath = Paths.get(currentDir, "tmo-product-scraper", filePath).toString();
		}

		FileWriter fileWriter = new FileWriter(fullPath);

		// Write CSV header
		fileWriter.write("CatalogNo,ProductName,Price,ScrapeDate\n");

		// Write each product as a CSV row
		for (FischerSciProduct product : products) {
			String catalogNo = escapeCsvField(product.getProductCatalogNo());
			String productName = escapeCsvField(product.getProductName().trim());
			String price = escapeCsvField(product.getProductPrice());
			String scrapeDate = escapeCsvField(product.getScrapeDate());

			fileWriter.write(String.format("%s,%s,%s,%s\n", catalogNo, productName, price, scrapeDate));
		}

		fileWriter.close();
		System.out.println("CSV output saved to: " + fullPath);
	}

	/**
	 * Escape CSV field - wrap in quotes if contains comma, quote, or newline
	 */
	private static String escapeCsvField(String field) {
		if (field == null) {
			return "";
		}

		// If field contains comma, quote, or newline, wrap in quotes and escape existing quotes
		if (field.contains(",") || field.contains("\"") || field.contains("\n")) {
			return "\"" + field.replace("\"", "\"\"") + "\"";
		}

		return field;
	}

	public static String getCurrentUTCDate() {

		DateTimeFormatter FOMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss");
		ZonedDateTime nowInLocalTimeZone = ZonedDateTime.now();
		ZonedDateTime nowInNYC = nowInLocalTimeZone.withZoneSameInstant(ZoneId.of("UTC"));

		return nowInNYC.format(FOMATTER);
	}

}
