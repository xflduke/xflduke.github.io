# Test Viewpoints（簡版）

## 原則
- **受容基準＝テスト**。仕様番号をテストにコメントで紐付け。

## 観点
1. 正常系: 仕様の主シナリオを網羅。
2. 異常系: 不正入力・権限違反・状態違反。
3. 境界: 0 / 1 / 上限 / 下限 / 空 / オーバーフロー。
4. ドメイン不変量: 計算式・状態遷移の不変条件を直接アサート。
5. 冪等: 同じ入力で同じ結果（リトライ安全）。
6. 回帰: バグ修正のたびに失敗するテストを残す。

## レイヤ別
- `domain/`: 純 pytest（DB/HTTP 不要）。最も多く書く。
- `services/`: ユースケース単位、リポジトリは fake で代替可。
- `repositories/`: SQLite in-memory 統合（`@pytest.mark.integration`）。
- `api/`: FastAPI TestClient（`@pytest.mark.integration`）。

## カバレッジ目標
- domain: 受容基準 100% カバー。行カバレッジは結果指標。
