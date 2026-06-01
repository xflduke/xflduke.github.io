---
description: フェーズ着手のキックオフ（サブディレクトリ命名空間例 → /phase:kickoff）
argument-hint: <フェーズ名 例: spec or design>
allowed-tools: Read
model: claude-opus-4-8
---
あなたは進行役。対象フェーズ：**$ARGUMENTS**

このコマンドは `commands/phase/kickoff.md` に置かれており、**サブディレクトリ命名空間**の例として `/phase:kickoff` で呼び出される（Claude Code の命名規則デモ）。

手順:
1. 該当フェーズの入力（前フェーズの成果物）を列挙。
2. 該当フェーズの harness を確認（feed-forward と feedback の両方）。
3. 進行に必要な合意事項・未決事項を整理して提示。
