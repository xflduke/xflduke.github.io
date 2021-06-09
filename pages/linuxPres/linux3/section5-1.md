
## パッケージのインストール



### ネットワークが直接接続できない環境でのパッケージインストール

 - 方法１：`dnf localinstall [xxx.rpm]`
   - システムバージョン対応のRPMを探すが必要（注意点は１回目の講義を参照）
 - 方法２：`ダウンロードして配置する`



## 演習：Apache Tomcat9のインストール



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
  - [unit](./tomcat@.service)ファイル作成
  - `systemctl daemon-reload`：リロード
  - `systemctl enable tomcat@9.service`：有効にする
  - `systemctl start tomcat@9.service`：起動する
<!-- 
  - `firewall-cmd --add-port=8080/tcp --permanent`
-->



- 結果確認
  - `curl 127.0.0.1:8080`
<!--
### rpmの常用コマンド

- `rpm [-i|-U|-F|-e|-q]`：インストール、アップグレード／インストール、アップグレード、アンインストール、検索
  - `-i`：--install
  - `-U`：--upgrade
  - `-F [--nodeps]`：--freshen
  - `-e [--nodeps]`：--erase
  - `--nodeps`：依存関係無視
-->
<!--
  - `-q [-a][-f ファイル名][-p パッケージファイル名][-c][-d][-i][-l][-R][--changelog]`
    - `-a`：インストールずみの全てのパッケージを表示
    - `-f ファイル名`：指定したファイルを含むパッケージ名を表示
    - `-p パッケージファイル名`：対象としてパッケージファイルを指定する
    - `-c`：設定ファイル
    - `-d`：ドキュメント
    - `-i`：パッケージ情報表示
    - `-l`：パッケージに含まれるファイルを表示
    - `-R|--requires`：パッケージが依存しているファイル等を表示
-->
