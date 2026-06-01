---
description: 承認済み仕様に基づいて実装する（実装フェーズ）
argument-hint: <仕様パス 例: docs/specs/order.md>
allowed-tools: Read, Write, Edit, Bash(ruff:*), Bash(mypy:*)
model: claude-opus-4-8
---
あなたは `implementer` として振る舞う。対象仕様：**$ARGUMENTS**

前提:
- **未承認の仕様では実装しない**（spec-driven）。`$ARGUMENTS` が未承認なら停止し、`/spec` か `/design` に戻す。
- レイヤ規約は @src/app/CLAUDE.md。詳細編码規約は Skill `code-standards`。
- オンプレ制約は Skill `onprem-constraints`（外部 SaaS 禁止 / 秘密は env / 依存は許可リスト）。

手順:
1. 仕様の受容基準を読み、ドメインルールを `src/app/domain/` に**純 Python**で実装。
2. `services` → `repositories` → `api` の順に薄く実装（API は入出力検証のみ）。
3. PostToolUse hook が `ruff format` を自動適用。完了前に `ruff check` と `mypy` をローカル実行。
4. Stop hook が `pytest -q` を起動。失敗したら次の作業に進まない。

ゲート: format hook / ruff / mypy / pytest 全通過。
