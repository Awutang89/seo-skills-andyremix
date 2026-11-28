# Scheduler adapters

The general skill never names a scheduler. It follows the contract in `../references/scheduler-handoff.md`. Each scheduler that can receive drafts gets its own folder here:

```text
adapters/
  <scheduler>/
    README.md    status (active | dormant | planned), key names, how the contract maps to the vendor's API or MCP
scripts/adapters/
  <scheduler>.py optional script, only once the adapter is built
```

Rules for every adapter:

- Dormant until its key exists in `.env`, as in `.env.example` (scripts read the process environment first, then that file, by key name only; never print or copy the value).
- Drafts are the default action. Scheduling and publishing happen only on an explicit request passed through by the skill.
- One scheduler draft per post idea, all requested platform versions attached, threads split on `---`.
- Report IDs or links only when the vendor returned them.

| Adapter | Status | Key |
|---|---|---|
| `zernio/` | planned (stub only) | `ZERNIO_API_KEY` (not yet in `.env`) |

File: social-content/adapters/README.md · Version 1.0.0 · November 2026
