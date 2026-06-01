#!/usr/bin/env bash
# Stop — 応答終了時にテストを実行（feedback センサー / 受容基準＝テスト）。
# 純ドメインテストはオフラインで高速。失敗時は exit 2 で気づける形に。
set -uo pipefail
command -v pytest >/dev/null 2>&1 || { echo "[tests] pytest 未導入のためスキップ"; exit 0; }
if pytest -q tests/test_order_domain.py >/tmp/opsm_pytest.log 2>&1; then
  echo "[tests] ドメインテスト 通過 ✓"
  exit 0
else
  echo "[tests] ドメインテスト 失敗 ✗ — 修正が必要"
  tail -20 /tmp/opsm_pytest.log
  exit 2
fi
