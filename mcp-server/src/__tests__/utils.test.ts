/**
 * Unit tests for MCP server utility functions
 */

import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";
import {
  parseCSV,
  searchSiteStructure,
  getPageByUrl,
  getBrandRulesSection,
  getTemplateInfo,
  createFeedback,
  generateFeedbackFilename,
  BRAND_RULES,
  TEMPLATES,
} from "../utils.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load test fixture
const fixtureCSV = fs.readFileSync(
  path.join(__dirname, "fixtures", "sample-site-structure.csv"),
  "utf-8"
);

describe("parseCSV", () => {
  it("should parse CSV content into array of objects", () => {
    const result = parseCSV(fixtureCSV);
    expect(Array.isArray(result)).toBe(true);
    expect(result.length).toBeGreaterThan(0);
  });

  it("should have correct column headers as keys", () => {
    const result = parseCSV(fixtureCSV);
    const firstRow = result[0];
    expect(firstRow).toHaveProperty("Page Name");
    expect(firstRow).toHaveProperty("Full URL");
    expect(firstRow).toHaveProperty("Writer");
    expect(firstRow).toHaveProperty("Target Keywords");
  });

  it("should handle empty CSV content", () => {
    const emptyCSV = "Level 1,Page Name,Full URL\n";
    const result = parseCSV(emptyCSV);
    expect(Array.isArray(result)).toBe(true);
    expect(result.length).toBe(0);
  });

  it("should handle CSV with BOM marker", () => {
    const bomCSV = "\ufeffLevel 1,Page Name\nHomepage,Test Page";
    const result = parseCSV(bomCSV);
    expect(result[0]).toHaveProperty("Level 1");
    expect(result[0]["Level 1"]).toBe("Homepage");
  });
});

describe("searchSiteStructure", () => {
  let testData: any[];

  beforeAll(() => {
    testData = parseCSV(fixtureCSV);
  });

  it("should find results matching page name", () => {
    const results = searchSiteStructure(testData, "FanDuel");
    expect(results.length).toBeGreaterThan(0);
    expect(results[0]["Page Name"]).toContain("FanDuel");
  });

  it("should be case-insensitive", () => {
    const lowerResults = searchSiteStructure(testData, "fanduel");
    const upperResults = searchSiteStructure(testData, "FANDUEL");
    const mixedResults = searchSiteStructure(testData, "FanDuel");

    expect(lowerResults.length).toBe(upperResults.length);
    expect(lowerResults.length).toBe(mixedResults.length);
  });

  it("should find results matching target keywords", () => {
    const results = searchSiteStructure(testData, "sportsbook bonuses");
    expect(results.length).toBeGreaterThan(0);
  });

  it("should find results matching URL", () => {
    const results = searchSiteStructure(testData, "best-apps.htm");
    expect(results.length).toBeGreaterThan(0);
  });

  it("should find results matching Level columns", () => {
    const results = searchSiteStructure(testData, "Comparison Pages");
    expect(results.length).toBeGreaterThan(0);
  });

  it("should return empty array for no matches", () => {
    const results = searchSiteStructure(testData, "nonexistent-xyz-page");
    expect(results).toEqual([]);
  });

  it("should handle empty query", () => {
    const results = searchSiteStructure(testData, "");
    expect(results.length).toBe(testData.length); // Empty string matches all
  });

  it("should handle partial matches", () => {
    const results = searchSiteStructure(testData, "Review");
    expect(results.length).toBeGreaterThan(1); // Multiple reviews
  });

  it("should handle special characters in query", () => {
    const results = searchSiteStructure(testData, "2025");
    expect(results.length).toBeGreaterThan(0);
  });
});

describe("getPageByUrl", () => {
  let testData: any[];

  beforeAll(() => {
    testData = parseCSV(fixtureCSV);
  });

  it("should find page by exact URL", () => {
    const result = getPageByUrl(testData, "https://www.example.com/betting/fanduel-review.htm");
    expect(result).not.toBeNull();
    expect(result["Page Name"]).toBe("FanDuel Sportsbook Review");
  });

  it("should return null for non-existent URL", () => {
    const result = getPageByUrl(testData, "https://www.example.com/nonexistent");
    expect(result).toBeNull();
  });

  it("should not match partial URLs", () => {
    const result = getPageByUrl(testData, "fanduel-review.htm");
    expect(result).toBeNull();
  });

  it("should return null for empty URL", () => {
    const result = getPageByUrl(testData, "");
    expect(result).toBeNull();
  });
});

describe("BRAND_RULES", () => {
  it("should have locked positions defined", () => {
    expect(BRAND_RULES.locked_positions).toBeDefined();
    expect(BRAND_RULES.locked_positions.position_1.brand).toBe("FanDuel");
    expect(BRAND_RULES.locked_positions.position_2.brand).toBe("BetMGM");
  });

  it("should have tier arrays with brands", () => {
    expect(BRAND_RULES.tier_1_brands).toContain("FanDuel");
    expect(BRAND_RULES.tier_1_brands).toContain("BetMGM");
    expect(BRAND_RULES.tier_1_brands).toContain("DraftKings");
    expect(BRAND_RULES.tier_2_brands.length).toBeGreaterThan(0);
    expect(BRAND_RULES.tier_3_brands.length).toBeGreaterThan(0);
  });

  it("should have brand guidelines for tier 1 brands", () => {
    expect(BRAND_RULES.brand_guidelines.FanDuel).toBeDefined();
    expect(BRAND_RULES.brand_guidelines.FanDuel.usp).toBeDefined();
    expect(BRAND_RULES.brand_guidelines.FanDuel.key_features).toBeInstanceOf(Array);
  });

  it("should have compliance rules", () => {
    expect(BRAND_RULES.compliance_rules.age_requirement_default).toBe("21+");
    expect(BRAND_RULES.compliance_rules.gambling_hotline).toBeDefined();
    expect(BRAND_RULES.compliance_rules.forbidden_language).toBeInstanceOf(Array);
  });

  it("should have writer assignments", () => {
    expect(BRAND_RULES.writer_assignments["Lewis Humphries"]).toBeDefined();
    expect(BRAND_RULES.writer_assignments["Tom Goldsmith"]).toBeDefined();
  });
});

