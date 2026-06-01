#!/usr/bin/env bash
# 各種ライフサイクル通知（SessionStart / SubagentStop / Notification / PreCompact）。
# 教育用に観測ログへ 1 行追記するだけ（AgentOps の最小版）。
set -uo pipefail
event="${1:-event}"
ts="$(date '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo now)"
mkdir -p .claude/.logs 2>/dev/null || true
echo "[$ts] $event" >> .claude/.logs/agent-events.log 2>/dev/null || true
exit 0
