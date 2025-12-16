/**
 * Utility functions for TopEndSports Content Briefs MCP Server
 * Extracted for testability
 */

import * as fs from "fs";
import * as path from "path";
import { parse } from "csv-parse/sync";

// Brand rules - locked positions and tier information
export const BRAND_RULES = {
  locked_positions: {
    position_1: {
      brand: "FanDuel",
      status: "LOCKED",
      rationale: "Active commercial deal - must always appear first"
    },
    position_2: {
      brand: "BetMGM",
      status: "LOCKED",
      rationale: "Active commercial deal - must always appear second"
    }
  },
  tier_1_brands: ["FanDuel", "BetMGM", "DraftKings", "Caesars", "bet365"],
  tier_2_brands: ["Fanatics", "theScore BET", "BetRivers", "Bally Bet", "BetParx"],
  tier_3_brands: ["Golden Nugget", "Unibet", "Borgata", "Betfred", "WynnBet", "SI Sportsbook"],
  brand_guidelines: {
    FanDuel: {
      usp: "Best Overall User Experience",
      key_features: ["4.9/5 App Store rating", "SGP builder", "40+ player props"],
      typical_position: 1
    },
    BetMGM: {
      usp: "Best Loyalty Rewards",
      key_features: ["MGM Rewards integration", "Up to $1,500 bonus", "2-hour payouts"],
      typical_position: 2
    },
    DraftKings: {
      usp: "Best for Props Variety",
      key_features: ["29.9% best underdog prices", "Flash Betting", "Props by category"],
      typical_position: 3
    },
    Caesars: {
      usp: "Best for Odds Boosts",
      key_features: ["Best spread favorites", "Live streaming", "VIP rewards"],
      typical_position: 4
    },
    bet365: {
      usp: "Best for Live Betting",
      key_features: ["Sharpest lines", "40+ props", "International reputation"],
      typical_position: 5
    },
    Fanatics: {
      usp: "Best for Rewards Integration",
      key_features: ["FanCash rewards", "Merchandise crossover", "Strong app experience"],
      typical_position: 6,
      badge_code: "FAN",
      badge_color: "#0050c8"
    },
    "theScore BET": {
      usp: "Best for Media Integration",
      key_features: ["theScore app integration", "Penn Play rewards", "Beginner friendly"],
      typical_position: 7,
      badge_code: "SCR",
      badge_color: "#6B2D5B",
      notes: "Formerly ESPN BET - rebranded December 2025"
    }
  },
  compliance_rules: {
    age_requirement_default: "21+",
    age_requirement_exceptions: ["MT", "NH", "RI", "WY", "DC"],
    gambling_hotline: "1-800-522-4700",
    affiliate_disclosure_required: true,
    responsible_gambling_section_required: true,
    forbidden_language: [
      "Guaranteed wins",
      "Can't lose",
      "Risk-free",
      "Beat the house"
    ]
  },
  writer_assignments: {
    "Lewis Humphries": {
      priority: ["Critical", "High"],
      content_types: ["Reviews", "Comparisons", "State Pages", "Promo Codes"]
    },
    "Tom Goldsmith": {
      priority: ["High", "Medium", "Low"],
      content_types: ["How-tos", "Explainers", "Secondary Reviews"]
    },
    "Gustavo Cantella": {
      priority: ["All"],
      content_types: ["All Spanish content (/es/ URLs)"],
      special_rules: ["21+ required", "USA-focused content"]
    }
  }
};

// Template definitions
export const TEMPLATES: Record<number, any> = {
  1: {
    name: "Review Template",
    description: "Individual sportsbook/product review page",
    typical_word_count: "2,500-3,500",
    structure: [
      "H1: [Brand] Review",
      "Quick Facts Box",
      "Pros & Cons",
      "Welcome Bonus Details",
      "Features Deep Dive",
      "Mobile App Review",
      "Payment Methods",
      "Customer Support",
      "Complete T&Cs",
      "FAQ (5-7 questions)",
      "Responsible Gambling"
    ],
    required_elements: [
      "App Store rating citation",
      "Complete T&Cs section",
      "5+ FAQs with schema"
    ]
  },
  2: {
    name: "Comparison Template",
    description: "Multi-brand comparison page (e.g., 'Best NFL Betting Sites')",
    typical_word_count: "3,000-4,000",
    structure: [
      "H1: Best [Topic]",
      "Comparison Table (sortable/filterable)",
      "Quick Winner Summaries",
      "Individual Brand Sections (300-500 words each)",
      "Feature-Specific Sections (props, live betting, etc.)",
      "How to [Topic] Guide",
      "Complete T&Cs for ALL brands",
      "FAQ (7+ questions)",
      "Responsible Gambling"
    ],
    required_elements: [
      "7+ brands compared",
      "Sortable comparison table",
      "Complete T&Cs for each brand",
      "7+ FAQs with schema"
    ]
  },
  3: {
    name: "How-To Template",
    description: "Educational/explanatory content",
    typical_word_count: "2,000-2,500",
    structure: [
      "H1: How to [Topic]",
      "Quick Answer Box",
      "Step-by-Step Guide",
      "Examples/Use Cases",
      "Tips & Strategies",
      "Common Mistakes",
      "Related Resources",
      "FAQ (5-7 questions)"
    ],
    required_elements: [
      "Step-by-step instructions",
      "Practical examples",
      "5+ FAQs with schema"
    ]
  },
  4: {
    name: "State Page Template",
    description: "State-specific legal sports betting guide",
    typical_word_count: "2,500-3,000",
    structure: [
      "H1: Sports Betting in [State]",
      "Legal Status Summary",
      "Available Sportsbooks Table",
      "State-Specific Regulations",
      "Taxes & Reporting",
      "Individual Sportsbook Sections",
      "How to Sign Up in [State]",
      "FAQ (5-7 state-specific questions)",
      "Responsible Gambling"
    ],
    required_elements: [
      "Current legal status",
      "State-specific age requirement",
      "Available sportsbooks list",
      "5+ FAQs with schema"
    ]
  }
};

