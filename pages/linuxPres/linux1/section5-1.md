# 設定関連の知識とFAQ



## VMソフトウェアの設定



### VMのネットワーク設定

- Bridged（ブリッジ）方式　←　勧め
  - VMが独立なIPで動作、host以外でもアクセスできる
- NAT（共用）方式
  - VMが内部IPで動作、hostのみアクセスできる



###  加速化設定（Hostのハードウェア依存、VMのOS起動NGならオフにしてください）

- Hypervisor：HostのOSを透過的にハードウェアのCPUインストラクション実行
- IOMMU：媒体からメモリへの読込はCPUより細かくコントロールではなく、DMAよりロードできる



##  VM OSインストール中のコマンド

- IP確認：(ensxx)
  - `ifconfig`
  - `ip addr show`
- ssh有無確認
  - `systemctl status sshd`
    - Active(Running)確認



## ssh無い場合のインストール

- rootへ切替：`su`（rootへ切替後、以下コマンドの先頭のsudoが不要になる）
- パッケージデータベース更新：`sudo dnf update`（必要に応じて）
- sshdのインストール：`sudo dnf install -y openssh-server`
- sshdの自動起動：`sudo systemctl enable sshd`
- sshdの起動：`sudo systemctl start sshd`
- sshdの停止：`sudo systemctl stop sshd`
- sshdの状態確認：`sudo systemctl status sshd`



## Hostからのアクセス

- sshより、`ssh username@VMOSのIPアドレス`
  - username：インストールする際に設定されたユーザアカウント
  - VMOSのIPアドレス：IP確認で取ったIPアドレス
  - 証明書承認が出ている場合、yesをしてEnterキー
- winscpなどのUIリモートアクセスツールより



## FAQ：sshよりrootアカウントをアクセスでき無い

- 管理者権限で`/etc/ssh/sshd_config`を開いて、PermitRootLoginをyesにする
  - sshd再起動：`sudo systemctl restart sshd`
  - sshd状態確認



## FAQ：ホストからVMOSへのPing接続不可

- 事象：ホストからVMOS接続にはタイムアウトエラー発生やpingで応答なし
  - 一時対策
    - selinuxを一旦停止(再起動まで無効)
      - `sudo setenforce 0`
    - firewalldを一旦停止
      - `sudo systemctl stop firewalld`
    - IPアドレスが制限されているか
      - `/etc/hosts.deny`と`/etc/hosts.allow`を確認
