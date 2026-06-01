# Security Checklist（簡版）

## 秘密管理
- [ ] DB パスワード / トークン / API キーがコード・設定ファイル・コミットに含まれていない。
- [ ] `pydantic-settings` 経由で env から読み取り、`.env` は `.gitignore` 対象。

## オンプレ制約
- [ ] 外部ネットワーク呼び出しがない（hook `no-external-net` で確認）。
- [ ] 依存パッケージが許可リスト（`pyproject.toml`）に含まれる。
- [ ] データが構内に駐留（外部ストレージへ送信しない）。

## 入力検証
- [ ] すべての API 入力が Pydantic スキーマで検証される。
- [ ] SQL は SQLAlchemy のパラメータ化クエリのみ（生 SQL 禁止）。

## 権限
- [ ] 認証 / 認可境界が明確（OPSM では教学用に最小限、本番は IdP 連携想定）。
- [ ] 操作ログに利用者・時刻・対象を残す。

## ログ
- [ ] PII / 秘密が出力されていない。
- [ ] 例外メッセージに秘密が含まれない。

## 重大度
- Critical（merge 不可） / High / Medium / Low。
