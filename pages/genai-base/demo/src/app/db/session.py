"""DB セッション（SQLAlchemy 2.0 sessionmaker）。

教学用の最小実装。本番ではプール設定・トランザクション管理を見直すこと。
"""

from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings

_settings = get_settings()
_url = _settings.database_url

# SQLite in-memory はコネクション毎に別 DB になるため、StaticPool で 1 接続を共有させる。
# 本番（PostgreSQL）は通常のプールに任せる。
if _url.startswith("sqlite") and ":memory:" in _url:
    _engine = create_engine(
        _url,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    _engine = create_engine(_url, future=True)

SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Iterator[Session]:
    """FastAPI Depends 用ジェネレータ。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
