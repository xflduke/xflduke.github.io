---
name: onprem-constraints
description: オンプレミス（構内）運用の制約を集約。外部 SaaS/クラウド呼び出し禁止、データ駐留、秘密は env、依存は許可リスト。実装/レビュー時に参照。
---
# onprem-constraints

## 鉄則
1. 外部ネットワークへの egress は原則禁止。例外は構内ホスト（localhost / private IP）のみ。
2. 秘密情報（DB パスワード、トークン）は **環境変数 / `.env`** から取得し、コードに残さない。
3. 依存パッケージは **許可リスト**で管理。新規追加は ADR/レビュー必須。
4. ログには PII / 秘密を出さない。
5. データは構内ストレージに駐留。クラウドストレージへ転送しない。

## 強制手段
- hook `no-external-net.sh`（PreToolUse・Bash）：curl/wget/外部 install を遮断。
- hook `secret-scan.sh`（PostToolUse・Edit / UserPromptSubmit）：API キー風文字列を検出。
- `.claude/settings.json` の `permissions.deny`：WebFetch / curl / wget / pip install / .env 読取禁止。
- CI で同一センサーを再実行（バイパス防止）。
