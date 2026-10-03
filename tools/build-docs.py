#!/usr/bin/env python3
"""Build conviction/docs/index.html from Keystone's conviction-theme-docs.md.

Usage: python3 tools/build-docs.py /path/to/conviction-theme-docs.md
Re-run whenever the docs change, then commit the HTML.
"""
import html
import re
import sys
from pathlib import Path

SUPPORT_URL = "/conviction/support/"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "conviction" / "docs" / "index.html"

GUIDE_BLURBS = {
    1: "Install, pick the Conviction or Alloy preset, and the five first steps.",
    2: "Colors, typography, layout, cart, search, social links and rail defaults.",
    3: "Hero blocks, variant styles, swatches, bundle tiers, subscriptions, pickup, gift cards.",
    4: "How it behaves, default and per-section messages, button labels, colors.",
    5: "15 modules, section buttons, starter stories, a different story per product.",
    6: "Heroes, editorial, commerce, content and utility sections.",
    7: "Filters, the phone filter panel and complementary products.",
    8: "App blocks, Custom Liquid and Follow on Shop.",
    9: "Translate theme text with Edit translations or Translate & Adapt.",
    10: "Answers to the questions merchants ask most.",
}


SEEN = set()


def slug(text):
    text = re.sub(r"^\d+\.\s*", "", text)
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    sid, n = base, 2
    while sid in SEEN:
        sid, n = f"{base}-{n}", n + 1
    SEEN.add(sid)
    return sid


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = text.replace("SUPPORT_URL", SUPPORT_URL)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def convert(md):
    lines = md.splitlines()
    out, toc, i = [], [], 0
    title = lines[0].lstrip("# ").strip()
    i = 1
    intro = []
    in_faq = False
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("## "):
            text = s[3:].strip()
            sid = slug(text)
            m = re.match(r"^(\d+)\.\s*(.*)", text)
            if m:
                toc.append((int(m.group(1)), m.group(2), sid))
            if in_faq:
                out.append("</div>")
            in_faq = sid == "faq"
            out.append(f'<h2 id="{sid}">{inline(text)}<a class="anchor" href="#{sid}" aria-label="Link to {html.escape(text)}">#</a></h2>')
            if in_faq:
                out.append('<div class="faq">')
            i += 1
            continue
        if s.startswith("### "):
            text = s[4:].strip()
            sid = slug(text)
            out.append(f'<h3 id="{sid}">{inline(text)}<a class="anchor" href="#{sid}" aria-label="Link to {html.escape(text)}">#</a></h3>')
            i += 1
            continue
        if s.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
            head, body = cells[0], [r for r in cells[2:]]
            t = ['<div class="table-wrap" role="region" tabindex="0" aria-label="Table"><table><thead><tr>']
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t))
            continue
        if re.match(r"^(-|\d+\.)\s", s):
            ordered = bool(re.match(r"^\d+\.", s))
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines) and re.match(r"^(-|\d+\.)\s", lines[i].strip()):
                items.append(re.sub(r"^(-|\d+\.)\s+", "", lines[i].strip()))
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||-\s|\d+\.\s|---)", lines[i].strip()):
            para.append(lines[i].strip())
            i += 1
        if in_faq and len(para) >= 2 and para[0].startswith("**") and para[0].endswith("**"):
            q = para[0].strip("*")
            a = " ".join(para[1:])
            out.append(f"<details><summary>{inline(q)}</summary><p>{inline(a)}</p></details>")
        elif not toc and not out:
            intro.append(inline(" ".join(para)))
        else:
            out.append(f"<p>{inline(' '.join(para))}</p>")
    if in_faq:
        out.append("</div>")
    return title, intro, toc, "\n".join(out)


