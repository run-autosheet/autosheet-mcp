# Autosheet plugin package

The repository root is the plugin package `autosheet` for the hosted MCP endpoint
`https://mcp.autosheet.com/mcp`. The Claude Code and Codex marketplaces
(`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`) install it
from `./`. Archives for other clients are attached to each release on GitHub.

## Layout

```text
<repo root>/
├── plugin.json                  Agent Plugins 1.0 manifest; OpenAI listing under extensions.com.openai
├── mcp.json                     Agent Plugins 1.0 MCP config, streamable-http
├── .claude-plugin/
│   ├── plugin.json              Claude Code manifest, MCP server declared inline
│   └── marketplace.json         Claude Code marketplace, plugin source "./"
├── .agents/plugins/
│   └── marketplace.json         Codex marketplace, plugin source "./"
├── assets/                      listing icons
├── skills/                      shared by every client, when present
└── LICENSE
```

## Who reads what

| Client | Files read | How it gets the package |
| --- | --- | --- |
| Claude Code | `.claude-plugin/plugin.json`, `skills/` | The `autosheet` marketplace in this repository |
| Codex | `plugin.json`, `mcp.json`, `skills/` | The `autosheet` marketplace in this repository |
| Other Agent Plugins 1.0 clients (VS Code, Cursor, GitHub Copilot, Kiro, …) | `plugin.json`, `mcp.json`, `skills/` | `autosheet-agent-plugin-<version>.zip` from the release. Don't point the client at the repository root, which also holds the marketplace manifests |

For users who just want the server, the README covers
[ChatGPT](../README.md#chatgpt) and the [Codex CLI](../README.md#codex-cli) with a
direct connection and no package at all.
