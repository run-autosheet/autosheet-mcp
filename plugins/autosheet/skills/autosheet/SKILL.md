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
   - The **spreadsheet ID or URL** — Google Sheets spreadsheet ID or full spreadsheet URL. If the URL carries a tab id (`#gid=N`), the agent starts on that tab; a bare ID (or a URL without a `gid`) starts on the first sheet. This is only a starting point — if the prompt names a sheet to work on, the agent uses that one instead.

2. Call `autosheet_start_agent_google_sheets_spreadsheet` with `prompt` and `spreadsheet_id`. The call waits up to 60 seconds. Short runs complete inside that window and return a summary of work performed along with an `agent_id`; longer runs return early with an `agent_id` and a progress snapshot.

3. For follow-up turns on the same spreadsheet, call `autosheet_follow_up_agent` with the `agent_id` from the previous result and the new `prompt`.

4. If a run returns early, call `autosheet_get_agent` with its `agent_id` until `status` is `available`, then present the result.

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
