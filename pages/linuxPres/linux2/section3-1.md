# コマンドに関する知識



# 準備できた環境に、講義を見ながら操作してみてください。



#### コンソールの基本使い方
##### ※MACOSでは、Ctrlはコンソール操作向けのCommandの理解でいいです。

 - キー操作
   - `Tabキー`：コマンドやパスを補完する
   - `Ctrl＋A、Ctrl+E`：入力中のコマンドラインの先頭、最後へカーソルを移動する
   - `Ctrl+C`：実行中処理中断する
   - `Ctrl+S、Ctrl+Q`：画面への出力を一時停止と再開
   - `Ctrl+Z`：処理を一時停止し、バックグラウンドへ移動



##### コマンドの記述

 - 一般記述方：`コマンド [オプション] [引数]`
 - 複数コマンドの実行
   - `コマンド１;コマンド２`：コマンド１に続いてコマンド２を実行
     - 例：`cd ~;ls`
   - `コマンド１&&コマンド２`：コマンド１が正常終了した時のみコマンド２を実行
     - 例：`cd ~;ls`



   - `コマンド１||コマンド２`：コマンド１が正常終了しなかった時のみコマンド２を実行
     - 例：`cd /home/notExsit||cd ~&&ls`
   - `コマンド > ファイル`：コマンドの実行結果をファイルに出力（上書き）
   - `コマンド >> ファイル`：コマンドの実行結果をファイルに出力（追記）
   - `(コマンド１;コマンド２)`：順次実行、結果は同一で出力
     - 例：`(date;pwd;ls -l) > dailyZZ.log`



##### 同一ユーザのコマンド実行履歴の参照

 - コマンド：`history`
   - `!履歴番号`：指定番号のコマンドを実行
   - `!!`：直前に実行下コマンドを再実行



# コマンドのマニュアル（manコマンド）について



##### linuxでの各種コマンド対応のマニュアルは`man -w`に格納されていて  
不明等があれば以下から参照ください。
 - manページの操作手順
   - `スペースキー`：次のページへ
   - `bキー`：前のページへ
   - `\キーワード`：後ろに指定のキーワードを探す
   - `?キーワード`：前方に指定のキーワードを探す
   - `Shift+Q`：ヘルプページを退出
   - `hキー`：マニュアル自身のヘルプを表示



 - 使い方不明もしくはコマンド名前忘れ
   - `man`コマンドを利用する
     - `man [コマンド名]`：指定コマンドのドキュメントを表示
     - `man [-f|-k] [キーワード]`：指定キーワードが含まれるドキュメントを探す
     - `man man`にも可能
<!-- [//] - マニュアルで表示された言語
[//]   - 必要に応じて言語パッケージをインストール
[//]     - `dnf -y install langpacks-ja`：日本語パッケージのインストール
[//]     - `dnf -y install langpacks-ja`：日本語パッケージのインストール
[//]     - `dnf list langpacks-*`：利用可能な言語パッケージ一覧を出す
[//]     - `localectl set-locale LANG=ja_JP.UTF-8`：システム全体の言語を変える
[//]     - `source /etc/locale.conf`：有効化
[//]     - `echo $LANG`：確認
[//]   - 利用可能なロケールを確認
[//]     - `locale -a`
[//]     - `dnf -y install man-pages-zh-CN`
[//]   - 指定の言語のマニュアルを開く
[//]     - `LANG=zh_CN man ls`-->



# 他言語のマニュアルのインストール



### REHLの８では日本語や中国語のマニュアルパッケージはまだリポジトリに取り込んでいない  
手動コンパイラーしてインストールが必要

#### 前提条件のパッケージをインストール
  - `dnf -y install autoconf`
  - `dnf -y install automake`
  - `dnf -y install python3`



#### openccのインストール
- 作業フォルダに移動し、例：`mkdir -p /work && cd /work`
- OpenCCのソースをチェックアウト：`git clone https://github.com/BYVoid/OpenCC && cd OpenCC`
- コンパイラーツールインストール：
  - `dnf install -y git gcc gcc-c++ ncurses-devel bison`
  - `dnf install doxygen.x86_64`



- インストール：`make && make install`
- リブの配置：`ln -s /usr/lib/libopencc.so.1.1 /usr/lib64/libopencc.so.1.1`
- 結果確認：`opencc --version`



- 言語パッケージをダウンロード`cd /work && git clone https://github.com/man-pages-zh/manpages-zh && cd manpages-zh`(中国語简体字の例)
- 設定：`autoreconf --install --force`
- makeファイル作成：`./configure --disable-zhtw --prefix=/usr/local/zhman`
- ビルド＆インストール`make && make install`
- 別名を定義`alias cman='man -M /usr/local/zhman/share/man/zh_CN'`
- 中国語マニュアルを開く：`cman man`