def page(title, intro, toc, body):
    guide_cards = []
    for n, name, sid in toc:
        cls = "guide guide--dark" if n == 1 else ("guide guide--sand" if "Rail" in name else "guide")
        label = f"{n:02d} · Start here" if n == 1 else (f"{n:02d} · Signature feature" if "Rail" in name else f"{n:02d}")
        guide_cards.append(
            f'<a class="{cls}" href="#{sid}"><span class="guide__n">{label}</span>'
            f'<span class="guide__t">{html.escape(name)}</span>'
            f'<span class="guide__d">{html.escape(GUIDE_BLURBS.get(n, ""))}</span></a>'
        )
    toc_items = "".join(f'<li><a href="#{sid}">{n}. {html.escape(name)}</a></li>' for n, name, sid in toc)
    intro_html = " ".join(intro)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Conviction theme documentation · ConvertCPG</title>
<meta name="description" content="Documentation for Conviction, the Shopify theme by ConvertCPG: setup, theme settings, the product page, the Adaptive Conviction Rail, story sections and FAQ.">
<link rel="canonical" href="https://convertcpg.com/conviction/docs/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ConvertCPG">
<meta property="og:title" content="Conviction theme documentation">
<meta property="og:description" content="Everything the Conviction Shopify theme can do, and how to set it up.">
<meta property="og:url" content="https://convertcpg.com/conviction/docs/">
<meta name="theme-color" content="#FAFAF7">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/assets/conviction.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header class="site-header">
<div class="site-header__inner">
<a class="logo" href="/"><span class="logo__mark" aria-hidden="true"></span>ConvertCPG</a>
<nav class="site-nav" aria-label="Main">
<a href="/conviction/docs/" aria-current="page">Docs</a>
<a href="/conviction/support/">Support</a>
<a class="pill" href="/conviction/support/">Contact support</a>
</nav>
</div>
</header>

<main id="content">
<section class="docs-hero">
<div class="eyebrow">Conviction documentation · v1.0.0</div>
<h1 class="display">{html.escape(title).replace("Conviction theme documentation", "Everything the theme can do,<br>and how to set it up.")}</h1>
<p class="lead">{intro_html}</p>
<div class="docs-search" role="search">
<label class="docs-search__box"><span class="visually-hidden">Search the docs</span>
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#6B6B68" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
<input type="search" id="docs-q" placeholder="Search: rail, swatches, bundles, subscriptions" autocomplete="off" aria-controls="docs-results" aria-expanded="false">
</label>
<div class="docs-search__results" id="docs-results" hidden></div>
</div>
<div class="popular">Popular:
<a href="#setting-the-messages">Rail messages</a>
<a href="#bundle-tiers-multipacks">Bundle tiers</a>
<a href="#color-swatches">Color swatches</a>
<a href="#subscriptions-and-purchase-options">Subscriptions</a>
</div>
</section>

<section class="guides" aria-labelledby="guides-title">
<h2 id="guides-title">Guides</h2>
<div class="guides__grid">
{chr(10).join(guide_cards)}
</div>
</section>

<div class="docs-layout">
<nav class="toc" aria-label="On this page">
<div class="toc__title">On this page</div>
<ol>{toc_items}</ol>
<div class="toc__help">Stuck? <a href="/conviction/support/">Contact support</a>. Include your store URL and a screenshot. We reply within 2 business days.</div>
</nav>
<article class="prose" id="docs">
{body}
<div class="callout">
<div><h2>Still stuck?</h2><p>The person who built Conviction answers, within 2 business days.</p></div>
<a class="button" href="/conviction/support/">Contact support</a>
</div>
</article>
</div>
</main>

<footer class="site-footer">
<div class="site-footer__top">
<div><div class="site-footer__brand">ConvertCPG</div><div>Makers of Conviction, a Shopify theme for brands that teach and sell on the same page.</div></div>
<div class="site-footer__links"><a href="/conviction/docs/">Documentation</a><a href="/conviction/support/">Support</a><a href="/">ConvertCPG</a></div>
</div>
<div class="site-footer__bottom"><span>© 2026 The Mendolia Group Corp. ConvertCPG is a Shopify Partner.</span><a href="mailto:support@convertcpg.com">support@convertcpg.com</a></div>
</footer>

