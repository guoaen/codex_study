(() => {
  "use strict";

  const site = {
    title: "小学知识点",
    subtitle: "静态内容库",
    footer: "小学知识点静态站 · 当前包含首页、英语清单页、英语课文页和英语单词页",
    nav: [
      { id: "home", label: "首页", href: "/" },
      { id: "english", label: "英语", href: "/subjects/english/" },
    ],
  };

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function getActiveNavId() {
    if (document.body.dataset.nav) return document.body.dataset.nav;

    const path = window.location.pathname.replace(/\/index\.html$/, "/");
    const active = site.nav.find((item) => item.href === path || (item.href !== "/" && path.startsWith(item.href)));
    return active ? active.id : "home";
  }

  function renderSiteHeader() {
    const mount = document.querySelector("[data-site-header]");
    if (!mount) return;

    const activeNavId = getActiveNavId();
    const navLinks = site.nav
      .map((item) => {
        const current = item.id === activeNavId ? ' aria-current="page"' : "";
        return `<a href="${escapeHtml(item.href)}"${current}>${escapeHtml(item.label)}</a>`;
      })
      .join("");

    mount.innerHTML = `
      <header class="site-header">
        <a class="brand" href="/" aria-label="返回首页">
          <span class="brand-mark">知</span>
          <span><strong>${escapeHtml(site.title)}</strong><small>${escapeHtml(site.subtitle)}</small></span>
        </a>
        <nav class="top-nav" aria-label="主导航">
          ${navLinks}
        </nav>
      </header>
    `;
  }

  function renderSiteFooter() {
    const mount = document.querySelector("[data-site-footer]");
    if (!mount) return;
    mount.innerHTML = `
      <footer class="site-footer">
        <p>${escapeHtml(site.footer)}</p>
      </footer>
    `;
  }

  function renderBackLinks() {
    document.querySelectorAll("[data-home-back], [data-section-back]").forEach((mount) => {
      const link = document.createElement("a");
      link.className = "back-link";
      link.href = mount.dataset.href || "/";
      link.textContent = mount.dataset.label || "返回首页";
      mount.replaceWith(link);
    });
  }

  function renderReaderTools() {
    const mount = document.querySelector("[data-reader-tools]");
    if (!mount) return;

    mount.innerHTML = `
      <section class="reader-tools" aria-label="朗读工具">
        <label class="voice-control" for="voiceSelect">
          <span>朗读声音</span>
          <select id="voiceSelect" aria-label="选择朗读声音">
            <option value="__google_tts__">Google TTS（在线固定）</option>
          </select>
        </label>
        <button class="stop-btn" type="button" id="stopButton">停止朗读</button>
        <p class="tts-status" id="ttsStatus" aria-live="polite"></p>
      </section>
    `;
  }

  function renderSiteShell() {
    renderSiteHeader();
    renderSiteFooter();
    renderBackLinks();
    renderReaderTools();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderSiteShell, { once: true });
  } else {
    renderSiteShell();
  }

  window.PrimaryKnowledgeSite = site;
})();