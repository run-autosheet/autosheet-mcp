# Autosheet MCP setup: Claude (claude.md)

Generated from the README at [https://github.com/run-autosheet/autosheet-mcp](https://github.com/run-autosheet/autosheet-mcp) (commit 764e1e3, 2026-10-10). Do not edit by hand.

Relay these steps to the user, written out. Do not add steps that aren't listed here.

## Before you start

To use Autosheet MCP you need:

- A [GPT for Work](https://gptforwork.com/) account. You sign in with your Google account. Available usage or credits are required for agent work, but not for the sheet-copy tool. If you do not have a GPT for Work account, the sign-in process automatically creates a free-trial account for you. Once the free trial has ended, [upgrade to a paid plan](https://gptforwork.com/docs/admin/billing/subscription/manage-your-plan) to continue using the spreadsheet agent.

- Access to the Google Sheets spreadsheets you want Autosheet to work on. The spreadsheet agent requires edit access. The sheet-copy tool requires read access to the source and edit access to the destination. Autosheet accesses spreadsheets through your Google account.

Signing in. Your client authenticates to Autosheet MCP with OAuth. Autosheet opens a browser window for Google sign-in when authentication is required. Your client stores the authentication credentials and reuses them for subsequent tool calls.

TIP

The sign-in process creates an Autosheet API key. The key is how Autosheet MCP identifies you, so the agent can reach the spreadsheets your Google account can edit. You can manage the key in the [GPT for Work dashboard](https://dashboard.gptforwork.com/).

## Claude

Install the [Autosheet connector from the Claude connectors directory](https://claude.ai/directory/connectors/autosheet). Installing the connector makes Autosheet available in Claude and Claude Code.

Follow the instructions for your Claude account type:

- [Personal account](https://github.com/run-autosheet/autosheet-mcp#claude-personal-account) — Free, Pro, or Max plan

- [Organization account](https://github.com/run-autosheet/autosheet-mcp#claude-organization-account) — Part of a team

### Claude personal account

1. Open Claude in your browser or in the Claude desktop app.

    If you're in the browser, you can go directly to the [Autosheet connector's directory listing](https://claude.ai/directory/connectors/autosheet) and continue from step 6.

2. In the main sidebar, click your user name and select Settings.

3. In the settings sidebar, select Customize > Connectors.

4. Search for Autosheet.

5. Select Autosheet.

6. Click Connect to Claude.

7. Follow the on-screen instructions to authenticate to Autosheet MCP.

You can now [use Autosheet](https://github.com/run-autosheet/autosheet-mcp#using-autosheet) in Claude.

### Claude organization account

An organization owner must first make the Autosheet connector available to organization members. Once the connector is available, members can individually authenticate to Autosheet MCP.

#### Add the Autosheet connector to your Claude organization

If you're an organization owner:

1. Open Claude in your browser or in the Claude desktop app.

2. In the main sidebar, click your user name and select Organization settings.

3. In the settings sidebar, select Plugins > Connectors.

4. Click Add > All available.

5. Search for Autosheet.

6. Click the + button for Autosheet.

7. Click Connect for your team.

8. (Optional) To modify the tool permission restrictions for your organization:

    1. Select the Tools tab.

    2. Check the permission restrictions and adjust them as needed.

The Autosheet connector is now available to your organization members.

#### Connect Claude to Autosheet MCP

1. Open Claude in your browser or in the Claude desktop app.

    If you're in the browser, you can go directly to the [Autosheet connector's directory listing](https://claude.ai/directory/connectors/autosheet), click Connect, and continue from step 5.

2. In the main sidebar, click your user name and select Settings.

3. In the settings sidebar, select Customize > Connectors.

4. Click Connect for Autosheet.

5. Follow the on-screen instructions to authenticate to Autosheet MCP.

6. (Optional) To modify the tool permissions:

    1. In the connectors list, select Autosheet.

    2. In the Tool permissions section, check the permissions and adjust them as needed.

You can now [use Autosheet](https://github.com/run-autosheet/autosheet-mcp#using-autosheet) in Claude.

## Troubleshooting connection problems

Sign-in fails, or the client says Autosheet needs authentication. Run your client's sign-in step rather than retrying the spreadsheet request. In ChatGPT and Claude, sign in again from the plugin's or connector's settings. This also covers Codex and Claude Code when they're connected through ChatGPT or Claude. If sign-in succeeds but the client still reports a problem, start a new session or chat and try again.

Claude cannot reach the server, but your network can. Remote connectors are brokered from Anthropic's servers, not from your machine. This is true in Claude Desktop and in Cowork as well. A firewall rule or VPN on your own machine is therefore not the cause, and allowing the address locally will not change the result.

Every tool call fails with a Google connection error. Connecting your client succeeds even when your Autosheet API key has no Google account attached, so the problem only shows up on the first tool call. Connect Google in the [GPT for Work dashboard](https://dashboard.gptforwork.com/), then try again.

Problems with your client itself. If your client will not add the connector or plugin, does not pick up its configuration file, does not recognize a command, or does not show the setup screens described here, that is a client-side problem rather than an Autosheet problem. Client interfaces change, so yours may differ from what is described here. Check your client's own documentation.
