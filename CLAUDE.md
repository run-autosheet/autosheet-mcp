# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

Public distribution repo for the Autosheet Claude Code / Codex plugin. It contains:

- `.claude-plugin/marketplace.json` — Claude Code marketplace (name: `autosheet`)
- `.agents/plugins/marketplace.json` — Codex marketplace (name: `autosheet`)
- `plugins/autosheet/` — the plugin: skills + MCP configuration for the hosted server at `https://mcp.autosheet.com/mcp/`

The MCP server source is **not** in this repo and is not open source.

## Rules

- **Never edit `plugins/` directly.** Its contents are synced from an internal upstream repo on each release and any direct edits will be overwritten by the next promotion. Changes to skills or plugin manifests must be made upstream and promoted via the publish script.
- **Versioning**: this repo only ever carries clean release versions (`X.Y.Z`). Pre-release/beta versions (`X.Y.Z-beta.N`) live in the internal upstream repo only.
- **Plugin renames/removals** must go through a top-level `renames` map in `.claude-plugin/marketplace.json` so existing installs migrate instead of erroring.

## MCP configuration — do not "clean up"

The plugin intentionally carries **two** MCP configs for the same server name (`autosheet`):

- `plugins/autosheet/.claude-plugin/plugin.json` → inline `mcpServers`: direct HTTP connection, used by **Claude Code**
- `plugins/autosheet/.mcp.json` → `npx mcp-remote` stdio bridge, used by **Codex** (workaround for an upstream Codex OAuth issuer bug, [openai/codex#31573](https://github.com/openai/codex/issues/31573))

Claude Code auto-discovers `.mcp.json` in plugin roots too, but when the same server name is defined both inline and in `.mcp.json`, the inline definition takes precedence (verified empirically 2026-07-21; this precedence is undocumented). This collision is deliberate — it keeps Claude Code on the direct HTTP connection while Codex uses the bridge. Do not merge or deduplicate these files.
