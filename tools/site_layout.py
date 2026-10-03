"""Shared head, header and footer for the ConvertCPG / Conviction pages."""
import html

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">')

NAV = [
    ("The Rail", "/#rail", "home"),
    ("Demos", "/#demos", "home"),
    ("Docs", "/conviction/docs/", "docs"),
    ("FAQ", "/conviction/faq/", "faq"),
    ("Support", "/conviction/support/", "support"),
    ("About", "/about/", "about"),
]


def head(title, description, path, og_image="/assets/conviction/img/sowfield-hero.jpg", extra=""):
    url = "https://convertcpg.com" + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ConvertCPG">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://convertcpg.com{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAFAF7">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="/assets/conviction.css">
{extra}</head>
<body>
<a class="skip" href="#content">Skip to content</a>
"""


def header(active=None, cta=("Read the docs", "/conviction/docs/")):
    links = []
    for label, href, key in NAV:
        cur = ' aria-current="page"' if key == active and not href.startswith("/#") else ""
        links.append(f'<a href="{href}"{cur}>{label}</a>')
    return f"""<header class="site-header">
<div class="site-header__inner">
<a class="logo" href="/"><span class="logo__mark" aria-hidden="true"></span>ConvertCPG</a>
<nav class="site-nav" id="site-nav" aria-label="Main">
{chr(10).join(links)}
<a class="pill" href="{cta[1]}">{cta[0]}</a>
</nav>
<button class="menu-toggle" type="button" aria-label="Menu" aria-expanded="false" aria-controls="site-nav"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 8h16M4 16h16"></path></svg></button>
</div>
</header>
"""


FOOTER = """<footer class="site-footer">
<div class="site-footer__top">
<div><div class="site-footer__brand">ConvertCPG</div><div>Makers of Conviction, a Shopify theme for brands that teach and sell on the same page.</div></div>
<div class="site-footer__links">
<a href="/">Conviction</a>
<a href="/conviction/docs/">Documentation</a>
<a href="/conviction/faq/">FAQ</a>
<a href="/conviction/support/">Support</a>
<a href="/about/">About</a>
<a href="/services/">Setup and CRO services</a>
</div>
</div>
<div class="site-footer__bottom"><span>© 2026 The Mendolia Group Corp. ConvertCPG is a Shopify Partner.</span><a href="mailto:support@convertcpg.com">support@convertcpg.com</a></div>
</footer>
<script src="/assets/conviction.js" defer></script>
"""


def tail():
    return FOOTER + "</body>\n</html>\n"
