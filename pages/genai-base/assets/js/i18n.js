/* i18n.js — 三语切换（zh / ja / en）
   策略：
   - 长篇正文用 .lang-zh/.lang-ja/.lang-en 内容块（CSS 控制显隐）。
   - 顶栏/导航/按钮等界面短文案用 data-i18n="key" + 下面的字典。
   - 选择存 localStorage，刷新记忆。 */
(function () {
  "use strict";

  var DICT = {
    zh: {
      "brand": "生成 AI × 开发 · 全体像",
      "nav.home": "全体像",
      "nav.part1": "1 · 应用方式",
      "nav.part2": "2 · 定制与标准",
      "nav.part3": "3 · 变迁与展望",
      "nav.demo": "事例",
      "nav.refs": "参照",
      "present.on": "演讲模式",
      "present.hint": "方向键 / 空格 翻屏 · Esc 退出",
      "toc": "本页目录",
      "footer": "教学演讲材料 · 静态站点 · 内容核实于 2026-05，带版本号/数字的条目请以最新官方信息为准。",
      "copy": "复制",
      "copied": "已复制",
      "lang.label": "语言"
    },
    ja: {
      "brand": "生成 AI × 開発 · 全体像",
      "nav.home": "全体像",
      "nav.part1": "1 · 活用方法",
      "nav.part2": "2 · カスタマイズと標準",
      "nav.part3": "3 · 変化と展望",
      "nav.demo": "ケーススタディ",
      "nav.refs": "参照",
      "present.on": "プレゼンモード",
      "present.hint": "矢印 / スペースで送る · Esc で終了",
      "toc": "目次",
      "footer": "教育・講演用資料 · 静的サイト · 内容は 2026-05 時点。バージョン/数値は最新の公式情報をご確認ください。",
      "copy": "コピー",
      "copied": "コピー済み",
      "lang.label": "言語"
    },
    en: {
      "brand": "Generative AI × Dev · Big Picture",
      "nav.home": "Overview",
      "nav.part1": "1 · How to Use",
      "nav.part2": "2 · Customization & Standards",
      "nav.part3": "3 · Shift & Outlook",
      "nav.demo": "Case Study",
      "nav.refs": "References",
      "present.on": "Present mode",
      "present.hint": "Arrows / Space to advance · Esc to exit",
      "toc": "On this page",
      "footer": "Teaching & talk material · static site · verified 2026-05; check official sources for versioned/numeric claims.",
      "copy": "Copy",
      "copied": "Copied",
      "lang.label": "Language"
    }
  };

  var LANGS = ["zh", "ja", "en"];

  function t(lang, key) {
    return (DICT[lang] && DICT[lang][key]) || (DICT.en[key]) || key;
  }

  function apply(lang) {
    if (LANGS.indexOf(lang) === -1) lang = "en";
    document.documentElement.setAttribute("data-lang", lang);
    document.documentElement.setAttribute("lang", lang === "zh" ? "zh-CN" : lang);

    // 文本节点
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = t(lang, el.getAttribute("data-i18n"));
    });
    // 属性（aria-label / placeholder / title）
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      var spec = el.getAttribute("data-i18n-attr"); // "attr:key"
      spec.split(",").forEach(function (pair) {
        var p = pair.split(":");
        if (p.length === 2) el.setAttribute(p[0].trim(), t(lang, p[1].trim()));
      });
    });
    // 语言按钮高亮
    document.querySelectorAll(".lang-switch button").forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-lang") === lang);
    });

    try { localStorage.setItem("site_lang", lang); } catch (e) {}
    document.dispatchEvent(new CustomEvent("langchange", { detail: { lang: lang } }));
  }

  function init() {
    var saved;
    try { saved = localStorage.getItem("site_lang"); } catch (e) {}
    apply(saved || "en");

    document.querySelectorAll(".lang-switch button").forEach(function (b) {
      b.addEventListener("click", function () { apply(b.getAttribute("data-lang")); });
    });
  }

  window.SiteI18n = { apply: apply, t: t };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
