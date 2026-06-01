# 設計：受注（Order）

> `docs/specs/order.md` を満たすための設計。教学用の簡版。

## レイヤ責務
| レイヤ | 責務 | 主要ファイル |
|---|---|---|
| api | HTTP 入出力検証・変換 | `src/app/api/orders.py` |
| services | ユースケース調整・トランザクション | `src/app/services/order_service.py` |
| repositories | 永続化（SQLAlchemy） | `src/app/repositories/order_repository.py` |
| domain | エンティティ・不変条件・状態遷移 | `src/app/domain/order.py` |

依存方向: `api → services → repositories → domain`（domain は誰にも依存しない）。

## ドメインモデル
```python
class OrderStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    SHIPPING = "shipping"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int      # >= 1
    unit_price: int    # >= 0 (円)

@dataclass
class Order:
    id: str
    customer_id: str
    lines: list[OrderLine]
    status: OrderStatus = OrderStatus.DRAFT
    APPROVAL_THRESHOLD: ClassVar[int] = 1_000_000
```

## 主要ふるまい
- `Order.total()`: 派生計算 `sum(line.quantity * line.unit_price for line in lines)`。
- `Order.requires_approval()`: `total() >= APPROVAL_THRESHOLD`。
- `Order.confirm(approved: bool)`: 状態遷移（AC-5, AC-6）。承認必要かつ未承認なら例外。
- `Order.advance_to_shipping()` / `Order.complete()` / `Order.cancel()`: 状態遷移。
- `Order.add_line(line)`: `DRAFT` のみ許可（AC-7 不変条件）。

## 状態遷移
```
draft ──confirm(approved)──> confirmed ──> shipping ──> completed
  │                              │              │
  └──cancel────────────cancel────┴──cancel──────┘   (completed からは不可)
```

## 例外モデル
- `OrderInvariantError`（domain）: 不正な数量・単価・空明細・状態違反。
- api 層で `HTTPException(400)` に変換。

## 依存方針
- domain は標準ライブラリのみ。
- 外部 SaaS 呼び出しなし（onprem-constraints）。
- 通知は将来構内メール経由。

## テスト戦略
- `tests/test_order_domain.py`: 純 pytest で AC-1〜AC-8 を網羅。
- `tests/test_orders_api.py`: SQLite in-memory で API 統合（`@pytest.mark.integration`）。
