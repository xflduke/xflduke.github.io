# ADR-0001: オンプレミス・アーキテクチャの選定

- ステータス: Accepted（教学用サンプル前提）
- 日付: -

## コンテキスト
顧客環境内（構内）での販売管理システム運用を前提とする。クラウド SaaS / 外部 API 連携は禁止。

## 決定
- ランタイム: Python 3.12 + FastAPI（同期/非同期両対応、教学に十分なシンプルさ）。
- 永続化: PostgreSQL + SQLAlchemy 2.0。
- 配布: Docker Compose（app / postgres / nginx）。すべて構内ホスト上で完結。
- 秘密管理: `.env` + `pydantic-settings`。コードへのハードコード禁止。
- CI: GitHub Actions（Self-hosted runner 推奨。本サンプルでは公開 runner で代替）。
- 依存追加は許可リスト方式。新規追加は ADR + レビュー必須。

## 代替案
- Java/Spring Boot, .NET 8: 既存資産があれば有力。本サンプルは教学のため Python を採用。
- Kubernetes: 構内運用で過剰。Compose で十分。

## 影響
- すべての外部接続呼び出しが hook `no-external-net` でブロックされる。
- 依存追加は CI / レビューで二重確認。
- データは構内 PostgreSQL に駐留。

## 備考
**栈/言語は仮置き**。実プロジェクトでは事前に AI と相談し、現場環境に合わせて選定する（選定自体が harness の一部）。
