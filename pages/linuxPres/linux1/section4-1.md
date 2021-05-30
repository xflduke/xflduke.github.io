# 個人のlinux環境の準備（CentOS）



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
