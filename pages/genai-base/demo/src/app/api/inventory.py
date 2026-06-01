"""在庫 API — 桩（API 雛形のみ）。詳細仕様は docs/specs/inventory.md（未決）。"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/{product_id}")
def get_inventory(product_id: str) -> dict[str, str | int]:
    """桩実装。本サンプルでは未対応。"""
    return {"product_id": product_id, "stock": 0, "note": "stub"}
