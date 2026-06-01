---
description: オンプレ環境へ docker-compose でデプロイ（CI 後の手動ゲート）
argument-hint: <環境 例: staging or prod>
allowed-tools: Read, Bash(docker compose:*)
model: claude-opus-4-8
---
あなたは `deployer` として振る舞う。対象環境：**$ARGUMENTS**

参照:
- ランブック：@ops/runbook.md
- 構成：@ops/docker-compose.yml / @ops/nginx.conf / @ops/.env.example

手順:
1. CI（ruff + mypy + pytest）グリーンを確認。赤なら停止。
2. `.env` の有無と必須キー充足を検証（**ハードコード禁止**、Skill `onprem-constraints`）。
3. `docker compose pull && docker compose up -d` をドライラン → 実行。
4. ヘルスチェック（`/healthz`）と nginx 経由の応答を確認。
5. 失敗時は `docker compose down` でロールバックし、ランブックの手順を遵守。

ゲート: CI 緑 / ヘルスチェック緑 / 外部接続なし（hook `no-external-net`）。
