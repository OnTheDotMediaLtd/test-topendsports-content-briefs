import { describe, it, expect } from 'vitest';

describe('MCP Server - Basic Tests', () => {
  it('should pass a basic test', () => {
    expect(true).toBe(true);
  });

  it('should have correct Node version', () => {
    const nodeVersion = process.version;
    expect(nodeVersion).toBeDefined();
    // Ensure Node.js version is 18 or higher
    const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
    expect(majorVersion).toBeGreaterThanOrEqual(18);
  });

  it('should have environment variables accessible', () => {
    expect(process.env).toBeDefined();
  });
});

describe('MCP Server - Package Structure', () => {
  it('should be able to import package.json', async () => {
    const packageJson = await import('../../package.json', {
      assert: { type: 'json' },
    });
    expect(packageJson.default.name).toBe('topendsports-content-briefs-mcp');
  });
});
