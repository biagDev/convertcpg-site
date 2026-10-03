#!/usr/bin/env python3
"""Build the ConvertCPG site pages: home, about, FAQ, services.
Also refreshes the shared header and footer on the support page.

Usage: python3 tools/build-site.py
Docs page: python3 tools/build-docs.py <conviction-theme-docs.md>
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import head, header, tail, FOOTER, add_clarity  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
IMG = "/assets/conviction/img/"
SOON = '<span class="button button--soon" aria-disabled="true">Coming soon to the Shopify Theme Store</span>'


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)
    print("Wrote", path)


# ---------------------------------------------------------------- HOME
RAIL_STEPS = [
    ("Story chapter", "The opening claim", "Why we built Sowfield.",
     "Six bottles on the counter and no idea what was in them. So we made one scoop with every dose printed.",
     "One scoop, every morning.", "Daily Foundation · $64", "Add to cart", "story-chapter.jpg"),
    ("Ingredients", "Proof, with doses and sources", "Every ingredient, with its dose.",
     "Nothing hidden behind a proprietary blend. Each card shows the amount and why it is there.",
     "Every dose on the label.", "Daily Foundation · $64", "Add to cart", "ingredients.jpg"),
    ("Stats", "Numbers with sources", "Every batch, tested.",
     "Large numbers with a source line under each, so the claim and the proof sit together.",
     "Tested batch by batch.", "Certificates on every batch page", "Add to cart", "batch-testing.jpg"),
    ("Reverse risk", "Removes the last doubt", "Try it for 60 days.",
     "Your guarantee, returns and shipping promises in one place, right before the decision.",
     "Love it or your money back.", "Pause or cancel any time", "Subscribe and save", "morning-glass.jpg"),
]
MODULES = [
    ("Story chapter", "One moment of the story, with image and link."),
    ("Story sequence", "Numbered steps, or pinned on scroll."),
    ("Ingredients", "Name, role, amount, benefit and source."),
    ("Difference", "“The usual way” next to “Our way”."),
    ("Why grid", "Icon, heading and text in 2 to 4 columns."),
    ("Why for you", "“If you’re… then this is for you.”"),
    ("Stats", "Large numbers with labels and sources."),
    ("Testimonial", "A review carousel with ratings."),
    ("Press", "Press logos with short quotes."),
    ("Customer photos", "A lightbox grid with “Shop the look”."),
    ("Comparison table", "You against up to 3 competitors."),
    ("FAQ", "Filterable accordions, with a jump to buy."),
    ("Reverse risk", "Guarantee, returns and shipping promises."),
    ("Founder note", "Portrait, letter, video and signature."),
    ("Manifesto", "One large statement, plain or dark."),
]
DIFF = [
    ("Product page", "Gallery, price, button, and a description nobody opens.", "A story that runs claim, proof, objection, offer."),
    ("Sticky cart", "Says “Add to cart” forever, whatever the shopper is reading.", "The Rail changes its message to match the section on screen."),
    ("Bundles", "Another app, another monthly bill, another script.", "Native bundle tiers with real savings and per-unit prices."),
    ("Proof", "Trust badges pasted at the bottom of the page.", "Stats, sources and reviews placed next to the claim they back."),
    ("Urgency", "Countdown timers and “12 people are viewing this.”", "None. Persuasion by the product’s real story."),
]


def home():
    e = html.escape
    steps = []
    for i, (sec, hint, hl, body, rail, sup, btn, _img) in enumerate(RAIL_STEPS):
        steps.append(
            f'<li><button type="button" data-rail-step aria-pressed="{"true" if i == 1 else "false"}" '
            f'data-section="{e(sec)}" data-headline="{e(hl)}" data-body="{e(body)}" data-rail-text="{e(rail)}" '
            f'data-support="{e(sup)}" data-button="{e(btn)}"><span class="n">0{i+1}</span>'
            f'<span class="t"><b>{e(sec)}</b><span>{e(hint)}</span></span><span class="on" aria-hidden="true">On screen</span></button></li>')
    imgs = "".join(f'<img src="{IMG}{s[7]}" alt="" loading="lazy" class="{"is-on" if i == 1 else ""}">' for i, s in enumerate(RAIL_STEPS))
    cur = RAIL_STEPS[1]
    mods = "".join(f'<div class="module"><small>{i+1:02d}</small><b>{e(n)}</b><span>{e(w)}</span></div>' for i, (n, w) in enumerate(MODULES))
    diff = ['<div class="head" aria-hidden="true"></div><div class="head">A typical theme</div><div class="head us">Conviction</div>']
    for k, a, b in DIFF:
        diff.append(f'<div class="k">{e(k)}</div><div>{e(a)}</div><div class="us">{e(b)}</div>')
    body = f"""<div class="announce">Conviction is in review for the Shopify Theme Store. <a href="/conviction/docs/">Read the docs</a></div>
{header('home')}
<main id="content">
<section class="hero" data-rail-hide>
<div class="hero__copy">
<div class="kicker">Conviction · A Shopify theme</div>
<h1>The product page that makes the case.</h1>
<p class="lead">Conviction turns your product page into a story, section by section. Its Rail keeps Add to cart on screen and changes the message as shoppers read.</p>
<div class="buttons">{SOON}<a class="button button--ghost" href="#rail">Watch the Rail work</a></div>
<div class="hero__micro"><span>One-time purchase on the Shopify Theme Store</span><span>Free updates</span><span>Support from the founder</span></div>
</div>
<div class="mock" aria-label="Example product page built with Conviction" role="img">
<div class="mock__bar"><i></i><i></i><i></i><span class="mock__url">sowfield-wellness.myshopify.com/products/daily-foundation</span></div>
<div class="mock__body">
<img src="{IMG}daily-foundation.jpg" alt="" width="967" height="1200">
<div class="mock__info">
<div class="mock__brand">Sowfield</div>
<div class="mock__title">Daily Foundation</div>
<div>One scoop every morning. Every dose on the label.</div>
<div class="mock__price">$64 <small>$2.13 per serving</small></div>
<div style="font-size:11px;color:#6B6B68">Flavor: Unflavored</div>
<div class="chips"><span class="chip chip--on">Unflavored</span><span class="chip">Citrus</span><span class="chip">Cacao</span></div>
<div class="mock__atc">Add to cart</div>
</div>
</div>
<div class="rail-demo"><div><strong>One scoop replaces six bottles.</strong><span>Reading: The difference</span></div><em>Add to cart · $64</em></div>
<div class="mock__tag">The Rail: its message follows the story</div>
</div>
</section>

