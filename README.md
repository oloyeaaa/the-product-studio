# The Product Studio

A product maker on your payroll, installed inside Claude Code. Give it a validated idea and it builds the
finished digital product, the cover, the sales page, and the checkout checklist that puts it on sale. It
remembers your format, your structure, and what actually sold, so the next product takes minutes, not weeks.

Works with Claude Code.

## Install

Clone the repo and point Claude Code at the plugin folder:

```
git clone https://github.com/oloyeaaa/the-product-studio
claude --plugin-dir the-product-studio
```

Then run `/product-studio:setup` to get started. To check the plugin is well-formed first, run
`claude plugin validate the-product-studio`. Once it's published to a marketplace, you'll be able to install
it from there instead. Full detail, prerequisites, and troubleshooting in `docs/SETUP.md`.

## What it does

- **Builds the product for real.** Not an outline, not a scaffold: the full content, written in your voice,
  with real substance in every section. Anything only you can supply (a personal story, a real screenshot)
  is marked plainly as a fill-in, never faked.
- **Renders a PDF you can sell.** Written formats ship as a print-ready file plus the finished PDF when a
  browser exists on your machine, and a one-keystroke manual path when one doesn't. A typographic cover and
  a mockup image come with it.
- **Stands up the storefront.** A self-contained sales page with a committed design direction, a
  step-by-step checkout checklist for Gumroad or Lemon Squeezy, and a delivery note. You paste one link and
  you're live.
- **Is honest about courses and video.** Those formats ship as complete outlines, full lesson scripts, and
  slide content. You record; it never pretends to have recorded for you, and every output says which parts
  ship finished and which parts you still record.
- **Learns your format and what sold.** A killed product becomes a lesson that binds every future build,
  and when something sells, that learning is written the same way. The tenth product is sharper than the
  first because the memory compounds.
- **Refuses to ship scaffold.** A deterministic quality gate checks every build before it reaches you:
  real word counts, real item counts, the promise delivered in the text, the price inside your comfort
  band, one clean CTA. Thin work gets blocked, not shipped.

## Module map

| Module | What it gives you | Command |
|---|---|---|
| Setup | The install wizard: the interview, voice calibration, your profile | `/product-studio:setup` |
| Build | One run: takes an idea, ships the finished product | `/product-studio:build` |
| Storefront | The sales page, the checkout checklist, the delivery note | `/product-studio:storefront` |
| Shelf | One screen: what's built, listed, selling, or killed | `/product-studio:shelf` |
| Kill product | Kill a product and keep the lesson | `/product-studio:kill-product` |
| Lesson | Teach it a format, offer, or copy rule directly | `/product-studio:lesson` |
| Eval | Regression check: is the quality gate still being cleared | `/product-studio:eval` |
| Brain setup | Set up the memory (local files or your own Airtable base) | `/product-studio:setup-brain` |

The Brain (the memory contract) and the voice pass (the writing system) also ship inside the plugin, but
they work behind the scenes: every build reads and writes the memory, and every piece of buyer-facing copy
goes through the voice pass. They're part of the same one employee, not extra commands to learn.

## One-hour quickstart

1. **Install.** See `docs/SETUP.md` for the exact install path (marketplace once published, or a local
   install with `claude --plugin-dir <folder>`).
2. **Run `/product-studio:setup`.** About 15-20 minutes. It interviews you on your niche, your specific
   buyer, the formats you can make, your pricing comfort, and your brand look, then calibrates your voice
   from a few real samples.
3. **Run `/product-studio:build`.** Give it a validated idea (it reads The Validator's automatically if
   you have it installed) or a short brief. It ends with the finished product on disk, plus the cover.
4. **Run `/product-studio:storefront`.** It builds the sales page and hands you the checkout checklist.
   Work through the checklist, paste the checkout link into the page, and you're selling.

## Works with The Validator

If The Validator (the product researcher from the same line) is installed on your machine, The Product
Studio reads its validated ideas automatically at build time and offers to build straight from one, with
the evidence-backed promise and price carried over. The Validator is never required: a short brief gives a
build everything it needs. Full detail in `docs/works-with-the-validator.md`.

## What it refuses

- **Recording your video.** Course and video formats ship as complete scripts and slides; the recording is
  yours, and the output says so plainly.
- **Inventing testimonials, results, or numbers.** If proof doesn't exist, the sales page uses the real
  contents as proof and says nothing false.
- **Shipping placeholders as finished work.** The quality gate blocks scaffold output; the only bracket a
  product may contain is a clearly marked fill-in for something only you can supply.

## Where everything lives

Your settings, voice profile, memory, and products all live outside the plugin, under
`~/.claude/product-studio/`, so they're yours and they survive plugin updates:

- `~/.claude/product-studio/config.json` - which profile is the default
- `~/.claude/product-studio/profiles/<slug>.json` - your profile (market, formats, pricing, brand)
- `~/.claude/product-studio/profiles/<slug>.voice.md` - your calibrated voice
- `~/.claude/product-studio/brain/<slug>/` - the memory: `products.md`, `lessons.md`, and `runs/`
- `~/.claude/product-studio/products/<slug>/` - the finished products themselves

Full detail in `docs/SETUP.md`.

## Licence

See `docs/LICENSE.md`.
