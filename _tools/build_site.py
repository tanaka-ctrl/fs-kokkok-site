#!/usr/bin/env python3
"""サイト全体を _site/ に組み立てる。
- index.html / about / contact / css / js / images / CNAME / .nojekyll をそのままコピー
- works_src/<slug>/ (写真 + info.txt) から 事例一覧 works/ と 事例詳細 works/<slug>/ を生成し、写真を縮小
使い方: python3 _tools/build_site.py   （GitHub Actions が push のたびに自動実行する）"""
import os,re,shutil,html,subprocess,sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC=f'{ROOT}/works_src'; OUT=f'{ROOT}/_site'
LARGE=1800; THUMB=900
IMG_EXT=('.jpg','.jpeg','.png')
RESERVED={'title','year','category','cover','order'}

# ---------- 画像縮小（Pillowがあれば使う。無ければmacOSのsips） ----------
try:
    from PIL import Image, ImageOps
    HAVE_PIL=True
except ImportError:
    HAVE_PIL=False
def resize(src,dst,maxpx):
    os.makedirs(os.path.dirname(dst),exist_ok=True)
    if os.path.exists(dst) and os.path.getmtime(dst)>=os.path.getmtime(src): return
    if HAVE_PIL:
        im=Image.open(src); im=ImageOps.exif_transpose(im).convert('RGB')
        im.thumbnail((maxpx,maxpx),Image.LANCZOS)
        im.save(dst,'JPEG',quality=82,optimize=True,progressive=True)
    else:
        o=subprocess.run(['sips','-g','pixelWidth','-g','pixelHeight',src],capture_output=True,text=True).stdout
        cur=max(int(x) for x in re.findall(r'(?:pixelWidth|pixelHeight): (\d+)',o))
        args=['sips']+(['-Z',str(maxpx)] if cur>maxpx else [])+['-s','format','jpeg','-s','formatOptions','82',src,'--out',dst]
        subprocess.run(args,capture_output=True)

# ---------- info.txt を読む ----------
def read_info(path):
    meta={}; credits=[]; body=''
    txt=open(path,encoding='utf-8').read().replace('\r\n','\n')
    head,sep,body=txt.partition('\n---')
    for line in head.split('\n'):
        if ':' not in line: continue
        k,v=line.split(':',1); k=k.strip(); v=v.strip()
        if not k: continue
        if k.lower() in RESERVED: meta[k.lower()]=v
        elif v: credits.append((k,v))
    body=body.lstrip('-').strip()
    return meta,credits,body

def esc(s): return html.escape(s,quote=True)
def nl2br(s): return '<br>'.join(esc(l) for l in s.split('\n'))

# ---------- 共通テンプレート ----------
NOINDEX='<meta name="robots" content="noindex, nofollow">'
def header(rel,current):
    def a(href,label,key):
        return f'<a href="{href}"{" aria-current=\"page\"" if key==current else ""}>{label}</a>'
    return f'''<header class="site-header">
  <a class="logo" href="{rel}" aria-label="株式会社KOKKOK"><span class="wordmark">KOKKOK</span></a>
  <nav class="site-nav">
    {a(rel,'HOME','home')}
    {a(rel+'works/','WORKS','works')}
    {a(rel+'about/','ABOUT','about')}
    {a(rel+'contact/','CONTACT','contact')}
  </nav>
</header>'''
FOOTER='''<footer class="site-footer">
  <div class="inner">
    <div>© 株式会社KOKKOK ｜ 神奈川県横浜市港北区新吉田町203</div>
    <div>CNC加工の受託は <a href="https://fabnode.jp" target="_blank" rel="noopener">FABNODE</a></div>
  </div>
</footer>'''
def page(title,desc,rel,current,main,extra_head='',extra_body=''):
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{NOINDEX}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{rel}css/style.css">
{extra_head}</head>
<body>

{header(rel,current)}

<main>
{main}
</main>

{FOOTER}
{extra_body}
</body>
</html>
'''

# ---------- 1. 静的ファイルをコピー ----------
if os.path.exists(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
for item in ['index.html','about','contact','css','js','images','CNAME','.nojekyll','robots.txt']:
    p=f'{ROOT}/{item}'
    if os.path.isdir(p): shutil.copytree(p,f'{OUT}/{item}')
    elif os.path.isfile(p): shutil.copy2(p,f'{OUT}/{item}')

# ---------- 2. 事例を読み込む ----------
works=[]
for slug in sorted(os.listdir(SRC)):
    d=f'{SRC}/{slug}'
    if not os.path.isdir(d) or slug.startswith('_'): continue
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]*',slug):
        print(f'[skip] {slug}: フォルダ名は半角小文字英数字とハイフンのみ'); continue
    info=f'{d}/info.txt'
    if not os.path.exists(info): print(f'[skip] {slug}: info.txt がありません'); continue
    meta,credits,body=read_info(info)
    photos=sorted(f for f in os.listdir(d) if f.lower().endswith(IMG_EXT) and not f.startswith('.'))
    if not photos: print(f'[skip] {slug}: 写真がありません'); continue
    cover=meta.get('cover') if meta.get('cover') in photos else photos[0]
    works.append(dict(slug=slug,dir=d,title=meta.get('title',slug),year=meta.get('year',''),category=meta.get('category',''),
                      credits=credits,body=body,photos=photos,cover=cover,order=meta.get('order')))
def sortkey(w):
    o=w['order']
    return (0,int(o)) if o and o.isdigit() else (1,-int(w['year']) if w['year'].isdigit() else 0)
works.sort(key=sortkey)

# ---------- 3. 写真を縮小 ----------
for w in works:
    for n,f in enumerate(w['photos'],1):
        base=f'{OUT}/images/works/{w["slug"]}/{n:02d}'
        resize(f'{w["dir"]}/{f}',base+'.jpg',LARGE)
        resize(f'{w["dir"]}/{f}',base+'_s.jpg',THUMB)
    resize(f'{w["dir"]}/{w["cover"]}',f'{OUT}/images/works/{w["slug"]}/cover.jpg',THUMB)

# ---------- 4. 一覧ページ ----------
cards=''.join(f'''        <a class="work-card" href="{w['slug']}/">
          <img src="../images/works/{w['slug']}/cover.jpg" alt="{esc(w['title'])}" loading="lazy">
          <span class="work-card-title">{esc(w['title'])}</span>
          <span class="work-card-meta">{esc(' / '.join(x for x in [w['category'],w['year']] if x))}</span>
        </a>
