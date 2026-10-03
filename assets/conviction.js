/* ConvertCPG site behaviors. Each block only runs when its markup is on the page. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Mobile menu */
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.menu-toggle');
  if (header && toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    header.addEventListener('click', function (e) {
      if (e.target.closest('.site-nav a')) { header.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('is-open')) { header.classList.remove('is-open'); toggle.setAttribute('aria-expanded', 'false'); toggle.focus(); }
    });
  }

  /* Rail demo (homepage phone) */
  var steps = document.querySelectorAll('[data-rail-step]');
  if (steps.length) {
    var phone = document.querySelector('.phone');
    var set = function (i) {
      steps.forEach(function (b, j) { b.setAttribute('aria-pressed', j === i ? 'true' : 'false'); });
      var s = steps[i].dataset;
      phone.querySelector('[data-f="section"]').textContent = s.section;
      phone.querySelector('[data-f="headline"]').textContent = s.headline;
      phone.querySelector('[data-f="body"]').textContent = s.body;
      phone.querySelector('[data-f="rail"]').textContent = s.railText;
      phone.querySelector('[data-f="support"]').textContent = s.support;
      phone.querySelector('[data-f="button"]').textContent = s.button;
      phone.querySelectorAll('.phone__img img').forEach(function (img, j) { img.classList.toggle('is-on', j === i); });
    };
    steps.forEach(function (b, i) { b.addEventListener('click', function () { set(i); }); });
  }

  /* The site's own Rail: appears after the hero, message follows the section on screen */
  var rail = document.querySelector('.site-rail');
  if (rail && 'IntersectionObserver' in window) {
    document.body.classList.add('has-rail');
    var hero = document.querySelector('[data-rail-hide]');
    var footer = document.querySelector('.site-footer');
    var headline = rail.querySelector('b');
    var sub = rail.querySelector('span');
    var current = null, heroVisible = true, footerVisible = false;
    var update = function () {
      var show = !heroVisible && !footerVisible;
      rail.classList.toggle('is-shown', show);
      rail.toggleAttribute('inert', !show);
      rail.setAttribute('aria-hidden', show ? 'false' : 'true');
    };
    new IntersectionObserver(function (en) { heroVisible = en[0].isIntersecting; update(); }).observe(hero);
    if (footer) new IntersectionObserver(function (en) { footerVisible = en[0].isIntersecting; update(); }).observe(footer);
    var swap = function (el) {
      if (el === current) return;
      current = el;
      var go = function () { headline.textContent = el.dataset.rail; sub.textContent = el.dataset.railSub || ''; rail.classList.remove('is-swapping'); };
      if (reduce) { go(); return; }
      rail.classList.add('is-swapping');
      setTimeout(go, 160);
    };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) swap(en.target); });
    }, { rootMargin: '-50% 0px -50% 0px' });
    document.querySelectorAll('[data-rail]').forEach(function (el) { io.observe(el); });
  }

  /* FAQ topic filter */
  var topicButtons = document.querySelectorAll('[data-topic]');
  if (topicButtons.length) {
    var items = document.querySelectorAll('[data-topics]');
    topicButtons.forEach(function (b) {
      b.addEventListener('click', function () {
        var t = b.dataset.topic;
        topicButtons.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        items.forEach(function (it) { it.hidden = !(t === 'all' || it.dataset.topics === t); });
      });
    });
  }

  /* Services: booking calendar dialog */
  var cal = document.getElementById('cal');
  if (cal) {
    var frame = cal.querySelector('iframe');
    var opener = null;
    document.querySelectorAll('[data-open-cal]').forEach(function (b) {
      b.addEventListener('click', function (e) {
        e.preventDefault();
        opener = b;
        if (!frame.src) frame.src = frame.dataset.src;
        if (typeof cal.showModal === 'function') cal.showModal(); else window.open(frame.dataset.src, '_blank');
      });
    });
    cal.querySelector('[data-close-cal]').addEventListener('click', function () { cal.close(); });
    cal.addEventListener('click', function (e) { if (e.target === cal) cal.close(); });
    cal.addEventListener('close', function () { if (opener) opener.focus(); });
  }

  /* Services: free audit prompts signup (Cloudflare Worker -> beehiiv) */
  var audit = document.getElementById('audit-form');
  if (audit) {
    audit.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = audit.querySelector('button');
      var st = document.getElementById('audit-status');
      var email = audit.elements.email.value.trim();
      if (!email) return;
      var q = new URLSearchParams(location.search);
      btn.disabled = true; var old = btn.textContent; btn.textContent = 'Sending...';
      fetch(audit.action, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({
        email: email,
        utm_source: q.get('utm_source') || 'website',
        utm_medium: q.get('utm_medium') || 'organic',
        utm_campaign: q.get('utm_campaign') || ''
      }) })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (!d.ok) throw new Error(d.error || '');
          audit.hidden = true; st.textContent = 'Done. The 7 prompts are on their way to your inbox.'; st.hidden = false;
        })
        .catch(function (err) {
          st.textContent = (err && err.message) || 'Something went wrong. Try again.'; st.hidden = false;
          btn.disabled = false; btn.textContent = old;
        });
    });
  }
})();
