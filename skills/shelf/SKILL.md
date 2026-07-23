---
name: shelf
description: The readout of the Product Studio's memory - what is drafting, built, listed, selling, and killed, plus the format and offer lessons currently binding every build. Use when the buyer runs /product-studio:shelf, asks "what have we built", "what's on sale", "what sold", "show me the shelf", or returns to The Product Studio and wants to see where things stand.
argument-hint: "[--profile <slug>]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Shelf

One screen from the Brain: memory made visible. This is what a returning buyer sees first. It reads, and
writes only when the buyer answers the revenue nudge.

## Step 0 - tenant resolution

Follow the Brain contract at `${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md`: parse `--profile <slug>` from
arguments; if absent read `defaultProfile` from `~/.claude/product-studio/config.json`; load
`~/.claude/product-studio/profiles/<slug>.json`; if missing, tell the user to run `/product-studio:setup`
and stop.

## Step 1 - read the Brain

Read the Products and Lessons tables per the Brain contract, in whichever mode the config says:

- Local: parse the pipe tables at `~/.claude/product-studio/brain/<slug>/products.md` and `lessons.md`
  (skip header and separator rows, reverse the `<br>` and `\|` escaping when reading cells back).
- Airtable: list records from `config.brain.airtable.tables.products` and `tables.lessons` using the base ID
  from `config.brain.airtable.baseId`.

If the Brain is empty or missing (no folder, no rows, or Airtable unreachable), say plainly: "nothing here
yet, run /product-studio:build". Do not invent content, and stop there.

## Step 2 - present one screen

Everything on one screen, grouped by Status in this order. Numbers first, scannable, no padding. For each
product show: the product, its promise, its price, the asset path, and the sales-page path (when one
exists).

### Drafting
Products with Status = `drafting`: also note what is blocking them (usually open fill-ins from the run
file).

### Built
Products with Status = `built`: finished on disk, not yet on sale. The obvious next step for each is
`/product-studio:storefront`.

### Listed
Products with Status = `listed`: on sale. Show Revenue if the buyer has reported any; show blank as blank,
never zero-fill or invent.

### Selling
Products with Status = `selling`: proven sellers. Show the Revenue running total.

### Killed
Products with Status = `killed`: the product plus the one-line why (from the row and its kill lesson).
Never soften a kill: the reason is the value.

### Lessons binding every build
The Active Lessons rows with Area `format` or `offer`, verbatim, plus the count of all Active rows. These
are the constraints the next `/product-studio:build` obeys.

## Step 3 - the one nudge

Check for `listed` products whose Added date (or listing date, if the run file records one) is more than 14
days ago AND whose Revenue cell is blank. If any exist, ask ONCE, for the oldest one:

> "<Product> has been on sale for over two weeks. Did it sell? Tell me the number and I'll learn from it."

If the buyer answers with a number:
- Write it into that Products row's Revenue cell (and flip Status to `selling` if it is selling steadily).
- Capture what the answer teaches as ONE Lessons row, Source = `performance` (e.g. sold well at that price:
  an `offer` lesson; sold nothing: ask the buyer what they think happened and record that as the rule).
  Apply the Brain contract's dedup rule first.

If they don't answer or say "not yet", note it and move on. Ask once per shelf run, never a pile of nags.

## Step 4 - one next action

End with exactly one next action, chosen from the state of the shelf. Examples: "1 product is built but not
listed: run /product-studio:storefront", "nothing is drafting or built: run /product-studio:build", "2
listed products have no revenue reported: check your store dashboard and tell me the numbers".

## Rules

- Never invent a row, a number, or a revenue figure. Everything on the shelf traces to a Brain row.
- Never soften a kill. Killed means killed, with the reason.
- Numbers first: counts, prices, revenue lead every line they belong to.
- Scannable: short lines, no paragraphs, one screen.
