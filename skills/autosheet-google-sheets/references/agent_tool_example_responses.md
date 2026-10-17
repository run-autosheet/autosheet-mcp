# Autosheet agent tools example responses

Some clients, including Claude Code, pass only the structured response to the model; others show only the text response. Both are shown here.

## autosheet_start_agent_google_sheets_spreadsheet example response

```text
Agent 9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4
Status: busy
Usage so far: $0.0559 (turn still running)

User: In the "Pipeline" tab, add a "Weighted Value" column at the end that multiplies Deal Size by Probability, then sort the sheet by that column descending.
Assistant: I'll check the Pipeline tab's headers first so the new column picks up the existing formats.
- get_sheet_overview: SUCCEEDED - sheet=Pipeline
- read_range: SUCCEEDED - A1:H1; sheet=Pipeline; read 1x8 (8 cells)
- spreadsheet_batch_update: RUNNING

The agent is still working — this is a progress snapshot, not a failure. Poll autosheet_get_agent with agent_id "9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4" until Status is available. Do NOT start a new agent or resend the prompt: the work is already in progress and would be duplicated.

```

## autosheet_start_agent_google_sheets_spreadsheet example structured response

```json
{
  "outcome": "running",
  "agent_id": "9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4",
  "status": "busy",
  "error_message": null,
  "error_code": null,
  "usage": null,
  "usage_so_far": { "agent_usage": 41200000, "tool_usage": 14700000, "total_usage": 55900000 },
  "next_action": "Poll autosheet_get_agent with agent_id \"9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4\" until status is available. Do NOT start a new agent.",
  "response": "I'll check the Pipeline tab's headers first so the new column picks up the existing formats.",
  "messages": [
    {
      "type": "user_message",
      "content": "In the \"Pipeline\" tab, add a \"Weighted Value\" column at the end that multiplies Deal Size by Probability, then sort the sheet by that column descending."
    },
    {
      "type": "assistant_message",
      "content": "I'll check the Pipeline tab's headers first so the new column picks up the existing formats."
    }
  ],
  "tool_calls": [
    {
      "tool": "read_range",
      "status": "succeeded",
      "request": { "range": "'Pipeline'!A1:H1" },
      "response": {
        "range": "A1:H1",
        "sheet_name": "Pipeline",
        "read": { "sheets": 1, "rows": 1, "columns": 8, "cells": 8 }
      }
    }
  ]
}

```

## autosheet_start_agent_google_sheets_spreadsheet example response (action required)

```text
Action required [SPREADSHEET_NOT_NATIVE]: This file is an Excel file stored in Google Drive, not a Google Sheet, so it cannot be read or edited. Open it and use File > Save as Google Sheets, then call again with the new file's URL.

```

## autosheet_start_agent_google_sheets_spreadsheet example structured response (action required)

```json
{
  "outcome": "action_required",
  "error": {
    "message": "This file is an Excel file stored in Google Drive, not a Google Sheet, so it cannot be read or edited. Open it and use File > Save as Google Sheets, then call again with the new file's URL.",
    "code": "SPREADSHEET_NOT_NATIVE",
    "error_code": "api-spreadsheet-not-native",
    "http_status": 400,
    "request_id": "128d88f1-d484-47c4-acb1-55ef36c5218d"
  }
}

```

## autosheet_get_agent example response (available agent)

```text
Agent 1a3e43da-71b5-44c3-86f7-3a869b13e817
Status: available
Usage: $0.0559

User: Fill column C with a one-line description for each product in B2:B41.
Assistant: I'll read the product column first, then generate the descriptions into C.
- read_range: SUCCEEDED - B2:B41; sheet=Catalog; read 40x1 (40 cells)
- ai_bulk_process_rows: SUCCEEDED - C2:C41; sheet=Catalog; 40 processed, 0 errors, of 40
Assistant: Done — 40 descriptions written to column C.

```

## autosheet_get_agent example structured response (available agent)

```json
{
  "outcome": "succeeded",
  "agent_id": "1a3e43da-71b5-44c3-86f7-3a869b13e817",
  "status": "available",
  "error_message": null,
  "error_code": null,
  "usage": { "agent_usage": 41200000, "tool_usage": 14700000, "total_usage": 55900000 },
  "response": "Done — 40 descriptions written to column C.",
  "messages": [
    { "type": "user_message", "content": "Fill column C with a one-line description for each product in B2:B41." },
    { "type": "assistant_message", "content": "I'll read the product column first, then generate the descriptions into C." },
    { "type": "assistant_message", "content": "Done — 40 descriptions written to column C." }
  ],
  "tool_calls": [
    {
      "tool": "read_range",
      "status": "succeeded",
      "request": { "range": "'Catalog'!B2:B41" },
      "response": { "range": "B2:B41", "sheet_name": "Catalog", "read": { "sheets": 1, "rows": 40, "columns": 1, "cells": 40 } }
    },
    {
      "tool": "ai_bulk_process_rows",
      "status": "succeeded",
      "request": {
        "inputColumns": ["'Catalog'!B"],
        "outputColumn": "'Catalog'!C",
        "firstRow": 2,
        "lastRow": 41,
        "model": "gpt-5.4-mini",
        "promptTemplate": "Write a one-line description of <product>{{'Catalog'!B}}</product>."
      },
      "response": { "sheet_name": "Catalog", "updated_range": "C2:C41", "rows": { "processed": 40, "errors": 0, "total": 40 } }
    }
  ]
}

```