<section class="strip" aria-label="Conviction in numbers" data-rail="Fifteen story sections. Zero apps needed." data-rail-sub="Built into the theme">
<div><b>15</b><span>story sections built for product pages</span></div>
<div><b>0</b><span>apps needed for the Rail, bundle tiers or stories</span></div>
<div><b>92+</b><span>mobile Lighthouse performance on both demo product pages</span></div>
<div><b>10 yrs</b><span>of Shopify conversion work behind every section</span></div>
</section>

<section class="section manifesto" data-rail="Your page has to sell the product." data-rail-sub="Not just look good">
<div class="rule" aria-hidden="true"></div>
<h2 class="h2">Most themes sell the look. Your product page has to sell the product.</h2>
<p>A gallery, a price and a button can't explain why yours is worth it. Conviction gives every product page room to make the argument: what it is, why it's different, the proof, and the answer to every doubt.</p>
</section>

<section class="section" style="padding-top:0" aria-label="Conviction compared with a typical theme" data-rail="Claim, proof, objection, offer." data-rail-sub="The difference">
<div class="diff">{''.join(diff)}</div>
</section>

<section class="section section--ink" id="rail" data-rail="You're looking at one right now." data-rail-sub="This bar is a Conviction Rail">
<div class="rail-section">
<div>
<div class="kicker">The Adaptive Conviction Rail</div>
<h2 class="h2" style="margin-top:22px">A buy button that knows what they just read.</h2>
<p class="lead" style="margin-top:22px">The Rail appears once the buy box scrolls away. As each story section crosses the screen, its message changes to match. Its button adds the exact variant, quantity and plan picked in the buy box. Tap a section to see it change.</p>
<ul class="rail-steps">{''.join(steps)}</ul>
</div>
<div class="phone" aria-live="polite">
<div class="phone__screen">
<div class="phone__img">{imgs}</div>
<div class="phone__copy"><small data-f="section">{e(cur[0])}</small><b data-f="headline">{e(cur[2])}</b><p data-f="body">{e(cur[3])}</p></div>
<div class="rail-demo"><div><strong data-f="rail">{e(cur[4])}</strong><span data-f="support">{e(cur[5])}</span></div><em data-f="button">{e(cur[6])}</em></div>
</div>
</div>
</div>
</section>

