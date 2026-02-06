import { describe, it, expect, beforeEach, vi } from 'vitest';
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import * as fs from 'fs';
import * as path from 'path';
import { setSiteStructureData } from '../../src/index.js';

// Mock fs and child_process modules
vi.mock('fs');
vi.mock('child_process');

describe('Tool Integration Tests', () => {
  let server: Server;

  beforeEach(() => {
    vi.clearAllMocks();

    // Create a mock server for testing
    server = new Server(
      { name: "test-server", version: "1.0.0" },
      { capabilities: { tools: {} } }
    );

    // Set up test CSV data
    const englishData = [
      {
        "Page Name": "NFL Betting Sites",
        "Target Keywords": "nfl betting sites",
        "Full URL": "https://www.topendsports.com/betting/nfl-betting-sites/",
        "Level 1": "Betting",
        "Level 2": "NFL",
        "Level 3": "",
        "Level 4": "",
        "Writer": "Lewis Humphries",
        "Status": "Published",
        "Priority": "Critical",
        "Volume": "12000",
        "Phase": "Phase 3",
        "Notes": "Commercial landing page"
      }
    ];

    const spanishData = [
      {
        "Page Name": "Mejores Casas de Apuestas",
        "Target Keywords": "mejores casas de apuestas",
        "Full URL": "https://www.topendsports.com/es/apuestas/",
        "Level 1": "Apuestas",
        "Level 2": "",
        "Level 3": "",
        "Level 4": "",
        "Writer": "Gustavo Cantella",
        "Status": "Published",
        "Priority": "Critical",
        "Volume": "8000",
        "Phase": "Phase 3",
        "Notes": "Spanish homepage"
      }
    ];

    setSiteStructureData(englishData, spanishData);
  });

  describe('lookup_site_structure tool', () => {
    it('should return search results for valid query', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              query: "nfl",
              language: "english",
              results_count: 1,
              results: [{
                page_name: "NFL Betting Sites",
                url: "https://www.topendsports.com/betting/nfl-betting-sites/",
                writer: "Lewis Humphries",
                status: "Published",
                priority: "Critical"
              }]
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "lookup_site_structure",
          arguments: { query: "nfl", language: "english" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.query).toBe("nfl");
      expect(data.results_count).toBeGreaterThan(0);
      expect(data.results[0].page_name).toContain("NFL");
    });

    it('should support Spanish language queries', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              query: "apuestas",
              language: "spanish",
              results_count: 1,
              results: [{
                page_name: "Mejores Casas de Apuestas"
              }]
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "lookup_site_structure",
          arguments: { query: "apuestas", language: "spanish" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.language).toBe("spanish");
    });

    it('should default to english language', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              query: "betting",
              language: "english",
              results_count: 1
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "lookup_site_structure",
          arguments: { query: "betting" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.language).toBe("english");
    });

    it('should limit results to 20', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              query: "betting",
              results_count: 50,
              results: new Array(20).fill({})
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "lookup_site_structure",
          arguments: { query: "betting" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.results.length).toBeLessThanOrEqual(20);
    });
  });

  describe('get_page_info tool', () => {
    it('should return page info for existing URL', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              "Page Name": "NFL Betting Sites",
              "Full URL": "https://www.topendsports.com/betting/nfl-betting-sites/",
              "Writer": "Lewis Humphries"
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_page_info",
          arguments: { url: "https://www.topendsports.com/betting/nfl-betting-sites/" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data["Page Name"]).toBe("NFL Betting Sites");
    });

    it('should return error for non-existent URL', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "Page not found",
              url: "https://www.example.com/not-found/"
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_page_info",
          arguments: { url: "https://www.example.com/not-found/" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.error).toBe("Page not found");
    });
  });

  describe('get_brand_rules tool', () => {
    it('should return all brand rules by default', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              locked_positions: { position_1: { brand: "FanDuel" } },
              tier_1_brands: ["FanDuel", "BetMGM"],
              compliance_rules: { age_requirement_default: "21+" }
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_brand_rules",
          arguments: {}
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.locked_positions).toBeDefined();
      expect(data.tier_1_brands).toBeDefined();
      expect(data.compliance_rules).toBeDefined();
    });

    it('should return only locked positions when section is locked_positions', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              position_1: { brand: "FanDuel", status: "LOCKED" },
              position_2: { brand: "BetMGM", status: "LOCKED" }
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_brand_rules",
          arguments: { section: "locked_positions" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.position_1).toBeDefined();
      expect(data.position_1.brand).toBe("FanDuel");
    });

    it('should return tiers when section is tiers', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              tier_1: ["FanDuel", "BetMGM", "DraftKings"],
              tier_2: ["Fanatics", "theScore BET"],
              tier_3: ["Golden Nugget"]
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_brand_rules",
          arguments: { section: "tiers" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.tier_1).toBeDefined();
      expect(data.tier_2).toBeDefined();
      expect(data.tier_3).toBeDefined();
    });

    it('should return compliance rules when section is compliance', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              age_requirement_default: "21+",
              gambling_hotline: "1-800-522-4700"
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_brand_rules",
          arguments: { section: "compliance" }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.age_requirement_default).toBe("21+");
      expect(data.gambling_hotline).toBe("1-800-522-4700");
    });
  });

  describe('list_active_briefs tool', () => {
    it('should list files in active directory', async () => {
      vi.spyOn(fs, 'existsSync').mockReturnValue(true);
      vi.spyOn(fs, 'readdirSync').mockReturnValue(['test-phase1.json'] as any);
      vi.spyOn(fs, 'statSync').mockReturnValue({
        size: 1024,
        mtime: new Date('2025-12-08T10:00:00Z')
      } as any);
      vi.spyOn(fs, 'readFileSync').mockReturnValue(
        JSON.stringify({ phase: 1, page_info: { page_name: "test" } })
      );

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              directory: "/path/to/active",
              count: 1,
              briefs: [
                {
                  filename: "test-phase1.json",
                  phase: 1,
                  page_name: "test"
                }
              ]
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "list_active_briefs",
          arguments: {}
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.count).toBeGreaterThan(0);
      expect(data.briefs).toBeDefined();
    });

    it('should return empty list if directory does not exist', async () => {
      vi.spyOn(fs, 'existsSync').mockReturnValue(false);

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              directory: "/path/to/active",
              count: 0,
              briefs: []
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "list_active_briefs",
          arguments: {}
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.count).toBe(0);
      expect(data.briefs).toEqual([]);
    });
  });

  describe('list_completed_briefs tool', () => {
    it('should list and categorize completed briefs', async () => {
      vi.spyOn(fs, 'existsSync').mockReturnValue(true);
      vi.spyOn(fs, 'readdirSync').mockReturnValue([
        'test-brief.md',
        'test-brief.docx'
      ] as any);
      vi.spyOn(fs, 'statSync').mockReturnValue({
        size: 5000,
        mtime: new Date('2025-12-08T10:00:00Z')
      } as any);

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              directory: "/path/to/output",
              total_count: 2,
              markdown_count: 1,
              docx_count: 1,
              briefs: [
                { filename: "test-brief.md", type: "md" },
                { filename: "test-brief.docx", type: "docx" }
              ]
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "list_completed_briefs",
          arguments: {}
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.total_count).toBe(2);
      expect(data.markdown_count).toBe(1);
      expect(data.docx_count).toBe(1);
    });
  });

  describe('read_phase_data tool', () => {
    it('should read phase 1 data successfully', async () => {
      const phase1Data = {
        phase: 1,
        page_info: { page_name: "test-page" },
        keyword_cluster: { primary: "test keyword" }
      };

      vi.spyOn(fs, 'existsSync').mockReturnValue(true);
      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(phase1Data));

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify(phase1Data)
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "read_phase_data",
          arguments: { page_name: "test-page", phase: 1 }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.phase).toBe(1);
      expect(data.page_info.page_name).toBe("test-page");
    });

    it('should read phase 2 data successfully', async () => {
      const phase2Data = {
        phase: 2,
        page_info: { page_name: "test-page" },
        content_outline: { h1: "Test H1" }
      };

      vi.spyOn(fs, 'existsSync').mockReturnValue(true);
      vi.spyOn(fs, 'readFileSync').mockReturnValue(JSON.stringify(phase2Data));

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify(phase2Data)
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "read_phase_data",
          arguments: { page_name: "test-page", phase: 2 }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.phase).toBe(2);
      expect(data.content_outline).toBeDefined();
    });

    it('should return error if phase file does not exist', async () => {
      vi.spyOn(fs, 'existsSync').mockReturnValue(false);
      vi.spyOn(fs, 'readdirSync').mockReturnValue([]);

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "Phase data file not found",
              expected_path: "/path/to/active/test-page-phase1.json",
              available_files: []
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "read_phase_data",
          arguments: { page_name: "test-page", phase: 1 }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.error).toBe("Phase data file not found");
    });
  });

  describe('submit_feedback tool', () => {
    it('should create feedback file successfully', async () => {
      const mkdirSyncSpy = vi.spyOn(fs, 'mkdirSync').mockImplementation(() => undefined);
      const writeFileSyncSpy = vi.spyOn(fs, 'writeFileSync').mockImplementation(() => {});
      vi.spyOn(fs, 'existsSync').mockReturnValue(false);

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              success: true,
              message: "Feedback submitted successfully",
              feedback: {
                page_name: "test-page",
                rating: 4,
                issues: ["Issue 1"],
                improvements: ["Improvement 1"],
                submitter: "Test User"
              }
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "submit_feedback",
          arguments: {
            page_name: "test-page",
            rating: 4,
            issues: ["Issue 1"],
            improvements: ["Improvement 1"],
            submitter: "Test User"
          }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.success).toBe(true);
      expect(data.feedback.page_name).toBe("test-page");
      expect(data.feedback.rating).toBe(4);
    });

    it('should handle optional issues and improvements', async () => {
      vi.spyOn(fs, 'existsSync').mockReturnValue(true);
      vi.spyOn(fs, 'writeFileSync').mockImplementation(() => {});

      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              success: true,
              feedback: {
                page_name: "test-page",
                rating: 5,
                issues: [],
                improvements: [],
                submitter: "Test User"
              }
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "submit_feedback",
          arguments: {
            page_name: "test-page",
            rating: 5,
            submitter: "Test User"
          }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.success).toBe(true);
      expect(data.feedback.issues).toEqual([]);
      expect(data.feedback.improvements).toEqual([]);
    });
  });

  describe('get_template_info tool', () => {
    it('should return template 1 (Review) info', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              name: "Review Template",
              description: "Individual sportsbook/product review page",
              typical_word_count: "2,500-3,500",
              structure: ["H1: [Brand] Review", "Quick Facts Box"]
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_template_info",
          arguments: { template_number: 1 }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.name).toBe("Review Template");
    });

    it('should return template 2 (Comparison) info', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              name: "Comparison Template",
              description: "Multi-brand comparison page",
              typical_word_count: "3,000-4,000"
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_template_info",
          arguments: { template_number: 2 }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.name).toBe("Comparison Template");
    });

    it('should return all templates when no number specified', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              1: { name: "Review Template" },
              2: { name: "Comparison Template" },
              3: { name: "How-To Template" },
              4: { name: "State Page Template" }
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_template_info",
          arguments: {}
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data[1]).toBeDefined();
      expect(data[2]).toBeDefined();
      expect(data[3]).toBeDefined();
      expect(data[4]).toBeDefined();
    });

    it('should return error for invalid template number', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "Invalid template number"
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "get_template_info",
          arguments: { template_number: 99 }
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.error).toBe("Invalid template number");
    });
  });

  describe('Unknown tool handler', () => {
    it('should return error for unknown tool', async () => {
      const mockHandler = vi.fn().mockResolvedValue({
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: "Unknown tool: invalid_tool_name"
            })
          }
        ]
      });

      server.setRequestHandler(CallToolRequestSchema, mockHandler);

      const response = await mockHandler({
        params: {
          name: "invalid_tool_name",
          arguments: {}
        }
      });

      const data = JSON.parse(response.content[0].text);
      expect(data.error).toContain("Unknown tool");
    });
  });
});
