# The Brain

The Brain is The Product Studio's memory. Every build reads from it before doing anything and writes to it
after. That is what makes the tenth product faster and sharper than the first, and why it never starts from
zero on your format.

## Why it matters

Without memory, every build starts blind: the same structure questions, the same format guesses, the same
mistakes. With the Brain, what worked gets reused, what sold gets favoured, and what got killed stays
killed. You build a product line, not a series of one-offs.

## What it stores

Two simple tables:

- **Products**: every product it has built, with the idea source, the specific buyer, the format, the
  one-line promise, the price, the status (drafting, built, listed, selling, or killed), where the files
  live, where the sales page lives, and the revenue you report once sales exist (never invented).
- **Lessons**: the rules it must follow, one line each, learned from kills, from what sold, or taught
  directly with `/product-studio:lesson`. Only active lessons apply.

There's also a `runs/` folder next to the tables: one record per build, the full output, which is what the
quality gate checks.

Lessons are grouped into four areas, so the right rule reaches the right step:

- **format** - your structure and format preferences, and what shape sold
- **offer** - pricing and promise learnings
- **copy** - sales-page voice rules
- **general** - everything else

## How the loop works

1. Before a build, The Product Studio reads every active lesson and every killed product. Lessons are hard
   constraints; killed products never get rebuilt in disguise.
2. After a build, it logs one Products row with the status.
3. When a product is killed (`/product-studio:kill-product`), the reason becomes a new active lesson,
   written as a rule the next build can actually follow. When a product sells and you report it, the
   what-converted learning is written the same way. Both bind every future build: that is the compounding.
4. If the Brain can't be reached for some reason, the run says so and carries on without it. You never lose
   a deliverable because memory failed.

## Two ways to run it

**Local (the default).** Plain markdown files on your own computer, under
`~/.claude/product-studio/brain/<slug>/`. No setup, no accounts, works the moment you install. Good for
most people.

**Airtable.** Your own base, created fresh for you, with the same two tables. Good if you already work in
Airtable or want to browse the memory outside Claude Code. Needs the Airtable connection to be active; if
it isn't, setup tells you and falls back to local so you're never stuck.

Both modes store exactly the same information. Switching modes does not change what The Product Studio can
do.

## Setting it up

Run `/product-studio:setup-brain` and pick local or Airtable when asked. The setup wizard offers this at
install time too. Every build still works before the Brain exists; it just won't remember anything between
builds yet.

## Switching later

You can move from local to Airtable at any time by running `/product-studio:setup-brain` again and choosing
Airtable. Your existing products and lessons stay in the local files; new entries go to the fresh base from
then on.
