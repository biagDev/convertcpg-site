#!/usr/bin/env node
// Rebuild the site from a Claude Design standalone export.
//   node tools/build.mjs "/path/to/Export (standalone).html" .
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';
import crypto from 'node:crypto';

const SRC = process.argv[2];
const ROOT = process.argv[3] || process.cwd();
const OUT = ROOT;
const GEN = ROOT;
const DOMAIN = 'convertcpg.com';
const ORIGIN = 'https://' + DOMAIN;

const html = fs.readFileSync(SRC, 'utf8');
const island = (t) => {
  const m = html.match(new RegExp('<script type="__bundler/' + t + '">([\\s\\S]*?)</script>', 'i'));
  if (!m) throw new Error('missing ' + t);
  return JSON.parse(m[1].trim());
};
const manifest = island('manifest');
const ext = island('ext_resources');
let template = island('template');

fs.rmSync(path.join(OUT,'assets'), { recursive: true, force: true });
fs.mkdirSync(path.join(OUT, 'assets'), { recursive: true });

const EXTOF = { 'image/png':'png','image/jpeg':'jpg','image/gif':'gif','image/webp':'webp',
  'image/svg+xml':'svg','font/woff2':'woff2','font/woff':'woff','application/javascript':'js',
  'text/javascript':'js','text/css':'css','application/json':'json' };
const slug = s => s.toLowerCase().replace(/['’]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,48);

// ---- name resolution -------------------------------------------------
const names = {};                                   // uuid -> basename
for (const e of ext) {                              // CDN libs: react.js, react-dom.js
  const base = e.id.split('/').pop().replace(/\.(production|development)\.min\.js$/,'.js');
  names[e.uuid] = base.replace(/@[\d.]+/,'');
}
for (const m of template.matchAll(/\/\*\s*([\w-]+)\s*\*\/\s*@font-face\s*\{[^}]*url\("([0-9a-f-]{36})"\)/g))
  names[m[2]] ??= 'inter-' + m[1] + '.woff2';       // font subsets by their CSS comment
for (const m of template.matchAll(/<img\b[^>]*>/g)) {
  const tag = m[0];
  const src = tag.match(/src="([0-9a-f-]{36})"/); const alt = tag.match(/alt="([^"]*)"/);
  if (src && alt && alt[1].trim() && manifest[src[1]])
    names[src[1]] ??= slug(alt[1]) + '.' + (EXTOF[manifest[src[1]].mime] || 'bin');
}
let jsN = 0;
const JS_ROLE = ['runtime.js', 'page.js'];
for (const m of template.matchAll(/([0-9a-f-]{36})/g)) {                // scripts, by appearance
  const u = m[1];
  if (names[u] || !manifest[u]) continue;
  if (/javascript/.test(manifest[u].mime)) names[u] = JS_ROLE[jsN++] || `script-${jsN}.js`;
}
let imgN = 0;
for (const [u, e] of Object.entries(manifest))
  names[u] ??= (e.mime.startsWith('image/') ? `image-${++imgN}` : `asset-${u.slice(0,8)}`)
    + '.' + (EXTOF[e.mime] || 'bin');

// ---- write assets, deduping identical bytes --------------------------
const byHash = {}, urlFor = {};
let saved = 0;
for (const [uuid, e] of Object.entries(manifest)) {
  let bytes = Buffer.from(e.data || '', 'base64');
  if (e.compressed) bytes = zlib.gunzipSync(bytes);
  const h = crypto.createHash('sha256').update(bytes).digest('hex');
  if (byHash[h]) { urlFor[uuid] = byHash[h]; saved += bytes.length; continue; }
  let name = names[uuid];
  while (fs.existsSync(path.join(OUT,'assets',name)))                    // same alt, different art
    name = name.replace(/(\.\w+)$/, (_,x) => '-2' + x);
  fs.writeFileSync(path.join(OUT, 'assets', name), bytes);
  urlFor[uuid] = byHash[h] = 'assets/' + name;
}
console.log('assets written:', fs.readdirSync(path.join(OUT,'assets')).length,
            '| duplicate bytes saved:', (saved/1024).toFixed(0) + 'KB');

// ---- rewrite template ------------------------------------------------
for (const uuid of Object.keys(manifest)) template = template.split(uuid).join(urlFor[uuid]);
template = template.replace(/\s+integrity="[^"]*"/gi,'').replace(/\s+crossorigin="[^"]*"/gi,'');
template = template.replace(/<html(?![^>]*\blang=)/i, '<html lang="en"');

const resourceMap = {};
for (const e of ext) if (urlFor[e.uuid]) resourceMap[e.id] = urlFor[e.uuid];

const TITLE = 'ConvertCPG — Shopify Conversion Rate Optimization for CPG Brands';
const DESC  = 'Shopify conversion rate optimization for CPG brands. Website restructuring that lifts CVR and AOV. $150M+ in online sales driven. Book a free audit.';
const jsonld = {
  '@context':'https://schema.org','@type':'ProfessionalService','name':'ConvertCPG',
  legalName:'The Mendolia Group Corp', url: ORIGIN + '/', logo: ORIGIN + '/assets/convert-cpg.png',
  image: ORIGIN + '/og-image.jpg', description: DESC,
  serviceType:'Conversion rate optimization for Shopify stores', areaServed:'Worldwide'
};
const head = `
<title>${TITLE}</title>
<meta name="description" content="${DESC}">
<link rel="canonical" href="${ORIGIN}/">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#161826">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ConvertCPG">
<meta property="og:url" content="${ORIGIN}/">
<meta property="og:title" content="${TITLE}">
<meta property="og:description" content="${DESC}">
<meta property="og:image" content="${ORIGIN}/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${TITLE}">
<meta name="twitter:description" content="${DESC}">
<meta name="twitter:image" content="${ORIGIN}/og-image.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<script type="application/ld+json">${JSON.stringify(jsonld)}</script>
<script>window.__resources = ${JSON.stringify(resourceMap).replace(/<\//g,'<\\/')};</script>
`;
const ho = template.match(/<head[^>]*>/i);
template = template.slice(0, ho.index + ho[0].length) + head + template.slice(ho.index + ho[0].length);
fs.writeFileSync(path.join(OUT,'index.html'), template);

// ---- static extras ---------------------------------------------------


fs.writeFileSync(path.join(OUT,'CNAME'), DOMAIN + '\n');
fs.writeFileSync(path.join(OUT,'.nojekyll'), '');
fs.writeFileSync(path.join(OUT,'robots.txt'),
  `User-agent: *\nAllow: /\n\nSitemap: ${ORIGIN}/sitemap.xml\n`);
fs.writeFileSync(path.join(OUT,'sitemap.xml'),
  `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url>\n    <loc>${ORIGIN}/</loc>\n    <changefreq>monthly</changefreq>\n    <priority>1.0</priority>\n  </url>\n</urlset>\n`);
fs.writeFileSync(path.join(OUT,'site.webmanifest'), JSON.stringify({
  name:'ConvertCPG', short_name:'ConvertCPG', start_url:'/', display:'standalone',
  background_color:'#161826', theme_color:'#161826',
  icons:[{src:'/apple-touch-icon.png',sizes:'180x180',type:'image/png'},
         {src:'/icon-512.png',sizes:'512x512',type:'image/png'}]
}, null, 2) + '\n');

console.log('index.html:', (Buffer.byteLength(template)/1024).toFixed(1)+'KB');