''' for w in works)
main=f'''  <section class="section">
    <div class="wrap">
      <p class="eyebrow">WORKS</p>
      <h1>事例</h1>
      <p class="lead">店舗什器・オーダー家具・試作開発など、これまでの製作事例です。</p>
      <div class="work-list">
{cards}      </div>
    </div>
  </section>'''
os.makedirs(f'{OUT}/works',exist_ok=True)
open(f'{OUT}/works/index.html','w',encoding='utf-8').write(page('事例｜株式会社KOKKOK','株式会社KOKKOKの製作事例。店舗什器、オーダー家具、試作開発。','../','works',main))

# ---------- 4b. トップページの横スライド ----------
slides=''.join(f'''      <a class="slide" href="works/{w['slug']}/">
        <img src="images/works/{w['slug']}/cover.jpg" alt="{esc(w['title'])}" loading="lazy">
        <span class="slide-title">{esc(w['title'])}</span>
      </a>
''' for w in works)
carousel=f'''    <div class="carousel" id="carousel">
      <button class="carousel-btn prev" type="button" aria-label="前へ">‹</button>
      <div class="track" id="track">
{slides}      </div>
      <button class="carousel-btn next" type="button" aria-label="次へ">›</button>
    </div>
    <script src="js/carousel.js"></script>
'''
idx=open(f'{OUT}/index.html',encoding='utf-8').read()
idx=re.sub(r'(<!-- WORKS_CAROUSEL_START[^>]*-->\n).*?(    <!-- WORKS_CAROUSEL_END -->)',lambda m:m.group(1)+carousel+m.group(2),idx,flags=re.S)
open(f'{OUT}/index.html','w',encoding='utf-8').write(idx)

# ---------- 5. 詳細ページ（グリッド＋クリック拡大） ----------
LIGHTBOX='''<div class="lb" id="lb" hidden>
  <button class="lb-close" id="lbClose" aria-label="閉じる">×</button>
  <button class="lb-prev" id="lbPrev" aria-label="前の写真">‹</button>
  <img id="lbImg" alt="">
  <button class="lb-next" id="lbNext" aria-label="次の写真">›</button>
  <div class="lb-count" id="lbCount"></div>
</div>
<script src="../../js/lightbox.js"></script>'''
for i,w in enumerate(works):
    photo=next((v for k,v in w['credits'] if k.lower()=='photo'),None)
    rows=[('year',w['year'])] if w['year'] else []
    rows+=w['credits']
    credits=''.join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k,v in rows)
    body=f'<p class="work-body">{nl2br(w["body"])}</p>' if w['body'] else ''
    tiles=''.join(f'''        <a class="tile" href="../../images/works/{w['slug']}/{n:02d}.jpg" data-index="{n-1}">
          <img src="../../images/works/{w['slug']}/{n:02d}_s.jpg" alt="{esc(w['title'])} {n}" loading="lazy">
        </a>
''' for n in range(1,len(w['photos'])+1))
    prev=works[i-1] if i>0 else None; nxt=works[i+1] if i<len(works)-1 else None
    nav=(f'<a href="../{prev["slug"]}/">← {esc(prev["title"])}</a>' if prev else '<span></span>')+'<a href="../">事例一覧</a>'+(f'<a href="../{nxt["slug"]}/">{esc(nxt["title"])} →</a>' if nxt else '<span></span>')
    main=f'''  <article class="section work-detail">
    <div class="wrap">
      <p class="eyebrow">WORKS</p>
      <h1>{esc(w['title'])}</h1>
      <div class="work-head">
        <dl class="credits">{credits}</dl>
        {body}
      </div>
      <div class="tiles" id="tiles">
{tiles}      </div>
      {f'<p class="photo-credit">photo: {esc(photo)}</p>' if photo else ''}
      <nav class="work-nav">{nav}</nav>
      <p><a class="btn" href="../../contact/">このような什器・家具のご相談</a></p>
    </div>
  </article>'''
    os.makedirs(f'{OUT}/works/{w["slug"]}',exist_ok=True)
    open(f'{OUT}/works/{w["slug"]}/index.html','w',encoding='utf-8').write(
        page(f"{w['title']}｜事例｜株式会社KOKKOK",f"{w['title']}（{w['year']}）の製作事例。",'../../','works',main,extra_body=LIGHTBOX))
print(f'build ok: {len(works)} works ->',OUT)
for w in works: print(f"  {w['slug']}: {len(w['photos'])}枚")