<section class="section" id="sections" data-rail="Fifteen ways to make the argument." data-rail-sub="Story sections">
<div class="section-head">
<div><div class="kicker">Story sections</div><h2 class="h2" style="margin-top:18px;max-width:760px">Fifteen ways to make the argument.</h2></div>
<p>Stack them inside a product story or use them on any page. Start from a Supplement or Tech story, then swap in your copy. Connect any field to a metafield and each product tells its own story.</p>
</div>
<div class="modules">{mods}</div>
</section>

<section class="section section--tint" id="demos" data-rail="Two presets. Two real stores." data-rail-sub="Conviction and Verity">
<div style="text-align:center;display:flex;flex-direction:column;align-items:center;gap:18px;margin-bottom:48px">
<div class="kicker kicker--plain">Two presets, two demo stores</div>
<h2 class="h2">See it on a real store.</h2>
<p class="lead" style="margin:0 auto">Every preset installs exactly like its demo. The live demos open when Conviction launches.</p>
</div>
<div class="demos">
<article class="demo">
<img src="{IMG}northform-hero.jpg" alt="Northform demo store: a graphite keyboard on a desk" loading="lazy" style="object-position:50% 72%">
<div class="demo__body">
<div class="demo__top"><h3 class="sans">Conviction</h3><span class="tag">Electronics</span></div>
<p>Graphite, steel and clean sans-serif headings. Built for devices, hardware and technical products. Demo store: Northform.</p>
<span class="button button--soon" aria-disabled="true">Demo coming soon</span>
</div>
</article>
<article class="demo">
<img src="{IMG}sowfield-hero.jpg" alt="Sowfield demo store: a Daily Foundation canister and a green drink on a kitchen counter" loading="lazy">
<div class="demo__body">
<div class="demo__top"><h3>Verity</h3><span class="tag">Wellness</span></div>
<p>Warm sand, moss and editorial serif headings. Built for supplements, wellness and ingredient-led products. Demo store: Sowfield.</p>
<span class="button button--soon" aria-disabled="true">Demo coming soon</span>
</div>
</article>
</div>
</section>

<section class="section" data-rail="Built and shot like real brands." data-rail-sub="The demo stores">
<div class="section-head">
<h2 class="h2" style="max-width:760px">Two brands, built and shot like real ones.</h2>
<p>Every product, photo and story section on the demos is set up the way a merchant would do it, in the theme editor.</p>
</div>
<div class="mosaic">
<img class="tall" src="{IMG}sowfield-counter.jpg" alt="Sowfield canister on a kitchen counter" loading="lazy">
<img src="{IMG}northform-typing.jpg" alt="Typing on a Northform keyboard" loading="lazy">
<img src="{IMG}sowfield-set.jpg" alt="Sowfield canister and tin together" loading="lazy">
<img class="wide" src="{IMG}northform-desk.jpg" alt="A Northform desk setup from above" loading="lazy">
</div>
</section>

<section class="section" style="padding-top:0" data-rail="The selling features, built in." data-rail-sub="No extra apps">
<div class="included">
<div style="display:flex;flex-direction:column;gap:20px">
<div class="kicker">Everything included</div>
<h2 class="h2">The selling features, built in.</h2>
<p class="lead">No extra apps for the things every product page needs. Fewer scripts, fewer monthly bills.</p>
</div>
<div class="included__cols">
<div><h3>Selling</h3><ul><li>Bundle tiers with savings</li><li>Subscriptions via selling plans</li><li>Color and image swatches</li><li>Unit pricing</li><li>Shop Pay Installments</li><li>Accelerated checkout</li><li>Gift cards with recipient</li><li>Local pickup</li></ul></div>
<div><h3>Store</h3><ul><li>Cart drawer or cart page</li><li>Free shipping progress bar</li><li>Predictive search</li><li>Collection filters</li><li>Quick buy and image zoom</li><li>Mega menu</li><li>Editorial blog layouts</li><li>Newsletter and contact</li></ul></div>
<div><h3>Control</h3><ul><li>App blocks on product pages</li><li>Custom Liquid everywhere</li><li>Metafield-driven stories</li><li>Shopify font library</li><li>French, German, Spanish, Italian</li><li>Keyboard and screen reader tested</li><li>Reduced motion respected</li><li>Free updates</li></ul></div>
</div>
</div>
</section>

