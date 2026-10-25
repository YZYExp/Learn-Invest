#!/usr/bin/env python3
"""Validate, render and build the book. Requires Python, Pandoc and Inkscape."""
from pathlib import Path
import argparse, json, re, subprocess, zipfile, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def sources():
    book = json.loads((ROOT/'book.json').read_text())
    return book, [ROOT/'appendices/00-reading-guide.md'] + [ROOT/c['source'] for c in book['chapters']] + [ROOT/'appendices/25-toolbox.md']

def validate():
    book, paths = sources()
    assert len(book['chapters']) == 24
    assert len({c['id'] for c in book['chapters']}) == 24
    chars, images = 0, set()
    for p in paths:
        text = p.read_text()
        assert not re.search(r'\bTODO\b|待补图|占位图',text), p
        chars += len(re.findall(r'[\u4e00-\u9fff]',text))
        for label, link in re.findall(r'!?\[([^\]]*)\]\(([^)]+)\)',text):
            if link.startswith(('https://','http://','#','mailto:')): continue
            target = (p.parent/link.split('#')[0]).resolve()
            assert target.is_file(), (p,link)
            if target.suffix == '.svg':
                ET.parse(target)
                images.add(target)
    assert len(images) == 24, len(images)
    result = {'chapters':24,'chinese_characters':chars,'teaching_figures':len(images),'local_links':'passed','svg_xml':'passed'}
    print(json.dumps(result,ensure_ascii=False))
    return book, paths, sorted(images), result

def render(images):
    from PIL import Image
    out = ROOT/'build/images'; out.mkdir(parents=True,exist_ok=True)
    for p in images:
        target=out/p.with_suffix('.png').name
        for attempt in range(3):
            temporary=out/f'{p.stem}-render-{attempt}.png'
            subprocess.run(['inkscape',str(p),'--export-type=png',f'--export-filename={temporary}','--export-width=1080'],check=True,capture_output=True)
            try:
                with Image.open(temporary) as im: im.load()
            except OSError:
                temporary.unlink(missing_ok=True)
                if attempt == 2: raise
                continue
            temporary.replace(target)
            break

def build():
    book, paths, images, result = validate()
    build = ROOT/'build'; build.mkdir(exist_ok=True)
    render(images)
    chunks = []
    toc = ['# 全书目录','']
    for c in book['chapters']:
        toc.append(f"- 第{int(c['id'][:2])}章 {c['title']}")
    for i,p in enumerate(paths):
        text = p.read_text()
        text = text.replace('../assets/images/','images/').replace('.svg)', '.png)')
        if p.parent.name == 'chapters':
            ch = next(c for c in book['chapters'] if c['source'] == str(p.relative_to(ROOT)))
            if ch['id'] in ['01-money','05-cash-bonds','09-primary-secondary','13-business','17-rates','21-plan']:
                text = f"# 第{ch['part']}篇 {ch['part_title']}\n\n" + text
        chunks.append(text)
    manuscript = build/'manuscript.md'
    manuscript.write_text('\n\n'.join(chunks))
    meta = build/'metadata.yaml'
    meta.write_text('title: "'+book['title']+'"\nsubtitle: "'+book['subtitle']+'"\nlang: zh-CN\ndate: "'+book['edition_date']+'"\n')
    epub = build/'Investment-From-Money-to-Markets.epub'
    subprocess.run(['pandoc',str(manuscript),'-o',str(epub),'--metadata-file',str(meta),'--toc','--toc-depth=1','--split-level=1','--css',str(ROOT/'assets/reader.css'),'--resource-path',str(build),'--epub-cover-image',str(ROOT/'assets/images/cover.png')],check=True)
    with zipfile.ZipFile(epub) as z:
        assert z.read('mimetype') == b'application/epub+zip'
        for n in z.namelist():
            if n.endswith(('.xhtml','.opf','.ncx')): ET.fromstring(z.read(n))
        embedded=[n for n in z.namelist() if n.endswith('.png')]
        assert len(embedded) == 25, embedded
        result['epub_embedded_images']=len(embedded)
    (build/'validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    (ROOT/'CONTENTS.md').write_text('\n'.join(toc)+'\n')
    print(epub)

if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    validate() if args.check else build()
