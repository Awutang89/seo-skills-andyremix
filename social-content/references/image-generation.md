# Image generation

This skill never talks to an image API itself. It hands a validated prompt seed to an optional image engine, `<image-engine>`, which owns key loading, provider and model choice, cost reporting and file saving.

## The gate

Generate only when all four hold:

1. The person asked for an image in this request, or accepted the offer.
2. A generation path is visible: the engine script exists and its provider check reports at least one available provider.
3. The person has been told it may cost API credits or use an app's image quota.
4. The path saves a file (or returns one) whose location can be reported.

A direct request counts as approval. Give the cost note and go ahead; no second confirmation unless the request is ambiguous.

No request yet, a path is visible, and a visual would help: offer once through the question tool, in words like:

> I can generate this image now. It may use API credits or your image quota.

Say only that image generation is set up. Never say where a key lives or which file holds it.

## Is a path visible?

```text
python "<image-engine>/scripts/check_providers.py"
```

It prints JSON of available providers without touching the network or making test images. If the script does not exist, or no provider is available, treat it as no path.

## Calling the engine

1. Save the seed as `SOCIAL_WORKSPACE/social-visuals/<slug>/prompt-seed.json` (no workspace: ask for a folder in the same question as the offer; suggest `social-visuals/` in the current project). Never write inside a skill folder.
2. Validate it with `--final`, which fails on unfilled `{PLACEHOLDERS}` and on leftover `_use_when` note keys from the worked seeds: `python "<repo>/social-content/scripts/check_post.py" seed "<seed path>" --final`.
3. Optional dry run, which prints the final prompt, the route and the spend so far and calls nothing:

```text
python "<image-engine>/scripts/<generate script>" --provider auto --prompt-file "<seed path>" --aspect 4:5 --out-dir "<SOCIAL_WORKSPACE>/social-visuals/<slug>" --dry-run
```

4. Real run: the same command without `--dry-run`. Add `--image "<path>"` for every reference image in the seed (the real screenshot for `annotated-screenshot` and `teardown-crop`, a logo for a branded card). Pick `--aspect` from the seed's `output.aspect_ratio` (1:1 or 4:5 for feeds; 16:9 or 3:2 when the platform crop calls for it). Leave `--provider auto` unless the person names one.
5. Read the output. Each saved image prints one `SUCCESS: <absolute path>` line. Exit codes: 0 fine, 1 config or input problem, 2 provider API error, 3 missing dependency. Report failure plainly at a high level ("the provider returned an error", "a dependency is missing") and never pretend the image exists.
6. Confirm the file exists before saying it does. Report the path. Keep the post draft and the image prompt separate in the reply.
7. If a packet is saved, fill its Visual Brief: concept, seed path, generation status (not requested, offered, dry run, generated, failed), artifact path.

## No path

If the engine or a provider is not available:

- return the post, when proof allows
- return the JSON seed
- say generation needs an optional image engine (`<image-engine>`) with at least one provider key set in `.env` (its documentation lists the key names)
- call nothing and claim no image

File: social-content/references/image-generation.md · Version 1.0.0 · November 2026
