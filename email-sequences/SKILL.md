---
name: email-sequences
version: 7.0
description: "Build email sequences that convert subscribers into customers. Use when you have a lead magnet and need a welcome sequence, nurture sequence, or sales sequence. Covers welcome, nurture, conversion, launch, and re-engagement sequences. Triggers on: write welcome emails, email sequence for, nurture sequence, convert my list, onboarding emails, launch sequence, drip campaign, email funnel. Outputs complete email sequences with subject lines, timing, and full copy."
---

# Email Sequences

Most lead magnets die in the inbox. Someone downloads your thing, gets one "here's your download" email, and never hears from you again. Or worse—they get blasted with "BUY NOW" emails before you've earned any trust.

The gap between "opted in" and "bought" is where money is made or lost. This skill builds sequences that bridge that gap.

---

## Brand Memory

On every invocation, load brand context before doing anything else:

```
./brand/
  ├── voice-profile.md      [voice, tone, vocabulary rules]
  ├── positioning.md        [angles, differentiators, audience]
  ├── audience.md           [ICP, segments, pain points]
  └── creative-kit.md       [taglines, proof points, assets]
```

Check each file:
- If it exists → load it silently, confirm with ✓ in context display
- If it's missing → mark with ✗ and note: "Run /brand-voice first to create this"

Display on load:
```
BRAND CONTEXT
✓ voice-profile.md loaded
✓ positioning.md loaded
✗ audience.md — not found (run /brand-voice to create)
✗ creative-kit.md — not found
```

If all files are missing: ask "Should I run /brand-voice first, or do you want to proceed without brand context?"

---

## Iteration Detection

Before generating output, check for existing work:

```
./campaigns/{project-name}/
  ├── copy/          [existing copy files]
  ├── emails/        [existing email sequences]
  └── keywords/      [existing keyword research]
```

If files exist:
- List what's there with a one-line summary of each
- Ask: "I found existing work for this project. Do you want to (R)evise, (A)dd to it, or (S)tart fresh?"
- Wait for response before generating anything new

If no files exist:
- Proceed normally

---

## File Output Protocol

When generating output, save to the appropriate location:

```
./campaigns/{project-name}/
  ├── copy/          → landing pages, CTAs, ad copy
  ├── emails/        → sequences and individual emails
  └── keywords/      → keyword research and content plans
```

**Naming convention:**
- `{project-name}-{type}-v{n}.md` (e.g., `acme-landing-page-v1.md`)
- Increment version number on each revision

**Email sequences — file per email:**

Save each email as its own file inside `emails/{sequence-name}/`:

```
./campaigns/{project-name}/emails/{sequence-name}/
  ├── email-01-delivery.md
  ├── email-02-connection.md
  ├── email-03-value.md
  └── ...
```

Each file uses YAML frontmatter:

```yaml
---
sequence: {sequence-name}
email_number: 1
purpose: delivery
send_timing: immediately
subject_safe_bet: "[Subject line]"
subject_bold_play: "[Subject line]"
subject_personal_touch: "[Subject line]"
subject_recommended: safe_bet
preview_text: "[Preview text]"
cta: "[CTA action]"
esp: {esp-name or unknown}
version: 1
---
```

Also save a sequence index file at `emails/{sequence-name}/00-sequence-index.md` listing all emails, timing, and subjects.

**After saving:**
- Confirm the file path
- State what changed vs. previous version (if revision)
- Ask: "Ready to move to the next step?"

---

## The core job

Transform a lead magnet subscriber into a customer through a **strategic email sequence** that:
- Delivers immediate value (the lead magnet)
- Builds trust and relationship
- Creates desire for the paid offer
- Converts without being sleazy

**Output format:** Complete email sequences with subject lines, preview text, full copy, send timing, and CTAs.

---

## Sequence Types

| Sequence | Purpose | Length | When to Use |
|----------|---------|--------|-------------|
| **Welcome** | Deliver value, build relationship | 5-7 emails | After opt-in |
| **Nurture** | Provide value, build trust | 4-6 emails | Between welcome and pitch |
| **Conversion** | Sell the product | 4-7 emails | When ready to pitch |
| **Launch** | Time-bound campaign | 6-10 emails | Product launch |
| **Re-engagement** | Win back cold subscribers | 3-4 emails | Inactive 30+ days |
| **Post-Purchase** | Onboard, reduce refunds, upsell | 4-6 emails | After purchase |

