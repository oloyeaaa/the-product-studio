---
name: eval
description: Regression check for The Product Studio. Re-runs the quality gate on the latest build's run file (or rebuilds the profile's fixed eval briefs from scratch) and reports every check. Clears a blocking REGRESSION lesson on a clean pass. Use for "run the eval", "did that change break anything", "regression check", "clear the regression", or /product-studio:eval.
argument-hint: "[--profile <slug>] [--from-scratch] [what changed, one line]"
allowed-tools: Read, Write, Edit, Bash
---

# /product-studio:eval - regression check against the gate

Arguments: **$ARGUMENTS**

This is a thin wrapper over the deterministic gate at
`${CLAUDE_PLUGIN_ROOT}/skills/build/scripts/eval_product.py`. It writes no Products rows and ships nothing;
it only checks that the pipeline still clears the gate, and clears the blocking `REGRESSION:` lesson when it
does.

## Step 0: resolve the tenant

Parse `--profile <slug>` from the arguments if present. Everything else is an optional `--from-scratch` flag
plus a free-text note on what changed. If no `--profile` flag, read `defaultProfile` from
`~/.claude/product-studio/config.json`. Load `~/.claude/product-studio/profiles/<slug>.json`. If that file
is missing, tell the buyer to run `/product-studio:setup` and stop.

## Default mode: re-gate the latest run

1. **Find the latest run file**: the newest `<date>-<product-slug>.json` in
   `~/.claude/product-studio/brain/<slug>/runs/` (per the Brain contract at
   `${CLAUDE_PLUGIN_ROOT}/skills/brain/SKILL.md`). If none exist, tell the buyer there is nothing to check
   yet (run `/product-studio:build` first, or use `--from-scratch`) and stop.

2. **Run the gate**:

   ```
   python "${CLAUDE_PLUGIN_ROOT}/skills/build/scripts/eval_product.py" "<run.json>" "<profile.json>"
   ```

   (If `python` is not on PATH, try `py` on Windows or `python3`.) `<profile.json>` is the resolved path
   `~/.claude/product-studio/profiles/<slug>.json`.

3. **Parse the `@@EVAL_JSON@@` line** and report per-check, plain English, one line each: format_known,
   no_placeholder_filler, fillins_marked_not_faked, substance_per_format, promise_delivered, price_carried,
   voice_and_cta, cover_present, status_valid. Show pass/fail and the detail for every failure. If the
   script crashed or the line cannot be parsed, treat the run as failed and show the error.

4. **On an all-pass:** if an Active Lessons row exists with Rule starting `REGRESSION:`, deactivate it (set
   Active = false, per the Brain contract). Tell the buyer the block is cleared and
   `/product-studio:build` will run again.

5. **On any failure:** name the failed checks and what to fix. Do not deactivate the `REGRESSION:` lesson.
   Do not soften the result.

## From-scratch mode (`--from-scratch`, or when the buyer asks for a full regression check)

The buyer wants to know the pipeline itself still produces gate-clean products, not just that the last run
was fine.

1. Read `eval.evalBriefs` from the profile. If missing or empty, tell the buyer this profile has no eval set
   yet (setup writes two fixed briefs; add them to `eval.evalBriefs`) and stop. A fixed eval set has to be
   chosen deliberately, not invented on the fly.
2. For each brief, run a fresh build following `${CLAUDE_PLUGIN_ROOT}/skills/build/SKILL.md`, with the
   product files and run JSON written to a temp folder in the session scratchpad, never into `runs/` or
   `products/`. Apply the active lessons as hard constraints, same as production, so the eval tests what a
   real build sees.
3. Gate each temp run with `eval_product.py` exactly as above and aggregate: passed/total across both
   briefs, plus every failed check named per brief.
4. Apply the same step 4 / step 5 outcome: all-pass clears an Active `REGRESSION:` lesson; any failure
   leaves it in place and reports plainly.

## Report

Tight, numbers first:
- Score as a fraction (checks passed / total), per run where more than one ran.
- Every failed check with its detail, in plain English.
- One clear recommendation: **safe to keep building** / **regression, fix before the next build**.
- If a `REGRESSION:` lesson was cleared or left in place, say which.

## Do not

- Do not write any Products row, save anything into `runs/` or `products/`, or touch the Brain beyond
  deactivating a cleared `REGRESSION:` lesson.
- Do not change a profile's eval briefs casually. If the buyer asks to change them, do it in the profile and
  say plainly that scores before and after are not comparable.
- Do not silently round a failure up to "probably fine". Name the checks that failed.
- Do not hardcode a base ID, table ID, or field ID. All of it comes from the resolved profile config.
