# Memory: the social workspace

Read this only when the run needs durable memory or earlier context.

## Where it lives

`SOCIAL_WORKSPACE` is whatever folder the person picked, relative or absolute. There is no silent default. Before the first write, ask once:

> Where should I keep reusable social work for this project? For example `example-outdoor/social/`, `content/social/`, or a hidden `.social-content/`.

Create the folder only after the answer. Use it for the index, profile, examples, packets, visuals and the delivery preference from then on.

Suggested convention: `<brand>/social/` beside the brand's `brand/` folder. Generated images go to `SOCIAL_WORKSPACE/social-visuals/<slug>/` (gitignored), never inside a skill folder.

## Layout

```text
SOCIAL_WORKSPACE/
  index.md
  voice-profile.md      social profile: goals, pillars, platforms, X status, visual taste, delivery
  voice-examples.md     real voice evidence (template and copyright rule: brand-voice/)
  posts/
    YYYY-MM-DD-slug.md  one packet per idea
  social-visuals/
    <slug>/             generated or annotated images
```

The profile holds durable rules. The examples file holds the evidence. Each packet holds one idea.

When the brand already has `<brand>/brand/voice-profile.md` from brand-voice, do not duplicate its voice rules here. The workspace profile then carries only the social sections (content goal, pillars, platforms, X status, visual preference, delivery) and points at the brand profile for voice.

## Voice examples

The examples file format, its "examples are voice, not proof" header, and the copyright boundary (full text only for the person's own or directly supplied writing; short excerpt plus link plus notes for anyone else's post; emulate the move, never the wording) belong to brand-voice. Use its template from `brand-voice/` when creating or updating the file. This file is not included in this repository. This skill only reads it and appends evidence when asked. Add new evidence to the examples file; touch the profile only when a durable pattern changes, so later runs can go straight to the evidence.

## When to write

- The person asks to save, remember, continue, reuse, or build a profile.
- The task refers to an earlier draft or saved packet.
- Durable voice rules, examples or brand preferences arrive.
- The proof in hand will probably be reused.

A draft being written is not by itself a reason to save a packet.

## Loading

1. Resolve the workspace: a path the person gave, one already set in this conversation, or an existing workspace they named before. Unknown and needed: ask.
2. When the person refers to earlier work, read `index.md` first.
3. Open only the profile, examples or packet the task needs.
4. An index row pointing at a missing file: mark it missing in the reply or the index. Never rebuild a packet's contents from recollection.
5. Several packets match: one short disambiguating question, or pick the obvious one and say which.

## Index

Keep it to one table (template: `templates/index.md`). Paths are relative to the workspace unless the person wants absolute paths. After any index edit, confirm each new `file` path exists:

```text
python "<repo>/social-content/scripts/check_post.py" index "<SOCIAL_WORKSPACE>/index.md"
```

## Packets

Template: `templates/post-packet.md`. Front matter holds date, slug, topic, platforms, status. Sections: Brief, Source Nuggets, Proof Ledger, Drafts (one H3 per platform), Visual Brief, Editing Pass, Revision Notes. Leave a heading empty only when it will likely be filled later; otherwise drop it and keep the packet short.

File: social-content/references/memory.md · Version 1.0.0 · November 2026
