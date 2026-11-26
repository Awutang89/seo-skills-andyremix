#!/usr/bin/env python
"""Plan (dry-run by default) the Search Console MCP setup on Windows.

Nothing changes unless you pass --execute or --copy-credential-from.
It never prints the contents of an OAuth file.

  python setup_gsc.py --status
  python setup_gsc.py --project-id <existing-google-ads-project-id>          (dry-run plan)
  python setup_gsc.py --copy-credential-from "%USERPROFILE%\\Downloads\\client_secret_....json"
  python setup_gsc.py --project-id <id> --execute                            (enable APIs + register MCP)

See ../references/setup.md for the full procedure.
"""

from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # pragma: no cover
    pass

SERVER_NAME = "gsc"
PACKAGE = "mcp-search-console"
ENV_VAR = "GSC_OAUTH_CLIENT_SECRETS_FILE"
APIS = ["searchconsole.googleapis.com", "analyticsdata.googleapis.com"]
DEST = {
    "secrets": Path(".secrets/gsc/client_secrets.json"),
    "claude": Path.home() / ".claude" / "mcp-gsc" / "client_secrets.json",
}


def run(cmd):
    try:
        return subprocess.run(cmd, check=False, text=True, capture_output=True, shell=False)
    except FileNotFoundError:
        return None


def out(cmd):
    exe = shutil.which(cmd[0])
    if not exe:
        return ""
    r = run([exe] + cmd[1:])
    return r.stdout.strip() if r and r.returncode == 0 else ""


def in_git_worktree(path: Path):
    """Return the repo root if `path` sits inside a git work tree, else None."""
    for parent in [path] + list(path.parents):
        if (parent / ".git").exists():
            return parent
    return None


def git_ignored(path: Path, repo: Path) -> bool:
    git = shutil.which("git")
    if not git:
        return False
    r = run([git, "-C", str(repo), "check-ignore", "-q", str(path)])
    return bool(r and r.returncode == 0)


def check_destination(dest: Path):
    repo = in_git_worktree(dest.parent if not dest.exists() else dest)
    if repo and not git_ignored(dest, repo):
        raise SystemExit(f"Refusing: {dest} is inside the git repo {repo} and not ignored. "
                         "OAuth files must never be tracked.")


def validate_credential(src: Path):
    if src.suffix.lower() != ".json" or not src.exists():
        raise SystemExit(f"Not an existing .json file: {src}")
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise SystemExit("The file is not valid JSON.")
    if "installed" not in data:
        if "web" in data:
            raise SystemExit("This is a Web-application client. Create a 'Desktop app' OAuth client instead.")
        raise SystemExit("No 'installed' (Desktop app) client found in the JSON.")
    return True


def status():
    creds = {k: {"path": str(v), "exists": v.exists()} for k, v in DEST.items()}
    return {
        "os": platform.system(), "python": sys.version.split()[0],
        "uv": shutil.which("uv"), "uvx": shutil.which("uvx"),
        "gcloud": shutil.which("gcloud"), "claude": shutil.which("claude"), "winget": shutil.which("winget"),
        "credential_files": creds,
        "gcloud_account": out(["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"]),
        "gcloud_project": out(["gcloud", "config", "get-value", "project"]),
        "gsc_mcp_registered": SERVER_NAME in out(["claude", "mcp", "list"]),
    }


def mcp_json(cred_path: Path):
    return {"type": "stdio", "command": shutil.which("uvx") or "uvx", "args": [PACKAGE],
            "env": {ENV_VAR: str(cred_path)}}


