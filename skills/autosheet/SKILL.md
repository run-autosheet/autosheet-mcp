---
name: autosheet
description: Use Autosheet to clean, transform, enrich, or analyze data in an existing Google Sheets spreadsheet, continue an Autosheet agent, check progress, stop work, or copy a spreadsheet tab using the connected Autosheet MCP tools.
---

# Autosheet

Use the connected Autosheet tools for work in Google Sheets. Discover the available
tools and their current schemas before calling them; deployments can customize
tool names and descriptions. If the connection is missing, ask the user to connect
Autosheet and complete its OAuth sign-in. Never ask for access tokens or API keys
in chat.

## Start or continue work

- Obtain the target spreadsheet URL or ID and the user's requested change. Preserve
  a supplied `gid` so the agent starts on the intended tab. Ask for a missing target
  rather than guessing one.
- Start work with `autosheet_start_agent_google_sheets_spreadsheet`, passing the
  spreadsheet and a clear instruction including the user's constraints.
- Continue an existing agent with `autosheet_follow_up_agent` and the returned
  `agent_id`. A follow-up stays on the original spreadsheet. Start a new agent when
  the user changes spreadsheets.
- Use `autosheet_copy_tab_from_one_spreadsheet_to_another` when available for a
  direct tab-copy request. Follow its schema for source, tab, and destination.
  Each successful call creates another tab; do not automatically retry after an
  ambiguous response.
- These tools can change spreadsheet data and consume account usage. Stay within
  the user's requested work and honor the host's approval controls.

## Follow work to completion

A `running` outcome means the agent is still working. Keep the returned agent ID
and call `autosheet_get_agent` using its default long-poll wait. Repeat while work
is running; avoid tight loops with `wait_seconds: 0`. If the host cannot continue
polling, report the current state and agent ID without claiming completion.

Use `autosheet_stop_agent` when the user asks to stop. Stopping does not imply
that earlier spreadsheet edits were undone.

Read `structuredContent` when present. Distinguish `succeeded`, `failed`,
`cancelled`, and `error` from `running`. Summarize confirmed results and errors,
link the spreadsheet, and distinguish requested changes from observed results.
Never report success solely because a start or follow-up request was accepted.
