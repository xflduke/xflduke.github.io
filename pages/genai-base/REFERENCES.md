# 参考摘要 / Reference Summary

> **最后核实：2026-05。** 这是**维护者用**的全量证据档（事实摘要 + URL + 易变性），与面向观众的 `references.html` 分工。
> ⚠️ 带**版本号 / 数字 / "原生支持列表"**的条目易变 —— 引用前请先复查官方最新信息。
>
> 记录格式：`话题 — 关键事实 — URL — 易变性(高/中/低)`

---

## 1 · Agent 互操作协议（标准化层）

- **MCP（Model Context Protocol，Anthropic）** — agent ↔ 工具/数据（纵向）。约 97M/月 SDK 下载、10000+ server、各大厂内置；事实标准。 — https://modelcontextprotocol.io/ — 易变性：中（数字会涨）。
- **A2A（Agent2Agent，Google → Linux Foundation）** — agent ↔ agent（横向，跨厂商）。三核心：Agent Card（`/.well-known/agent.json`）、Task、传输 HTTP/SSE/JSON-RPC 2.0。**v1.2**（签名 Agent Card）；**150+ 组织**生产环境。原生支持：Google ADK、LangGraph、CrewAI、LlamaIndex、Semantic Kernel、AutoGen。 — https://a2a-protocol.org/ · codelab https://codelabs.developers.google.com/intro-a2a-purchasing-concierge — 易变性：**高**（版本/支持列表）。
  - 真实编排例：ADK 控制台 → LangGraph 规划器 → CrewAI 执行小组（零售补货）；采购 concierge(ADK client) 调用 Burger(CrewAI)+Pizza(LangGraph)。 — https://codelabs.developers.google.com/next26/scale-agents
- **ACP（Agent Communication Protocol，IBM / BeeAI → Linux Foundation）** — 跨框架 inter-agent，纯 HTTP、可 curl/浏览器直连；与 A2A 同层并走向融合。搭建：`brew install i-am-bee/beeai/beeai` → `beeai env setup` → `from acp_sdk.server import Server` + `@server.agent()` → `uv run server` → `beeai run` 在 `localhost:8333`。OTLP → Arize Phoenix。 — https://github.com/i-am-bee/acp · https://framework.beeai.dev/integrations/acp — 易变性：中。
- **AG-UI（Agent-User Interaction，CopilotKit 等）** — agent ↔ 前端 UI。事件流（消息/工具活动/UI 状态），每数百 ms 推送，实时显示 agent thinking/工具调用；对接 Langfuse/Arize。 — https://docs.ag-ui.com/ · https://github.com/ag-ui-protocol/ag-ui — 易变性：中。
- **综述论文** — MCP / ACP / A2A / ANP 互操作协议 survey。 — https://arxiv.org/abs/2505.02279 — 易变性：低。
- **分层结论**：四层互补非竞争 —— `AG-UI(用户↔agent) → A2A/ACP(agent↔agent) → MCP(agent↔工具) → 数据/系统`；多归 Linux Foundation。 — 易变性：低（趋势）。

## 2 · Harness 工程

- **精确定义（已复核，2026-05）** — `Agent = Model + Harness`。harness = 包裹模型的**运行时机制**：调用模型、分发工具调用、管理上下文、执行安全、失败恢复的那个**循环**，外加它驱动的 prompt/工具/钩子/沙箱/子代理/反馈与恢复路径。 — Hugging Face agent glossary https://huggingface.co/blog/agent-glossary · DataCamp https://www.datacamp.com/blog/agent-harness · Salesforce https://www.salesforce.com/agentforce/ai-agents/agent-harness/ · Addy Osmani https://addyosmani.com/blog/agent-harness-engineering/ · arXiv:2603.05344 — 易变性：中（术语仍在收敛）。
- **三层别混淆（回答"违和感"）** — **Scaffolding**＝首个 prompt 前组装的静态部分（系统提示/工具 schema/子代理注册）；**Harness**＝运行时循环，驱动**单个** agent；**Orchestration**＝把**多个** agent 当单元管理，各自跑自己的 harness（多 agent 系统）。「agent 管理」属于 orchestration（在 harness 之上）；单 agent 内的子代理调度属于 harness。 — 同上 — 易变性：中。
- **前馈/反馈结构** — harness 内部：① 前馈 Feed-forward（skills/guardrails/rules/reference）+ ② 反馈 Feedback/Sensors（tests/lint/type-check/review/evals）。 — https://martinfowler.com/articles/harness-engineering.html — 易变性：低。
- **作用与学科** — 让 agent 在规模下可靠；工程师从「写代码」转向「设计治理 agent 如何写代码的系统」；抑制架构漂移、统一安全/合规、确定性约束替代概率性合规。 — Thoughtworks https://www.thoughtworks.com/en-us/insights/blog/generative-ai/harness-engineering-agent-feedback-exploring-ai-coding-sensors · Augment Code https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents · https://github.com/ai-boost/awesome-harness-engineering — 易变性：低。

