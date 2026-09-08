# Autosheet plugin packaging

The repository root is a standalone plugin package named `autosheet-mcp` for the
hosted MCP endpoint `https://mcp.autosheet.com/mcp`. It is separate from the
release-managed package under `plugins/autosheet/`, which the Claude and Codex
marketplaces (`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`)
install under the name `autosheet`. Root-package changes do not update that
package; its manifests are edited in the internal upstream and promoted through
that project's release process. Never edit `plugins/` here.

**This two-package layout is transitional.** The target is one package at the
repository root serving every client; see [Target layout](#target-layout) below.

## Target layout

Two packages for one server is the source of most confusion in this repo: two
names, two manifests, two copies of the listing text, and rules asking maintainers
to keep them aligned. The intended end state is a single root package, the layout
Exa uses in `exa-labs/exa-mcp-server`:

```text
<repo root>/
├── plugin.json                  Agent Plugins 1.0 manifest (Codex, ChatGPT, VS Code, Cursor, ...)
├── mcp.json                     Agent Plugins 1.0 MCP config, streamable-http
├── .claude-plugin/
│   ├── plugin.json              Claude Code manifest, MCP server declared inline
│   └── marketplace.json         Claude marketplace, plugin source "./"
├── .agents/plugins/
│   └── marketplace.json         Codex marketplace, plugin source "./"
├── skills/                      shared by every format
├── scripts/build-plugin-archives.py
├── LICENSE
└── docs/plugin.md
```

`plugins/` disappears. There is one plugin name, `autosheet`, so existing
marketplace installs keep working and no `renames` entry is needed. The Claude
manifest keeps its MCP server inline, so no root `.mcp.json` is ever added (Claude
Code would load one as a project server for every contributor). `plugin.json`
stays the single source of the OpenAI listing block under
`extensions.com.openai`, and the build script keeps generating the OpenAI ZIP.

Why it is not done in this PR: `plugins/autosheet/` is not authored here. The
internal upstream repository publishes it into this one on every release, so
consolidating means changing that publish step to write the root files instead,
and moving the improved `interface` block into the upstream source.

### Migration steps

1. **Verify the OpenAI import path.** OpenAI's GitHub importer documents only
   `.codex-plugin/plugin.json` for marketplace entries; Codex's loader accepts a
   root Agent Plugins manifest, but the importer is unverified. Push a scratch
   repo with the target layout and import it into ChatGPT and Codex. If the
   importer rejects it, keep the build script's generated `.codex-plugin/plugin.json`
   out of git and add a marketplace entry with `"source": "url"` instead, or
   accept committing the native manifest and drop the §8 strictness.
2. **Upstream:** change the publish script to emit `.claude-plugin/plugin.json`,
   `skills/`, and the Agent Plugins `plugin.json` + `mcp.json` at the root of this
   repo, under the name `autosheet`; carry the `interface` block from the current
   root `plugin.json` into the upstream source; drop the upstream `.codex-plugin/`
   and `.mcp.json` outputs.
3. **Here, in the same release:** point both marketplace entries at `"./"`, delete
   `plugins/`, remove the transitional notes from this file and `AGENTS.md`, and
   rename the root package from `autosheet-mcp` to `autosheet` in `plugin.json`.
4. **Verify:** `scripts/build-plugin-archives.py` still builds both archives; the
   Claude marketplace installs from `./` in a fresh Claude Code session; Codex
   installs from the marketplace and connects through `mcp.json`; run the
   [acceptance checks](#acceptance-checks) once per client.

## Who reads the root package

| Client | Files read | How it gets the package |
| --- | --- | --- |
| Agent Plugins 1.0 clients: ChatGPT, Codex, VS Code, Cursor, GitHub Copilot, Kiro, Hermes, OpenClaw, Grok Bot, NanoClaw | `plugin.json`, `mcp.json` | Point the client at the repository root (or a clone of it) as a plugin, or install the portable ZIP built below |
| ChatGPT workspace-admin import (`chatgpt.com/admin/plugins`) and local Codex marketplaces | generated `.codex-plugin/plugin.json` | Import the OpenAI ZIP built below through **Admin > Plugins** in ChatGPT, or add it to a local Codex marketplace. Imported plugins that declare MCP servers are **desktop-only**, including remote HTTPS servers, and workspace policy may restrict imports. This ZIP cannot go to the plugin portal: its only ZIP path is skills-only and rejects a package with `mcpServers`; the public directory goes through the **With MCP** form |

Adding this repository as a marketplace, or importing it from GitHub, does **not**
surface `autosheet-mcp`: both importers read the marketplace manifests, which list
only `autosheet` from `plugins/autosheet/`. The root package is reached by a
marketplace entry that points at the repository root, or by the ZIPs built below.
OpenAI's GitHub importer documents only `.codex-plugin/plugin.json` for marketplace
entries; whether it accepts a root Agent Plugins manifest is unverified, so if a
marketplace entry for the root package is ever added, test that path first.

How Codex loads this layout (from `codex-rs/core-plugins` in the Codex source):
because the root `plugin.json` declares the agent-plugins.org `$schema`, Codex
treats it as the primary manifest. Identity, `version` and `description` come from
it, MCP servers come from `mcp.json` (`streamable-http`; legacy `sse` is
rejected), skills would come from `skills/`, and the listing block comes from
`extensions.com.openai.interface`. Codex prefers that block over a
`.codex-plugin/plugin.json` overlay when both exist, so the generated file is
never needed at runtime.

For users who just want the server, the README already covers
[ChatGPT](../README.md#chatgpt) and the [Codex CLI](../README.md#codex-cli) with a
direct connection and no package at all.

## Package layout

| Path | Purpose |
| --- | --- |
| `plugin.json` | Agent Plugins 1.0 manifest. Carries the OpenAI listing block under `extensions.com.openai.interface` |
| `mcp.json` | Agent Plugins 1.0 MCP configuration, `type: "streamable-http"` |
| `LICENSE` | MIT, matching the `license` field |
| `scripts/build-plugin-archives.py` | Builds both ZIPs and generates the OpenAI manifest; not part of either package |

The Agent Plugins spec (§8) requires client-specific data to live under a
reverse-domain namespace, either in `extensions` or in a top-level directory of
that name. `com.openai` is Codex's namespace, so the listing block in
`extensions` is the spec-conformant form and nothing client-specific sits loose at
the root.

Deliberately absent:

- **No committed `.codex-plugin/plugin.json`.** The ChatGPT workspace-admin import
  and Codex marketplaces need that file, so the build script generates it from
  `plugin.json` and `mcp.json` into the archive. Committing it would break the §8 layout and duplicate the
  listing block.
- **No root `.mcp.json`.** Claude Code loads a repository-root `.mcp.json` as a
  project-scoped MCP server for everyone who opens the repo.
- **No root `.claude-plugin/plugin.json` yet.** While `plugins/autosheet/` exists,
  a root Claude manifest would give Claude Code a second, differently named copy of
  the same server. It arrives with the consolidation in [Target layout](#target-layout),
  when `plugins/` goes away.
- **No skills, screenshots, or logo images.** The MCP tool descriptions carry the
  workflow. `interface.logo` and `interface.composerIcon` are required by the
  package checks; add square images under `./assets/`, declare both fields in the
  `interface` block, and teach the build script to copy them before relying on
  that path. Render them from `https://autosheet.com/icon.svg`.

## Building the archives

```bash
scripts/build-plugin-archives.py
```

This writes two files to `dist/` (git-ignored), named with the version from
`plugin.json`:

| Archive | Contents | For |
| --- | --- | --- |
| `autosheet-agent-plugin-<version>.zip` | `plugin.json`, `mcp.json`, `LICENSE` | Agent Plugins 1.0 clients |
| `autosheet-mcp-plugin-<version>.zip` | generated `.codex-plugin/plugin.json` + `.mcp.json`, `LICENSE` | ChatGPT workspace-admin import (`chatgpt.com/admin/plugins`) and local Codex marketplaces. Not the plugin portal: its ZIP path is skills-only and rejects a package with `mcpServers`; the public directory goes through the **With MCP** form |

The generated OpenAI manifest copies identity, author, license and keywords from
`plugin.json`, converts the `mcp.json` server to `type: "http"` in a generated `.mcp.json`,
points the manifest at it with `"mcpServers": "./.mcp.json"` (OpenAI's upload
validator rejects an inline `mcpServers` object with *"mcpServers must be a string
path for the root .mcp.json"*), and takes `interface` from `extensions.com.openai`. The script
refuses to build if the listing text breaks the OpenAI limits below, so a bad edit
fails locally instead of at import. Bump `version` in `plugin.json` for every
release; Agent Plugins clients use it for update checks.

Never archive the whole repository: `zip -r .` would bundle `plugins/autosheet/`
and both marketplace manifests, producing two plugin roots under different names.

## Listing metadata constraints (package checks)

OpenAI runs its shared package checks on the generated `.codex-plugin/plugin.json`
when the package is imported through the ChatGPT workspace admin or a Codex
marketplace. Limits that bind the current manifest (the build script checks the
ones marked ✓):

| Field | Rule |
| --- | --- |
| `name` | ASCII letters, digits, `_`, `-`; starts alphanumeric; at most 64 characters ✓ |
| `version` | Semantic version; a new release must change it |
| `description` | Required, at most 1,024 characters ✓ |
| `author.name` | Required, and must match `interface.developerName` ✓ |
| `interface.displayName`, `interface.shortDescription` | Required, one line, at most 30 characters ✓ |
| `interface.longDescription` | Required, at most 4,000 characters; line breaks allowed ✓ |
| `interface.category` | One of the supported categories; `Productivity` here |
| `interface.defaultPrompt` | At most 3 entries, each one line, at most 128 characters, unique, no `@mention` ✓ |
| `interface.logo`, `interface.composerIcon` | Required; square image, 48x48 to 4,096x4,096, under 5 MiB, path starting `./` |
| `interface.brandColor` | At least 2:1 contrast against white; the navy `#13263A` passes, the brand green does not |
| `interface.brandColorDark` | At least 2:1 contrast against `#212121`; the green `#00E795` passes |
| Listing URLs | `websiteURL`, `supportURL`, `privacyPolicyURL`, `termsOfServiceURL` all present and HTTPS ✓ |
| `interface.screenshots` | Rejected unless the tool scan reports a UI output template; ship none |

Full list of validation codes: [submission error reference](https://developers.openai.com/plugins/deploy/submission-errors).

## Public directory listing (With MCP)

The **With MCP** submission is a portal form, not a package upload. Listing text,
logo, server URL, starter prompts and test cases are entered in the portal and
nothing in this repository is consumed by it. Prerequisites live on the server
and in the portal draft:

- A domain-verification token served as plain text at
  `https://mcp.autosheet.com/.well-known/openai-apps-challenge` (currently 404),
  returning exactly the one token the portal issues.
- A successful tool scan of the production endpoint, with explicit `readOnlyHint`,
  `openWorldHint` and `destructiveHint` values and a justification for each tool.
- Reviewer demo credentials, since the server uses OAuth.
- A demo recording, test cases (five positive and three negative), and release notes.
- Apps Management write access and a verified identity in the owning OpenAI organization.

Binding an imported plugin to a ChatGPT-web connection requires a registered
connection ID (`asdk_app_…`) in an `.app.json` file; none is shipped because no
ID exists yet. See [Connect and test](https://developers.openai.com/plugins/deploy/connect-chatgpt),
[Claude plugin migration](https://developers.openai.com/plugins/guides/submit-claude-plugin)
and [plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Acceptance checks

Package validation is separate from a working authenticated session. Run these
against the deployed connection before announcing compatibility for a client:

1. Install or register the connection, finish OAuth, and verify tool discovery.
2. On a test spreadsheet, request a small explicit change and verify the actual cells.
3. Follow up with the same agent ID and verify that it stays on the original spreadsheet.
4. Exercise a longer job: `running` must lead to polling and a final outcome.
5. Stop a running job and verify cancellation is reported accurately.
6. Test an inaccessible spreadsheet and confirm a useful error instead of success.
7. Copy a test tab once and inspect it.

Record the client, date, deployed tool list, and results. After metadata changes,
refresh the connection in the client and rerun the affected checks in a new chat.
