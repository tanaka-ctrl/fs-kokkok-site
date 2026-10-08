# fs-kokkok-site — 株式会社KOKKOK 法人サイト

GitHub Pages で公開する静的サイト。`main` に push すると GitHub Actions が `_tools/build_site.py` を実行してサイトを組み立て、公開する。

## フォルダ構成

| 場所 | 内容 |
|---|---|
| `index.html` | トップページ（手書きHTML） |
| `about/index.html` | 会社概要（/about/） |
| `contact/index.html` | お問い合わせ（/contact/、mailto方式） |
| `works_src/` | **事例の元データ**。1事例＝1フォルダ（写真＋info.txt）。足し方は `works_src/README.txt` |
| `css/style.css` / `js/lightbox.js` | 共通スタイル、写真の拡大表示 |
| `images/` | トップページ用の画像（縮小済み） |
| `_tools/build_site.py` | サイト生成スクリプト（事例ページ生成・写真縮小・`_site/` へ出力） |
| `.github/workflows/deploy.yml` | push のたびに自動で生成＋公開 |
| `_archive/wix/` | 旧Wixサイトのバックアップ（文章・元サイズ画像）。公開はされない |
| `_site/` | 生成結果（gitには入れない） |

## 事例の足し方

`works_src/README.txt` を参照。フォルダを1つ追加して push（または github.com でアップロード）するだけ。

## 検索エンジン対策（現在）

全ページに `<meta name="robots" content="noindex, nofollow">` が入っており検索結果に載らない。公開OKになったら `index.html` / `about` / `contact` の各HTMLと `_tools/build_site.py` の `NOINDEX` から外す。

## 独自ドメイン

www.fs-kokkok.com を使うときはリポジトリ直下に `CNAME` ファイル（中身は `www.fs-kokkok.com` の1行）を置く。生成スクリプトが `_site/` にコピーする。

## ローカルで確認する

```bash
python3 _tools/build_site.py && python3 -m http.server 8765 --directory _site
```
