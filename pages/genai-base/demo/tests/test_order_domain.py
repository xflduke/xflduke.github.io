"""受注ドメインの単体テスト — 純 pytest（FastAPI/DB 不要）。

仕様: docs/specs/order.md の AC-1〜AC-8 を 1:1 で検証する。
"""

from __future__ import annotations

import pytest

from app.domain.order import Order, OrderInvariantError, OrderLine, OrderStatus


def _line(product_id: str = "P-1", quantity: int = 1, unit_price: int = 100) -> OrderLine:
    return OrderLine(product_id=product_id, quantity=quantity, unit_price=unit_price)


# AC-2 数量
def test_ac2_quantity_must_be_positive() -> None:
    with pytest.raises(OrderInvariantError):
        OrderLine(product_id="P-1", quantity=0, unit_price=100)
    with pytest.raises(OrderInvariantError):
        OrderLine(product_id="P-1", quantity=-1, unit_price=100)


# AC-3 単価
def test_ac3_unit_price_non_negative() -> None:
    OrderLine(product_id="P-1", quantity=1, unit_price=0)  # 0 は許可
    with pytest.raises(OrderInvariantError):
        OrderLine(product_id="P-1", quantity=1, unit_price=-1)


# AC-4 合計
def test_ac4_total_is_sum_of_lines() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line(quantity=2, unit_price=300))
    order.add_line(_line(product_id="P-2", quantity=3, unit_price=100))
    assert order.total() == 2 * 300 + 3 * 100


# AC-1 空明細では確定不可
def test_ac1_cannot_confirm_empty() -> None:
    order = Order(id="O-1", customer_id="C-1")
    with pytest.raises(OrderInvariantError):
        order.confirm()


# AC-5 状態遷移：許可ルート
def test_ac5_happy_path_state_transitions() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line())
    order.confirm()
    assert order.status is OrderStatus.CONFIRMED
    order.advance_to_shipping()
    assert order.status is OrderStatus.SHIPPING
    order.complete()
    assert order.status is OrderStatus.COMPLETED


# AC-5 不正遷移
def test_ac5_invalid_transitions() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line())
    with pytest.raises(OrderInvariantError):
        order.advance_to_shipping()  # draft からは不可
    order.confirm()
    with pytest.raises(OrderInvariantError):
        order.complete()  # confirmed → completed は不可（shipping を経由）


# AC-5 completed からのキャンセル不可
def test_ac5_cannot_cancel_completed() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line())
    order.confirm()
    order.advance_to_shipping()
    order.complete()
    with pytest.raises(OrderInvariantError):
        order.cancel()


# AC-5 各状態からのキャンセル可
@pytest.mark.parametrize("advance_to", ["draft", "confirmed", "shipping"])
def test_ac5_cancel_allowed_states(advance_to: str) -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line())
    if advance_to in ("confirmed", "shipping"):
        order.confirm()
    if advance_to == "shipping":
        order.advance_to_shipping()
    order.cancel()
    assert order.status is OrderStatus.CANCELLED


# AC-6 高額受注は承認必須
def test_ac6_high_value_requires_approval() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line(quantity=1, unit_price=1_000_000))
    assert order.requires_approval() is True
    with pytest.raises(OrderInvariantError):
        order.confirm()  # 未承認は不可
    order.confirm(approved=True)
    assert order.status is OrderStatus.CONFIRMED


def test_ac6_low_value_does_not_require_approval() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line(quantity=1, unit_price=999_999))
    assert order.requires_approval() is False
    order.confirm()  # 承認不要
    assert order.status is OrderStatus.CONFIRMED


# AC-7 確定済み受注の明細は変更不可
def test_ac7_lines_immutable_after_confirm() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line())
    order.confirm()
    with pytest.raises(OrderInvariantError):
        order.add_line(_line(product_id="P-2"))


# AC-8 確定操作は冪等
def test_ac8_confirm_is_idempotent() -> None:
    order = Order(id="O-1", customer_id="C-1")
    order.add_line(_line())
    order.confirm()
    order.confirm()  # 再度呼んでも例外にならず状態維持
    assert order.status is OrderStatus.CONFIRMED


# 不変条件（id / customer_id 必須）
def test_invariants_required_fields() -> None:
    with pytest.raises(OrderInvariantError):
        Order(id="", customer_id="C-1")
    with pytest.raises(OrderInvariantError):
        Order(id="O-1", customer_id="")
    with pytest.raises(OrderInvariantError):
        OrderLine(product_id="", quantity=1, unit_price=100)
