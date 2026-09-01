(() => {
  'use strict';

  /* -----------------------------------------------------------------------
   *  Feature Detection & Environment
   *  ----------------------------------------------------------------------- */

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const hasFinePointer = matchMedia('(pointer:fine)').matches;

  /* -----------------------------------------------------------------------
   *  DOM References
   *  ----------------------------------------------------------------------- */

  const header = document.querySelector('[data-header]');
  const menu = document.querySelector('[data-menu]');
  const nav = document.querySelector('[data-nav]');
  const revealItems = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');

  /* -----------------------------------------------------------------------
   *  Mobile Menu
   *  ----------------------------------------------------------------------- */

  const isMenuOpen = () => nav?.classList.contains('is-open');

  const openMenu = () => {
    menu?.classList.add('is-open');
    nav?.classList.add('is-open');
    menu?.setAttribute('aria-expanded', 'true');
    menu?.setAttribute('aria-label', 'Закрити меню');
    document.body.style.overflow = 'hidden';
    // Focus first link inside menu
    const firstLink = nav?.querySelector('a');
    firstLink?.focus();
  };

  const closeMenu = () => {
    menu?.classList.remove('is-open');
    nav?.classList.remove('is-open');
    menu?.setAttribute('aria-expanded', 'false');
    menu?.setAttribute('aria-label', 'Відкрити меню');
    document.body.style.overflow = '';
    menu?.focus();
  };

  menu?.addEventListener('click', () => {
    isMenuOpen() ? closeMenu() : openMenu();
  });

  // Close menu on nav link click
  nav?.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  // Trap focus inside mobile menu
  nav?.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab' || !isMenuOpen()) return;
    const links = [...nav.querySelectorAll('a')];
    const first = links[0];
    const last = links[links.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  // Escape closes menu
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && isMenuOpen()) {
      closeMenu();
    }
  });

  /* -----------------------------------------------------------------------
   *  Scroll-Linked Intersection Observer (Reveal Animations)
   *  ----------------------------------------------------------------------- */

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
      // Animate counters inside revealed elements
      entry.target.querySelectorAll('[data-count]').forEach(animateCount);
    });
  }, { threshold: 0.13, rootMargin: '0px 0px -5% 0px' });

  if (reducedMotion) {
    // Show everything immediately
    revealItems.forEach((item) => item.classList.add('is-visible'));
  } else {
    revealItems.forEach((item) => revealObserver.observe(item));
  }

  /* -----------------------------------------------------------------------
   *  Counter Animation (count-up numbers)
   *  ----------------------------------------------------------------------- */

  function animateCount(element) {
    if (element.dataset.counted || reducedMotion) return;
    element.dataset.counted = 'true';
    const target = Number(element.dataset.count);
    if (Number.isNaN(target)) return;

    const started = performance.now();
    const duration = 1200;

    const frame = (now) => {
      const progress = Math.min((now - started) / duration, 1);
      // Out-quad easing for natural deceleration
      const eased = 1 - Math.pow(1 - progress, 3);
      element.textContent = String(Math.round(target * eased));
      if (progress < 1) {
        requestAnimationFrame(frame);
      }
    };
    requestAnimationFrame(frame);
  }

  // Animate counters not inside reveal containers immediately
  document.querySelectorAll('[data-count]').forEach((counter) => {
    const host = counter.closest('.reveal, .reveal-left, .reveal-right');
    if (!host) animateCount(counter);
  });

  /* -----------------------------------------------------------------------
   *  Scroll-Linked Effects (throttled via rAF)
   *  ----------------------------------------------------------------------- */

  let ticking = false;

  const updateScrollEffects = () => {
    const y = window.scrollY;

    // Header background
    header?.classList.toggle('is-scrolled', y > 18);

    // Parallax
    if (!reducedMotion) {
      document.querySelectorAll('[data-parallax]').forEach((item) => {
        const speed = Number(item.dataset.parallax);
        item.style.translate = `0 ${y * speed}px`;
      });
    }

    // Timeline progress bar
    const timeline = document.querySelector('.timeline');
    const progress = document.querySelector('[data-progress]');
    if (timeline && progress) {
      const rect = timeline.getBoundingClientRect();
      const ratio = Math.max(0, Math.min(1, (window.innerHeight * 0.62 - rect.top) / rect.height));
      progress.style.height = `${ratio * 100}%`;
    }

    // Active nav link (using findLast for correct highlight)
    const sections = [...document.querySelectorAll('main section[id]')];
    const active = sections.findLast((section) => {
      return section.getBoundingClientRect().top < window.innerHeight * 0.3;
    });

    nav?.querySelectorAll('a').forEach((link) => {
      link.classList.toggle(
        'is-active',
        active && link.getAttribute('href') === `#${active.id}`
      );
    });

    ticking = false;
  };

  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateScrollEffects);
      ticking = true;
    }
  }, { passive: true });

  // Initial call
  updateScrollEffects();

  /* -----------------------------------------------------------------------
   *  Tilt Effect (pointermove on cards)
   *  Only enabled for fine-pointer devices without reduced motion preference
   *  ----------------------------------------------------------------------- */

  if (!reducedMotion && hasFinePointer) {
    document.querySelectorAll('[data-tilt]').forEach((card) => {
      let rafId = null;

      card.addEventListener('pointermove', (event) => {
        if (rafId) return; // throttle to one per frame
        rafId = requestAnimationFrame(() => {
          const rect = card.getBoundingClientRect();
          const x = (event.clientX - rect.left) / rect.width - 0.5;
          const y = (event.clientY - rect.top) / rect.height - 0.5;
          card.style.transform = `perspective(900px) rotateX(${-y * 4}deg) rotateY(${x * 4}deg)`;
          card.style.setProperty('--mx', `${event.clientX - rect.left}px`);
          card.style.setProperty('--my', `${event.clientY - rect.top}px`);
          rafId = null;
        });
      });

      card.addEventListener('pointerleave', () => {
        if (rafId) {
          cancelAnimationFrame(rafId);
          rafId = null;
        }
        card.style.transform = '';
      });
    });
  }

  /* -----------------------------------------------------------------------
   *  FAQ Accordion — Single open item
   *  ----------------------------------------------------------------------- */

  document.querySelectorAll('details').forEach((details) => {
    details.addEventListener('toggle', () => {
      if (!details.open) return;
      document.querySelectorAll('details[open]').forEach((other) => {
        if (other !== details) other.open = false;
      });
    });
  });

  /* -----------------------------------------------------------------------
   *  Contact Form Validation
   *  ----------------------------------------------------------------------- */

  const form = document.querySelector('[data-form]');
  if (!form) return;

  const messages = {
    name: 'Вкажіть ім\'я (щонайменше 2 символи)',
    email: 'Вкажіть коректний робочий email',
    message: 'Розкажіть трохи більше про задачу',
  };

  const validateField = (field) => {
    const valid = field.checkValidity();
    field.classList.toggle('is-error', !valid);
    const error = field.parentElement?.querySelector('small');
    if (error) {
      error.textContent = valid ? '' : (messages[field.name] || 'Заповніть поле');
    }
    return valid;
  };

  // Live validation on blur
  form.querySelectorAll('[required]').forEach((field) => {
    field.addEventListener('blur', () => validateField(field));
    field.addEventListener('input', () => {
      if (field.classList.contains('is-error')) validateField(field);
    });
  });

  // Submit handler
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const fields = [...form.querySelectorAll('[required]')];
    const valid = fields.map(validateField).every(Boolean);

    if (!valid) {
      const firstInvalid = fields.find((field) => !field.checkValidity());
      firstInvalid?.focus();
      return;
    }

    // Show success state
    const success = form.querySelector('.form__success');
    if (success) {
      success.hidden = false;
      // Announce to screen readers
      success.setAttribute('aria-live', 'polite');
    }
    form.reset();
  });

  /* -----------------------------------------------------------------------
   *  Dynamic Year in Footer
   *  ----------------------------------------------------------------------- */

  const year = document.querySelector('[data-year]');
  if (year) year.textContent = new Date().getFullYear();

  /* -----------------------------------------------------------------------
   *  Reduced Motion Listener (dynamic preference changes)
   *  ----------------------------------------------------------------------- */

  window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', (event) => {
    if (event.matches) {
      // Show all reveal elements
      document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach((el) => {
        el.classList.add('is-visible');
      });
      // Reset parallax elements
      document.querySelectorAll('[data-parallax]').forEach((el) => {
        el.style.translate = '';
      });
    }
  });
})();