<script>
(function () {{
  var q = document.getElementById('docs-q');
  var box = document.getElementById('docs-results');
  var heads = Array.prototype.slice.call(document.querySelectorAll('#docs h2[id], #docs h3[id]'));
  var index = heads.map(function (h) {{
    var text = '', n = h.nextElementSibling;
    while (n && !/^H[23]$/.test(n.tagName)) {{ text += ' ' + n.textContent; n = n.nextElementSibling; }}
    var parent = h;
    if (h.tagName === 'H3') {{ parent = h.previousElementSibling; while (parent && parent.tagName !== 'H2') parent = parent.previousElementSibling; }}
    return {{ id: h.id, title: h.textContent.replace(/#$/, ''), section: parent && parent !== h ? parent.textContent.replace(/#$/, '') : '', body: text.toLowerCase() }};
  }});
  function esc(s) {{ return s.replace(/[&<>"]/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}
  function close() {{ box.hidden = true; q.setAttribute('aria-expanded', 'false'); }}
  q.addEventListener('input', function () {{
    var term = q.value.trim().toLowerCase();
    if (term.length < 2) {{ close(); return; }}
    var hits = index.filter(function (e) {{ return e.title.toLowerCase().indexOf(term) > -1 || e.body.indexOf(term) > -1; }})
      .sort(function (a, b) {{ return (b.title.toLowerCase().indexOf(term) > -1) - (a.title.toLowerCase().indexOf(term) > -1); }})
      .slice(0, 8);
    box.innerHTML = hits.length ? hits.map(function (h) {{
      return '<a href="#' + h.id + '">' + esc(h.title) + (h.section ? '<small>' + esc(h.section) + '</small>' : '') + '</a>';
    }}).join('') : '<div class="docs-search__empty">No match. Try another word, or <a href="/conviction/support/">ask support</a>.</div>';
    box.hidden = false; q.setAttribute('aria-expanded', 'true');
  }});
  box.addEventListener('click', function (e) {{ if (e.target.closest('a')) {{ close(); q.value = ''; }} }});
  document.addEventListener('keydown', function (e) {{ if (e.key === 'Escape') close(); }});
  document.addEventListener('click', function (e) {{ if (!e.target.closest('.docs-search')) close(); }});

  var links = Array.prototype.slice.call(document.querySelectorAll('.toc a'));
  if ('IntersectionObserver' in window && links.length) {{
    var map = {{}};
    links.forEach(function (a) {{ map[a.getAttribute('href').slice(1)] = a; }});
    var io = new IntersectionObserver(function (entries) {{
      entries.forEach(function (en) {{
        if (en.isIntersecting && map[en.target.id]) {{
          links.forEach(function (a) {{ a.classList.remove('is-active'); }});
          map[en.target.id].classList.add('is-active');
        }}
      }});
    }}, {{ rootMargin: '-20% 0px -70% 0px' }});
    Object.keys(map).forEach(function (id) {{ var el = document.getElementById(id); if (el) io.observe(el); }});
  }}

  if (location.hash === '' ) return;
  var target = document.getElementById(location.hash.slice(1));
  if (target && target.closest('details')) target.closest('details').open = true;
}})();
</script>
</body>
</html>
"""


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    if not src or not src.exists():
        sys.exit("Usage: python3 tools/build-docs.py /path/to/conviction-theme-docs.md")
    title, intro, toc, body = convert(src.read_text())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out = page(title, intro, toc, body)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from site_layout import header, FOOTER, add_clarity
    out = re.sub(r'<header class="site-header">.*?</header>\n', lambda m: header("docs"), out, count=1, flags=re.S)
    out = re.sub(r'<footer class="site-footer">.*?</footer>\n', lambda m: FOOTER, out, count=1, flags=re.S)
    OUT.write_text(add_clarity(out))
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(toc)} sections)")


if __name__ == "__main__":
    main()