/**
 * Find the project root by looking for content-briefs-skill directory
 */
export const findProjectRoot = (startDir?: string): string => {
  const currentDir = startDir || process.cwd();

  const possiblePaths = [
    currentDir,
    path.dirname(currentDir),
    path.join(currentDir, ".."),
    "/home/user/topendsports-content-briefs"
  ];

  for (const p of possiblePaths) {
    if (fs.existsSync(path.join(p, "content-briefs-skill"))) {
      return p;
    }
  }

  return currentDir;
};

/**
 * Parse CSV content into structured data
 */
export const parseCSV = (content: string): any[] => {
  return parse(content, {
    columns: true,
    skip_empty_lines: true,
    bom: true
  });
};

/**
 * Load CSV data from file
 */
export const loadCSVFile = (filePath: string): any[] => {
  if (!fs.existsSync(filePath)) {
    return [];
  }
  const content = fs.readFileSync(filePath, "utf-8");
  return parseCSV(content);
};

/**
 * Search site structure data
 */
export const searchSiteStructure = (
  data: any[],
  query: string
): any[] => {
  const queryLower = query.toLowerCase();

  return data.filter(row => {
    const searchFields = [
      row["Page Name"],
      row["Target Keywords"],
      row["Full URL"],
      row["Level 1"],
      row["Level 2"],
      row["Level 3"],
      row["Level 4"]
    ];

    return searchFields.some(field =>
      field && field.toLowerCase().includes(queryLower)
    );
  });
};

/**
 * Get page by exact URL
 */
export const getPageByUrl = (data: any[], url: string): any | null => {
  return data.find(row => row["Full URL"] === url) || null;
};

/**
 * List briefs in a directory
 */
export const listBriefs = (directory: string): any[] => {
  if (!fs.existsSync(directory)) {
    return [];
  }

  const files = fs.readdirSync(directory);
  return files.map(file => {
    const filePath = path.join(directory, file);
    const stats = fs.statSync(filePath);
    const ext = path.extname(file);

    let content = null;
    if (ext === ".json") {
      try {
        content = JSON.parse(fs.readFileSync(filePath, "utf-8"));
      } catch (e) {
        // Ignore parse errors
      }
    }

    return {
      filename: file,
      path: filePath,
      size: stats.size,
      modified: stats.mtime.toISOString(),
      type: ext.replace(".", ""),
      phase: content?.phase || content?.page_info?.phase || null,
      page_name: content?.page_info?.page_name || null
    };
  });
};

/**
 * Get brand rules by section
 */
export const getBrandRulesSection = (section: string): any => {
  switch (section) {
    case "locked_positions":
      return BRAND_RULES.locked_positions;
    case "tiers":
      return {
        tier_1: BRAND_RULES.tier_1_brands,
        tier_2: BRAND_RULES.tier_2_brands,
        tier_3: BRAND_RULES.tier_3_brands
      };
    case "guidelines":
      return BRAND_RULES.brand_guidelines;
    case "compliance":
      return BRAND_RULES.compliance_rules;
    case "writers":
      return BRAND_RULES.writer_assignments;
    default:
      return BRAND_RULES;
  }
};

/**
 * Get template info
 */
export const getTemplateInfo = (templateNumber?: number): any => {
  if (templateNumber !== undefined) {
    return TEMPLATES[templateNumber] || { error: "Invalid template number" };
  }
  return TEMPLATES;
};

/**
 * Create feedback object
 */
export const createFeedback = (
  pageName: string,
  rating: number,
  submitter: string,
  issues?: string[],
  improvements?: string[]
): any => {
  return {
    page_name: pageName,
    rating,
    issues: issues || [],
    improvements: improvements || [],
    submitter,
    submitted_at: new Date().toISOString(),
    status: "submitted"
  };
};

/**
 * Generate feedback filename
 */
export const generateFeedbackFilename = (pageName: string): string => {
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  return `${pageName.toLowerCase().replace(/\s+/g, "-")}-${timestamp}.json`;
};
