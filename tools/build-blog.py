#!/usr/bin/env python3
"""Build the ConvertCPG blog from markdown posts in blog-src/.

Writes:
  blog/<slug>/index.html        one page per published post
  blog/index.html               the list, newest first
  blog/topics/<cluster>/        one hub page per cluster (only when it has posts)
  blog/feed.xml                 RSS 2.0 with full HTML content
  sitemap.xml                   blog URLs added or refreshed; other URLs untouched

Posts with `draft: true` are skipped. Front matter is described in blog-src/README.md.

Usage: python3 tools/build-blog.py
"""
import datetime as dt
import email.utils
import html
import json
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("python-markdown is required: pip3 install markdown")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from site_layout import head, header, tail  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "blog-src"
OUT = ROOT / "blog"
SITE = "https://convertcpg.com"
ORG_ID = SITE + "/#org"
PERSON_ID = SITE + "/about/#person"
AUTHOR = "Biagio Mendolia"
PORTRAIT = "/assets/conviction/img/biagio-portrait.jpg"
DEFAULT_OG = "/assets/conviction/img/sowfield-hero.jpg"
BLOG_CSS = '<link rel="stylesheet" href="/assets/blog.css">\n'
FEED_LINK = '<link rel="alternate" type="application/rss+xml" title="ConvertCPG blog" href="/blog/feed.xml">\n'
REQUIRED = ("title", "slug", "description", "date", "cluster")

e = html.escape


# ---------------------------------------------------------------- front matter
def parse_front_matter(text, name):
    """Minimal YAML-ish parser: `key: value`, inline [a, b] lists, and `- item` lists."""
    if not text.startswith("---"):
        sys.exit(f"{name}: missing front matter")
    try:
        _, fm, body = text.split("---", 2)
    except ValueError:
        sys.exit(f"{name}: front matter not closed")
    meta, key = {}, None
    for raw in fm.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.lstrip().startswith("- ") and key:
            meta.setdefault(key, [])
            if not isinstance(meta[key], list):
                meta[key] = []
            meta[key].append(raw.strip()[2:].strip().strip('"\''))
            continue
        if ":" not in raw:
            sys.exit(f"{name}: cannot parse front matter line: {raw!r}")
        key, val = raw.split(":", 1)
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            meta[key] = [v.strip().strip('"\'') for v in val[1:-1].split(",") if v.strip()]
        elif val == "":
            meta[key] = []  # list follows on the next lines
        else:
            meta[key] = val.strip('"\'')
    return meta, body.lstrip("\n")


def as_list(v):
    if isinstance(v, list):
        return v
    return [x.strip() for x in str(v).split(",") if x.strip()] if v else []


def as_bool(v):
    return str(v).strip().lower() in ("true", "yes", "1")


def parse_date(s, name, field):
    try:
        return dt.date.fromisoformat(str(s).strip())
    except ValueError:
        sys.exit(f"{name}: {field} must be YYYY-MM-DD, got {s!r}")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def human(d):
    return d.strftime("%B %-d, %Y")


def rfc822(d):
    return email.utils.format_datetime(dt.datetime(d.year, d.month, d.day, 9, 0, tzinfo=dt.timezone.utc))


# ---------------------------------------------------------------- images
def image_size(src):
    """(width, height) for a local image, or None."""
    if not src.startswith("/"):
        return None
    p = ROOT / src.lstrip("/")
    if not p.is_file():
        return None
    try:
        from PIL import Image
        with Image.open(p) as im:
            return im.size
    except Exception:
        return None


