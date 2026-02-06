# MCP Server Test Suite

This directory contains the comprehensive test suite for the TopEndSports Content Briefs MCP Server.

## Test Structure

```
tests/
├── setup.ts                          # Global test setup
├── unit/                             # Unit tests
│   └── index.test.ts                 # Tests for helper functions
├── integration/                      # Integration tests
│   └── tools.test.ts                 # Tests for MCP tool handlers
└── fixtures/                         # Test data
    ├── site-structure-english.csv    # Sample English site structure
    ├── site-structure-spanish.csv    # Sample Spanish site structure
    ├── sample-phase1.json            # Sample Phase 1 brief data
    └── sample-phase2.json            # Sample Phase 2 brief data
```

## Running Tests

### Run all tests
```bash
npm test
```

### Run tests in watch mode
```bash
npm run test:watch
```

### Run tests with coverage
```bash
npm run test:coverage
```

### Run tests with UI
```bash
npm run test:ui
```

## Test Coverage

The test suite includes:

### Unit Tests (37 tests)
- **findProjectRoot()** - Tests path resolution for finding project root
  - Current directory scenarios
  - Parent directory checks
  - Fallback behavior

- **searchSiteStructure()** - Tests site structure search functionality
  - Case-insensitive search
  - Multiple field search (page name, keywords, URL, levels)
  - English and Spanish language support
  - Partial matching
  - Edge cases (empty results)

- **getPageByUrl()** - Tests exact URL lookup
  - Exact match scenarios
  - English and Spanish content
  - Not found cases

- **listBriefs()** - Tests directory listing
  - File enumeration
  - Metadata extraction (size, modified date)
  - JSON parsing for phase data
  - Error handling for invalid JSON

- **BRAND_RULES constant** - Validates brand rules structure
  - Locked positions (FanDuel #1, BetMGM #2)
  - Brand tiers (Tier 1, 2, 3)
  - Brand guidelines and USPs
  - Compliance rules
  - Writer assignments
  - theScore BET rebrand notes

### Integration Tests (23 tests)
Tests for all MCP tool handlers:

- **lookup_site_structure** - Site structure search tool
  - Query handling
  - Language parameter (English/Spanish)
  - Result limiting (20 max)

- **get_page_info** - Page info retrieval by URL
  - Valid URL lookups
  - Error handling for missing pages

- **get_brand_rules** - Brand rules access
  - Full rules retrieval
  - Section filtering (locked_positions, tiers, guidelines, compliance, writers)

- **list_active_briefs** - Active briefs listing
  - Directory enumeration
  - Phase data extraction

- **list_completed_briefs** - Completed briefs listing
  - Markdown and DOCX categorization
  - File counting

- **read_phase_data** - Phase data reading
  - Phase 1 and Phase 2 data access
  - Error handling for missing files

- **submit_feedback** - Feedback submission
  - File creation
  - Optional fields handling

- **get_template_info** - Template information retrieval
  - Individual template lookup
  - All templates retrieval
  - Invalid template handling

## Test Fixtures

### CSV Fixtures
The CSV fixtures contain sample site structure data:
- **site-structure-english.csv**: 10 English content pages
- **site-structure-spanish.csv**: 5 Spanish content pages

### JSON Fixtures
The JSON fixtures contain complete phase data examples:
- **sample-phase1.json**: Complete Phase 1 research data with keyword clusters, competitor analysis, and brand selection
- **sample-phase2.json**: Complete Phase 2 writer brief with content outline, FAQs, and technical requirements

## Mocking Strategy

The tests use Vitest's mocking capabilities:

- **fs module**: Mocked for file system operations
- **child_process**: Mocked for script execution
- **CSV data**: Injected using `setSiteStructureData()` helper

## Coverage Targets

Current coverage thresholds:
- **Statements**: 25%
- **Branches**: 70%
- **Functions**: 100%
- **Lines**: 25%

The lower statement/line coverage reflects that we're testing exported helper functions and tool logic, not the full MCP server initialization and connection code.

## Writing New Tests

### Unit Test Template
```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { yourFunction } from '../../src/index.js';

describe('yourFunction', () => {
  beforeEach(() => {
    // Setup
  });

  it('should do something', () => {
    const result = yourFunction();
    expect(result).toBe(expected);
  });
});
```

### Integration Test Template
```typescript
import { describe, it, expect, vi } from 'vitest';
import { Server } from "@modelcontextprotocol/sdk/server/index.js";

describe('tool_name tool', () => {
  it('should handle request', async () => {
    const mockHandler = vi.fn().mockResolvedValue({
      content: [{ type: "text", text: JSON.stringify({ data: "value" }) }]
    });

    const response = await mockHandler({
      params: { name: "tool_name", arguments: {} }
    });

    const data = JSON.parse(response.content[0].text);
    expect(data).toBeDefined();
  });
});
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:
- Fast execution (< 3 seconds)
- No external dependencies
- Deterministic results
- Clear error messages

## Troubleshooting

### Tests failing with module errors
- Ensure you've run `npm install`
- Check that `type: "module"` is in package.json
- Verify `.js` extensions on imports

### Coverage not meeting thresholds
- Check `vitest.config.ts` threshold settings
- Run `npm run test:coverage` to see detailed report
- Coverage HTML report is in `coverage/index.html`

### Mock issues
- Clear mocks with `vi.clearAllMocks()` in `beforeEach`
- Check mock return values match expected types
- Use `vi.spyOn()` for partial mocking

## Future Enhancements

Potential test additions:
- E2E tests with real MCP client
- Performance benchmarks
- Snapshot testing for JSON outputs
- Parameterized tests for edge cases
- Resource handler tests (currently mocked in integration tests)
