# linuxのバージョン



## 1.0~2.6.39時代



### A.B.C.D形式

 - A：方向性が変化がある大きな変更
 - B：重大な変更
   - 偶数は安定版
   - 奇数は開発版
 - C：軽微の変更（バグやドライブなど）
 - D：軽微の変更（ほぼ緊急バグ）



## 3.0~時代


### major.minor.patch-build.desc形式

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



# パッケージのバージョン(RPM)



### name.version.release.arch.ext

 - name：パッケージの名前
 - version：バージョン番号
 - release：リリース番号
   - **linux-distributionと同じ**
 - arch：アーキテクチャ
 - ext：拡張子