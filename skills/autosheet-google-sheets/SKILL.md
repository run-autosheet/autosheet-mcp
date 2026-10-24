---
name: autosheet-google-sheets
description: "Use this skill for work on a Google Sheets spreadsheet: reading, updating, and analyzing data, from everyday spreadsheet work (formulas, formatting, data cleanup, restructuring, charts, pivots) to multi-step large-scale workflows involving bulk processing with AI and web search (content generation, categorization, translation, enrichment, extraction, scoring) as well as consolidating sheets from multiple spreadsheets. Use this skill when the user shares a Google Sheets URL (https://docs.google.com/spreadsheets/d/{spreadsheetId}/). The skill runs a spreadsheet-specialized Autosheet agent through the Autosheet MCP server. The agent works autonomously on the spreadsheet from a natural-language prompt. Also use when the user asks questions about Autosheet."
license: LicenseRef-Talarian-Work
compatibility: "Requires the Autosheet MCP server (https://mcp.autosheet.com/mcp) connected with OAuth, and a Google account with edit access to the target Google Sheets spreadsheets. Without the connection, the skill guides the setup."
metadata:
  author: Talarian
  version: "1.0.0"
---

# Working efficiently in Google Sheets with Autosheet

In this skill definition, "agent" always means the Autosheet agent, while "you" (explicitly or implicitly) means you, the host.

## Setup

Before using Autosheet, check whether the Autosheet MCP tools, such as autosheet_start_agent_google_sheets_spreadsheet, are available. Some clients add a prefix to MCP tool names, and some list tool names but load their definitions only on demand, so search for or load the tools before concluding they are missing.

If the tools are NOT available: Tell the user that the Autosheet MCP server must be connected at https://mcp.autosheet.com/mcp, and give them the setup steps for their client from the matching file in references/setup/ (claude.md, claude-code-cli.md, chatgpt.md, codex-cli.md, or other-clients.md for any other client), written out in your reply, not only as a link. If you cannot open that file, point the user to the README at https://github.com/run-autosheet/autosheet-mcp. Do not invent setup steps for an unsupported or unfamiliar client. While Autosheet is unavailable, do not describe or simulate what the agent would have done, and do not fall back to Google Drive or Sheets connectors for the spreadsheet work itself. Once the tools appear, continue with the user's original request.

If the tools are available: Proceed with the user's actual task. Do not make a dummy call to test the connection. Every tool needs authentication and none will work without it. The client handles authentication through OAuth and may open a browser window for Google sign-in on the first real tool call, and again if the sign-in expires. If a call fails to authenticate, ask the user to complete the sign-in or run their client's sign-in step (see references/setup/ for their client), then retry the same call once. If it still fails, report the error rather than retrying further. Two failures look like connection problems but are not:

- Every call fails with a Google connection error: The user's Autosheet account has no Google account connected. Ask them to connect one in the Autosheet dashboard (https://dashboard.autosheet.com/), then retry.
- Sign-in succeeded but the tools still fail or are missing: The client needs a new session or chat before it picks up the connection.

The authenticated Google account must have edit access to the target spreadsheet. Copying a sheet requires read access to the source spreadsheet and edit access to the destination, and does not consume usage or credits.

If the user asks about Autosheet itself, such as pricing, the company, or working in the Google Sheets sidebar instead, read references/about.md.

## Available tools

Autosheet MCP provides the following tools:

| Tool | Parameters | Purpose |
| --- | --- | --- |
| autosheet_start_agent_google_sheets_spreadsheet | prompt, spreadsheet_id | Start a new Autosheet agent. Each agent gets its own UUID (agent_id). |
| autosheet_follow_up_agent | prompt, agent_id | Send a follow-up to an existing Autosheet agent. |
| autosheet_get_agent | agent_id, wait_seconds? (default 25, max 50) | Fetch the current status and latest-turn messages and outcome for an Autosheet agent. Status can be available (it has finished its latest turn and can be followed up) or busy (it is still running and cannot yet receive a follow-up) |
| autosheet_stop_agent | agent_id | Stop a running Autosheet agent. Use when the agent is clearly going the wrong path or the user explicitly asks to stop the agent. |
| autosheet_copy_tab_from_one_spreadsheet_to_another | source_spreadsheet_id, destination_spreadsheet_id, and one of sheet_id (the gid from the URL, if present) or sheet_name (exact sheet title) | Copy a sheet to another spreadsheet, or duplicate it within the same spreadsheet. |

