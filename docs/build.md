# How a build works

`/product-studio:build` is the one job: one run takes an idea and ends with a finished product on disk.
Here's what happens at each step, what each format actually ships, and how to read what comes back.

## What you give it

A validated idea, a short brief, or nothing at all. If The Validator is installed, the build reads its
validated ideas automatically and offers to build straight from one. Otherwise (or if you decline) it asks
a short intake: the product concept, the buyer, the pain, the promise, and a price. Flags:

- `--profile <slug>` - build against a different profile if you have more than one.

## Step by step

1. **Memory first.** Before writing anything, the build loads your active lessons and every killed product
   from the Brain. Lessons are hard constraints: your proven structure gets reused, what converted gets
   respected, and a killed product never gets rebuilt in a new hat.
2. **The idea.** From The Validator's row (with its evidence-backed promise and price), or from your brief.
   Same shape either way.
3. **The format.** It recommends one from the formats you said you can make, plus what the memory says has
   worked for you, then confirms with you. It states plainly what will ship finished and what you'll still
   record.
4. **The product.** The full content, written in your voice, with real substance in every section. Then it
   renders (see the PDF path below) and generates the cover and mockup.
5. **The gate.** A deterministic quality check runs before anything reaches you (word counts, item counts,
   the promise delivered in the text, the price in your band, no placeholders). Fails get fixed and
   re-checked, up to three times, never quietly shipped.
6. **The record.** One row lands in your Products table and one run record lands in `runs/`, so the shelf
   and every future build can see it.

## The 8 formats: what ships finished, what you record

| Format | What ships | Finished, or you record? |
|---|---|---|
| PDF guide | Full written guide, print-ready file, PDF, cover, mockup | Finished |
| Ebook | Same as the guide, longer form | Finished |
| Template pack | 4+ genuinely usable template files plus import instructions | Finished |
| Worksheet | Prompts and write-in space, print-ready, PDF | Finished |
| Checklist | 15+ real actions with enough detail to do each one, PDF | Finished |
| Prompt pack | 15+ prompts, each with when-to-use and its variables explained | Finished |
| Course | Full outline, every lesson fully scripted, slide content | You record the lessons |
| Video script | Full outline plus complete scripts | You record the video |

For course and video formats, every part you need to record is marked with a plain RECORD marker in the
scripts. The output never claims a finished course; it says exactly which parts are done and which are
yours.

## Fill-ins: the one honest bracket

Some things only you can supply: a personal story, a real screenshot, a real client result. The build never
fakes these. Instead it marks the exact spot with `[FILL-IN: what goes here and why]` and lists every
fill-in at the end of the run, so you can complete them in one pass.

Why it exists: the alternative is a product with invented stories and fake specifics, which is worse than a
marked gap. The quality gate enforces this from both sides: any other kind of placeholder fails the build,
and more than 10 fill-ins fails it too, because at that point it's a scaffold wearing a product's clothes.

To complete them: open the product file, search for `[FILL-IN:`, replace each with the real thing, and
delete the marker. A product with open fill-ins is recorded as `drafting`, not `built`, when they would
block a sale.

## The PDF path

The source of truth for every rendered format is a print-ready file that opens in any browser, always. From
there:

- **Automatic (the normal case):** the build finds a browser already on your machine (Chrome, Edge,
  Chromium, or Brave; Edge ships with Windows) and prints the PDF, the cover image, and the mockup image
  for you. No accounts, no uploads, nothing to install.
- **Manual (the honest fallback):** if no browser is found, the build says so plainly and gives you the
  one-keystroke path: open the file in any browser, print, save as PDF. The output never claims a finished
  PDF unless the file actually exists.

Template packs skip rendering entirely: they ship as ready-to-use files plus import instructions. Course
formats ship scripts plus a slides file, with the same print path if you want the slides as a PDF.

## The run record

Every build writes two files to `~/.claude/product-studio/brain/<slug>/runs/`:

- `<date>-<product-slug>.json` - the structured record: the idea, the buyer, the promise, the price, the
  format, the file paths, and every fill-in. This is what the quality gate checks and what
  `/product-studio:eval` reads.
- `<date>-<product-slug>.md` - the same content laid out for you to read.

## What you do next

Complete the fill-ins if any, record the lessons if it's a course, then run `/product-studio:storefront` to
put it on sale. See `docs/storefront.md`.