def fix_images(body_html, name):
    """Add width/height (when the file is local), loading=lazy and decoding=async to every <img>."""
    def fix(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]*)"', tag)
        if src and ('width="' not in tag or 'height="' not in tag):
            size = image_size(src.group(1))
            if size:
                tag = tag.replace("<img", f'<img width="{size[0]}" height="{size[1]}"', 1)
            else:
                print(f"  warning: {name}: no width/height for image {src.group(1)}")
        if 'loading="' not in tag:
            tag = tag.replace("<img", '<img loading="lazy"', 1)
        if 'decoding="' not in tag:
            tag = tag.replace("<img", '<img decoding="async"', 1)
        if 'alt="' not in tag:
            print(f"  warning: {name}: image without alt: {tag[:80]}")
        return tag
    return re.sub(r"<img\b[^>]*>", fix, body_html)


# ---------------------------------------------------------------- posts
def load_posts():
    posts = []
    for path in sorted(SRC.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"), path.name)
        if as_bool(meta.get("draft", "false")):
            print(f"Skipping draft {path.name}")
            continue
        missing = [k for k in REQUIRED if not meta.get(k)]
        if missing:
            sys.exit(f"{path.name}: missing front matter: {', '.join(missing)}")
        slug = str(meta["slug"]).strip("/")
        if slug != slugify(slug) or "/" in slug:
            sys.exit(f"{path.name}: slug must be lowercase letters, digits and hyphens: {slug!r}")
        date = parse_date(meta["date"], path.name, "date")
        updated = parse_date(meta["updated"], path.name, "updated") if meta.get("updated") else date
        if updated < date:
            sys.exit(f"{path.name}: updated is before date")
        md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"],
                               extension_configs={"toc": {"toc_depth": "2-3", "permalink": False}})
        body_html = md.convert(body)
        if "<h1" in body_html:
            print(f"  warning: {path.name}: body has an <h1>; the title is already the h1, start at ##")
        body_html = fix_images(body_html, path.name)
        words = len(re.sub(r"<[^>]+>", " ", body_html).split())
        posts.append({
            "file": path.name, "title": str(meta["title"]), "slug": slug,
            "description": str(meta["description"]), "date": date, "updated": updated,
            "tags": as_list(meta.get("tags")), "cluster": str(meta["cluster"]),
            "cluster_slug": slugify(str(meta["cluster"])),
            "cover": meta.get("cover") or "", "cover_alt": meta.get("cover_alt") or "",
            "video": meta.get("video") or "", "html": body_html,
            "toc": [t for t in md.toc_tokens if t["level"] == 2],
            "url": f"/blog/{slug}/", "words": words,
        })
    slugs = [p["slug"] for p in posts]
    dupes = {s for s in slugs if slugs.count(s) > 1}
    if dupes:
        sys.exit(f"duplicate slugs: {', '.join(sorted(dupes))}")
    posts.sort(key=lambda p: (p["date"], p["slug"]), reverse=True)
    return posts


# ---------------------------------------------------------------- rendering
def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    print("Wrote", path)


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>\n"


def card(p):
    return (f'<li class="post-card"><div class="post-card__meta"><time datetime="{p["date"].isoformat()}">{human(p["date"])}</time>'
            f'<a class="tag" href="/blog/topics/{p["cluster_slug"]}/">{e(p["cluster"])}</a></div>'
            f'<h2><a href="{p["url"]}">{e(p["title"])}</a></h2><p>{e(p["description"])}</p></li>')


def cluster_links(posts, current=None):
    clusters = {}
    for p in posts:
        clusters.setdefault(p["cluster_slug"], p["cluster"])
    if not clusters:
        return ""
    all_cur = ' aria-current="page"' if current is None else ""
    links = [f'<a href="/blog/"{all_cur}>All posts</a>']
    for cs, name in sorted(clusters.items(), key=lambda kv: kv[1].lower()):
        cur = ' aria-current="page"' if cs == current else ""
        links.append(f'<a href="/blog/topics/{cs}/"{cur}>{e(name)}</a>')
    return '<nav class="clusters" aria-label="Filter by topic">' + "".join(links) + "</nav>"


