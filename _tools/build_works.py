#!/usr/bin/env python3
"""works.json から 事例一覧(works/index.html) と 事例詳細(works/<slug>/index.html) を生成する。
使い方: python3 _tools/build_works.py  （リポジトリのルートで実行）"""
import json,os,glob,html
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W=json.load(open(f'{ROOT}/_tools/works.json',encoding='utf-8'))
NOINDEX='<meta name="robots" content="noindex, nofollow">'
def esc(s): return html.escape(s,quote=True)
def header(rel,current):
    def a(href,label,key):
        cur=' aria-current="page"' if key==current else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    return f'''<header class="site-header">
  <a class="logo" href="{rel}" aria-label="株式会社KOKKOK"><span class="wordmark">KOKKOK</span></a>
  <nav class="site-nav">
    {a(rel,'HOME','home')}
    {a(rel+'works/','事例','works')}
    {a(rel+'about/','会社概要','about')}
    {a(rel+'contact/','お問い合わせ','contact')}
  </nav>
</header>'''
FOOTER='''<footer class="site-footer">
  <div class="inner">
    <div>© 株式会社KOKKOK ｜ 神奈川県横浜市港北区新吉田町203</div>
    <div>CNC加工の受託は <a href="https://fabnode.jp" target="_blank" rel="noopener">FABNODE</a></div>
  </div>
</footer>'''
def page(title,desc,rel,current,main):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{NOINDEX}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{rel}css/style.css">
</head>
<body>

{header(rel,current)}

<main>
{main}
</main>

{FOOTER}

</body>
</html>
'''
# 一覧
cards=''
for w in W:
    cards+=f'''        <a class="work-card" href="{w['slug']}/">
          <img src="../images/works/{w['slug']}/thumb.jpg" alt="{esc(w['title'])}" loading="lazy">
          <span class="work-card-title">{esc(w['title'])}</span>
          <span class="work-card-meta">{esc(w['client'])} / {w['year']}</span>
        </a>
'''
main=f'''  <section class="section">
    <div class="wrap">
      <p class="eyebrow">WORKS</p>
      <h1>事例</h1>
      <p class="lead">店舗什器・オーダー家具・試作開発など、これまでの製作事例です。</p>
      <div class="work-list">
{cards}      </div>
    </div>
  </section>'''
os.makedirs(f'{ROOT}/works',exist_ok=True)
open(f'{ROOT}/works/index.html','w',encoding='utf-8').write(page('事例｜株式会社KOKKOK','株式会社KOKKOKの製作事例。店舗什器、オーダー家具、試作開発。','../','works',main))
# 詳細
for i,w in enumerate(W):
    imgs=sorted(f for f in os.listdir(f"{ROOT}/images/works/{w['slug']}") if f[0].isdigit())
    photo=next((v for k,v in w['credits'] if k=='photo'),None)
    credits=''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k,v in [('year',w['year'])]+w['credits'])
    body=f'<p class="work-body">{esc(w["body"])}</p>' if w['body'] else ''
    figs=''
    for f in imgs:
        cap=f'<figcaption>photo: {esc(photo)}</figcaption>' if photo else ''
        figs+=f'        <figure><img src="../../images/works/{w["slug"]}/{f}" alt="{esc(w["title"])}" loading="lazy">{cap}</figure>\n'
    prev=W[i-1] if i>0 else None; nxt=W[i+1] if i<len(W)-1 else None
    nav=''
    if prev: nav+=f'<a href="../{prev["slug"]}/">← {esc(prev["title"])}</a>'
    nav+='<a href="../">事例一覧</a>'
    if nxt: nav+=f'<a href="../{nxt["slug"]}/">{esc(nxt["title"])} →</a>'
    main=f'''  <article class="section work-detail">
    <div class="wrap">
      <p class="eyebrow">WORKS</p>
      <h1>{esc(w['title'])}</h1>
      <div class="work-head">
        <dl class="credits">{credits}</dl>
        {body}
      </div>
      <div class="work-photos">
{figs}      </div>
      <nav class="work-nav">{nav}</nav>
      <p><a class="btn" href="../../contact/">このような什器・家具のご相談</a></p>
    </div>
  </article>'''
    os.makedirs(f"{ROOT}/works/{w['slug']}",exist_ok=True)
    open(f"{ROOT}/works/{w['slug']}/index.html",'w',encoding='utf-8').write(
        page(f"{w['title']}｜事例｜株式会社KOKKOK",f"{w['title']}（{w['year']}）の製作事例。",'../../','works',main))
print('generated',1+len(W),'pages')
