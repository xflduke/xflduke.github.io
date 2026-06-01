---
name: code-standards
description: 編码規約（命名・レイヤ・型注釈・例外・テスト・依存）。詳細は references/coding-conventions.md を参照。
---
# code-standards

精錬原則のみ。詳細は `references/coding-conventions.md`（必要時のみ読み込み）。

- レイヤ：api → services → repositories → domain（依存は内向き）。
- 型注釈：すべての public 関数に注釈。`mypy --strict` を通す。
- 例外：domain 層で固有例外を定義し、api 層で HTTP に変換。
- 命名：snake_case（関数・変数）、PascalCase（クラス）、UPPER_SNAKE（定数）。
- 依存：外部 SaaS/クラウド禁止、秘密は env。
