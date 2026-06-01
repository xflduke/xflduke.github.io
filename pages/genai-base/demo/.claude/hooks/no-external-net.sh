#!/usr/bin/env bash
# PreToolUse(Bash) — オンプレ制約の強制（feedback センサー / 迂回不可）。
# 外部ネットワークへ出る恐れのあるコマンドをブロック（exit 2）。
# Claude Code から stdin に JSON（tool_input.command）が渡る。
#
# ⚠️ 教学用：プロセスレベルの文字列マッチのみ。`bash -c "$(echo curl ...)"` 等で容易に回避可能。
#   本番は OS レベルで遮断（Linux network namespace / iptables / nftables / Docker network 隔離 /
#   コンテナを `--network none` で起動して必要なものだけプロキシ経由 等）すること。
set -uo pipefail
input="$(cat 2>/dev/null || true)"
cmd="$(printf '%s' "$input" | grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed 's/.*: *"//;s/"$//')"
[ -z "${cmd:-}" ] && exit 0

# 構内ホスト（localhost / プライベートIP）は許可、それ以外の外向きは拒否
if printf '%s' "$cmd" | grep -Eq '(curl|wget|nc|ssh|scp|pip[0-9]* +install|npm +install|pip install)'; then
  if printf '%s' "$cmd" | grep -Eqv '(localhost|127\.0\.0\.1|::1|10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)'; then
    echo "[no-external-net] オンプレ制約：外部ネットワークへの接続は禁止です → $cmd" >&2
    exit 2
  fi
fi
exit 0
