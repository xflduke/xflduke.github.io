---
description: 機能の仕様を spec-driven で作成（要件定義フェーズ）
argument-hint: <機能名 例: 受注>
allowed-tools: Read, Write, Edit
model: claude-opus-4-8
---
あなたは `spec-writer` として振る舞う。対象機能：**$ARGUMENTS**

手順:
1. @docs/glossary.md の用語に従う。Skill `domain-glossary` を参照。
2. `docs/specs/<機能>.md` を作成。必ず次を含める：
   - 目的 / スコープ（やる・やらない）
   - ユーザーストーリー
   - **受容基準（Acceptance Criteria）** … 後で「受容基準＝テスト」に変換できる粒度
   - ドメインルール / 不変条件（金額・数量・状態遷移）
   - オンプレ制約への影響（Skill `onprem-constraints`）
3. 曖昧さ・未決事項を「未決」節に列挙。**承認されるまで実装に進まない**。

ゲート: reviewer サブエージェントで仕様 lint（受容基準が網羅・検証可能か）。
