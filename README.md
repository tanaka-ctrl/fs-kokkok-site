# fs-kokkok-site — 株式会社KOKKOK 法人サイト

GitHub Pages で公開する静的サイト（HTML + CSS のみ、ビルド不要）。

## フォルダ構成

| 場所 | 内容 |
|---|---|
| `index.html` | トップページ |
| `about/index.html` | 会社概要（/about/） |
| `contact/index.html` | お問い合わせ（/contact/、mailto方式） |
| `css/style.css` | 全ページ共通のスタイル |
| `images/` | サイトで使う画像（長辺2000px程度に縮小済み） |
| `_archive/wix/` | 旧Wixサイトのバックアップ（文章・元サイズ画像）。公開ページからは使わない |
| `CNAME` | 独自ドメイン設定（www.fs-kokkok.com） |

## ページの足し方（例：事例ページ）

1. `works/index.html` のように「フォルダ名/index.html」を作る（URLは `/works/` になる）
2. 中身は `about/index.html` をコピーして、`<main>` の中だけ書き換える
3. ヘッダーの `<nav>` に `<a href="../works/">事例</a>` のようにリンクを1行足す（全ページ分）
4. 画像は `_archive/wix/` の元画像から `images/` に縮小コピーして使う
   - 縮小コマンド例（Mac標準の sips）: `sips -Z 2000 -s format jpeg -s formatOptions 82 元画像.jpg --out images/新しい名前.jpg`
5. コミットして `main` に push すると数分で公開される

## 公開設定

- GitHub Pages: `main` ブランチ / ルート
- 独自ドメイン: www.fs-kokkok.com（CNAMEファイル）
