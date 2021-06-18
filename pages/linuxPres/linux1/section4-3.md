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
  
