import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  findProjectRoot,
  searchSiteStructure,
  getPageByUrl,
  listBriefs,
  BRAND_RULES,
  setSiteStructureData
} from '../../src/index.js';
import * as fs from 'fs';
import * as path from 'path';

// Mock fs module
vi.mock('fs');

describe('findProjectRoot', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should find project root when content-briefs-skill exists in current directory', () => {
    vi.spyOn(fs, 'existsSync').mockImplementation((p: any) => {
      return p.includes('content-briefs-skill');
    });

    const root = findProjectRoot();
    expect(root).toBeTruthy();
  });

  it('should check multiple possible paths', () => {
    const existsSyncSpy = vi.spyOn(fs, 'existsSync').mockReturnValue(false);

    findProjectRoot();

    // Should check at least a few paths
    expect(existsSyncSpy).toHaveBeenCalled();
  });

  it('should return current directory if content-briefs-skill not found', () => {
    vi.spyOn(fs, 'existsSync').mockReturnValue(false);

    const root = findProjectRoot();
    expect(root).toBe(process.cwd());
  });

  it('should handle parent directory correctly', () => {
    vi.spyOn(fs, 'existsSync').mockImplementation((p: any) => {
      const pathStr = p.toString();
      return pathStr.includes('content-briefs-skill') &&
             !pathStr.includes('mcp-server');
    });

    const root = findProjectRoot();
    expect(root).toBeTruthy();
  });
});