<section class="fit" aria-label="Who Conviction is for" data-rail="Built for products worth explaining." data-rail-sub="Is it right for you?">
<div><h3>Conviction is for you if</h3><ul><li>Your product needs explaining before people buy it</li><li>You sell a hero product or a small, focused catalog</li><li>You run paid traffic to product pages</li><li>You'd rather earn trust than fake urgency</li></ul></div>
<div class="muted"><h3>Probably not if</h3><ul><li>You sell thousands of SKUs and shoppers mostly browse</li><li>You want a marketplace feel</li><li>Your products sell on the photo alone</li></ul></div>
</section>

<section class="section" data-rail="Support comes from the person who built it." data-rail-sub="A note from the founder">
<div class="founder">
<img src="{IMG}biagio-portrait.jpg" alt="Biagio Mendolia, founder of ConvertCPG" width="960" height="1200" loading="lazy">
<div class="founder__copy">
<div class="kicker">A note from the founder</div>
<blockquote>“I spent ten years rebuilding product pages by hand for Shopify brands. Conviction is that page, built into a theme.”</blockquote>
<p>I ran ecommerce for a Shopify agency, worked on hundreds of brands, and built and sold my own. The pages that sold told a story and kept the buy button close. Now that's the default. When you email support, you get me.</p>
<div class="founder__foot"><div class="sig">Biagio<small>Biagio Mendolia, founder of ConvertCPG</small></div><a href="/about/">Read the full story →</a></div>
</div>
</div>
</section>

<section class="section" style="padding-top:0" data-rail="Docs, support and updates in the open." data-rail-sub="After you buy">
<div class="promise">
<a class="dark" href="/conviction/support/"><h3>Answered by the builder</h3><p>No ticket queue. The person who wrote the code reads your request, within 2 business days.</p><span class="go">Contact support →</span></a>
<a href="/conviction/docs/"><h3>Docs for every setting</h3><p>Every section, block and setting explained in plain language, with a troubleshooting FAQ.</p><span class="go">Read the docs →</span></a>
<a href="/conviction/docs/#version-history"><h3>Updated in the open</h3><p>Free updates. Every release is dated and listed with what changed.</p><span class="go">See the changelog →</span></a>
</div>
</section>

<section class="section" style="padding-top:0" data-rail="Questions before you buy?" data-rail-sub="Straight answers">
<div class="mini-faq">
<div style="display:flex;flex-direction:column;gap:20px"><h2 class="h2">Before you buy.</h2><a href="/conviction/faq/">All questions →</a></div>
<dl>
<dt>When can I buy Conviction?</dt><dd>Conviction is in review for the Shopify Theme Store. Once it's approved, it will be sold there and only there.</dd>
<dt>Will I be able to try it first?</dt><dd>Yes. Shopify lets you add a Theme Store theme to your store and customize it with your own products for free. You pay when you publish.</dd>
<dt>Is it a one-time payment?</dt><dd>Yes. One payment on the Shopify Theme Store, with free updates.</dd>
<dt>Does it work with my apps?</dt><dd>Reviews and bundle apps plug in with app blocks. Shopify Subscriptions, Recharge, Skio, Smartrr and other selling plan apps show in the buy box on their own.</dd>
</dl>
</div>
</section>

<section class="final" data-rail="Coming soon to the Shopify Theme Store." data-rail-sub="Conviction">
<h2>Let your product page make the case.</h2>
<p>Conviction is in review for the Shopify Theme Store.</p>
<div class="buttons" style="justify-content:center"><span class="button button--soon-dark" aria-disabled="true">Coming soon to the Shopify Theme Store</span><a class="button button--light" href="/conviction/docs/">Read the docs</a></div>
</section>
</main>

