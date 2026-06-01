"""pytest 共通フィクスチャ。"""

from __future__ import annotations

import sys
from pathlib import Path

# src を import path に追加（pyproject の packages 設定なしでテストできるよう）
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
