"""受注リポジトリ（永続化のみ）。"""

from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import OrderLineRow, OrderRow
from app.domain.order import Order, OrderLine, OrderStatus


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, order: Order) -> None:
        row = self._session.get(OrderRow, order.id)
        if row is None:
            row = OrderRow(id=order.id, customer_id=order.customer_id, status=order.status.value)
            self._session.add(row)
        else:
            row.customer_id = order.customer_id
            row.status = order.status.value
            row.lines.clear()
        for line in order.lines:
            row.lines.append(
                OrderLineRow(
                    product_id=line.product_id,
                    quantity=line.quantity,
                    unit_price=line.unit_price,
                )
            )
        self._session.flush()

    def get(self, order_id: str) -> Order | None:
        row = self._session.get(OrderRow, order_id)
        if row is None:
            return None
        return Order(
            id=row.id,
            customer_id=row.customer_id,
            lines=[
                OrderLine(product_id=ln.product_id, quantity=ln.quantity, unit_price=ln.unit_price)
                for ln in row.lines
            ],
            status=OrderStatus(row.status),
        )
