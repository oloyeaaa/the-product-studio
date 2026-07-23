# Setup

How to install The Product Studio, what the setup wizard asks and why, how the memory works, and how to get
from zero to a finished product inside an hour.

## Install

**From a marketplace (once published):** follow the marketplace's own install instructions for the
`product-studio` plugin.

**Local or zip install (available now):**

1. Get the plugin folder onto your machine (unzip it if it came as a zip).
2. Run:
   ```
   claude --plugin-dir <path-to-the-plugin-folder>
   ```
3. Claude Code loads the plugin for that session. Run `/product-studio:setup` to get started.

To check the plugin is well-formed before installing it anywhere, you can run
`claude plugin validate <path-to-the-plugin-folder>`.

## Prerequisites

- **Claude Code**, installed and working, with your own subscription. Everything runs inside it.
- **Python 3.10+**, for two small scripts with no extra packages: the quality gate that checks every build,
  and the PDF renderer. Everything else runs with nothing extra installed.
- **A browser** (Chrome, Edge, Chromium, or Brave; Edge ships with Windows). Used only to turn the finished
  product into a PDF and the cover into an image, automatically. If none is found, you still get everything
  as files that open in any browser, plus one-keystroke instructions to save the PDF yourself.
- **Nothing else is required.** Airtable (for the memory) is optional; local files are the default. The
  Validator (the researcher from the same line) is optional; a short brief works without it.

## The setup wizard, step by step

Run `/product-studio:setup`. It takes about 15-20 minutes and walks through:

1. **A short welcome** explaining what The Product Studio does: it takes your validated idea and builds the
   finished product plus everything needed to put it on sale.
2. **The interview**: your name or brand, your region, your niche in one plain sentence, and your specific
   buyer. It pushes past "everyone": a product for everyone is a product for no one, so it keeps asking
   until there's a real person on the page. It also asks for the pains your audience already tells you
   about, which formats you can realistically make (and it says plainly which ship finished and which ship
   as scripts you record), how many hours a week you can give, your pricing comfort (the lowest and highest
   price you'd feel right charging; every price it ever sets stays inside that band), your brand look (your
   wordmark and two colours, used on every cover and sales page), and where you plan to sell (Gumroad,
   Lemon Squeezy, or not decided yet).
3. **Voice calibration**: it asks for 2-3 real samples of how you write or talk and learns your sentence
   length, energy, and the phrases you actually use. No samples handy? A quick 5-question interview stands
   in, marked as a draft to refine after your first build. Everything the system writes for your buyers,
   the product itself and the sales page, gets checked against this.
4. **Your files are written**: your profile and voice profile are saved outside the plugin, under
   `~/.claude/product-studio/`, so they're yours and survive plugin updates.
5. **The Brain choice**: it offers to set up the memory. Local files by default, no accounts needed, or
   your own Airtable base if you already live there. Every build still works without the Brain; it just
   won't remember anything between builds yet. You can switch modes later with
   `/product-studio:setup-brain`. Full detail in `docs/brain.md`.
6. **The first build**: it offers to run `/product-studio:build` right there, from a validated idea or a
   short brief, so you see it working before you close the session.

Why it asks all this: every build reads from what you tell it here. Your buyer shapes the content, your
formats bound what it offers to make, your pricing comfort bounds every price, your brand look styles every
cover and page, and your voice shapes every line of copy. Nothing is hardcoded to any one person.

## The first hour

A realistic path from a cold install to a product you could sell today:

1. Install and run `/product-studio:setup` (about 20 minutes including voice calibration).
2. Run `/product-studio:build` with a validated idea or a short brief (what it is, who it's for, the pain,
   the promise, a price). The build writes the full content, renders the PDF and cover, and passes the
   quality gate before you see it.
3. Read the product. Complete any fill-ins it marked (things only you can supply).
4. Run `/product-studio:storefront`. It builds the sales page and hands you the checkout checklist.
5. Work through the checklist on Gumroad or Lemon Squeezy, paste the checkout link into the sales page, and
   make the test purchase.

## Where every file lives

Everything you generate lives outside the plugin, under `~/.claude/product-studio/`:

- `config.json` - which profile is the default
- `profiles/<slug>.json` - your profile (market, buyer, formats, pricing, brand, storefront preference)
- `profiles/<slug>.voice.md` - your calibrated voice
- `brain/<slug>/products.md` and `brain/<slug>/lessons.md` - the memory tables (local mode)
- `brain/<slug>/runs/` - one record per build (what the quality gate checks)
- `products/<slug>/<product-slug>/` - the product itself: the content, the PDF, the cover, the mockup, the
  sales page, the checkout checklist, and the delivery note

## Troubleshooting

- **A command says "run /product-studio:setup first".** Your profile is missing or the default doesn't
  match. Run `/product-studio:setup`, or check `~/.claude/product-studio/config.json` names a profile that
  exists under `~/.claude/product-studio/profiles/`.
- **The build says no PDF was produced.** No browser was found on the machine. You still have the full
  product as a file that opens in any browser; open it, print, and save as PDF (one keystroke). Install any
  Chromium-based browser to make it automatic next time.
- **The gate keeps failing a build.** The quality gate found a real problem: thin sections, a promise the
  text doesn't deliver, a price outside your comfort band, or leftover placeholders. The build fixes and
  retries up to three times; if it still fails, it presents the work with the failure named instead of
  shipping it quietly.
- **The Airtable step fell back to local.** The Airtable connection wasn't active when
  `/product-studio:setup-brain` ran, so it set up local files instead so you weren't stuck. Connect
  Airtable in Claude Code and run it again to switch.
- **Python not found.** The quality gate and the automatic PDF are affected; the interview, the writing,
  and the copy all still run. Install Python 3.10+ (Windows: `winget install Python.Python.3.12`; macOS:
  `brew install python`).
