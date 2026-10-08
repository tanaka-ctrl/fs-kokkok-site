【事例の追加方法】

1. このフォルダ（works_src）の中に、事例ごとにフォルダを1つ作る。
   フォルダ名は半角英数字とハイフンだけ（例: cafe-yokohama-2026）。
   この名前がそのままページのURLになります（/works/cafe-yokohama-2026/）。

2. そのフォルダに写真（.jpg / .jpeg / .png）を入れる。
   ・ファイル名の順（01.jpg, 02.jpg …）に並びます。
   ・1枚目が一覧のサムネイルになります。別の写真にしたいときは info.txt に「cover: 03.jpg」と書く。
   ・大きい写真のままで大丈夫です（自動で縮小されます）。

3. _template/info.txt をコピーして、同じフォルダに info.txt という名前で入れ、中身を書き換える。
   ・「項目名: 内容」の行がクレジットとして表示されます（title / year / category / cover / order 以外は全部クレジット扱い）。
   ・「---」の下に書いた文章が説明文になります。
   ・order: 数字 を書くと一覧の並び順を指定できます（小さい順。書かなければ year の新しい順）。

4. GitHub（github.com の tanaka-ctrl/fs-kokkok-site）にこのフォルダを入れると、2〜3分で自動的にページができて公開されます。
   やり方: リポジトリの works_src を開く → 右上「Add file」→「Upload files」→ フォルダごとドラッグ → 緑の「Commit changes」。

※ _template フォルダと README.txt は無視されます。
※ フォルダ名の先頭が「_」のものは公開されません（下書きに使えます）。
