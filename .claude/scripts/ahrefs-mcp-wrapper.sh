#!/bin/bash
# Wrapper script to ensure API_KEY is set for Ahrefs MCP
export API_KEY="SjPt1JPhRgqMpi5UN8G7e8P3s57SjW86734J2r1Z"
exec node /root/.global-node-modules/lib/node_modules/@ahrefs/mcp/build/index.js "$@"
