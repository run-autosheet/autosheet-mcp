# AGENTS.md

Guidance for coding agents working in this repository.

## What this repo is

Public distribution repo for the Autosheet Claude Code / Codex plugin. It contains:

- `.claude-plugin/marketplace.json` — Claude Code marketplace (name: `autosheet`)
- `.agents/plugins/marketplace.json` — Codex marketplace (name: `autosheet`)
- `plugins/autosheet/` — the plugin: skills + MCP configuration for the hosted server at `https://mcp.autosheet.com/mcp`

The MCP server source is **not** in this repo and is not open source.

## Rules

- **Never edit `plugins/` directly.** Its contents are synced from an internal upstream repo on each release and any direct edits will be overwritten by the next promotion. Changes to skills or plugin manifests must be made upstream and promoted via the publish script.
- **Versioning**: this repo only ever carries clean release versions (`X.Y.Z`). Pre-release/beta versions (`X.Y.Z-beta.N`) live in the internal upstream repo only.
- **Plugin renames/removals** must go through a top-level `renames` map in `.claude-plugin/marketplace.json` so existing installs migrate instead of erroring.

## MCP configuration

All clients share the single direct-HTTPS config in `plugins/autosheet/.mcp.json` (`https://mcp.autosheet.com/mcp`) — Claude auto-discovers it at the plugin root, and the Codex manifest references it explicitly. **Never add `command`-based (stdio/npx) MCP servers**: ChatGPT rejects them at import, and security scans flag runtime package fetching as a supply-chain vector (OWASP MCP Top 10). The former `npx mcp-remote` bridge for Codex was removed once the server started serving the MCP handshake anonymously and stopped advertising RFC 9207 `iss` support (workaround for [openai/codex#31573](https://github.com/openai/codex/issues/31573)).

Transitional note: `.claude-plugin/plugin.json` still carries a legacy inline `mcpServers` block with the same server name. Claude Code gives the inline definition precedence over `.mcp.json` (verified empirically 2026-07-21; undocumented) — both now point at the same server, and the inline block is removed upstream and will disappear with the next release promotion. Don't re-add it.
