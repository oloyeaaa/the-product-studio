---
name: storefront
description: Put a built product on sale. Builds the self-contained sales page, fills the checkout checklist for the buyer's platform, and writes the delivery note. Use whenever a buyer runs /product-studio:storefront, says "put it on sale", "make the sales page", "list my product", "get this ready to sell", or has a built product with no sales page yet.
argument-hint: "[--profile <slug>] [product name or latest]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Storefront

One run takes a built product and produces everything needed to sell it: a self-contained sales page with a
real design direction, a step-by-step checkout checklist for the buyer's platform, and a delivery note. It
ends with the product marked `listed` and one clear next action.

## Step 0 - resolve the tenant, the memory, and the product

Parse `--profile <slug>` from arguments. If absent, read `defaultProfile` from
`~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If that file
is missing, tell the user to run `/product-studio:setup` and stop. Never type a literal ID or personal
value; everything comes from this config.

Then:

1. **Load the voice profile** at `~/.claude/product-studio/profiles/<slug>.voice.md` (the path in
   `voice.profilePath`). Every line of sales copy gets checked against it.
2. **Load the Brain** per the contract at `${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md`: read the ACTIVE
   Lessons rows for areas `copy`, `offer`, and `general`. Every kept lesson is a hard constraint on the
   page. If the Brain is unreachable, say so and carry on; a memory failure never blocks the deliverable.
3. **Resolve the product.** If the arguments name a product, find its Products row. Otherwise take the
   latest Products row with Status `built`. If none is `built` but one is `drafting`, offer it with a plain
   warning: "this product still has open fill-ins; the page can be built, but do not go live until they are
   done." If there is no product at all, tell the buyer to run `/product-studio:build` first and stop.
4. **Read the run JSON** from the row's Source cell
   (`~/.claude/product-studio/brain/<slug>/runs/<date>-<product-slug>.json`). This is the source of truth
   for the promise, the price, the format, and the file paths. Read the actual product files it points at;
   the "what's inside" section is written from what genuinely exists on disk, never from imagination.

## Step 1 - the sales page

Build ONE file: `~/.claude/product-studio/products/<slug>/<product-slug>/sales-page.html`. Self-contained:
inline CSS, no external fonts, images, scripts, or stylesheets. A tiny inline IntersectionObserver script
for fade-up scroll reveals, wrapped so `prefers-reduced-motion` disables it, and gated behind a `js`
class the script adds to `<html>` (hide-then-reveal styles apply only under `.js`), so the page is
fully visible when scripts do not run. Mobile-first, single column,
with a desktop breakpoint around 760px. It must look finished when opened straight from disk with no
connection.

Do not write a line of HTML until both design passes are done.

### Pass A: commit a design direction (a short written brief)

Write the brief out before coding:

- **Subject, buyer, one job**, one line each. The job is always the same: this page sells one digital
  product. The buyer comes from the run JSON.
- **Colour**: 4 to 6 named hex tokens seeded from `profile.brand.colors` (base and accent), each with a
  one-line reason tied to the product's own subject. "Trust blue" is not a reason. Derive the supporting
  tones (surface, text, muted) from the base so the page reads as one brand, not a template with two
  colours dropped in.
- **Type**: one display face and one body face, named, with system-font fallback stacks (the page loads
  nothing external). Set the scale and weights.
- **Signature**: ONE memorable element drawn from the product's own subject world: a motif, a numbering
  style, a texture, a way of labelling sections. This is what stops the page looking like every other AI
  page. It must actually appear in the built page.

### Pass B: the anti-slop critique

Interrogate the brief before coding. For every choice ask: "would I pick this exact thing for a completely
different business?" If yes, it is generic; replace it. Reject on sight: indigo or purple gradients on
white, three identical feature cards as the only layout idea, emoji used as icons, glassmorphism by
default, fake testimonials, invented statistics or invented buyer counts. Only move to code once the
direction is specific to THIS product and THIS brand.

### The page structure (fixed)

1. **Sticky top bar**: the wordmark from `profile.brand.wordmark` plus a buy button.
2. **Hero**: the run's promise as the headline, one subline, a buy CTA.
3. **The pain**: the problem this product ends, specific and felt, in the buyer's words from the run.
4. **What's inside**: the REAL contents, pulled from the actual product files on disk: real section titles,
   real template names, real lesson titles. Never invented, never padded.
5. **Honest proof**: only what exists. If no testimonials or results exist, use the concrete contents and
   spec as the proof (word counts, section counts, what ships finished) and say nothing false. No fake
   quotes, no invented numbers, ever.
6. **Price**: the run's price with its currency, framed simply, with a plain "what you get" list.
7. **FAQ**: 4 to 6 real questions a buyer would actually ask, always including how delivery works and the
   refund position.
8. **Final CTA band**: the promise restated, one buy button.
9. **Plain footer**: the wordmark, nothing clever.

### The buy buttons (the one rule the gate checks)

EVERY buy button on the page carries `data-cta="buy"` and `href="#REPLACE-WITH-CHECKOUT-LINK"`. All of them
identical, all pointing at the same placeholder. The checkout checklist owns replacing it with the real
URL. The eval gate checks that every `data-cta="buy"` marker points at exactly one distinct target; a
second target fails the run.

### The copy

Write every line through `${CLAUDE_PLUGIN_ROOT}/skills/voice/SKILL.md` against the loaded voice profile:
the buyer's voice, not a generic marketing voice. No em dashes. None of the profile's `bannedWords`. One
CTA action for the entire page: buy. No "join the newsletter", no "follow me", no second ask anywhere.
Benefit-led: the outcome the buyer walks away with, not the feature list. No fabricated numbers, no
invented urgency, no fake scarcity.

## Step 2 - the checkout checklist

Copy `${CLAUDE_PLUGIN_ROOT}/skills/storefront/templates/checkout-checklist.md` to
`~/.claude/product-studio/products/<slug>/<product-slug>/checkout-checklist.md`, next to the sales page.
Fill every `[BRACKET]` slot from the run: the product name, the price with currency, the exact asset file
to upload (the PDF, the zip of templates, or the scripts folder zipped), and the cover file (`cover.png`,
or `cover.html` with a note if no PNG was rendered). Keep only the section for
`profile.storefront.platform`; if the platform is `undecided`, keep both sections and say so.

## Step 3 - the delivery note

Write a short `DELIVERY.md` in the same folder:

- **What the customer receives**: the exact files, by name.
- **How it reaches them**: the platform's own delivery email after purchase (that is the whole fulfilment
  path in v1; nothing else to wire).
- **One test-purchase instruction**: buy it yourself once via the platform's test route and confirm the
  file arrives and opens, before sharing the page anywhere.

## Step 4 - update the Brain and re-run the gate

1. Update the Products row: Status `listed`, Sales-page path set to the sales page file. Never mark
   `listed` unless the sales page file actually exists on disk.
2. Update the run JSON: set `files.salesPage` and the status.
3. Re-run the eval gate so the sales-page checks run:
   `python "${CLAUDE_PLUGIN_ROOT}/skills/build/scripts/eval_product.py" <run.json> <profile.json>`
   (if `python` is not found, try `py` then `python3`). On failure, fix the named check and re-run, up to
   three times. Never silently ship a failed gate: if it still fails, present the work with the failure
   named and leave the Status as it was.

## Step 5 - report

End with:

- The sales page path, and "open it in a browser to see it".
- The checklist path and the delivery note path.
- The one next action: work through the checkout checklist, then replace
  `#REPLACE-WITH-CHECKOUT-LINK` in the sales page with the real checkout URL from the platform.

## Do not

- No fake testimonials, invented statistics, or invented buyer counts, anywhere on the page.
- No second CTA action. Buy is the only ask.
- No external assets the page depends on: no CDN fonts, no remote images, no linked stylesheets. The page
  must render fully from the single file, offline.
- Never mark the product `listed` until the sales page file exists on disk.
