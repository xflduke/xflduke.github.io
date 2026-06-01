"""受注（Order）ドメイン — 純 Python（FastAPI / DB 非依存）。

仕様: docs/specs/order.md（AC-1〜AC-8）
設計: docs/design/order-design.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar


class OrderInvariantError(ValueError):
    """ドメイン不変条件違反。api 層で HTTP 400 に変換する。"""


class OrderStatus(str, Enum):
    DRAFT = "draft"
    CONFIRMED = "confirmed"
    SHIPPING = "shipping"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price: int

    def __post_init__(self) -> None:
        if not self.product_id:
            raise OrderInvariantError("product_id は必須です")
        if self.quantity < 1:
            raise OrderInvariantError("数量は 1 以上の整数（AC-2）")
        if self.unit_price < 0:
            raise OrderInvariantError("単価は 0 以上の整数（AC-3）")

    def subtotal(self) -> int:
        return self.quantity * self.unit_price


@dataclass
class Order:
    id: str
    customer_id: str
    lines: list[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.DRAFT

    APPROVAL_THRESHOLD: ClassVar[int] = 1_000_000

    def __post_init__(self) -> None:
        if not self.id:
            raise OrderInvariantError("id は必須です")
        if not self.customer_id:
            raise OrderInvariantError("customer_id は必須です")

    def total(self) -> int:
        """受注合計（AC-4）。派生属性。"""
        return sum(line.subtotal() for line in self.lines)

    def requires_approval(self) -> bool:
        """高額受注は承認必須（AC-6）。"""
        return self.total() >= self.APPROVAL_THRESHOLD

    def add_line(self, line: OrderLine) -> None:
        """明細追加は DRAFT のみ（AC-7 不変条件）。"""
        if self.status is not OrderStatus.DRAFT:
            raise OrderInvariantError("確定済み受注の明細は変更できません（AC-7）")
        self.lines.append(line)

    def confirm(self, approved: bool = False) -> None:
        """draft → confirmed（AC-1, AC-5, AC-6, AC-8 冪等）。"""
        if self.status is OrderStatus.CONFIRMED:
            return  # AC-8: 冪等
        if self.status is not OrderStatus.DRAFT:
            raise OrderInvariantError(
                f"確定可能なのは draft のみ。現状: {self.status.value}（AC-5）"
            )
        if not self.lines:
            raise OrderInvariantError("明細が空の受注は確定できません（AC-1）")
        if self.requires_approval() and not approved:
            raise OrderInvariantError("高額受注は承認が必要です（AC-6）")
        self.status = OrderStatus.CONFIRMED

    def advance_to_shipping(self) -> None:
        if self.status is not OrderStatus.CONFIRMED:
            raise OrderInvariantError(
                f"出荷準備可能なのは confirmed のみ。現状: {self.status.value}（AC-5）"
            )
        self.status = OrderStatus.SHIPPING

    def complete(self) -> None:
        if self.status is not OrderStatus.SHIPPING:
            raise OrderInvariantError(
                f"完了可能なのは shipping のみ。現状: {self.status.value}（AC-5）"
            )
        self.status = OrderStatus.COMPLETED

    def cancel(self) -> None:
        """completed からのキャンセルは不可（AC-5）。"""
        if self.status is OrderStatus.COMPLETED:
            raise OrderInvariantError("完了済み受注はキャンセルできません（AC-5）")
        if self.status is OrderStatus.CANCELLED:
            return  # 冪等
        self.status = OrderStatus.CANCELLED
