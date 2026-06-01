"""受注 API の統合テスト（SQLite in-memory）。

`@pytest.mark.integration` を付与。`pytest -m integration` で実行可能。
教学用のため、設定の差し替えは最小限。
"""

from __future__ import annotations

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("sqlalchemy")

from fastapi.testclient import TestClient  # noqa: E402

pytestmark = pytest.mark.integration


@pytest.fixture()
def client() -> TestClient:
    from app.db.models import Base
    from app.db.session import SessionLocal
    from app.main import app

    # 起動時の create_all を明示実行（TestClient の lifespan は環境差があるため）
    with SessionLocal() as s:
        Base.metadata.create_all(bind=s.get_bind())
    return TestClient(app)


def test_create_and_confirm_order(client: TestClient) -> None:
    payload = {
        "id": "O-1",
        "customer_id": "C-1",
        "lines": [{"product_id": "P-1", "quantity": 2, "unit_price": 300}],
    }
    r = client.post("/orders", json=payload)
    assert r.status_code == 200
    assert r.json()["total"] == 600
    assert r.json()["requires_approval"] is False

    r = client.post("/orders/O-1/confirm")
    assert r.status_code == 200
    assert r.json()["status"] == "confirmed"


def test_high_value_requires_approval(client: TestClient) -> None:
    payload = {
        "id": "O-2",
        "customer_id": "C-1",
        "lines": [{"product_id": "P-1", "quantity": 1, "unit_price": 1_000_000}],
    }
    r = client.post("/orders", json=payload)
    assert r.status_code == 200

    r = client.post("/orders/O-2/confirm")
    assert r.status_code == 400  # 未承認は不可

    r = client.post("/orders/O-2/confirm?approved=true")
    assert r.status_code == 200
