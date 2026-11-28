# Setup: connect Search Console (Windows)

**The user runs this once.** Nothing
here is run automatically during an audit.

The end result: a Claude Code MCP server named **`gsc`** (the `gsc-audit` skill looks for
`mcp__gsc__...` tools), running the `mcp-search-console` package through `uvx`, signed in with a
**Desktop app** OAuth client that belongs to the **existing Google Cloud project the user created for
Google Ads**. No new Cloud project.

---

## 0. Dry run first
```powershell
cd "gsc-audit\scripts"
python setup_gsc.py --status                    # what is installed, which credential paths exist
python setup_gsc.py --project-id <PROJECT_ID>   # prints every step; changes nothing
```
The helper only changes something with `--copy-credential-from` (stores the OAuth file) or
`--execute` (enables the two APIs and registers the MCP server). It never prints credential
contents, and it refuses to store the OAuth file inside a git repo unless the path is gitignored.

## 1. Tools (skip what is already installed)
```powershell
winget install --id astral-sh.uv -e          # gives uv and uvx
winget install --id Google.CloudSDK -e       # optional: only for enabling APIs from the command line
```
Open a new terminal afterwards so PATH updates. Check: `uvx --version`, `gcloud --version`.

## 2. Pick the existing Google Ads project
```powershell
gcloud auth login                 # browser: sign in with the Google account that owns Search Console for your sites
gcloud projects list              # find the project that holds the Google Ads OAuth client
gcloud config set project <PROJECT_ID>
```
Without gcloud: open https://console.cloud.google.com/ and use the project picker. It is the
project whose **APIs & Services > Credentials** page lists the Google Ads OAuth client.

## 3. Enable the APIs in that project
```powershell
gcloud services enable searchconsole.googleapis.com analyticsdata.googleapis.com --project <PROJECT_ID>
```
or in the console: **APIs & Services > Library**, then enable **Google Search Console API** and
**Google Analytics Data API** (GA4). The GA4 API is not used by `gsc-audit` yet.

## 4. OAuth consent screen (reuse it)
**APIs & Services > OAuth consent screen** (Google Auth Platform > Branding/Audience/Data access in
the newer console):
- Keep the existing app from the Google Ads setup.
- Under data access or scopes, add `https://www.googleapis.com/auth/webmasters.readonly`
  (Search Console, read-only) and, for later, `https://www.googleapis.com/auth/analytics.readonly`.
- If the app is **External + Testing**, make sure the user's Google account is on the test-user list.
  In Testing mode, Google expires refresh tokens after about 7 days, so the server will ask the user to
  sign in again weekly. Moving the app to **In production** (unverified is fine for personal use:
  the user will click through an "unverified app" warning) avoids that.

## 5. Create a Desktop OAuth client
**APIs & Services > Credentials > Create credentials > OAuth client ID > Application type: Desktop
app**, name it `gsc-mcp`, then **Download JSON**. It must be a Desktop client (the JSON has an
`installed` key). A Web client will not work, and the helper rejects it.

## 6. Store the JSON outside every repo
```powershell
python setup_gsc.py --copy-credential-from "$env:USERPROFILE\Downloads\client_secret_XXXX.json"             # -> .secrets/gsc/client_secrets.json (default)
python setup_gsc.py --copy-credential-from "...json" --dest claude                                          # -> %USERPROFILE%\.claude\mcp-gsc\client_secrets.json
```
Then delete the copy in Downloads. Record only the **key name/location** in `.env` (see `.env.example`)
(for example `GSC_OAUTH_CLIENT_SECRETS_FILE=<path to the JSON>`), never the values.
Never put the file in the skills folder or any other project folder.

## 7. Register the MCP server
```powershell
claude mcp add gsc --scope user -e GSC_OAUTH_CLIENT_SECRETS_FILE=".secrets/gsc/client_secrets.json" -- uvx mcp-search-console
```
or let the helper do it with the exact JSON (`claude mcp add-json`):
```powershell
python setup_gsc.py --project-id <PROJECT_ID> --execute
```
Why user scope: audits run from several folders (the skills folder, `<workspace>`), and user
scope keeps the entry in `~\.claude.json`, outside any repo. Use `--scope local` to limit it to
one folder. Never use project scope (`.mcp.json` would be committed). Keep the name exactly `gsc`.

## 8. Verify
1. Restart Claude Code (or `/mcp`, then reconnect `gsc`).
2. `/mcp` shows `gsc` as connected.
3. Ask: **"List my GSC properties"**. The first call opens a browser for Google consent. Each
   property you own (for example `example.com`) should appear (Domain properties show as
   `sc-domain:...`).
4. If it fails, ask Claude to call the `gsc` server's capabilities tool and read the auth status.
5. Smoke test: a 7-day `page` pull for one store, saved into a test run folder, then
   `python gsc_analyzer.py analyze --run-dir <folder>`.

Do not claim the server works until step 3 has returned the properties.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `uvx` not found in Claude Code | Open a new terminal, or register with the full path from `(Get-Command uvx).Source` |
| Tools not visible | `/mcp`, reconnect `gsc`, or restart Claude Code |
| "Access blocked" / not a test user | Add the account under Audience > Test users, or publish the app |
| No properties listed | The signed-in Google account lacks Search Console access. Sign in with the owner account, or add the account as a user in Search Console settings |
| Asked to re-auth weekly | The app is in Testing mode (step 4) |
| Stale or bad token | Ask the server to re-authenticate, or delete its cached token file and sign in again |
| `uvx mcp-search-console` fails | Fallback: `git clone https://github.com/AminForou/mcp-gsc` into `%USERPROFILE%\.claude\mcp-gsc\source`, `uv venv`, `uv pip install -r requirements.txt`, then register the venv's `python.exe` with `gsc_server.py` as the command, same env var, same name `gsc` |

Client or prospect sites: do not connect their property with our OAuth app unless the owner has
added the user's account in Search Console. Until then the lane reports `not_run`, and the
recommendation asks the owner for access.

File: gsc-audit/references/setup.md · Version 1.0 · November 2026
