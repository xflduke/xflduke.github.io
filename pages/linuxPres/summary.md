# Linux 基礎

２０２１年５月２２日　杜

* TOC {:toc}

## **Linux 概念紹介**

## １．主なOS家族

![image](asserts/image/linux-history.png )

## ２．linuxのの名前について

- linux kernel
- linux Distribution（ディストリビューション）
- xx系 linux

### linux kernel

![image](https://get.wallhere.com/photo/Linus-Torvalds-Linux-Nvidia-middle-finger-1380653.jpg)

### リーナス・トーバルズによって開発が開始された、GPLライセンス採用のOSカーネル、主に以下の機能が持っている

- プロセス管理
- メモリ管理
- デバイス管理
- システムコール

### linux distribution（ディストリビューション）

### kernelとOSを構成するその他のソフトウェアを組合せ  

例：

- パッケージの管理
- インストール方式
- システム構成

### xx系 Linux

1. debian系
2. slackware系
3. redhat系
4. Enoch系
5. Arch系
6. その他

### repos（リポジトリ）

### linuxのパッケージの集合的に保存する場所

- 特定のdistributionのLinuxは対応のreposから各種ソフトを取ってインストール
  - 商用リポ、非営利組織のリポ
  - 本体、ミラー

## linuxのバージョン

### 1.0~2.6.39時代

#### A.B.C.D形式

- A：方向性が変化がある大きな変更
- B：重大な変更
  - 偶数は安定版
  - 奇数は開発版
- C：軽微の変更（バグやドライブなど）
- D：軽微の変更（ほぼ緊急バグ）

### 3.0~時代

#### major.minor.patch-build.desc形式

- major：メインバージョン
- minor：カーネルバージョン
- patch-build：セキュリティパッケージ
- desc：当該バージョンの特別情報。例↓ 
  - rc：release candidate
  - pp：redhatのテスト版
  - EL：redhatの企業版
  - x86_64：64ビット向け
  - smp：マルチプロセッサ
  - lts：長期サポート版

## パッケージのバージョン(RPM)

### name.version.release.arch.ext

- name：パッケージの名前
- version：バージョン番号
- release：リリース番号
  - **linux-distributionと同じ**
- arch：アーキテクチャ
- ext：拡張子

## 個人のlinux環境の準備（CentOS）

### 今の時代いろんな選択肢

- Cloud Computer Instance
  - AWS、Azures、GCP...
- Virtual Machine
  - VMWare、VirtualBox、Hyper-V、KVM...
- Host Install

### お勧め

- [AWS Cloud](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
  - EC2 12月無料、What You need↓ 
    - Amazon AWS アカウント
    - クレジットカード
    - Market上のCentOSのAMIを使って加速化可能
- Virtual Machine
  - 個人PC
- Host
  - 上級者以外勧めない

### CentOSのバージョンに関して

- CentOS 8
  - 最後のREHL安定版
- CentOS Stream
  - スケジューライング更新方式

### CentOSメディアタイプ（VMやHostのinstall用）

- Full installation Media
  - 約９GByte、必要なパッケージ内包されている
- Minimal installation Media
  - 約２GByte、最小限のパッケージ内包
- Boot Media
  - 約0.７GByte、ブートのみ、インストール中repo設定必要
  - インストール中ネットワーク接続必須

### AWS Cloudのlinux環境の準備（Step1）

#### CentOS 8のAMIで起動

- EC2で「インスタンス起動」
- AWS Marketplace上「CentOS 8 (x86_64) - with Updates HVM」を選択
- 料金表示画面で「Continue」
- 「確認と作成」⇒「起動」
- 新いキーペアの作成、「20210618CentOS8」で入力
- 「キーペアダウンロード」⇒「インスタンス作成」

### AWS Cloudのlinux環境の準備（Step2）

#### Step2 CentOS 8に接続

- 上記ダウンロードしたキーペアファイルをAWS Cloudshellにuploadする
- EC2で先ほど作成した「CentOS 8」の状態を確認
  - 5分程「ステータスチェック」状態は「2/2 のチェックに合格しました」なら、利用可能
  - AWS CloudShellより下記コマンドで接続
    - `ssh -i "20210618CentOS8.pem" centos@XXX.XXX.XXX.XXX`

### AWS Cloudのlinux環境の準備（Step3）

#### Step3 CentOS 8廃止

- EC2で「インスタンス終了」を忘れずに実施してください。

## 設定関連の知識とFAQ

### VMソフトウェアの設定

### VMのネットワーク設定

- Bridged（ブリッジ）方式　←　勧め
  - VMが独立なIPで動作、host以外でもアクセスできる
- NAT（共用）方式
  - VMが内部IPで動作、hostのみアクセスできる

### 設定（Hostのハードウェア依存、VMのOS起動NGならオフにしてください）

- Hypervisor：HostのOSを透過的にハードウェアのCPUインストラクション実行
- IOMMU：媒体からメモリへの読込はCPUより細かくコントロールではなく、DMAよりロードできる
- side channel mitigations：サイド チャネルの緩和策を無効にすると安定性と性能がアップできる、自端末での検証ではOFFでいい

### VM OSインストール中のコマンド

- IP確認：(ensxx)
  - `ifconfig`
  - `ip addr show`
- ssh有無確認
  - `systemctl status sshd`
    - Active(Running)確認

### ssh無い場合のインストール

- rootへ切替：`su`（rootへ切替後、以下コマンドの先頭のsudoが不要になる）
- パッケージデータベース更新：`sudo dnf update`（必要に応じて）
- sshdのインストール：`sudo dnf install -y openssh-server`
- sshdの自動起動：`sudo systemctl enable sshd`
- sshdの起動：`sudo systemctl start sshd`
- sshdの停止：`sudo systemctl stop sshd`
- sshdの状態確認：`sudo systemctl status sshd`

### Hostからのアクセス

- sshより、`ssh username@VMOSのIPアドレス`
  - username：インストールする際に設定されたユーザアカウント
  - VMOSのIPアドレス：IP確認で取ったIPアドレス
  - 証明書承認が出ている場合、yesをしてEnterキー
- winscpなどのUIリモートアクセスツールより

### FAQ：sshよりrootアカウントをアクセスでき無い

- 管理者権限で`/etc/ssh/sshd_config`を開いて、PermitRootLoginをyesにする
  - sshd再起動：`sudo systemctl restart sshd`
  - sshd状態確認

### FAQ：ホストからVMOSへのPing接続不可

- 事象：ホストからVMOS接続にはタイムアウトエラー発生やpingで応答なし
  - 一時対策
    - selinuxを一旦停止(再起動まで無効)
      - `sudo setenforce 0`
    - firewalldを一旦停止
      - `sudo systemctl stop firewalld`
    - IPアドレスが制限されているか
      - `/etc/hosts.deny`と`/etc/hosts.allow`を確認

### 宿題１

- linuxの発行版に、三つの家族を列挙ください。
  - 各家族にそれぞれ三つのよく知られているディストリビューションをあげてください。

### 宿題２

- CentOS Linux 8の環境を準備ください
- SSHよりアクセスできるように設定ください。

### 宿題１（中国語）

- 请列举出来3中Linux发行家族
  - 在各个家族中分别列举出3个常用的Linux发行版

### 宿題２（中国語）

- 准备CentOS Linux 8环境
- 用SSH完成对CentOS Linux的远程访问

### [アンケート提出](https://forms.gle/1YhqExbK212Wpmtu7)

### [宿題提出](https://forms.gle/1en4nd1MJvWAWpzEA)

## **Linuxコマンド、エディター、シェル**

## ワークフォルダを作成

- 目標：指定場所に作業フォルダを作成

## 必要な知識

### パスについて

- パスの表記
  - `.`：カレントディレクトリ
  - `..`：一つ上のディレクトリ
- 絶対パス：階層構造の頂点（最上位階層）からの位置関係
  - 例：ローカルパスやリモートパスがあり
    - `/usr/duke/`
    - `file:///c:/xxx/xxx/`
    - `https://xflduke.github.io/`
- 相対パス：階層構造の現在位置の相対関係
  - 例：現在の位置は`/home/duke/`の場合
    - `/root/`をアクセスする際に、相対パスは`../../root/`となります
      - ※この際の絶対パスアクセス方法を考えてください
    - 現在フォルダのindex.htmlファイルの有無を確認したい場合
      - `file ./index.html`で確認する。
        - 設定より、`file index.html`でもアクセスできる場合がある。※

### Linuxの各ユーザのホームフォルダ（Windowのユーザフホームォルダと類似のもの）

- 変更ができますので、ここではCentOS8での規定値を例で説明
  - 一般的に`/home/[username]`を指定している

### 利用されるコマンド

- 階層構造の中に位置移動
  - `cd [絶対パス｜相対パス]`
- フォルダ作成
  - `mkdir [-p] [フォルダパス]`
- ファイル作成
  - `touch [ファイルパス]`
- 現在所在位置の確認
  - `pwd`

### 演習

- ユーザホームフォルダの直下にをworkフォルダを作成
- linuxCourseフォルダにwork1.shのファイルを作成
- 豆知識：`~`は現在ユーザのホームディレクトリを表すメタキャラクタ

## コマンドに関する知識

### 準備できた環境に、講義を見ながら操作してみてください。

### コンソールの基本使い方个：MACOSでは、Ctrlはコンソール操作向けのCommandの理解でいいです。

- キー操作
  - `Tabキー`：コマンドやパスを補完する
  - `Ctrl＋A、Ctrl+E`：入力中のコマンドラインの先頭、最後へカーソルを移動する
  - `Ctrl+C`：実行中処理中断する
  - `Ctrl+S、Ctrl+Q`：画面への出力を一時停止と再開
  - `Ctrl+Z`：処理を一時停止し、バックグラウンドへ移動

### コマンドの記述

- 一般記述方：`コマンド [オプション] [引数]`
- 複数コマンドの実行
  - `コマンド１;コマンド２`：コマンド１に続いてコマンド２を実行
    - 例：`cd ~;ls`
  - `コマンド１&&コマンド２`：コマンド１が正常終了した時のみコマンド２を実行
    - 例：`cd ~&&ls`
  - `コマンド１||コマンド２`：コマンド１が正常終了しなかった時のみコマンド２を実行
    - 例：`cd /home/notExsit||cd ~&&ls`
  - `コマンド > ファイル`：コマンドの実行結果をファイルに出力（上書き）
  - `コマンド >> ファイル`：コマンドの実行結果をファイルに出力（追記）
  - `(コマンド１;コマンド２)`：順次実行、結果は同一で出力
    - 例：`(date;pwd;ls -l) > dailyZZ.log`

### 同一ユーザのコマンド実行履歴の参照

- コマンド：`history`
  - `!履歴番号`：指定番号のコマンドを実行
  - `!!`：直前に実行下コマンドを再実行

### コマンドのマニュアル（manコマンド）について

#### linuxでの各種コマンド対応のマニュアルは`man -w`に格納されていて、不明等があれば以下から参照ください。

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
- マニュアルで表示された言語
  - 必要に応じて言語パッケージをインストール
    - `dnf -y install langpacks-ja`：日本語パッケージのインストール
    - `dnf -y install langpacks-ja`：日本語パッケージのインストール
    - `dnf list langpacks-*`：利用可能な言語パッケージ一覧を出す
    - `localectl set-locale LANG=ja_JP.UTF-8`：システム全体の言語を変える
    - `source /etc/locale.conf`：有効化
    - `echo $LANG`：確認
  - 利用可能なロケールを確認
    - `locale -a`
    - `dnf -y install man-pages-zh-CN`
  - 指定の言語のマニュアルを開く
    - `LANG=zh_CN man ls`

#### コマンドやドキュメントの位置について

- `which コマンド名`：指定コマンド所在の絶対パスを表示
- `whereis コマンド名`：指定コマンドのバイナリファイル、ソースコード、マニュアルファイルの絶対パスを表示

### 他言語のマニュアルのインストール

#### REHLの８では日本語や中国語のマニュアルパッケージはまだリポジトリに取り込んでいない  手動コンパイラーしてインストールが必要

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

## ファイル操作コマンド

### ディレクトリ内容を表示

- `ls [-a][-l][-t][-r]`：ディレクトリ内のファイル情報確認
  - `[-a]`：先頭が．の全てファイルを表示
  - `[-l]`：ファイルの詳細名情報を表示
  - `[-t]`：日付順で表示
  - `[-r]`：表示順を逆にする

## 演習：ディレクトリ中に最新のファイル詳細情報を一番下に表示する

### ファイル移動

- `cp [-i][-p][-r][-d][-a]`：ファイルコピー
  - `-i`：上書きを確認する
  - `-p`：コピー元の属性を保持
  - `-d`：ソフトリンクをリンクのままコピー
  - `-a`：`-dpR`と同じ意味
- `mv`：ファイル移動
- `mkdir [-m][-p]`：フォルダ作成
  - `-m`：指定アクセス権限のフォルダ作成
  - `-p`：親フォルダも同時に作成
- `rmdir [-p]`：フォルダ削除
- `rm [-i][-r][-f]`：ファイル削除`[削除前に確認][子含む][確認なし削除]`
- `touch`：ファイルのタイムスタンプを変更
  - 一般てはファイル作成用
- `file`：ファイルの種別詳細情報を表示

### 演習（バックアップ）

- `~/work/work1.sh`を`~/backup/work/work1.sh`へコピー
- `~/work/work1.sh`のファイルを削除

### エディター

#### nanoについて

- `nano ファイルパス`
  - コマンド存在しない場合：`dnf -y install nano`.
  - `nano`のイメージ
![nanoイメージ](../asserts/image/nano.png)
- メタキーの説明
  - Windows：`^キーはCtrlとキー同時押下、M-キーはAltとキー同時押下`
  - MacOS  ：`^キーはCtrlとキー同時押下、M-キーはEsc押下後キー押下`

#### viについて

- コマンドモード
- 編集モード
![vimキー配置図](../asserts/image/vim_keyboard.jpg)
![vimヘルプ](../asserts/image/vim_help.jpg)

#### その他エディター：Emacs ← 興味があれば勉強してください

#### 演習１：`~/work/`配下に14lines.txtを作成、以下の文字を入力

That this huge stage presenteth nought but shows  
Whereon the stars in secret influence comment;

## テキスト処理

### ファイル内容表示

- `cat [-n]`：ファイル内容を表示
  - [-n]：行番号表示
- `head [-n 行数]`：先頭から指定行数分表示
- `tail [-n 行数][-f]`：末尾から指定行数分表示
  - `-f`：ファイルの末尾に追加された行を表示続ける

### 演習：`/var/log/messages` の出力内容を監視する

<!--`tail -200f /var/log/system.log`-->

### ファイル統計

- `wc [-c][-l][-w]`：ファイルのバイト数、行数、単語数を表示

### その他コマンド

- `cut file`：ファイルの各行から指定下フィールドを取り出す
- `paste file1 file2 ...`：一つ以上のファイルを行ごとに水平連結
- `tr [-d][-s] [文字列１] [文字列２]`：文字列変換
- `sort [-b][-f][-r][-n] [+開始位置 [-終了位置]] [ファイル名]`
- `split [- 行数]`：指定されたサイズでファイル分割
- `uniq [-d][-u]`：ファイル中に重複行を調べ

### コマンドの組合せ及び出力

#### 標準入出力について

- 標準入力：デフォルトはキーボード
- 標準出力：画面（コンソール）
- 標準エラー出力：画面（コンソール）

#### パイプ

- 概念：コマンドの出力結果（標準出力）次のコマンドの標準入力に渡す
- 使い方：`コマンド１ | コマンド２`
- 演習：指定ディレクトリ直下のファイルの数知りたい<!-- `ls | wc -l` -->
- 演習：書込み中のファイルに指定キーワードの出力を監視<!-- `tail -200f /var/log/messages | grep login` -->

#### teeコマンド

- 使い方：コマンドの実行結果をファイルに保存するとともに標準出力に渡す
  - アプリの実行結果をコンソール見ながらファイルに出力
- 例：`ls -l | tee java_version.log`

#### xargsコマンド

- 使い方：コマンドの実行結果を引数に指定して、与えられたコマンドを実行
  - `コマンド１ | xargs コマンド２`
- 演習：指定ディレクトリ直下のファイルごとの行数を知りたい
<!-- `find . -type f | xargs wc -l` -->
<!-- `ls | xargs wc -l | grep -v ^wc` -->

#### リダイレクト

- 概念：コマンドの実行結果を指定のストリーム（ファイル等）へ出力
  - 使い方：`コマンド１ [リダイレクト] ストリーム（ファイルパスなど）`
  - 例：`ls -l > filelist.log`
  - 主なリダイレクトオペレーター
    - `>,>>,2>,2>>,&>,&>>`
    - `コマンド１ > 標準出力 2>&1`：標準出力と標準エラー出力を書込み
    - `コマンド < 終了文字`：終了文字が現れるまで標準入力へ送る

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

### findの利用例

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

### 演習：/etc/ssh/sshd_config中のコメント行の一覧を出す

 <!-- cat /etc/ssh/sshd_config | grep ^# -->

### 演習：/etc/ssh/sshd_config中のコメントではない行の一覧を出す

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
  - 関数fun1の結果を出力して、正常終了

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

### [アンケート提出](https://forms.gle/VkVu5ZYHVdi7WG877)

### [宿題提出](https://forms.gle/DKfohEPoRHYNgEm78)## コマンドの利用例

## **Linux As a Service**

## ユーザとグループの認識

### 目的：ユーザとグループの管理、権限設定の技能学習

### ユーザに関する

- `/etc/passwd` に管理している
- user:x:1000:1002:comment:/home/user:/bin/bash
  - `user`：アカウント名
  - `x`：パスワード位、実際の保持場所→`/etc/shadow`
  - `1000`：UID、ユーザを識別のID
    - rootユーザは必ず０、０〜９９は一般的にシステム管理アカウントで利用
    - 一般的に普通のユーザは１０００からスタート
    - `1002`：GID、ユーザのプライムグループを識別のID
    - `comment`：なんでもいい、メモ情報
    - `/home/user`：ホームディレクトリ
    - `/bin/bash`：ユーザがログインしたり新たにシェルを開いた際に起動されるシェルの絶対パス

### グループに関する

- `/etc/group`ファイルに管理している
  - 書式：`groupName:x:1002:groupMembers`
  - x`：パスワード位、実際の保持場所→`/etc/gshadow`
    - 設定されたら、グループ外のユーザをこのグループへ切替（newgrp）の際にパスワードが必要

### コマンド

- `useradd [-c コメント][-d ホームディレクトリパス][-g GID][-u UID][-s シェルパス]`
  - GIDを指定しないと、自動的に同名のグループを作成（userdelも同じ）
- `usermod [オプション][-L ロック対象ユーザ][-U アンロック対象ユーザ]`
- `userdel [-r]`：`-r`はホームディレクトリも削除
- `passwd [-l][-u] ユーザ`：パスワード「ロック」「アンロック」「変更」
- `groupadd グループ名`
- `groupmod [-g 新GID][-n 新グループ名] グループ名`
- `groupdel グループ名`
- `gpasswd [-a][-d][-A] アカウント名 グループ名`：ユーザをグループに`[追加][削除][プライム指定]`
- `chage [-i] アカウント`：アカウントパラメータ表示や変更
- `id [-g][-G][-n][-r][-u]`：ユーザ情報表示`[プライムGID][所在GIDs][名前表示][実際ID][アカウントID]`
- `whoami`：現在アカウント名前を表示
- `groups アカウント名`：=`id -gn アカウント名`
- `newgrp グループ名`：指定グループをプライムへ一時切替、新たなbashプロセスが作成、終了まで維持
- 管理者権限を実行できるsudoersについて
  - `visudo`で`/etc/sudoers`から確認できる
- 管理権限でコマンドを実行について
  - `sudo コマンド`：コマンドの先頭にsudoを追加
- 他のユーザに切り替え
  - `su [user]`：指定ユーザ権限に切替え、省略の場合はroot
  - `su - [user]`：環境設定を含めて指定ユーザに切り替え

### 演習（アカウント）

- 以下のアカウントを作成する
  - プライムグループ：toyosu
  - 所在グループ：tokyo
  - ユーザ名前：自分の名前
  - ホームディレクトリ：`/home/自分の名前`

### 権限について

- `ls -l`：コマンドでの実行結果にファイルの左側に`-rwxrwxrwx`の表現の説明
  - `[ファイルタイプ][所有者権限][グループ権限][その他ユーザ権限]`
  - 先頭１桁：`-、l、d`の三種類
    - `-`：普通のファイル
    - `l`：ソフトリンク（シンポンリンク）
    - `d`：ディレクトリ
    - `b or c`：IO設備（byteとcharacter）
- `rwx`に関する説明
  - `r`：読込可能：数値４（二進制：100）で表す
  - `w`：書込可能：数値２（二進制：010）で表す
  - `x`：実行可能：数値１（二進制：001）で表す
    - ディレクトリの場合はパスに入るは可能
  - 質問：`drwxr--r--`の権限は？
  - 質問：`-rwxr-xr--`の権限は？
  - `rwx`の数値表記：それぞれの代表の数値の合算で表示
    - 例：`rw-`の数値表示は`6`
    - 例：`r-x`の数値表示は`5`
    - 例：`---`の数値表示は`0`
  - 質問：`rwxr--r--`の数値表現は？
  - 質問：ファイルの`664`の意味は？

### 演習：所有者と所在グループのみから実行可能  

所有者のみが編集可能、全てのユーザが読込可能なシェルファイルを作成

### その他（権限）

- `rwsrwsrwt`の設定について
  - `t`：作ったユーザのみ削除可能
    - 利用例：`/tmp`
  - `s`：実行する際に、s所在ユーザ／グループで実行
    - 利用例：`/bin/passwd`
- `umask`：該当ユーザのデフォルト権限を設定## ファイルシステム階層標準について

### 目的：標準構造の理解、パッケージインストールの各種資材の設置

### よく利用されるパス(FHS)

- `/bin`：基本的なコマンドの配置場所、例：cdコマンド
  - 実際の位置は`/usr/bin`
- `/sbin`：システム管理に必須のコマンドの配置場所、例shudownコマンド
  - 実際の位置は`/usr/sbin`
- `/etc`：システムやアプリの設定情報、スクリプトの設定位置
  - 質問：sshの設定ファイルはどこに格納している？
- `/lib`：共用ライブラリやカーネルモジュールの配置場所
  - 実際の位置は`/usr/lib``/bin、/sbin`の各種コマンドが必要となるライブラリもここに配置している
- `/opt`：パッケージ管理の仕組みを使ってプログラムがインストールされるディレクトリである
  - 手動インストールの際にもここに配置がほとんどです（拡張アプリケーション・ソフトウェアパッケージをインストールする場合）
- `/var`：ログ、キャッシュ等が格納している
  - `/var/cache/`
  - `/var/lock/`
  - `/var/spool/`：プリンタ等の
  - `/var/log`：ログファイルの位置
  - `/var/run`：アプリケーションの実行プロセスIDのデフォルト格納位置
- `/usr`：コマンドやユーティリティなどの配置位置
  - `/usr/bin`、`/usr/sbin`、`/usr/lib`
  - `/usr/local`：システム管理者がソフトウェアをローカルにインストールする場所
  - `/usr/share`：x84やx86_64といったシステムアーキテクチャに依存しないファイルの配置場所
  - `/usr/src`：ソースコードの格納位置

### ハードリンクとソフト（シンボリック）リンクに関して

![リンクについて](../asserts/image/link_type.png)

- `ln [-s][-P] リンク元パス リンク名`
  - `-P`：ハードリンク
    - デフォルトオプション
    - 同一ファイルシステムに存在が必要
  - `-s`：ソフトリンク
  - 演習：同じファイルに対してソフトリンクとハードリンクをそれぞれ作成

### その他（FHS）

- `/dev`：デバイスファイル
- `/proc`：カーネル内部の情報にアクセスするための仮想的なファイルシステム
- `/root`：スーパーユーザのホームディレクトリ
- `/home`：ユーザごとのホームディレクトリ
  - `/home/bin 、　/home/.local/`：一般ユーザがプログラムをインストールする場所
- `/boot`：起動に必要な設定やカーネルイメージの格納場所、起動時にBIOSの制限を受けないようにするため、ルートファイルシステムとは別に、ディスクの先頭付近に配置されることがある
- `/media`：DVDなどのマウントポイントの配置場所
- `/mnt`：一時的にマウントするファイルシステムのマウントポイント
  - 外接HDDなどの一般的にマウント場所
  - マウント一覧は`/etc/fstab`を参照
  - 一時マウントを含むのマウント一覧は`/etc/mtab`を参照
- `/tmp`：一時ファイルの格納位置、全てのユーザが読書き可能のように設定している

## パッケージのインストール

### 管理ツールよりリポジトリからインターネット経由でのインストール

### 演習：Apache httpdのインストール

- リポジトリの設定
  - `/etc/yum.repos.d`：配下に追加や削除は可能
- `yum`のコマンド：`yum [オプション] [サブコマンド] [パッケージ]`
- 操作
  - `check-update`：更新ありのパッケージリスト表示
  - `update [パッケージ名]`：指定パッケージをアップデート
    - 指定なしの場合はすべてのパッケージをアップデート
  - `install [パッケージ]`：指定のパッケージをインストール
  - `remove [パッケージ]`
- 検索
  - `info package`：パッケージの情報を表示
  - `list`：全てのパッケージ情報をリスト
  - `repolist`：現在利用中のリポジトリ一覧を表示
  - `search キーワード`：パッケージ情報をキーワードで検索
  - `search all キーワード`：パッケージ名及び説明文等全てを検索
  - `groups list`：パッケージグループをリスト表示する
  - `groups install group`：指定下グループをインストールする
- `dnf`のコマンド：`yum [オプション] [サブコマンド] [パッケージ]`
  - `yum`の利用方法とほぼ一緒

### Apache httpd 2.4のパッケージをインストール

### httpdのインストールと起動

- インストール：`dnf -y install httpd-2.4.37`
- 状態確認：`systemctl status httpd`
- 起動：`systemctl start httpd`
- 自動起動有効：`systemctl enable httpd`
- 設定ファイルを確認＆ホームページ作成
  - ルートディレクトリ確認：`cat /etc/httpd/conf/httpd.conf | grep DocumentRoot`
  - ホームページ作成：`vi [ルートディレクトリ]/index.html`
    - `<h1>Hello World!</h1>`を入力して保存
  - 結果確認：`IPをアクセスして、結果画面を確認`

### その他：Javaのインストール

- OpenJDK-1.8のインストール
  - `dnf install java-1.8.0-openjdk`

### ネットワークが直接接続できない環境でのパッケージインストール

- 方法１：`dnf localinstall [xxx.rpm]`
  - システムバージョン対応のRPMを探すが必要（注意点は１回目の講義を参照）
- 方法２：`ダウンロードして配置する`

### 演習：Apache Tomcat9のインストール

- tomcatのパッケージをダウンロード
  - ホストマシン（WindowsまたはMacOS）へ切り戻し
    - `curl https://ftp.riken.jp/net/apache/tomcat/tomcat-9/v9.0.46/bin/apache-tomcat-9.0.46.tar.gz --output tomcat9.tar.gz`
    - `scp tomcat9.tar.gz root@[CentOSのIPアドレス]:/opt/`
      - windows環境にはwinscpが利用可能
- パッケージ解凍及びフォルダ配置
  - フォルダを作成：`mkdir -p /opt/tomcat9`
  - `tar -C /opt -xf tomcat9.tar.gz`：解凍
  - `ln -s /opt/tomcat-9* /opt/tomcat9`：リンク作成
  <!-- - `mv *tomcat-9* tomcat9`：フォルダー名前変更 -->
- `mkdir -p /var/tomcat9/`：作業フォルダを作成
- `ln -s /opt/tomcat9/logs /var/tomcat9/logs`：ログファイルのリンク
- `mkdir -p /etc/tomcat9`
- `ln -s /opt/tomcat9/conf /etc/tomcat9/conf`：設定ファイルのリンク
- `mkdir /run/tomcat9`
- `tomcat`ユーザ作成と権限設定
  - `userdd -M -s /sbin/nologin tomcat`：ホームディレクトリ不要、ログイン不可
  - `chown tomcat:tomcat -R /opt/tomcat9`：所有者をtomcatへ変更
  - `chown tomcat:tomcat -R /var/tomcat9`
  - `chown tomcat:tomcat -R /etc/tomcat9`
  - `chown tomcat:tomcat -R /run/tomcat9`
- システムサービスとして追加
  - javaのパスを探す：`ls -l /usr/lib/jvm/`
  - [unit](./linux3/tomcat@.service)ファイル作成
  - `systemctl daemon-reload`：リロード
  - `systemctl enable tomcat@9.service`：有効にする
  - `systemctl start tomcat@9.service`：起動する

<!-- 
  - `firewall-cmd --add-port=8080/tcp --permanent`
-->

- 結果確認
  - `curl 127.0.0.1:8080`

### rpmの常用コマンド

- `rpm [-i|-U|-F|-e|-q]`：インストール、アップグレード／インストール、アップグレード、アンインストール、検索
  - `-i`：--install
  - `-U`：--upgrade
  - `-F [--nodeps]`：--freshen
  - `-e [--nodeps]`：--erase
  - `--nodeps`：依存関係無視
  - `-q [-a][-f ファイル名][-p パッケージファイル名][-c][-d][-i][-l][-R][--changelog]`
    - `-a`：インストールずみの全てのパッケージを表示
    - `-f ファイル名`：指定したファイルを含むパッケージ名を表示
    - `-p パッケージファイル名`：対象としてパッケージファイルを指定する
    - `-c`：設定ファイル
    - `-d`：ドキュメント
    - `-i`：パッケージ情報表示
    - `-l`：パッケージに含まれるファイルを表示
    - `-R|--requires`：パッケージが依存しているファイル等を表示

### 宿題

- Apache httpd →　Apache TomcatのAJP経由の連携
- 以下のいずれのサービスのインストール
  - データベース（PostgreSQL等）
  - メールサーバ（Postfix等）
  - ネーミングサーバ（Bind等）
  - NTPサーバ（chrony等）
  - リバースプロキシ（nginx等）
  - ファイル改ざん監視（Tripwire等）
  - その他色々

## その他システム中よく使われるコマンド

### システム関連（性能、メモリ、サービス、システム管理）

- ディスク容量
  - `df -h`：残りの容量
  - `df -i`：索引区の残る容量
- 性能やプロセスの確認
  - `ps aux`：プロセスを表示
  - `top -s`：性能指標を定期的に表示
  - `vmstat -w`：システム性能監視
- ネットワーク
  - `ping IPアドレス`：指定IPアドレスに接続確認
  - `traceroute IPアドレス`：指定IPへのルート表示
  - `route [add][del]`：ルーティング表示、追加、削除
    - `/etc/sysconfig/network-scripts/`：再起動でも有効の場合はここに追加
  - `netstat -anop`：開放されているポートの確認
  - `ip addr show`：IPアドレスの確認
- ファイアウォール
  - `systemctl [enable|disable|start|stop|status] firewalld`
  - ルール追加：`firewall-cmd --add-port=ポート番号/プロトコル(tcpなど) --permanent && firewall-cmd --reload`
- セキュリティ
  - 一時的に無効させ：`sudo setenforce 0`
  - 有効性変更：`/etc/selinux/config`を修正（再起動要）
  - 状態確認：`sestatus`
- タスク
  - `crond`：定期実行のプロセス
    - フォーマット：`* * * * *`：：`分 時 日 月 週 コマンド`
    - `*`ごとの用語ごとの用語
      - `,`：例挙、`-`：範囲、`*`：任意、`%`：毎にに
      - 例：`*10 8-18 * * 1,2,3,4,5 curl xx` 
  - `crond`：定期実行のプロセス
    - 設定ファイル
      - `/etc/crontab、/etc/cron.d`：システムレベル
      - `/var/spool/cron`：ユーザレベル
    - `crontab [-e|l|r|u]`：作成、一覧表示、削除、実行ユーザー指定、ファイルから読込、時間パラメー実行
  - `atd`：一回のみ実行の計画任務任務
    - `at [-m|c|q|f|t]`：完成時メール、標準出力に、隊列指定、時間パラメータ
    - `atq`：隊列を表示隊列を表示
    - `atrm`：削除

<!--
# システム自動化

- サービス紹介
- 自動化スクリプト
-->

### [アンケート提出](https://forms.gle/RWhY2Zud4H9KRdeh9)

### [宿題提出](https://forms.gle/ft53Go9iUGWXE4Ar7)