def list_page(all_posts, shown, title, path, heading, lead, current=None):
    items = "".join(card(p) for p in shown)
    body = (f'<ul class="post-list">{items}</ul>' if shown
            else '<p class="post-empty">First posts coming soon. Until then, <a href="/conviction/docs/">read the Conviction docs</a>.</p>')
    page = f"""{header('blog')}
<main id="content">
<section class="blog-hero">
<div class="kicker kicker--plain">{'Blog' if current is None else 'Blog · Topic'}</div>
<h1 class="display" style="font-size:clamp(36px,5vw,60px)">{e(heading)}</h1>
<p class="lead">{e(lead)}</p>
</section>
<section class="blog-wrap"><div class="blog-inner blog-inner--wide">
{cluster_links(all_posts, current)}
{body}
</div></section>
</main>
"""
    extra = BLOG_CSS + FEED_LINK
    if current is None:
        extra += jsonld({"@context": "https://schema.org", "@type": "Blog", "@id": SITE + "/blog/#blog",
                         "name": "ConvertCPG Blog", "url": SITE + "/blog/",
                         "description": lead, "publisher": {"@id": ORG_ID}})
    write(path, head(title, lead, "/" + path.replace("index.html", ""), extra=extra) + page + tail())


def lite_youtube(video_id, title):
    vid = e(video_id)
    return (f'<div class="lite-yt" data-id="{vid}">'
            f'<button type="button" aria-label="Play video: {e(title)}">'
            f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" width="480" height="360" alt="" loading="lazy" decoding="async">'
            f'<span class="lite-yt__play" aria-hidden="true"></span></button></div>')


LITE_YT_JS = """<script>
document.querySelectorAll('.lite-yt button').forEach(function(b){b.addEventListener('click',function(){var w=b.parentNode,f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+w.dataset.id+'?autoplay=1&rel=0';f.title=b.getAttribute('aria-label').replace('Play video: ','');f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';f.allowFullscreen=true;w.replaceChild(f,b);});});
</script>
"""