---

## Before Starting: Gather Context

Get these inputs before writing any sequence:

1. **What's the lead magnet?** (What did they opt in for?)
2. **What's the paid offer?** (What are you eventually selling?)
3. **What's the price point?** (Affects how much trust-building needed)
4. **What's the bridge?** (How does free → paid make logical sense?)
5. **What voice/brand?** (Run brand-voice skill first if not defined)
6. **What objections?** (Why might they NOT buy?)

---

## ESP detection

Before writing, identify the email service provider. This affects merge tag syntax, automation trigger language, and formatting recommendations.

**Ask if not provided:** "Which ESP are you using? This affects how I format merge tags and automation notes."

| ESP | Merge tag format | Automation trigger style |
|-----|-----------------|--------------------------|
| **Mailchimp** | `*\|FNAME\|*` | Workflow / Customer Journey |
| **ConvertKit** | `{{ subscriber.first_name }}` | Sequence / Automation |
| **ActiveCampaign** | `%FIRSTNAME%` | Automation |
| **Klaviyo** | `{{ first_name }}` | Flow |
| **HubSpot** | `{{ contact.firstname }}` | Workflow |
| **Drip** | `{{ subscriber.first_name }}` | Workflow |
| **Beehiiv** | Plain name (no merge tags in body) | — |
| **Substack** | Plain text only | — |
| **Unknown / Generic** | `[FIRST NAME]` placeholder | Describe trigger in plain English |

**What to output based on ESP:**
- Use correct merge tag format in subject lines and email body
- Label automation triggers in the ESP's terminology
- Flag any features the ESP may not support (e.g., Substack has no sequences)
- If ESP is unknown, default to `[FIRST NAME]` and note: "Replace with your ESP's merge tag"

---

## The Welcome Sequence (5-7 emails)

This is the most important sequence. First impressions compound.

### Purpose
- Deliver the lead magnet
- Set expectations
- Begin the relationship
- Identify engaged subscribers
- Plant seeds for the offer

### The Framework: DELIVER → CONNECT → VALUE → BRIDGE

```
Email 1: DELIVER — Give them what they came for
Email 2: CONNECT — Share your story, build rapport
Email 3: VALUE — Teach something useful (quick win)
Email 4: VALUE — Teach something else (builds authority)
Email 5: BRIDGE — Show what's possible with more help
Email 6: SOFT PITCH — Introduce the offer gently
Email 7: DIRECT PITCH — Make the ask
```

### Email 1: Delivery (Send immediately)

**Purpose:** Deliver the lead magnet, set expectations, get first micro-engagement.

**Subject line formulas:**
- "[Lead magnet name] is inside"
- "Your [lead magnet] + quick start guide"
- "Here's [what they asked for]"

**Structure:**
```
[Greeting — keep it simple]

[Deliver the goods — link to lead magnet]

[Quick start — one action they can take in next 5 minutes]

[Set expectations — what emails are coming]

[Micro-CTA — hit reply, answer a question, or take one action]

[Sign off]
```

**Example:**
```
Hey,

Your positioning skill is attached. Here's how to use it in 60 seconds:

1. Download the .md file
2. Add it to Claude Code (or paste into any Claude conversation)
3. Ask Claude: "Find positioning angles for [your product]"

That's it. Try it on whatever you're working on right now.

Over the next week, I'll send you a few emails showing how to get the most out of this skill—and what else is possible when Claude has real methodology instead of generic prompts.

Quick question: What are you hoping to use this for? Hit reply and let me know. I read every response.

— James
```

**Timing:** Immediately after opt-in

---

### Email 2: Connection (Day 2)

**Purpose:** Build rapport through vulnerability and shared experience.

**Subject line formulas:**
- "Why I created [lead magnet]"
- "The mistake that led to this"
- "Quick story about [topic]"

**Structure:**
```
[Story hook — specific moment or realization]

[The struggle — what you went through]

[The insight — what you learned]

[The connection — how this relates to them]

[Soft forward reference — hint at what's coming]

[Sign off]
```

