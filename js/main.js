/* =========================================================
   Estatein — интерактив вёрстки
   Всё на ванильном JS, без зависимостей.
   ========================================================= */
(function () {
  "use strict";

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ---------- Верхняя полоса: закрытие ---------- */
  function initTopbar() {
    var bar = $("[data-topbar]");
    if (!bar) return;
    try {
      if (sessionStorage.getItem("estatein:topbar") === "closed") bar.hidden = true;
    } catch (e) { /* приватный режим */ }

    var close = $("[data-topbar-close]", bar);
    if (!close) return;
    close.addEventListener("click", function () {
      bar.hidden = true;
      try { sessionStorage.setItem("estatein:topbar", "closed"); } catch (e) {}
    });
  }

  /* ---------- Мобильное меню ---------- */
  function initMenu() {
    var menu = $("[data-menu]");
    var open = $("[data-menu-open]");
    var close = $("[data-menu-close]");
    if (!menu || !open) return;

    function setOpen(state) {
      menu.classList.toggle("is-open", state);
      document.body.classList.toggle("is-locked", state);
      open.setAttribute("aria-expanded", String(state));
      menu.setAttribute("aria-hidden", String(!state));
    }

    open.addEventListener("click", function () { setOpen(true); });
    if (close) close.addEventListener("click", function () { setOpen(false); });
    $$("a", menu).forEach(function (a) {
      a.addEventListener("click", function () { setOpen(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
    window.addEventListener("resize", function () {
      if (window.innerWidth >= 1024) setOpen(false);
    });
    setOpen(false);
  }

  /* ---------- Слайдеры (объекты, отзывы, FAQ, клиенты) ---------- */
  function initSliders() {
    $$("[data-slider]").forEach(function (root) {
      var track = $("[data-slider-track]", root);
      if (!track) return;

      var prev = $("[data-slider-prev]", root);
      var next = $("[data-slider-next]", root);
      var current = $("[data-slider-current]", root);
      var total = $("[data-slider-total]", root);
      var slides = $$(":scope > *", track);
      var index = 0;

      function perView() {
        var w = window.innerWidth;
        if (root.classList.contains("slider--2")) return w >= 1024 ? 2 : 1;
        if (w >= 1024) return 3;
        if (w >= 720) return 2;
        return 1;
      }

      function maxIndex() {
        return Math.max(0, slides.length - perView());
      }

      function pad(n) { return (n < 10 ? "0" : "") + n; }

      function render() {
        index = Math.min(index, maxIndex());
        var slide = slides[0];
        if (!slide) return;
        var gap = parseFloat(getComputedStyle(track).columnGap || "0") || 0;
        var step = slide.getBoundingClientRect().width + gap;
        track.style.translate = -(step * index) + "px";
        if (prev) prev.disabled = index === 0;
        if (next) next.disabled = index >= maxIndex();
        if (current) current.textContent = pad(index + 1);
        if (total) {
          var declared = parseInt(total.getAttribute("data-total") || "0", 10);
          total.textContent = pad(declared || slides.length);
        }
      }

      if (prev) prev.addEventListener("click", function () { index = Math.max(0, index - 1); render(); });
      if (next) next.addEventListener("click", function () { index = Math.min(maxIndex(), index + 1); render(); });

      /* свайп на тач-устройствах */
      var startX = null;
      track.addEventListener("touchstart", function (e) { startX = e.touches[0].clientX; }, { passive: true });
      track.addEventListener("touchend", function (e) {
        if (startX === null) return;
        var dx = e.changedTouches[0].clientX - startX;
        if (Math.abs(dx) > 45) {
          index = dx < 0 ? Math.min(maxIndex(), index + 1) : Math.max(0, index - 1);
          render();
        }
        startX = null;
      });

      window.addEventListener("resize", debounce(render, 150));
      render();
    });
  }

  /* ---------- Галерея на странице объекта ---------- */
  function initViewer() {
    var viewer = $("[data-viewer]");
    if (!viewer) return;

    var thumbs = $$("[data-viewer-thumb]", viewer);
    var stage = $$("[data-viewer-stage] img", viewer);
    var dots = $$("[data-viewer-dots] span", viewer);
    var prev = $("[data-viewer-prev]", viewer);
    var next = $("[data-viewer-next]", viewer);
    if (!thumbs.length || stage.length < 2) return;

    var pairs = [];
    for (var i = 0; i < thumbs.length; i += 2) {
      pairs.push([thumbs[i], thumbs[i + 1] || thumbs[i]]);
    }
    var index = 0;

    function render() {
      var pair = pairs[index];
      stage[0].src = pair[0].getAttribute("data-full");
      stage[0].alt = pair[0].getAttribute("data-alt") || "";
      stage[1].src = pair[1].getAttribute("data-full");
      stage[1].alt = pair[1].getAttribute("data-alt") || "";
      thumbs.forEach(function (t, i) {
        t.classList.toggle("is-active", i === index * 2 || i === index * 2 + 1);
      });
      dots.forEach(function (d, i) { d.classList.toggle("is-active", i === index); });
    }

    thumbs.forEach(function (t, i) {
      t.addEventListener("click", function () { index = Math.floor(i / 2); render(); });
    });
    if (prev) prev.addEventListener("click", function () {
      index = (index - 1 + pairs.length) % pairs.length; render();
    });
    if (next) next.addEventListener("click", function () {
      index = (index + 1) % pairs.length; render();
    });
    render();
  }

  /* ---------- Табы (офисы) ---------- */
  function initTabs() {
    $$("[data-tabs]").forEach(function (root) {
      var buttons = $$("[data-tab]", root);
      var targetSel = root.getAttribute("data-tabs");
      var panel = $(targetSel);
      if (!panel) return;
      var items = $$("[data-tab-item]", panel);

      buttons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var value = btn.getAttribute("data-tab");
          buttons.forEach(function (b) {
            b.classList.toggle("is-active", b === btn);
            b.setAttribute("aria-selected", String(b === btn));
          });
          items.forEach(function (item) {
            var kind = item.getAttribute("data-tab-item");
            item.hidden = !(value === "all" || kind === value);
          });
        });
      });
    });
  }

  /* ---------- Формы ---------- */
  function initForms() {
    /* select меняет цвет, когда выбрано значение */
    $$(".control select").forEach(function (sel) {
      var sync = function () { sel.classList.toggle("is-filled", !!sel.value); };
      sel.addEventListener("change", sync);
      sync();
    });

    $$("form[data-form]").forEach(function (form) {
      var status = $("[data-form-status]", form);

      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var ok = true;

        $$("[required]", form).forEach(function (input) {
          var field = input.closest(".field") || input.closest(".checkbox");
          var valid = input.type === "checkbox" ? input.checked : String(input.value).trim() !== "";
          if (valid && input.type === "email") {
            valid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value.trim());
          }
          if (field && field.classList) field.classList.toggle("has-error", !valid);
          if (!valid) ok = false;
        });

        if (!ok) {
          if (status) status.textContent = "Please fill in the required fields correctly.";
          return;
        }
        if (status) status.textContent = "Thanks! Your message has been sent.";
        form.reset();
        $$(".control select", form).forEach(function (s) { s.classList.remove("is-filled"); });
      });
    });
  }

  /* ---------- Плавное появление секций ---------- */
  function initReveal() {
    var items = $$(".reveal");
    if (!items.length || !("IntersectionObserver" in window)) {
      items.forEach(function (i) { i.classList.add("is-visible"); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });
    items.forEach(function (i) { io.observe(i); });
  }

  /* ---------- Мелочи ---------- */
  function debounce(fn, wait) {
    var t;
    return function () {
      clearTimeout(t);
      t = setTimeout(fn, wait);
    };
  }

  function initYear() {
    $$("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initTopbar();
    initMenu();
    initSliders();
    initViewer();
    initTabs();
    initForms();
    initReveal();
    initYear();
  });
})();
