"""FastAPI エントリポイント。"""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.api import inventory, orders
from app.db.models import Base
from app.db.session import SessionLocal


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """教学用：起動時にスキーマを作成（SQLite in-memory 既定値）。本番は alembic 等の migration を使用。"""
    with SessionLocal() as session:
        Base.metadata.create_all(bind=session.get_bind())
    yield


app = FastAPI(title="OPSM (On-Prem Sales Management)", version="0.1.0", lifespan=lifespan)
app.include_router(orders.router)
app.include_router(inventory.router)


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
