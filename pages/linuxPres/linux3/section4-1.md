
## パッケージのインストール



### 管理ツールよりリポジトリからインターネット経由でのインストール



## 演習：Apache httpdのインストール



- リポジトリの設定
  - `/etc/yum.repos.d`：配下に追加や削除は可能
- `yum`のコマンド：`yum [オプション] [サブコマンド] [パッケージ]`
- 操作
  - `check-update`：更新ありのパッケージリスト表示
  - `update [パッケージ名]`：指定パッケージをアップデート
    - 指定なしの場合はすべてのパッケージをアップデート
  - `install [パッケージ]`：指定のパッケージをインストール
<!--  - `remove [パッケージ]` -->



- 検索
  - `info package`：パッケージの情報を表示
  - `list`：全てのパッケージ情報をリスト
  - `repolist`：現在利用中のリポジトリ一覧を表示
  - `search キーワード`：パッケージ情報をキーワードで検索
  - `search all キーワード`：パッケージ名及び説明文等全てを検索
<!--
  - `groups list`：パッケージグループをリスト表示する
  - `groups install group`：指定下グループをインストールする
-->



- `dnf`のコマンド：`yum [オプション] [サブコマンド] [パッケージ]`
- `yum`の利用方法とほぼ一緒



## Apache httpd 2.4のパッケージをインストール



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