<div class="site-rail" role="complementary" aria-label="Conviction Rail" aria-hidden="true" inert>
<div><b>You're looking at a Conviction Rail.</b><span>This site runs its own</span></div>
<a href="/conviction/docs/">Read the docs</a>
</div>
"""
    jsonld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"Organization","name":"ConvertCPG",'
              '"legalName":"The Mendolia Group Corp","url":"https://convertcpg.com/","logo":"https://convertcpg.com/assets/convert-cpg.png",'
              '"email":"support@convertcpg.com","founder":{"@type":"Person","name":"Biagio Mendolia"}}</script>\n')
    write("index.html", head("Conviction · A Shopify theme by ConvertCPG",
                             "Conviction is a Shopify theme for brands that teach and sell on the same page. Story sections and the Adaptive Conviction Rail. Coming soon to the Shopify Theme Store.",
                             "/", extra=jsonld) + body + tail())


# ---------------------------------------------------------------- ABOUT
def about():
    cases = [("A", "0.52%", "1.19%", "$27,727 to $47,019"), ("B", "1.4%", "4.31%", "$4,000 to $17,000"), ("C", "3.3%", "4.73%", "$84,150 to $138,924")]
    cs = "".join(f'<div class="case"><small>DTC brand on Shopify · {a}</small><div class="nums"><s>{b}</s><b>{c}</b></div><p>Conversion rate. Monthly revenue from {d}.</p></div>' for a, b, c, d in cases)
    body = f"""{header('about')}
<main id="content">
<section class="section about-hero">
<div style="display:flex;flex-direction:column;gap:26px">
<div class="kicker kicker--plain">About ConvertCPG</div>
<h1>A product page is an argument. I built the theme that makes it.</h1>
<p class="lead">Ten years of building, fixing and rebuilding Shopify stores. Conviction is what I kept building by hand, finally made into a theme.</p>
</div>
<figure class="portrait" style="margin:0">
<img src="{IMG}biagio-portrait.jpg" alt="Biagio Mendolia" width="960" height="1200">
<figcaption><strong>Biagio Mendolia</strong><br><span>Founder, ConvertCPG. Builder of Conviction.</span></figcaption>
</figure>
</section>

<section class="strip" aria-label="Background">
<div><b>10+</b><span>years in ecommerce, since age 16</span></div>
<div><b>100s</b><span>of Shopify brands worked on as an agency ecommerce director</span></div>
<div><b>$150M+</b><span>in online sales for the brands I've worked on</span></div>
<div><b>2</b><span>business days, the most you'll wait for a reply from me</span></div>
</section>

<section class="section letter">
<div>
<div class="kicker kicker--plain" style="margin-bottom:16px">The founder note</div>
<blockquote>“Most themes give your product a price and a button. They don't give it room to make the case.”</blockquote>
<div class="rule" aria-hidden="true"></div>
</div>
<div class="letter__body">
<p>I built my first online store at 16. I've been doing some version of this ever since.</p>
<p>I ran ecommerce for a Shopify agency for three years. Hundreds of brands came through. Supplements, skincare, drinks, gadgets, food. I built a DTC brand of my own and sold it. Today I work with CPG founders on one thing: getting more of the people who land on their store to buy.</p>
<p>Over all those stores, the same thing kept happening. A founder picks a beautiful theme. They load their product. The page looks great and sells badly. There's a gallery, a price and a button, and nowhere to make the argument. What this is. Why it's different. Why it's worth the money. What happens if it doesn't work.</p>
<p>So I'd rebuild the product page by hand. Story first. Proof right next to the claim. Objections answered before anyone asks. A buy button that never leaves the screen and knows what the shopper just read. It worked, over and over, on stores of every size.</p>
<p>Conviction is that page, built into a theme. So you get it without hiring me to rebuild yours.</p>
<p>When you email support, you get me. I'd rather hear what's broken than guess.</p>
<div class="sig" style="padding-top:8px">Biagio<small>Biagio Mendolia, founder</small></div>
</div>
</section>

<section class="section section--tint">
<div class="section-head">
<h2 class="h2" style="max-width:720px;font-size:clamp(32px,3.6vw,48px)">What the approach did before it was a theme.</h2>
<p style="font-size:14px;color:#6B6B68">Client results from my agency and consulting work. Same brand, before and after a product page rebuild. Not results from the Conviction theme.</p>
</div>
<div class="cases">{cs}</div>
</section>

