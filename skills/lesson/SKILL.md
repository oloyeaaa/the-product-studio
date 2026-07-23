---
name: lesson
description: Teach The Product Studio a format, offer, or copy rule directly, without waiting for a kill. Writes one Active Lessons row that binds every future build. Use for "teach the product studio", "add a lesson", "remember this about my products", "this format sold", or /product-studio:lesson.
argument-hint: "[--profile <slug>] [--area format|offer|copy|general] <the lesson, in plain English>"
allowed-tools: Read, Write, Edit
---

# /product-studio:lesson - teach The Product Studio something directly

Arguments: **$ARGUMENTS**

## Step 0: resolve the tenant

Parse `--profile <slug>` from the arguments if present. If no `--profile` flag, read `defaultProfile` from
`~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If that file
is missing, tell the buyer to run `/product-studio:setup` and stop.

## Steps

1. **Parse `--area <format|offer|copy|general>`** from the remaining arguments. Default to `general` if not
   passed. Everything left after removing `--profile` and `--area` is the lesson text. If no lesson text was
   passed, ask the buyer for it and stop. Do not invent one.

2. **Rewrite the input as a short imperative rule** if it isn't already one. "My people never finish long
   ebooks" becomes "Keep guides under 40 pages for this audience." Keep it under 100 characters where
   possible.

3. **Check for a near-duplicate.** Read the existing Active Lessons rows for this Area (plus `general`) per
   the Brain contract (`${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md`). If one already says roughly the same
   thing, tell the buyer instead of creating a second row.

4. **Write the Lessons row**: Rule = the rewritten imperative rule, Area = the parsed area, Active = true,
   Source = `manual`, Added = today's date. If the lesson reports a real sale or performance result ("the
   checklist sold 12 copies at 19"), set Source = `performance` instead, and if the buyer names a revenue
   number for a listed product, also update that Products row's Revenue cell per the Brain contract.

5. **Report**: show the exact rule saved, so the buyer can confirm it was captured the way they meant it. If
   the rewrite changed the meaning, say so and ask if it's right.

## Do not

- Do not soften or generalise the lesson so much it loses the actual instruction.
- Do not create a duplicate of an existing active lesson for the same area.
- Do not invent a lesson when no text was given. Ask and stop.
- Do not hardcode a base ID, table ID, or field ID. All of it comes from the resolved profile config.
