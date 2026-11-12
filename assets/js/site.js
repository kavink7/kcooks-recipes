/* Small enhancements. Everything here is optional — the site works without it. */
(function () {
  'use strict';

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- Theme toggle -------------------------------------------------- */

  var root = document.documentElement;

  function currentTheme() {
    if (root.dataset.theme) return root.dataset.theme;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  document.querySelectorAll('[data-theme-toggle]').forEach(function (button) {
    button.addEventListener('click', function () {
      var next = currentTheme() === 'dark' ? 'light' : 'dark';
      root.dataset.theme = next;
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  });

  /* ---- Masthead condenses once the page scrolls ---------------------- */

  var masthead = document.querySelector('.masthead');
  if (masthead) {
    var onScroll = function () {
      masthead.classList.toggle('is-stuck', window.scrollY > 12);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- Reveal tiles as they come into view --------------------------- */

  var targets = Array.prototype.slice.call(document.querySelectorAll('.reveal'));

  function revealAll() {
    targets.forEach(function (el) { el.classList.add('is-in'); });
  }

  if (reduced || !('IntersectionObserver' in window)) {
    revealAll();
  } else {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-in');
        observer.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });

    targets.forEach(function (el) { observer.observe(el); });

    // Never let the effect be the reason something is unreadable: printing,
    // find-in-page, or an observer that simply never fires.
    window.addEventListener('beforeprint', revealAll);
    setTimeout(revealAll, 4000);
  }

  /* ---- Random recipe -------------------------------------------------- */

  document.querySelectorAll('[data-random-recipe]').forEach(function (button) {
    button.addEventListener('click', function () {
      var index = document.getElementById('recipe-index');
      if (!index) return;
      var urls = JSON.parse(index.textContent);
      if (!urls.length) return;
      var choices = urls.length > 1 ? urls.filter(function (u) { return u !== location.pathname; }) : urls;
      var pick = choices[Math.floor(Math.random() * choices.length)];
      window.location.href = pick;
    });
  });

  /* ---- Cross ingredients off as you gather them ---------------------- */

  document.querySelectorAll('.checklist').forEach(function (list) {
    list.addEventListener('click', function (event) {
      var button = event.target.closest('button');
      if (!button) return;
      button.parentElement.classList.toggle('is-got');
      button.setAttribute('aria-pressed', String(button.parentElement.classList.contains('is-got')));
    });
    list.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
  });

  /* ---- Visit counter (counts once per browser session) --------------- */

  var counter = document.querySelector('[data-visit-counter]');
  if (counter && window.fetch) {
    var base = 'https://abacus.jasoncameron.dev/';
    var key = 'kavink7-kcooks-recipes/visits';
    var counted = false;
    try { counted = sessionStorage.getItem('visit-counted') === '1'; } catch (e) {}
    fetch(base + (counted ? 'get/' : 'hit/') + key)
      .then(function (res) { return res.ok ? res.json() : Promise.reject(); })
      .then(function (data) {
        if (typeof data.value !== 'number') return;
        try { sessionStorage.setItem('visit-counted', '1'); } catch (e) {}
        counter.querySelector('[data-visit-count]').textContent = data.value.toLocaleString();
        counter.hidden = false;
      })
      .catch(function () {});
  }
})();
