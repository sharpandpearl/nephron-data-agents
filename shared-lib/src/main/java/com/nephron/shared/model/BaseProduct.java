package com.nephron.shared.model;

/**
 * Base class for product data models.
 * Provides common fields shared across all scraped products.
 */
public abstract class BaseProduct {

    protected String catalogNumber;
    protected String productName;
    protected String price;
    protected String scrapeDate;

    public BaseProduct() {
    }

    public String getCatalogNumber() {
        return catalogNumber;
    }

    public void setCatalogNumber(String catalogNumber) {
        this.catalogNumber = catalogNumber;
    }

    public String getProductName() {
        return productName;
    }

    public void setProductName(String productName) {
        this.productName = productName;
    }

    public String getPrice() {
        return price;
    }

    public void setPrice(String price) {
        this.price = price;
    }

    public String getScrapeDate() {
        return scrapeDate;
    }

    public void setScrapeDate(String scrapeDate) {
        this.scrapeDate = scrapeDate;
    }
}
