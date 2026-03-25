/**
 *
 */
package nephrontools;

/**
 * @author andri
 *
 */
public class FischerSciProduct {

	String Product_CatalogNo = "";
	String Product_Name = "";
	String Product_Price = "";
	String Product_ScrapeDate ="";


	public FischerSciProduct() {
	}

	public FischerSciProduct(String d, String pName, String pCatalogNo, String pDate) {
		Product_CatalogNo = pCatalogNo;
		Product_Name = pName;
		Product_Price = d;
		Product_ScrapeDate = pDate;
		// TODO Auto-generated constructor stub
	}

	public String getProductPrice() {
		return Product_Price;
	}

	public void setProductPrice(String productPrice) {
		Product_Price = productPrice;
	}

	public String getProductName() {
		return Product_Name;
	}

	public void setProductName(String productName) {
		Product_Name = productName;
	}

	public String getProductCatalogNo() {
		return Product_CatalogNo;
	}

	public void setProductCatalogNo(String productID) {
		Product_CatalogNo = productID;
	}

	public String getScrapeDate() {
		return Product_ScrapeDate;
	}

	public void setScrapeDate(String scrapeDate) {
		Product_ScrapeDate = scrapeDate;
	}
}
