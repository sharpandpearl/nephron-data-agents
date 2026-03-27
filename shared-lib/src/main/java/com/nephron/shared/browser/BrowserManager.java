package com.nephron.shared.browser;

import com.microsoft.playwright.Browser;
import com.microsoft.playwright.BrowserType;
import com.microsoft.playwright.Playwright;
import java.util.List;

/**
 * Manages Playwright browser instances for scrapers.
 * Provides common browser configuration and setup.
 */
public class BrowserManager {

    /**
     * Launch a Playwright browser with standard configuration.
     *
     * @param playwright Playwright instance
     * @param headless   Run in headless mode
     * @return Configured Browser instance
     */
    public static Browser launchBrowser(Playwright playwright, boolean headless) {
        BrowserType.LaunchOptions options = new BrowserType.LaunchOptions()
                .setHeadless(headless)
                .setArgs(List.of(
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-dev-shm-usage"
                ));

        return playwright.chromium().launch(options);
    }
}
