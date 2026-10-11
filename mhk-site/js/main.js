/* ============================================
   MHK ASSO — main.js
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  // ── Navbar scroll effect ──
  const navbar = document.getElementById('navbar');
  const scrollTop = document.getElementById('scrollTop');

  const onScroll = () => {
    const y = window.scrollY;
    if (navbar) navbar.classList.toggle('scrolled', y > 60);
    if (scrollTop) scrollTop.classList.toggle('visible', y > 400);
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  // ── Hamburger menu ──
  const hamburger = document.getElementById('hamburger');
  const navLinks  = document.getElementById('navLinks');

  if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
      const open = navLinks.classList.toggle('open');
      hamburger.setAttribute('aria-expanded', open);
      // Animate bars
      const bars = hamburger.querySelectorAll('span');
      if (open) {
        bars[0].style.transform = 'translateY(7px) rotate(45deg)';
        bars[1].style.opacity   = '0';
        bars[2].style.transform = 'translateY(-7px) rotate(-45deg)';
      } else {
        bars.forEach(b => { b.style.transform = ''; b.style.opacity = ''; });
      }
    });

    // Close on nav link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
        const bars = hamburger.querySelectorAll('span');
        bars.forEach(b => { b.style.transform = ''; b.style.opacity = ''; });
      });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!navbar.contains(e.target)) {
        navLinks.classList.remove('open');
        const bars = hamburger.querySelectorAll('span');
        bars.forEach(b => { b.style.transform = ''; b.style.opacity = ''; });
      }
    });
  }

  // ── Scroll to top ──
  if (scrollTop) {
    scrollTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // ── Scroll reveal system ──
  const revealCSS = document.createElement('style');
  revealCSS.textContent = `
    .rv  { opacity:0; transform:translateY(30px);  transition:opacity .65s ease, transform .65s cubic-bezier(.22,.68,0,1.2); }
    .rvL { opacity:0; transform:translateX(-40px); transition:opacity .65s ease, transform .65s cubic-bezier(.22,.68,0,1.2); }
    .rvR { opacity:0; transform:translateX(40px);  transition:opacity .65s ease, transform .65s cubic-bezier(.22,.68,0,1.2); }
    .rvS { opacity:0; transform:scale(.93);        transition:opacity .5s ease, transform .5s cubic-bezier(.34,1.56,.64,1); }
    .rv.vi,.rvL.vi,.rvR.vi,.rvS.vi { opacity:1; transform:none; }
  `;
  document.head.appendChild(revealCSS);

  const ro = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('vi'); ro.unobserve(e.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  // Bas → haut
  document.querySelectorAll(
    '.style-card, .cours-card, .prof-card, .prof-row, .event-item, .event-card, ' +
    '.value-card, .tarif-card, .info-card, .sidebar-card, .form-card, ' +
    '.partenaire-badge, .chiffre-item, .galerie-item, .yt-card, ' +
    '.bitg-cat-card, .prof-full-card, .event-full-card, .bitg-cat'
  ).forEach(el => { el.classList.add('rv'); ro.observe(el); });

  // Gauche → droite
  document.querySelectorAll(
    '.story-text, .bitg-hero-text, .about-text, .events-header, .cta-inner'
  ).forEach(el => { el.classList.add('rvL'); ro.observe(el); });

  // Droite → gauche
  document.querySelectorAll(
    '.story-img, .about-visual'
  ).forEach(el => { el.classList.add('rvR'); ro.observe(el); });

  // Scale (badges, titres, hero cards)
  document.querySelectorAll(
    '.badge, .hero-card, .text-center, .section-title, .section-sub'
  ).forEach(el => { el.classList.add('rvS'); ro.observe(el); });

  // ── Stagger grilles ──
  document.querySelectorAll(
    '.styles-grid, .cours-grid, .profs-preview, .values-grid, .tarifs-grid, ' +
    '.chiffres-grid, .yt-grid, .events-grid, .galerie-grid'
  ).forEach(grid => {
    Array.from(grid.children).forEach((child, i) => {
      child.style.transitionDelay = `${i * 0.07}s`;
    });
  });

  // ── Active nav link ──
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPage) link.classList.add('active');
    else if (currentPage === '' && href === 'index.html') link.classList.add('active');
  });

  // ── Hero card hover parallax ──
  const heroCards = document.querySelectorAll('.hero-card');
  if (heroCards.length) {
    document.addEventListener('mousemove', (e) => {
      const cx = window.innerWidth / 2;
      const cy = window.innerHeight / 2;
      const dx = (e.clientX - cx) / cx;
      const dy = (e.clientY - cy) / cy;
      heroCards.forEach((card, i) => {
        const depth = (i + 1) * 6;
        card.style.transform += ` translate(${dx * depth}px, ${dy * depth}px)`;
      });
    });
  }

  // ── Form feedback ──
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', (e) => {
      const action = form.getAttribute('action') || '';
      if (action.includes('formspree')) {
        // Real form — let it submit
        return;
      }
      // Demo forms
      e.preventDefault();
      const btn = form.querySelector('button[type="submit"]');
      if (btn) {
        const original = btn.textContent;
        btn.textContent = '✓ Message envoyé !';
        btn.style.background = 'var(--teal)';
        btn.disabled = true;
        setTimeout(() => {
          btn.textContent = original;
          btn.style.background = '';
          btn.disabled = false;
          form.reset();
        }, 3000);
      }
    });
  });

  // ── Galerie filter (simple) ──
  document.querySelectorAll('.galerie-filters .filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.galerie-filters .filter-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

});
