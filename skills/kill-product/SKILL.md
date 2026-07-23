---
name: kill-product
description: Kill a product, record why (and any revenue it made), and turn the reason into a lesson that binds every future build. The killed row plus the lesson are the compounding memory, The Product Studio never rebuilds what got killed. Use for "kill this product", "it didn't sell", "scrap that one", or /product-studio:kill-product.
argument-hint: "[--profile <slug>] <the product, or blank for the latest> [reason]"
allowed-tools: Read, Write, Edit, Bash
---

# /product-studio:kill-product - kill a product and keep the lesson

Arguments: **$ARGUMENTS**

## Step 0: resolve the tenant

Parse `--profile <slug>` from the arguments if present. Everything else is an optional product to match plus
an optional reason. If no `--profile` flag, read `defaultProfile` from
`~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If that file
is missing, tell the buyer to run `/product-studio:setup` and stop.

## Steps

1. **Find the Products row.** Per the Brain contract (`${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md`), match
   the remaining argument text against the Product cells. If no argument text was given, take the most
   recent row with Status = `listed` or `built`. If nothing matches, list what exists in the Products table
   and stop.

2. **Show the buyer the row**: the product, the promise, the price, the current status, and any revenue
   recorded so far. Then ask for anything missing, two things at most:
   - **Any revenue it made**, if it was listed and sold at all (e.g. "3 sales, 87 total"). Write the number
     into the Revenue cell. If it never sold, leave Revenue as it is and note that in the reason.
   - **The one-line why.** This is required (use the reason from the arguments if one was passed). Never
     skip it, it is how the lesson gets captured at all.

3. **Flip the status.** Set Status = `killed` on that row.
   - Local mode: edit the row in place in `products.md`, per the Brain contract's escaping rules.
   - Airtable mode: update the record. Table and base IDs come from the profile config, never typed
     literally.

4. **Write ONE Lessons row** from the why: rewrite the raw reason as a short imperative rule under 100
   characters, specific enough that a future build can obey it. Pick the Area by content:
   - `format` for shape and structure rules ("Never build another 80-page ebook for this audience").
   - `offer` for pricing and promise truths ("This audience won't pay over 30 for a checklist").
   Source = `kill reason`, Active = true, Added = today. Apply the Brain contract's dedup rule first.

5. **Report**: the killed product, the revenue recorded (if any), the saved lesson verbatim so the buyer can
   confirm it was captured correctly, and the plain line: **"killed products bind every future build; this
   one will not come back"**.

## Do not

- Do not kill without a why. If the buyer won't give one, stop, the kill without the lesson wastes the moat.
- Do not delete the row. A killed row IS the memory; the build skill reads it as a hard constraint.
- Do not delete the product files on disk. The row is killed; the files stay unless the buyer removes them.
- Do not soften the reason. "Nobody bought it at that price" stays that, not "could revisit later".
- Do not invent a revenue number. Blank means the buyer never reported one.
- Do not write a vague or restated-complaint lesson. Rewrite it as a rule the next build can actually follow.
- Do not hardcode a base ID, table ID, or field ID. All of it comes from the resolved profile config.