<section class="section values">
<div><small>01</small><h3>Honest pages only</h3><p>No countdown timers. No fake stock counts. Conviction persuades with the product's real story and real proof.</p></div>
<div><small>02</small><h3>Native, not bolted on</h3><p>The Rail, bundle tiers and story sections are built into the theme. No extra app to install, pay for or slow you down.</p></div>
<div><small>03</small><h3>One theme, done well</h3><p>We make one theme. Every update and every support reply goes into making it better.</p></div>
</section>

<section class="cta-band">
<h2>See the page I kept building by hand.</h2>
<div class="buttons"><a class="button button--light" href="/#rail">See how it works</a><a class="button button--outline-light" href="/conviction/support/">Ask me a question</a></div>
</section>
</main>
"""
    write("about/index.html", head("About · ConvertCPG",
                                   "ConvertCPG is Biagio Mendolia: ten years building and rebuilding Shopify stores, now the maker of the Conviction theme.",
                                   "/about/", og_image=IMG + "biagio-portrait.jpg") + body + tail())


# ---------------------------------------------------------------- FAQ
FAQS = [
    ("buying", "When can I buy Conviction?", "Conviction is in review for the Shopify Theme Store. Once it's approved, it will be sold there and only there. Shopify handles the payment and the license."),
    ("buying", "Will I be able to try it before I pay?", "Yes. Shopify lets you add a Theme Store theme to your store and customize it with your own products for free. You only pay when you publish it."),
    ("buying", "Is it a one-time payment?", "Yes. One payment on the Shopify Theme Store, no subscription. Updates are free for as long as you use the theme."),
    ("license", "Can I use it on more than one store?", "Each purchase covers one store. One license covers every market inside that store. For a second store, buy Conviction from that store."),
    ("license", "Can I move it to a new store?", "Shopify allows a transfer when both stores have the same owner and the old store is closed. Contact Shopify Support to start it."),
    ("updates", "How do updates work?", "New versions appear in your theme library. Updates that change settings install as a copy, so you can review before publishing. Every release is listed in the docs with what changed."),
    ("updates", "Will it slow my store down?", "Conviction has no app dependencies, and every release is tested with Lighthouse before it ships. Shopify also checks speed before listing any theme."),
    ("fit", "Is Conviction right for my store?", "It's built for brands with a product worth explaining: supplements, wellness, food and drink, beauty, devices. If you sell thousands of SKUs and shoppers mostly browse, a catalog-first theme will serve you better."),
    ("fit", "Do I need a developer?", "No. Everything is set in the theme editor. The docs walk through every section, and support answers setup questions."),
    ("fit", "Does it work with my apps?", "Reviews, bundles and other apps plug in with app blocks on the product page. Subscriptions from Shopify Subscriptions, Recharge, Skio, Smartrr and any app that uses selling plans show up in the buy box on their own."),
    ("fit", "Can I use my own fonts?", "Conviction uses Shopify’s font library, which works on every device and loads fast. Pick any font there in Theme settings."),
    ("support", "Who answers support?", "The person who built Conviction. We reply within 2 business days, Monday to Friday."),
    ("support", "Can you set it up or customize it for me?", "Yes, as a separate paid service from the same team. It is not part of the theme price."),
]


def faq():
    labels = [("all", "All questions"), ("buying", "Buying"), ("license", "Licensing"), ("updates", "Updates and speed"), ("fit", "Fit and apps"), ("support", "Support")]
    topics = "".join(f'<button type="button" data-topic="{k}" aria-pressed="{"true" if k == "all" else "false"}">{v}</button>' for k, v in labels)
    items = "".join(f'<details data-topics="{t}"{" open" if i == 0 else ""}><summary>{html.escape(q)}</summary><p>{html.escape(a)}'
                    + (' <a href="/services/">See setup and CRO services</a>.' if t == "support" and "customize" in q else "")
                    + '</p></details>' for i, (t, q, a) in enumerate(FAQS))
    body = f"""{header('faq')}
