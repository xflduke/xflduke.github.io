# OPSM — オンプレ販売管理システム（教育用サンプル）

> **重要：本デモは教育用です。**
>
> - **harness（モデル以外の一切：ルール / 技能 / ツール / フック / サブエージェント）が全工程で品質を担保する流れ**を見せるサンプルであり、特定の製品とは無関係です。
> - **技術スタックは"仮置き"**：Python/FastAPI/PostgreSQL は流れを見せるために選んだだけ。
>   実プロジェクトでは**着手前に AI と相談し、現場環境（チーム技能・既存資産・コンプラ・運用制約）に合わせて選定**してください。**選定そのものが harness の一部**です。
> - **本工程は適当に簡略化**しています（規約・チェックリストは簡版）。実工程は各社の process（レビュー手順・承認・分岐戦略・リリース）に合わせて拡張してください。

## 全体像

販売管理ドメイン（見積/受注/発注/在庫/請求/入金/マスタ）のうち、**受注（Order）を仕様→設計→実装→テスト→デプロイまで貫通**実装し、harness が各フェーズでどう品質を担保するかを示します。

## 実行（最小：domain テストのみ・依存最少）

```bash
python -m pytest tests/test_order_domain.py -q
```

純 Python のドメインテストは PostgreSQL なしで動きます（hook / CI でも同じセンサーを使用）。

## 実行（API 統合・任意）

```bash
pip install -e ".[dev]"
pytest -q -m integration
```

## 実行（オンプレ デプロイ・任意）

```bash
cp ops/.env.example ops/.env  # 秘密値を実値に変更
cd ops && docker compose up -d
curl http://localhost/healthz
```

## ディレクトリ

- `AGENTS.md` / `CLAUDE.md` / `src/app/CLAUDE.md`：メモリ層（権威 + 薄壳 + ネスト）
- `.claude/`：commands / agents / skills / hooks / output-styles / settings / statusline
- `.mcp.json`：MCP（構内 PostgreSQL 読取・docs 文件サーバ示例）
- `docs/`：specs（受注貫通 + 4 桩） / design（受注 + ADR） / glossary
- `src/app/`：api / services / repositories / domain（純 Python・貫通）
- `tests/`：test_order_domain（純 pytest 必達） / test_orders_api（integration）
- `ops/`：docker-compose / nginx / .env.example / runbook
- `.github/workflows/ci.yml`：ruff + mypy + pytest（hook と同一センサーを CI で再実行）

## harness を見るポイント

- **Feed-forward**：AGENTS.md / commands / agents / skills（references を厚く分離）
- **Feedback**：hooks（format / run-tests / secret-scan / no-external-net / notify） + CI（同一センサー）
- **spec-driven**：未承認の仕様で実装しない（commands で強制）
- **on-prem 制約**：外部接続を hook で遮断、秘密は env、依存は許可リスト
