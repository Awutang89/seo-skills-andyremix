---
name: shopify-collection-embed
description: "Embed a related products collection grid inside Shopify blog articles using the public Collections AJAX API. Use when you want to display shoppable product grids inside blog content — no app install, no theme edits, no auth required. Triggers on: insert collection in article, embed products in blog post, add related products to article, add shop widget to article."
---

# Shopify Collection Embed

Inserts a self-contained HTML/JS widget into article files that fetches and renders a live product grid from any Shopify collection — inline, inside the article body. Requires no app, no theme edit, and no API key on the frontend.

---

## How it works

A small `<script>` block placed in `body_html` calls the public endpoint:

```
/collections/{handle}/products.json?limit=4
```

This endpoint is unauthenticated and available on any Shopify store. The script renders a 4-product grid with images, titles, prices, and a "View All →" link to the collection page.

---

## When to use this skill

- You want to monetize a blog article by showing relevant products
- You're adding new articles and want collection widgets from the start
- You need to update the collection a widget points to

**Do not use** if the article is not yet uploaded to Shopify (run your publish step first).

---

## Key files

| File | Purpose |
|------|---------|
| `your-project/snippets/related-collection.html` | Master template with `[collection-handle]` placeholder |
| `your-project/snippets/collection-mapping.md` | Maps each article to its collection handle |
| `your_snippet_inserter.py` | Insert the snippet into each article's HTML (idempotent) |
| `your_handle_fixer.py` | Correct wrong collection handles in already-inserted snippets |
| `your_padding_fixer.ps1` | Adjust CSS padding alignment across all files |
| `your-project/shopify-article-ids.csv` | Maps article filenames to Shopify article IDs |
| `your_shopify_push.ps1` | Your Shopify single-article push step (edit `$filename` var) |
| `your_shopify_batch_push.ps1` | Your Shopify batch push step — push existing articles, post any new ones |

---

## Confirmed collection handles (example.com)

These are example handles. Verify each against your live store before use — only use handles that resolve:

| Handle | URL |
|--------|-----|
| `[collection-handle]` | `/collections/[collection-handle]` |
| `best-sellers` | `/collections/best-sellers` |
| `new-arrivals` | `/collections/new-arrivals` |
| `category-a` | `/collections/category-a` |
| `product-type-b` | `/collections/product-type-b` |

> **Tip:** Verify a handle before using it by visiting `example.com/collections/{handle}/products.json` in the browser. If it returns `{"products":[...]}` the handle is valid.

---

## Workflow

```
MAP → INSERT → VERIFY HANDLES → PUSH TEST → PUSH ALL
```

---

### Step 1 — Map articles to collections

Open `your-project/snippets/collection-mapping.md` and confirm or update the collection handle for each article you want to embed.

Use the handle list above. Choose the most specific collection that fits the article topic.

---

### Step 2 — Insert snippets into HTML files

Run the insert script. It is **idempotent** — it skips files that already have the snippet:

```powershell
python your_snippet_inserter.py   # insert the snippet into each article's HTML (idempotent)
```

The script inserts the snippet **just before `<h2>FAQ</h2>`** in each article. Fallback: before the schema markup line. Second fallback: appended to end.

---

### Step 3 — Verify handles are correct

After inserting, confirm the collection handle in each file matches a real collection. The quickest check:

```
https://example.com/collections/{handle}/products.json
```

If it returns products → handle is correct.
If it returns `{"products":[]}` → handle exists but collection is empty.
If it returns 404 → handle is wrong.

To fix wrong handles across multiple files, correct the collection handles and run your handle-fix step:

```powershell
python your_handle_fixer.py   # correct wrong collection handles
```

---

### Step 4 — Push one article to test

Edit `$filename` in your single-article push step to the article you want to test, then run:

```powershell
powershell -ExecutionPolicy Bypass -File your_shopify_push.ps1   # your Shopify single-article push step
```

Visit the live article. The "Shop Related" section should appear and load products.

---

### Step 5 — Push all articles

Once the test article looks correct, run the batch script to update all remaining articles:

```powershell
powershell -ExecutionPolicy Bypass -File your_shopify_batch_push.ps1   # your Shopify batch push step
```

This step:
- **PUTs** your existing articles already in `shopify-article-ids.csv`
- **POSTs** any new articles not yet in Shopify (as drafts)
- Logs every article filename, ID, and Shopify handle
- Appends new article IDs to `shopify-article-ids.csv` automatically

---

## CSS and styling notes

The snippet includes scoped styles using `.rc-*` class names — they will not conflict with theme CSS.

**Current CSS settings (as tuned):**
```css
.rc-related { margin: 2rem 0; padding: 1.5rem 0; border-top: 2px solid #e5e7eb; }
```

- `padding: 1.5rem 0` — top/bottom padding only; left/right is zero so content aligns with article text
- `border-top` — horizontal rule separating snippet from article content

To adjust padding across all files:

```powershell
powershell -ExecutionPolicy Bypass -File your_padding_fixer.ps1   # adjust CSS padding across all files
```

Then re-push the affected articles.

---

## Credentials required

All stored in `.env`:

```
SHOPIFY_CLIENT_ID=...
SHOPIFY_CLIENT_SECRET=...
SHOPIFY_STORE_URL=your-store.myshopify.com
SHOPIFY_BLOG_ID=...
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Loading products..." stuck | Collection handle wrong or collection has no products | Verify handle via browser, correct the handle, re-push |
| "See our full collection." | Handle is valid but collection has 0 published products | Add products to collection in Shopify admin |
| Widget doesn't appear at all | Snippet not in the HTML file | Re-run your snippet-insert step, or re-insert any missing snippets |
| Content misaligned (left gap) | Left padding on `.rc-related` | Run your padding-fix step, re-push |
| API push fails with 400 | `.env` credentials wrong or expired | Check `SHOPIFY_CLIENT_ID` and `SHOPIFY_CLIENT_SECRET` in `.env` |
| "Not a valid shop domain" | `SHOPIFY_STORE_URL` has wrong format | Must be `storename.myshopify.com` — no `https://`, no trailing slash |
