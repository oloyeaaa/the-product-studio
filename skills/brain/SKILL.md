---
name: brain
description: Use whenever any module needs to read or write the Product Studio's memory (the Brain) - reading active lessons and killed products before a build, logging a product after a build, or capturing a lesson from a kill, a correction, or a sale. Trigger on "log to the brain", "check lessons", "what has been built", "what got killed", "what sold", or any module about to produce or judge a product. This is the one contract; it is not a user-facing command.
---

# Brain

The Brain is the memory of The Product Studio. It is not one build's private notebook: every build, kill,
and lesson lands in the same two tables so The Product Studio learns THIS buyer's format, structure, and
what actually sold, and never starts from zero.

This file is the ONE contract. Every skill, command, and agent that touches the Brain points here instead of
re-describing the rules.

## Step 0 - tenant resolution (do this first, every time)

Parse `--profile <slug>` from arguments. If absent, read `defaultProfile` from
`~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If that file
is missing, tell the user to run `/product-studio:setup` and stop. Never type a literal ID or personal
value; everything comes from this config, including `config.brain.mode` and, for airtable mode,
`config.brain.airtable`.

## The loop contract

Every module that produces or judges products obeys this:

1. **Before producing:** read Lessons rows where `Active` = true and `Area` matches the module's area (plus
   `general`), AND read every Products row where `Status` = killed. Apply every kept lesson as a hard
   constraint, and never rebuild what got killed.
2. **After a build:** append one Products row.
3. **When a product is killed or a rule is taught:** write one Lessons row. Keep it an imperative rule,
   under 100 characters, `Active` = true.
   **The dedup rule:** before writing, read the existing Active lessons for that Area plus `general`. If one
   already covers the same rule (same constraint in different words), do not add a duplicate: tell the user
   which existing lesson already covers it and stop. Only genuinely new rules get a row.
4. **Degrade gracefully:** if the Brain is unreachable (no local files yet, Airtable not connected, a read or
   write fails), say so in the output, skip the logging step, and never block the deliverable on a Brain
   failure.

## The schema (same columns in both modes)

### Products
| Column | Notes |
|---|---|
| Product | one line, what it is |
| Idea source | validator run/row path, or "brief" |
| Buyer | who it is for, specific |
| Format | pdf-guide / ebook / template-pack / worksheet / checklist / prompt-pack / course / video-script |
| Promise | the one-line outcome promise, carried from the idea |
| Price | the price (or band) carried from the idea, inside the comfort band |
| Status | drafting / built / listed / selling / killed |
| Asset path | where the finished product lives on disk |
| Sales-page path | where the sales page lives (blank until storefront runs) |
| Revenue | running total the buyer reports (blank until sales exist; never invented) |
| Source | run file path |
| Added | date |

### Lessons
| Column | Notes |
|---|---|
| Rule | the lesson, imperative, one line, under 100 characters |
| Area | format / offer / copy / general |
| Active | checkbox, only Active rows are applied |
| Source | kill reason / manual / performance |
| Added | date |

Areas for this system: `format` (this buyer's structure and format preferences, what shape sold), `offer`
(pricing and promise learnings), `copy` (sales-page voice rules), `general`.

## Mode 1: local (default, zero dependencies)

Files live at `~/.claude/product-studio/brain/<slug>/`:

```
~/.claude/product-studio/brain/<slug>/
  products.md
  lessons.md
  runs/          (build run files, written by the build skill; not a pipe table)
```

If this folder does not exist yet, tell the user to run `/product-studio:setup-brain` and treat the Brain as
unreachable for this run (degrade gracefully, do not block).

### Exact markdown table format

Every local Brain table is a pipe table with a fixed header row and a separator row, so every module reads
and writes it identically. Append new rows at the bottom. Never reorder or rename columns.

**products.md**
```
| Product | Idea source | Buyer | Format | Promise | Price | Status | Asset path | Sales-page path | Revenue | Source | Added |
|---|---|---|---|---|---|---|---|---|---|---|---|
| <one line> | brief | <specific buyer> | pdf-guide | <outcome promise> | 29 GBP | built | products/<slug>/<product-slug>/product.pdf | | | runs/2026-01-01-product.json | 2026-01-01 |
```

**lessons.md**
```
| Rule | Area | Active | Source | Added |
|---|---|---|---|---|
| <imperative rule, under 100 chars> | format | true | kill reason | 2026-01-01 |
```

To read: parse the pipe table, skip the header and separator rows, filter as needed (e.g. `Active` = true and
`Area` in the module's set, or `Status` = killed). To write: append one new row to the bottom of the table
in the same format. Never touch the header or separator rows.

Multiline text (a long promise or a detailed revenue note) breaks a pipe table. When writing a cell: replace
every newline with `<br>` and every `|` with `\|`. When reading a cell back: reverse it. If the cell is
longer than about 500 characters, save it instead as a side file next to the tables and put that relative
path in the cell.

**One writer at a time.** Local mode has no locking. Do a fresh read of a file immediately before appending
to it, and do not run two commands that write the same Brain in parallel. If a read shows the file changed
since you planned the work (for example a new Active lesson appeared), apply the new state before writing.

The `runs/` folder is not a table: the build skill writes one run file per build there
(`<date>-<product-slug>.json` plus a readable `.md` twin). Modules read run files directly by path; the
Products row's Source cell points at the run file, and the eval gate takes the run JSON as its input.

## Mode 2: airtable

IDs are read from `config.brain.airtable` at run time (`baseId` and a `tables` map with the table IDs for
Products and Lessons). Never hardcode an ID; always read it from the tenant config.

`/product-studio:setup-brain` creates the buyer's OWN base via the Airtable MCP (`create_base` +
`create_table`), then writes the returned IDs back into the config. Never reference any existing base, and
never assume a base already exists.

Placeholders in examples always look like this (never a real ID):

```
baseId:  YOUR_BRAIN_BASE_ID
tables:
  products: YOUR_PRODUCTS_TABLE_ID
  lessons:  YOUR_LESSONS_TABLE_ID
```

Reading before producing (airtable mode):
1. `list_records` (or the equivalent MCP tool) on the Lessons table (`tables.lessons`), filtering `Active` =
   true and `Area` in the module's set plus `general`.
2. `list_records` on the Products table (`tables.products`), filtering `Status` = killed.
3. Apply every kept lesson as a hard constraint, and never rebuild what got killed.

Logging after producing (airtable mode):
1. Create one record in the matching table (`tables.products` or `tables.lessons`) using the columns above.
   Use `typecast: true` if a select value might not already exist as an option.

If the Airtable MCP is not connected, or a call fails, say so in the output, skip the read or write, and fall
back to treating the module's work as ungated by lessons (never block the deliverable).

## Single source of truth

This file is the only place the Brain contract lives. Every other skill, command, and agent references it by
path (`skills/brain/SKILL.md`) instead of restating the rules. If the contract changes, it changes here once.