def post_page(p, posts):
    url = SITE + p["url"]
    crumbs = ('<ol class="crumbs"><li><a href="/">Home</a></li><li><a href="/blog/">Blog</a></li>'
              f'<li aria-current="page">{e(p["title"])}</li></ol>')
    meta = (f'<div class="post-meta"><a href="/about/">{AUTHOR}</a>'
            f'<span>Published <time datetime="{p["date"].isoformat()}">{human(p["date"])}</time></span>')
    if p["updated"] != p["date"]:
        meta += f'<span>Updated <time datetime="{p["updated"].isoformat()}">{human(p["updated"])}</time></span>'
    meta += f'<a class="tag" href="/blog/topics/{p["cluster_slug"]}/">{e(p["cluster"])}</a></div>'

    cover = ""
    if p["cover"]:
        size = image_size(p["cover"])
        dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
        if not size:
            print(f"  warning: {p['file']}: cover has no local size: {p['cover']}")
        cover = f'<figure class="post-cover"><img src="{e(p["cover"])}" alt="{e(p["cover_alt"])}"{dims} fetchpriority="high" decoding="async"></figure>'

    toc = ""
    if len(p["toc"]) >= 3:
        toc = ('<details class="post-toc" open><summary>In this post</summary><ol>'
               + "".join(f'<li><a href="#{t["id"]}">{t["html"]}</a></li>' for t in p["toc"]) + "</ol></details>")

    video = lite_youtube(p["video"], p["title"]) if p["video"] else ""

    related = [q for q in posts if q["cluster_slug"] == p["cluster_slug"] and q["slug"] != p["slug"]][:3]
    related_html = ""
    if related:
        related_html = (f'<section class="related" aria-labelledby="related-h"><h2 id="related-h">More on {e(p["cluster"])}</h2>'
                        '<ul class="post-list">' + "".join(card(q) for q in related) + "</ul></section>")

    author = (f'<div class="author"><img src="{PORTRAIT}" alt="" width="64" height="64" loading="lazy" decoding="async">'
              f'<div><b>{AUTHOR}, founder of ConvertCPG</b>'
              '<span>Ten years building and rebuilding Shopify stores. Maker of the Conviction theme. '
              '<a href="/about/">About Biagio →</a></span></div></div>')
    docs_card = ('<a class="docs-card" href="/conviction/docs/"><div><b>Built on Conviction? Read the docs.</b>'
                 '<span>Every section, block and setting explained in plain language.</span></div><span class="go">Open the docs →</span></a>')

    page = f"""{header('blog')}
<main id="content">
<article class="post">
<header class="post-head"><div class="blog-inner">
{crumbs}
<h1 class="post-title">{e(p["title"])}</h1>
<p class="post-dek">{e(p["description"])}</p>
{meta}
{cover}
{toc}
</div></header>
<div class="blog-wrap"><div class="blog-inner">
<div class="prose post-body">
{video}{p["html"]}
</div>
<footer class="post-foot">
{author}
{docs_card}
</footer>
{related_html}
</div></div>
</article>
</main>
{LITE_YT_JS if p["video"] else ""}"""

    article = {
        "@context": "https://schema.org", "@type": "BlogPosting", "@id": url + "#post",
        "mainEntityOfPage": url, "headline": p["title"], "description": p["description"],
        "datePublished": p["date"].isoformat(), "dateModified": p["updated"].isoformat(),
        "author": {"@type": "Person", "@id": PERSON_ID, "name": AUTHOR, "url": SITE + "/about/"},
        "publisher": {"@type": "Organization", "@id": ORG_ID, "name": "ConvertCPG"},
        "url": url, "inLanguage": "en", "articleSection": p["cluster"], "wordCount": p["words"],
        "isPartOf": {"@id": SITE + "/blog/#blog"},
    }
    if p["tags"]:
        article["keywords"] = ", ".join(p["tags"])
    if p["cover"]:
        article["image"] = SITE + p["cover"]
    if p["video"]:
        article["video"] = {"@type": "VideoObject", "name": p["title"], "description": p["description"],
                            "thumbnailUrl": f"https://i.ytimg.com/vi/{p['video']}/hqdefault.jpg",
                            "uploadDate": p["date"].isoformat(),
                            "embedUrl": f"https://www.youtube-nocookie.com/embed/{p['video']}"}
    crumbs_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": p["title"], "item": url},
    ]}
    og_extra = (f'<meta property="article:published_time" content="{p["date"].isoformat()}">\n'
                f'<meta property="article:modified_time" content="{p["updated"].isoformat()}">\n'
                f'<meta property="article:author" content="{SITE}/about/">\n'
                f'<meta property="article:section" content="{e(p["cluster"])}">\n'
                + "".join(f'<meta property="article:tag" content="{e(t)}">\n' for t in p["tags"])
                + f'<meta name="author" content="{AUTHOR}">\n')
    extra = BLOG_CSS + FEED_LINK + og_extra + jsonld(article) + jsonld(crumbs_ld)
    page_head = head(f'{p["title"]} | ConvertCPG', p["description"], p["url"],
                     og_image=p["cover"] or DEFAULT_OG, extra=extra)
    page_head = page_head.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">', 1)
    write(f"blog/{p['slug']}/index.html", page_head + page + tail())


# ---------------------------------------------------------------- feed
def absolutize(h):
    return re.sub(r'(src|href)="/(?!/)', rf'\1="{SITE}/', h)


