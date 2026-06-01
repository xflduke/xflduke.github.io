"""受注ユースケース（services 層）。トランザクション境界。"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.domain.order import Order, OrderInvariantError, OrderLine
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._repo = OrderRepository(session)

    def create_draft(
        self, order_id: str, customer_id: str, lines: list[OrderLine]
    ) -> Order:
        order = Order(id=order_id, customer_id=customer_id)
        for line in lines:
            order.add_line(line)
        self._repo.save(order)
        self._session.commit()
        return order

    def confirm(self, order_id: str, approved: bool = False) -> Order:
        order = self._repo.get(order_id)
        if order is None:
            raise OrderInvariantError(f"受注が見つかりません: {order_id}")
        order.confirm(approved=approved)
        self._repo.save(order)
        self._session.commit()
        return order
