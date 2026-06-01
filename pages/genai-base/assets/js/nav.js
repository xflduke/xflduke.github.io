/* nav.js — 左导航 scroll-spy + 进度条 + 移动端抽屉 + 演讲模式（scroll-snap/键盘） + 代码复制 + Tabs */
(function () {
  "use strict";

  var body = document.body;

  /* ---------- 移动端导航抽屉 ---------- */
  var menuToggle = document.querySelector(".menu-toggle");
  if (menuToggle) {
    menuToggle.addEventListener("click", function () { body.classList.toggle("nav-open"); });
  }

  /* ---------- 页内目录 scroll-spy ---------- */
  var sections = Array.prototype.slice.call(document.querySelectorAll(".section[id]"));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll(".sidebar a[href^='#']"));
  var linkFor = {};
  navLinks.forEach(function (a) { linkFor[a.getAttribute("href").slice(1)] = a; });

  function setActive(id) {
    navLinks.forEach(function (a) { a.classList.remove("active"); });
    if (linkFor[id]) linkFor[id].classList.add("active");
  }

  if (sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) setActive(e.target.id);
      });
    }, { rootMargin: "-30% 0px -60% 0px", threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  // 点击页内链接后在移动端收起抽屉
  navLinks.forEach(function (a) {
    a.addEventListener("click", function () { body.classList.remove("nav-open"); });
  });

  /* ---------- 进度条 ---------- */
  var progress = document.querySelector(".scroll-progress");
  function scrollHost() {
    return body.classList.contains("present")
      ? document.querySelector(".content")
      : (document.scrollingElement || document.documentElement);
  }
  function updateProgress() {
    if (!progress) return;
    var host = scrollHost();
    var max = host.scrollHeight - host.clientHeight;
    var pct = max > 0 ? (host.scrollTop / max) * 100 : 0;
    progress.style.width = pct.toFixed(1) + "%";
  }
  window.addEventListener("scroll", updateProgress, { passive: true });

  /* ---------- 演讲模式 ---------- */
  var presentToggle = document.querySelector(".present-toggle");
  var content = document.querySelector(".content");

  function currentIndex() {
    if (!sections.length) return 0;
    var host = scrollHost();
    var top = host.scrollTop;
    var best = 0, bestDist = Infinity;
    sections.forEach(function (s, i) {
      var d = Math.abs(s.offsetTop - top);
      if (d < bestDist) { bestDist = d; best = i; }
    });
    return best;
  }

  function goTo(i) {
    if (!sections.length) return;
    i = Math.max(0, Math.min(sections.length - 1, i));
    sections[i].scrollIntoView({ behavior: "smooth", block: "start" });
    setActive(sections[i].id);
  }

  function setPresent(on) {
    body.classList.toggle("present", on);
    try { localStorage.setItem("present_mode", on ? "1" : "0"); } catch (e) {}
    if (presentToggle) presentToggle.setAttribute("aria-pressed", on ? "true" : "false");
    // 重新绑定滚动监听到正确的宿主
    if (on && content) content.addEventListener("scroll", updateProgress, { passive: true });
    updateProgress();
  }

  if (presentToggle) {
    presentToggle.addEventListener("click", function () {
      setPresent(!body.classList.contains("present"));
    });
    var savedP;
    try { savedP = localStorage.getItem("present_mode"); } catch (e) {}
    if (savedP === "1") setPresent(true);
  }

  document.addEventListener("keydown", function (e) {
    if (!body.classList.contains("present")) return;
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea") return;

    switch (e.key) {
      case "ArrowDown": case "ArrowRight": case "PageDown": case " ":
        e.preventDefault(); goTo(currentIndex() + 1); break;
      case "ArrowUp": case "ArrowLeft": case "PageUp":
        e.preventDefault(); goTo(currentIndex() - 1); break;
      case "Home": e.preventDefault(); goTo(0); break;
      case "End": e.preventDefault(); goTo(sections.length - 1); break;
      case "Escape": setPresent(false); break;
    }
  });

  /* ---------- 主题（浅色 / 深色） ---------- */
  var themeBtn = document.querySelector(".theme-toggle");
  function setTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    try { localStorage.setItem("site_theme", t); } catch (e) {}
    if (themeBtn) themeBtn.textContent = (t === "light") ? "🌙" : "☀";
    document.dispatchEvent(new CustomEvent("themechange", { detail: { theme: t } }));
  }
  if (themeBtn) {
    var savedT;
    try { savedT = localStorage.getItem("site_theme"); } catch (e) {}
    setTheme(savedT || document.documentElement.getAttribute("data-theme") || "dark");
    themeBtn.addEventListener("click", function () {
      var cur = document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark";
      setTheme(cur === "light" ? "dark" : "light");
    });
  }

  /* ---------- 字号（S / M / L） ---------- */
  var fsButtons = Array.prototype.slice.call(document.querySelectorAll(".fs-switch button"));
  function setFs(f) {
    document.documentElement.setAttribute("data-fs", f);
    try { localStorage.setItem("site_fs", f); } catch (e) {}
    fsButtons.forEach(function (b) { b.classList.toggle("active", b.getAttribute("data-fs") === f); });
  }
  if (fsButtons.length) {
    var savedF;
    try { savedF = localStorage.getItem("site_fs"); } catch (e) {}
    setFs(savedF || document.documentElement.getAttribute("data-fs") || "m");
    fsButtons.forEach(function (b) {
      b.addEventListener("click", function () { setFs(b.getAttribute("data-fs")); });
    });
  }

  /* ---------- 代码复制按钮 ---------- */
  function copyLabel() { return window.SiteI18n ? window.SiteI18n.t(document.documentElement.getAttribute("data-lang") || "zh", "copy") : "复制"; }
  function copiedLabel() { return window.SiteI18n ? window.SiteI18n.t(document.documentElement.getAttribute("data-lang") || "zh", "copied") : "已复制"; }

  document.querySelectorAll("pre > code").forEach(function (code) {
    var pre = code.parentElement;
    if (pre.parentElement && pre.parentElement.classList.contains("code-block")) return;
    var wrap = document.createElement("div");
    wrap.className = "code-block";
    pre.parentNode.insertBefore(wrap, pre);
    wrap.appendChild(pre);
    var btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.textContent = copyLabel();
    wrap.appendChild(btn);
    btn.addEventListener("click", function () {
      navigator.clipboard.writeText(code.innerText).then(function () {
        btn.textContent = copiedLabel(); btn.classList.add("ok");
        setTimeout(function () { btn.textContent = copyLabel(); btn.classList.remove("ok"); }, 1600);
      });
    });
  });
  document.addEventListener("langchange", function () {
    document.querySelectorAll(".copy-btn:not(.ok)").forEach(function (b) { b.textContent = copyLabel(); });
  });

  /* ---------- Tabs ---------- */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var btns = group.querySelectorAll(".tab-btn");
    var panes = group.querySelectorAll(".tab-panes > .pane");
    btns.forEach(function (b, i) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.classList.remove("active"); });
        panes.forEach(function (x) { x.classList.remove("active"); });
        b.classList.add("active");
        if (panes[i]) panes[i].classList.add("active");
      });
    });
  });

  /* ---------- 图片失败回退 ---------- */
  document.querySelectorAll(".figure img").forEach(function (img) {
    img.addEventListener("error", function () {
      var fig = img.closest(".figure");
      if (fig) {
        img.style.display = "none";
        fig.classList.add("placeholder");
        if (!fig.querySelector(".ph-label")) {
          var d = document.createElement("div");
          d.className = "ph-label";
          d.textContent = img.getAttribute("data-ph") || "（图示）";
          fig.appendChild(d);
        }
      }
    });
  });

  updateProgress();
})();
