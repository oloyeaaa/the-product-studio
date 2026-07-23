# Checkout checklist - [PRODUCT NAME]

Work through this top to bottom. Each step is one small thing. At the end you have a live product page, a
working buy button, and proof the file actually arrives.

Product: [PRODUCT NAME]
Price: [PRICE]
File to upload: [ASSET FILE]
Cover image: [COVER PNG]

---

## If you sell on Gumroad

1. Go to gumroad.com and create an account, or log in if you already have one.
2. From your dashboard, click **New product**.
3. Choose **Digital product** as the type.
4. Name it exactly: **[PRODUCT NAME]**.
5. Set the price to **[PRICE]**.
6. Upload **[ASSET FILE]** as the product file. This is the exact file your customer receives.
7. For the description, open `sales-page.html` in your browser and copy the short pitch from the top of the
   page (the headline and the line under it). Paste that in. Keep it short; the sales page does the selling.
8. Upload **[COVER PNG]** as the cover image.
9. Find the receipt or thank-you message setting and paste in the text from `DELIVERY.md` (the "what you
   receive" lines), so the purchase email tells the customer exactly what they got.
10. Click **Publish**, then copy the product URL Gumroad gives you.
11. Open `sales-page.html` in a text editor. Find every `#REPLACE-WITH-CHECKOUT-LINK` and replace each one
    with the product URL you just copied. Save the file.
12. Make a test purchase. Gumroad lets you create a 100% discount code, so you can buy your own product for
    nothing: create one, buy through it, and confirm the email arrives and **[ASSET FILE]** opens.

## If you sell on Lemon Squeezy

1. Go to lemonsqueezy.com and create an account, or log in. If this is your first product, complete the
   short store setup it asks for (store name and currency).
2. Click **New product**.
3. Name it exactly: **[PRODUCT NAME]**.
4. Set the price to **[PRICE]** as a single payment.
5. Under **Digital delivery** (in the product's files or variants section), upload **[ASSET FILE]**. This is
   what the customer receives after paying.
6. For the description, copy the short pitch from the top of `sales-page.html` (the headline and the line
   under it) and paste it in.
7. Upload **[COVER PNG]** as the product image.
8. In the confirmation email settings, paste the text from `DELIVERY.md` so the purchase email tells the
   customer exactly what they got.
9. Publish the product, then copy the **Buy link** (the checkout URL) from the product's sharing options.
10. Open `sales-page.html` in a text editor. Find every `#REPLACE-WITH-CHECKOUT-LINK` and replace each one
    with the checkout URL you just copied. Save the file.
11. Make a test purchase. Lemon Squeezy has a test mode: switch it on, buy your own product with the test
    card details it provides, and confirm the email arrives and **[ASSET FILE]** opens. Switch test mode off
    afterwards.

---

## Go live check (do all five before sharing the page)

1. The price on the platform matches [PRICE], the price in the run.
2. [ASSET FILE] downloads and opens on a machine that is not yours, or at least in a fresh folder.
3. The cover shows correctly on the product page.
4. Every buy button in `sales-page.html` opens the real checkout, not the placeholder.
5. Your test purchase delivered the file to your inbox.

When all five pass, the product is live. Share the sales page.
