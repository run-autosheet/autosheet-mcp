#!/usr/bin/env python3
"""Build the two distributable archives for the root `autosheet-mcp` package.

Source of truth is `plugin.json` (Agent Plugins 1.0) and `mcp.json`. The OpenAI
manifest `.codex-plugin/plugin.json` is generated here from those two files and
never committed, so the repository root stays a clean Agent Plugins package. The
OpenAI archive is for the ChatGPT workspace-admin import and local Codex
marketplaces; the plugin portal's ZIP path is skills-only and rejects it.

Usage: scripts/build-plugin-archives.py [OUT_DIR]   (default: dist/)
"""
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPENAI_NAMESPACE = "com.openai"
AGENT_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AGENT_MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


def fail(message):
    sys.exit(f"error: {message}")


def check(condition, message):
    if not condition:
        fail(message)


def load(path):
    with open(ROOT / path, encoding="utf-8") as handle:
        return json.load(handle)


def openai_manifest(plugin, mcp):
    """Derive the native OpenAI manifest from the portable files."""
    interface = plugin.get("extensions", {}).get(OPENAI_NAMESPACE, {}).get("interface")
    check(interface, f"plugin.json needs extensions.{OPENAI_NAMESPACE}.interface")

    servers = {}
    for name, server in mcp["mcpServers"].items():
        check(server["type"] == "streamable-http", f"mcp.json server {name}: only streamable-http is supported")
        entry = {"type": "http", "url": server["url"]}
        if "headers" in server:
            entry["headers"] = server["headers"]
        servers[name] = entry

    manifest = {
        "name": plugin["name"],
        "version": plugin["version"],
        "description": plugin["description"],
        "author": plugin["author"],
        "homepage": plugin["homepage"],
        "repository": plugin["repository"],
        "license": plugin["license"],
        "keywords": plugin["keywords"],
        "mcpServers": servers,
        "interface": interface,
    }

    # Limits from OpenAI's shared package checks (workspace-admin import, Codex marketplaces); see docs/plugin.md.
    check(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", manifest["name"]), "name: letters, digits, _ or -, at most 64 chars")
    check(len(manifest["description"]) <= 1024, "description over 1,024 characters")
    check(manifest["author"]["name"] == interface.get("developerName"), "author.name must equal interface.developerName")
    for field in ("displayName", "shortDescription"):
        value = interface.get(field, "")
        check(value and "\n" not in value and len(value) <= 30, f"interface.{field}: one line, 1-30 characters")
    check(len(interface.get("longDescription", "")) <= 4000, "interface.longDescription over 4,000 characters")
    prompts = interface.get("defaultPrompt", [])
    check(len(prompts) <= 3 and len(set(prompts)) == len(prompts), "interface.defaultPrompt: at most 3 unique entries")
    check(all("\n" not in p and len(p) <= 128 and "@" not in p for p in prompts), "interface.defaultPrompt: one line, <=128 chars, no @mention")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        check(interface.get(field, "").startswith("https://"), f"interface.{field} must be an HTTPS URL")
    return manifest


def write_zip(target, files):
    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for arcname, source in files:
            archive.write(source, arcname)
    shown = target.relative_to(ROOT) if target.is_relative_to(ROOT) else target
    print(f"wrote {shown}: {', '.join(name for name, _ in files)}")


def main():
    out_dir = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "dist")
    plugin = load("plugin.json")
    mcp = load("mcp.json")
    check(plugin.get("$schema") == AGENT_PLUGIN_SCHEMA, "plugin.json $schema is not Agent Plugins 1.0.0")
    check(mcp.get("$schema") == AGENT_MCP_SCHEMA, "mcp.json $schema is not Agent Plugins 1.0.0")
    version = plugin["version"]
    native_manifest = openai_manifest(plugin, mcp)  # validates before anything is written

    write_zip(out_dir / f"autosheet-agent-plugin-{version}.zip", [
        ("plugin.json", ROOT / "plugin.json"),
        ("mcp.json", ROOT / "mcp.json"),
        ("LICENSE", ROOT / "LICENSE"),
    ])

    with tempfile.TemporaryDirectory() as tmp:
        manifest_path = Path(tmp) / ".codex-plugin" / "plugin.json"
        manifest_path.parent.mkdir()
        manifest_path.write_text(json.dumps(native_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        write_zip(out_dir / f"autosheet-mcp-plugin-{version}.zip", [
            (".codex-plugin/plugin.json", manifest_path),
            ("LICENSE", ROOT / "LICENSE"),
        ])


if __name__ == "__main__":
    main()
