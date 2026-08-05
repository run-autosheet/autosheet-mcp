---
name: autosheet
description: >-
  Run an AI agent on a Google Sheets spreadsheet. Use whenever the user wants
  work done in a spreadsheet or Google Sheet — adding or filling columns
  (sentiment, categories, translations, summaries, scores), cleaning,
  validating or deduplicating data, analyzing or classifying rows, extracting
  or transforming cell contents — or pastes a docs.google.com/spreadsheets
  URL. Triggers include "add a column with sentiment", "categorize my leads",
  "translate column B", "validate these emails", "analyze the feedback in my
  sheet". Do NOT use for local .xlsx/.csv files the user wants edited on disk.
argument-hint: "<prompt> on <spreadsheet_id_or_url>"
---

Use the Autosheet MCP tools to run an agent against a Google Sheets spreadsheet.

## Instructions

1. Collect the following, asking the user only for whatever is missing:
   - The **prompt** (what they want the agent to do)
   - The **spreadsheet ID or URL** (Google Sheets — full URLs are accepted; the tool extracts the ID, and a tab id in the URL (`#gid=N`) is honored automatically)

   If a specific sheet is not already selected by a URL with a `gid`, include its name in the prompt. Otherwise, the agent starts on the first sheet.

2. Call `autosheet_start_agent_google_sheets_spreadsheet` with `prompt` and `spreadsheet_id`. The tool launches the agent and returns the result when it finishes, or a running snapshot for longer jobs.

3. For follow-up turns on the same spreadsheet, call `autosheet_follow_up_agent` with the `agent_id` from the previous result and the new `prompt`.

4. If the result is still running, the agent keeps working server-side — don't report it as failed or start a new agent. Call `autosheet_get_agent` with that `agent_id` until `status` is `available`, then present the result.

## Authentication

The Autosheet MCP server uses OAuth (scopes: `mcp:agents:run`, `mcp:agents:read`, `mcp:agents:stop`). The first time you invoke a tool, Claude Code opens your browser to authorize.

## Examples

- "Score these leads against our scoring rules" on spreadsheet `1BxiMVs0XRA5n...`
- "Validate all emails in column A and flag issues in column B" on `Sheet1`
- Follow-up: "Now sort by email_status" (pass the `agent_id` from the previous run)

## Available Tools

| Tool | Inputs | Purpose |
|------|--------|---------|
| `autosheet_start_agent_google_sheets_spreadsheet` | `prompt`, `spreadsheet_id` | Start a new agent |
| `autosheet_follow_up_agent` | `prompt`, `agent_id` | Continue an existing agent |
| `autosheet_get_agent` | `agent_id`, `wait_seconds?` (default 25, max 300) | Fetch latest status, messages, and tool calls for an agent |
| `autosheet_stop_agent` | `agent_id` | Stop a running agent |
