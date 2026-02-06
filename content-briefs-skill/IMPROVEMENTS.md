# System Improvements - December 2025

## Overview
This document tracks improvements made to the content brief generation system.

## Ahrefs API Script Improvements

### 1. Environment Variable Support
- API key can now be set via `AHREFS_API_KEY` environment variable
- Fallback to embedded key for backward compatibility
- See `.env.example` for configuration

### 2. Retry Logic for Transient Errors
- Automatic retry with exponential backoff for 503 errors
- Default: 3 retries with 1s, 2s, 4s delays
- Prevents brief generation failures from transient network issues

### 3. Response Caching
- 1-hour cache for API responses
- Reduces redundant API calls during brief generation
- Cache is in-memory (resets on script restart)

### 4. Logging
- All API requests logged with timestamps
- Errors logged with full context
- Logs to stderr to not interfere with JSON output

### 5. Parameter Validation
- Required parameters validated before API call
- Clear error messages for missing parameters
- Prevents 400 errors from invalid requests

## DOCX Conversion Improvements

### Optional MD Cleanup
- New `--cleanup-md` flag removes source .md files after conversion
- Only deletes after successful .docx creation
- Usage: `python convert_to_docx.py --all --cleanup-md`

## Usage Examples

### Setting API Key
```bash
export AHREFS_API_KEY="your_key_here"
python3 .claude/scripts/ahrefs-api.py keywords-explorer/overview '{"select":"keyword,volume","country":"us","keywords":"test"}'
```

### Converting with Cleanup
```bash
python3 content-briefs-skill/scripts/convert_to_docx.py --all --cleanup-md
```
