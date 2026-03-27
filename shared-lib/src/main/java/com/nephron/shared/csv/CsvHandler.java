package com.nephron.shared.csv;

/**
 * Utility class for CSV file operations.
 * Provides common CSV formatting and escaping functions.
 */
public class CsvHandler {

    /**
     * Escape a CSV field by wrapping in quotes if necessary.
     * Handles fields containing commas, quotes, or newlines.
     *
     * @param field The field to escape
     * @return Escaped field ready for CSV output
     */
    public static String escapeCsvField(String field) {
        if (field == null) {
            return "";
        }

        // If field contains comma, quote, or newline, wrap in quotes and escape existing quotes
        if (field.contains(",") || field.contains("\"") || field.contains("\n")) {
            return "\"" + field.replace("\"", "\"\"") + "\"";
        }

        return field;
    }
}