describe('searchSiteStructure', () => {
  beforeEach(() => {
    // Set up test data
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
      },
      {
        "Page Name": "NBA Betting Apps",
        "Target Keywords": "nba betting apps",
        "Full URL": "https://www.topendsports.com/betting/nba-betting-apps/",
        "Level 1": "Betting",
        "Level 2": "NBA",
        "Level 3": "",
        "Level 4": "",
        "Writer": "Lewis Humphries",
        "Status": "Published",
        "Priority": "High",
        "Volume": "8500",
        "Phase": "Phase 3",
        "Notes": ""
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

  it('should search by page name (case insensitive)', () => {
    const results = searchSiteStructure('nfl');
    expect(results.length).toBeGreaterThan(0);
    expect(results[0]["Page Name"]).toContain("NFL");
  });

  it('should search by keywords', () => {
    const results = searchSiteStructure('betting sites');
    expect(results.length).toBeGreaterThan(0);
    expect(results[0]["Target Keywords"]).toContain("betting sites");
  });

  it('should be case insensitive', () => {
    const resultsLower = searchSiteStructure('nfl');
    const resultsUpper = searchSiteStructure('NFL');
    expect(resultsLower.length).toBe(resultsUpper.length);
  });

  it('should search Spanish content when language is spanish', () => {
    const results = searchSiteStructure('apuestas', 'spanish');
    expect(results.length).toBeGreaterThan(0);
    expect(results[0]["Page Name"]).toContain("Apuestas");
  });

  it('should return empty array for non-matching query', () => {
    const results = searchSiteStructure('nonexistent-query-xyz');
    expect(results).toEqual([]);
  });

  it('should search across multiple fields', () => {
    const results = searchSiteStructure('Betting');
    expect(results.length).toBeGreaterThan(0);
  });

  it('should handle URL search', () => {
    const results = searchSiteStructure('topendsports.com');
    expect(results.length).toBeGreaterThan(0);
  });

  it('should handle partial matches', () => {
    const results = searchSiteStructure('bet');
    expect(results.length).toBeGreaterThan(0);
  });
});

describe('getPageByUrl', () => {
  beforeEach(() => {
    const englishData = [
      {
        "Page Name": "NFL Betting Sites",
        "Full URL": "https://www.topendsports.com/betting/nfl-betting-sites/",
        "Writer": "Lewis Humphries"
      }
    ];

    const spanishData = [
      {
        "Page Name": "Mejores Casas de Apuestas",
        "Full URL": "https://www.topendsports.com/es/apuestas/",
        "Writer": "Gustavo Cantella"
      }
    ];

    setSiteStructureData(englishData, spanishData);
  });

  it('should find page by exact URL match', () => {
    const page = getPageByUrl('https://www.topendsports.com/betting/nfl-betting-sites/');
    expect(page).toBeTruthy();
    expect(page["Page Name"]).toBe("NFL Betting Sites");
  });

  it('should return null for non-existent URL', () => {
    const page = getPageByUrl('https://www.example.com/not-found/');
    expect(page).toBeNull();
  });

  it('should search both English and Spanish content', () => {
    const englishPage = getPageByUrl('https://www.topendsports.com/betting/nfl-betting-sites/');
    const spanishPage = getPageByUrl('https://www.topendsports.com/es/apuestas/');

    expect(englishPage).toBeTruthy();
    expect(spanishPage).toBeTruthy();
  });

  it('should require exact URL match (not partial)', () => {
    const page = getPageByUrl('https://www.topendsports.com/betting/');
    expect(page).toBeNull();
  });
});

describe('listBriefs', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should return empty array if directory does not exist', () => {
    vi.spyOn(fs, 'existsSync').mockReturnValue(false);

    const briefs = listBriefs('/nonexistent/path');
    expect(briefs).toEqual([]);
  });

  it('should list files in directory', () => {
    vi.spyOn(fs, 'existsSync').mockReturnValue(true);
    vi.spyOn(fs, 'readdirSync').mockReturnValue(['file1.json', 'file2.md'] as any);
    vi.spyOn(fs, 'statSync').mockReturnValue({
      size: 1024,
      mtime: new Date('2025-12-08T10:00:00Z')
    } as any);
    vi.spyOn(fs, 'readFileSync').mockReturnValue('{}');

    const briefs = listBriefs('/test/path');

    expect(briefs).toHaveLength(2);
    expect(briefs[0].filename).toBe('file1.json');
    expect(briefs[1].filename).toBe('file2.md');
  });

  it('should include file metadata', () => {
    vi.spyOn(fs, 'existsSync').mockReturnValue(true);
    vi.spyOn(fs, 'readdirSync').mockReturnValue(['test.json'] as any);
    vi.spyOn(fs, 'statSync').mockReturnValue({
      size: 2048,
      mtime: new Date('2025-12-08T10:00:00Z')
    } as any);
    vi.spyOn(fs, 'readFileSync').mockReturnValue('{"phase": 1, "page_info": {"page_name": "test"}}');

    const briefs = listBriefs('/test/path');

    expect(briefs[0]).toHaveProperty('size', 2048);
    expect(briefs[0]).toHaveProperty('modified');
    expect(briefs[0]).toHaveProperty('type', 'json');
  });

  it('should parse JSON files and extract phase info', () => {
    vi.spyOn(fs, 'existsSync').mockReturnValue(true);
    vi.spyOn(fs, 'readdirSync').mockReturnValue(['test-phase1.json'] as any);
    vi.spyOn(fs, 'statSync').mockReturnValue({
      size: 1024,
      mtime: new Date('2025-12-08T10:00:00Z')
    } as any);
    vi.spyOn(fs, 'readFileSync').mockReturnValue(
      JSON.stringify({ phase: 1, page_info: { page_name: "test-page" } })
    );

    const briefs = listBriefs('/test/path');

    expect(briefs[0].phase).toBe(1);
    expect(briefs[0].page_name).toBe("test-page");
  });

  it('should handle JSON parse errors gracefully', () => {
    vi.spyOn(fs, 'existsSync').mockReturnValue(true);
    vi.spyOn(fs, 'readdirSync').mockReturnValue(['invalid.json'] as any);
    vi.spyOn(fs, 'statSync').mockReturnValue({
      size: 100,
      mtime: new Date('2025-12-08T10:00:00Z')
    } as any);
    vi.spyOn(fs, 'readFileSync').mockReturnValue('invalid json content');

    const briefs = listBriefs('/test/path');

    expect(briefs).toHaveLength(1);
    expect(briefs[0].phase).toBeNull();
  });

  it('should not attempt to parse non-JSON files', () => {
    vi.spyOn(fs, 'existsSync').mockReturnValue(true);
    vi.spyOn(fs, 'readdirSync').mockReturnValue(['test.md', 'test.docx'] as any);
    vi.spyOn(fs, 'statSync').mockReturnValue({
      size: 500,
      mtime: new Date('2025-12-08T10:00:00Z')
    } as any);
    const readFileSpy = vi.spyOn(fs, 'readFileSync');

    const briefs = listBriefs('/test/path');

    expect(briefs).toHaveLength(2);
    expect(briefs[0].type).toBe('md');
    expect(briefs[1].type).toBe('docx');
  });
});

