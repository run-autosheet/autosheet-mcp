# Autosheet MCP setup: Claude Code CLI (claude-code-cli.md)

Generated from the README at [https://github.com/run-autosheet/autosheet-mcp](https://github.com/run-autosheet/autosheet-mcp) (commit 764e1e3, 2026-10-10). Do not edit by hand.

Relay these steps to the user, written out. Do not add steps that aren't listed here.

## Before you start

To use Autosheet MCP you need:

- A [GPT for Work](https://gptforwork.com/) account. You sign in with your Google account. Available usage or credits are required for agent work, but not for the sheet-copy tool. If you do not have a GPT for Work account, the sign-in process automatically creates a free-trial account for you. Once the free trial has ended, [upgrade to a paid plan](https://gptforwork.com/docs/admin/billing/subscription/manage-your-plan) to continue using the spreadsheet agent.

- Access to the Google Sheets spreadsheets you want Autosheet to work on. The spreadsheet agent requires edit access. The sheet-copy tool requires read access to the source and edit access to the destination. Autosheet accesses spreadsheets through your Google account.

Signing in. Your client authenticates to Autosheet MCP with OAuth. Autosheet opens a browser window for Google sign-in when authentication is required. Your client stores the authentication credentials and reuses them for subsequent tool calls.

TIP

The sign-in process creates an Autosheet API key. The key is how Autosheet MCP identifies you, so the agent can reach the spreadsheets your Google account can edit. You can manage the key in the [GPT for Work dashboard](https://dashboard.gptforwork.com/).

## Claude Code CLI

NOTE

If you already have [Claude connected to Autosheet MCP](https://github.com/run-autosheet/autosheet-mcp#claude), the Claude Code CLI is also connected — provided you're signed in to the CLI with the same Claude user account.

1. Open your terminal and run the following command:

    ```bash
    claude mcp add --transport http autosheet https://mcp.autosheet.com/mcp
    ```

    This adds the server for the current project only. To make the server available in all your projects, add --scope user to the command:

    ```bash
    claude mcp add --transport http autosheet https://mcp.autosheet.com/mcp --scope user
    ```

2. Start a new Claude Code CLI session.

3. Run /mcp, select autosheet, and select Authenticate. Follow the on-screen instructions to authenticate to Autosheet MCP.

You can now [use Autosheet](https://github.com/run-autosheet/autosheet-mcp#using-autosheet) in the Claude Code CLI.

## Troubleshooting connection problems

Sign-in fails, or the client says Autosheet needs authentication. Run your client's sign-in step rather than retrying the spreadsheet request. In ChatGPT and Claude, sign in again from the plugin's or connector's settings. This also covers Codex and Claude Code when they're connected through ChatGPT or Claude. If sign-in succeeds but the client still reports a problem, start a new session or chat and try again.

Browser sign-in in a terminal, a remote session, or a headless environment. In the Codex CLI, connect the Autosheet plugin in ChatGPT on any device, and then select I've installed it in the CLI. In the Claude Code CLI, connect the Autosheet connector in Claude on any device, and then start a new CLI session. Signing in from the CLI itself with /mcp needs a browser on the machine running the CLI.

Every tool call fails with a Google connection error. Connecting your client succeeds even when your Autosheet API key has no Google account attached, so the problem only shows up on the first tool call. Connect Google in the [GPT for Work dashboard](https://dashboard.gptforwork.com/), then try again.

Problems with your client itself. If your client will not add the connector or plugin, does not pick up its configuration file, does not recognize a command, or does not show the setup screens described here, that is a client-side problem rather than an Autosheet problem. Client interfaces change, so yours may differ from what is described here. Check your client's own documentation.