## autosheet_get_agent example response (busy agent)

```text
Agent 1a3e43da-71b5-44c3-86f7-3a869b13e817
Status: busy
Usage so far: $0.0559 (turn still running)

User: Fill column C with a one-line description for each product in B2:B41.
Assistant: I'll read the product column first, then generate the descriptions into C.
- read_range: SUCCEEDED - B2:B41; sheet=Catalog; read 40x1 (40 cells)
- ai_bulk_process_rows: RUNNING - sheet=Catalog; 17 processed, 0 errors, of 40

The agent is still working — this is a progress snapshot, not a failure. Poll autosheet_get_agent with agent_id "1a3e43da-71b5-44c3-86f7-3a869b13e817" until Status is available. Do NOT start a new agent or resend the prompt: the work is already in progress and would be duplicated.

```

## autosheet_get_agent example structured response (busy agent)

```json
{
  "outcome": "running",
  "agent_id": "1a3e43da-71b5-44c3-86f7-3a869b13e817",
  "status": "busy",
  "error_message": null,
  "error_code": null,
  "usage": null,
  "usage_so_far": { "agent_usage": 41200000, "tool_usage": 14700000, "total_usage": 55900000 },
  "next_action": "Poll autosheet_get_agent with agent_id \"1a3e43da-71b5-44c3-86f7-3a869b13e817\" until status is available. Do NOT start a new agent.",
  "response": "I'll read the product column first, then generate the descriptions into C.",
  "messages": [
    { "type": "user_message", "content": "Fill column C with a one-line description for each product in B2:B41." },
    { "type": "assistant_message", "content": "I'll read the product column first, then generate the descriptions into C." }
  ],
  "tool_calls": [
    {
      "tool": "read_range",
      "status": "succeeded",
      "request": { "range": "'Catalog'!B2:B41" },
      "response": { "range": "B2:B41", "sheet_name": "Catalog", "read": { "sheets": 1, "rows": 40, "columns": 1, "cells": 40 } }
    },
    {
      "tool": "ai_bulk_process_rows",
      "status": "running",
      "request": {
        "inputColumns": ["'Catalog'!B"],
        "outputColumn": "'Catalog'!C",
        "firstRow": 2,
        "lastRow": 41,
        "model": "gpt-5.4-mini",
        "promptTemplate": "Write a one-line description of <product>{{'Catalog'!B}}</product>."
      },
      "response": { "sheet_name": "Catalog", "rows": { "processed": 17, "errors": 0, "total": 40 } }
    }
  ]
}

```

## autosheet_follow_up_agent example response

```text
Agent 9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4
Status: available
Usage: $0.0231

User: Now highlight any row where Weighted Value is above 50000 in bold on a green fill.
Assistant: I'll apply conditional formatting across the data rows so new deals inherit the rule too.
- spreadsheet_batch_update: SUCCEEDED
Assistant: Done — rows with Weighted Value above 50,000 now render bold on a light green fill. Two rows match: Northwind and Contoso.

```

## autosheet_follow_up_agent example structured response

```json
{
  "outcome": "succeeded",
  "agent_id": "9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4",
  "status": "available",
  "error_message": null,
  "error_code": null,
  "usage": { "agent_usage": 23100000, "tool_usage": 0, "total_usage": 23100000 },
  "response": "Done — rows with Weighted Value above 50,000 now render bold on a light green fill. Two rows match: Northwind and Contoso.",
  "messages": [
    {
      "type": "user_message",
      "content": "Now highlight any row where Weighted Value is above 50000 in bold on a green fill."
    },
    {
      "type": "assistant_message",
      "content": "I'll apply conditional formatting across the data rows so new deals inherit the rule too."
    },
    {
      "type": "assistant_message",
      "content": "Done — rows with Weighted Value above 50,000 now render bold on a light green fill. Two rows match: Northwind and Contoso."
    }
  ],
  "tool_calls": []
}

```

## autosheet_stop_agent example response

```text
Agent 9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4
Status: available
Error: Agent cancelled by user.

User: Rebuild every quarterly tab from the raw export and re-link all the dashboard formulas.
Assistant: Starting with the raw export so I can map the columns before rebuilding each quarterly tab.
- get_sheet_overview: SUCCEEDED - sheet=Raw Export
- read_range: SUCCEEDED - A1:M2000; sheet=Raw Export; read 2000x13 (26000 cells)

```

## autosheet_stop_agent example structured response

```json
{
  "outcome": "cancelled",
  "agent_id": "9f3c1a4e-7d20-4b6e-8c11-2a5f0e93b7d4",
  "status": "available",
  "error_message": "Agent cancelled by user.",
  "usage": null,
  "response": "Starting with the raw export so I can map the columns before rebuilding each quarterly tab.",
  "messages": [
    {
      "type": "user_message",
      "content": "Rebuild every quarterly tab from the raw export and re-link all the dashboard formulas."
    },
    {
      "type": "assistant_message",
      "content": "Starting with the raw export so I can map the columns before rebuilding each quarterly tab."
    }
  ],
  "tool_calls": [
    {
      "tool": "read_range",
      "status": "succeeded",
      "request": { "range": "'Raw Export'!A1:M2000" },
      "response": {
        "range": "A1:M2000",
        "sheet_name": "Raw Export",
        "read": { "sheets": 1, "rows": 2000, "columns": 13, "cells": 26000 }
      }
    }
  ]
}

```
