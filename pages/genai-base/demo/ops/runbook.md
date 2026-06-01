# Runbook（教学用簡版）

## 起動
1. `cp ops/.env.example ops/.env` 後、`ops/.env` の秘密値を実値に変更（**コミット禁止**）。
2. `cd ops && docker compose up -d`
3. ヘルスチェック: `curl http://localhost/healthz` → `{"status":"ok"}`

## 停止 / ロールバック
- 停止: `docker compose down`
- データ保持で再起動: `docker compose restart`
- 完全リセット（教学用のみ）: `docker compose down -v`

## ログ確認
- `docker compose logs -f app`
- `docker compose logs -f nginx`

## 障害対応
1. ヘルスチェック失敗 → `docker compose logs app` で例外確認。
2. DB 接続失敗 → `.env` の認証情報・コンテナ間ネットワークを確認。
3. 外部接続が必要に見えるエラー → onprem-constraints 違反の疑い。原因のソースを review し、構内代替に切り替え。

## 注意
- 本 runbook は教学用簡版。実プロジェクトでは：監視・バックアップ・キャパシティ・DR・変更管理を追加すること。
