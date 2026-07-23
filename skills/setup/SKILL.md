---
name: setup
description: The install wizard for The Product Studio. Interviews the buyer on their niche, buyer, formats, pricing comfort and brand look, calibrates their voice, writes the tenant profile, and offers the Brain and the first build. Use whenever a buyer runs /product-studio:setup, says "set up the product studio", "get started", "install", or has no profile yet at ~/.claude/product-studio/profiles/<slug>.json.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# Product Studio setup wizard

This is the whole install story. A stranger with Claude Code and no context should finish this wizard with a
working profile, a calibrated voice profile, and (ideally) their first product build underway, in under an
hour.

Do this as a conversation, not a form dump. Ask a few questions at a time, confirm what you heard, move on.
Never invent an answer on the buyer's behalf. If they skip something, write a sensible placeholder and say so.

## Where the files go (non-negotiable)

The tenant root is always `~/.claude/product-studio/`, where `~` is the operating-system home directory of
the person running Claude (on Windows that is `%USERPROFILE%`). Resolve `~` to that absolute home path and
write there. Never write tenant files to the current working directory, a `./home` folder, the plugin folder
(`${CLAUDE_PLUGIN_ROOT}`), or any sandbox, even if the request looks like a test or a demo. If you cannot
resolve the home directory, stop and ask the buyer rather than guessing a location. Every other Product
Studio skill reads from this exact root, so a profile written anywhere else is invisible to them.

## Step 0 - check for an existing setup

Read `~/.claude/product-studio/config.json`. If it already has a `defaultProfile` and
`~/.claude/product-studio/profiles/<slug>.json` exists, tell the buyer they already have The Product Studio
set up for that profile, show the display name, and ask if they want to reconfigure it, add a second profile,
or stop. Do not overwrite an existing profile or config without a clear yes.

## a. Welcome

Open with one short paragraph, plain language, no jargon:

> The Product Studio is a product maker that takes your validated idea and builds the finished digital
> product, the cover, the sales page, and the checkout checklist that puts it on sale. Setup takes 15-20
> minutes and ends with your first build if you want it.

## b. The interview

Ask for (batch into a few natural questions, not ten separate prompts):

1. **Name or brand** (becomes `displayName`; slug = kebab-case of it, e.g. "Corner Bloom Coaching" becomes
   `corner-bloom-coaching`).
2. **Region and language**: sets `region` and `language` (British English for UK/Ireland, US English for the
   US, plain English otherwise; ask if genuinely unclear).
3. **The niche**: the space they serve, in one plain sentence, into `market.niche`.
4. **The specific buyer**: who actually buys from them. Push past "everyone". If they say "everyone",
   "anyone", or something equally broad, ask again: "Who actually pulls out a card? Picture the last person
   who paid you, or the person most likely to. Who are they?" The wizard REFUSES to write "everyone" into the
   profile; keep asking until there is a specific person on the page, into `market.buyer`.
5. **Pains they already hear**: 2-3 real problems their audience already tells them about, in the audience's
   own words, not marketing-speak, into `market.painsSeen` (one line each).
6. **What they can actually make**: which formats they could realistically produce, from: pdf-guide, ebook,
   template-pack, worksheet, checklist, prompt-pack, course, video-script, into `formats.canMake` (array).
   Say plainly which ship finished (the written and no-code ones) and which ship as complete scripts they
   record themselves (course, video-script). And "How many hours a week can you honestly give to making
   products?" into `formats.hoursPerWeek`.
7. **Pricing comfort**: "What is the lowest price you would feel right charging for something you made? And
   the highest?" Plus the currency, into `pricing.floor`, `pricing.ceiling`, `pricing.currency`. Every
   product price The Product Studio ever sets stays inside this band.
8. **Brand look**: three quick things, used on every cover and sales page:
   - Their **wordmark**: their name or brand exactly as it should appear on a cover, into `brand.wordmark`.
   - A **base colour** and an **accent colour**, as hex codes. If they have brand colours, take them. If
     they don't, offer a sensible default (a dark base with one bright accent reads well on covers and
     pages) and let them pick or tweak. Into `brand.colors.base` and `brand.colors.accent`.
   - `brand.bannedWords` and `brand.signaturePhrases` get filled by the voice calibration below.
9. **Storefront preference**: "Where do you plan to sell: Gumroad, Lemon Squeezy, or not decided yet?" into
   `storefront.platform` (`gumroad` / `lemonsqueezy` / `undecided`). Undecided is fine; the storefront skill
   asks again when it matters. Optionally get `storefront.deliveryEmail` if they know the email address their
   store sends from. Leave `brand.cta.url` blank: it gets filled when a real checkout link exists, never
   before.

Confirm the summary back in a few lines before moving on.

## c. Voice calibration

Explain in one line: "Now I'll learn how you actually sound, so nothing this system writes for your buyers
sounds like a robot."

**Ask for 2-3 real samples first.** Any of:
- A few real social posts or captions they've written
- A couple of real emails or messages to their audience
- A voice-note transcript (paste the text, or dictate and let them paste it)

