---
title: "We scanned 776 small CPG Shopify stores. Here's what their product pages are missing."
slug: cpg-shopify-product-page-scan-2026
description: "Original data from 776 small CPG Shopify stores: how many product pages lack reviews, a sticky add to cart, shipping info, photos or a subscription option."
date: 2026-10-09
cluster: "Teardowns and original data"
tags: [original data, product pages, shopify cro, cpg, reviews, sticky add to cart]
draft: false
---

Of the 442 small CPG Shopify stores in our scan that were never filtered for quality, 35% show no review widget on the product page, 62% show no sticky add to cart we could detect, and 49% sell a consumable with no subscription option. The pages are not broken. They are unfinished: theme defaults left as shipped, one photo, a thin description, and nothing about shipping or returns near the buy button.

## How we got the data, and why the pool numbers are worse

Between Sept 19 and 27, 2026 we collected 799 domains of small, founder-run CPG brands (food, beverage, pet, body care) from state "made in" directories, farmers-market vendor lists, maple and honey trade-association member lists, Startup CPG Shelfie finalist pages and "Powered by Shopify" searches. On Oct 7 we scanned every one. 776 were live Shopify stores and 752 gave us a product page we could parse: one per store, the first purchasable product.

This is not a random sample of Shopify. It skews small. And 310 of the 752 come from our buyer pool, which an earlier qualifier had scored as needing visible conversion work, so that set is tilted toward weak sites by design. The fair number in each finding is the raw-only set: the 442 stores sourced the same way but never qualified. Pool numbers show how bad it gets at the small end. Where a number only exists for all 752 pages, I say so.

## 1. 35% show no reviews on the product page

Raw-only: 35%. Pool: 60%. All 752 pages: 45% (340 of 752). "Reviews present" means the widget markup is on the page, not that it holds reviews, so the real gap is larger.

The shopper's first question is whether it is any good. No stars, no answer. Spiegel Research Center found a product with five reviews had a 270% higher purchase likelihood than one with none, and most of the gain came from the first five. Grade B: a large observational dataset, one research group.

The fix: a star summary with a count by the title, full reviews lower down. If you already pay for a review app, check the widget block is actually in your product template. 25 stores (3% of 752) had a review app installed and nothing on the page.

## 2. 62% show no sticky add to cart (an upper bound)

Raw-only: 62%. Pool: 90%. Our lowest-confidence signal: we matched class and setting names like sticky-add-to-cart, so a theme that names it differently was missed. Treat 62% as a ceiling.

The shopper scrolls down to read the ingredients and the buy button is gone. The evidence for sticky bars is grade B. One agency test on a supplement brand saw +7.9% orders on desktop and +5.2% on mobile when the bar opened an add-to-cart drawer in place. The same client's mobile bar that only scrolled back to the top did nothing. Vendor ranges like "5 to 12%" trace to no study.

The fix: a short, opaque bar that appears once the main button leaves the screen and adds in place. Disclosure: we make Conviction, a theme in development for the Shopify Theme Store; its bar changes message with the section in view. The bar is grade B. The changing message is grade D, no published test, so it is built with an off switch. Setup notes are in [the docs](/conviction/docs/).

## 3. 34% say nothing about shipping, 76% say nothing about returns

Both numbers cover all 752 parsed pages; there is no raw-only split. Shipping information beyond the theme's stock "Shipping calculated at checkout." line was absent from 34% (254 of 752). Returns, guarantee or refund wording was absent from 76% (573 of 752).

Baymard's abandonment surveys put "extra costs too high" first, at 40% of abandoners. Grade A. 64% of users start thinking about shipping cost on the product page and 60% look for the return policy there, both grade B. A footer link does not count: 27% of test users missed free shipping that lived only in a sitewide banner.

The fix: one line under the buy button with the shipping cost or threshold, a delivery estimate if you have one, and the returns rule in plain words.

## 4. 39% have one product photo or none

All 752 pages: 39% (294 of 752). 41 had no image, 253 had exactly one. Median: 2.

Baymard: 56% of users explore the images as their first action on a product page. Grade B. With CPG you are asking someone to buy something they haven't tasted, smelled or used. One packshot shows the packaging, rarely the size, the texture or how it fits into someone's life.

The fix: three to five images (grade C, a Baymard guideline). At minimum: a readable label, a photo for scale and the product in use. People love seeing someone like them use a product they haven't tried. A professional shoot is still best. The cheaper route: phone photos on a white background, cleaned up with AI enhancement.

