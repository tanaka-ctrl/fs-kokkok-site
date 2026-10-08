# fs-kokkok-site — 株式会社KOKKOK 法人サイト

GitHub Pages で公開する静的サイト（HTML + CSS のみ、ビルド不要）。

## フォルダ構成

| 場所 | 内容 |
|---|---|
| `index.html` | トップページ |
| `about/index.html` | 会社概要（/about/） |
| `contact/index.html` | お問い合わせ（/contact/、mailto方式） |
| `works/` | 事例一覧と各詳細（/works/、/works/<slug>/）。`_tools/build_works.py` が生成 |
| `_tools/works.json` | 事例データ（タイトル・年・クレジット・本文）。ここを直して生成スクリプトを実行 |
| `css/style.css` | 全ページ共通のスタイル |
| `images/` | サイトで使う画像（長辺2000px程度に縮小済み） |
| `_archive/wix/` | 旧Wixサイトのバックアップ（文章・元サイズ画像）。公開ページからは使わない |
| `CNAME` | 独自ドメイン設定（www.fs-kokkok.com） |

## 検索エンジン対策（現在）

全ページに `<meta name="robots" content="noindex, nofollow">` を入れてあり、Google等の検索結果には載らない。公開OKになったら全HTMLからこの1行を削除する。

## 事例の足し方

1. `_archive/wix/` などの元画像を `images/works/<slug>/01.jpg, 02.jpg…`（長辺1800px）と `thumb.jpg`（長辺1000px）に縮小して置く
2. `_tools/works.json` に1件分を追記
3. `python3 _tools/build_works.py` を実行すると `works/` 配下のHTMLが作り直される

## 新しい種類のページの足し方（例：How to order）

1. `works/index.html` のように「フォルダ名/index.html」を作る（URLは `/works/` になる）
2. 中身は `about/index.html` をコピーして、`<main>` の中だけ書き換える
3. ヘッダーの `<nav>` に `<a href="../works/">事例</a>` のようにリンクを1行足す（全ページ分）
4. 画像は `_archive/wix/` の元画像から `images/` に縮小コピーして使う
   - 縮小コマンド例（Mac標準の sips）: `sips -Z 2000 -s format jpeg -s formatOptions 82 元画像.jpg --out images/新しい名前.jpg`
5. コミットして `main` に push すると数分で公開される

## 公開設定

- GitHub Pages: `main` ブランチ / ルート
- 独自ドメイン: www.fs-kokkok.com（CNAMEファイル）
