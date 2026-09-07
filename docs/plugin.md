# Autosheet plugin packaging

This repository contains a distributable plugin for the production MCP endpoint
`https://mcp.autosheet.com/mcp`. Plugin versioning is independent of the server's
package version. No server build or local credentials are needed to distribute it.

## Package layout

The root package is a separate, standalone entry point named `autosheet-mcp`,
serving OpenAI (ChatGPT and Codex) and Agent Plugins 1.0 clients. It is distinct
from the release-managed marketplace package under `plugins/autosheet/`, which
remains the target of the Claude and Codex marketplaces declared in
`.claude-plugin/marketplace.json` and `.agents/plugins/marketplace.json`. Install
one entry point at a time. Root-package changes do not update the release-managed
package: its updates are made in the internal upstream and promoted through that
project's release process.

| Path | Purpose |
| --- | --- |
| `.codex-plugin/plugin.json` | Native OpenAI plugin manifest, including the `interface` listing block |
| `.mcp.json` | Native OpenAI HTTP MCP connection, referenced by the manifest's `mcpServers` field |
| `plugin.json` | Agent Plugins 1.0 manifest, matching Exa's layout |
| `mcp.json` | Agent Plugins 1.0 Streamable HTTP connection |
| `docs/plugin.md` | Installation and verification instructions |

The root package ships no `.claude-plugin/plugin.json`. Claude installs
`plugins/autosheet/` through the marketplace, and OpenAI's portal prefers
`.codex-plugin/plugin.json`; a second Claude manifest at the root would offer a
duplicate, differently-named install of the same server.

It also ships no branding images. `interface.brandColor` and
`interface.brandColorDark` carry the brand for local marketplace installs and
workspace publishing. The public directory listing does not read this manifest
at all: the **With MCP** submission is a portal form, and the logo is uploaded
there (the portal caps that upload at roughly 10 KB). `interface.logo` and
`interface.composerIcon` are only validated when the package itself is uploaded
as a ZIP, so add them only if that path is ever used. Render any logo from the
official mark at `https://autosheet.com/icon.svg` rather than committing a
hand-traced copy.

The native MCP file uses `type: "http"`; the Agent Plugins file uses
`type: "streamable-http"`. Both target the same server. Keep the identity,
description, and version aligned across manifests and the URLs aligned across
MCP files. Each client should load the format it supports; do not manually install
both MCP declarations into the same client.

Create an upload archive from the repository root with this explicit file list:

```bash
zip /tmp/autosheet-mcp-plugin.zip .codex-plugin/plugin.json .mcp.json plugin.json mcp.json docs/plugin.md
```

Use a fresh archive filename for subsequent releases. Do not archive the entire
server repository: its source, environment files, and infrastructure documentation
are not part of the plugin. This package does not create a personal marketplace
or change any installed client configuration.

## Listing metadata constraints

OpenAI validates `.codex-plugin/plugin.json` at upload and again, more strictly,
at directory submission. The limits that bind the current manifest:

| Field | Rule |
| --- | --- |
| `name` | ASCII letters, digits, `_`, `-`; starts alphanumeric; at most 64 characters |
| `version` | Semantic version; a new release must change it |
| `description` | Required, at most 1,024 characters |
| `author.name` | Required, and must match `interface.developerName` |
| `interface.displayName` | Required, one line, at most 30 characters at final submission |
| `interface.shortDescription` | Required, one line, at most 30 characters at final submission |
| `interface.longDescription` | Required, at most 4,000 characters; line breaks allowed |
| `interface.category` | One of the supported categories; `Productivity` here |
| `interface.defaultPrompt` | At most 3 entries, each one line, at most 128 characters, unique, no `@mention` |
| `interface.logo`, `interface.composerIcon` | Required only when the package is uploaded as a ZIP; square image, at least 48x48, at most 4,096x4,096, under 5 MiB, path starting `./`. Not read by the portal form |
| `interface.brandColor` | Needs at least 2:1 contrast against white, so the navy `#13263A` is used, not the green |
| `interface.brandColorDark` | Needs at least 2:1 contrast against `#212121`, which the green `#00E795` meets |
| Listing URLs | `websiteURL`, `supportURL`, `privacyPolicyURL`, and `termsOfServiceURL` are all required for an MCP-backed submission and must be HTTPS |

