# AGENTS.md

Guidance for coding agents working in this repository.

## What this repo is

Public distribution repo for the Autosheet plugin packages (Claude Code, Codex, ChatGPT, and Agent Plugins clients). It contains:

- `.claude-plugin/marketplace.json` — Claude Code marketplace (name: `autosheet`)
- `.agents/plugins/marketplace.json` — Codex marketplace (name: `autosheet`)
- `plugins/autosheet/` — the plugin: skills + MCP configuration for the hosted server at `https://mcp.autosheet.com/mcp`
- the repository root — a second, standalone package named `autosheet-mcp`: `plugin.json` + `mcp.json` (Agent Plugins 1.0, read by ChatGPT, Codex, VS Code, Cursor, GitHub Copilot, Kiro and other portable-plugin clients). OpenAI listing metadata lives in `plugin.json` under `extensions.com.openai.interface`; there is no native `.codex-plugin/plugin.json` at the root — Codex reads the listing from `plugin.json`. `scripts/build-plugin-archives.py` builds one ZIP per destination: Claude and ChatGPT/Codex from `plugins/autosheet/`, Agent Plugins from the root. The plugin portal's ZIP path is skills-only and rejects MCP packages; the public directory goes through the **With MCP** form. Documented in `docs/plugin.md`. It is not reachable through either marketplace above.

The MCP server source is **not** in this repo and is not open source.

## Rules

- **Never edit `plugins/` directly.** Its contents are synced from an internal upstream repo on each release and any direct edits will be overwritten by the next promotion. Changes to skills or plugin manifests must be made upstream and promoted via the publish script.
- **Versioning**: this repo only ever carries clean release versions (`X.Y.Z`). Pre-release/beta versions (`X.Y.Z-beta.N`) live in the internal upstream repo only.
- **Plugin renames/removals** must go through a top-level `renames` map in `.claude-plugin/marketplace.json` so existing installs migrate instead of erroring.
- **The root package and `plugins/autosheet/` are separate entry points, and that split is transitional.** Editing the root package does not update the release-managed one, and vice versa. `plugin.json` and `mcp.json` are the only sources of truth for the root package; edit them, never a generated file. The target is a single root package named `autosheet` serving every client, with `plugins/` removed; the layout and migration steps are in `docs/plugin.md` under "Target layout", and the consolidation has to be coordinated with the upstream publish script.
- **Don't add a `.codex-plugin/plugin.json` at the root.** Codex reads the listing from `plugin.json`'s `extensions.com.openai` block; a root native manifest would put a client-specific file outside the reverse-domain layout the Agent Plugins spec requires (§8) and create a second copy of the listing metadata to keep in sync. The ChatGPT/Codex ZIP is built from `plugins/autosheet/`, which has its own.
- **Don't add a root `.mcp.json`.** Claude Code loads a repository-root `.mcp.json` as a project-scoped MCP server for every contributor who opens this repo (without prompting in `claude -p`, SDK and cloud sessions), and it would duplicate the plugin-installed `autosheet` server. The root package declares its server in `mcp.json`; the ChatGPT/Codex ZIP comes from `plugins/autosheet/`, whose `.mcp.json` is inside the archive where OpenAI's validator expects it (`mcpServers` must be the string path `./.mcp.json`).
- **Don't add a root `.claude-plugin/plugin.json` before the consolidation.** While `plugins/autosheet/` exists it would give Claude Code a second, differently named copy of the same server. It becomes the Claude manifest of the single root package once `plugins/` is removed (see `docs/plugin.md`, "Target layout").
- **Root-package listing metadata is validated by OpenAI's package checks when the ZIP is imported through the ChatGPT workspace admin or a Codex marketplace** — `interface.displayName` and `interface.shortDescription` are capped at 30 characters, `brandColor` needs 2:1 contrast against white, and `logo`/`composerIcon` are required there. The build script enforces the text limits; the public directory listing (the **With MCP** submission) is a portal form that never reads the manifest. `docs/plugin.md` records the full set; check it before editing `extensions.com.openai.interface` in `plugin.json`.

## MCP configuration

Two files declare the same server, and both must point at `https://mcp.autosheet.com/mcp`:

- `plugins/autosheet/.mcp.json` (release-managed) — Claude auto-discovers it at the plugin root, and `plugins/autosheet/.codex-plugin/plugin.json` references it explicitly.
- `mcp.json` at the root — `type: "streamable-http"`, the Agent Plugins 1.0 format, used by Codex and every other Agent Plugins client for the root package.

**Never add `command`-based (stdio/npx) MCP servers**: ChatGPT rejects them at import, and security scans flag runtime package fetching as a supply-chain vector (OWASP MCP Top 10). The former `npx mcp-remote` bridge for Codex was removed once the server started serving the MCP handshake anonymously and stopped advertising RFC 9207 `iss` support (workaround for [openai/codex#31573](https://github.com/openai/codex/issues/31573)).

Transitional note: `plugins/autosheet/.claude-plugin/plugin.json` still carries a legacy inline `mcpServers` block with the same server name. Claude Code gives the inline definition precedence over `.mcp.json` (verified empirically 2026-07-21; undocumented) — both now point at the same server, and the inline block is removed upstream and will disappear with the next release promotion. Don't re-add it.
