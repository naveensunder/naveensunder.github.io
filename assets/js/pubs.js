// Abstract / Cite panels on the publication lists. One panel open per entry.
(function () {
  document.querySelectorAll(".pub-tab").forEach(function (tab) {
    tab.addEventListener("click", function () {
      var panel = document.getElementById(tab.getAttribute("data-target"));
      var entry = tab.closest(".pub");
      if (!panel || !entry) return;
      var open = tab.getAttribute("aria-expanded") === "true";
      entry.querySelectorAll(".pub-tab").forEach(function (t) {
        if (t !== tab) { t.setAttribute("aria-expanded", "false"); t.classList.remove("is-active"); }
      });
      entry.querySelectorAll(".pub-panel").forEach(function (p) { if (p !== panel) p.hidden = true; });
      tab.setAttribute("aria-expanded", String(!open));
      tab.classList.toggle("is-active", !open);
      panel.hidden = open;
    });
  });

  document.querySelectorAll(".pub-cite-panel").forEach(function (panel) {
    var formats = panel.querySelectorAll(".cite-fmt");
    var texts = panel.querySelectorAll(".cite-text");
    var copy = panel.querySelector(".cite-copy");

    formats.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var fmt = btn.getAttribute("data-fmt");
        formats.forEach(function (f) {
          f.classList.toggle("is-active", f === btn);
          f.setAttribute("aria-pressed", String(f === btn));
        });
        texts.forEach(function (t) { t.hidden = t.getAttribute("data-fmt") !== fmt; });
        copy.textContent = "Copy";
      });
    });

    copy.addEventListener("click", function () {
      var el = panel.querySelector(".cite-text:not([hidden])");
      var text = el.textContent;
      var done = function () {
        copy.textContent = "Copied";
        setTimeout(function () { copy.textContent = "Copy"; }, 1500);
      };
      var fallback = function () {
        var range = document.createRange();
        range.selectNodeContents(el);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        try { if (document.execCommand("copy")) done(); } catch (e) {}
        sel.removeAllRanges();
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else {
        fallback();
      }
    });
  });
})();
