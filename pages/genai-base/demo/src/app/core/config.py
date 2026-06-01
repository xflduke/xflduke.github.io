"""アプリケーション設定（pydantic-settings 経由で env から読み込む）。

オンプレ制約: 秘密はコードにハードコードしない。
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="OPSM_",
        extra="ignore",
    )

    env: str = Field(default="onprem", description="onprem / dev / test")
    database_url: str = Field(
        default="sqlite+pysqlite:///:memory:",
        description="教学用既定値は SQLite in-memory。本番は PostgreSQL を env で注入。",
    )
    log_level: str = Field(default="INFO")


def get_settings() -> Settings:
    """シングルトン的に Settings を返す（依存注入用）。"""
    return Settings()
