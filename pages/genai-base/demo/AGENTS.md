# AGENTS.md — オンプレ販売管理システム（OPSM）

> このファイルは Claude Code / 互換エージェントが**毎ターン読む権威ルール**です。
> 原則だけを簡潔に置き、**重い参照は Skill / docs に逃がします**（毎回の文脈を膨らませない）。

## ⚠ 本プロジェクトについて（教育用）
- これは **harness（モデル以外の一切：ルール・技能・ツール・フック・サブエージェント）** が
  **全工程で品質を担保する流れ**を見せる**教育用サンプル**です。特定の製品とは無関係。
- **技術スタックは"仮置き"**：Python/FastAPI は流れを見せるために選んだだけ。
  実プロジェクトでは**着手前に AI と相談し、現場環境（チーム技能・既存資産・コンプラ・運用制約）に合わせて選定**すること。選定自体が harness の一部。
- **内容は簡略版**。実工程は各社の process（レビュー手順・承認・分岐戦略・リリース）に合わせて拡張すること。

## ドメイン
販売管理（見積→受注→発注→在庫→請求→入金、マスタ・承認・帳票）。
本サンプルは **受注（Order）** を仕様→設計→実装→テスト→デプロイまで**貫通**実装し、他は雛形に留める。
用語は @docs/glossary.md を参照。

## オンプレミス制約（厳守）
- **外部 SaaS / クラウド API を呼ばない**。データは構内に留める（データ駐留）。
- **秘密情報は環境変数 / `.env`** から取得。**ハードコード禁止**。
- 依存は許可リスト方式。外部ネットワークegress は原則遮断（hook で検査）。

## アーキテクチャ（レイヤ）
`api`（FastAPI ルータ）→ `services`（ユースケース）→ `repositories`（永続化）→ `domain`（エンティティ・不変条件）。
- ドメインの中核ルールは**純 Python**（FastAPI/DB 非依存）で書き、単体テスト可能に保つ。
- 詳細な規約は Skill **`code-standards`** を参照（`references/coding-conventions.md`）。

## ワークフロー（spec-driven）
1. **承認済み仕様が無いコードは書かない**。まず `/spec`。
2. 順序：`/spec` → `/design` → `/implement` → `/test` → `/review` → `/deploy`。
3. 各フェーズに **feedback（センサー）** があり、通過しないと先へ進めない（下記）。

## 品質ゲート（feedback / 迂回不可）
- 実装後：`ruff` 整形 + `ruff check` + `mypy`（hook `format` / CI）。
- 変更後：`pytest -q`（hook `run-tests` / CI）。受容基準＝テスト。
- レビュー：`reviewer` / `sec-auditor` サブエージェント + チェックリスト。
- 観点・チェックリストは Skill **`quality-gates`** を参照（review / test / security）。
- 秘密スキャン・外部接続遮断：hook `secret-scan` / `no-external-net`。

## 参照（重い内容はこちらへ）
- 編码規約 … Skill `code-standards`
- レビュー / テスト / セキュリティ観点 … Skill `quality-gates`
- オンプレ制約の詳細 … Skill `onprem-constraints`
- ドメイン用語 … @docs/glossary.md
