# Autosheet MCP setup: ChatGPT (chatgpt.md)

Generated from the README at [https://github.com/run-autosheet/autosheet-mcp](https://github.com/run-autosheet/autosheet-mcp) (commit 764e1e3, 2026-10-10). Do not edit by hand.

Relay these steps to the user, written out. Do not add steps that aren't listed here.

## Before you start

To use Autosheet MCP you need:

- An [Autosheet](https://autosheet.com/) account. You sign in with your Google account. Available usage or credits are required for agent work, but not for the sheet-copy tool. If you do not have an Autosheet account, the sign-in process automatically creates a free-trial account for you. Once the free trial has ended, [upgrade to a paid plan](https://autosheet.com/docs/admin/billing/subscription/manage-your-plan) to continue using the spreadsheet agent.

- Access to the Google Sheets spreadsheets you want Autosheet to work on. The spreadsheet agent requires edit access. The sheet-copy tool requires read access to the source and edit access to the destination. Autosheet accesses spreadsheets through your Google account.

Signing in. Your client authenticates to Autosheet MCP with OAuth. Autosheet opens a browser window for Google sign-in when authentication is required. Your client stores the authentication credentials and reuses them for subsequent tool calls.

TIP

The sign-in process creates an Autosheet API key. The key is how Autosheet MCP identifies you, so the agent can reach the spreadsheets your Google account can edit. You can manage the key in the [Autosheet dashboard](https://dashboard.autosheet.com/).

## ChatGPT

Install the [Autosheet plugin from the ChatGPT plugins directory](https://chatgpt.com/plugins/plugin_asdk_app_6aa196d5c8488191a3de00c74c9534ac). Installing the plugin makes Autosheet available in ChatGPT and Codex, including the Codex CLI.

Follow the instructions for your ChatGPT account type:

- [Personal account](https://github.com/run-autosheet/autosheet-mcp#chatgpt-personal-account)

- [Organization account](https://github.com/run-autosheet/autosheet-mcp#chatgpt-organization-account) — Part of a managed workspace

### ChatGPT personal account

1. Sign in to ChatGPT in your browser or in the ChatGPT desktop app.

    If you're in the browser, you can go directly to the [Autosheet plugin's directory listing](https://chatgpt.com/plugins/plugin_asdk_app_6aa196d5c8488191a3de00c74c9534ac), click Install plugin, and continue from step 5.

2. In the sidebar, select Plugins.

3. Search for Autosheet.

4. Click the + button for Autosheet. In the ChatGPT desktop app, click Install instead.

5. Click Continue to Autosheet.

6. Follow the on-screen instructions to authenticate to Autosheet MCP with your Google account.

You can now [use Autosheet](https://github.com/run-autosheet/autosheet-mcp#using-autosheet) in ChatGPT as well as in Codex, including the Codex CLI.

### ChatGPT organization account

A workspace admin or owner must first make the Autosheet plugin available to workspace members. Once the plugin is available, members can individually connect to Autosheet MCP.

#### Add the Autosheet plugin to your ChatGPT workspace

If you're a workspace admin or owner:

1. Sign in to the [OpenAI Admin Console](https://admin.openai.com/).

2. In the sidebar, select Plugins.

3. Search for Autosheet.

4. In the public search results, select Autosheet.

5. Click Enable.

6. In the Availability section, select how you want to make the Autosheet plugin available to your workspace members:

    - Available: Members can search for and install the plugin if they want to use Autosheet.

    - Installed: Members have the plugin preinstalled, but they still need to authenticate before they can use Autosheet.

7. Check and configure the other plugin settings. For more information, see the [OpenAI documentation](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors).

The Autosheet plugin is now available to your workspace members. To connect to Autosheet MCP, members can follow the instructions in [Connect ChatGPT to Autosheet MCP](https://github.com/run-autosheet/autosheet-mcp#connect-chatgpt-to-autosheet-mcp).

#### Connect ChatGPT to Autosheet MCP

- If the Autosheet plugin is not available in your workspace, ask your workspace admin or owner to add it. They can follow the instructions in [Add the Autosheet plugin to your ChatGPT workspace](https://github.com/run-autosheet/autosheet-mcp#add-the-autosheet-plugin-to-your-chatgpt-workspace).

- If the Autosheet plugin is available but not preinstalled in your workspace, follow the instructions in [ChatGPT personal account](https://github.com/run-autosheet/autosheet-mcp#chatgpt-personal-account).

- If the Autosheet plugin is preinstalled in your workspace:

    1. Sign in to ChatGPT in your browser or in the ChatGPT desktop app.

        If you're in the browser, you can go directly to the [Autosheet plugin's directory listing](https://chatgpt.com/plugins/plugin_asdk_app_6aa196d5c8488191a3de00c74c9534ac), click Manage, and continue from step 5.

    2. In the sidebar, select Plugins.

    3. Under Installed, select Autosheet.

    4. Click Manage.

    5. Click Connect.

    6. Click Continue to Autosheet.

    7. Follow the on-screen instructions to authenticate to Autosheet MCP with your Google account.

You can now [use Autosheet](https://github.com/run-autosheet/autosheet-mcp#using-autosheet) in ChatGPT as well as in Codex, including the Codex CLI.

## Troubleshooting connection problems

Sign-in fails, or the client says Autosheet needs authentication. Run your client's sign-in step rather than retrying the spreadsheet request. In ChatGPT and Claude, sign in again from the plugin's or connector's settings. This also covers Codex and Claude Code when they're connected through ChatGPT or Claude. If sign-in succeeds but the client still reports a problem, start a new session or chat and try again.

Every tool call fails with a Google connection error. Connecting your client succeeds even when your Autosheet API key has no Google account attached, so the problem only shows up on the first tool call. Connect Google in the [Autosheet dashboard](https://dashboard.autosheet.com/), then try again.

Problems with your client itself. If your client will not add the connector or plugin, does not pick up its configuration file, does not recognize a command, or does not show the setup screens described here, that is a client-side problem rather than an Autosheet problem. Client interfaces change, so yours may differ from what is described here. Check your client's own documentation.
