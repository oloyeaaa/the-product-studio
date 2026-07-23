---
name: setup-brain
description: Create or adopt the Brain for The Product Studio - local markdown files by default, or the buyer's own Airtable base. Use when the buyer runs /product-studio:setup-brain, asks to set up the Product Studio's memory, or wants to switch the Brain between local and Airtable.
argument-hint: "[--profile <slug>] [local|airtable]"
allowed-tools: Read, Write, Edit, Bash, ToolSearch, AskUserQuestion
---

# Setup brain

Set up the Brain for one profile: the memory that every module in The Product Studio reads and writes. Full
contract: `${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md`.

## Step 0 - tenant resolution

Parse `--profile <slug>` from arguments. If absent, read `defaultProfile` from
`~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If that file
is missing, tell the user to run `/product-studio:setup` first and stop. Never type a literal ID or personal
value; everything comes from this config.

Naming note for every step below: "the config" means the PROFILE file
`~/.claude/product-studio/profiles/<slug>.json` (its `brain` block and `lastUpdated` field). The separate
`~/.claude/product-studio/config.json` holds only `defaultProfile` and is never written by this skill.

## Step 1 - create or adopt

The Brain EXISTS only if the local brain folder for this slug has files in it, or
`config.brain.airtable.baseId` is non-empty. (`config.brain.mode` alone does not count: the fresh profile
template ships with `mode: "local"` already set.) If the Brain exists, tell the user what is already
configured and ask if they want to reinitialise or leave it alone. Do not overwrite existing data without
confirmation.

Otherwise, if the mode was not passed as an argument, ask the buyer one question: **local or Airtable?**

- Local: zero setup, works immediately, good default for most buyers.
- Airtable: their own base, useful if they already live in Airtable or want to view the Brain outside Claude
  Code. Requires the Airtable MCP to be connected.

## Step 2a - local mode

1. Create `~/.claude/product-studio/brain/<slug>/` if it does not exist, plus an empty `runs/` subfolder
   (the build skill writes its run files there).
2. Copy the two templates from `${CLAUDE_PLUGIN_ROOT}/skills/brain/templates/` into that folder:
   `products.md` and `lessons.md`.
3. Set `config.brain.mode = "local"` and `config.brain.localPath = "brain"`.

## Step 2b - airtable mode

1. Check that an Airtable MCP is connected (a tool like `create_base` is available; if the tools are
   deferred, load them via ToolSearch first). If it is not connected, tell the buyer plainly that Airtable
   is not connected, and fall back to Step 2a (local mode) instead.
2. Create a new base named `<displayName> Product Studio Brain` using `create_base`. Never reference or
   reuse any existing base.
3. Create the two tables with `create_table`, matching the schema in
   `${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md`:

   - **Products**: Product (single line text, primary), Idea source (single line text), Buyer (single line
     text), Format (single select: pdf-guide, ebook, template-pack, worksheet, checklist, prompt-pack,
     course, video-script), Promise (long text), Price (single line text), Status (single select: drafting,
     built, listed, selling, killed), Asset path (single line text), Sales-page path (single line text),
     Revenue (single line text), Source (single line text), Added (date).
   - **Lessons**: Rule (long text, primary), Area (single select: format, offer, copy, general), Active
     (checkbox), Source (single line text), Added (date).

4. Write the returned base ID and each table ID into `config.brain.airtable`:
   ```
   "brain": {
     "mode": "airtable",
     "localPath": "brain",
     "airtable": {
       "baseId": "<returned base id>",
       "tables": {
         "products": "<returned table id>",
         "lessons": "<returned table id>"
       }
     }
   }
   ```
   In documentation and examples elsewhere, these placeholders are always written as `YOUR_BRAIN_BASE_ID`,
   `YOUR_PRODUCTS_TABLE_ID`, `YOUR_LESSONS_TABLE_ID`. Only the real IDs returned by the MCP for this buyer's
   own base get written into their local config file.
5. Set `config.brain.mode = "airtable"`.

## Step 3 - finish

Update `config.lastUpdated` to the current date and save the tenant config.

Report back to the user in chat:
- Which mode was set up (local or airtable).
- Where the memory lives (the folder path or the base name).
- The loop contract in one line: every build reads Active lessons and killed products first, then logs one
  Products row after, so The Product Studio gets sharper with every build.
