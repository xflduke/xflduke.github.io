/* demos.js — Part 1 的纯前端模拟 demo（无需任何 API Key）
   - 所有"网络"都是预置数据 + 动画，离线可跑。
   - 文案随当前语言（html[data-lang]）切换。
   - 尊重 prefers-reduced-motion：跳过逐字动画，直接呈现。 */
(function () {
  "use strict";

  function lang() { return document.documentElement.getAttribute("data-lang") || "zh"; }
  function reduced() { return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches; }
  function pick(obj) { return obj[lang()] || obj.zh; }

  // 逐字打印
  function typeInto(el, text, done, speed) {
    speed = speed || 18;
    if (reduced()) { el.textContent = text; if (done) done(); return; }
    el.textContent = "";
    el.classList.add("caret");
    var i = 0;
    (function step() {
      if (i <= text.length) {
        el.textContent = text.slice(0, i);
        i++;
        setTimeout(step, speed);
      } else {
        el.classList.remove("caret");
        if (done) done();
      }
    })();
  }

  /* ================= 1. Chat demo ================= */
  var CHAT = {
    zh: { q: "用一句话解释什么是 RAG？", a: "RAG（检索增强生成）= 先从你的知识库里检索相关资料，再把它塞进提示词让模型基于这些事实作答，从而减少幻觉、引用最新数据。" },
    ja: { q: "RAG とは何か一言で説明して。", a: "RAG（検索拡張生成）＝ まず知識ベースから関連資料を検索し、それをプロンプトに加えて事実に基づき回答させる手法。ハルシネーションを抑え、最新データを引用できます。" },
    en: { q: "Explain RAG in one sentence.", a: "RAG (Retrieval-Augmented Generation) = retrieve relevant docs from your knowledge base, inject them into the prompt, and let the model answer grounded in those facts — reducing hallucination and citing fresh data." }
  };
  document.querySelectorAll('[data-demo="chat"]').forEach(function (root) {
    var chat = root.querySelector(".chat");
    var btn = root.querySelector(".btn");
    function run() {
      chat.innerHTML = "";
      btn.disabled = true;
      var c = pick(CHAT);
      var u = document.createElement("div"); u.className = "msg user"; u.textContent = c.q; chat.appendChild(u);
      var b = document.createElement("div"); b.className = "msg bot"; chat.appendChild(b);
      setTimeout(function () { typeInto(b, c.a, function () { btn.disabled = false; }, 16); }, 380);
    }
    btn.addEventListener("click", run);
  });

  /* ================= 2. API demo（模拟流式响应） ================= */
  var APIRESP = {
    zh: "RAG 的关键是把检索到的事实作为上下文交给模型，让回答有据可依。",
    ja: "RAG の要は、検索した事実を文脈としてモデルに渡し、根拠ある回答を得ることです。",
    en: "The key to RAG is feeding retrieved facts as context so the answer stays grounded."
  };
  document.querySelectorAll('[data-demo="api"]').forEach(function (root) {
    var out = root.querySelector(".api-out");
    var btn = root.querySelector(".btn");
    function run() {
      btn.disabled = true;
      out.textContent = "";
      var head = '{\n  "id": "msg_01R4g…",\n  "model": "claude-…",\n  "content": [{ "type": "text", "text": "';
      var tail = '" }],\n  "usage": { "input_tokens": 312, "output_tokens": 28 }\n}';
      out.textContent = head;
      var body = pick(APIRESP);
      if (reduced()) { out.textContent = head + body + tail; btn.disabled = false; return; }
      var i = 0;
      (function step() {
        if (i <= body.length) { out.textContent = head + body.slice(0, i); i++; setTimeout(step, 22); }
        else { out.textContent = head + body + tail; btn.disabled = false; }
      })();
    }
    btn.addEventListener("click", run);
  });

  /* ================= 2b. 内置功能：web_search ================= */
  var WS = {
    zh: [
      { t: 'tool', x: '→ 模型决定调用内置工具 web_search("2026 最新 LLM 上下文窗口")' },
      { t: 'obs',  x: '🔎 检索中… 命中 3 条结果（带来源 URL）' },
      { t: 'answer', x: '据最新资料，主流模型上下文已达百万级 token。[1] 来源：docs.example.com/context' }
    ],
    ja: [
      { t: 'tool', x: '→ モデルが組込みツール web_search("2026 最新 LLM コンテキスト") を呼ぶと判断' },
      { t: 'obs',  x: '🔎 検索中… 3 件ヒット（出典 URL 付き）' },
      { t: 'answer', x: '最新情報では主要モデルのコンテキストは 100 万トークン級に。[1] 出典: docs.example.com/context' }
    ],
    en: [
      { t: 'tool', x: '→ Model decides to call built-in tool web_search("2026 latest LLM context window")' },
      { t: 'obs',  x: '🔎 Searching… 3 results (with source URLs)' },
      { t: 'answer', x: 'Per fresh data, leading models now reach ~1M-token context. [1] src: docs.example.com/context' }
    ]
  };
  document.querySelectorAll('[data-demo="builtin"]').forEach(function (root) {
    var steps = root.querySelector(".agent-steps");
    var btn = root.querySelector(".btn");
    function run() {
      btn.disabled = true; steps.innerHTML = "";
      var data = pick(WS);
      data.forEach(function (s, i) {
        var el = document.createElement("div");
        el.className = "agent-step";
        el.innerHTML = '<span class="tag ' + s.t + '">' + s.t + '</span><div class="txt"></div>';
        steps.appendChild(el);
        var delay = reduced() ? 0 : i * 850 + 250;
        setTimeout(function () { el.classList.add("show"); el.querySelector(".txt").textContent = s.x; if (i === data.length - 1) btn.disabled = false; }, delay);
      });
      if (reduced()) btn.disabled = false;
    }
    btn.addEventListener("click", run);
  });

  /* ================= 3. Agent ReAct 循环 ================= */
  var AGENT = {
    zh: [
      { t: 'think',  x: '思考：用户问"东京现在几点穿什么"。我需要先查时间，再查天气。' },
      { t: 'tool',   x: 'get_weather(city="Tokyo")', code: '{ "tool": "get_weather", "arguments": { "city": "Tokyo" } }' },
      { t: 'obs',    x: '观察：{ "temp_c": 14, "condition": "小雨" }' },
      { t: 'think',  x: '思考：14°C 且下雨，建议外套+伞。可以回答了。' },
      { t: 'answer', x: '东京现在 14°C 有小雨，建议穿件外套并带把伞。' }
    ],
    ja: [
      { t: 'think',  x: '思考：「東京の今の服装は？」。まず天気を調べる必要がある。' },
      { t: 'tool',   x: 'get_weather(city="Tokyo")', code: '{ "tool": "get_weather", "arguments": { "city": "Tokyo" } }' },
      { t: 'obs',    x: '観察：{ "temp_c": 14, "condition": "小雨" }' },
      { t: 'think',  x: '思考：14°C で雨。上着と傘を勧めよう。回答できる。' },
      { t: 'answer', x: '東京は今 14°C で小雨です。上着を羽織って傘をお持ちください。' }
    ],
    en: [
      { t: 'think',  x: 'Think: "What to wear in Tokyo now?" I should check the weather first.' },
      { t: 'tool',   x: 'get_weather(city="Tokyo")', code: '{ "tool": "get_weather", "arguments": { "city": "Tokyo" } }' },
      { t: 'obs',    x: 'Observe: { "temp_c": 14, "condition": "light rain" }' },
      { t: 'think',  x: 'Think: 14°C and rainy — suggest a jacket and umbrella. Ready to answer.' },
      { t: 'answer', x: "It's 14°C with light rain in Tokyo — wear a jacket and bring an umbrella." }
    ]
  };
  document.querySelectorAll('[data-demo="agent"]').forEach(function (root) {
    var steps = root.querySelector(".agent-steps");
    var btn = root.querySelector(".btn");
    function run() {
      btn.disabled = true; steps.innerHTML = "";
      var data = pick(AGENT);
      data.forEach(function (s, i) {
        var el = document.createElement("div");
        el.className = "agent-step";
        var inner = '<span class="tag ' + s.t + '">' + s.t + '</span><div class="txt"><div class="line"></div>';
        if (s.code) inner += '<pre><code>' + s.code.replace(/</g, "&lt;") + '</code></pre>';
        inner += '</div>';
        el.innerHTML = inner;
        steps.appendChild(el);
        var delay = reduced() ? 0 : i * 950 + 200;
        setTimeout(function () {
          el.classList.add("show");
          el.querySelector(".line").textContent = s.x;
          if (i === data.length - 1) btn.disabled = false;
        }, delay);
      });
      if (reduced()) btn.disabled = false;
    }
    btn.addEventListener("click", run);
  });

  /* ================= 4. CLI 终端式 agent ================= */
  var CLI = {
    zh: [
      { c: '$ ', cmd: 'agent "给 utils.py 加单元测试并跑通"' },
      { o: '· 读取 utils.py …', cls: 'dim' },
      { o: '· 生成 test_utils.py（6 个用例）', cls: 'file' },
      { o: '$ pytest -q', cls: 'cmd' },
      { o: '...... 6 passed in 0.42s', cls: 'ok' },
      { o: '✓ 完成：已新增测试并全部通过', cls: 'ok' }
    ],
    ja: [
      { c: '$ ', cmd: 'agent "utils.py に単体テストを追加して通して"' },
      { o: '· utils.py を読み込み …', cls: 'dim' },
      { o: '· test_utils.py を生成（6 ケース）', cls: 'file' },
      { o: '$ pytest -q', cls: 'cmd' },
      { o: '...... 6 passed in 0.42s', cls: 'ok' },
      { o: '✓ 完了：テストを追加し全て成功', cls: 'ok' }
    ],
    en: [
      { c: '$ ', cmd: 'agent "add unit tests for utils.py and make them pass"' },
      { o: '· reading utils.py …', cls: 'dim' },
      { o: '· generating test_utils.py (6 cases)', cls: 'file' },
      { o: '$ pytest -q', cls: 'cmd' },
      { o: '...... 6 passed in 0.42s', cls: 'ok' },
      { o: '✓ done: tests added, all passing', cls: 'ok' }
    ]
  };
  document.querySelectorAll('[data-demo="cli"]').forEach(function (root) {
    var bodyEl = root.querySelector(".terminal .body");
    var btn = root.querySelector(".btn");
    function run() {
      btn.disabled = true; bodyEl.innerHTML = "";
      var data = pick(CLI);
      var idx = 0;
      function next() {
        if (idx >= data.length) { btn.disabled = false; return; }
        var s = data[idx]; idx++;
        var line = document.createElement("div"); line.className = "term-line";
        if (s.c !== undefined) {
          line.innerHTML = '<span class="pmt">' + s.c + '</span><span class="cmd"></span>';
          bodyEl.appendChild(line);
          typeInto(line.querySelector(".cmd"), s.cmd, function () { setTimeout(next, reduced() ? 0 : 250); }, 22);
        } else {
          line.innerHTML = '<span class="' + (s.cls || "") + '"></span>';
          line.firstChild.textContent = s.o;
          bodyEl.appendChild(line);
          setTimeout(next, reduced() ? 0 : 480);
        }
      }
      next();
    }
    btn.addEventListener("click", run);
  });

  /* ================= 5. IDE 行内补全 ================= */
  var IDE = {
    zh: { hint: "点「Tab ⏎ 接受」采纳灰色幽灵补全", done: "已采纳补全 ✓" },
    ja: { hint: "「Tab ⏎ 採用」でゴースト補完を採用", done: "補完を採用 ✓" },
    en: { hint: "Click “Tab ⏎ accept” to take the ghost completion", done: "completion accepted ✓" }
  };
  document.querySelectorAll('[data-demo="ide"]').forEach(function (root) {
    var ghost = root.querySelector(".ghost");
    var btn = root.querySelector(".btn");
    var status = root.querySelector(".ide-status");
    var ghostText = ghost ? ghost.textContent : "";
    function reset() {
      if (ghost) { ghost.textContent = ghostText; ghost.style.display = ""; }
      if (status) status.textContent = pick(IDE).hint;
      btn.disabled = false;
      btn.classList.remove("ghost");
    }
    function accept() {
      if (!ghost) return;
      var solid = document.createElement("span");
      solid.className = "str";
      solid.textContent = ghost.textContent;
      ghost.replaceWith(solid);
      ghost = null;
      if (status) status.textContent = pick(IDE).done;
      btn.disabled = true;
    }
    btn.addEventListener("click", accept);
    document.addEventListener("langchange", function () { if (status && !btn.disabled) status.textContent = pick(IDE).hint; });
    reset();
  });

  // 语言切换后，提示类静态文案刷新（已运行的动画不重跑）
})();
