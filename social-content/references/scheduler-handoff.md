# Scheduler handoff

A platform-neutral contract for passing approved drafts to a social scheduler. The contract is fixed; each scheduler plugs in as an adapter under `adapters/` (see `adapters/README.md`). None is active today. Zernio is the planned first adapter.

## 1. Detect

Treat a scheduler as installed when any of these is true in the current session:

- a scheduler skill or slash command appears in the active skill or command list
- an MCP server exposing scheduling tools (create draft, schedule post, list queue) is connected
- an adapter folder under `adapters/<name>/` has status `active` in its README

Do not hard-code install paths or plugin cache folders; people install at user, project or marketplace scope and those layouts move. Do not look for API keys, open `.env` files or grep credential files to decide availability. Authentication is the scheduler's own business.

Nothing installed: say nothing about queueing unless the person raises it.

## 2. Offer once

During reusable setup, when a scheduler is installed, ask one compact question:

> I see <scheduler> is set up. Once you approve a post, should I offer to add it there as a draft? Drafts only; I will not schedule or publish unless you tell me to.

Save the answer in the workspace profile's Delivery section:

```markdown
## Delivery

- scheduler: <name> | none | unknown
- scheduler workflow: offer approved draft queueing | manual only | unknown
- default action: create drafts only
- schedule or publish: only on an explicit request
```

No answer and setup can continue: leave it `unknown`. Delivery never blocks drafting.

## 3. When queueing is allowed

At least one must hold:

- the person approved the drafts and asked to queue them
- the profile opts in, the skill offered after approval, and they accepted
- they asked to schedule, publish, or check the queue

Never queue a draft they have not seen and approved. Never schedule or publish when they approved drafts only.

## 4. Shape

- One post, one platform: one scheduler draft with the full text.
- Fan-out: one scheduler draft per post idea, not per platform, carrying every requested platform version.
- Threads (X or Meta) are split on lines containing only `---`.
- Never add a platform during delivery that was not requested.

Hand-off payload, regardless of scheduler:

```text
Draft 1: <short angle or source name>
  X: <full X text, --- between thread posts>
  LinkedIn: <full LinkedIn text>
  Threads: <full Threads text, --- between posts>
  Media: <artifact path, if an approved image exists>
```

## 5. Failures and results

- Scheduler reports missing setup or auth: pass on its setup instruction, stop delivery, and keep the drafts in the reply or packet so nothing is lost.
- Success: report the draft IDs or links only if the scheduler returned them. Never claim a draft exists that the scheduler did not confirm.
- Update the packet status (`queued`, `scheduled`, `published`) only on a confirmed result.

File: social-content/references/scheduler-handoff.md · Version 1.0.0 · November 2026
