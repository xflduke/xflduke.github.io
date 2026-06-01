#!/usr/bin/env bash
# statusLine 例：ブランチ / モデル / オンプレモードを 1 行で表示。
# 標準入力に Claude Code から JSON が渡る（model.display_name など）。教育用に簡略実装。
#
# ⚠️ 教学用：grep + sed で雑に JSON をパース。本番は jq を使うこと（例：`jq -r .model.display_name`）。
set -euo pipefail

input="$(cat 2>/dev/null || true)"
model="$(printf '%s' "$input" | grep -o '"display_name"[^,]*' | head -1 | sed 's/.*: *"//;s/"//g')"
[ -z "${model:-}" ] && model="claude"

branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo no-git)"
env_mode="${OPSM_ENV:-onprem}"

printf 'OPSM | %s | ⎇ %s | 🔒 %s' "$model" "$branch" "$env_mode"
