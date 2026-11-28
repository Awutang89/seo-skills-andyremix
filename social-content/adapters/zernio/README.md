# Zernio adapter (stub)

Status: planned. Not built, not active. The skill treats Zernio as not installed until this README says `active`.

When it is built, it must:

- read `ZERNIO_API_KEY` from the environment or `.env` by name, never printing it
- map the handoff payload in `../../references/scheduler-handoff.md` to Zernio's draft creation, one draft per post idea with every requested platform version
- create drafts only by default; schedule or publish only when the skill passes an explicit request
- return the draft IDs or links Zernio gives back, and nothing it did not confirm
- relay Zernio's own setup or auth error and stop

Check Zernio's current API or MCP documentation at build time; nothing here has been verified against it.

File: social-content/adapters/zernio/README.md · Version 1.0.0 · November 2026
