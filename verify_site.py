#!/usr/bin/env python3
"""Validate generated GitHub Pages site before deployment."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import subprocess

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
