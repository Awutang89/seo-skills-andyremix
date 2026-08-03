# Marketing & SEO Skills

A library of **25 modular skills** for Claude Code and Claude Desktop that cover the
full SEO + content-marketing lifecycle: from keyword research → content →
on-page/technical SEO → internal linking → schema → distribution → conversion.

Each skill is a self-contained `SKILL.md` (plus reference files) that Claude loads
on demand. They share one lightweight framework (`_system/`) so a brand voice you
define once is reused everywhere. **Everything here is a niche-neutral template** —
examples use placeholders like `[product]`, `[category]`, `example.com`, and
`your-store.myshopify.com`. No live sites, no data, and no API keys are included.

---

## Quick start

**Option A — install into Claude (recommended):**
```bash
cd _system/scripts
./install.sh            # copies every skill into ~/.claude/skills/
./doctor.sh             # verifies the install
```
On Windows, run these from Git Bash, or use Option B.

**Option B — manual:** copy each skill folder (and `_system/`) into your
`~/.claude/skills/` directory (or a project-level `.claude/skills/`).

Then, in any Claude conversation, start with **`/start-here`** — it scans your
project, helps build a brand foundation, and routes you to the right skill. Or
invoke any skill directly by name (e.g. "use keyword-research for …").

---

## How it works

- **`/start-here`** is the orchestrator. It reads your project state and either
  routes you to one skill or chains several into a workflow.
- **Brand memory** (`_system/brand-memory.md`): skills read/write a `./brand/`
  folder (voice, positioning, audience, keyword plan…). Define your voice once and
  every content skill matches it.
- **Tool detection**: skills use an MCP server if present, else an API key from
  `.env`, else they output import-ready files. Optional integrations (all
  swappable): Replicate (images/video), DataForSEO + AnswerThePublic (keyword
  data), NeuronWriter (content scoring), Shopify (publishing). Copy
  `.env.example` to `.env` and add your own keys — none ship in this package.

---

## The skills, individually

### Foundation
| Skill | What it does on its own |
|-------|--------------------------|
| **start-here** | Entry point / router. Scans the project, builds brand foundation, routes any marketing request to the right skill or workflow. |
| **brand-voice** | Extracts or builds a reusable brand voice profile so all downstream copy sounds consistent. |
| **positioning-angles** | Generates 3–5 distinct positioning angles + headline directions — the "why this, why now" hook before you write. |

### SEO research & strategy
| Skill | What it does on its own |
|-------|--------------------------|
| **keyword-research** | Generates 1,000–3,500 validated keywords (LLM + AnswerThePublic + DataForSEO) with volume, difficulty, parent-keyword clusters, and an ROI-forecasted content plan. |
| **keyword-database-article-map** | Maps every keyword to exactly one article (zero cannibalization) and produces a prioritized writing roadmap. |
| **information-gain** | Surfaces rare, citable statistics from PDFs, government reports, and papers so your content has data competitors don't. |

### Content creation
| Skill | What it does on its own |
|-------|--------------------------|
| **seo-content** | Turns a keyword/cluster into a complete, rankable article that reads like a human wrote it (structure, optimization, anti-AI voice). |
| **comparison-pages** | Playbook for X-vs-Y, alternatives-to-X, and best-[category] roundups with feature-matrix + schema discipline for commercial-intent SERPs. |
| **content-humanizer** | Rewrites robotic / AI-sounding drafts to sound genuinely human — removes AI tells and injects voice. |
| **faq-jsonld** | Generates FAQ structured data (JSON-LD) and manages it via a Shopify metafield. |

### On-page & technical SEO
| Skill | What it does on its own |
|-------|--------------------------|
| **seo-onpage-audit** | Audits a live page's on-page + technical SEO (title/meta, headings, canonical, indexability, CWV) and returns a 0–100 score + fix list. |
| **seo-page-diagnosis** | Diagnoses *why* a published article underperforms (SERP-backwards analysis, page-type mismatch) before you rewrite it. |
| **seo-schema** | Generates & validates JSON-LD beyond FAQ — Article/BlogPosting, BreadcrumbList, Product, ItemList — plus the delivery method. |
| **internal-linking** | Auto-inserts internal links into articles using semantic matching + anchor-text variation across a content cluster. |
| **image-seo-audit** | Audits images for SEO + Core Web Vitals (alt text, size, format, dimensions, lazy-load, ImageObject schema). |
| **seo-image-gen** | Generates SEO-ready images (OG cards, heroes, infographics) and applies alt text, WebP, descriptive filenames, schema. |
| **seo-backlinks** | Analyzes a domain's backlink profile (referring domains, anchors, toxic links, competitor link gaps) with a health score. |