**Example:**
```
Quick story:

Two years ago, I spent $2,400 on a brand strategist. She was smart. She delivered a 47-page PDF. It sat in my Google Drive for six months.

Not because it was bad. Because I didn't know how to USE it.

That's when I realized: frameworks without implementation are just expensive decoration.

So I started building something different. Not strategy decks. Not consulting. Something you could actually use, immediately, every time you needed it.

That's what the positioning skill is—strategy that executes itself.

Tomorrow I'll show you what Sarah found when she ran it on her SaaS product. (Her exact words: "I've been explaining this wrong for two years.")

— James
```

**Timing:** Day 2

---

### Email 3: Value (Day 4)

**Purpose:** Teach something useful. Demonstrate expertise. Create a quick win.

**Subject line formulas:**
- "The [X] mistake everyone makes"
- "Try this: [specific tactic]"
- "What [person] discovered about [topic]"

**Structure:**
```
[Hook — insight or observation]

[The problem — what most people get wrong]

[The solution — what to do instead]

[Example or proof — show it working]

[Action step — what they can do right now]

[Sign off]
```

**Timing:** Day 4

---

### Email 4: More Value (Day 6)

**Purpose:** Continue building trust. Different angle or topic.

**Subject line formulas:**
- "[Number] things that [outcome]"
- "The question I get most"
- "This changed how I think about [topic]"

**Structure:** Same as Email 3, different topic.

**Timing:** Day 6

---

### Email 5: Bridge (Day 8)

**Purpose:** Show the gap between where they are and where they could be. Introduce concept of the paid offer without pitching.

**Subject line formulas:**
- "You can [do X] now. But can you [do Y]?"
- "The next step most people miss"
- "What [lead magnet] doesn't do"

**Structure:**
```
[Acknowledge progress — what they can now do with the lead magnet]

[Reveal the gap — what they still can't do]

[Paint the picture — what's possible with the full solution]

[Soft mention — the offer exists, no hard sell]

[Sign off]
```

**Example:**
```
By now you've probably run the positioning skill on at least one project.

You can find angles. That's the foundation.

But here's what you can't do with just one skill:

- Turn that angle into a landing page that converts
- Write emails that get opened and clicked
- Create content that ranks AND reads well
- Build sequences that turn subscribers into customers

The positioning skill is 1 of 9 in the full system.

Each skill handles a different piece: copy, content, newsletters, lead magnets, email sequences, content distribution.

Together they give Claude a complete marketing methodology—not prompts, but the actual frameworks behind $400k+ in revenue.

I'll tell you more about it tomorrow. For now, keep using the positioning skill. It's yours forever.

— James
```

**Timing:** Day 8

---

### Email 6: Soft Pitch (Day 10)

**Purpose:** Introduce the offer properly. Handle objections. Let them self-select.

**Subject line formulas:**
- "The full system (if you want it)"
- "Should you get [product]? Let's see."
- "This isn't for everyone"

**Structure:**
```
[Transition — building on bridge email]

[The offer — what it is, what's included]

[Who it's for — specific situations]

[Who it's NOT for — disqualification]

[Social proof — if available]

[The ask — soft CTA, no urgency yet]

[Sign off]
```

**Timing:** Day 10

---

### Email 7: Direct Pitch (Day 12)

**Purpose:** Make the clear ask. Create urgency if authentic.

**Subject line formulas:**
- "Last thing about [product]"
- "[Product] — yes or no?"
- "Quick decision"

**Structure:**
```
[Direct opener — no buildup]

[Restate core value — one sentence]

[Handle remaining objection — the big one]

[Urgency — if real (price increase, bonus deadline, limited)]

[Clear CTA — exactly what to do]

[Final thought — personal note]

[Sign off]
```

**Timing:** Day 12

---

## The Conversion Sequence (4-7 emails)

For when you're ready to pitch—either after welcome sequence or as a standalone campaign.

### The Framework: OPEN → DESIRE → PROOF → OBJECTION → URGENCY → CLOSE

```
Email 1: OPEN — Introduce the offer, core promise
Email 2: DESIRE — Paint the transformation, show the gap
Email 3: PROOF — Testimonials, case studies, results
Email 4: OBJECTION — Handle the biggest "but..."
Email 5: URGENCY — Why now matters (if authentic)
Email 6: CLOSE — Final push, clear CTA
Email 7: LAST CALL — Deadline reminder (if applicable)
```

