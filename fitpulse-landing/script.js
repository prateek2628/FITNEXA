/* =============================================
   FitNexa — JAVASCRIPT INTERACTIONS
   ============================================= */

// ---- NAVBAR SCROLL EFFECT ----
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
}, { passive: true });


// ---- HAMBURGER MENU ----
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');
const navCta = document.querySelector('.nav-cta');

hamburger.addEventListener('click', () => {
  const isOpen = hamburger.classList.toggle('open');
  if (isOpen) {
    navLinks.style.cssText = `
      display: flex;
      flex-direction: column;
      position: fixed;
      top: 64px;
      left: 0;
      right: 0;
      background: rgba(8, 11, 20, 0.97);
      backdrop-filter: blur(20px);
      padding: 24px;
      gap: 8px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      z-index: 999;
    `;
    hamburger.children[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
    hamburger.children[1].style.opacity = '0';
    hamburger.children[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
  } else {
    navLinks.style.display = '';
    hamburger.children[0].style.transform = '';
    hamburger.children[1].style.opacity = '';
    hamburger.children[2].style.transform = '';
  }
});

// Close menu on link click
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    navLinks.style.display = '';
    hamburger.children[0].style.transform = '';
    hamburger.children[1].style.opacity = '';
    hamburger.children[2].style.transform = '';
  });
});


// ---- SCROLL REVEAL ANIMATIONS ----
const revealElements = document.querySelectorAll([
  '.feature-card',
  '.step',
  '.stat-block',
  '.testimonial-card',
  '.pricing-card',
  '.section-header',
  '.partners-logos',
  '.cta-content'
].join(','));

revealElements.forEach(el => el.classList.add('reveal'));

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry, i) => {
    if (entry.isIntersecting) {
      // Stagger the animation for grid items
      const siblings = Array.from(entry.target.parentElement.children);
      const index = siblings.indexOf(entry.target);
      setTimeout(() => {
        entry.target.classList.add('visible');
      }, index * 80);
      revealObserver.unobserve(entry.target);
    }
  });
}, {
  threshold: 0.12,
  rootMargin: '0px 0px -40px 0px'
});

revealElements.forEach(el => revealObserver.observe(el));


// ---- COUNTER ANIMATION ----
function animateCounter(el, target, duration = 1800) {
  const start = performance.now();
  const isLarge = target > 1000;

  const update = (now) => {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // Ease out cubic
    const eased = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(eased * target);

    if (isLarge) {
      // Format millions
      if (current >= 1000000) {
        el.textContent = (current / 1000000).toFixed(1) + 'M';
      } else if (current >= 1000) {
        el.textContent = Math.floor(current / 1000) + 'K';
      } else {
        el.textContent = current;
      }
    } else {
      el.textContent = current;
    }

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      // Final value
      if (isLarge) {
        el.textContent = '2M';
      } else {
        el.textContent = target;
      }
    }
  };
  requestAnimationFrame(update);
}

const statsSection = document.getElementById('stats');
let statsAnimated = false;

const statsObserver = new IntersectionObserver((entries) => {
  if (entries[0].isIntersecting && !statsAnimated) {
    statsAnimated = true;
    document.querySelectorAll('.stat-number[data-target]').forEach(el => {
      animateCounter(el, parseInt(el.dataset.target));
    });
  }
}, { threshold: 0.3 });

if (statsSection) statsObserver.observe(statsSection);


// ---- PRICING TOGGLE ----
const toggleMonthly = document.getElementById('toggle-monthly');
const toggleAnnual = document.getElementById('toggle-annual');

function updatePrices(period) {
  document.querySelectorAll('.price-amount').forEach(el => {
    const target = period === 'monthly' ? el.dataset.monthly : el.dataset.annual;
    // Animate price change
    el.style.opacity = '0';
    el.style.transform = 'translateY(-8px)';
    setTimeout(() => {
      el.textContent = target;
      el.style.transition = 'opacity 0.25s ease, transform 0.25s ease';
      el.style.opacity = '1';
      el.style.transform = 'translateY(0)';
    }, 200);
  });
}