If they provide samples, extract and write up:
- **Sentence length and rhythm**: short and punchy, or longer and conversational?
- **Energy**: calm and plain, upbeat, blunt, warm, formal?
- **Phrases they actually use**: real recurring words or turns of phrase, quoted directly from the samples.
- **Words they would never use**: jargon, corporate phrases, or tone that doesn't fit, either named by the
  buyer or obviously absent/avoided across the samples.

**If they have no samples**, run this 5-question quickfire instead, one at a time:
1. "How would you tell a mate what you do, in one breath?"
2. "What annoys you about how people sell things in your niche?"
3. "What's a phrase you say all the time when you're talking to your audience?"
4. "If a follower asked you a question right now, how would you actually reply, word for word?"
5. "What's one word or phrase you'd never want to sound like you're saying?"

Use their real answers as the sample text and mark the resulting profile **"draft, refine after first build"**
in the header.

### Write the voice profile

Write `~/.claude/product-studio/profiles/<slug>.voice.md` in this format:

```markdown
# Voice profile - <Name>

Status: <calibrated from real samples | draft, refine after first build>
Written: <date>

## How you sound
- Sentence length: <short and direct | longer, conversational | mixed>
- Energy: <e.g. calm and plain, upbeat, blunt and confident, warm>
- Formality: <casual | plain professional | formal>

## Phrases to use
- "<real phrase 1>"
- "<real phrase 2>"
- "<real phrase 3>"

## Words you would never use
- <banned word/phrase 1>
- <banned word/phrase 2>

## Example before / after
**Generic AI version:** "<a bland, jargon-y sentence about what they do>"
**In your voice:** "<the same idea, rewritten in the calibrated voice>"

## Notes
<any other calibration notes, e.g. always leads with a number, never uses emoji, always ends on the CTA>
```

Every piece of public copy this system produces (the product itself, the sales page) gets checked against
this file via `skills/voice`. This format is the ONE canonical voice profile shape; `skills/voice` writes the
same format when it calibrates a voice outside setup.

**Mirror the voice into the profile config.** From the calibration, also fill these config fields so the
config and the profile never drift apart:
- `brand.bannedWords`: the "Words you would never use" list (replace the template's placeholder examples).
- `brand.signaturePhrases`: the "Phrases to use" list.

## d. Write the eval briefs

Invent two fixed short product briefs WITH the buyer, from their own niche. Each brief is 2-4 lines: a
product concept, the buyer it serves, the pain, the promise, a price inside their band, and a format from
`formats.canMake`. These go into `eval.evalBriefs` in the profile and become the regression baseline:
`/product-studio:eval` can rebuild them any time to check nothing has drifted. Pick briefs that are
representative of what this buyer would actually make, agree them out loud, and write them down exactly.
They should not change casually afterwards.

## e. Write the tenant files

1. Copy `${CLAUDE_PLUGIN_ROOT}/skills/setup/templates/profile.template.json` to
   `~/.claude/product-studio/profiles/<slug>.json` and fill in every field gathered above. Leave the `brain`
   block at its template defaults (placeholders only; real values are written by
   `/product-studio:setup-brain`, never here). Set `voice.profilePath` to `<slug>.voice.md`, leave
   `formats.preferred` empty (it gets learned), and set `lastUpdated` to today.
2. Create or update `~/.claude/product-studio/config.json`:
   ```json
   { "defaultProfile": "<slug>" }
   ```
   If this is a second profile for the same buyer, keep the existing `defaultProfile` unless they ask to
   switch it, and just make sure the new `profiles/<slug>.json` exists.

Confirm both files were written and tell the buyer exactly where they live.

## f. Offer the Brain

Tell the buyer, in one line: "The Product Studio keeps a memory: every product you build, every kill, and
everything that sold binds the next build, so it learns your format and never repeats a dud. Run
`/product-studio:setup-brain` now and I'll set it up, local by default (no accounts needed), or your own
Airtable base if you already use one." If they say yes, hand off to that command's flow (or tell them to run
it now). If they say later, note that every build still works without the Brain, it just won't remember
anything between builds yet.

## g. Offer the first build

Say: "Want to see this working right now? Run `/product-studio:build` and I'll make your first product. If
you have The Validator installed, I can read your validated ideas from it and build straight from one;
otherwise give me a short brief and that works just as well." If yes, hand off to that command.

## Close

End with a short, plain summary:

```
You're set up. Here's what runs day to day:

/product-studio:build         - one run: takes an idea, ships the finished product
/product-studio:storefront    - the sales page and the checkout checklist, ready to go live
/product-studio:shelf         - one screen: what's built, what's listed, what sold, what got killed
/product-studio:kill-product  - kill a product and make sure the mistake never repeats
/product-studio:lesson        - teach it a format, offer, or copy rule it must never forget

Everything lives here:
- Your profile:   ~/.claude/product-studio/profiles/<slug>.json
- Your voice:     ~/.claude/product-studio/profiles/<slug>.voice.md
- Its memory:     ~/.claude/product-studio/brain/<slug>/ (or your Airtable base)
- Your products:  ~/.claude/product-studio/products/<slug>/

Run /product-studio:build any time you have an idea ready to become a product.
```
