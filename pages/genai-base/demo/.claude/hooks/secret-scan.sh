#!/usr/bin/env bash
# 秘密情報スキャン（feedback センサー）。
#   引数 prompt : UserPromptSubmit でプロンプト本文を検査
#   引数 files  : PostToolUse で作業ツリーの差分を検査
# 検出時は exit 2 でブロックし、env/.env への外出しを促す。
#
# ⚠️ 教学用：単純 regex ベースで穴がある（例：base64 化や分割文字列は検出不可）。
#   本番では gitleaks / trufflehog / GitHub Advanced Security と併用すること。
set -uo pipefail
mode="${1:-files}"
pattern='(AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|password\s*=\s*["'\''][^"'\'' ]{6,}|secret\s*=\s*["'\''][^"'\'' ]{6,}|sk-[A-Za-z0-9]{20,})'

scan() { grep -REn --include='*.py' --include='*.toml' --include='*.yml' --include='*.yaml' -- "$pattern" . 2>/dev/null; }

hits=""
if [ "$mode" = "prompt" ]; then
  body="$(cat 2>/dev/null || true)"
  hits="$(printf '%s' "$body" | grep -En -- "$pattern" || true)"
else
  hits="$(scan || true)"
fi

if [ -n "$hits" ]; then
  echo "[secret-scan] 秘密情報の疑い。env/.env へ外出ししてください（ハードコード禁止）:" >&2
  printf '%s\n' "$hits" | head -5 >&2
  exit 2
fi
echo "[secret-scan] OK"
exit 0