toggleMonthly.addEventListener('click', () => {
  toggleMonthly.classList.add('active');
  toggleAnnual.classList.remove('active');
  updatePrices('monthly');
});

toggleAnnual.addEventListener('click', () => {
  toggleAnnual.classList.add('active');
  toggleMonthly.classList.remove('active');
  updatePrices('annual');
});


// ---- ACTIVE NAV LINK HIGHLIGHT ----
const sections = document.querySelectorAll('section[id]');
const navLinkEls = document.querySelectorAll('.nav-link');

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinkEls.forEach(link => {
        link.style.color = '';
        link.style.background = '';
        if (link.getAttribute('href') === `#${entry.target.id}`) {
          link.style.color = 'var(--text-primary)';
          link.style.background = 'var(--surface-hover)';
        }
      });
    }
  });
}, { threshold: 0.4 });

sections.forEach(s => sectionObserver.observe(s));


// ---- HERO PARALLAX ----
const heroContainer = document.querySelector('.hero-container');
const heroVisual = document.getElementById('hero-visual');

window.addEventListener('mousemove', (e) => {
  if (window.innerWidth < 768) return;
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 10;

  if (heroVisual) {
    heroVisual.style.transform = `translate(${x * 0.4}px, ${y * 0.4}px)`;
  }
  if (heroContainer) {
    heroContainer.style.transform = `translate(${x * -0.15}px, ${y * -0.15}px)`;
  }
  document.querySelector('.orb-1').style.transform = `translate(${x * 0.8}px, ${y * 0.8}px)`;
  document.querySelector('.orb-2').style.transform = `translate(${x * -0.5}px, ${y * -0.5}px)`;
}, { passive: true });


// ---- FEATURE CARD TILT EFFECT ----
document.querySelectorAll('.feature-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width - 0.5) * 10;
    const y = ((e.clientY - rect.top) / rect.height - 0.5) * -10;
    card.style.transform = `translateY(-4px) rotateX(${y}deg) rotateY(${x}deg)`;
    card.style.transition = 'transform 0.1s ease';
  });

  card.addEventListener('mouseleave', () => {
    card.style.transform = '';
    card.style.transition = 'all 0.35s ease';
  });
});


// ---- TESTIMONIAL CARD CURSOR GLOW ----
document.querySelectorAll('.testimonial-card, .pricing-card').forEach(card => {
  card.addEventListener('mousemove', (e) => {
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    card.style.background = `radial-gradient(circle 200px at ${x}px ${y}px, rgba(168,85,247,0.06), transparent 60%), var(--bg-card)`;
  });

  card.addEventListener('mouseleave', () => {
    card.style.background = '';
  });
});


// ---- SMOOTH SCROLL ----
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const href = anchor.getAttribute('href');
    const target = document.querySelector(href);
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});


// ---- BUTTON RIPPLE EFFECT ----
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', function(e) {
    const ripple = document.createElement('span');
    const rect = btn.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.cssText = `
      position: absolute;
      border-radius: 50%;
      width: ${size}px;
      height: ${size}px;
      left: ${x}px;
      top: ${y}px;
      background: rgba(255,255,255,0.2);
      animation: rippleAnim 0.5s ease-out forwards;
      pointer-events: none;
      z-index: 10;
    `;

    // Add ripple keyframe if not present
    if (!document.getElementById('ripple-style')) {
      const style = document.createElement('style');
      style.id = 'ripple-style';
      style.textContent = `
        @keyframes rippleAnim {
          from { transform: scale(0); opacity: 1; }
          to { transform: scale(2); opacity: 0; }
        }
      `;
      document.head.appendChild(style);
    }

    btn.appendChild(ripple);
    setTimeout(() => ripple.remove(), 600);
  });
});


// ---- CONSOLE BRAND MESSAGE ----
console.log(`
%c⚡ FitNexa
%cBuilt with ❤️ and pure HTML + CSS + JS
`, 'font-size: 24px; font-weight: bold; color: #a855f7;', 'font-size: 14px; color: #94a3b8;');