### Timing
- Standard: Every 2 days
- Launch: Daily or every other day
- Deadline: Final 3 emails in 3 days

---

## The Launch Sequence (6-10 emails)

For time-bound campaigns: product launches, promotions, cohort opens.

### The Framework: SEED → OPEN → VALUE → PROOF → URGENCY → CLOSE

**Pre-Launch (Optional, 1-2 emails):**
- Seed interest, build anticipation
- "Something's coming" without revealing

**Cart Open (2-3 emails):**
- Announcement, full details
- Value deep-dive, transformation
- Social proof, testimonials

**Mid-Launch (2-3 emails):**
- Objection handling
- Case study or story
- FAQ or "is this for me?"

**Cart Close (2-3 emails):**
- Urgency (24-48 hours)
- Final testimonial
- Last call (deadline day)

### Launch Email Timing
```
Day -3: Seed (optional)
Day -1: Coming tomorrow
Day 0: Cart open (morning)
Day 0: Cart open (evening, different angle)
Day 2: Deep-dive on value
Day 4: Social proof
Day 5: Objection handling
Day 6: 48-hour warning
Day 7: 24-hour warning (morning)
Day 7: Final hours (evening)
Day 7: Last call (before midnight)
```

---

## The Re-engagement Sequence (3-4 emails)

For subscribers who haven't opened in 30+ days.

### The Framework: PATTERN INTERRUPT → VALUE → DECISION

```
Email 1: Pattern interrupt — different subject line style, acknowledge absence
Email 2: Pure value — best content, no ask
Email 3: Direct question — do you want to stay?
Email 4: Final — removing from list (creates urgency)
```

### Subject Line Examples
- "Did I do something wrong?"
- "Should I stop emailing you?"
- "Breaking up is hard to do"
- "You're about to miss [thing]"
- "[First name], still there?"

---

## Subject Line Formulas

### What Gets Opens

**1. Curiosity Gap**
- "The [X] mistake that cost me [Y]"
- "Why [surprising thing] actually works"
- "I was wrong about [topic]"

**2. Direct Benefit**
- "How to [outcome] in [timeframe]"
- "[Number] ways to [benefit]"
- "The fastest way to [result]"

**3. Personal/Story**
- "Quick story about [topic]"
- "What happened when I [action]"
- "The email I almost didn't send"

**4. Question**
- "Can I ask you something?"
- "What would you do with [outcome]?"
- "Are you making this mistake?"

**5. Urgency (when real)**
- "[X] hours left"
- "Closing tonight"
- "Last chance: [offer]"

**6. Pattern Interrupt**
- "." (just a period)
- "So..."
- "Bad news"
- "[First name]"

### What Kills Opens

- ALL CAPS
- Excessive punctuation!!!
- "Newsletter #47"
- "[COMPANY NAME] Weekly Update"
- Clickbait that doesn't deliver
- Same format every time

---

## Subject line variants

Every email in a sequence gets three subject line options — never one.

**The three strategies:**

| Variant | Strategy | Tone |
|---------|----------|------|
| **Safe Bet** | Clear + specific benefit | Direct, informational |
| **Bold Play** | Provocation or pattern interrupt | Edgy, contrarian |
| **Personal Touch** | Conversational, first-person | Casual, human |

**Deliver as:**

```
Subject line options for Email [N]:
- Safe Bet:       "[Subject line]"
- Bold Play:      "[Subject line]"
- Personal Touch: "[Subject line]"
Recommended: [Which one + one-line reason]
```

**Sequence position affects subject strategy:**
- Email 1 (cold/new subscriber): Safe Bet or Personal Touch — earn trust before provocation
- Emails 2-4 (warming up): Bold Play becomes more viable as relationship builds
- Final email (conversion): Safe Bet — clarity over cleverness at decision point

**The test:** Read each subject line out of context. Does it sound like something a real person sent you? If it sounds like marketing, rewrite it.

---

## Email Copy Principles

### The P.S. Is Prime Real Estate
40% of people read the P.S. first. Use it for:
- The core CTA
- A second hook
- Personal note
- Deadline reminder

### One CTA Per Email
Multiple CTAs = no CTAs. Every email should have ONE clear action.

Exception: Delivery email can have "download" + "reply with question"

