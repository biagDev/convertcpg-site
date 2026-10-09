#!/usr/bin/env python3
"""Tell Bing about new or updated pages (Bing Webmaster URL Submission API).

Usage:
  python3 tools/ping-bing.py https://convertcpg.com/blog/some-post/ [more URLs]
  python3 tools/ping-bing.py --blog     # every post URL in sitemap.xml under /blog/

The API key is read from ~/.convertcpg/bing-webmaster.key (never commit it).
Quota: 100 URLs a day, 2,300 a month.
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

SITE = "https://convertcpg.com/"
KEY_FILE = Path.home() / ".convertcpg" / "bing-webmaster.key"
ENDPOINT = "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch?apikey="


def blog_urls():
    sitemap = (Path(__file__).resolve().parent.parent / "sitemap.xml").read_text()
    return [u for u in re.findall(r"<loc>([^<]+)</loc>", sitemap) if "/blog/" in u]


def main(args):
    if not KEY_FILE.exists():
        sys.exit(f"No Bing key at {KEY_FILE}")
    urls = blog_urls() if args == ["--blog"] else args
    if not urls:
        sys.exit("No URLs to submit.")
    body = json.dumps({"siteUrl": SITE, "urlList": urls[:100]}).encode()
    req = urllib.request.Request(ENDPOINT + KEY_FILE.read_text().strip(), data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(resp.status, resp.read().decode() or "ok")
    print("Submitted:", *urls[:100], sep="\n  ")


if __name__ == "__main__":
    main(sys.argv[1:])
