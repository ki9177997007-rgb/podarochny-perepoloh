#!/usr/bin/env python3
"""Validate generated GitHub Pages site before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import subprocess
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        for key in ('href','src'):
            if key in d and d[key]:self.refs.append((tag,key,d[key]))

errors=[]
pages=list(ROOT.glob('*.html'))
if len(pages)<150:errors.append(f'Generated HTML pages missing: found {len(pages)}')
for page in pages:
    parser=Links()
    try:parser.feed(page.read_text(encoding='utf-8'))
    except Exception as exc:
        errors.append(f'{page.name}: HTML parse failed: {exc}')
        continue
    for tag,key,ref in parser.refs:
        if ref.startswith(('#','data:','mailto:','tel:','javascript:')):continue
        u=urlsplit(ref)
        if u.scheme or u.netloc:continue
        target=(ROOT/u.path.lstrip('/') if u.path.startswith('/') else page.parent/unquote(u.path)).resolve()
        if target.is_dir():target=target/'index.html'
        if not target.exists():errors.append(f'{page.name}: missing {key}={ref}')
sitemap=(ROOT/'sitemap.xml').read_text(encoding='utf-8') if (ROOT/'sitemap.xml').exists() else ''
if 'powerbank-ili-zaryadnoe-ustroystvo.html' not in sitemap:
    errors.append('Original comparison missing from sitemap.xml')
# Enforce sitemap, canonical and noindex consistency for every generated HTML page.
BASE = 'https://ki9177997007-rgb.github.io/podarochny-perepoloh/'
class Seo(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.noindex = False
    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == 'link' and d.get('rel') == 'canonical':
            self.canonical = d.get('href')
        if tag == 'meta' and d.get('name') == 'robots':
            self.noindex = 'noindex' in d.get('content', '').lower()

sitemap_urls = []
try:
    sitemap_root = ET.fromstring(sitemap)
    sitemap_urls = [loc.text.strip() for loc in sitemap_root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if loc.text]
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append('Duplicate URLs in sitemap.xml')
except ET.ParseError as exc:
    errors.append(f'Invalid sitemap.xml: {exc}')
for url in sitemap_urls:
    if not url.startswith(BASE):
        errors.append(f'Sitemap URL outside site: {url}')
        continue
    target = ROOT / (unquote(url[len(BASE):]) or 'index.html')
    if not target.is_file():
        errors.append(f'Sitemap URL missing page: {url}')
for page in pages:
    seo = Seo()
    seo.feed(page.read_text(encoding='utf-8'))
    expected = BASE + ('' if page.name == 'index.html' else page.name)
    if not seo.noindex:
        if seo.canonical != expected:
            errors.append(f'{page.name}: incorrect canonical URL')
        if expected not in sitemap_urls:
            errors.append(f'{page.name}: indexable page missing from sitemap.xml')
    elif expected in sitemap_urls:
        errors.append(f'{page.name}: noindex page present in sitemap.xml')
if not (ROOT/'robots.txt').exists() or BASE+'sitemap.xml' not in (ROOT/'robots.txt').read_text(encoding='utf-8'):
    errors.append('robots.txt missing sitemap reference')
video=ROOT/'media'/'powerbank-vs-charger-motion.mp4'
if not video.exists() or video.stat().st_size<10000:
    errors.append('Animated vertical video missing or empty')
else:
    try:
        meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,duration','-of','json',str(video)],text=True))
        stream=meta['streams'][0]
        if int(stream['width'])>=int(stream['height']):errors.append('Video is not vertical')
        if float(stream.get('duration',0))<8:errors.append('Video is shorter than 8 seconds')
    except Exception as exc:errors.append(f'Video probe failed: {exc}')
if errors:
    print('\n'.join(errors[:50]))
    raise SystemExit(f'Site validation failed with {len(errors)} issue(s)')
print(f'OK: {len(pages)} HTML pages, local links, sitemap and animated vertical video')