## 3 · Spec-Driven Development（SDD）与生态

- **主线论点** — Karpathy 2025 提「vibe coding」，一年后自述其落幕，进入「agentic engineering」（按详细规格编排 agent + 人监督）。 — https://towardsdatascience.com/from-vibe-coding-to-spec-driven-development/ — 易变性：低。
- **SDD 定义** — 规格＝主权文档；循环 `Spec → Plan → Tasks → Implement`；解决 intent drift 与 context decay。 — https://sddbook.com/ · https://www.augmentcode.com/guides/what-is-spec-driven-development — 易变性：低。
- **生态（仅类别列举）** — GitHub Spec Kit、AWS Kiro、Cursor、OpenSpec、BMAD、Tessl、Google Antigravity… **30+ 框架**。 — https://github.com/github/spec-kit · https://www.deeplearning.ai/courses/spec-driven-development-with-coding-agents/ — 易变性：**高**（项目数/名单）。
- **角色转变** — 开发者转向 steering / review / 架构决策。 — 易变性：低。

## 4 · Context Engineering / Evals / 安全护栏（带数字）

- **上下文文件写法** — bullet 规则 + Preferred/Avoid 代码对照 + metadata(last_updated/owner/scope)；排查 context gap。 — https://packmind.com/context-engineering-ai-coding/context-engineering-best-practices/ — 易变性：低。
- **Evals** — 测全轨迹（工具选择+结果），非仅最终答案。 — https://andriifurmanets.com/blogs/ai-agents-2026-practical-architecture-tools-memory-evals-guardrails — 易变性：低。
- **五层安全护栏** — prompt 级 → schema 工具门控（双 agent 隔离）→ 运行时审批 → 工具级校验 → 生命周期 hook；policy-as-code + 防注入。 — 同上 — 易变性：低。
- **上下文管理收益（数字，需复查出处）** — context editing **+29%**；叠加 memory tool **+39%**；100 轮检索 token **省 84%**。 — 同上（源引 Anthropic 数据） — 易变性：**高**（具体数字）。
- **Subagent 模式** — 隔离上下文、各返回 1–2k token 摘要；Anthropic 研究系统较单 agent **+90.2%**。 — Anthropic multi-agent research system — 易变性：**高**（数字）。

## 5 · 新型 AI 助手

- **OpenClaw**（Peter Steinberger） — 自托管个人 AI agent，多通道，自写技能/自改进，bring-your-own-key；约 **68k+ GitHub stars**。 — https://github.com/openclaw/openclaw · https://openclaw.ai/ — 易变性：**高**（star 数）。
- **Hermes Agent**（Nous Research，**2026-02**） — 自托管持久 agent，闭环学习（写可复用技能），**200+ 模型**；约 **110k stars/10 周**；偏会话非编码优先。 — https://hermes-agent.nousresearch.com/ · https://github.com/nousresearch/hermes-agent — 易变性：**高**（star 数/时间）。

## 6 · LLM 应用模式 / RAG / 记忆 / 多模态

