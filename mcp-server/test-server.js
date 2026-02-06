#!/usr/bin/env node
/**
 * Simple test script to verify MCP server functionality
 */

import { spawn } from "child_process";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const serverPath = join(__dirname, "dist", "index.js");

// Start the MCP server
const server = spawn("node", [serverPath], {
  stdio: ["pipe", "pipe", "pipe"]
});

// Helper to send JSON-RPC request
function sendRequest(method, params = {}) {
  const request = {
    jsonrpc: "2.0",
    id: Date.now(),
    method,
    params
  };
  const message = JSON.stringify(request);
  const header = `Content-Length: ${Buffer.byteLength(message)}\r\n\r\n`;
  server.stdin.write(header + message);
}

// Collect response
let buffer = "";
server.stdout.on("data", (data) => {
  buffer += data.toString();

  // Try to parse response
  const headerEnd = buffer.indexOf("\r\n\r\n");
  if (headerEnd !== -1) {
    const headerPart = buffer.slice(0, headerEnd);
    const contentLengthMatch = headerPart.match(/Content-Length: (\d+)/);
    if (contentLengthMatch) {
      const contentLength = parseInt(contentLengthMatch[1], 10);
      const bodyStart = headerEnd + 4;
      const bodyEnd = bodyStart + contentLength;

      if (buffer.length >= bodyEnd) {
        const body = buffer.slice(bodyStart, bodyEnd);
        try {
          const response = JSON.parse(body);
          console.log("Response:", JSON.stringify(response, null, 2));
        } catch (e) {
          console.log("Raw body:", body);
        }
        buffer = buffer.slice(bodyEnd);
      }
    }
  }
});

server.stderr.on("data", (data) => {
  console.error("Server:", data.toString().trim());
});

// Test sequence
console.log("Testing MCP Server...\n");

// Initialize
setTimeout(() => {
  console.log("1. Initializing server...");
  sendRequest("initialize", {
    protocolVersion: "2024-11-05",
    capabilities: {},
    clientInfo: { name: "test-client", version: "1.0.0" }
  });
}, 100);

// List tools
setTimeout(() => {
  console.log("\n2. Listing tools...");
  sendRequest("tools/list", {});
}, 500);

// Test lookup_site_structure
setTimeout(() => {
  console.log("\n3. Testing lookup_site_structure...");
  sendRequest("tools/call", {
    name: "lookup_site_structure",
    arguments: { query: "NFL betting" }
  });
}, 1000);

// Test get_brand_rules
setTimeout(() => {
  console.log("\n4. Testing get_brand_rules...");
  sendRequest("tools/call", {
    name: "get_brand_rules",
    arguments: { section: "locked_positions" }
  });
}, 1500);

// Test list_active_briefs
setTimeout(() => {
  console.log("\n5. Testing list_active_briefs...");
  sendRequest("tools/call", {
    name: "list_active_briefs",
    arguments: {}
  });
}, 2000);

// Cleanup
setTimeout(() => {
  console.log("\nTests complete. Shutting down...");
  server.kill();
  process.exit(0);
}, 3000);
