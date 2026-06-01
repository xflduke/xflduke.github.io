#!/usr/bin/env python3
"""
gen_images.py — 用 gpt-image-2 为本站生成主视觉/架构插画。

直接调用 OpenAI Images API（不经过 codex）。输出 PNG 到 ../assets/img/，
文件名与各 HTML 页面里引用的一致；缺失时页面会自动回退为渐变占位，
所以本脚本是「锦上添花」，可随时跑、随时重跑。

用法：
    pip install openai            # 或 pip install -r scripts/requirements.txt
    export OPENAI_API_KEY=sk-...  # Windows PowerShell: $env:OPENAI_API_KEY="sk-..."
    python scripts/gen_images.py              # 生成所有缺失的图
    python scripts/gen_images.py --force      # 覆盖已存在的图
    python scripts/gen_images.py --only hero-overview   # 只生成某一张
    python scripts/gen_images.py --model gpt-image-2 --size 1536x1024

环境变量（可选）：
    OPENAI_API_KEY   必需
    IMAGE_MODEL      默认 gpt-image-2
    IMAGE_SIZE       默认 1536x1024
"""

import argparse
import base64
import os
import sys

# 日文 Windows 控制台是 cp932，避免打印非 ASCII 时崩溃。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# 企业代理会拦截 TLS；用 Windows 系统信任库做证书校验，
# 绕开 OpenSSL 3.x 对企业根证书 Basic Constraints 的严格检查。
try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

# 统一视觉规范，拼到每个 prompt 后面，保证风格一致、图内无文字。
STYLE_DARK = (
    "Dark high-tech aesthetic, deep navy/near-black background (#0a0e1a), "
    "neon blue (#5b8cff) and purple (#b07bff) accents with subtle cyan, "
    "clean flat / isometric vector illustration, glowing circuit and neural-network "
    "motifs, soft depth and glow, generous margins for cropping, "
    "NO text, NO words, NO letters, NO numbers anywhere in the image. "
    "High quality, balanced composition, presentation-friendly."
)
STYLE_LIGHT = (
    "Clean light presentation aesthetic, soft off-white / very light gray "
    "background (#f4f6fb), deep blue (#2f63ff) and purple (#8a45f0) accents with teal, "
    "crisp flat / isometric vector illustration, subtle circuit and neural-network "
    "motifs, light soft shadows, strong contrast for a projector, generous margins, "
    "NO text, NO words, NO letters, NO numbers anywhere in the image. "
    "High quality, balanced composition, professional."
)
STYLES = {"dark": ("", STYLE_DARK), "light": ("-light", STYLE_LIGHT)}

# 文件名 → 画面描述（与 HTML 中 <img src> 一一对应）
IMAGES = {
    "hero-overview": (
        "A panoramic hero scene of humans collaborating with AI agents to build "
        "software: developers at laptops connected by flowing streams of data to "
        "abstract glowing AI agents, gears and code blocks forming a cohesive system."
    ),
    "part1-modes": (
        "A conceptual collage of six distinct ways to use a large language model: "
        "a chat bubble, an API plug/socket, an autonomous agent robot with a tool, "
        "a terminal/command-line window, a code editor with an inline suggestion, "
        "and a persistent always-on assistant orb — arranged as six glowing tiles."
    ),
    "part2-harness": (
        "A central glowing AI model core wrapped and supported by a surrounding "
        "scaffold/harness made of modular blocks labeled only by distinct icons: "
        "rules, skills, tools, hooks, sub-agents — like a race-car chassis around an engine."
    ),
    "part2-protocols": (
        "A layered network diagram metaphor showing four stacked connection layers "
        "between a user, multiple AI agents from different vendors, and tools/data "
        "systems — glowing nodes connected by luminous links, isometric perspective."
    ),
    "part3-shift": (
        "An evolution/progression metaphor: on the left a single developer hand-typing "
        "code bricks, transforming toward the right into an architect orchestrating many "
        "autonomous agents from a control desk — a blueprint-to-factory transition."
    ),
}

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "assets", "img"))


def main():
    ap = argparse.ArgumentParser(description="Generate site visuals with gpt-image-2.")
    ap.add_argument("--model", default=os.environ.get("IMAGE_MODEL", "gpt-image-2"))
    ap.add_argument("--size", default=os.environ.get("IMAGE_SIZE", "1536x1024"))
    ap.add_argument("--only", help="only generate this filename stem (e.g. hero-overview)")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--variant", choices=["dark", "light", "both"], default="dark",
                    help="which theme variant to generate (light writes <name>-light.png)")
    ap.add_argument("--insecure", action="store_true",
                    help="disable TLS verification (last resort behind a broken corporate proxy)")
    args = ap.parse_args()

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("ERROR: set OPENAI_API_KEY first (PowerShell: $env:OPENAI_API_KEY=\"sk-...\").")

    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("ERROR: pip install openai")

    if args.insecure:
        import httpx
        client = OpenAI(http_client=httpx.Client(verify=False))
    else:
        client = OpenAI()
    os.makedirs(OUT_DIR, exist_ok=True)

    targets = {args.only: IMAGES[args.only]} if args.only else IMAGES
    if args.only and args.only not in IMAGES:
        sys.exit(f"ERROR: unknown image '{args.only}'. Choose from: {', '.join(IMAGES)}")

    variants = ["dark", "light"] if args.variant == "both" else [args.variant]
    ok, skipped, failed = 0, 0, 0
    for stem, desc in targets.items():
        for v in variants:
            suffix, style = STYLES[v]
            name = stem + suffix + ".png"
            path = os.path.join(OUT_DIR, name)
            if os.path.exists(path) and not args.force:
                print(f"skip   {name} (exists; use --force to overwrite)")
                skipped += 1
                continue

            prompt = f"{desc} {style}"
            print(f"gen    {name}  ...", flush=True)
            try:
                resp = client.images.generate(
                    model=args.model, prompt=prompt, size=args.size, n=1
                )
                data = resp.data[0]
                if getattr(data, "b64_json", None):
                    raw = base64.b64decode(data.b64_json)
                elif getattr(data, "url", None):
                    import urllib.request
                    with urllib.request.urlopen(data.url) as r:
                        raw = r.read()
                else:
                    raise RuntimeError("response had neither b64_json nor url")
                with open(path, "wb") as f:
                    f.write(raw)
                print(f"  [ok] wrote {path} ({len(raw)//1024} KB)")
                ok += 1
            except Exception as e:  # noqa: BLE001 — keep going on per-image failure
                print(f"  [FAIL] {name}: {e}")
                failed += 1

    print(f"\nDone. generated={ok} skipped={skipped} failed={failed} -> {OUT_DIR}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