- **2026 模式** — RAG-first、可用长上下文、多模态、agent 工作流、混合部署；模型路由成战略（别让一个模型干所有）。 — https://nat.io/blog/llms-in-2026-from-bigger-to-better — 易变性：中。
- **检索 / Agentic Search（已扩充，2026-05）** — 标准 RAG → 模块化 RAG（查询改写 + 混合检索 keyword+vector + 重排 reranking）→ **Agentic Search / Agentic Retrieval**（agent 做查询规划、拆解子查询、并行 keyword/vector/hybrid、语义重排、按需迭代）→ GraphRAG → Contextual Retrieval。 — Azure AI Search agentic retrieval https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-overview · Redis https://redis.io/blog/agentic-retrieval-techniques/ · Elasticsearch agentic hybrid search（Medium） — 易变性：中。
- **记忆与召回（已扩充）** — 三层：episodic（对话/会话，向量库）/ semantic（实体/事实/关系，知识图谱多跳）/ state（工作状态，事务 RDB）。**召回不止向量库**：向量(ANN) + 全文检索(FTS5/BM25) + 倒排索引 + 知识图谱/GraphDB + LLM 生成 wiki/摘要。2026 共识＝**混合架构**（向量广度 + 图深度）。 — atlan https://atlan.com/know/agent-memory-architectures/ · mem0 https://mem0.ai/blog/state-of-ai-agent-memory-2026 — 易变性：中。
- **端侧** — sub-1B~4B 小模型处理有界任务。 — 同上 — 易变性：中。
- **治理提醒** — Gartner：别把改名的 chatbot 当 agentic AI；治理/可审计/透明是底线。 — https://www.clarifai.com/blog/llms-and-ai-trends — 易变性：低。
- **Provider 内置功能** — web search、code execution / code interpreter、computer use、file search/retrieval、结构化输出/JSON mode、视觉多模态。 — 各厂商 API 文档 — 易变性：中。

## 7 · AgentOps / 可观测

- **AgentOps** — 可观测/评估/治理/反馈/安全/弹性/版本化贯穿 agent 全生命周期；多用 OpenTelemetry 暴露元数据。 — https://opentelemetry.io/ · https://langfuse.com/ · https://arize.com/ — 易变性：低。

---

### 复查清单（下次更新时优先核对）
- [ ] A2A 版本号与原生支持框架列表（高）
- [ ] SDD 框架数量与名单（高）
- [ ] context editing/memory/subagent 的百分比数字与一手出处（高）
- [ ] OpenClaw / Hermes 的 star 数与发布时间（高）
- [ ] MCP server 数量、SDK 下载量（中）

## 7 · Claude Code 官方文档（demo 工程引用）

- **Hooks** — PreToolUse / PostToolUse / UserPromptSubmit 等。`exit 2` でブロック、迂回不可。 — https://docs.claude.com/en/docs/claude-code/hooks — 易变性：低。
- **Subagents** — 役割別 agent、モデル個別指定、自動委譲。 — https://docs.claude.com/en/docs/claude-code/sub-agents — 易变性：低。
- **Skills** — `SKILL.md` + references 形式の再利用可能手順。 — https://docs.claude.com/en/docs/claude-code/skills — 易变性：低。
- **Slash commands** — `/spec` `/design` `/implement` 等のフェーズコマンド。 — https://docs.claude.com/en/docs/claude-code/slash-commands — 易变性：低。
- **Output styles** — `outputStyle` で出力テンプレを切替（オンプレレビュー観点等）。 — https://docs.claude.com/en/docs/claude-code/output-styles — 易变性：低。
- **Status line** — モデル / ブランチ / モードを 1 行で可視化。 — https://docs.claude.com/en/docs/claude-code/statusline — 易变性：低。
- **MCP** — オンプレ DB / 社内 doc を agent に接続（read-only DSN 等）。 — https://docs.claude.com/en/docs/claude-code/mcp · https://modelcontextprotocol.io/ — 易变性：中。
- **Plugins** — 上記をバンドル配布。 — https://docs.claude.com/en/docs/claude-code/plugins — 易变性：低。
- **AGENTS.md** — agent 共通の権威メモリ規約（Claude Code / Codex / Copilot CLI 等が読む）。 — https://agents.md/ — 易变性：中。
