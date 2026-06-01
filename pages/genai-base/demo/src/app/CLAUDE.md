# src/app/CLAUDE.md — 実装レイヤ固有ルール（ネストされたメモリ）

> 親の @../../AGENTS.md を継承。ここでは `src/app` 配下の実装規約のみ補足。

## レイヤ責務
- `api/`：FastAPI ルータ。**入出力の検証と変換のみ**。ビジネスロジックを書かない。
- `services/`：ユースケース調整。トランザクション境界。`repositories` と `domain` を組み合わせる。
- `repositories/`：永続化のみ。SQL/ORM はここに閉じ込める。`domain` を返す。
- `domain/`：エンティティと**不変条件・計算ルール**。**純 Python、FastAPI/DB 非依存**。

## 厳守
- `domain` から `api`/`services`/`repositories` を import しない（依存は内向き）。
- 金額・数量の計算は `domain` に置き、テストで受容基準を固定する。
- 例外は `domain` のドメイン例外 → `api` で HTTP に変換。
- 詳細規約は Skill `code-standards` を参照。
