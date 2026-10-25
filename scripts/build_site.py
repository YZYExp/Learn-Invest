#!/usr/bin/env python3
"""Build the public homepage and reader from the authoritative manuscript."""
import argparse
import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser
import markdown
from build_book import validate

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-path', default='/')
    args = parser.parse_args()
    base = '/' + args.base_path.strip('/') + '/' if args.base_path.strip('/') else '/'
    book, _, _, _ = validate()
    out = ROOT / 'build/site'
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(ROOT / 'assets', out / 'assets')
    for name in ['style.css', 'app.js']: shutil.copy(ROOT / 'site' / name, out / name)
    (out / '.nojekyll').touch()
    units = [dict(c, slug=Path(c['source']).stem) for c in book['front_matter']] + book['chapters'] + [dict(c, slug=Path(c['source']).stem) for c in book['back_matter']]
    source_urls = {c['source']: base+c['slug']+'.html' for c in units}
    esc = html.escape
    def layout(title, content, active=''):
        nav = ''.join(f'<a class="{"active" if c["slug"] == active else ""}" href="{base}{c["slug"]}.html">{esc(c["title"])}</a>' for c in units)
        return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="投资基础图解：从钱、资产、市场交易到财报估值和投资方法。"><title>{esc(title)} · 看懂投资</title><link rel="stylesheet" href="{base}style.css"><script defer src="{base}app.js"></script></head><body><header><a class="brand" href="{base}">看懂投资<span>从一笔钱到整个市场</span></a><nav><a href="{base}#contents">全书目录</a><a href="https://github.com/YZYExp/Learn-Invest">GitHub ↗</a><button id="size" type="button" aria-label="切换正文字号">字号 A</button></nav></header><div class="shell"><aside><details open><summary>阅读目录</summary><input id="search" type="search" placeholder="搜索全书" aria-label="搜索全书"><div id="results"></div><div id="chapters">{nav}</div></details></aside><main>{content}</main></div><footer>看懂投资 · 六篇二十四章 · 教学案例与配图的假设及出处见各章</footer><dialog id="zoom"><button type="button" id="close-zoom">关闭 ×</button><img alt=""></dialog></body></html>'''
    groups = []
    for part in range(1, 7):
        chapters = [c for c in book['chapters'] if c['part'] == part]
        cards = ''.join(f'<a class="card" href="{base}{c["slug"]}.html"><small>CHAPTER {c["id"][:2]}</small><h3>{esc(c["title"])}</h3><span>阅读这一章 →</span></a>' for c in chapters)
        groups.append(f'<section class="part"><h2><small>0{part}</small> {esc(chapters[0]["part_title"])}</h2><div class="cards">{cards}</div></section>')
    hero = f'''<section class="hero"><div><p class="eyebrow">THE INVESTMENT ATLAS</p><h1>看懂投资</h1><p class="subtitle">从一笔钱到整个市场</p><p>理解钱的任务，认识资产与风险。看懂价格如何形成，再建立自己的投资判断。</p><div class="actions"><a class="primary" href="{base}00-reading-guide.html">开始阅读 →</a><a href="#contents">浏览全书目录 ↓</a></div><p class="stats">6 篇主题 · 24 章正文 · 24 幅教学图</p></div><img src="{base}assets/images/cover.png" alt="看懂投资封面" width="720" height="960"></section><section class="intro"><h2>让每一个概念都有落点</h2><p>沿着一家公司的经营、一张债券的现金流和一个家庭的资金安排，连接资产、交易、估值与风险。图中的数值均为可核算的教学假设。</p><p>从“主力出逃时谁在买”，到“好公司为什么也可能是差投资”，回到市场运作的具体机制。</p></section><div id="contents">{''.join(groups)}</div><section class="intro"><h2>随手查阅</h2><p><a href="{base}25-toolbox.html">判断表与词汇 →</a></p><p><a href="https://github.com/YZYExp/Learn-Invest/actions/workflows/epub.yml">导出 EPUB 与下载构建产物 ↗</a>（需 GitHub 登录，产物保留 90 天）</p></section>'''
    (out / 'index.html').write_text(layout(book['title'], hero), encoding='utf-8')
    search = []
    for i, c in enumerate(units):
        path = ROOT / c['source']
        text = path.read_text()
        def rewrite(match):
            label, link = match.groups()
            if urlsplit(link).scheme or link.startswith('#'): return match.group(0)
            target = (path.parent / link.split('#')[0]).resolve().relative_to(ROOT).as_posix()
            suffix = '#' + link.split('#', 1)[1] if '#' in link else ''
            return f'[{label}]({source_urls.get(target, base+target)}{suffix})'
        text = re.sub(r'\[([^\]]*)\]\(([^)]+)\)', rewrite, text)
        content = markdown.markdown(text, extensions=['tables', 'footnotes', 'fenced_code', 'toc'])
        content = content.replace('<img ', '<img loading="lazy" decoding="async" ')
        links = []
        if i: links.append(f'<a href="{base}{units[i-1]["slug"]}.html">← {esc(units[i-1]["title"])}</a>')
        if i+1 < len(units): links.append(f'<a href="{base}{units[i+1]["slug"]}.html">{esc(units[i+1]["title"])} →</a>')
        page = f'<article>{content}</article><nav class="pager">{"".join(links)}</nav>'
        (out / (c['slug']+'.html')).write_text(layout(c['title'], page, c['slug']), encoding='utf-8')
        search.append(dict(title=c['title'], url=base+c['slug']+'.html', text=re.sub('<[^>]+>', ' ', content)))
    (out / 'search.json').write_text(json.dumps(search, ensure_ascii=False), encoding='utf-8')
    class Links(HTMLParser):
        def handle_starttag(self, tag, attrs):
            for key, value in attrs:
                if key in ('src', 'href') and value and not urlsplit(value).scheme and not value.startswith('#'):
                    target = unquote(urlsplit(value).path)
                    assert target.startswith(base), value
                    assert (out / target[len(base):]).exists(), value
    for page in out.glob('*.html'): Links().feed(page.read_text())
    print(f'Built and checked {len(units)+1} HTML pages with {len(list((out/"assets/images").glob("fig-*.svg")))} teaching figures at {base}')

if __name__ == '__main__': main()