The four agent tools return a text summary of the latest turn and structured results with outcome, agent_id, status, and usage (see "How to run an Autosheet agent" and "How to track usage costs"). The copy tool returns its result directly: outcome and the new sheet's sheet_id and title. It has no agent_id, polling or follow-ups.

If you need to interpret a response field that isn't explained here, read references/agent_tool_example_responses.md.

## How to run an Autosheet agent

An Autosheet agent is autonomous. It explores the spreadsheet, and locates and inspects the relevant sheets and ranges. You do not need to compute ranges, row numbers, or per-cell values for it. It plans and performs read and write operations as needed, and verifies the results. To get a plan or a preview of a write operation, request it explicitly. If the task is very large or ambitious, break it down into several follow-ups.

### Running and waiting

- Each autosheet_start_agent_google_sheets_spreadsheet call starts a fresh agent with no memory of previous runs or of this conversation.
- Runs take from a few seconds to several minutes, and results may vary between runs with the same instruction.
- Start and follow-up calls wait up to about a minute for the agent to finish. Short runs complete within that time window and return the final result, including a summary of the work performed, with an agent_id. Longer runs return early with a progress snapshot and the agent_id. Continue a longer run with autosheet_get_agent until the run is complete.
- Copy the agent_id exactly from the latest tool result. Do not guess, shorten, or reuse one from another conversation.
- Do not start a second agent for work that is still running. Instead, poll the running agent or stop it. Multiple agents can work on one spreadsheet at the same time, but avoid running more than one on a given sheet unless their work is clearly separate, because they may overwrite each other's changes.

### Reading results

Check how each call ended before doing anything else. In a structured result, read outcome; in a text summary, read the Status: line and any Action required: or Error: line:

- running (text: Status: busy): The agent is still working. Poll autosheet_get_agent with the same agent_id. Do not start a new agent or resend the prompt.
- succeeded: Report what the agent did.
- failed (text: Error:): Read the error, then follow up to correct course, or start a new agent if the agent's understanding of the spreadsheet is wrong.
- cancelled: The turn was stopped, for example with autosheet_stop_agent. Anything the agent already wrote stays in the spreadsheet.
- action_required (text: Action required: or Action required [CODE]:): The user must fix something first, such as reconnecting an account, granting access, converting the file, or topping up credit. Relay the message and any dashboard link to the user exactly as given, and do not retry until they have fixed it.
- error (text: Error [CODE]:): The call itself failed. If the message says to try the same request again, retry once. Otherwise, do not assume nothing ran: Check the spreadsheet before starting again.

Status: available means the agent can take another turn, not that its last turn succeeded.

If a usage or spending limit interrupts a running agent, keep its agent_id. Once the user has fixed the limit, poll that same agent first, then follow up if needed. Do not start a new agent.

### Following up or starting a new agent

- If the new task needs the agent's memory of this session, for example to correct, refine, or extend what the agent just did, use autosheet_follow_up_agent. You do not need to repeat the context the agent already has, but be explicit about anything new. Otherwise, start a new agent.
- Start a new agent when the task is unrelated to a previous run, targets a different spreadsheet, or when the previous agent failed in a way that suggests its understanding of the spreadsheet is wrong.
- If the agent has expired, the follow-up returns an error. Start a new agent and include the context it needs, since it has no memory of the earlier run.
- The agent usually recovers from its own mistakes. If it gets stuck, stop it and steer it with a follow-up.

### Checking the agent's work

The agent will usually not return range data to you, because that would be very token inefficient. If you want to check specific values or formulas, ask for them explicitly, but sparingly. Having the agent build or read back wide helper tables is also expensive. Prefer narrow helper columns and count-based checks, such as COUNTIF or COUNTUNIQUE, over reading ranges back.

## Before changing data or spending credits

The agent works directly on the user's spreadsheet and applies changes by default. Read-only work and bulk AI processing never overwrite cells that already hold data. Other write operations can add, overwrite, move, or clear data.

