---
name: build
description: The Product Studio's core job. Takes a validated idea (from The Validator if present, or a short brief) and turns it into a finished digital product on disk, with a cover, a mockup, and a gated build record. Use for "build my product", "turn this idea into a product", "make the ebook", "make the guide", "make the course", or /product-studio:build.
argument-hint: "[--profile <slug>] [--from-validator] [a short brief or nothing]"
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion
---

# Build: the one job

One run = one finished digital product on disk, honestly labelled: what ships finished, what the buyer
still supplies or records, where every file lives, and a build record the eval gate has passed. Never
ship a scaffold dressed up as a product.

## Step 0: resolve the tenant and load the memory

1. Parse `--profile <slug>` from the arguments. If absent, read `defaultProfile` from
   `~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If
   missing, tell the buyer to run `/product-studio:setup` and stop. `~` is always the OS home directory
   (`%USERPROFILE%` on Windows). Never write tenant files to the current directory, a `./home` folder,
   the plugin folder, or any sandbox, even for a test or a demo.
2. Load the voice profile at the path in `voice.profilePath` (relative paths resolve against
   `~/.claude/product-studio/`).
3. Read the Brain contract at `${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md` and load, per that contract:
   - All ACTIVE Lessons (areas `format`, `offer`, `copy`, `general`). Every one is a hard constraint:
     reuse this buyer's proven structure, respect what converted, never rebuild what got killed.
   - All Products rows with Status `killed`. Never rebuild a killed product or a thin variation of it
     without the buyer explicitly overriding, and cite the kill reason when it comes up.
4. If an ACTIVE lesson starting `REGRESSION:` exists, stop and tell the buyer to run
   `/product-studio:eval` first. A gate that failed last time must be cleared, not ignored.
5. If the Brain is unreachable, say so, continue without memory, and skip the write steps at the end.

## Step 1: get the idea

If `validator.autoRead` is true in the profile, look for a Validator tenant on this machine:

- Glob `~/.claude/validator/brain/*/ideas.md`. Parse the pipe-table rows and keep the ones with Verdict
  `validated` or `testing`.
- Also read `~/.claude/validator/brain/*/runs/*.json` when present; those carry the richer fields
  (promise, price band, pain, evidence).
- List what was found (idea, promise, price band, verdict) and offer to build one.

If nothing was found, or the buyer declines the list, run the short intake instead. Capture the same
shape either way:

- The product concept (one line, what it is).
- The specific buyer (never "everyone").
- The pain, in the buyer's words.
- The one-line outcome promise (an outcome, not a topic).
- The price or price band. It must sit inside the profile's `pricing.floor` to `pricing.ceiling`
  comfort band; if it falls outside, say so plainly and resolve it with the buyer (adjust the price or
  the band) before continuing.
- Any format preference.

State plainly which path was used: "idea from your Validator" or "idea from your brief". The Validator
is never required; a brief is a first-class input.

## Step 2: confirm the format

Recommend ONE format from `formats.canMake`, based on the idea's shape plus any ACTIVE `format`-area
lessons (the learned default beats a cold guess: if a lesson says this buyer's checklists sell,
recommend the checklist). Confirm the choice with the buyer before producing anything.

State plainly what will ship finished versus what the buyer still records: written and no-code formats
ship completely finished; course and video formats ship as complete outlines, full word-for-word
scripts, and slide content, and the buyer records the footage.

## Step 3: produce the product

Write the real, complete content, in the buyer's voice: load the writing system at
`${CLAUDE_PLUGIN_ROOT}/skills/voice/SKILL.md` and the buyer's voice profile, and pass all copy through
it. Never lorem, never a summary standing in for content, never a scaffold with headings and thin
paragraphs. The substance bar per format (the eval gate enforces these minimums):

| Format | What ships | Substance minimum (eval) |
|---|---|---|
| pdf-guide / ebook | product.md + A4 HTML + PDF + cover + mockup | >= 2,000 words, >= 4 sections, actionable steps not summary |
| template-pack | 4+ template files + IMPORT.md + cover | >= 4 templates, each genuinely usable as-is |
| worksheet | A4 HTML/PDF with prompts + write-in space | >= 8 prompts/exercises with real instruction text |
| checklist | A4 HTML/PDF | >= 15 items, each an action with enough detail to do it |
| prompt-pack | product.md + A4 HTML/PDF | >= 15 prompts, each with when-to-use and variables explained |
| course | outline + per-lesson full scripts + slides.html | every lesson scripted >= 300 words; RECORD markers present |
| video-script | outline + full scripts | every script >= 300 words; RECORD markers present |

**The fill-in convention.** Anything only the buyer can supply (a personal story, a real screenshot, a
real case number, their own login) is written exactly as `[FILL-IN: what goes here and why]`, listed
again at the end of the product under a "Your fill-ins" heading, and never faked. Maximum 10 fill-ins;
more than that means the product is a scaffold, so write more real content instead.

**Course and video formats.** Every lesson gets a complete word-for-word script (what the buyer says on
camera, in full), plus one line starting `RECORD:` naming exactly what the buyer films or records for
that lesson, plus slide content. Slides go in `course/slides.html` using the A4 template's landscape
variant (the template's comment explains the swap) or a simple slide-per-page layout.

## Step 4: files on disk

Everything goes under `~/.claude/product-studio/products/<slug>/<product-slug>/`:

```
~/.claude/product-studio/products/<slug>/<product-slug>/
  product.md            the full content, always (the canonical source)
  product.html          print-ready A4 HTML (rendered formats)
  product.pdf           when a browser was found (Step 5)
  cover.html / cover.png
  mockup.html / mockup.png
  templates/            (template-pack: the individual template files + IMPORT.md)
  course/               (course: 00-outline.md, NN-<lesson>.md per lesson, slides.html)
```

- **Always** write `product.md` with the complete content.
- **Rendered formats** (pdf-guide, ebook, worksheet, checklist, prompt-pack): also write
  `product.html`, built FROM `${CLAUDE_PLUGIN_ROOT}/skills/build/templates/product-a4.html`: copy the
  template, fill the `@brand-tokens` block from the profile's `brand.colors` and `brand.wordmark`, then
  fill the content into the page blocks (one `.page` per sheet, split long sections across pages).
- **Template packs**: write each template as `templates/<name>.md` (or `.csv` where a spreadsheet fits
  better), plus `templates/IMPORT.md` with per-tool import steps (Notion, Google Docs or Sheets, and
  plain files).
- **Courses**: write `course/00-outline.md`, one `course/NN-<lesson-slug>.md` per lesson, and
  `course/slides.html`.

## Step 5: render portably

1. **PDF**: run `python "${CLAUDE_PLUGIN_ROOT}/skills/build/scripts/render_pdf.py" pdf <product.html> <product.pdf>`.
   If `python` is not on PATH, try `py` (Windows) or `python3`.
2. **Cover**: copy `${CLAUDE_PLUGIN_ROOT}/skills/build/templates/cover.html` into the product folder,
   fill the token block plus the title, subtitle (the promise), and wordmark slots, then run
   `render_pdf.py shot <cover.html> <cover.png> --size 1200x1600`.
3. **Mockup**: copy `${CLAUDE_PLUGIN_ROOT}/skills/build/templates/mockup.html`, fill the tokens and
   paste the filled cover content into both marked slots, then run
   `render_pdf.py shot <mockup.html> <mockup.png> --size 1600x1200`.

If the script reports no browser found (exit code 2): keep the HTML files (they are real deliverables
on their own), tell the buyer exactly how to save the PDF themselves (open the HTML in any browser,
print, choose Save as PDF), and NEVER claim a PDF or PNG exists unless the file is actually on disk.

## Step 6: write the run, then gate it

1. Write the structured run JSON to
   `~/.claude/product-studio/brain/<slug>/runs/<YYYY-MM-DD>-<product-slug>.json`, with absolute file
   paths, in this exact shape:

```json
{
  "date": "<YYYY-MM-DD>",
  "product": "<one line, what it is>",
  "format": "pdf-guide | ebook | template-pack | worksheet | checklist | prompt-pack | course | video-script",
  "ideaSource": "validator:<path to the Validator run or ideas row>  OR  brief",
  "buyer": "<the specific buyer>",
  "pain": "<the pain, in the buyer's words>",
  "promise": "<the one-line outcome promise>",
  "promiseDelivery": ["<section heading that delivers the promise>", "..."],
  "price": "<currency><n>  or  <currency><n>-<currency><n>",
  "files": {
    "productMd": "<absolute path>",
    "productHtml": "<absolute path or null>",
    "productPdf": "<absolute path, or null if not produced>",
    "cover": "<absolute path to cover.html>",
    "coverPng": "<absolute path, or null if not produced>",
    "mockupPng": "<absolute path, or null if not produced>",
    "salesPage": null,
    "extras": []
  },
  "fillIns": ["exact fill-in text without the brackets", "..."],
  "recordCount": 0,
  "lessonCount": 0,
  "finishedParts": ["<what ships finished>", "..."],
  "buyerParts": ["<what the buyer supplies or records>", "..."],
  "status": "built | drafting"
}
```

   `recordCount` is the number of `RECORD:` lines and `lessonCount` the number of lessons (course and
   video formats only; both 0 otherwise). `salesPage` stays null until `/product-studio:storefront`
   runs.

2. Run the gate:
   `python "${CLAUDE_PLUGIN_ROOT}/skills/build/scripts/eval_product.py" <run.json> <profile.json>`
   (try `py` or `python3` if `python` is missing) and parse the `@@EVAL_JSON@@` line. If any check
   fails, fix the product or the run record and re-run the gate, up to 3 attempts. If it still fails:
   present the work WITH the failure named plainly, write the Products row with Status `drafting`, and
   write a `REGRESSION:` Active lesson per the Brain contract. Never silently ship a failed gate.
3. Write the readable twin `runs/<date>-<product-slug>.md` (the same record laid out for a human).
4. Per the Brain contract, append one Products row: Status `built`, or `drafting` if the gate failed or
   fill-ins remain that block a sale (a buyer could not honestly charge for it as-is).

## Step 7: report

End the session output with, in order:

1. What shipped finished (the format and the finished parts).
2. What needs the buyer: the fill-ins list, and for course or video formats the `RECORD:` list.
3. The exact file paths (product, PDF or the save-it-yourself note, cover, mockup, run record).
4. The one next action: run `/product-studio:storefront` to put it on sale.

Short, scannable, honest about anything that did not render.

## Do not

- Do not invent stats, testimonials, or case studies, anywhere in the product.
- Do not leave unmarked placeholders; the only allowed placeholder is `[FILL-IN: ...]`.
- Do not use lorem ipsum or filler copy of any kind.
- Do not claim a file exists (PDF, PNG, anything) unless it is actually on disk.
- Do not write any literal platform ID or personal value; everything comes from the profile config.
- Do not let a Brain failure block the deliverable; say it, skip the write, carry on.
- Do not fake a buyer fill-in; if only the buyer can supply it, mark it and move on.