`interface.screenshots` is rejected unless the MCP tool scan reports a UI output
template, so this package ships none. The package ships no skills either: the
MCP tool descriptions carry the workflow, and OpenAI's **With MCP** route treats
skills as optional. If one is added later, it must use provider-neutral language
rather than naming a specific assistant, and the manifest must declare
`"skills": "./skills/"`.

See the [submission error reference](https://developers.openai.com/plugins/deploy/submission-errors)
for the full list of validation codes.

## Directory submission prerequisites outside this repository

The **With MCP** submission is a portal form, not a package upload. Listing
details, the MCP server URL, starter prompts, and test cases are entered there,
and nothing in this repository is consumed by it. The following are properties of
the deployed server and the portal draft, not of these files:

- A domain-verification token served as plain text at
  `https://mcp.autosheet.com/.well-known/openai-apps-challenge`, matching the
  token the portal issues. The endpoint must return exactly that one token: no
  JSON, no list, no multiple tokens.
- A current, successful tool scan of the production endpoint, with explicit
  `readOnlyHint`, `openWorldHint`, and `destructiveHint` values plus a
  justification for each on every tool.
- Reviewer-ready demo credentials, because the server uses OAuth.
- A demo recording, exactly five positive and three negative test cases, and
  release notes.
- Apps Management write access and a verified individual or business identity in
  the owning OpenAI organization.

## ChatGPT desktop and Codex

Import the plugin archive through the supported plugin import flow for your
workspace. Complete OAuth and start a new conversation with Autosheet enabled.
Workspace policy may restrict imports.

For a direct Codex connection without installing the plugin:

```bash
codex mcp add autosheet --url https://mcp.autosheet.com/mcp
codex mcp login autosheet
```

## ChatGPT web

An imported plugin declaring MCP servers in `.mcp.json` or `mcp.json` is currently
desktop-only, including remote HTTPS servers. Publishing these files on GitHub
does not by itself enable the plugin on ChatGPT web or publish a directory listing.
See [OpenAI plugin management](https://learn.chatgpt.com/docs/enterprise/plugin-management).

To test the server on ChatGPT web, enable developer mode in Settings → Security
and login, open Plugins, select the plus button, and create a Server URL connection
to `https://mcp.autosheet.com/mcp`. Complete OAuth, review the discovered tools, and
test in a new chat. Availability depends on account and workspace policy.
See [Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt).

To bind a plugin to that registered connection, obtain its actual `asdk_app_…`
ID (remove the `plugin_` prefix from a `plugin_asdk_app_…` browser URL). Add an
`.app.json` file containing an `apps` object with an `autosheet` entry whose `id`
is that real ID and `required` is `true`. In the web package, replace the native
manifest's `mcpServers` field with `apps: "./.app.json"` and exclude both raw MCP
files and the alternative client manifests. Keep the native manifest.
No `.app.json` is shipped here because a registered connection ID has not been
provided. Do not invent an ID or commit a placeholder as a working connection.

For public directory distribution, use OpenAI's **With MCP** submission route
with the hosted endpoint. Complete the listing, authentication,
tool scan, and review in the portal; a Claude approval does not transfer.
See [Claude plugin migration](https://developers.openai.com/plugins/guides/submit-claude-plugin)
and [plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Acceptance checks

Package validation is separate from a successful authenticated ChatGPT session.
Run the following against the deployed connection before announcing compatibility:

1. Install or register the connection, finish OAuth, and verify tool discovery.
2. On a test spreadsheet, request a small explicit change and verify the actual cells.
3. Follow up with the same agent ID and verify that it stays on the original spreadsheet.
4. Exercise a longer job: `running` must lead to polling and a final outcome.
5. Stop a running job and verify cancellation is reported accurately.
6. Test an inaccessible spreadsheet and confirm a useful error instead of success.
7. If the deployed server exposes tab copying, copy a test tab once and inspect it.

Record the client, date, deployed tool list, and results. Refresh the ChatGPT
developer connection after metadata changes and rerun affected checks in a new chat.
Published plugins use reviewed metadata snapshots and require the publication
update flow; live metadata-sheet edits alone do not update those snapshots.