def plan(project_id, cred_path: Path, scope):
    pid = project_id or "<EXISTING_GOOGLE_ADS_PROJECT_ID>"
    return [
        {"id": "install-uv", "run_by": "The user", "command": "winget install --id astral-sh.uv -e",
         "skip_if": "uvx already on PATH"},
        {"id": "install-gcloud", "run_by": "The user (optional)", "command": "winget install --id Google.CloudSDK -e",
         "skip_if": "you enable the APIs in the Cloud Console instead"},
        {"id": "gcloud-login", "run_by": "The user (browser)", "command": "gcloud auth login"},
        {"id": "find-project", "run_by": "The user", "command": "gcloud projects list",
         "note": "Pick the project that already holds the Google Ads OAuth client. Do not create a new one."},
        {"id": "enable-apis", "run_by": "script with --execute",
         "command": f"gcloud services enable {' '.join(APIS)} --project {pid}"},
        {"id": "consent-screen", "run_by": "The user (browser)",
         "url": f"https://console.cloud.google.com/apis/credentials/consent?project={pid}",
         "note": "Reuse the existing consent screen. Add the Search Console read-only scope if the screen lists scopes; make sure your Google account is a test user (or the app is In production)."},
        {"id": "desktop-client", "run_by": "The user (browser)",
         "url": f"https://console.cloud.google.com/apis/credentials?project={pid}",
         "note": "Create credentials > OAuth client ID > Desktop app, name it 'gsc-mcp', download the JSON."},
        {"id": "store-credential", "run_by": "script",
         "command": f"python setup_gsc.py --copy-credential-from <downloaded.json> --dest {'secrets' if cred_path == DEST['secrets'] else 'claude'}"},
        {"id": "register-mcp", "run_by": "script with --execute",
         "command": f"claude mcp add-json {SERVER_NAME} --scope {scope} '{json.dumps(mcp_json(cred_path))}'",
         "manual_equivalent": f"claude mcp add {SERVER_NAME} --scope {scope} -e {ENV_VAR}=\"{cred_path}\" -- uvx {PACKAGE}"},
        {"id": "verify", "run_by": "The user", "command": "Restart Claude Code, run /mcp, then ask: List my GSC properties"},
    ]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Dry-run-first setup planner for the gsc MCP server.")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--project-id")
    ap.add_argument("--dest", choices=list(DEST), default="secrets", help="where the OAuth JSON lives")
    ap.add_argument("--scope", choices=["user", "local"], default="user")
    ap.add_argument("--copy-credential-from")
    ap.add_argument("--execute", action="store_true", help="enable the APIs and register the MCP server")
    a = ap.parse_args(argv)
    cred = DEST[a.dest]

    if a.status:
        print(json.dumps(status(), indent=2))
        return 0
    if a.copy_credential_from:
        src = Path(a.copy_credential_from).expanduser()
        validate_credential(src)
        check_destination(cred)
        cred.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, cred)
        print(f"Stored the Desktop OAuth client at {cred} (contents not shown). Delete the copy in Downloads.")
        return 0
    steps = plan(a.project_id, cred, a.scope)
    if not a.execute:
        print(json.dumps({"mode": "dry_run", "changes_made": False, "credential_path": str(cred), "steps": steps}, indent=2))
        return 0
    if not a.project_id:
        raise SystemExit("--execute needs --project-id (the existing Google Ads project).")
    if not cred.exists():
        raise SystemExit(f"Store the OAuth JSON first (--copy-credential-from). Missing: {cred}")
    gcloud, claude = shutil.which("gcloud"), shutil.which("claude")
    results = []
    if gcloud:
        r = run([gcloud, "services", "enable", *APIS, "--project", a.project_id])
        results.append({"step": "enable-apis", "returncode": r.returncode if r else None, "stderr": (r.stderr.strip() if r else "gcloud missing")[-400:]})
    else:
        results.append({"step": "enable-apis", "skipped": "gcloud not installed; enable both APIs in the Cloud Console"})
    if claude:
        r = run([claude, "mcp", "add-json", SERVER_NAME, "--scope", a.scope, json.dumps(mcp_json(cred))])
        results.append({"step": "register-mcp", "returncode": r.returncode if r else None, "stderr": (r.stderr.strip() if r else "")[-400:]})
    else:
        results.append({"step": "register-mcp", "skipped": "claude CLI not on PATH"})
    print(json.dumps({"mode": "execute", "results": results, "next": "Restart Claude Code, then: List my GSC properties"}, indent=2))
    return 0 if all(r.get("returncode", 0) in (0, None) for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
