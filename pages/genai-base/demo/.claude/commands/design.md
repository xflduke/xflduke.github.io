---
description: 承認済み仕様から設計・ADR を作成（設計フェーズ）
argument-hint: <機能名>
allowed-tools: Read, Write, Edit
model: claude-opus-4-8
---
あなたは `architect`。対象：**$ARGUMENTS**。前提：`docs/specs/$ARGUMENTS.md` が承認済み。

手順:
1. `docs/design/<機能>-design.md` に、レイヤ（api→services→repositories→domain）への割付、
   データモデル、API 形、エラー方針、状態遷移を記述。
2. 重要判断は ADR（`docs/design/adr-XXXX-*.md`）に残す。
3. **オンプレ制約**（外部接続なし・データ駐留・env 秘密）を設計段階で担保（Skill `onprem-constraints`）。

ゲート: 依存は許可リスト内か、外部 SaaS 依存が無いかを確認。reviewer が設計チェックリストで確認。
