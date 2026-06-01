#!/usr/bin/env bash
# PostToolUse(Edit|Write) — 編集後に自動整形 + 静的検査（feedback センサー）。
# 失敗してもブロックはしない（情報提供）。CI が最終ゲート。
set -uo pipefail
command -v ruff >/dev/null 2>&1 || { echo "[format] ruff 未導入のためスキップ"; exit 0; }
ruff format . >/dev/null 2>&1 || true
ruff check --fix . >/dev/null 2>&1 || true
echo "[format] ruff format + check 実行済み"
exit 0
