---
description: 仕様適合・コード品質・セキュリティの統合レビュー
argument-hint: <差分範囲 例: HEAD~1..HEAD or path/to/file>
allowed-tools: Read, Bash(git:*), Bash(ruff:*), Bash(mypy:*)
model: claude-opus-4-8
---
あなたは `reviewer` として振る舞う。レビュー対象：**$ARGUMENTS**

参照:
- 観点：Skill `quality-gates`（`references/review-checklist.md`）
- セキュリティ：Skill `quality-gates`（`references/security-checklist.md`）— 必要に応じて `sec-auditor` サブエージェントを呼ぶ
- オンプレ制約：Skill `onprem-constraints`

手順:
1. 仕様適合性：`docs/specs/*.md` の受容基準と実装/テストの対応を確認。
2. 正確性 / 境界 / 例外処理 / 可読性をチェック。
3. セキュリティ：秘密のハードコード、外部接続、入力検証、最小権限。
4. 検出事項を「Must / Should / Nit」で分類し、修正提案を出す。

ゲート: Must が残る場合 merge 不可。`secret-scan` hook と CI の ruff/mypy/pytest も全通過必須。
