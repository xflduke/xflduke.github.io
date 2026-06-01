# 用語集（Glossary） — 販売管理ドメイン（OPSM）

> 実装・仕様・テストの命名はこの用語と完全一致させる。

| 日本語 | 英語/コード | 説明 |
|---|---|---|
| 見積 | Quotation | 顧客への価格提示。受注の前段階。 |
| 受注 | Order | 顧客から確定した注文。OPSM の貫通対象。 |
| 受注明細 | OrderLine / LineItem | 受注に含まれる商品行（商品・数量・単価）。 |
| 発注 | PurchaseOrder | 仕入先への発注。在庫補充。 |
| 在庫 | Inventory | 倉庫の在庫数量。 |
| 請求 | Invoice | 顧客への請求。受注完了後に発行。 |
| 入金 | Payment | 顧客からの入金記録。 |
| マスタ | Master | 顧客・商品・倉庫などの基準データ。 |
| 顧客 | Customer | 受注先。 |
| 商品 | Product | 受注/発注/在庫の対象 SKU。 |
| 単価 | UnitPrice | 商品 1 単位の価格。 |
| 数量 | Quantity | 単位は商品マスタの単位に従う。負値不可。 |
| 受注ステータス | OrderStatus | `draft` / `confirmed` / `shipping` / `completed` / `cancelled`。 |
| 承認 | Approval | 一定額以上の受注は承認が必要（教学用簡略化）。 |
| 帳票 | Report | 受注一覧・売上帳など。 |
