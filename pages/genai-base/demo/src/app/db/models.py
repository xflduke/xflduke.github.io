"""SQLAlchemy ORM モデル（受注のみ実装、他は将来課題）。"""

from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class OrderRow(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    customer_id: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="draft")
    lines: Mapped[list[OrderLineRow]] = relationship(
        "OrderLineRow", back_populates="order", cascade="all, delete-orphan"
    )


class OrderLineRow(Base):
    __tablename__ = "order_lines"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[int] = mapped_column(Integer, nullable=False)
    order: Mapped[OrderRow] = relationship("OrderRow", back_populates="lines")