def feed(posts):
    items = []
    for p in posts:
        url = SITE + p["url"]
        content = p["html"]
        if p["video"]:
            content = f'<p><a href="https://www.youtube.com/watch?v={e(p["video"])}">Watch the video</a></p>' + content
        content = absolutize(content)
        items.append(
            "<item>\n"
            f"<title>{e(p['title'])}</title>\n<link>{url}</link>\n<guid isPermaLink=\"true\">{url}</guid>\n"
            f"<pubDate>{rfc822(p['date'])}</pubDate>\n<dc:creator>{AUTHOR}</dc:creator>\n"
            f"<category>{e(p['cluster'])}</category>\n"
            + "".join(f"<category>{e(t)}</category>\n" for t in p["tags"])
            + f"<description>{e(p['description'])}</description>\n"
            f"<content:encoded><![CDATA[{content.replace(']]>', ']]]]><![CDATA[>')}]]></content:encoded>\n"
            "</item>")
    last = rfc822(max([p["updated"] for p in posts], default=dt.date.today()))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
           "<channel>\n<title>ConvertCPG Blog</title>\n"
           f"<link>{SITE}/blog/</link>\n"
           f'<atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>\n'
           "<description>Shopify conversion for CPG brands: product pages, teardowns and the Conviction theme, from Biagio Mendolia.</description>\n"
           f"<language>en</language>\n<lastBuildDate>{last}</lastBuildDate>\n"
           + "\n".join(items) + ("\n" if items else "")
           + "</channel>\n</rss>\n")
    write("blog/feed.xml", xml)


# ---------------------------------------------------------------- sitemap
def sitemap(posts, clusters):
    path = ROOT / "sitemap.xml"
    xml = path.read_text(encoding="utf-8")
    # Drop every existing blog entry (ours to manage); leave all other <url> blocks byte for byte.
    xml = re.sub(r"\s*<url>(?:(?!</url>).)*?<loc>https://convertcpg\.com/blog/(?:(?!</url>).)*?</url>", "", xml, flags=re.S)
    entries = []
    if posts:
        newest = max(p["updated"] for p in posts)
        entries.append(f"  <url><loc>{SITE}/blog/</loc><lastmod>{newest.isoformat()}</lastmod><changefreq>weekly</changefreq></url>")
    else:
        entries.append(f"  <url><loc>{SITE}/blog/</loc><changefreq>weekly</changefreq></url>")
    for cs in sorted(clusters):
        newest = max(p["updated"] for p in posts if p["cluster_slug"] == cs)
        entries.append(f"  <url><loc>{SITE}/blog/topics/{cs}/</loc><lastmod>{newest.isoformat()}</lastmod><changefreq>weekly</changefreq></url>")
    for p in posts:
        entries.append(f"  <url><loc>{SITE}{p['url']}</loc><lastmod>{p['updated'].isoformat()}</lastmod></url>")
    xml = xml.rstrip()
    assert xml.endswith("</urlset>"), "sitemap.xml: expected </urlset> at the end"
    xml = xml[: -len("</urlset>")].rstrip("\n") + "\n" + "\n".join(entries) + "\n</urlset>\n"
    path.write_text(xml, encoding="utf-8")
    print("Updated sitemap.xml")


# ---------------------------------------------------------------- main
def main():
    if not SRC.is_dir():
        sys.exit(f"missing {SRC}")
    posts = load_posts()
    # Clean generated output so removed or renamed posts do not linger.
    if OUT.exists():
        shutil.rmtree(OUT)
    lead = "Shopify conversion for CPG brands: product pages, teardowns and what we learn building Conviction."
    list_page(posts, posts, "Blog | ConvertCPG", "blog/index.html", "Notes on pages that sell.", lead)
    clusters = {}
    for p in posts:
        clusters.setdefault(p["cluster_slug"], p["cluster"])
    for cs, name in clusters.items():
        shown = [p for p in posts if p["cluster_slug"] == cs]
        list_page(posts, shown, f"{name} | ConvertCPG Blog", f"blog/topics/{cs}/index.html", name,
                  f"Posts about {name.lower()} from the ConvertCPG blog.", current=cs)
    for p in posts:
        post_page(p, posts)
    feed(posts)
    sitemap(posts, clusters)
    print(f"Built {len(posts)} post(s), {len(clusters)} topic page(s).")


if __name__ == "__main__":
    main()