### Short Paragraphs
1-3 sentences max. Email is scanned, not read.

### Preview Text Matters
First 40-90 characters appear in inbox preview. Make them count.

**Bad:** "Having trouble viewing this email?"
**Good:** "[Continuation of subject line curiosity]"

### Open Loops
Create curiosity within emails:
- "I'll explain why tomorrow."
- "But that's not even the interesting part."
- "The third one surprised me."

### Specificity Creates Credibility
- Not "made money" → "$47,329 in one day"
- Not "many customers" → "2,847 customers"
- Not "recently" → "Last Tuesday"

---

## Sequence Architecture Patterns

### The Straight Line
```
Email 1 → Email 2 → Email 3 → Email 4 → Pitch
```
Simple. Works for short sequences. No branches.

### The Branch
```
Email 1 → Email 2 → [Clicked?] → YES: Pitch sequence
                              → NO: More value sequence
```
Behavior-based. More sophisticated. Requires automation.

### The Hybrid
```
Welcome (5 emails) → [Wait 7 days] → Conversion (5 emails) → [No purchase] → Nurture (ongoing)
```
Full lifecycle. Most complete.

---

## Timing Guidelines

### Send Frequency by Sequence

| Sequence | Frequency | Notes |
|----------|-----------|-------|
| Welcome | Days 0, 2, 4, 6, 8, 10, 12 | Front-load value |
| Nurture | Weekly or 2x/week | Consistent rhythm |
| Conversion | Every 2 days | Enough touch without annoying |
| Launch | Daily or every other day | Intensity justified by deadline |
| Re-engagement | Days 0, 3, 7, 10 | Give time to respond |

### Best Send Times

These are starting defaults — always test against your own list. Audience behavior beats industry averages.

| Audience type | Best days | Best times (recipient timezone) | Avoid |
|---------------|-----------|--------------------------------|-------|
| **B2B / professionals** | Tue–Thu | 9–11am | Mon AM, Fri PM, weekends |
| **B2C / consumers** | Tue–Thu | 7–9am or 7–9pm | Mon AM, Fri PM |
| **Creators / solopreneurs** | Any day | 8–10am | No strong pattern — test |
| **E-commerce** | Tue, Thu, Sat | 10am or 8pm | Sunday AM |
| **Newsletter readers** | Consistent day/time | Match your established cadence | Inconsistency itself |

**Send-time notes:**
- "Recipient timezone" matters more than your timezone — use ESP timezone detection if available
- For launch sequences with deadlines: send final email 1-2 hours before midnight of deadline day
- Re-engagement emails: Wednesday or Thursday tends to outperform — midweek, midday
- The best send time is the one your specific audience responds to — run a send-time A/B test after 500+ subscribers

### When to Start Selling
- Low price (<$100): After 3-5 value emails
- Medium price ($100-500): After 5-7 value emails
- High price (>$500): After 7-10 value emails or sales call

Trust required scales with price.

---

## Output Format

### Sequence Overview

```
# [Sequence Name] — [Product/Offer]

## Sequence Goal
[What this sequence accomplishes]

## Timing
[Send schedule]

## Emails

### Email 1: [Name]
**Send:** [Timing]
**Subject:** [Subject line]
**Preview:** [Preview text]
**Purpose:** [What this email does]

[Full email copy]

---

### Email 2: [Name]
...
```

### Individual Email Template

Each email is saved as its own `.md` file with YAML frontmatter:

```
---
sequence: [sequence-name]
email_number: [N]
purpose: [delivery | connection | value | bridge | soft-pitch | pitch | re-engagement]
send_timing: [immediately | day-2 | day-4 | trigger: clicked-link]
subject_safe_bet: "[Subject line]"
subject_bold_play: "[Subject line]"
subject_personal_touch: "[Subject line]"
subject_recommended: [safe_bet | bold_play | personal_touch]
preview_text: "[First 60 chars]"
cta: "[Action the reader takes]"
esp: [mailchimp | convertkit | activecampaign | klaviyo | unknown]
version: 1
---

[FULL EMAIL COPY]

---
P.S. [If applicable]
```

---

## Example: Welcome Sequence for Skills Pack Lead Magnet

### Context
- Lead magnet: Free positioning-angles skill
- Paid offer: 9-skill marketing pack ($149)
- Bridge: One skill → want the other 8
- Audience: Founders/marketers using Claude

