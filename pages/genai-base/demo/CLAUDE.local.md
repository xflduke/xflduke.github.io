# CLAUDE.local.md（個人用・gitignore 対象の例）

> これは**個人の作業環境向けオーバーライド**の例です。`.gitignore` に入れ、
> リポジトリには配布しません（チーム共有は AGENTS.md / .claude/settings.json）。

- 例：ローカルの PostgreSQL 接続は `DATABASE_URL` を各自の `.env` で設定。
- 例：重い統合テストはローカルでは `pytest -m "not integration"` で除外してよい
  （CI では全実行）。
- 例：個人的に好む補足メモやショートカットはここに。チームのルールは変えない。
