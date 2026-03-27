package com.nephron.shared.util;

import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

/**
 * Utility class for date and time operations.
 * Provides standardized date formatting across scrapers.
 */
public class DateUtils {

    private static final DateTimeFormatter ISO_FORMATTER = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss");

    /**
     * Get current UTC timestamp in ISO format.
     *
     * @return Current UTC timestamp (e.g., "2026-03-26T14:30:00")
     */
    public static String getCurrentUTCDate() {
        ZonedDateTime nowInLocalTimeZone = ZonedDateTime.now();
        ZonedDateTime nowInUTC = nowInLocalTimeZone.withZoneSameInstant(ZoneId.of("UTC"));
        return nowInUTC.format(ISO_FORMATTER);
    }

    /**
     * Get current UTC timestamp in ISO format with 'Z' suffix.
     *
     * @return Current UTC timestamp with Z suffix (e.g., "2026-03-26T14:30:00Z")
     */
    public static String getCurrentUTCDateWithZ() {
        return getCurrentUTCDate() + "Z";
    }
}
