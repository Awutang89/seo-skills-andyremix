# Link classes

Every class the classifier removes, why it is not an editorial link, and what it
looks like. Read this when a classification looks wrong, when a new farm shape
appears, or when a vendor disputes a count.

The test for `editorial` is one question: **did a human on an independent site
choose to reference this domain in content?** Everything below fails it.

Contents:
- [Behavioural classes](#behavioural-classes) — the two that catch the most
- [Encyclopaedia scrapers](#encyclopaedia-scrapers)
- [Duplication classes](#duplication-classes)
- [User-generated and machine-generated](#user-generated-and-machine-generated)
- [Tooling and directories](#tooling-and-directories)
- [Link spam](#link-spam)
- [What stays editorial](#what-stays-editorial)
- [Tuning](#tuning)

---

## Behavioural classes

Host patterns cannot catch a farm built from ordinary-looking domains. These two
detectors work on behaviour instead, and in the source audit they removed more
than every host pattern combined.

### `cross-target-farm`
**One host linking to 4+ of the candidate domains.** The largest junk class found
in the source audit. A site that links to four unrelated domains from the same
vendor shortlist is a directory, not an editor.

Examples caught: `<host-1>`, `<host-2>`,
`<host-3>`, `<host-4>`.

This only works with the whole candidate list in one input file. Classifying one
domain at a time disables it — always pass every candidate together.

### `syndicated-farm`
**One page title reused across 3+ distinct referring hosts.** Article-spinning
networks publish the same piece everywhere. Two hosts sharing a title can be
coincidence or a wire service; three is a network.

Caught by title collision, e.g. one article title
appearing on both `<host-2>` and `<host-4>`.

---

## Encyclopaedia scrapers

### `wiki-mirror`
**The most misleading class in any vendor profile.** These sites copy Wikipedia
wholesale, inheriting enormous apparent authority — a scraper can read DR≈62 —
while representing zero editorial judgement. Nobody chose to link to anything.

**A Wikipedia mirror as a domain's single
strongest backlink** is itself a finding: if a scraper is the best thing
pointing at a domain, there is no real link equity.

Shapes: `wiki<word>.com` (`wikiterminal`, `wiki386`, `wikines`, `wikithot`,
`wikifreehand`, `wikixp`, `wikious`), plus named clones — `wikiwand`, `dbpedia`,
`alchetron`, `everipedia`, `knowledger.de`, `marefa`, `wiki34`, `stringfixer`,
`zxc.wiki`, the `*-academic.com` family, and `[high-risk-host-patterns]`.

### `wikimedia-official`
Real Wikipedia, Wikibooks, Wiktionary and friends. **Genuine, but almost always
nofollow**, so it passes no equity. Kept as its own class purely so it is never
confused with the scrapers above — a real Wikipedia citation is worth reporting
even when it transfers nothing.

---

## Duplication classes

One editorial decision, counted many times. The referring-domain count inflates;
the underlying endorsement does not.

### `ftp-mirror`
Documentation and software mirrors. A single HOWTO reproduced across dozens of
university and ISP mirrors yields dozens of referring domains from one author's
decision. Hits translation and documentation domains hardest.

Shapes: `ftp.*`, `mirror(s).*`, `pub.*`, `dl.*`, plus known mirror operators
(`dotsrc.org`, `riken.jp`, `icm.edu.pl`, `nvg.ntnu.no`, `ibiblio.org`, `funet.fi`).

### `cache-archive`
Copies of someone else's page: `web.archive.org`, `archive.ph`, `megalodon.jp`,
`archive.wn.com`, `webcache`, `ipfs.io`. The link is in the archived copy, not an
independent decision.

---

## User-generated and machine-generated

Nobody vouched for anything; a machine or a passer-by emitted a URL.

### `free-blog`
Blogspot, WordPress.com, Tumblr, LiveJournal, tistory, fc2, livedoor,
`[high-risk-host-patterns]`, Medium, Substack, `sites.google.com`. Free to create, trivially spammed,
and frequently used in bulk sprays.

Watch the concentration: for three candidates in the source audit, most backlinks came from
`blogspot.com` alone. A high free-blog share is itself a finding worth reporting.

### `code-host`
GitHub, GitLab, SourceForge, Launchpad, AUR, package registries, manpage mirrors.
Overwhelmingly issue threads, dependency manifests and auto-published docs. A
GitHub issue mentioning a URL is not an endorsement.

### `qa-forum`
Stack Exchange, Reddit, Quora, bitcointalk, Discourse and phpBB boards, and any
host starting `forum.` / `forums.` / `bbs.`. User posts, not editorial.

### `mailing-list`
List archives and IRC logs: `lists.*`, `mail-archive.com`, `marc.info`, `gmane`,
`groups.google.com`, `irclogs.*`. A URL pasted into a thread in 2006.

### `tracker`
Bug trackers and issue systems: `bugs.*`, `bugzilla.*`, `jira.*`, `redmine.*`.

### `paste-shortener`
Pastebin, gist, and URL shorteners (`tinyurl`, `bit.ly`, `t.co`). A shortener link
carries no editorial signal and often no equity.

### `scraper-farm`
Free hosting used for generated content: `*.pages.dev`, `*.workers.dev`,
`*.vercel.app`, `*.netlify.app`, `*.herokuapp.com`, `*.repl.co`.

---

## Tooling and directories

### `stats-directory`
SEO and domain-stats sites that auto-generate a page for every domain in
existence: `statscrop`, `siteprice`, `hypestat`, `similarweb`, `whois*`,
`builtwith`, `netcraft`, `semrush`, `ahrefs`, `moz.com`. Every domain gets one.

### `validator-tool`
Validator and testing output: `validator.w3.org`, `jigsaw.w3.org`, `gtmetrix`,
`pingdom`, `ssllabs`. Machine-emitted. Note that a bare `w3.org` link is usually
validator output rather than a W3C citation — check the URL path before
overriding.

### `doc-share`
Slideshare, Scribd, Issuu, Academia.edu, ResearchGate, DocPlayer. Uploaded copies.

### `social`
Facebook, X, LinkedIn, Pinterest, Instagram, YouTube, Telegram. Almost always
nofollow, and never editorial in this sense.

### `mass-listing`
Title-matched, not host-matched: pages that are lists rather than articles —
*"Sites Sharing IP Addresses"*, *"Links to Other…"*, *"Directory listing"*,
*"Most Visited website list"*, *"Non-English … Information"*. A research dataset
or link dump enumerating thousands of domains is not an endorsement of any of
them.

---

## Link spam

### `link-spam`
Hosts openly advertising link sales — `bhs-links*`, `seo-anomaly`, and hosts
matching `backlink` / `pbn` / `linkbuilding` / `dofollow` in the name.

Most spam-network hosts are ordinary-looking domains that only `cross-target-farm`
catches. When a specific network is identified during an audit, add its hosts to
this class by hand for that run.

**Do not overstate these.** Check indexation first with `<SERP API>`: a
network whose pages Google has not indexed passes nothing and is not a live
penalty risk. A doorway network firing many
dofollow links can return **zero** results for `site:host/path` — real spam,
zero effect. It says what the domain is, not what the vendor did.

---

## What stays editorial

A referring domain survives when it is none of the above. Survivors look like
major news outlets, universities, research centres and academic publishers, all real
institutions that chose to link.

That is the standard. If a survivor would not plausibly appear in a list like
that, the classifier has missed a class — add it.

---

## Tuning

**Bias generous to the vendor.** Borderline hosts stay editorial. The survival
rate reported is then the optimistic reading, and a vendor cannot argue it down
— they can only argue it further in the buyer's favour, which is not a position they want
to take.

**`--min-rank` is the authority floor**, default 300 (DR≈30 on DataForSEO's
0–1000 scale). Raise it for a buyer who only wants strong links; lower it toward 0
to see the shape of the whole profile. Report the floor used alongside the number,
since the count is meaningless without it.

**Pass every candidate in one file** or `cross-target-farm` cannot fire.

**When a new farm shape appears**, prefer a behavioural rule over a host pattern.
Host lists rot; behaviour does not.

**`[high-risk-host-patterns]`** is a placeholder. Some hosts carry a high share of link spam. Add their patterns to the class that fits.

File: domain-acquisition-audit/references/link-classes.md · Version 1.0 · November 2026