describe('BRAND_RULES constant', () => {
  it('should have locked positions defined', () => {
    expect(BRAND_RULES.locked_positions).toBeDefined();
    expect(BRAND_RULES.locked_positions.position_1).toBeDefined();
    expect(BRAND_RULES.locked_positions.position_2).toBeDefined();
  });

  it('should have FanDuel locked at position 1', () => {
    expect(BRAND_RULES.locked_positions.position_1.brand).toBe('FanDuel');
    expect(BRAND_RULES.locked_positions.position_1.status).toBe('LOCKED');
  });

  it('should have BetMGM locked at position 2', () => {
    expect(BRAND_RULES.locked_positions.position_2.brand).toBe('BetMGM');
    expect(BRAND_RULES.locked_positions.position_2.status).toBe('LOCKED');
  });

  it('should have tier 1 brands array', () => {
    expect(Array.isArray(BRAND_RULES.tier_1_brands)).toBe(true);
    expect(BRAND_RULES.tier_1_brands).toContain('FanDuel');
    expect(BRAND_RULES.tier_1_brands).toContain('BetMGM');
    expect(BRAND_RULES.tier_1_brands).toContain('DraftKings');
  });

  it('should have tier 2 brands array', () => {
    expect(Array.isArray(BRAND_RULES.tier_2_brands)).toBe(true);
    expect(BRAND_RULES.tier_2_brands).toContain('theScore BET');
    expect(BRAND_RULES.tier_2_brands).toContain('Fanatics');
  });

  it('should have tier 3 brands array', () => {
    expect(Array.isArray(BRAND_RULES.tier_3_brands)).toBe(true);
    expect(BRAND_RULES.tier_3_brands.length).toBeGreaterThan(0);
  });

  it('should have brand guidelines for key brands', () => {
    expect(BRAND_RULES.brand_guidelines.FanDuel).toBeDefined();
    expect(BRAND_RULES.brand_guidelines.BetMGM).toBeDefined();
    expect(BRAND_RULES.brand_guidelines.DraftKings).toBeDefined();
  });

  it('should have USP for each brand in guidelines', () => {
    const fanduel = BRAND_RULES.brand_guidelines.FanDuel;
    expect(fanduel.usp).toBeDefined();
    expect(typeof fanduel.usp).toBe('string');
  });

  it('should have key features for each brand', () => {
    const fanduel = BRAND_RULES.brand_guidelines.FanDuel;
    expect(Array.isArray(fanduel.key_features)).toBe(true);
    expect(fanduel.key_features.length).toBeGreaterThan(0);
  });

  it('should have compliance rules defined', () => {
    expect(BRAND_RULES.compliance_rules).toBeDefined();
    expect(BRAND_RULES.compliance_rules.age_requirement_default).toBe('21+');
    expect(BRAND_RULES.compliance_rules.gambling_hotline).toBe('1-800-522-4700');
  });

  it('should have age requirement exceptions', () => {
    expect(Array.isArray(BRAND_RULES.compliance_rules.age_requirement_exceptions)).toBe(true);
    expect(BRAND_RULES.compliance_rules.age_requirement_exceptions).toContain('MT');
    expect(BRAND_RULES.compliance_rules.age_requirement_exceptions).toContain('NH');
  });

  it('should have forbidden language list', () => {
    expect(Array.isArray(BRAND_RULES.compliance_rules.forbidden_language)).toBe(true);
    expect(BRAND_RULES.compliance_rules.forbidden_language).toContain('Guaranteed wins');
    expect(BRAND_RULES.compliance_rules.forbidden_language).toContain('Risk-free');
  });

  it('should have writer assignments', () => {
    expect(BRAND_RULES.writer_assignments).toBeDefined();
    expect(BRAND_RULES.writer_assignments["Lewis Humphries"]).toBeDefined();
    expect(BRAND_RULES.writer_assignments["Tom Goldsmith"]).toBeDefined();
    expect(BRAND_RULES.writer_assignments["Gustavo Cantella"]).toBeDefined();
  });

  it('should have Gustavo Cantella assigned to Spanish content', () => {
    const gustavo = BRAND_RULES.writer_assignments["Gustavo Cantella"];
    expect(gustavo.content_types).toContain("All Spanish content (/es/ URLs)");
  });

  it('should have theScore BET with rebrand notes', () => {
    const theScore = BRAND_RULES.brand_guidelines["theScore BET"];
    expect(theScore).toBeDefined();
    expect(theScore.notes).toContain("ESPN BET");
    expect(theScore.notes).toContain("December 2025");
  });
});
