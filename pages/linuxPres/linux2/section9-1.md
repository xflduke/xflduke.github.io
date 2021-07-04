## シェル



### 宿題：以下のシェルを作成：

- シェル名前：countSteps.sh
- パラメータ：ディレクトリパス
- 結果ファイルをディレクトリ名.logに出力：
  - 先頭行：処理日付と開始時間
  - 次：ディレクトリのフルパス
  - 次：ディレクトリ直下のファイル一覧と空白では無いの行の数
  - 末尾：処理日付と終了時点
<!-- 
```bash
#!/bin/bash
date
echo $1
#ls $1 | wc -l
#(find $1 -maxdepth 1 -type f' -print0 | xargs cat ) | wc -l
#find . -maxdepth 1 -type f | xargs wc -l
#total=0

for file in `find $1 -mindepth 1 -type f`; do
 numLines=`cat $file | grep -v "^\s*$" | wc -l`
# total=$(($total + $numLines))
 echo "  " $numLines $file
done
date
```
-->



### bashの主な仕様

- bashの先頭に実行環境の定義
  - 例：`#!/bin/bash`
- bashの実行方法
  - `bash シェルファイル`
  - `source シェルファイル`
  - `. シェルファイル`
  - `シェルファイルのパス`：シェルファイルに実行権必要



### 引数について

- `$0`：シェルスクリプトファイルフルパス
- `$[1|2|...N]`：第N番目のに引数
- `$#`：引数の数
- `$@`：全ての引数（スペース区切り）
- `$*`：全ての引数（環境変数IFSで指定の区切り）



### 戻り値について

- `echo $?`：戻り値を表示
  - `0`：正常終了
  - `0以外`：異常終了



### 条件判断について

- `test 条件文` または `条件文`
- 例：`-f パス`　←（ディレクトリ以外）ファイルがあれば真
- 例：`-d パス`　←ディレクトリがあれば真
- 例：`数値１ -eq 数値２`：数値の等しいテスト



- 例：`!条件式`：条件式の否定
- 例：`条件式1 -a 条件２`：両方が真のテスト（and）
- 例：`条件式1 -o 条件２`：いずれかが真のテスト（or）



### 制御構造について

- IF文
```bash
if　条件式
then
 実行文
elif 条件式
then
 実行文
else
 実行文
fi
```



- for文
```bash
for 変数名 in 対象リスト
do
 実行文
done
```



- while文
```bash
while 条件文
do
 実行文
done
```



- 関数
```bash
function 関数名()
{
  コマンド
} 
```



- リターンに関して
  - 関数func1の結果を出力して、正常終了
```bash
function func1() {
  echo 'ok'
}
function func2()  {
  local res=$(func1)
  echo $res
  exit 0
}
func2
```



### 標準入力から値を取得

- `read 変数名`
- 例：
```bash
read yourname
echo "hello, $yourname"
```



### その他興味がある方探してください

- 環境変数及びシェルの変数
- シェルのカスタマイズオプション(set -o)
- bashの設定ファイル（各種profile）