### Distribution & growth
| Skill | What it does on its own |
|-------|--------------------------|
| **content-distribution** | Off-site amplification + AI-visibility plan (Reddit, YouTube, LinkedIn, email, entity platforms) to earn links and AI citations. |
| **content-atomizer** | Two modes. **Split:** breaks a very long article into linked child articles with distinct keywords and entity cores, via a tunable ruleset and a SERP/entity/Q&A decision cascade. **Atomize:** repurposes content into platform-native assets — including long-form X posts and LinkedIn Articles/Newsletters/series, not just short posts — plus broadcast email and infographic briefs. |
| **shopify-collection-embed** | Embeds a shoppable related-products grid inside blog articles via Shopify's public Collections AJAX API. |

### Conversion & lifecycle
| Skill | What it does on its own |
|-------|--------------------------|
| **direct-response-copy** | Writes high-converting copy (landing pages, sales pages, CTAs) using classic direct-response frameworks. |
| **email-sequences** | Builds welcome, nurture, launch, and re-engagement email sequences with subject lines, timing, and full copy. |
| **lead-magnet** | Produces 3–5 lead-magnet concepts with hooks, formats, and a bridge to the paid offer. |
| **newsletter** | Designs newsletter formats and writes publication-ready editions (roundup, deep-dive, essay, curated). |
| **creative** | AI creative engine — product photos, video, social graphics, talking heads, and ad creative from one brand kit. |

---

## Does this cover "most of SEO"?

Together these skills cover the **full on-site SEO lifecycle end to end**:

> research keywords → map to articles → write → humanize → optimize on-page →
> add schema → internal-link → optimize images → diagnose underperformers →
> distribute & earn citations

Plus the adjacent **content-marketing and conversion** layer (copy, email,
lead magnets, newsletter, creative, social repurposing).

**Strong coverage:** keyword strategy, content production, on-page / technical SEO,
structured data, internal linking, image SEO, comparison / commercial content,
off-site distribution & AI-search visibility, and conversion assets.

**Not covered (natural gaps to add later):** local SEO / Google Business Profile,
Search Console & analytics reporting / rank tracking, automated outreach & link
building, and international / multilingual SEO. A few skills (faq-jsonld,
shopify-collection-embed, and the delivery step of seo-schema / seo-onpage-audit)
assume **Shopify** — the methodology transfers to any CMS with light adaptation.

---

## Credits & attribution

Parts of this library adapt ideas and techniques from two excellent open-source
(MIT) projects by [Daniel Agrici](https://github.com/AgriciDaniel) — heavily
modified and folded into this skill framework, but credit where it's due:

- **[claude-seo](https://github.com/AgriciDaniel/claude-seo)** — SERP-clustering
  approach (keyword deduplication), GEO/AI-visibility checklist, thin-content
  heuristics, CWV & on-page reference, page-type taxonomy, schema-type reference,
  and image-SEO patterns.
- **[claude-blog](https://github.com/AgriciDaniel/claude-blog)** — research-quality
  rubric & FLOW citation model (information-gain), content-templates library,
  schema stack, editorial heuristics, cognitive-load and AI-tells checklists.

The **content-humanizer** skill builds on an MIT-licensed skill by
**Alireza Rezvani** (credited in that skill's frontmatter).

Individual files note their source inline where material was adapted. Classic
marketing frameworks referenced by name (April Dunford's positioning, Eugene
Schwartz's awareness stages, Alex Hormozi's offer framework, Nielsen's usability
heuristics) belong to their respective authors.

---

*Structure:* each skill lives in its own folder with a `SKILL.md`; shared framework
in `_system/` (brand-memory protocol, output format, JSON schemas, install / doctor
scripts). Start with `/start-here`.
