---
name: quality-gates
description: レビュー / テスト / セキュリティ観点の集約。詳細は references/{review-checklist,test-viewpoints,security-checklist}.md を参照。
---
# quality-gates

精錬原則のみ。詳細チェックリストは `references/` に分離（必要時のみ読み込み）。

- レビュー観点：仕様適合 / 正確性 / 境界・例外 / セキュリティ / オンプレ制約 / テスト網羅 / 可読性。
- テスト観点：正常 / 異常 / 境界 / ドメイン不変量 / 冪等 / 回帰、受容基準＝テスト。
- セキュリティ観点：秘密の env 化 / 依存許可リスト / 最小権限 / 入力検証 / 外部接続なし。

`/review`・`reviewer`・`/test`・`test-engineer`・`sec-auditor` は**同じ references を共有**してドリフトを防ぐ。
