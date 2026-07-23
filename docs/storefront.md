# The storefront

`/product-studio:storefront` takes a built product and produces everything needed to sell it: the sales
page, the checkout checklist, and the delivery note. Run it straight after a build, or any time on any
built product.

## The sales page

One file: `sales-page.html`, saved next to your product. It's completely self-contained: open it in any
browser, on any machine, with no connection, and it looks finished. No fonts to load, no images to host, no
code to install. That also means you can host it anywhere that serves a single file, or just send it.

It isn't a template with your name dropped in. Before writing any code, the run commits a design direction
for THIS product: colours seeded from your own brand with a reason for each, a type choice, and one
signature element drawn from the product's own subject. Then it critiques that direction against the
generic defaults every AI page reaches for, and only builds once the look belongs to your product and
nobody else's.

The structure is built to sell one thing: your promise as the headline, the pain it ends, what's actually
inside (pulled from the real product files, never invented), honest proof only, the price framed simply, a
short FAQ covering delivery and refunds, and one buy button repeated down the page.

Two honesty rules hold everywhere:

- **No fake proof.** If you don't have testimonials yet, the page uses the product's real contents as the
  proof and says nothing false. Nothing is invented: no fake quotes, no made-up numbers, no imaginary
  buyer counts.
- **One ask.** Every button on the page does the same thing: buy. No newsletter signups, no follow-me
  links, no second action to dilute the one that pays you.

## The checkout checklist

`checkout-checklist.md`, saved next to the sales page, filled in with your product's real name, price, and
files. It walks you through your platform, Gumroad or Lemon Squeezy (both, if you haven't decided), in
about ten plain steps: create the product, upload the file, set the price, paste the pitch, upload the
cover, set the delivery email text, publish, and copy the checkout URL. No screenshots needed; each step
names exactly what to click and what to paste.

## Replacing the placeholder link

Every buy button in the sales page starts out pointing at `#REPLACE-WITH-CHECKOUT-LINK`. That's
deliberate: the page is built before the checkout exists, so it can't know the real URL yet.

Once your platform gives you the product's checkout URL, open `sales-page.html` in a text editor, find
every `#REPLACE-WITH-CHECKOUT-LINK`, and replace each one with that URL. The checklist walks you through
it. Until you do this, the buttons go nowhere, which is the honest state of a page with no checkout behind
it.

## The test purchase

Before you share the page anywhere, buy your own product once. Gumroad supports a 100% discount code for
self-testing; Lemon Squeezy has a test mode with test card details. Confirm three things: the checkout
works, the delivery email arrives, and the file inside it opens. The delivery note (`DELIVERY.md`, saved
next to the page) spells out exactly what the customer should receive so you can check against it.

## What "listed" means on the shelf

When the storefront run finishes, your product's row in the memory flips to `listed`: the sales page
exists and the sell path is in your hands. It does not mean the checkout link is live yet; that last paste
is yours. When real sales come in, tell the system (`/product-studio:lesson`, or answer the shelf when it
asks) and the row moves to `selling`, with the learning written down so future builds lean toward what
converted.
