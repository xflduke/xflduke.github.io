"""受注 API ルータ（入出力検証と変換のみ。ビジネスロジックは services 以降）。"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.domain.order import OrderInvariantError, OrderLine
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


class OrderLineIn(BaseModel):
    product_id: str = Field(min_length=1)
    quantity: int = Field(ge=1)
    unit_price: int = Field(ge=0)


class OrderCreateIn(BaseModel):
    id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    lines: list[OrderLineIn] = Field(min_length=1)


class OrderOut(BaseModel):
    id: str
    customer_id: str
    status: str
    total: int
    requires_approval: bool


@router.post("", response_model=OrderOut)
def create_order(payload: OrderCreateIn, db: Session = Depends(get_db)) -> OrderOut:
    try:
        order = OrderService(db).create_draft(
            order_id=payload.id,
            customer_id=payload.customer_id,
            lines=[
                OrderLine(product_id=ln.product_id, quantity=ln.quantity, unit_price=ln.unit_price)
                for ln in payload.lines
            ],
        )
    except OrderInvariantError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return OrderOut(
        id=order.id,
        customer_id=order.customer_id,
        status=order.status.value,
        total=order.total(),
        requires_approval=order.requires_approval(),
    )


@router.post("/{order_id}/confirm", response_model=OrderOut)
def confirm_order(
    order_id: str, approved: bool = False, db: Session = Depends(get_db)
) -> OrderOut:
    try:
        order = OrderService(db).confirm(order_id=order_id, approved=approved)
    except OrderInvariantError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return OrderOut(
        id=order.id,
        customer_id=order.customer_id,
        status=order.status.value,
        total=order.total(),
        requires_approval=order.requires_approval(),
    )
