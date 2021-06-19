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



- ファイアウォル
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
