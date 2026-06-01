# Coding Conventions（簡版）

> 教学用のサンプル。実プロジェクトでは各社のスタイルガイドへ拡張すること。

## 1. レイヤと依存
- `api/`: FastAPI ルータ。Pydantic スキーマで入出力を検証。**ビジネスロジック禁止**。
- `services/`: ユースケース調整、トランザクション境界。
- `repositories/`: 永続化のみ。SQLAlchemy はここに閉じる。`domain` を返す。
- `domain/`: エンティティ・値オブジェクト・不変条件。**FastAPI/DB 非依存（純 Python）**。
- 依存は内向き：`domain` は誰にも依存しない。

## 2. 命名
- ファイル: snake_case。クラス: PascalCase。関数/変数: snake_case。定数: UPPER_SNAKE。
- ドメイン用語は @docs/glossary.md と一致させる（例: `Order`, `LineItem`, `Quantity`）。

## 3. 型注釈
- すべての public 関数 / メソッド / クラス属性に型注釈。
- `mypy --strict` を通すこと。`Any` の使用は最小化。

## 4. エラーハンドリング
- ドメイン違反は `domain/exceptions.py` の固有例外で表現（例: `OrderInvariantError`）。
- api 層で HTTP に変換（`HTTPException`）。例外メッセージに秘密を含めない。

## 5. ロギング
- 構造化ログ（JSON）。PII / 秘密を出力しない。
- レベル: DEBUG（開発のみ）/ INFO / WARNING / ERROR。

## 6. 依存・セキュリティ
- 外部ネットワーク呼び出し禁止（onprem-constraints）。
- 秘密は環境変数（`pydantic-settings` 経由）。コードや設定ファイルにハードコードしない。
- 依存追加は ADR とレビュー。

## 7. テスト
- domain は純 pytest（DB/HTTP 不要）。
- API/DB 統合は `@pytest.mark.integration`。
- 受容基準コメント（仕様番号）を必ず付ける。

## 8. フォーマット
- `ruff format`（line-length=100、target-version=py312）。
- `ruff check`（select: E, F, I, B, UP, S）。
