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
argument-hint: "<prompt> on <spreadsheet_id_or_url> (sheet: <sheet_name>)"
---

Use the Autosheet MCP tools to run an agent against a Google Sheets spreadsheet.

## Instructions

1. Collect the following, asking the user only for whatever is missing:
   - The **prompt** (what they want the agent to do)
   - The **spreadsheet ID or URL** (Google Sheets — full URLs are accepted; the tool extracts the ID, and a tab id in the URL (`#gid=N`) is honored automatically)
   - The **sheet name** — only needed when the spreadsheet input doesn't already pinpoint the tab: a URL with a `gid` targets that tab, and otherwise the agent defaults to the first sheet. Don't ask for it unless the user's request is ambiguous about which tab to use.

2. Call `autosheet_run` with these parameters. The tool launches the agent, polls until it finishes (default 600s, max 600s via `timeout_seconds`), and returns the formatted result. It returns as soon as the agent finishes, so the high default is free for short jobs and lets long, multi-step jobs (translations, bulk categorization over many rows) complete in one call.

3. For follow-up turns on the same spreadsheet, pass the `agent_id` from the previous result back into `autosheet_run` along with the new `prompt` (and `sheet_name` or `sheet_id` if the turn targets a different tab).

4. If a job is so long that it still exceeds the wait, the agent keeps running server-side — don't report it as failed. The timeout error includes the agent ID (`Timed out waiting for agent <id>`); call `autosheet_status` with that `agent_id` to poll until `status` is `idle`, then present the result.

## Authentication

The Autosheet MCP server uses OAuth (scopes: `mcp:agents:run`, `mcp:agents:read`, `mcp:agents:stop`). The first time you invoke a tool, Claude Code opens your browser to authorize.

## Examples

- "Score these leads against our scoring rules" on spreadsheet `1BxiMVs0XRA5n...`
- "Validate all emails in column A and flag issues in column B" on `Sheet1`
- Follow-up: "Now sort by email_status" (pass the `agent_id` from the previous run)

## Available Tools

| Tool | Inputs | Purpose |
|------|--------|---------|
| `autosheet_run` | `prompt`, `spreadsheet_id`, `sheet_name?`, `sheet_id?`, `agent_id?`, `timeout_seconds?` (default 600, max 600) | Start a new agent or continue an existing one and wait for completion |
| `autosheet_status` | `agent_id` | Fetch latest status, messages, and tool calls for an agent |
| `autosheet_stop` | `agent_id` | Stop a running agent |