<main id="content">
<section class="support-hero">
<div class="eyebrow">Questions before you buy</div>
<h1 class="display">Straight answers.</h1>
<p class="lead">Buying, licensing, updates and what Conviction works with. Setup how-tos live in the <a href="/conviction/docs/">documentation</a>.</p>
</section>
<section class="section faq-page" style="padding-top:56px">
<div class="topics" role="group" aria-label="Filter by topic"><small>Filter by topic</small>{topics}</div>
<div class="faq faq--big">{items}</div>
</section>
<section class="cta-band" style="background:var(--tint);color:var(--ink)">
<div><h2 style="font-size:clamp(28px,3vw,40px)">Didn't see your question?</h2><p style="margin:8px 0 0;color:#3A3A38">Ask before you buy. The founder answers, within 2 business days.</p></div>
<a class="button" href="/conviction/support/">Ask a question</a>
</section>
</main>
"""
    jsonld = ('<script type="application/ld+json">' +
              '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' +
              ",".join('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (jstr(q), jstr(a)) for _, q, a in FAQS) +
              ']}</script>\n')
    write("conviction/faq/index.html", head("Conviction FAQ · ConvertCPG",
                                            "Straight answers about Conviction, the Shopify theme: buying, licensing, updates, apps and support.",
                                            "/conviction/faq/", extra=jsonld) + body + tail())


def jstr(s):
    import json
    return json.dumps(s)


# ---------------------------------------------------------------- SERVICES
CAL = "https://calendar.google.com/calendar/appointments/schedules/AcZssZ1MlwJUQRLryfM-Jmb5kQ7xuu3ASUg3G94ceDhWId4oDg8nM4r-BFE31bzVqb5iEkl2EhtcKrH4?gv=true"


def services():
    cases = [
        ("Case Study 01", "1.4%", "4.31%", "$69.40", "$85.07", "$4,000/m", "$17,000/m", "Complete conversion-focused rebuild · Clear offer stack · Urgency layering · Proper mobile hierarchy"),
        ("Case Study 02", "3.3%", "4.73%", "$78.04", "$91.00", "$84,150/m", "$138,924/m", "Structured proof · Full PDP restructuring · Clear offer stack · Bundle logic and AOV lift strategy"),
        ("Case Study 03", "0.52%", "1.19%", "$315.45", "$316.79", "$27,727/m", "$47,019/m", "Bundle logic · Trust badges and social proof placement · Clear offer stack · UGC placement · Mobile-first optimization"),
    ]
    cc = "".join(f"""<article class="svc-case"><header><small>{n}</small><span>DTC brand on Shopify</span></header>
<dl><div><dt>CVR</dt><dd><s>{a}</s><b class="big">{b}</b></dd></div><div><dt>AOV</dt><dd><s>{c}</s><b>{d}</b></dd></div><div><dt>Revenue</dt><dd><s>{f}</s><b>{g}</b></dd></div></dl>
<footer><strong>What we changed</strong>{w}</footer></article>""" for n, a, b, c, d, f, g, w in cases)
    shead = f"""<header class="site-header">
<div class="site-header__inner">
<a class="logo" href="/services/"><span class="logo__mark" aria-hidden="true"></span>ConvertCPG</a>
<nav class="site-nav" id="site-nav" aria-label="Main">
<a href="#results">Results</a>
<a href="#process">Process</a>
<a href="#call" data-open-cal>Book a Call</a>
<a class="pill" href="#call" data-open-cal>Book a Free Audit</a>
</nav>
<button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 8h16M4 16h16"></path></svg></button>
</div>
</header>
"""
    body = f"""{shead}
<main id="content">
<section class="svc-hero">
<span class="badge">Certified Shopify Partner</span>
<h1>We Help CPG Brands Increase Shopify Conversion Rates</h1>
<p class="lead" style="margin:0 auto">Website restructuring focused on CVR + AOV lift. Over 10 years of conversion optimization on Shopify.</p>
<a class="button" href="#call" data-open-cal>Book a Free Audit</a>
</section>

<section class="strip strip--3" aria-label="Results in numbers">
<div><b>$150M+</b><span>In online sales for brands</span></div>
<div><b>84%</b><span>Client success rate</span></div>
<div><b>3.12%</b><span>Avg conversion rate for brands</span></div>
</section>

<section class="section" id="results">
<div class="kicker kicker--plain">Proven results</div>
<h2 class="h2" style="margin:14px 0 48px">Case studies</h2>
<div class="svc-cases">{cc}</div>
</section>