- If the user shares a spreadsheet URL without saying what they want done, ask what they want before starting an agent, because every start runs a paid agent turn. If the conversation already makes the task clear, proceed.
- When the user wants data cleaned, normalized, translated, or otherwise transformed, tell the agent to write the results to a new column and leave the source column untouched, unless the user explicitly asked to replace the data in place.
- Prompt the user for permission before any step they did not explicitly request that deletes or clears pre-existing data, deletes a pre-existing sheet, or overwrites existing data.
- When a task involves deleting or clearing data, ask the agent in the same prompt to list every column, row range, or sheet it deleted or cleared, sheet by sheet. Check the list for anything outside the task.
- To regenerate a bulk column, write to a new column, or prompt the user for permission before clearing the old data.
- Before a bulk run over more than 500 rows, have the agent process a few rows first. Show the user the sample and the projected cost (see "How to track usage costs"), and prompt them for permission before the full run, unless they have asked you not to stop for permission.
- Before a large merge, split, or reclassification that depends on a business decision the user has not made, such as whether a company's branches count as one supplier, show the user the evidence and ask them to decide.
- Fix failed or incorrect rows one pass at a time: In each follow-up, ask the agent to regenerate the failing rows once and check them once. Review the outcome and usage before asking for another pass, and check the row counts: If a pass processes fewer rows than expected, or none, its row filter did not match as intended, so do not treat it as successful. Prefer formula checks for literal rules. If failures keep recurring, stop and ask the user how to proceed.
- If something went wrong, tell the user they can restore an earlier version from the spreadsheet's version history. Warn them that restoring also reverts every later change, including other people's.

The user's explicit instructions take precedence over the above defaults.

## What an Autosheet agent can do (features)

The agent handles everyday spreadsheet work: creating, fixing, and explaining formulas; analyzing data and detecting errors; building charts, pivot tables, and dashboards; looking up data; merging, moving, copy/pasting, and restructuring sheets, columns, rows, and cells; cleaning and deduplicating data; applying formatting, validation, and conditional formatting; and similar tasks.

The agent also handles row-by-row bulk processing with AI across large datasets: bulk web enrichment, categorization, translation, extraction, scoring, content generation or rewriting, and similar tasks. The agent generates the output for each row; do not produce the results yourself and pass them to the agent to write. The agent usually knows when to use AI processing versus deterministic formulas, but you can explicitly request either. When a column is a fixed function of another column, such as a label from an ID, ask for a lookup formula, not AI processing, and have the agent check the result with a formula before you report success.

The agent can also search the web and cite its sources.

Before asking the agent for stock, index, fund, currency, or crypto data in a spreadsheet, read references/googlefinance.md.

## What an Autosheet agent cannot do (and how to work around it)

The agent cannot currently:

- Work directly on Excel or CSV files (.xlsx, .xls, .csv, .tsv). The agent works only on Google Sheets spreadsheets. If the user wants, the file can be converted to Google Sheets, worked on there, and exported back to the original format. Ask the user before doing this, because they may not want a copy in their Google Drive, and Sheets does not convert Excel workbooks with high fidelity in many cases. For an Excel workbook, the user can also use the GPT for Excel add-in to work directly in the workbook.
- Read the content of a specific URL. The agent can only find information through web search.
- Analyze images.
- Show sources for bulk web enrichment.
- Record or run macros. If you have computer use, use it for that directly; Autosheet is not needed.
- Run Apps Script or other add-ons. The agent can write a script, but cannot install or run it. If you have computer use, use it to set up and run the script.
- Copy sheets between spreadsheets. Use the autosheet_copy_tab_from_one_spreadsheet_to_another tool instead.
- Export, download, or convert spreadsheet files, or create new files. Use a Google Drive connector or computer use, if available.

## Bulk AI processing and enrichment

The agent can bulk-process hundreds of thousands of rows, one row at a time, with AI prompt templates.

