#!/usr/bin/env python3
"""Build one installable ZIP per destination for the Autosheet plugin.

Two packages live in this repository, and each client reads exactly one:

  plugins/autosheet/   release-managed (synced from the internal upstream): the
                       Claude and Codex manifests, the shared skill and .mcp.json
  <repo root>          the Agent Plugins 1.0 package (plugin.json + mcp.json) for
                       Cursor, VS Code, Copilot, Kiro and Codex installing by URL

Archives written to OUT_DIR (default dist/, git-ignored):

  autosheet-claude-plugin-<v>.zip  .claude-plugin/plugin.json, .mcp.json, skills/  Claude.ai / Claude Code upload
  autosheet-plugin-<v>.zip         .codex-plugin/plugin.json, .mcp.json, skills/   ChatGPT workspace-admin import, local Codex marketplaces
  autosheet-agent-plugin-<v>.zip   plugin.json, mcp.json, LICENSE                  Agent Plugins 1.0 clients

<v> is each package's own manifest version, so a filename never claims a version
its contents do not carry. The root listing block (extensions.com.openai.interface)
is validated against OpenAI's package limits before anything is written; Codex
reads it straight from plugin.json, so no native manifest is generated for the root.

None of these ZIPs is for the OpenAI plugin portal: its ZIP path is skills-only and
rejects packages with MCP servers. The public directory is the With MCP form.
ChatGPT marks workspace-imported plugins that carry .mcp.json as desktop-only.

Usage: scripts/build-plugin-archives.py [OUT_DIR]
"""
import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_PLUGIN = ROOT / "plugins" / "autosheet"
OPENAI_NAMESPACE = "com.openai"
AGENT_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENT_MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


def fail(message):
    sys.exit(f"error: {message}")


def check(condition, message):
    if not condition:
        fail(message)


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def validate_openai_listing(plugin):
    """Apply the limits OpenAI's package checks enforce on a native manifest to the
    root listing block, so a bad edit fails here instead of at import."""
    interface = plugin.get("extensions", {}).get(OPENAI_NAMESPACE, {}).get("interface")
    check(interface, f"plugin.json needs extensions.{OPENAI_NAMESPACE}.interface")
    check(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", plugin["name"]), "name: letters, digits, _ or -, at most 64 chars")
    check(len(plugin["description"]) <= 1024, "description over 1,024 characters")
    check(plugin["author"]["name"] == interface.get("developerName"), "author.name must equal interface.developerName")
    for field in ("displayName", "shortDescription"):
        value = interface.get(field, "")
        check(value and "\n" not in value and len(value) <= 30, f"interface.{field}: one line, 1-30 characters")
    check(len(interface.get("longDescription", "")) <= 4000, "interface.longDescription over 4,000 characters")
    prompts = interface.get("defaultPrompt", [])
    check(len(prompts) <= 3 and len(set(prompts)) == len(prompts), "interface.defaultPrompt: at most 3 unique entries")
    check(all("\n" not in p and len(p) <= 128 and "@" not in p for p in prompts), "interface.defaultPrompt: one line, <=128 chars, no @mention")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        check(interface.get(field, "").startswith("https://"), f"interface.{field} must be an HTTPS URL")


def marketplace_version():
    claude = load(MARKETPLACE_PLUGIN / ".claude-plugin" / "plugin.json")
    codex = load(MARKETPLACE_PLUGIN / ".codex-plugin" / "plugin.json")
    check(claude["version"] == codex["version"],
          f"plugins/autosheet manifests disagree on version: {claude['version']} vs {codex['version']}")
    return claude["version"]


def files_under(base, relative_dir):
    """(arcname, path) for every regular file under base/relative_dir, sorted."""
    directory = base / relative_dir
    check(directory.is_dir(), f"missing directory {directory.relative_to(ROOT)}")
    return sorted(
        (str(path.relative_to(base)), path)
        for path in directory.rglob("*")
        if path.is_file() and path.name != ".DS_Store"
    )


def write_zip(target, files):
    for _, source in files:
        check(source.is_file(), f"missing file {source.relative_to(ROOT)}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for arcname, source in files:
            archive.write(source, arcname)
    shown = target.relative_to(ROOT) if target.is_relative_to(ROOT) else target
    print(f"wrote {shown}: {', '.join(name for name, _ in files)}")


def main():
    out_dir = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "dist")

    plugin = load(ROOT / "plugin.json")
    mcp = load(ROOT / "mcp.json")
    check(plugin.get("$schema") == AGENT_PLUGIN_SCHEMA, "plugin.json $schema is not Agent Plugins 1.0.0")
    check(mcp.get("$schema") == AGENT_MCP_SCHEMA, "mcp.json $schema is not Agent Plugins 1.0.0")
    validate_openai_listing(plugin)
    root_version = plugin["version"]
    plugin_version = marketplace_version()  # every check runs before anything is written

    skills = files_under(MARKETPLACE_PLUGIN, "skills")
    mp = MARKETPLACE_PLUGIN
    write_zip(out_dir / f"autosheet-claude-plugin-{plugin_version}.zip", [
        (".claude-plugin/plugin.json", mp / ".claude-plugin" / "plugin.json"),
        (".mcp.json", mp / ".mcp.json"),
        *skills,
    ])
    write_zip(out_dir / f"autosheet-plugin-{plugin_version}.zip", [
        (".codex-plugin/plugin.json", mp / ".codex-plugin" / "plugin.json"),
        (".mcp.json", mp / ".mcp.json"),
        *skills,
    ])
    write_zip(out_dir / f"autosheet-agent-plugin-{root_version}.zip", [
        ("plugin.json", ROOT / "plugin.json"),
        ("mcp.json", ROOT / "mcp.json"),
        ("LICENSE", ROOT / "LICENSE"),
    ])


if __name__ == "__main__":
    main()
