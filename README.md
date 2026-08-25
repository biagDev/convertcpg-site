# convertcpg.com

Marketing site for **ConvertCPG** (The Mendolia Group Corp) — Shopify conversion rate
optimization for CPG brands.

Static site, no build step required to serve. Hosted on GitHub Pages at
<https://convertcpg.com>.

## Layout

```
index.html          the whole page (inline CSS, ~70KB)
assets/             images, Inter font subsets, React + page runtime
CNAME               custom domain for GitHub Pages
.nojekyll           serve files as-is, skip Jekyll processing
favicon.* / apple-touch-icon.png / icon-512.png / site.webmanifest
og-image.jpg        1200x630 social share card
robots.txt, sitemap.xml
tools/build.mjs     regenerates index.html + assets/ from a Claude Design export
```

Everything the page needs is served from this repo — there are no CDN or Google Fonts
requests at runtime. React and the Inter subsets are vendored into `assets/`.

## Deploying

Pushing to `main` publishes automatically via GitHub Pages. There is no CI step.

## Updating the design

The page is authored in Claude Design. To pull in a new version:

1. Export the design as **standalone HTML** (a single self-extracting file).
2. Rebuild:

```bash
node tools/build.mjs "/path/to/ConvertCPG Site (standalone).html" .
```

That rewrites `index.html` and repopulates `assets/`. It unpacks the export's embedded
resource manifest to real files, gives them readable names from their `alt` text,
de-duplicates identical images, and re-injects the SEO/Open Graph `<head>`.

Icons and `og-image.jpg` are committed artwork — the build leaves them alone. Regenerate
them by hand if the branding changes.

3. Check it locally, then commit:

```bash
python3 -m http.server 8000
```
