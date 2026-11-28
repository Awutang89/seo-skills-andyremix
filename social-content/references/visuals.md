# Visuals

Read this when a visual might improve the post or an image is requested. Generation itself is in `image-generation.md`.

The visual is part of the packaging, decided before the final copy so text and image each get their own job. Text-only is the default. A plain post beats a post with an image that looks generated, overdesigned or pointless.

## When to recommend one

Recommend a visual when it makes the first stop in the feed, strengthens the proof, or makes the idea faster to grasp: a screenshot, chart, dashboard, before and after, workflow, checklist, annotated photo, or simple stat card; a concept that stops the scroll without faking evidence; or a request that mentions an image, graphic, screenshot or prompt.

Do not recommend one when the person asked for text only, the post is stronger as plain words, or the visual would need invented proof. If it creates no curiosity before the text is read, leave it out.

## The 12 roles

Pick exactly one before final drafting.

| Role | Use when | What the text does |
|---|---|---|
| `none` | The words carry it better. | Carries the whole post. |
| `raw-screenshot` | A real dashboard, terminal, doc, email, analytics view, product UI or messy field proof exists. | Says what the artifact means; never describes it. |
| `annotated-screenshot` | A real artifact needs a crop, blur, arrow, circle, highlight or short label. | Explains why the marked spot matters. |
| `receipt-strip` | The proof sits in an email, DM, review, changelog, calendar, invoice, ticket or before and after snippet. | Adds the context and the caveats. |
| `chart` | One metric moved over time, or one comparison matters. | States the consequence, not the number again. |
| `diagram` | The idea is a workflow, contrast, decision tree, system map or mental model. | Delivers the take; the diagram carries the structure. |
| `checklist` | The value is a process people can lift and use. | Says who it is for and why. |
| `teardown-crop` | One spot on a website, ad, email, search result, product screen or landing page teaches the lesson. | Names the lesson from the callout. |
| `stat-card` | One or two sourced numbers are the proof and no real artifact exists. | States the consequence, not the numbers again. |
| `meme` | The joke or contrast is the post. | Stays short; never explains the joke. |
| `lo-fi-photo` | A real desk, notebook, whiteboard, event, product or human moment exists. | Adds the lesson, casually. |
| `generated-scene` | No real artifact exists, but a metaphor or photo-style image adds personality or stopping power. | Makes the claim; the image sets mood and context only. |

Real artifacts beat generated ones. If the person has the screenshot, chart, dashboard or photo, use it or annotate it; never generate a replacement.

## Capture requests

When the best visual is a screenshot or receipt the person has not supplied, ask for it instead of generating it. A generated screenshot, dashboard, receipt, testimonial or product state is invented proof even when the story behind it is true. The capture brief names:

- the target screen or document
- the detail that must be visible
- the crop
- what to blur or redact (customer names, emails, order numbers, revenue the person does not want public, account IDs)
- an optional annotation

## Ranking

Prefer, in order:

1. The real artifact, lightly cleaned: screenshot, chart, terminal, dashboard, email, product UI, photo.
2. The real artifact annotated: crop, arrow, circle, blur, highlight, or one short label.
3. A practical diagram or checklist: workflow, decision tree, teardown, simple system map.
4. A branded stat card, only when the sourced number is strong enough to carry an image.
5. A lo-fi photo or whiteboard, only when it genuinely comes from the work.
6. A meme or generated scene, only when the joke or metaphor is sharper than the post alone.

Generated images should almost never pose as proof. They suit diagrams, stat cards and simple metaphors, not fake dashboards, screenshots, receipts or people.

## Platform defaults

- **X:** raw and unproduced wins. Messy screenshots, crops, chart snippets, terminal captures, quote-post embeds, phone photos, quick scribbled annotations. No polished brand templates unless the account already uses them. A proof image means even tighter copy.
- **Threads:** same rules as X, and the same image usually works. A little more finish is fine as long as it still feels like a native share, not an ad.
- **LinkedIn:** business relevance and phone readability. Stat cards, diagrams, annotated screenshots, before and after proof, teardown crops. A big red arrow or circle is fine when it makes the point obvious on a phone. Skip decorative AI art. A single image belongs here; when the idea really needs several slides, that is a carousel job, not a reason to cram a deck into one image.