- The agent writes one prompt template per output column. Each template can use several input columns.
- The prompt templates run one output column at a time, respecting dependencies between columns. Within each column, the template runs row by row: For each row, its column placeholders are filled with that row's data.
- Speed: Bulk processing runs at up to about 1,000 rows per minute. The actual speed depends mostly on the AI model and provider.
- Polling for progress: Bulk runs can take minutes or even hours. Poll with autosheet_get_agent. Results report row counters for each bulk step (rows processed, errors, and total), so after the first poll you can estimate the remaining time from the elapsed time and the rows completed.
- Bulk processing works for generating or rewriting content, and also for reviewing and scoring.
- You can chain bulk operations, or ask the agent to orchestrate the chain.
- The agent can apply cleanup rules to each answer before writing it: Force answers into a list of allowed values, trim whitespace, change case, strip stray punctuation, quotes, or list numbering, or apply a find-and-replace pattern. The agent picks rules from the task, but you can ask for them. For categorization, give the exact allowed labels and ask the agent to enforce them. An answer that matches no label is replaced with the closest one, so include a fallback label such as "Other" if some rows may fit none.
- Each row is processed on its own and produces one cell. State the exact format for each output column, such as allowed values, number or date format, maximum length, or language. Several outputs per row means several output columns, each processed separately. Do not ask the bulk step for anything that compares rows, such as unique values, no repetition, or sequential numbering: The bulk step cannot see other rows. Handle those with formulas or a separate step.
- Some bulk workflows need planning: A single AI pass over every row is often less accurate and more expensive than a short chain that first narrows the work, for example deduplicating values before matching them, or selecting only the relevant glossary terms for each row. This applies to categorization with a large taxonomy, fuzzy matching and deduplication, bulk web enrichment, content generation under constraints or with varied outputs, and translation with a large glossary. For these, have the agent preview the whole chain on a few rows before any full run, following "Before changing data or spending credits".

## AI models

Autosheet uses three AI models, all set by the user in the Autosheet dashboard (https://dashboard.autosheet.com/): the default agent model, the default bulk model, and the default bulk model for web enrichment. The agent picks between the two bulk models per task, but neither you nor the agent can choose a model per call. If the user wants different quality, speed, or cost, point them to the dashboard's Models page.

## How to track usage costs

Every start and follow-up call runs a paid agent turn. The copy tool does not use credits. Tell the user the cost of each finished turn.

Tool results report the cost:

- For a finished turn, the text summary contains a Usage: line with the cost in US dollars, for example 0.0559.
- For an in-progress turn, the text summary instead contains a Usage so far: line. This is a running subtotal, so never report it as the cost of the turn.
- In structured results, usage holds the finished turn's cost in nano-dollars (divide by 1,000,000,000), and usage_so_far holds the running subtotal.

The agent cannot estimate the cost of a future run from scratch. To project a full bulk run, take the usage of a preview on a few rows and multiply it by the ratio of total rows to preview rows.

## Common patterns and use-cases

- If you prefer to resolve an ambiguity by asking the user, say so in your prompt to the agent, and it will offer you options, which you can then present to the user. Follow up with their choice.
- The agent uses formulas and helper ranges to check its own work, and may place them in the working sheets. If you want these, and any other scratch work, kept in separate, temporary sheets instead, say so in your prompt.
- You may want to ask the agent to report any decision where it departed from a literal reading of your instructions, for example after discovering how the spreadsheet is actually laid out.
- To consolidate sheets from several spreadsheets into one, use the autosheet_copy_tab_from_one_spreadsheet_to_another tool. Each copy is added as the last sheet, titled "Copy of …". Formulas that refer to sheets missing in the destination can break.

## Troubleshooting and common pitfalls

- For usage, credit, or access problems, follow the action_required rule in "How to run an Autosheet agent": Relay the message and any dashboard link to the user exactly as given.
- If the agent is clearly going the wrong way, or the user asks you to stop it, call autosheet_stop_agent. Then course-correct with a follow-up.
- Comparing versions of data (diffing) is not a native operation in Google Sheets. Do not ask the agent for diffs or try to build them yourself; use helper ranges and formulas to compare data instead.
- IMPORTRANGE needs one-time access approval: The first time a spreadsheet imports from another spreadsheet, the user must click "Allow access" in the cell. The agent cannot approve it.
- Agents expire after a week or more without activity. If a follow-up fails because the agent has expired, start a new agent and include the context it needs.
