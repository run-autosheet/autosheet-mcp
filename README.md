# Autosheet MCP

Autosheet MCP is a hosted remote MCP server. It lets compatible MCP clients run the **Autosheet spreadsheet agent** directly in your existing Google Sheets spreadsheets. You describe the work in plain language, and the agent carries it out in the spreadsheet.

You do not install or run a server. Autosheet MCP is hosted by Autosheet at a single address:

```text
https://mcp.autosheet.com/mcp
```

Autosheet MCP uses stateless Streamable HTTP transport. Access is authenticated with OAuth. The first time your client calls an Autosheet tool, it opens your browser so you can sign in. Clients can list the available tools before signing in; running one requires sign-in.

You set up Autosheet MCP by connecting directly to the hosted server. This works in every client covered below and gives you the [full set of Autosheet tools](#tool-reference).

Dedicated setup instructions are provided for [Claude](#claude), [Claude Code](#claude-code), [ChatGPT](#chatgpt), and [Codex](#codex). You can also use [any other MCP client](#other-compatible-mcp-clients) that supports remote servers over Streamable HTTP with OAuth.

For more about the product, see [autosheet.com](https://autosheet.com/).

## Get started

### Before you start

To use Autosheet MCP you need:

- A GPT for Work account.

- Membership of a [GPT for Work space](https://gptforwork.com/docs/resources/guides/concepts#space) that has usage or credits available.

- Edit access to the Google Sheets spreadsheets you want the agent to work on.

**Signing in.** Your client authenticates to Autosheet MCP with OAuth. The first Autosheet tool call opens a browser window for sign-in. After that, your client stores the credentials and reuses them. Separately, the agent works on spreadsheets through your Google account, so it can only reach spreadsheets that your account is allowed to edit.

**Approving tool calls.** MCP clients ask you to approve tool calls before they run. Where that prompt appears, how it is worded, and whether you can pre-approve a tool all vary by client. The tools that start work declare themselves as making changes, so clients that act on that will prompt you before the agent touches a spreadsheet; checking status is declared read-only and is usually not prompted. Keep approval required for the tools that make changes rather than allowing them automatically. For more information, see [Important behavior and safe use](#important-behavior-and-safe-use).

**Telling the agent which spreadsheet to use.** Give the agent either the full Google Sheets URL or the bare spreadsheet ID. In a URL, the ID is the part between `/d/` and `/edit`. For example, in the URL `https://docs.google.com/spreadsheets/d/1etZyGGQPami0R9D2W6WlJMWbrd_JvStLDdsteFegnko/edit`, the ID is `1etZyGGQPami0R9D2W6WlJMWbrd_JvStLDdsteFegnko`.

**Telling the agent which sheet to work on.** Copy the URL while the sheet you want is open. A Google Sheets URL carries a tab id, such as `#gid=123456`, and the agent starts on that sheet. A bare spreadsheet ID, or a URL without a tab id, starts the agent on the first sheet. Either way, naming a sheet in your instruction takes precedence — for example, "clean up the emails on the Contacts sheet". The agent can explore the spreadsheet and move between sheets as the work requires, so the starting sheet is a starting point rather than a boundary.

### Claude

To connect Claude to Autosheet MCP:

1. Open Claude in your browser or in the Claude desktop app.

1. In the main sidebar, click your user name and select **Settings**.

1. In the settings sidebar, select **Customize > Connectors**.

1. Click **Add > Browse connectors**.

1. Search for `Autosheet`.

1. Click the **+** button for **Autosheet**.

1. Follow the on-screen instructions to authenticate to Autosheet MCP.

### Claude Code

> **NOTE!** If you've [installed the Autosheet connector for Claude](#claude), Claude Code is already connected to Autosheet MCP — provided you're signed in to Claude Code with the same Claude user account. If you have not or cannot install the connector in Claude, follow the instructions below.

To connect Claude Code to Autosheet MCP:

1. Open your terminal and run the following command:

   ```bash
   claude mcp add --transport http autosheet https://mcp.autosheet.com/mcp
   ```

   This adds the server for the current project only. To make the server available in all your projects, append the command with `--scope user`:

   ```bash
   claude mcp add --transport http autosheet https://mcp.autosheet.com/mcp --scope user
   ```

1. Start a new Claude Code session.

1. Run `/mcp`, select `autosheet`, and select `Authenticate`. Follow the on-screen instructions to authenticate to Autosheet MCP.

### ChatGPT

> **NOTE!** You connect ChatGPT to Autosheet MCP by configuring a custom plugin. You need to enable developer mode to install and use custom plugins.

To connect ChatGPT to Autosheet MCP:

1. Open ChatGPT in your browser.

1. In the main sidebar, click your user name and select **Settings**.

1. Enable developer mode:

   1. In the settings sidebar, select **Plugins**.

   1. At the bottom of the panel, select **Developer mode**.

   1. Enable **Developer mode**.

1. Install the plugin:

   1. In the settings sidebar, select **Plugins**.

   1. At the bottom of the panel, select **Browse plugins**.

   1. At the top of the panel, click the **+** button.

   1. Define the plugin settings:

      - **Name**: Enter `Autosheet`.

      - **Connection**: Select **Server URL** and enter `https://mcp.autosheet.com/mcp`.

      - Check **I understand and want to continue**.

   1. Click **Create**.

   1. Follow the on-screen instructions to authenticate to Autosheet MCP.

### Codex

To connect Codex to Autosheet MCP for all projects:

1. Open your terminal and run the following command:

   ```bash
   codex mcp add autosheet --url https://mcp.autosheet.com/mcp
   ```

1. Follow the on-screen instructions to authenticate to Autosheet MCP.

To connect Codex to Autosheet MCP for a specific project:

1. Open `<project>/.codex/config.toml` in an editor and add the following configuration:

   ```toml
   [mcp_servers.autosheet]
   url = "https://mcp.autosheet.com/mcp"
   ```

1. Save the file.

1. Open your terminal, change to the project directory, and run the following command:

   ```bash
   codex mcp login autosheet
   ```

1. Follow the on-screen instructions to authenticate to Autosheet MCP.

### Other compatible MCP clients

Any MCP client that supports remote servers over Streamable HTTP with OAuth can connect to Autosheet MCP. Point it at `https://mcp.autosheet.com/mcp` and complete the browser sign-in when the client prompts you.

Clients other than the ones above have not been tested with Autosheet MCP. Configuration keys, transport names, and sign-in commands differ between clients, so follow your client's own documentation for the setup steps.

## How Autosheet MCP works

You describe the work you want done in plain language. Your MCP client passes that instruction, along with the spreadsheet you identified, to Autosheet MCP. The spreadsheet agent runs on Autosheet's servers, works through the spreadsheet, and reports back a summary of what it did.

**Starting work.** When you ask for spreadsheet work, your client calls the start tool with your instruction and the spreadsheet. The agent begins working in the spreadsheet.

**Following up.** After the agent reports back, you can keep going in the same conversation. Your client calls the follow-up tool, which continues with the same agent rather than starting a new one. Use this for corrections and for work that builds on what the agent just did.

**Long runs.** Short jobs finish inside the first call and come straight back. Longer jobs do not hold the call open: it returns quickly with a progress snapshot, and the agent carries on working on Autosheet's servers. **A snapshot is not a failure.** Your client then polls the status tool until the agent is idle and collects the result. The status tool waits a short while for the agent before answering, so polling costs few calls. If your client reports work as failed or starts a second agent for the same instruction, that is the client mishandling a snapshot — see [Troubleshooting and support](#troubleshooting-and-support).

**Stopping.** If the agent is doing the wrong thing, ask your client to stop it. Work already written to the spreadsheet stays there. See [Important behavior and safe use](#important-behavior-and-safe-use).

Clients display all of this differently. Tool names, approval prompts, and progress reporting vary, so what you see depends on the client you use.

### Tool reference

| Tool | Title | What it does | Inputs |
| --- | --- | --- | --- |
| `autosheet_start_agent` | Start an Autosheet agent | Starts a new agent on a spreadsheet with your instruction. | `prompt`, `spreadsheet_id` |
| `autosheet_follow_up_agent` | Follow up with an Autosheet agent | Continues an existing agent conversation with a new instruction. | `prompt`, `agent_id` |
| `autosheet_get_agent` | Get the status of an Autosheet agent | Reports the current status, messages, and progress of an agent. | `agent_id` |
| `autosheet_stop_agent` | Stop an Autosheet agent | Stops an agent that is still running. | `agent_id` |

Notes on the inputs:

- `spreadsheet_id` accepts either a bare Google Sheets ID or a full spreadsheet URL. A tab id in the URL sets the sheet the agent starts on.

- `agent_id` identifies an agent that is already running. Your client takes it from the previous result — you do not need to handle it yourself.

- A follow-up takes no spreadsheet input. It continues on the agent's own spreadsheet and current sheet, which is why it cannot be redirected to a different spreadsheet. If you want to work on a new spreadsheet, start a new agent.

## What you can do

Autosheet handles most of the work you would otherwise do by hand in your spreadsheet. The agent explores the spreadsheet and its sheets, plans the work, does it, checks its own results, and corrects its mistakes.

**Everyday spreadsheet work** — formulas, structure, analysis, and formatting:

- "Write a formula in column F that flags any order over 30 days old and still unpaid."

- "Explain what the formula in G2 does and why it returns an error."

- "Clean up the company names in column B and remove the duplicate rows."

- "Validate every email address in column A and flag the bad ones in column D."

- "Build a pivot table of revenue by region and quarter on a new sheet."

- "Add conditional formatting so anything below target turns red."

- "Merge the two contact sheets and reconcile the duplicates."

**Bulk processing, row by row** — the agent works out its own approach and applies it across the whole range:

- "Score every lead in this spreadsheet against our scoring rules and put the score in column H."

- "Categorize each support ticket by topic and add the category in a new column."

- "For every company in column A, look up the CEO and the headcount and fill them in."

- "Translate the product descriptions in column C into German."

- "Work through the responses sheet and tag each row with a sentiment."

The agent can research on the web when the work needs information that is not already in the spreadsheet. For work it cannot do, see [Autosheet limitations](#autosheet-limitations).

## Important behavior and safe use

**The agent works directly in your spreadsheet.** It can add, overwrite, move, and clear content. It is not working on a copy.

**The agent applies changes by default.** It does not propose a plan and wait for you to accept it. If you want to see the intended approach before anything is written, ask for it explicitly — for example, "plan this first and show me before you change anything". For bulk work, you can ask the agent to do a few rows first so you can check the result before it processes the rest.

**Permissions matter.** The agent works through your Google account and can change anything that account can edit in the spreadsheets you point it at. Check that you are pointing it at the right spreadsheet before you start, particularly with a shared spreadsheet where other people depend on the data.

**Keep write approval on.** MCP clients let you approve tool calls before they run, and some let you pre-approve a tool so it runs without asking. Leave approval required for the Autosheet start and follow-up tools. The approval prompt is the point where you can see which spreadsheet is about to be changed and stop a request that names the wrong one.

**Recovering earlier content.** You can review or restore earlier versions of a spreadsheet using Google Sheets version history. Restoring an earlier version also reverts other changes made to the spreadsheet since that version, including changes made by other people. For more information, see [Find what's changed in a file](https://support.google.com/docs/answer/190843) (Google Docs Editors Help).

**Check the server address.** The only official Autosheet MCP server address is `https://mcp.autosheet.com/mcp`. If you are asked to add an Autosheet connector at a different address, do not add it.

## Platforms and compatibility

| Client | Tested | Direct connection | Restrictions to know |
| --- | --- | --- | --- |
| Claude | Yes | Yes | None |
| Claude Code | Yes | Yes | None |
| ChatGPT | Yes | Yes | Developer mode must be enabled. |
| Codex | Yes | Yes | None |
| Other MCP clients | No | Yes, if the client supports Streamable HTTP with OAuth | Untested. Follow your client's own documentation. |

Every client needs Streamable HTTP support and OAuth to connect.

**Tested** means the setup steps in this document have been run on that client and the spreadsheet agent confirmed working end to end. **No** means untested rather than incompatible: Any client that supports Streamable HTTP with OAuth should be able to connect, but you will need to work out the setup details from your client's own documentation.

## Autosheet limitations

Autosheet works with existing Google Sheets spreadsheets only. It does not work with local `.xlsx`, `.xls`, `.csv`, or `.tsv` files.

The spreadsheet agent cannot currently:

- See a spreadsheet visually or use color-based logic
- Record or run a macro
- Run Apps Script or other add-ons
- Convert or download a spreadsheet to other formats
- Make copies of a spreadsheet or create new files

## Troubleshooting and support

**Sign-in fails, or the client says Autosheet needs authentication.** Run your client's sign-in step rather than retrying the spreadsheet request: `/mcp` in Claude Code, `codex mcp login autosheet` in Codex. In Claude and ChatGPT, the browser sign-in starts from the first tool call. If sign-in succeeds but the client still reports a problem, start a new session or chat and try again.

**Browser sign-in in a terminal, a remote session, or a headless environment.** Sign-in needs a browser on the machine running the client. In Codex, `mcp_oauth_callback_port` and `mcp_oauth_callback_url` let you control the callback so it can reach a remote machine.

**Claude cannot reach the server, but your network can.** Remote connectors are brokered from Anthropic's servers, not from your machine. This is true in Claude Desktop and in Cowork as well. A firewall rule or VPN on your own machine is therefore not the cause, and allowing the address locally will not change the result.

**The agent cannot open the spreadsheet.** Check that the Google account you signed in with has edit access to that spreadsheet, and that the spreadsheet has not been moved or deleted.

**The spreadsheet URL or ID is rejected.** Supply either the full Google Sheets URL or the bare ID. In a URL such as `https://docs.google.com/spreadsheets/d/1etZyGGQPami0R9D2W6WlJMWbrd_JvStLDdsteFegnko/edit`, the ID is the part between `/d/` and `/edit`. Links from other Google products, and shortened links, may not contain the ID.

**The agent worked on the wrong sheet.** Name the sheet in your instruction — that takes precedence over everything else. Otherwise the agent starts on the sheet identified by the tab ID in the URL you supplied, or on the first sheet if you supplied a bare spreadsheet ID or a URL without one. Copying the URL while the sheet you want is open is the simplest way to get this right.

**A follow-up went to the wrong spreadsheet.** A follow-up always continues on the agent's own spreadsheet and cannot be pointed at a different one. Start a new agent instead.

**Work is taking a long time.** Longer jobs return a progress snapshot rather than holding the call open, and the agent keeps running on Autosheet's servers. This is normal and is not a failure. Ask your client to check the agent's status rather than repeating the instruction — repeating it starts a second agent on the same spreadsheet, and the two will collide.

**The client reported the work as failed, or started over.** Some clients misread a progress snapshot as an error or a timeout. Check the spreadsheet and ask the client for the agent's status before running anything again.

**Continuing a conversation with the agent.** Ask your client to follow up rather than describing the whole task again. This continues with the same agent, which still has the context of what it just did.

**Stopping work in progress.** Ask your client to stop the agent. Anything already written to the spreadsheet stays there. To get back to an earlier state, use Google Sheets version history. For more information, see [Important behavior and safe use](#important-behavior-and-safe-use).

**Problems with your client itself.** If your client will not add the connector or plugin, does not pick up its configuration file, does not recognize a command, or does not show the setup screens described here, that is a client-side problem rather than an Autosheet problem. Client interfaces change, so yours may differ from what is described here. Check your client's own documentation.

**Support and policies.**

- [Contact support](https://support.gptforwork.com/hc/en-us/requests/new)

- [Trust center](https://security.talarian.io) — certifications, security practices, and vulnerability reporting

- [Security and privacy FAQ](https://gptforwork.com/help/get-started/security-privacy-faq)

- [Privacy policy](https://talarian.io/privacy-policy)

- [Terms of service](https://gptforwork.com/terms-of-service)

- [Data processing agreement](https://talarian.io/data-processing-agreement)

- [Pricing](https://gptforwork.com/pricing)

- [Release notes](https://gptforwork.com/help/get-started/release-notes)

To report a security vulnerability, follow the responsible disclosure process on the [Talarian trust center](https://security.talarian.io).

To report a bug in this documentation, open an issue on this repository.

## About this repository

This repository is the canonical documentation for Autosheet MCP.

You do not need anything from this repository to use Autosheet MCP. Connecting a client directly to `https://mcp.autosheet.com/mcp` is enough, and there is no server for you to install or run.

The MCP server source is not in this public repository and is not open source.

## License

[MIT](LICENSE)
