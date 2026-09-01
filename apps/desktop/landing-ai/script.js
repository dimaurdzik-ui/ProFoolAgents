/**
 * НейроХаб — Landing Page JavaScript
 * =================================================
 * Features:
 *   - IntersectionObserver для анімацій при скролі
 *   - FAQ accordion (один відкритий одночасно)
 *   - Pricing toggle (місяць / рік)
 *   - Mobile menu (бургер + overlay)
 *   - Navbar scroll effect (sticky + зміна стилю)
 *   - Lucide Icons ініціалізація
 *   - Smooth scroll для anchor links
 *   - Active nav link підсвічування при скролі
 */

(function () {
  'use strict';

  // ==================== ІНІЦІАЛІЗАЦІЯ LUCIDE ICONS ====================
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  // ==================== DOM REFERENCES ====================
  const header = document.getElementById('header');
  const burger = document.getElementById('burger');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileOverlay = document.getElementById('mobileOverlay');
  const pricingSwitch = document.getElementById('pricingSwitch');
  const labelMonthly = document.getElementById('labelMonthly');
  const labelYearly = document.getElementById('labelYearly');
  const faqItems = document.querySelectorAll('[data-faq]');
  const animateElements = document.querySelectorAll('[data-animate]');
  const navLinks = document.querySelectorAll('.nav__link');
  const mobileMenuLinks = document.querySelectorAll('.mobile-menu__link');

  // ==================== 1. NAVBAR SCROLL EFFECT ====================
  let lastScrollY = 0;
  const SCROLL_THRESHOLD = 50;

  function handleNavbarScroll() {
    const scrollY = window.scrollY;

    if (scrollY > SCROLL_THRESHOLD) {
      header.classList.add('header--scrolled');
      document.body.classList.add('scrolled');
    } else {
      header.classList.remove('header--scrolled');
      document.body.classList.remove('scrolled');
    }

    lastScrollY = scrollY;
  }

  // ==================== 2. ACTIVE NAV LINK (ScrollSpy) ====================
  function updateActiveNavLink() {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.scrollY + 100;

    let currentSection = '';

    sections.forEach(function (section) {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;

      if (scrollY >= sectionTop && scrollY < sectionTop + sectionHeight) {
        currentSection = section.getAttribute('id');
      }
    });

    navLinks.forEach(function (link) {
      link.classList.remove('nav__link--active');
      const href = link.getAttribute('href');
      if (href === '#' + currentSection) {
        link.classList.add('nav__link--active');
      }
    });
  }

  // ==================== 3. INTERSECTION OBSERVER (Scroll Animations) ====================
  function initScrollAnimations() {
    if (!('IntersectionObserver' in window)) {
      // Fallback: показати всі елементи одразу
      animateElements.forEach(function (el) {
        el.classList.add('animate--visible');
      });
      return;
    }

    const observerOptions = {
      root: null,
      rootMargin: '0px 0px -60px 0px',
      threshold: 0.1,
    };

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          const el = entry.target;
          const delay = el.getAttribute('data-delay');

          if (delay) {
            el.style.transitionDelay = delay * 0.1 + 's';
          }

          el.classList.add('animate--visible');
          observer.unobserve(el);
        }
      });
    }, observerOptions);

    animateElements.forEach(function (el) {
      observer.observe(el);
    });
  }

  // ==================== 4. FAQ ACCORDION ====================
  function initFaqAccordion() {
    faqItems.forEach(function (item) {
      const questionBtn = item.querySelector('.faq__question');

      questionBtn.addEventListener('click', function () {
        const isActive = item.classList.contains('faq__item--active');

        // Закрити всі
        faqItems.forEach(function (otherItem) {
          otherItem.classList.remove('faq__item--active');
          otherItem.querySelector('.faq__question').setAttribute('aria-expanded', 'false');
        });

        // Відкрити поточний (якщо не був відкритий)
        if (!isActive) {
          item.classList.add('faq__item--active');
          questionBtn.setAttribute('aria-expanded', 'true');
        }
      });
    });
  }

  // ==================== 5. PRICING TOGGLE (Місяць / Рік) ====================
  let isYearly = false;

  function initPricingToggle() {
    function updatePrices() {
      // Оновлюємо стан toggle
      if (isYearly) {
        pricingSwitch.classList.add('pricing__switch--yearly');
        pricingSwitch.setAttribute('aria-checked', 'true');
        labelMonthly.classList.remove('pricing__toggle-label--active');
        labelYearly.classList.add('pricing__toggle-label--active');
      } else {
        pricingSwitch.classList.remove('pricing__switch--yearly');
        pricingSwitch.setAttribute('aria-checked', 'false');
        labelMonthly.classList.add('pricing__toggle-label--active');
        labelYearly.classList.remove('pricing__toggle-label--active');
      }

      // Оновлюємо ціни
      const priceElements = document.querySelectorAll('[data-price-monthly]');
      priceElements.forEach(function (el) {
        const monthly = el.getAttribute('data-price-monthly');
        const yearly = el.getAttribute('data-price-yearly');
        el.textContent = isYearly
          ? Number(yearly).toLocaleString('uk-UA')
          : Number(monthly).toLocaleString('uk-UA');
      });

      // Оновлюємо періоди
      const periodElements = document.querySelectorAll('[data-period-monthly]');
      periodElements.forEach(function (el) {
        el.textContent = isYearly
          ? el.getAttribute('data-period-yearly')
          : el.getAttribute('data-period-monthly');
      });
    }

    pricingSwitch.addEventListener('click', function () {
      isYearly = !isYearly;
      updatePrices();
    });

    // Keyboard accessibility
    pricingSwitch.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        isYearly = !isYearly;
        updatePrices();
      }
    });

    labelMonthly.addEventListener('click', function () {
      if (isYearly) {
        isYearly = false;
        updatePrices();
      }
    });

    labelYearly.addEventListener('click', function () {
      if (!isYearly) {
        isYearly = true;
        updatePrices();
      }
    });
  }

  // ==================== 6. MOBILE MENU ====================
  let isMenuOpen = false;

  function openMobileMenu() {
    isMenuOpen = true;
    mobileMenu.classList.add('mobile-menu--open');
    mobileOverlay.classList.add('mobile-menu__overlay--visible');
    burger.classList.add('burger--active');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    isMenuOpen = false;
    mobileMenu.classList.remove('mobile-menu--open');
    mobileOverlay.classList.remove('mobile-menu__overlay--visible');
    burger.classList.remove('burger--active');
    document.body.style.overflow = '';
  }

  function initMobileMenu() {
    burger.addEventListener('click', function () {
      if (isMenuOpen) {
        closeMobileMenu();
      } else {
        openMobileMenu();
      }
    });

    mobileOverlay.addEventListener('click', closeMobileMenu);

    // Закриваємо меню при кліку на посилання
    mobileMenuLinks.forEach(function (link) {
      link.addEventListener('click', closeMobileMenu);
    });

    // Закриваємо меню при натисканні Escape
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && isMenuOpen) {
        closeMobileMenu();
      }
    });
  }

  // ==================== 7. SMOOTH SCROLL ДЛЯ ВСІХ ANCHOR LINKS ====================
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href');

        if (targetId === '#') return;

        const targetElement = document.querySelector(targetId);

        if (targetElement) {
          e.preventDefault();
          const headerHeight = header.offsetHeight;
          const targetPosition =
            targetElement.getBoundingClientRect().top +
            window.pageYOffset -
            headerHeight;

          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth',
          });
        }
      });
    });
  }

  // ==================== 8. СКРОЛ-ЛІСТЕНЕР (об'єднаний) ====================
  let ticking = false;

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(function () {
        handleNavbarScroll();
        updateActiveNavLink();
        ticking = false;
      });
      ticking = true;
    }
  }

  // ==================== ІНІЦІАЛІЗАЦІЯ ====================
  function init() {
    initScrollAnimations();
    initFaqAccordion();
    initPricingToggle();
    initMobileMenu();
    initSmoothScroll();

    // Початковий стан navbar
    handleNavbarScroll();

    // Scroll listener
    window.addEventListener('scroll', onScroll, { passive: true });

    // Resize listener для закриття меню на десктопі
    window.addEventListener('resize', function () {
      if (window.innerWidth > 768 && isMenuOpen) {
        closeMobileMenu();
      }
    });
  }

  // Запускаємо після завантаження DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