## 5. 29% describe the product in under 50 words

Raw-only: 29%. Pool: 33%. The median across all 752 pages is 83 words.

Fifty words cannot cover what it is, what is in it, how to use it and why it costs what it costs. NN/g: people read the start of a description and skim the rest, so lead with the essentials. Grade C.

The fix: answer those four questions in the first 100 words. Put the story below, with headings, so it scans. Keep every claim to what your label can back.

## 6. 49% sell a consumable with no subscription option

Raw-only: 49%. Pool: 69%.

Most of these products run out. With no reorder path the shopper does the remembering. Baymard's subscription research is grade B: users need the price per delivery visible and plain details on pausing, skipping and cancelling.

The fix: offer subscribe and save with one-time selected by default. Defaults move choices strongly (meta-analysis of 58 studies, grade A), which is exactly why preselecting the subscription is a legal risk under ROSCA in the US and the EU ban on pre-ticked boxes. Show both prices and say how cancelling works.

## 7. 30% run a free theme, 12% run a vintage one

Raw-only: 30% on a free theme. Pool: 88%. Across the 765 stores with a readable theme name, Dawn alone was 20% (156) and Shopify's vintage free themes such as Debut, Brooklyn and Minimal were 12% (92). Placeholder copy like "Welcome to our store" was still live on 2% of raw-only homepages and 7% of pool homepages.

A free theme is not the problem. An unfinished one is. Free-theme stores had no product-page reviews 53% of the time against 36% for paid or custom themes, and no sticky bar detected 82% against 64% (all 752).

The fix: open the theme editor and use what is there. Place the review block. Turn on the sticky bar if your theme has one. Delete the placeholder sections. On a vintage theme, plan the move before your BFCM freeze. Shopify only ships security fixes for them, and they can't use app blocks.

## Good enough for now: why these pages stay unfinished

Founders get a site up so they can start selling. It's good enough for now, and it usually is. But no one ever specifies how long "now" is. A couple of weeks turns into a couple of years. At the agency, brands came to us for a rebuild after four years live with half a website the whole time. They thought the website was a dead end because it didn't make them money. And it won't, if it stays half finished. Only your most loyal people buy.

A half-built page can waste the attention you worked very hard to earn, or pay for. You're running ads, sending emails, landing the brand in stores. Then someone hits the product page and every gap trips a wire. Each one triggers the next, like dominoes, and it's up to you whether they finish where the person buys or where the person leaves. The cost isn't just a missed order. It's more support tickets, fewer repeat purchases, and marketing decisions based on a website that never gave the product a fair chance.

Time and money matter, but ownership is usually the biggest issue. Somebody has to own the entire online shopping experience, and once a brand scales offline it's usually not the founder. The founder owns the product, the designer the visuals, the developer the build, a marketer the ads. Unless one person, on the team or at an agency, brings those pieces together, the gaps sit there forever. Launching the site is a milestone. The website needs to grow with the brand.

## What the data cannot tell us

One product page per store; the hero might be polished and the long tail bare, or the reverse. No JavaScript ran, so widgets and bars injected after load were missed. That is why "no sticky bar", "no FAQ" and "no trust badges" are upper bounds, and why I left the last two out. "Reviews present" means markup, not review count. The sample is small CPG from directories, not Shopify at large.

And none of it measures demand. 16% of stores (122 of 758) had not published a product in over a year. A page can be fixed. A store nobody visits will not show the lift. Nor will a store that can't tie the lift to its ads or email: 21% of homepages (159 of 772) showed no Meta pixel, no GA4 id and no Klaviyo. Our method can miss GA4, so the true share is likely a little lower.

## If you only fix three things

Start with the product page, not the homepage. Write down the questions a visitor asks that the page can't answer: what is this, what's in it, why should I trust it, where does it ship from, how fast can I get it. Fix the biggest one on each page. Then use that page as the standard for the rest of your catalog. Stuck for questions? Open someone else's site and ask them out loud.

1. Reviews on the product page, star summary by the title. Grade B, and the largest gap a shopper actually sees.
2. One plain line under the buy button: shipping cost or threshold, delivery time, returns. Grade A on the cost side.
3. Photos that answer questions: a readable label, something for scale, the product in use. Grade B on behavior, and a phone can do it this weekend.

Sticky bar and subscriptions come next; test rather than assume.

More from the [teardowns and original data](/blog/topics/teardowns-and-original-data/) series.
