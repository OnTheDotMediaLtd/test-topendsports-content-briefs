#!/usr/bin/env node
/**
 * TopEndSports Content Briefs MCP Server
 *
 * Provides tools for the content briefs generation system:
 * - Site structure lookup (CSV search)
 * - Brand rules and positioning
 * - Brief management (list active/completed)
 * - Document conversion (markdown to docx)
 * - Feedback submission
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema, ListResourcesRequestSchema, ReadResourceRequestSchema, } from "@modelcontextprotocol/sdk/types.js";
import * as fs from "fs";
import * as path from "path";
import { parse } from "csv-parse/sync";
import { execSync } from "child_process";
// Determine base paths - look for content-briefs-skill directory
export const findProjectRoot = () => {
    // Get the directory where this script is located
    const scriptDir = path.dirname(new URL(import.meta.url).pathname);
    // On Windows, remove leading slash from /C:/... paths
    const normalizedScriptDir = process.platform === 'win32' && scriptDir.startsWith('/')
        ? scriptDir.slice(1)
        : scriptDir;
    let currentDir = process.cwd();
    // Try to find the project root by looking for content-briefs-skill
    const possiblePaths = [
        currentDir,
        path.dirname(currentDir), // Parent of mcp-server
        path.join(currentDir, ".."),
        path.resolve(normalizedScriptDir, "../.."), // Two levels up from dist/index.js
        path.resolve(normalizedScriptDir, ".."), // One level up
    ];
    for (const p of possiblePaths) {
        try {
            if (fs.existsSync(path.join(p, "content-briefs-skill"))) {
                return p;
            }
        }
        catch {
            // Continue to next path if this one fails
        }
    }
    return currentDir;
};
const PROJECT_ROOT = findProjectRoot();
const SKILL_DIR = path.join(PROJECT_ROOT, "content-briefs-skill");
const DATA_DIR = path.join(SKILL_DIR, "assets", "data");
const ACTIVE_DIR = path.join(SKILL_DIR, "active");
const OUTPUT_DIR = path.join(SKILL_DIR, "output");
const FEEDBACK_DIR = path.join(SKILL_DIR, "feedback");
const SCRIPTS_DIR = path.join(SKILL_DIR, "scripts");
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
    tier_2_brands: ["Fanatics", "theScore BET", "BetRivers", "Bally Bet", "BetParx"], // Note: ESPN BET rebranded to theScore BET Dec 2025
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
// CSV data cache
export let siteStructureEnglish = [];
export let siteStructureSpanish = [];
// Helper to set CSV data (for testing)
export const setSiteStructureData = (english, spanish) => {
    siteStructureEnglish = english;
    siteStructureSpanish = spanish;
};
// Load CSV data
export const loadCSVData = () => {
    try {
        const englishPath = path.join(DATA_DIR, "site-structure-english.csv");
        const spanishPath = path.join(DATA_DIR, "site-structure-spanish.csv");
        if (fs.existsSync(englishPath)) {
            const content = fs.readFileSync(englishPath, "utf-8");
            siteStructureEnglish = parse(content, {
                columns: true,
                skip_empty_lines: true,
                bom: true
            });
        }
        if (fs.existsSync(spanishPath)) {
            const content = fs.readFileSync(spanishPath, "utf-8");
            siteStructureSpanish = parse(content, {
                columns: true,
                skip_empty_lines: true,
                bom: true
            });
        }
    }
    catch (error) {
        console.error("Error loading CSV data:", error);
    }
};
// Search site structure
export const searchSiteStructure = (query, language = "english") => {
    const data = language === "spanish" ? siteStructureSpanish : siteStructureEnglish;
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
        return searchFields.some(field => field && field.toLowerCase().includes(queryLower));
    });
};
// Get page by URL
export const getPageByUrl = (url) => {
    const allData = [...siteStructureEnglish, ...siteStructureSpanish];
    return allData.find(row => row["Full URL"] === url) || null;
};
// List briefs in a directory
export const listBriefs = (directory) => {
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
            }
            catch (e) {
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
// Create the MCP server
const server = new Server({
    name: "topendsports-content-briefs",
    version: "1.0.0"
}, {
    capabilities: {
        tools: {},
        resources: {}
    }
});
// Define available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
        tools: [
            {
                name: "lookup_site_structure",
                description: "Search the site structure CSV to find page information, target keywords, writer assignments, and priorities. Always search by keywords or page name, not by URL.",
                inputSchema: {
                    type: "object",
                    properties: {
                        query: {
                            type: "string",
                            description: "Search query - can be page name, keyword, or partial URL"
                        },
                        language: {
                            type: "string",
                            enum: ["english", "spanish"],
                            description: "Language version to search (default: english)"
                        }
                    },
                    required: ["query"]
                }
            },
            {
                name: "get_page_info",
                description: "Get complete page information by exact URL",
                inputSchema: {
                    type: "object",
                    properties: {
                        url: {
                            type: "string",
                            description: "The full URL of the page"
                        }
                    },
                    required: ["url"]
                }
            },
            {
                name: "get_brand_rules",
                description: "Get brand positioning rules, locked positions, tier information, and compliance requirements",
                inputSchema: {
                    type: "object",
                    properties: {
                        section: {
                            type: "string",
                            enum: ["all", "locked_positions", "tiers", "guidelines", "compliance", "writers"],
                            description: "Which section of brand rules to return (default: all)"
                        }
                    }
                }
            },
            {
                name: "list_active_briefs",
                description: "List all work-in-progress brief JSON files in the active directory",
                inputSchema: {
                    type: "object",
                    properties: {}
                }
            },
            {
                name: "list_completed_briefs",
                description: "List all completed briefs (markdown and docx) in the output directory",
                inputSchema: {
                    type: "object",
                    properties: {}
                }
            },
            {
                name: "read_phase_data",
                description: "Read the JSON data for a specific phase of a brief",
                inputSchema: {
                    type: "object",
                    properties: {
                        page_name: {
                            type: "string",
                            description: "The page name slug (e.g., 'nfl-betting-sites')"
                        },
                        phase: {
                            type: "number",
                            enum: [1, 2],
                            description: "Phase number (1 or 2)"
                        }
                    },
                    required: ["page_name", "phase"]
                }
            },
            {
                name: "convert_to_docx",
                description: "Convert markdown brief files to Word documents (.docx)",
                inputSchema: {
                    type: "object",
                    properties: {
                        files: {
                            type: "array",
                            items: { type: "string" },
                            description: "List of markdown file paths to convert. Use '--all' as single item to convert all markdown files in output folder."
                        }
                    },
                    required: ["files"]
                }
            },
            {
                name: "submit_feedback",
                description: "Submit feedback for a content brief to the continuous improvement system",
                inputSchema: {
                    type: "object",
                    properties: {
                        page_name: {
                            type: "string",
                            description: "Name of the page the feedback is about"
                        },
                        rating: {
                            type: "number",
                            minimum: 1,
                            maximum: 5,
                            description: "Rating from 1-5"
                        },
                        issues: {
                            type: "array",
                            items: { type: "string" },
                            description: "List of issues found"
                        },
                        improvements: {
                            type: "array",
                            items: { type: "string" },
                            description: "Suggested improvements"
                        },
                        submitter: {
                            type: "string",
                            description: "Name of person submitting feedback"
                        }
                    },
                    required: ["page_name", "rating", "submitter"]
                }
            },
            {
                name: "get_template_info",
                description: "Get information about content templates (comparison, review, how-to, state)",
                inputSchema: {
                    type: "object",
                    properties: {
                        template_number: {
                            type: "number",
                            enum: [1, 2, 3, 4],
                            description: "Template number: 1=Review, 2=Comparison, 3=How-To, 4=State Page"
                        }
                    }
                }
            }
        ]
    };
});
// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    // Ensure CSV data is loaded
    if (siteStructureEnglish.length === 0) {
        loadCSVData();
    }
    switch (name) {
        case "lookup_site_structure": {
            const query = args.query;
            const language = args.language || "english";
            const results = searchSiteStructure(query, language);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify({
                            query,
                            language,
                            results_count: results.length,
                            results: results.slice(0, 20).map(r => ({
                                page_name: r["Page Name"],
                                url: r["Full URL"],
                                writer: r["Writer"],
                                status: r["Status"],
                                priority: r["Priority"],
                                target_keywords: r["Target Keywords"],
                                volume: r["Volume"],
                                phase: r["Phase"],
                                notes: r["Notes"]
                            }))
                        }, null, 2)
                    }
                ]
            };
        }
        case "get_page_info": {
            const url = args.url;
            const page = getPageByUrl(url);
            return {
                content: [
                    {
                        type: "text",
                        text: page
                            ? JSON.stringify(page, null, 2)
                            : JSON.stringify({ error: "Page not found", url }, null, 2)
                    }
                ]
            };
        }
        case "get_brand_rules": {
            const section = args.section || "all";
            let result = {};
            switch (section) {
                case "locked_positions":
                    result = BRAND_RULES.locked_positions;
                    break;
                case "tiers":
                    result = {
                        tier_1: BRAND_RULES.tier_1_brands,
                        tier_2: BRAND_RULES.tier_2_brands,
                        tier_3: BRAND_RULES.tier_3_brands
                    };
                    break;
                case "guidelines":
                    result = BRAND_RULES.brand_guidelines;
                    break;
                case "compliance":
                    result = BRAND_RULES.compliance_rules;
                    break;
                case "writers":
                    result = BRAND_RULES.writer_assignments;
                    break;
                default:
                    result = BRAND_RULES;
            }
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(result, null, 2)
                    }
                ]
            };
        }
        case "list_active_briefs": {
            const briefs = listBriefs(ACTIVE_DIR);
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify({
                            directory: ACTIVE_DIR,
                            count: briefs.length,
                            briefs
                        }, null, 2)
                    }
                ]
            };
        }
        case "list_completed_briefs": {
            const briefs = listBriefs(OUTPUT_DIR);
            // Group by type
            const byType = {
                markdown: briefs.filter(b => b.type === "md"),
                docx: briefs.filter(b => b.type === "docx")
            };
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify({
                            directory: OUTPUT_DIR,
                            total_count: briefs.length,
                            markdown_count: byType.markdown.length,
                            docx_count: byType.docx.length,
                            briefs
                        }, null, 2)
                    }
                ]
            };
        }
        case "read_phase_data": {
            const pageName = args.page_name;
            const phase = args.phase;
            const filename = `${pageName}-phase${phase}.json`;
            const filePath = path.join(ACTIVE_DIR, filename);
            if (!fs.existsSync(filePath)) {
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify({
                                error: "Phase data file not found",
                                expected_path: filePath,
                                available_files: fs.existsSync(ACTIVE_DIR)
                                    ? fs.readdirSync(ACTIVE_DIR).filter(f => f.endsWith(".json"))
                                    : []
                            }, null, 2)
                        }
                    ]
                };
            }
            const content = JSON.parse(fs.readFileSync(filePath, "utf-8"));
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(content, null, 2)
                    }
                ]
            };
        }
        case "convert_to_docx": {
            const files = args.files;
            const scriptPath = path.join(SCRIPTS_DIR, "convert_to_docx.py");
            if (!fs.existsSync(scriptPath)) {
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify({
                                error: "Conversion script not found",
                                expected_path: scriptPath
                            }, null, 2)
                        }
                    ]
                };
            }
            try {
                let command;
                if (files.length === 1 && files[0] === "--all") {
                    command = `python3 "${scriptPath}" --all`;
                }
                else {
                    const quotedFiles = files.map(f => `"${f}"`).join(" ");
                    command = `python3 "${scriptPath}" ${quotedFiles}`;
                }
                const output = execSync(command, {
                    cwd: SKILL_DIR,
                    encoding: "utf-8"
                });
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify({
                                success: true,
                                output
                            }, null, 2)
                        }
                    ]
                };
            }
            catch (error) {
                return {
                    content: [
                        {
                            type: "text",
                            text: JSON.stringify({
                                error: "Conversion failed",
                                message: error.message,
                                stderr: error.stderr?.toString()
                            }, null, 2)
                        }
                    ]
                };
            }
        }
        case "submit_feedback": {
            const { page_name, rating, issues, improvements, submitter } = args;
            // Ensure feedback directory exists
            const submittedDir = path.join(FEEDBACK_DIR, "submitted");
            if (!fs.existsSync(submittedDir)) {
                fs.mkdirSync(submittedDir, { recursive: true });
            }
            const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
            const filename = `${page_name.toLowerCase().replace(/\s+/g, "-")}-${timestamp}.json`;
            const filePath = path.join(submittedDir, filename);
            const feedback = {
                page_name,
                rating,
                issues: issues || [],
                improvements: improvements || [],
                submitter,
                submitted_at: new Date().toISOString(),
                status: "submitted"
            };
            fs.writeFileSync(filePath, JSON.stringify(feedback, null, 2));
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify({
                            success: true,
                            message: "Feedback submitted successfully",
                            file: filePath,
                            feedback
                        }, null, 2)
                    }
                ]
            };
        }
        case "get_template_info": {
            const templateNumber = args.template_number;
            const templates = {
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
            const result = templateNumber
                ? templates[templateNumber] || { error: "Invalid template number" }
                : templates;
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify(result, null, 2)
                    }
                ]
            };
        }
        default:
            return {
                content: [
                    {
                        type: "text",
                        text: JSON.stringify({ error: `Unknown tool: ${name}` }, null, 2)
                    }
                ]
            };
    }
});
// Define available resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
    return {
        resources: [
            {
                uri: "briefs://site-structure/english",
                name: "English Site Structure",
                description: "Complete site structure data for English content",
                mimeType: "application/json"
            },
            {
                uri: "briefs://site-structure/spanish",
                name: "Spanish Site Structure",
                description: "Complete site structure data for Spanish content",
                mimeType: "application/json"
            },
            {
                uri: "briefs://brand-rules",
                name: "Brand Rules",
                description: "Complete brand positioning and compliance rules",
                mimeType: "application/json"
            }
        ]
    };
});
// Handle resource reads
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
    const uri = request.params.uri;
    // Ensure CSV data is loaded
    if (siteStructureEnglish.length === 0) {
        loadCSVData();
    }
    switch (uri) {
        case "briefs://site-structure/english":
            return {
                contents: [
                    {
                        uri,
                        mimeType: "application/json",
                        text: JSON.stringify(siteStructureEnglish, null, 2)
                    }
                ]
            };
        case "briefs://site-structure/spanish":
            return {
                contents: [
                    {
                        uri,
                        mimeType: "application/json",
                        text: JSON.stringify(siteStructureSpanish, null, 2)
                    }
                ]
            };
        case "briefs://brand-rules":
            return {
                contents: [
                    {
                        uri,
                        mimeType: "application/json",
                        text: JSON.stringify(BRAND_RULES, null, 2)
                    }
                ]
            };
        default:
            throw new Error(`Unknown resource: ${uri}`);
    }
});
// Start the server
async function main() {
    loadCSVData();
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("TopEndSports Content Briefs MCP Server running on stdio");
}
main().catch(console.error);
//# sourceMappingURL=index.js.map