/* ── Hero Slider ── */
(function () {
  const slides = document.querySelectorAll('.hero-slide');
  const dots   = document.querySelectorAll('.hero-dot');
  if (!slides.length) return;
  let cur = 0;
  function go(n) {
    slides[cur].classList.remove('opacity-100');
    slides[cur].classList.add('opacity-0');
    dots[cur]?.classList.remove('bg-primary-600', 'w-7');
    dots[cur]?.classList.add('bg-white/40', 'w-2');
    cur = n;
    slides[cur].classList.remove('opacity-0');
    slides[cur].classList.add('opacity-100');
    dots[cur]?.classList.remove('bg-white/40', 'w-2');
    dots[cur]?.classList.add('bg-primary-600', 'w-7');
  }
  dots.forEach((d, i) => d.addEventListener('click', () => { clearInterval(timer); go(i); timer = setInterval(() => go((cur + 1) % slides.length), 6000); }));
  let timer = setInterval(() => go((cur + 1) % slides.length), 6000);
})();

/* ── Stats Counter ── */
(function () {
  const counters = document.querySelectorAll('[data-count]');
  if (!counters.length) return;
  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el  = entry.target;
      const end = parseInt(el.dataset.count, 10);
      const dur = 2000;
      let start = null;
      function step(ts) {
        if (!start) start = ts;
        const p = Math.min((ts - start) / dur, 1);
        el.textContent = Math.floor((1 - Math.pow(1 - p, 3)) * end).toLocaleString();
        if (p < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
      obs.unobserve(el);
    });
  }, { threshold: 0.4 });
  counters.forEach(c => obs.observe(c));
})();

/* ── Job accordion ── */
document.querySelectorAll('.job-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const detail = btn.closest('.job-card').querySelector('.job-detail');
    const arrow  = btn.querySelector('.job-arrow');
    const open   = !detail.classList.contains('hidden');
    detail.classList.toggle('hidden', open);
    arrow.style.transform = open ? '' : 'rotate(180deg)';
  });
});
