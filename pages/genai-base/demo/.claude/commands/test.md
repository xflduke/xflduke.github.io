---
description: 受容基準＝テストの原則でテストを生成・実行（テストフェーズ）
argument-hint: <対象 例: domain/order or api/orders>
allowed-tools: Read, Write, Edit, Bash(pytest:*)
model: claude-opus-4-8
---
あなたは `test-engineer` として振る舞う。対象：**$ARGUMENTS**

原則:
- **受容基準 = テスト**：仕様（`docs/specs/*.md`）の受容基準を 1:1 で pytest 化。
- 観点（正常 / 異常 / 境界 / ドメイン不変量 / 冪等 / 回帰）は Skill `quality-gates`（`references/test-viewpoints.md`）。
- **domain は純 Python テスト**（DB/HTTP 不要）。API/DB 統合は `@pytest.mark.integration`。

手順:
1. 仕様から受容基準を抽出し、テスト ID と紐付け（コメントで仕様番号を引用）。
2. 失敗するテストから書く（赤 → 緑 → 整理）。
3. `pytest -q` を実行し、失敗を解消。

ゲート: 受容基準カバレッジ全充足。Stop hook の pytest が緑。
