## 検索＆置換え



### findコマンド

- `find [検索ディレクトリ] [検索式]`
  - 主な検索式
    - `-name`：ファイル名を指定
    - `mtime`：最終更新時刻で検索
    - `size`：サイズで検索



    - `type [f|d|l]`：ファイル種類で検索
      - `f`：ファイル、`d`：ディレクトリ、`l`：ソフトリンク
    - `exec コマンド {} \;`：マッチしたファイルに対してコマンド実行
    - `ok コマンド {} \;`：マッチしたファイルに対してコマンド実行（確認あり）



#### findの利用例

- 例：過去３０日以上アクセスされていない且つサイズが１００MByteを超えるファイルを検索して削除
  - `find ~/work -type f -atime +30 -size +100M -ok rm {} \;` 



### grepコマンド

- `grep [-c][-f ファイル][-i][-n][-v][-E] 検索パターン ファイル名`
  - `-c`：パターンがマッチ下行の行数だけを表示
  - `-f`：検索パターンをファイルから読み込む
  - `-i`：大文字と小文字を区別せずに検索
  - `-n`：検索結果と合わせて行番号も表示
  - `-v`：パターンがマッチしない行を表示する
  - `-E`：拡張正規表現を利用



 #### 演習：/etc/ssh/sshd_config中のコメント行の一覧を出す
 <!-- cat /etc/ssh/sshd_config | grep ^# -->
 #### 演習：/etc/ssh/sshd_config中のコメントではない行の一覧を出す
 <!-- cat /etc/ssh/sshd_config | grep -v ^# -->
 <!-- cat /etc/ssh/sshd_config | grep -v ^# | uniq -->
 <!-- cat /etc/ssh/sshd_config | grep -v ^# | grep -v ^$ -->



### grepのその他

- `egrep`：拡張正規表現を利用のgrep（=`grep -E`）
- `fgrep`：正規表現を使わないのgrep



### sedコマンド

- `sed [-f ファイル][[-i][-n] コマンド] [ファイル]`
  - オプション
    - `-f ファイル`：スクリプトを指定（この場合コマンドが不要）
    - `-i`：処理結果をファイル自身を上書き
    - `-n`：処理後の結果のみを出力



- コマンド：
  - `a|d|i`：指定行の次の行を追加、削除、前行を追加
    - 例：`nl /etc/passwd | sed '1,1d'`
    - 例：`nl /etc/passwd | sed '1i TITLE：Hello World'`
  - `s`：パターン指定の置き換え
    - 例：`nl /etc/passwd | sed '1,10s/bin/BIN/g'`
  - `y`：文字ごとの置き換え
    - 例：`nl /etc/passwd | sed '1,10y/bin/BIN/g'`