### Email 1: Delivery

**Send:** Immediately
**Subject:** Your positioning skill is inside
**Preview:** Here's how to use it in 60 seconds

Hey,

Your positioning skill is attached. [LINK]

Here's how to use it in 60 seconds:

1. Download the .md file
2. Add it to Claude Code (or paste into a Claude conversation)
3. Ask: "Find positioning angles for [your product]"

That's it. Try it right now on whatever you're working on.

Over the next week, I'll send you a few emails showing how to get more out of this—plus what happens when Claude has an entire marketing methodology instead of one skill.

Quick question: What project are you hoping to use this for? Hit reply and tell me. I read every one.

— James

---

### Email 2: Connection

**Send:** Day 2
**Subject:** Why I built this (quick story)
**Preview:** $2,400 on a strategist and nothing to show for it

Quick story:

Two years ago I hired a brand strategist. $2,400. She delivered a 47-page PDF.

It sat in my Google Drive for six months.

Not because it was bad. Because I had no idea how to implement it. Every time I tried to write a landing page or position an offer, I'd open the PDF, get overwhelmed, and close it.

That's when I realized: Frameworks without implementation are expensive decoration.

So I started building something different.

Not strategy decks. Not consulting. Something you could actually USE—every time you needed to write copy, find an angle, plan content, or build a sequence.

The positioning skill you downloaded? That's one piece.

Tomorrow I'll show you what happened when Sarah ran it on her SaaS product. (Her words: "I've been explaining this wrong for two years.")

— James

---

### Email 3: Value/Proof

**Send:** Day 4
**Subject:** What Sarah found in 12 minutes
**Preview:** "I've been explaining this wrong for two years"

Sarah runs a SaaS tool for freelancers. Revenue had plateaued.