<section class="section section--ink" id="process">
<div class="kicker kicker--plain" style="color:var(--sand)">How it works</div>
<h2 class="h2" style="margin:14px 0 48px">Simple 4-Step Process</h2>
<div class="process">
<div><b>01</b><h3>Audit + Revenue Leak Mapping</h3><p>We identify exactly where your store is losing conversions and revenue.</p></div>
<div><b>02</b><h3>Custom Structure Rebuild</h3><p>Your site is restructured for maximum conversion from paid traffic.</p></div>
<div><b>03</b><h3>Offer &amp; Bundle Optimization</h3><p>Strategic offer stacking and bundle logic to lift AOV.</p></div>
<div><b>04</b><h3>30-Day Performance Check</h3><p>We review the data, optimize further, and lock in your results.</p></div>
</div>
</section>

<section class="section audit">
<div style="display:flex;flex-direction:column;gap:18px">
<div class="kicker kicker--plain">Free Audit Prompts</div>
<h2 class="h2" style="font-size:clamp(34px,4vw,54px)">Find your store's leaks in 20 minutes</h2>
<p class="lead">Get the 7-prompt AI CRO audit we run on real CPG stores, free. Plus one store teardown a week. No spam, unsubscribe anytime.</p>
</div>
<div>
<form id="audit-form" action="https://convertcpg-subscribe.convertcpg.workers.dev" method="POST">
<label class="field" style="gap:8px"><span>Email</span><input type="email" name="email" required autocomplete="email" placeholder="you@yourbrand.com"></label>
<button class="button" type="submit">Get the audit</button>
<p>Delivered instantly. Reply with your store URL and we might tear it down on the channel.</p>
</form>
<p id="audit-status" class="form-msg" role="status" hidden style="background:var(--ok-bg);color:var(--ok)"></p>
</div>
</section>

<section class="final" id="call">
<div class="kicker kicker--plain" style="color:var(--sand)">Schedule a call now</div>
<h2 style="font-size:clamp(34px,4.6vw,64px)">Ready to Stop Leaving Revenue on the Table?</h2>
<p style="max-width:680px">Book a free audit call. We'll map your revenue leaks, show you what's broken, and give you a clear plan, whether we work together or not.</p>
<a class="button button--light" href="{CAL}" data-open-cal>Book a Free Audit</a>
<p style="font-size:14px;color:#9A9892">No commitment. No pitch deck. Just value.</p>
</section>
</main>

<dialog class="cal" id="cal" aria-label="Book a free audit">
<header><span>Book a Free Audit</span><button type="button" data-close-cal aria-label="Close">×</button></header>
<iframe title="Book an appointment" data-src="{CAL}"></iframe>
</dialog>
"""
    jsonld = ('<script type="application/ld+json">{"@context":"https://schema.org","@type":"ProfessionalService","name":"ConvertCPG",'
              '"legalName":"The Mendolia Group Corp","url":"https://convertcpg.com/services/","logo":"https://convertcpg.com/assets/convert-cpg.png",'
              '"image":"https://convertcpg.com/og-image.jpg","description":"Shopify conversion rate optimization for CPG brands. Website restructuring that lifts CVR and AOV.",'
              '"serviceType":"Conversion rate optimization for Shopify stores","areaServed":"Worldwide"}</script>\n')
    foot = FOOTER.replace('<a href="/services/">Setup and CRO services</a>', '<a href="/">Conviction, our Shopify theme</a>')
    write("services/index.html", head("ConvertCPG · Shopify Conversion Rate Optimization for CPG Brands",
                                      "Shopify conversion rate optimization for CPG brands. Website restructuring that lifts CVR and AOV. $150M+ in online sales driven. Book a free audit.",
                                      "/services/", og_image="/og-image.jpg", extra=jsonld) + body + foot + "</body>\n</html>\n")


# ---------------------------------------------------------------- SUPPORT (refresh shared chrome)
def support():
    p = ROOT / "conviction/support/index.html"
    s = p.read_text()
    s = re.sub(r'<header class="site-header">.*?</header>\n', lambda m: header("support"), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="site-footer">.*?</footer>\n(<script src="/assets/conviction.js" defer></script>\n)?', lambda m: FOOTER, s, count=1, flags=re.S)
    s = s.replace('<a href="/">See ConvertCPG services →</a>', '<a href="/services/">See setup and CRO services →</a>')
    p.write_text(add_clarity(s))
    print("Refreshed conviction/support/index.html")


if __name__ == "__main__":
    home()
    about()
    faq()
    services()
    support()