## Visual concept

When a visual is worth proposing, give:

- `concept`: what the image shows
- `why`: the job it does for the post
- `role`: one of the 12
- `source constraints`: numbers, labels, screenshots or claims that must be kept exactly
- `brand constraints`: website, colors, logo, type or visual examples from the saved profile
- `avoid`: anything unsupported, tacky, misleading or off brand
- `prompt_seed`: valid JSON the person can reuse (below)

A good visual makes the proof clearer, the contrast quicker, or adds one specific personality cue. "Abstract gradient with icons" is nearly always the weak option.

## Prompt seed

The seed is a production brief for the image, not a strategy brief for the post. Leave out the post text, the persuasion goal and audience psychology unless they change something visible.

Field order, which is the order image models follow best: output and canvas, reference inputs, subject or artifact, composition, camera and light, style, on-image text, constraints.

Blank schema: `templates/prompt-seed.json`. Worked seeds to copy and adapt (one at a time; never merge them into one mega prompt):

- `templates/seeds/annotated-screenshot.json`
- `templates/seeds/stat-card.json`
- `templates/seeds/diagram.json`
- `templates/seeds/lo-fi-photo.json`
- `templates/seeds/teardown-crop.json`

Validate before handing it on:

```text
python "<repo>/social-content/scripts/check_post.py" seed path\to\seed.json
```

The optional image engine (`<image-engine>`) accepts this JSON directly as `--prompt-file` and adds its own provider wording.

## Prompt writing rules

- Describe only what should be visible.
- Tie every number, label, logo, quote or product state to a supplied fact or a reference image. Anything else goes in `do_not_invent`.
- One visual idea. No collage of every point in the post.
- On-image text only when it helps; most feed images want 0 to 8 words. Dense text belongs in the post.
- Mobile first: say where the focal point is, what the background is, the spacing, contrast, safe area, hierarchy, and what must be legible at feed size.
- Photos and scenes: state framing, camera angle, lens or view, light, depth of field and texture. "Phone photo under a cluttered desk lamp" beats "authentic".
- Diagrams: state viewpoint, shapes, arrows, step order, label positions, line weight, spacing and background.
- Screenshot edits: say what comes from each reference image, what stays untouched, and what may change.
- Missing screenshot: return a capture brief, never a seed that recreates the missing proof.
- Branded diagrams or stat cards: use the saved website, colors and logo. None saved: ask during reusable setup, or keep the design restrained and unbranded. `<image-engine>/scripts/extract_brand.py <url> --out-dir <dir>` can pull colors, fonts and logo from a website into `brand-identity.json`.
- Add negatives for common drift: no fake logos, extra metrics, gibberish UI, watermarks, extra captions, or stock people unless requested.

## Bad visual smells

Fix or drop the visual when:

- it restates the post on a generic card
- a fake generated dashboard stands in for a real screenshot
- it adds a metric, testimonial, logo, quote or customer the source never gave
- it needs more than one sentence to justify existing
- the post got longer because the text now explains the image
- it does not stop the scroll before the text is read
- it is "startup gradient plus floating icons" with no proof in it

## Quality checks

Before finalising a seed or an image:

- The role is explicit and useful for this platform.
- On-image text is only sourced numbers, the person's exact wording, or neutral labels.
- No fake quote, testimonial, result or logo.
- Real screenshots, charts, photos and dashboards are used as proof, not replaced.
- The image can stop the scroll before the text is read.
- It suits the platform and the reader.
- The seed names subject, style, mobile composition, text rules, brand constraints, negatives and aspect ratio.
- The post does not restate what the image shows; a proof image means a shorter post that interprets.
- Any artifact path exists before success is claimed.

File: social-content/references/visuals.md · Version 1.0.0 · November 2026
