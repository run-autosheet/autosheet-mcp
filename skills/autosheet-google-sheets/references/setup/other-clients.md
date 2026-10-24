# Autosheet MCP setup: Other MCP clients (other-clients.md)

Generated from the README at [https://github.com/run-autosheet/autosheet-mcp](https://github.com/run-autosheet/autosheet-mcp) (commit 764e1e3, 2026-10-10). Do not edit by hand.

Use this file for any client not covered by the other files in this folder. Relay these steps to the user, written out. Do not add steps that aren't listed here.

## Before you start

To use Autosheet MCP you need:

- An [Autosheet](https://autosheet.com/) account. You sign in with your Google account. Available usage or credits are required for agent work, but not for the sheet-copy tool. If you do not have an Autosheet account, the sign-in process automatically creates a free-trial account for you. Once the free trial has ended, [upgrade to a paid plan](https://autosheet.com/docs/admin/billing/subscription/manage-your-plan) to continue using the spreadsheet agent.

- Access to the Google Sheets spreadsheets you want Autosheet to work on. The spreadsheet agent requires edit access. The sheet-copy tool requires read access to the source and edit access to the destination. Autosheet accesses spreadsheets through your Google account.

Signing in. Your client authenticates to Autosheet MCP with OAuth. Autosheet opens a browser window for Google sign-in when authentication is required. Your client stores the authentication credentials and reuses them for subsequent tool calls.

TIP

The sign-in process creates an Autosheet API key. The key is how Autosheet MCP identifies you, so the agent can reach the spreadsheets your Google account can edit. You can manage the key in the [Autosheet dashboard](https://dashboard.autosheet.com/).

## Other compatible MCP clients

Any MCP client that supports remote servers over Streamable HTTP with OAuth can connect to Autosheet MCP. Point it at https://mcp.autosheet.com/mcp and complete the browser sign-in when the client prompts you.

Clients other than Claude, the Claude Code CLI, ChatGPT, and the Codex CLI have not been tested with Autosheet MCP. Configuration keys, transport names, sign-in commands, and tool permission settings differ between clients, so follow your client's own documentation for the setup steps.

## Troubleshooting connection problems

Sign-in fails, or the client says Autosheet needs authentication. Run your client's sign-in step rather than retrying the spreadsheet request. In ChatGPT and Claude, sign in again from the plugin's or connector's settings. This also covers Codex and Claude Code when they're connected through ChatGPT or Claude. If sign-in succeeds but the client still reports a problem, start a new session or chat and try again.

Browser sign-in in a terminal, a remote session, or a headless environment. In the Codex CLI, connect the Autosheet plugin in ChatGPT on any device, and then select I've installed it in the CLI. In the Claude Code CLI, connect the Autosheet connector in Claude on any device, and then start a new CLI session. Signing in from the CLI itself with /mcp needs a browser on the machine running the CLI.

Every tool call fails with a Google connection error. Connecting your client succeeds even when your Autosheet API key has no Google account attached, so the problem only shows up on the first tool call. Connect Google in the [Autosheet dashboard](https://dashboard.autosheet.com/), then try again.

Problems with your client itself. If your client will not add the connector or plugin, does not pick up its configuration file, does not recognize a command, or does not show the setup screens described here, that is a client-side problem rather than an Autosheet problem. Client interfaces change, so yours may differ from what is described here. Check your client's own documentation.
