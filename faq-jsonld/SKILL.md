# FAQ JSON-LD Metafield Skill

## Purpose

Populate the `jsonld.faq` Shopify metafield on blog articles so the theme can render FAQ structured data (JSON-LD) automatically. This keeps FAQ schema in sync with article content and managed through a single metafield rather than hardcoded in templates.

---

## Metafield Definition

| Field | Value |
|-------|-------|
| Namespace | `jsonld` |
| Key | `faq` |
| Type | `single_line_text_field` |
| Owner | Article |

The metafield definition is already created in Shopify admin. Every blog article can have one `jsonld.faq` metafield value.

---

## Format

Plain text. Pipe `|` separates question from answer. Double pipe `||` separates Q&A pairs.

### Single Q&A

```
What size [product] do I need?|Size depends on your [key spec] requirements. Calculate your maximum simultaneous demand and add a 30% safety margin.
```

### Multiple Q&A

```
What size [product] do I need?|Size depends on your [key spec] requirements. Calculate your maximum simultaneous demand and add a 30% safety margin.||How long does a [product] last?|[Type A] models last 80,000-100,000 hours with proper maintenance. [Type B] models last 15,000-30,000 hours before a major service.||Is [attribute A] better than [attribute B]?|Neither is universally better. [Attribute A] is required for certain specialized use cases. [Attribute B] lasts longer and costs less for general use.
```

### Rules

1. **Word-for-word match.** Question and answer text must match the article's FAQ section exactly. Do not paraphrase, summarize, or rewrite.
2. **Strip markdown links.** Convert `[anchor text](url)` to just `anchor text`. The metafield value is plain text — no HTML or markdown.
3. **Strip markdown formatting.** Remove `**bold**`, `*italic*`, and other markdown syntax. Keep the text content only.
4. **Multi-paragraph answers.** Join consecutive paragraphs within a single FAQ answer with a single space. Do not include blank lines.
5. **No trailing pipes.** The value must not start or end with `|` or `||`.
6. **No newlines.** The entire value is a single line of text.

---

## How to Generate the Value from an Article

1. Open the article's `.md` file in `your-project/Written Articles/`
2. Find the `## FAQ` or `## Frequently Asked Questions` section
3. Each `### ` heading is a question
4. The paragraph(s) between headings form the answer
5. Strip markdown links: `[text](url)` becomes `text`
6. Strip bold/italic markers: `**text**` becomes `text`, `*text*` becomes `text`
7. Join multi-paragraph answers with a single space
8. Concatenate: `Q1|A1||Q2|A2||Q3|A3`
9. Verify the result matches the article word-for-word (minus formatting)

---

## Upload Methods

### Batch upload script (preferred)

```bash
# Dry run — parse all articles, print values, no upload
python your_metafield_upload.py --dry-run   # your Shopify GraphQL metafield upload

# Upload all articles
python your_metafield_upload.py --upload   # your Shopify GraphQL metafield upload

# Single article — test one before batch
python your_metafield_upload.py --single [slug]   # your Shopify GraphQL metafield upload

# Update your keyword register with generated values
python your_metafield_upload.py --update-csv   # your Shopify GraphQL metafield upload
```

The step reads `.md` files, parses FAQ sections, maps filenames to Shopify article IDs via `shopify-article-ids.csv`, and uploads via the Shopify GraphQL API (metafieldsSet).

### Manual (Shopify admin)

1. Generate the pipe-separated value using the steps above
2. Go to Shopify admin > Blog posts > select article
3. Scroll to Metafields section
4. Find `jsonld.faq` field
5. Paste the value
6. Save

### Per-article (during content workflow)

When writing a new article, generate the FAQ metafield value as part of your publish workflow:
1. Write the article with FAQ section
2. Generate the pipe-separated value from the FAQ content
3. Record the value in your keyword register
4. Upload to Shopify using `--single` mode or paste manually

---

## Integration with SEO Content Workflow

The FAQ metafield value is included in the `<!-- ARTICLE-NOTES -->` block at the bottom of each `.md` file:

```
<!-- ARTICLE-NOTES
SEO Title: ...
Meta Description: ...
Internal links: ...
Schema: Article + FAQ
FAQ Metafield: Q1|A1||Q2|A2||Q3|A3
-->
```

After generating the article and running your publish step, the FAQ metafield value should be:
1. Appended to your keyword register
2. Uploaded to Shopify (single article mode or saved for batch)

---

## Troubleshooting

**Metafield not showing in theme:** Verify the metafield definition exists in Shopify admin (Settings > Custom data > Articles > jsonld.faq). The theme must read and render this metafield in a JSON-LD script block.

**Pipe characters in answer text:** Literal pipe characters `|` in article text will break the format. This hasn't occurred in existing articles (FAQ answers use dashes, not pipes, for lists). If it does, replace with a dash or rephrase.

**Value too long:** The `single_line_text_field` type supports up to 100,000 characters. No article FAQ section approaches this limit.
