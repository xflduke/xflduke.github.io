# 生成 AI × 开发 · 全体像 — 教学演讲静态站

面向 IT 从业人员的教学/演讲用静态站点：用一条主线讲清**生成 AI 应用于开发与生产**的全体像——应用方式、工具定制与标准、开发模式的变迁与展望。

- **形态**：滚动式多页站点 + 左侧导航 + 滚动高亮。
- **演讲模式**：右上角开关，开启后逐屏 `scroll-snap`，方向键 / 空格 / PageDown 翻屏，Esc 退出 —— 同一份内容既能自学又能直接上台讲。
- **三语**：中 / 日 / 英 切换（右上角，`localStorage` 记忆）。默认英文。
- **主题**：浅色 / 深色 一键切换（☀/🌙）。深色默认；**投影仪建议用浅色**，对比更清晰。
- **字号**：S / M / L 三段调整（`A` 大小按钮），正文/标题/代码随之缩放，便于投屏。
- 主题 / 字号 / 语言均存 `localStorage`，并在页面渲染前注入（无闪烁）。
- **Demo**：纯前端**模拟/预置**，**无需任何 API Key**，离线可跑。
- **风格**：深色科技主题；纯 HTML/CSS/vanilla JS + CDN（Mermaid / highlight 可选）；**无构建步骤**。

## 页面结构

| 文件 | 内容 |
|---|---|
| `index.html` | 全体像 · 整体地图 · 三部分入口 · 观众路径 |
| `part1.html` | LLM 六种应用形态（Chat / API+内置功能 / Agent / CLI / IDE / 持久化助手）+ 模拟 demo + 前沿最佳实践 |
| `part2.html` | 通用定制构件（rule/skill/command/hook/agent/MCP…）+ MCP/A2A/ACP/AG-UI 协议 + Harness |
| `part3.html` | 变迁时间线 · vibe→规格驱动 · AgentOps · Harness 工程 · 挑战与机遇 |
| `references.html` | 面向观众的精简参照链接 |
| `REFERENCES.md` | **维护者用**的全量参考摘要（事实 + URL + 核实日期 + 易变性） |
| `assets/css/style.css` | 主题、布局、演讲模式、组件、动画 |
| `assets/js/i18n.js` | 三语切换 |
| `assets/js/nav.js` | scroll-spy · 进度条 · 演讲模式键盘 · 代码复制 · Tabs · 图片回退 |
| `assets/js/demos.js` | Part 1 各模拟 demo |
| `assets/img/` | 主视觉/架构插画（见下） |

## 本地预览

纯静态，直接用浏览器打开 `index.html` 即可。若要模拟 GitHub Pages 子路径：

```bash
python -m http.server 8000
# 访问 http://localhost:8000/
```

## 发布到 GitHub Pages

1. 把本目录推到 GitHub 仓库。
2. 仓库 **Settings → Pages**，Source 选择对应分支的根目录（`/`）。
3. `.nojekyll` 已包含，确保 `assets/` 正常加载。
4. 所有资源使用相对路径，兼容 `https://<user>.github.io/<repo>/` 子路径。

## 配图（gpt-image-2，可选）

页面已引用 5 张图片；**缺失时会自动回退为渐变占位**（不影响发布）。生成脚本见 `scripts/gen_images.py`，直接调 OpenAI Images API（gpt-image-2），统一深色科技风、图内无文字、留边便于裁切：

```bash
pip install -r scripts/requirements.txt
# PowerShell: $env:OPENAI_API_KEY="sk-..."   |   bash: export OPENAI_API_KEY=sk-...
python scripts/gen_images.py            # 生成所有缺失的图
python scripts/gen_images.py --force    # 覆盖重生
python scripts/gen_images.py --only hero-overview   # 只生成一张
python scripts/gen_images.py --variant light        # 浅色主题用的一套（输出 <name>-light.png）
python scripts/gen_images.py --variant both --force # 深+浅两套
```

> 站点会按当前主题自动切换图片：深色用 `<name>.png`，浅色用 `<name>-light.png`（两张 `<img>` 由 CSS 显隐）。当前已为首页/Part1/Part3 三张主视觉各生成深浅两版。

> 企业代理（TLS 拦截）环境下：`requirements.txt` 已含 `truststore`，脚本会自动用系统信任库校验证书；若仍失败可加 `--insecure` 兜底（关闭校验，最后手段）。

生成的文件名与页面引用一一对应：`hero-overview.png`（首页全景）、`part1-modes.png`（六形态拼贴）、`part2-harness.png`（模型被 harness 包裹）、`part2-protocols.png`（MCP/A2A/ACP 分层网络）、`part3-shift.png`（写代码→设计 agent 系统）。提示词与画面描述写在脚本顶部，可按需微调。

## 内容时效

内容核实于 **2026-05**。带版本号/数字（协议版本、star 数、百分比等）的条目随时间变化快，引用前请对照 `REFERENCES.md` 的复查清单核对最新官方信息。
