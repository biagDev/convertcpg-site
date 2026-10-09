# Blog sources

One markdown file per post in this folder. `python3 tools/build-blog.py` turns them into
`/blog/<slug>/index.html`, the list at `/blog/`, topic pages at `/blog/topics/<cluster>/`,
the RSS feed at `/blog/feed.xml`, and refreshes the blog entries in `sitemap.xml`.
Commit the generated files; GitHub Pages serves them as-is.

Requires python-markdown (`pip3 install markdown`). Pillow is optional; when present the build
reads local image sizes and writes `width`/`height` on every `<img>`.

## Front matter

```
---
title: The product page that makes the case      # required, also the <h1>
slug: product-page-that-makes-the-case           # required, lowercase-hyphens, final URL /blog/<slug>/
description: One or two sentences, ~150 chars.   # required, meta description and card text
date: 2026-10-14                                 # required, YYYY-MM-DD, publish date
updated: 2026-11-02                              # optional, shown only when it differs from date
tags: [product pages, rail]                      # optional, also accepts a "- item" list
cluster: Product pages                           # required, groups posts into a topic page and "Related"
cover: /assets/blog/my-post/cover.jpg            # optional, hero image and og:image (local path, 1200x630 or wider)
cover_alt: What the cover shows                  # optional but recommended when cover is set
video: dQw4w9WgXcQ                               # optional YouTube id, click-to-load embed above the body
draft: true                                      # optional, drafts are skipped by the build
---
```

## Body

- Start headings at `##`. The title is already the `<h1>`.
- Three or more `##` headings produce a table of contents.
- Standard markdown plus tables, footnotes, fenced code and attribute lists
  (python-markdown `extra`), e.g. `![alt](/assets/blog/x.jpg){: width=1200 height=800 }`.
- Images: put them under `/assets/blog/<slug>/`, keep them under 200 KB, always write alt text.
  Local images get `width`/`height` and `loading="lazy"` automatically.
- Internal links are root-relative (`/conviction/docs/`); the feed makes them absolute.
- Every post needs one original element (data, screenshot, teardown, first-hand opinion).

## Publishing

1. Write the post with `draft: true`, run `python3 tools/build-blog.py`, preview with
   `python3 -m http.server 8000` and open `http://localhost:8000/blog/<slug>/`.
2. Set `draft: false` (or remove the line), set `date` to the publish date, rebuild.
3. Commit the markdown and the generated `blog/` and `sitemap.xml`, then merge to `main`.

Do not rename a slug after publishing; GitHub Pages cannot redirect.

## After publishing
Tell Bing about the new post: `python3 tools/ping-bing.py https://convertcpg.com/blog/<slug>/` (key lives in ~/.convertcpg/bing-webmaster.key, never in git). Google picks it up from the sitemap.
