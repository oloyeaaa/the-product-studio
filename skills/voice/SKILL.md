---
name: voice
description: Write or edit ANY public-facing copy (a guide's intro, a sales-page hero, product sections, covers, checkout descriptions) so it sounds like the buyer, hits one emotion, opens with a real hook, rides a framework, tells a story, and passes a human check. Use whenever writing or polishing anything public in the buyer's voice. This is the writing pass every product and sales page in The Product Studio runs through.
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# Voice: the writing system

One system for writing anything public in the buyer's own voice. Every piece must do six things:
**sound like the buyer · reach for ONE emotion · earn the first 3 seconds · ride a framework · tell a
story · pass the human check.** Skip none.

## Step 0: resolve the tenant

Parse `--profile <slug>` from the arguments. If absent, read `defaultProfile` from
`~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If that file
is missing, tell the user to run `/product-studio:setup` and stop.

## Step 0.5: load the voice

Read `~/.claude/product-studio/profiles/<slug>.voice.md` (the path is `config.voice.profilePath`, resolved
under the same profiles folder). Also read `config.brand` for `bannedWords`, `signaturePhrases`, and `cta`.

- **If the voice profile file exists:** load it and use it as the calibrated voice for every piece below.
- **If it does not exist:** run the calibration interview (below), write the profile file, then continue.

## Step 1: lock the target before a single word

Write one line first:
**Audience → the ONE emotion I want them to feel → the ONE action I want.**
If you can't name the emotion and the action, don't write yet. One piece = one emotion = one CTA.

---

## The Fix: the content formula (lead with this)

The strongest copy follows one shape: **pick a problem your reader has, find a solution, present it.**
- **Be a solution provider, not a seller.** Teach or solve something the reader can act on immediately.
  Value first, always. A product page earns the sale by proving the product solves the problem.
- **Guide, not hero.** The reader solves their own problem with what you hand them.
- **Sometimes wrapped in a story**, but the spine is always problem then solution then present.
- **Close, per piece:** a product section ends on the next step inside the product; a sales page ends on
  its one buy CTA. Never a hard-sell pile-on.

---

## 2. Voice: sound like the buyer (non-negotiable)

- **Kill the jargon.** Never say AI/automation/MCP/agent/LLM/workflow/pipeline/API/model. Say what it *does*:
  "prices your next booking", "plans your week", "writes itself in an afternoon", "saves you hours".
- **First-person "I"/"we"** for proof; **"you/your"** for the reader. Match `config.language`. Confident,
  never hype.
- **The number is the hero** (a real time or money figure). Call it out, don't bury it.
- **Sign-off:** end on the CTA. No catchphrase sign-off unless the voice profile explicitly defines one.
- **Banned words:** never use anything in `config.brand.bannedWords`.
- **Signature phrases:** favour anything in `config.brand.signaturePhrases` where it fits naturally; never
  force one in.
- **Emoji:** essentially none in public copy unless the voice profile says otherwise.
- **One CTA per piece.** On a sales page that means ONE buy action, repeated if the layout needs it but
  always pointing at the same place (`config.brand.cta.url` once a checkout link exists).

## 3. Emotion: reach for the right one

Decide the feeling, then engineer it. Neutral writing is the enemy. A reliable spine is **loss → relief**:
name what the reader is quietly losing, then the calm on the other side.

| Want them to feel | Reach for it by | Example |
|---|---|---|
| **The cost of inaction** (lead) | name a specific, concrete loss | "You quoted low again. That booking cost you 300 quid before you picked up the camera." |
| **Relief / control** | show the calm after | "One afternoon with this guide and your price list is done." |
| **Pride / being seen** | respect their craft | "You're brilliant at the work. That's exactly why the pricing slips." |
| **Belonging / 'that's me'** | mirror their exact day | "Rewriting the same quote email for the tenth time this month." |
| **Hope (earned)** | a concrete near-future, never hype | "Next enquiry: you send the price with a straight back." |

Rules: lead with the loss, resolve to relief/pride. Be specific (a real figure, not "revenue"). Never
manufacture fear with fake stats. True and vivid beats shaky and inflated.

## 4. Hook: earn the first 3 seconds

The first line does ~90% of the work. In a guide, that is the intro's opening line. On a sales page, that is
the hero. If the hook fails, nothing else matters.

**Text hook moves** (pick one, keep it short, one idea, open a loop):
- **The cost:** "Underpricing one wedding costs you a week's work."
- **The callout:** "Wedding photographers: your price list is the leak."
- **The number:** "Three enquiries this week. Two ghosted at the price."
- **The contrarian:** "Charging more isn't the risky move. Guessing is."
- **The open loop:** "She loved the photos. She still didn't book. Here's why."
- **The question (they can't say no to):** "When did you last raise your prices on purpose?"

**Sales-page hero principles:**
- Lead with the promise (the outcome), not the format ("a 38-page PDF" is proof material, not the hero).
- Show the loss or the outcome, not a logo or a mission statement.
- The buy CTA sits close to the hero, in plain words: what they get and what happens next.

## 5. Framework: give it a spine

Pick ONE (don't free-style):
- **PAS** (Problem → Agitate → Solution): the default loss-led shape, and the natural sales-page spine.
  Agitate with *empathy*, never cruelty.
- **BAB** (Before → After → Bridge): best when there's a clean transformation to show (great for a guide's
  intro or a case-style section).
- **StoryBrand-lite**: the **reader is the hero, the buyer is the guide** (Yoda, not Luke): "You're not
  failing, you're missing one piece."
- **AIDA**: keep the *spine* (hook → build → want → ask), drop the salesy "desire/dream" spirit.

Sales-page rules: hero carries the promise · the pain section mirrors the reader's own words · "what's
inside" lists the REAL contents from the actual product · proof is honest only (no invented testimonials; if
none exist, the contents are the proof) · price stated plainly · one buy CTA, repeated to the same target ·
FAQ answers real objections.

## 6. Story: make it move

- The **reader is the hero**; the buyer is the guide who hands them the tool.
- **Specific, hard-to-fabricate detail** beats generality ("she booked the barn on the Friday rate" beats
  "a customer converted").
- **Transformation** (messy before → calm after) + **stakes** (what it costs).
- One **human moment**: a real beat, an aside, a bit of mess. Benefits over features.

## 7. Sound human: the humanise pass

After drafting, scrub the AI tells. These are the patterns worth killing:
1. **Kill AI vocab:** delve, tapestry, testament, landscape (abstract), leverage, underscore, foster, robust,
   seamless, elevate, realm, navigate (abstract), "in today's fast-paced world". Say the plain word.
2. **No copula avoidance:** "serves as / stands as / boasts" becomes **is / has**.
3. **No rule-of-three padding** ("talks, panels, and networking") unless all three are real and needed.
4. **No signposting:** delete "let's dive in", "here's what you need to know", "without further ado": just
   start.
5. **No superficial "-ing" depth:** "symbolising the region's connection..." → say the fact.
6. **No false ranges:** "from X to Y" only on a real scale; else just list.
7. **No chatbot closers / sycophancy:** "I hope this helps", "great question", "you're absolutely right" :
   gone.
8. **No generic positive conclusions:** "the future looks bright" → a concrete next step.
9. **Cut filler:** "in order to" → "to"; "due to the fact that" → "because"; "has the ability to" → "can".
10. **Trim hedging:** "could potentially possibly" → "may".
11. **No manufactured staccato drama** ("No preference. No nostalgia. No prior.") and **no aphorism
    formulas** ("X is the Y of Z") unless genuinely earned.
12. **No fake-candid openers:** standalone "Honestly?" / "Look, here's the thing".

**Standing exceptions:**
- **No em dashes.** Use full stops, commas, colons, parentheses, or rewrite the sentence.
- **Curly vs straight quotes:** follow the platform / design system, don't force a change.
- **Bold/accent the number or keyword on purpose:** that's a style choice, not "AI boldface".
- **The evidence rule overrides everything:** no invented stats, no unverifiable named sources, never imply
  results the buyer doesn't have. A true observation beats a shiny number. On a sales page this is hard law:
  no fake testimonials, no invented buyer counts, ever.

## The loop (how to run this)

1. **Step 0 / 0.5**: resolve the tenant, load the voice profile + config.brand.
2. **Step 1**: one line: audience + emotion + action.
3. **Draft**: hook first, then a framework, then the story.
4. **Humanise**: run the §7 checklist.
5. **Audit**: ask three questions and fix what fails:
   - *What still sounds AI here?*
   - *Is the intended emotion actually on the page?*
   - *Would the buyer say this out loud, to one person, in plain language?*

## Don't over-edit: preserve human signs

Keep: specific concrete details, real opinions and mixed feelings, varied sentence length, genuine
asides/self-corrections. Plain technical/reference text **stays plain**, don't inject personality where
neutral is the right choice (a checklist item or a template instruction should read clean, not performed).
Only fix tells when they **cluster**; one formal word is not a crime.

## The calibration interview (when no voice profile exists yet)

Run this once per profile, then write the profile file so future runs skip straight to Step 0.5.

1. **Ask for 3 samples** of the buyer's real writing or talking: a voice note transcript, a text
   message thread, an email, a video transcript, anything unscripted. If they truly have none, ask them to
   talk for 60 seconds about what they do as if explaining it to a friend, and transcribe that.
2. **Extract from the samples:**
   - Sentence length and rhythm (short and punchy? long and winding?)
   - Words and phrases they actually use, and words they'd never say
   - Sentence openers and transitions they favour
   - Their stance: blunt, warm, dry, formal, playful
   - Any recurring line or belief they repeat (a signature phrase candidate)
3. **Ask directly for:**
   - Words to ban (jargon, competitor terms, anything that makes them cringe)
   - Whether they want a sign-off line, or just end on the CTA
4. **Write the profile** to `~/.claude/product-studio/profiles/<slug>.voice.md`. Use the ONE canonical
   format defined in `${CLAUDE_PLUGIN_ROOT}/skills/setup/SKILL.md` (section "Write the voice
   profile"): `# Voice profile - <Name>` with a Status and Written line, then the sections
   `## How you sound`, `## Phrases to use`, `## Words you would never use`, `## Example before / after`,
   `## Notes`. The setup wizard writes the same format, so both paths produce an identical file. Put stance,
   hard rules, and any signature belief in `## Notes`. Also mirror the banned words into
   `config.brand.bannedWords` and the recurring phrases into `config.brand.signaturePhrases` so the config
   and the profile never drift apart.
5. **Confirm** the profile with the user before using it on real copy. Update the file any time they correct
   the voice; corrections are the fastest way to sharpen it.