She'd tried:
- New features (users didn't care)
- Price changes (didn't move the needle)
- More content (traffic but no conversions)

Then she ran the positioning skill.

12 minutes later, she had 5 distinct angles she'd never considered.

The winner: Stop positioning as "invoicing software." Start positioning as "get paid faster without awkward follow-ups."

Same product. Different angle. Her landing page conversion went from 2.1% to 4.7%.

The skill didn't write her landing page. It found the angle that made everything else easier.

That's what methodology does—it changes what you see.

Try it again today. Pick something that's not converting the way you want. Find the angle you've been missing.

— James

P.S. Tomorrow: the one thing the positioning skill can't do (and why it matters).

---

### Email 4: Bridge

**Send:** Day 6
**Subject:** You can find angles now. But can you do this?
**Preview:** What one skill doesn't cover

By now you've probably found a few angles using the skill.

That's the foundation. Positioning is where everything starts.

But here's what you can't do with just one skill:

- Turn that angle into a landing page that converts
- Write an email sequence that turns subscribers into customers
- Create content that ranks AND reads well
- Build a lead magnet that actually gets downloaded
- Atomize one piece of content into 15 platform-native posts

The positioning skill is 1 of 9.

Together they give Claude a complete marketing methodology. Not prompts—methodology. The frameworks behind $400k+ in 9 months.

I'll tell you more about the full system tomorrow.

For now, keep finding angles. The skill is yours forever.

— James

---

### Email 5: Soft Pitch

**Send:** Day 8
**Subject:** The full system (if you want it)
**Preview:** 9 skills, one methodology, $149

You've been using the positioning skill for a week.

If you're finding it useful, here's what else is available:

**The Marketing & SEO Skills Pack — $149**

9 skills that give Claude a complete marketing methodology:

| Skill | What It Does |
|-------|--------------|
| brand-voice | Defines how you sound |
| positioning-angles | Finds angles that sell (you have this) |
| keyword-research | Identifies what to write about |
| lead-magnet | Creates opt-in offer concepts |
| direct-response-copy | Writes pages that convert |
| seo-content | Writes content that ranks |
| newsletter | Creates email editions |
| email-sequences | Builds sequences that convert |
| content-atomizer | Turns 1 piece into 15 |

Plus the orchestrator—a meta-skill that tells you which skill to run and in what order.

**This is for you if:**
- You use Claude for marketing but get generic output
- You know methodology matters but don't have time to learn it all
- You want a system, not random prompts

**This is NOT for you if:**
- You've never used Claude (start there first)
- You want someone to do it for you (this is a tool, not a service)
- You don't do your own marketing

$149 once. All 9 skills. All future updates.

[GET THE FULL SYSTEM]

No pressure. The positioning skill is yours either way.

— James

---

### Email 6: Direct Pitch

**Send:** Day 10
**Subject:** Last thing about the skills pack
**Preview:** Then I'll stop talking about it

Last email about this, then I'll leave you alone.

The skills pack is $149. That's $16.55 per skill.

For context:
- A brand strategist charges $2,000-5,000
- A positioning consultant charges $3,000-10,000
- A copywriter charges $500-2,000 per page

You get methodology that handles all of it. Reusable. Forever.

The question isn't "is $149 a lot?" It's "what's one good landing page worth?"

If a better angle, clearer copy, or smarter content strategy gets you even ONE extra customer, you've made the money back.

[GET THE SKILLS PACK — $149]

If you have questions, hit reply. I answer everything.

— James

P.S. 200+ marketers are using this system. Join them: [LINK]

---

### Email 7: Final

**Send:** Day 12
**Subject:** Quick question
**Preview:** And then back to regularly scheduled programming

Quick question:

Did you decide on the skills pack?

Either answer is fine. But if something's holding you back, I'd love to know what it is. Hit reply and tell me.

After this, I'll go back to regular emails—tactics, strategies, things I'm learning. No more pitching.

If you want the skills pack later, it'll be here: [LINK]

— James

---

## How This Connects to Other Skills

**email-sequences uses:**
- **brand-voice** — Ensures email voice matches brand
- **positioning-angles** — The angle informs the pitch
- **lead-magnet** — The sequence delivers the lead magnet
- **direct-response-copy** — Individual emails use copy principles

**email-sequences feeds:**
- **content-atomizer** — Best emails can become social content
- **newsletter** — Sequence insights inform newsletter strategy

**The flow:**
1. **lead-magnet** creates the opt-in offer
2. **email-sequences** builds the welcome → conversion path
3. **direct-response-copy** principles inform each email
4. Subscriber becomes customer

---

## The Test

A good email sequence passes all 10:

1. **Delivers value before asking** — At least 3-5 value emails before any pitch
2. **Has clear purpose per email** — Each email does ONE job; no email tries to do two things
3. **Sounds human** — Read aloud: does it sound like a person or a marketing team?
4. **Creates momentum** — Each email ends in a way that makes the next feel anticipated
5. **Handles objections** — Pre-empts the "but..." before the reader thinks it
6. **Has one CTA** — Every email drives one action (two CTAs = zero CTAs)
7. **Respects the reader** — Easy to unsubscribe, no dark patterns, no manufactured urgency
8. **Subject lines pass the inbox test** — Does each subject line look like something a real person sent? Would you open it?
9. **Preview text earns the open** — First 60 characters continue the subject line's hook, not "Having trouble viewing this email?"
10. **Readable on mobile** — Short paragraphs (1-3 sentences), no walls of text, links tap-friendly

**Failure mode to watch for:** The sequence escalates into "BUY NOW BUY NOW" without earning it. If emails 1-4 are weak value, emails 5-7 will be ignored.

**The read-aloud test:** Read every email out loud before approving it. If you stumble, rewrite. If it sounds like a newsletter from 2012, rewrite. If you wouldn't send it to a friend, rewrite.

---

## Output Summary Format

End every output with this summary block:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILL: email-sequences | PROJECT: [project-name] | v[n]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLETED: [What was produced — 1 line]
SAVED TO:  [File path if saved]
NEXT STEP: [Recommended next action]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## What to run next

A sequence is stronger with supporting assets. Once the emails are done:

- **Landing page:** Run `/direct-response-copy` to write the page the sequence points to
- **Angles:** Run `/positioning-angles` if the sequence isn't converting
- **Keywords:** Run `/keyword-research` to find content topics for a nurture series

---

## Feedback

After every output, ask:

> "Before we move on — did this hit the mark?
> - (Y) Yes, this works
> - (T) Tweak it — [tell me what to change]
> - (R) Redo — different direction entirely"

If (T): make the requested change and re-deliver.
If (R): ask one clarifying question, then regenerate.
If no response: proceed to next step.