describe("getBrandRulesSection", () => {
  it("should return locked_positions section", () => {
    const result = getBrandRulesSection("locked_positions");
    expect(result).toEqual(BRAND_RULES.locked_positions);
  });

  it("should return tiers section with correct structure", () => {
    const result = getBrandRulesSection("tiers");
    expect(result.tier_1).toEqual(BRAND_RULES.tier_1_brands);
    expect(result.tier_2).toEqual(BRAND_RULES.tier_2_brands);
    expect(result.tier_3).toEqual(BRAND_RULES.tier_3_brands);
  });

  it("should return guidelines section", () => {
    const result = getBrandRulesSection("guidelines");
    expect(result).toEqual(BRAND_RULES.brand_guidelines);
  });

  it("should return compliance section", () => {
    const result = getBrandRulesSection("compliance");
    expect(result).toEqual(BRAND_RULES.compliance_rules);
  });

  it("should return writers section", () => {
    const result = getBrandRulesSection("writers");
    expect(result).toEqual(BRAND_RULES.writer_assignments);
  });

  it("should return all brand rules for unknown section", () => {
    const result = getBrandRulesSection("all");
    expect(result).toEqual(BRAND_RULES);
  });

  it("should return all brand rules for invalid section", () => {
    const result = getBrandRulesSection("invalid-section");
    expect(result).toEqual(BRAND_RULES);
  });
});

describe("TEMPLATES", () => {
  it("should have 4 templates defined", () => {
    expect(Object.keys(TEMPLATES).length).toBe(4);
  });

  it("should have Review template at position 1", () => {
    expect(TEMPLATES[1].name).toBe("Review Template");
    expect(TEMPLATES[1].structure).toBeInstanceOf(Array);
    expect(TEMPLATES[1].required_elements).toBeInstanceOf(Array);
  });

  it("should have Comparison template at position 2", () => {
    expect(TEMPLATES[2].name).toBe("Comparison Template");
  });

  it("should have How-To template at position 3", () => {
    expect(TEMPLATES[3].name).toBe("How-To Template");
  });

  it("should have State Page template at position 4", () => {
    expect(TEMPLATES[4].name).toBe("State Page Template");
  });
});

describe("getTemplateInfo", () => {
  it("should return specific template by number", () => {
    const result = getTemplateInfo(1);
    expect(result.name).toBe("Review Template");
  });

  it("should return all templates when no number provided", () => {
    const result = getTemplateInfo();
    expect(result).toEqual(TEMPLATES);
  });

  it("should return error for invalid template number", () => {
    const result = getTemplateInfo(99);
    expect(result.error).toBe("Invalid template number");
  });

  it("should return error for template number 0", () => {
    const result = getTemplateInfo(0);
    expect(result.error).toBe("Invalid template number");
  });
});

describe("createFeedback", () => {
  it("should create feedback object with required fields", () => {
    const feedback = createFeedback("Test Page", 4, "John Doe");

    expect(feedback.page_name).toBe("Test Page");
    expect(feedback.rating).toBe(4);
    expect(feedback.submitter).toBe("John Doe");
    expect(feedback.status).toBe("submitted");
    expect(feedback.submitted_at).toBeDefined();
  });

  it("should include optional issues array", () => {
    const issues = ["Issue 1", "Issue 2"];
    const feedback = createFeedback("Test Page", 3, "Jane Doe", issues);

    expect(feedback.issues).toEqual(issues);
  });

  it("should include optional improvements array", () => {
    const improvements = ["Improvement 1"];
    const feedback = createFeedback("Test Page", 5, "Jane Doe", undefined, improvements);

    expect(feedback.improvements).toEqual(improvements);
  });

  it("should default issues and improvements to empty arrays", () => {
    const feedback = createFeedback("Test Page", 4, "John Doe");

    expect(feedback.issues).toEqual([]);
    expect(feedback.improvements).toEqual([]);
  });

  it("should have valid ISO timestamp", () => {
    const feedback = createFeedback("Test Page", 4, "John Doe");
    const timestamp = new Date(feedback.submitted_at);

    expect(timestamp instanceof Date).toBe(true);
    expect(isNaN(timestamp.getTime())).toBe(false);
  });
});

describe("generateFeedbackFilename", () => {
  it("should generate filename with slugified page name", () => {
    const filename = generateFeedbackFilename("Test Page Name");
    expect(filename).toMatch(/^test-page-name-/);
  });

  it("should include timestamp in filename", () => {
    const filename = generateFeedbackFilename("Test");
    expect(filename).toMatch(/\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}/);
  });

  it("should end with .json extension", () => {
    const filename = generateFeedbackFilename("Test");
    expect(filename).toMatch(/\.json$/);
  });

  it("should handle multiple spaces", () => {
    const filename = generateFeedbackFilename("Test   Multiple   Spaces");
    expect(filename).toMatch(/^test-multiple-spaces-/);
  });

  it("should convert to lowercase", () => {
    const filename = generateFeedbackFilename("UPPERCASE PAGE");
    expect(filename).toMatch(/^uppercase-page-/);
  });
});
