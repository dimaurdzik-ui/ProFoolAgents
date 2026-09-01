#  Дизайн-бриф: Лендінг AI/ШІ Послуг

**Версія:** 1.0
**Дата:** 06.08.2026
**Тема:** Light Theme (світла)
**Формат:** Односторінковий лендінг (Single Page Application)
**Цільова аудиторія:** Бізнес-клієнти, CTO, менеджери продуктів, підприємці
**Виконавець дизайну:** UI Designer 173f

---

##  Зміст

1. [Дизайн-токени (CSS Variables)](#1-дизайн-токени-css-variables)
2. [Типографіка](#2-типографіка)
3. [Сітка та відступи](#3-сітка-та-відступи)
4. [Іконографіка](#4-іконографіка)
5. [Секція 1: Hero](#5-секція-1-hero)
6. [Секція 2: Features (Можливості)](#6-секція-2-features-можливості)
7. [Секція 3: How It Works (Як це працює)](#7-секція-3-how-it-works-як-це-працює)
8. [Секція 4: Testimonials (Відгуки)](#8-секція-4-testimonials-відгуки)
9. [Секція 5: Pricing (Тарифи)](#9-секція-5-pricing-тарифи)
10. [Секція 6: FAQ](#10-секція-6-faq)
11. [Секція 7: Contact (Контакти)](#11-секція-7-contact-контакти)
12. [Секція 8: Footer](#12-секція-8-footer)
13. [Глобальні анімації](#13-глобальні-анімації)
14. [Адаптивність (Responsive)](#14-адаптивність-responsive)
15. [Чеклист для розробника](#15-чеклист-для-розробника)

---

## 1. Дизайн-токени (CSS Variables)

```css
:root {
  /* ═══════════════════════════════════════════
     КОЛЬОРОВА ПАЛІТРА — Світла тема
     ═══════════════════════════════════════════ */

  /* --- Primary (Акцентний) — глибокий синьо-фіолетовий градієнт --- */
  --color-primary-50:  #f0f4ff;
  --color-primary-100: #dbe4ff;
  --color-primary-200: #bac8ff;
  --color-primary-300: #91a7ff;
  --color-primary-400: #748ffc;
  --color-primary-500: #5c7cfa;
  --color-primary-600: #4c6ef5;
  --color-primary-700: #4263eb;
  --color-primary-800: #3b5bdb;
  --color-primary-900: #364fc7;

  /* --- Secondary (Допоміжний) — бірюзовий/teal --- */
  --color-secondary-50:  #e6fcf5;
  --color-secondary-100: #c3fae8;
  --color-secondary-200: #96f2d7;
  --color-secondary-300: #63e6be;
  --color-secondary-400: #38d9a9;
  --color-secondary-500: #20c997;
  --color-secondary-600: #12b886;
  --color-secondary-700: #0ca678;
  --color-secondary-800: #099268;
  --color-secondary-900: #087f5b;

  /* --- Accent (Яскравий акцент) — теплий кораловий --- */
  --color-accent-50:  #fff0f3;
  --color-accent-100: #ffdee5;
  --color-accent-200: #ffb8cc;
  --color-accent-300: #ff85a8;
  --color-accent-400: #ff5c8a;
  --color-accent-500: #fa386e;
  --color-accent-600: #e61a55;
  --color-accent-700: #c21047;
  --color-accent-800: #a0103d;
  --color-accent-900: #801038;

  /* --- Neutral (Нейтральні / сірі) --- */
  --color-neutral-50:  #f8f9fa;
  --color-neutral-100: #f1f3f5;
  --color-neutral-200: #e9ecef;
  --color-neutral-300: #dee2e6;
  --color-neutral-400: #ced4da;
  --color-neutral-500: #adb5bd;
  --color-neutral-600: #868e96;
  --color-neutral-700: #495057;
  --color-neutral-800: #343a40;
  --color-neutral-900: #212529;

  /* --- Semantic (Семантичні) --- */
  --color-success:       #40c057;
  --color-success-light: #d3f9d8;
  --color-warning:       #fab005;
  --color-warning-light: #fff3bf;
  --color-error:         #f03e3e;
  --color-error-light:   #ffe3e3;
  --color-info:          #339af0;
  --color-info-light:    #d0ebff;

  /* --- Backgrounds (Фони) --- */
  --bg-page:            #ffffff;
  --bg-section-primary: #ffffff;
  --bg-section-alt:     #f8f9fa;   /* --color-neutral-50 — чергування секцій */
  --bg-card:            #ffffff;
  --bg-overlay:         rgba(33, 37, 41, 0.4);  /* модальні затемнення */

  /* --- Text (Текст) --- */
  --text-primary:       #212529;    /* --color-neutral-900 */
  --text-secondary:     #495057;    /* --color-neutral-700 */
  --text-tertiary:      #868e96;    /* --color-neutral-600 */
  --text-inverse:       #ffffff;
  --text-link:          #4c6ef5;    /* --color-primary-600 */
  --text-link-hover:    #4263eb;    /* --color-primary-700 */

  /* --- Borders (Рамки) --- */
  --border-light:       #e9ecef;    /* --color-neutral-200 */
  --border-default:     #dee2e6;    /* --color-neutral-300 */
  --border-strong:      #ced4da;    /* --color-neutral-400 */
  --border-focus:       #5c7cfa;    /* --color-primary-500 — outline для focus-visible */

  /* ═══════════════════════════════════════════
     РАДІУСИ (Border Radius)
     ═══════════════════════════════════════════ */
  --radius-none:   0;
  --radius-sm:     4px;    /* інлайн-елементи: теги, бейджі */
  --radius-md:     8px;    /* кнопки, інпути, селекти */
  --radius-lg:     12px;   /* картки, модальні вікна */
  --radius-xl:     16px;   /* великі картки (pricing, testimonials) */
  --radius-2xl:    24px;   /* hero-блоки, великі контейнери */
  --radius-full:   9999px; /* пігулки, бейджі, кнопки-пігулки */

  /* ═══════════════════════════════════════════
     ТІНІ (Box Shadows)
     ═══════════════════════════════════════════ */
  --shadow-xs:  0 1px 2px 0 rgba(0, 0, 0, 0.03);
  --shadow-sm:  0 1px 3px 0 rgba(0, 0, 0, 0.06),
                0 1px 2px -1px rgba(0, 0, 0, 0.06);
  --shadow-md:  0 4px 6px -1px rgba(0, 0, 0, 0.07),
                0 2px 4px -2px rgba(0, 0, 0, 0.06);
  --shadow-lg:  0 10px 15px -3px rgba(0, 0, 0, 0.08),
                0 4px 6px -4px rgba(0, 0, 0, 0.06);
  --shadow-xl:  0 20px 25px -5px rgba(0, 0, 0, 0.10),
                0 8px 10px -6px rgba(0, 0, 0, 0.06);
  --shadow-2xl: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  --shadow-card-hover: 0 16px 32px -8px rgba(76, 110, 245, 0.12),
                       0 4px 8px -4px rgba(0, 0, 0, 0.06);

  /* ═══════════════════════════════════════════
     ПЕРЕХОДИ (Transitions)
     ═══════════════════════════════════════════ */
  --transition-fast:    150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base:    250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow:    400ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-spring:  500ms cubic-bezier(0.34, 1.56, 0.64, 1);

  /* ═══════════════════════════════════════════
     ГРАДІЄНТИ
     ═══════════════════════════════════════════ */
  --gradient-primary:   linear-gradient(135deg, #5c7cfa 0%, #7950f2 50%, #845ef7 100%);
  --gradient-secondary: linear-gradient(135deg, #20c997 0%, #38d9a9 100%);
  --gradient-hero:      linear-gradient(180deg, #f0f4ff 0%, #ffffff 100%);
  --gradient-accent:    linear-gradient(135deg, #fa386e 0%, #ff5c8a 100%);
  --gradient-card:      linear-gradient(135deg, rgba(92,124,250,0.04) 0%, rgba(121,80,242,0.04) 100%);
  --gradient-text:      linear-gradient(135deg, #5c7cfa 0%, #845ef7 100%);

  /* ═══════════════════════════════════════════
     ШРИФТИ
     ═══════════════════════════════════════════ */
  --font-sans:      'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-display:   'Inter', var(--font-sans);
  --font-mono:      'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

  /* ═══════════════════════════════════════════
     РОЗМІРИ ШРИФТІВ (Font Sizes)
     ═══════════════════════════════════════════ */
  --text-2xs: 0.625rem;     /* 10px */
  --text-xs:  0.75rem;      /* 12px */
  --text-sm:  0.875rem;     /* 14px */
  --text-base: 1rem;        /* 16px — базовий */
  --text-lg:  1.125rem;     /* 18px */
  --text-xl:  1.25rem;      /* 20px */
  --text-2xl: 1.5rem;       /* 24px */
  --text-3xl: 1.875rem;     /* 30px */
  --text-4xl: 2.25rem;      /* 36px */
  --text-5xl: 3rem;         /* 48px */
  --text-6xl: 3.75rem;      /* 60px — тільки Hero */

  /* ═══════════════════════════════════════════
     ВІДСТУПИ (Spacing Scale — 4px base)
     ═══════════════════════════════════════════ */
  --space-0:   0;
  --space-px:  1px;
  --space-1:   0.25rem;  /* 4px */
  --space-2:   0.5rem;   /* 8px */
  --space-3:   0.75rem;  /* 12px */
  --space-4:   1rem;     /* 16px */
  --space-5:   1.25rem;  /* 20px */
  --space-6:   1.5rem;   /* 24px */
  --space-8:   2rem;     /* 32px */
  --space-10:  2.5rem;   /* 40px */
  --space-12:  3rem;     /* 48px */
  --space-14:  3.5rem;   /* 56px */
  --space-16:  4rem;     /* 64px */
  --space-20:  5rem;     /* 80px */
  --space-24:  6rem;     /* 96px */
  --space-32:  8rem;     /* 128px */

  /* ═══════════════════════════════════════════
     MACET (Layout)
     ═══════════════════════════════════════════ */
  --container-max: 1200px;
  --container-narrow: 900px;
  --container-wide: 1320px;
  --section-padding-y: var(--space-24);   /* вертикальний відступ секцій: 96px */
  --section-padding-y-mobile: var(--space-16); /* 64px на мобільних */
}
```

---

## 2. Типографіка

### 2.1. Завантаження шрифтів

```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

### 2.2. Типографічна шкала

| Рівень | Тег | Клас | font-size | line-height | font-weight | letter-spacing | Де використовується |
|--------|-----|------|-----------|-------------|-------------|----------------|---------------------|
| Display XL | h1 (Hero) | `.text-display-xl` | 60px (3.75rem) | 1.1 | 800 | -0.025em | Hero headline |
| Display L | h2 | `.text-display-l` | 48px (3rem) | 1.15 | 800 | -0.02em | Секційні заголовки |
| Heading M | h3 | `.text-heading-m` | 36px (2.25rem) | 1.25 | 700 | -0.015em | Підзаголовки секцій |
| Heading S | h4 | `.text-heading-s` | 24px (1.5rem) | 1.3 | 700 | -0.01em | Заголовки карток |
| Body L | p (lead) | `.text-body-l` | 18px (1.125rem) | 1.6 | 400 | 0 | Hero subheadline |
| Body M | p | `.text-body-m` | 16px (1rem) | 1.6 | 400 | 0 | Основний текст |
| Body S | p, span | `.text-body-s` | 14px (0.875rem) | 1.5 | 400 | 0 | Допоміжний текст, дати |
| Caption | span, label | `.text-caption` | 12px (0.75rem) | 1.5 | 500 | 0.02em | Підписи, теги, бейджі |
| Overline | span | `.text-overline` | 11px (0.6875rem) | 1.4 | 600 | 0.08em | надзаголовки (UPPERCASE) |
| Mono | code, pre | `.text-mono` | 14px (0.875rem) | 1.6 | 400 | 0 | Технічні блоки |

### 2.3. Стилі для градієнтного тексту

```css
.text-gradient {
  background: var(--gradient-text);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
/* Використовується для ключових слів у Hero та секційних заголовках */
```

### 2.4. Обмеження ширини тексту (читабельність)

```css
/* Для параграфів у hero/features — max-width для оптимальної читабельності */
.prose-max { max-width: 65ch; }
.prose-narrow { max-width: 55ch; }
```

---

## 3. Сітка та відступи

### 3.1. Загальна сітка

```css
/* 12-колонкова сітка з відступами (gutter) 24px */
.container {
  max-width: var(--container-max);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-6);   /* 24px */
  padding-right: var(--space-6);  /* 24px */
}

/* Grid utility */
.grid { display: grid; gap: var(--space-6); }
.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
/* На мобільних (< 768px) усе стає 1 колонкою: див. розділ 14 */
```

### 3.2. Вертикальний ритм секцій

Кожна секція має вертикальні відступи `--section-padding-y` (96px desktop / 64px mobile).
Чергування фонів секцій: `white → var(--bg-section-alt) → white → var(--bg-section-alt) → ...`

```
Секція 1 (Hero):         bg = var(--gradient-hero)  ← виняток
Секція 2 (Features):     bg = var(--bg-section-primary) (#fff)
Секція 3 (HowItWorks):   bg = var(--bg-section-alt) (#f8f9fa)
Секція 4 (Testimonials): bg = var(--bg-section-primary) (#fff)
Секція 5 (Pricing):      bg = var(--bg-section-alt) (#f8f9fa)
Секція 6 (FAQ):          bg = var(--bg-section-primary) (#fff)
Секція 7 (Contact):      bg = var(--bg-section-alt) (#f8f9fa)
Секція 8 (Footer):       bg = #212529 (темний, див. специфікацію)
```

### 3.3. Відступи між компонентами всередині секції

- Заголовок секції → підзаголовок: `var(--space-4)` (16px)
- Заголовок секції → перший компонент: `var(--space-12)` (48px)
- Між картками в grid: `var(--space-6)` (24px) — задано через grid gap
- Всередині картки: `var(--space-6)` padding
- Між елементами всередині картки: `var(--space-4)` (16px)

---

## 4. Іконографіка

### 4.1. Джерело іконок

**Lucide Icons** (https://lucide.dev) — відкрита бібліотека, 1400+ іконок, легкі, консистентні.
Формат: SVG, розмір за замовчуванням 24×24px.

### 4.2. Розміри іконок

| Контекст | Розмір | stroke-width | Колір |
|----------|--------|-------------|-------|
| Hero (великі декоративні) | 48-64px | 1.5 | primary-500 |
| Картки Features | 40px | 1.75 | primary-500, на primary-50 фоні |
| Кроки HowItWorks | 36px | 2 | primary-500, у circle-контейнері |
| Pricing (галочки/хрестики) | 20px | 2.5 | success / neutral-400 |
| FAQ (chevron) | 20px | 2 | neutral-500 |
| Соцмережі у Footer | 20px | 1.5 | neutral-400 → hover: primary-400 |

### 4.3. Іконки по секціях

| Секція | Призначення | Назва іконки Lucide | Стиль |
|--------|-------------|---------------------|-------|
| **Hero** | Декоративний елемент біля headline | `Sparkles` | 64px, обертання 15°, absolute позиціювання |
| **Hero** | Стрілка в CTA кнопці | `ArrowRight` | 20px, всередині кнопки |
| **Hero** | Іконка "прокрутити вниз" | `ChevronDown` | 24px, пульсуюча анімація |
| **Features** | AI Automation | `Bot` | 40px, у квадраті 72×72, `--radius-lg` |
| **Features** | Natural Language Processing | `MessageSquareText` | 40px |
| **Features** | Data Analytics | `BarChart3` | 40px |
| **Features** | 24/7 Support | `Headphones` | 40px |
| **Features** | Custom Integration | `Blocks` | 40px |
| **Features** | Security | `ShieldCheck` | 40px |
| **HowItWorks** | Крок 1: Connect | `Plug` | 36px, у круглому контейнері 72×72 |
| **HowItWorks** | Крок 2: Configure | `Settings2` | 36px |
| **HowItWorks** | Крок 3: Automate | `Play` | 36px |
| **HowItWorks** | Стрілка між кроками | `ArrowRight` | 24px, neutral-300 |
| **Testimonials** | Лапки (декоративні) | `Quote` | 32px, primary-200, absolute |
| **Testimonials** | Аватар (fallback) | `User` | 24px, всередині аватара |
| **Testimonials** | Зірки рейтингу | `Star` | 18px (×5), fill="--color-warning" |
| **Pricing** | Галочка "включено" | `Check` | 20px, color="--color-success" |
| **Pricing** | Хрестик "не включено" | `X` | 20px, color="--color-neutral-400" |
| **Pricing** | Популярний план (бейдж) | `Crown` | 16px, color="--color-warning" |
| **FAQ** | Розгорнути/згорнути | `ChevronDown` | 20px, neutral-500, rotate 180° on open |
| **FAQ** | Питання (декоративний) | `HelpCircle` | 24px, primary-300 |
| **Contact** | Email | `Mail` | 20px, всередині input group |
| **Contact** | Телефон | `Phone` | 20px |
| **Contact** | Локація | `MapPin` | 20px |
| **Contact** | Надіслати | `Send` | 20px, всередині кнопки submit |
| **Footer** | LinkedIn | Linkedin icon (якщо є) або `Globe` | 20px |
| **Footer** | Twitter/X | `Twitter` | 20px |
| **Footer** | GitHub | `Github` | 20px |
| **Footer** | YouTube | `Youtube` | 20px |
| **Header (Nav)** | Мобільне меню | `Menu` → `X` (toggle) | 24px |
| **Header (Nav)** | Логотип | `BrainCircuit` | 28px, primary-500 |

---

## 5. Секція 1: Hero

### 5.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  [Header / Navbar — фіксований, прозорий → blur on scroll] │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │                                                  │  │
│  │  ⚡ [Icon: Sparkles — абсолютне позиціювання]     │  │
│  │                                                  │  │
│  │  <span class="overline">AI-POWERED SOLUTIONS</>  │  │
│  │                                                  │  │
│  │  <h1>                                            │  │
│  │    Перетворіть ваш бізнес                        │  │
│  │    за допомогою                                  │  │
│  │    <span class="text-gradient">Штучного</span>   │  │
│  │    <span class="text-gradient">Інтелекту</span>  │  │
│  │  </h1>                                           │  │
│  │                                                  │  │
│  │  <p class="text-body-l">                         │  │
│  │    Ми допомагаємо компаніям впроваджувати         │  │
│  │    AI-рішення ... (до 2 рядків)                  │  │
│  │  </p>                                            │  │
│  │                                                  │  │
│  │  [CTA Primary: "Розпочати"] [CTA Secondary]      │  │
│  │  [Соціальний доказ: "200+ клієнтів" ...]         │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  [Hero Illustration / 3D-абстракція — справа]           │
│                                                         │
│  [↓ Scroll indicator — внизу по центру]                │
└─────────────────────────────────────────────────────────┘
```

**Ширина:** `--container-max` (1200px), вирівнювання по центру.

### 5.2. Детальні специфікації

**Фон:** `var(--gradient-hero)` — ніжний вертикальний градієнт від `#f0f4ff` (primary-50) до `#fff`.

**Overline (надзаголовок):**
```css
.hero__overline {
  font-size: var(--text-xs);           /* 12px */
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-primary-600);
  margin-bottom: var(--space-4);       /* 16px */
  display: inline-block;
  padding: var(--space-1) var(--space-3);  /* 4px 12px */
  background: rgba(76, 110, 245, 0.08);
  border-radius: var(--radius-full);
}
```

**Headline (h1):**
```css
.hero__headline {
  font-size: clamp(2.5rem, 5vw, var(--text-6xl));  /* 40px → 60px */
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  max-width: 8em;  /* обмеження ширини */
  margin-bottom: var(--space-6); /* 24px */
}
```

**Subheadline (p):**
```css
.hero__subtitle {
  font-size: var(--text-lg);      /* 18px */
  line-height: 1.6;
  color: var(--text-secondary);
  max-width: 45ch;
  margin-bottom: var(--space-10); /* 40px */
}
```

### 5.3. CTA Кнопки

```css
/* Primary CTA */
.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-8);  /* 16px 32px */
  background: var(--gradient-primary);
  color: var(--text-inverse);
  font-size: var(--text-base);
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);   /* 8px */
  cursor: pointer;
  box-shadow: 0 4px 14px 0 rgba(76, 110, 245, 0.35);
  transition: all var(--transition-base);
  text-decoration: none;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px 0 rgba(76, 110, 245, 0.45);
}
.btn-primary:active {
  transform: translateY(0);
  box-shadow: 0 2px 8px 0 rgba(76, 110, 245, 0.3);
}

/* Secondary CTA */
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4) var(--space-8);  /* 16px 32px */
  background: transparent;
  color: var(--text-primary);
  font-size: var(--text-base);
  font-weight: 600;
  border: 2px solid var(--border-strong);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  text-decoration: none;
}
.btn-secondary:hover {
  border-color: var(--color-primary-500);
  color: var(--color-primary-500);
  background: var(--color-primary-50);
}
```

**CTA Group:**
```css
.hero__cta-group {
  display: flex;
  align-items: center;
  gap: var(--space-4);  /* 16px між кнопками */
  margin-bottom: var(--space-12); /* 48px */
  flex-wrap: wrap;
}
```

### 5.4. Соціальний доказ (Social Proof)

```css
.hero__social-proof {
  display: flex;
  align-items: center;
  gap: var(--space-6);  /* 24px */
  color: var(--text-tertiary);
  font-size: var(--text-sm);  /* 14px */
}
.hero__social-proof-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}
.hero__social-proof-item strong {
  font-size: var(--text-xl);    /* 20px */
  font-weight: 700;
  color: var(--text-primary);
  display: block;
}
```

### 5.5. Hero Illustration

Справа — абстрактна 3D-ілюстрація або SVG-анімація (геометричні форми, що пливуть: кола, хвилі, точки).
Рекомендовано використовувати анімовану SVG або Lottie-анімацію.

```css
.hero__illustration {
  flex: 0 0 45%;
  max-width: 560px;
  animation: float 6s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50%      { transform: translateY(-20px); }
}
```

### 5.6. Scroll Indicator

```css
.scroll-indicator {
  position: absolute;
  bottom: var(--space-8); /* 32px */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  color: var(--text-tertiary);
  font-size: var(--text-xs);
  cursor: pointer;
  animation: bounce 2s ease-in-out infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateX(-50%) translateY(0); }
  50%      { transform: translateX(-50%) translateY(8px); }
}
```

### 5.7. Header / Navbar

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0; right: 0;
  z-index: 100;
  padding: var(--space-4) var(--space-6);  /* 16px 24px */
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: transparent;
  transition: background var(--transition-base),
              box-shadow var(--transition-base),
              padding var(--transition-base);
}
.navbar--scrolled {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: var(--shadow-sm);
  padding: var(--space-3) var(--space-6);  /* 12px 24px — трохи менше */
}
```

**Навігаційні посилання:**
```css
.nav-link {
  font-size: var(--text-sm);  /* 14px */
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  padding: var(--space-2) var(--space-3); /* 8px 12px */
  border-radius: var(--radius-md);
  transition: color var(--transition-fast),
              background var(--transition-fast);
}
.nav-link:hover {
  color: var(--color-primary-600);
  background: var(--color-primary-50);
}
```

---

## 6. Секція 2: Features (Можливості)

### 6.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  padding-y: var(--section-padding-y)   [96px]            │
│  bg: var(--bg-section-primary) [#fff]                    │
│                                                         │
│  ┌─── Заголовок секції (по центру) ──────────────────┐  │
│  │  <span class="overline">ЧОМУ ОБИРАЮТЬ НАС</span>  │  │
│  │  <h2>Ключові можливості платформи</h2>            │  │
│  │  <p class="text-body-l, prose-max, mx-auto">      │  │
│  │    Короткий опис переваг (1-2 речення)...         │  │
│  │  </p>                                             │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── Сітка 3×2 (6 карток) ─────────────────────────┐  │
│  │                                                    │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │  │
│  │  │ [Icon]   │ │ [Icon]   │ │ [Icon]   │           │  │
│  │  │ Title    │ │ Title    │ │ Title    │           │  │
│  │  │ Desc     │ │ Desc     │ │ Desc     │           │  │
│  │  └──────────┘ └──────────┘ └──────────┘           │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐           │  │
│  │  │ [Icon]   │ │ [Icon]   │ │ [Icon]   │           │  │
│  │  │ Title    │ │ Title    │ │ Title    │           │  │
│  │  │ Desc     │ │ Desc     │ │ Desc     │           │  │
│  │  └──────────┘ └──────────┘ └──────────┘           │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 6.2. Картка Feature

```css
.feature-card {
  padding: var(--space-8);       /* 32px */
  background: var(--bg-card);    /* #fff */
  border: 1px solid var(--border-light);  /* #e9ecef */
  border-radius: var(--radius-xl);       /* 16px */
  transition: all var(--transition-base);
  position: relative;
}
.feature-card:hover {
  border-color: var(--color-primary-200);
  box-shadow: var(--shadow-card-hover);
  transform: translateY(-4px);
}

/* Іконка в квадратному контейнері */
.feature-card__icon-box {
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-50);
  border-radius: var(--radius-lg);    /* 12px */
  margin-bottom: var(--space-6);      /* 24px */
  transition: background var(--transition-base),
              transform var(--transition-base);
}
.feature-card:hover .feature-card__icon-box {
  background: var(--color-primary-100);
  transform: scale(1.05);
}

.feature-card__title {
  font-size: var(--text-xl);    /* 20px */
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-3); /* 12px */
}

.feature-card__description {
  font-size: var(--text-sm);    /* 14px */
  line-height: 1.6;
  color: var(--text-secondary);
}
```

### 6.3. Анімація появи

```css
/* Scroll reveal — картки з'являються при скролі */
.feature-card {
  opacity: 0;
  transform: translateY(40px);
  transition: opacity 0.6s ease-out,
              transform 0.6s ease-out;
}
.feature-card.revealed {
  opacity: 1;
  transform: translateY(0);
}
/* Stagger delay для кожної картки */
.feature-card:nth-child(1) { transition-delay: 0ms; }
.feature-card:nth-child(2) { transition-delay: 100ms; }
.feature-card:nth-child(3) { transition-delay: 200ms; }
.feature-card:nth-child(4) { transition-delay: 300ms; }
.feature-card:nth-child(5) { transition-delay: 400ms; }
.feature-card:nth-child(6) { transition-delay: 500ms; }
```

**JS-логіка:** IntersectionObserver із `threshold: 0.15`. При входженні в область видимості додає клас `.revealed`. Спостерігач створюється один раз для всіх карток.

---

## 7. Секція 3: How It Works (Як це працює)

### 7.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  padding-y: var(--section-padding-y)   [96px]            │
│  bg: var(--bg-section-alt) [#f8f9fa]                     │
│                                                         │
│  ┌─── Заголовок секції (по центру) ──────────────────┐  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── Горизонтальна стежка з 3 кроків ───────────────┐  │
│  │                                                    │  │
│  │  [Крок 1]  ───→  [Крок 2]  ───→  [Крок 3]        │  │
│  │   (коло)   стрілка  (коло)   стрілка  (коло)      │  │
│  │   Title             Title             Title        │  │
│  │   Desc              Desc              Desc         │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 7.2. Крок (Step)

```css
.steps-container {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 0;
  position: relative;
}

.step {
  flex: 1;
  max-width: 320px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

/* З'єднувальна лінія між кроками */
.step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 36px;                  /* половина висоти circle */
  left: calc(50% + 40px);    /* початок після circle */
  width: calc(100% - 80px);
  height: 2px;
  background: var(--color-neutral-200);
  z-index: 0;
}

/* Номер кроку в колі */
.step__circle {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-full);  /* 9999px */
  background: white;
  border: 2px solid var(--color-primary-200);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: var(--space-6);     /* 24px */
  position: relative;
  z-index: 1;
  transition: all var(--transition-base);

  /* Номер всередині */
  font-size: var(--text-2xl);  /* 24px */
  font-weight: 800;
  color: var(--color-primary-500);
}
.step:hover .step__circle {
  border-color: var(--color-primary-500);
  background: var(--color-primary-50);
  box-shadow: 0 0 0 8px rgba(76, 110, 245, 0.06);
  transform: scale(1.08);
}

.step__title {
  font-size: var(--text-xl);     /* 20px */
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-3); /* 12px */
}

.step__description {
  font-size: var(--text-sm);     /* 14px */
  color: var(--text-secondary);
  line-height: 1.6;
  max-width: 28ch;
}
```

### 7.3. Анімація номерів кроків

При scroll-reveal: номер всередині `.step__circle` запускає CSS-анімацію count-up (якщо потрібна інтерактивність) або просто fade-in зі scale.

```css
.step {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.5s ease-out,
              transform 0.5s ease-out;
}
.step.revealed {
  opacity: 1;
  transform: translateY(0);
}
.step:nth-child(1) { transition-delay: 0ms; }
.step:nth-child(2) { transition-delay: 200ms; }
.step:nth-child(3) { transition-delay: 400ms; }
```

---

## 8. Секція 4: Testimonials (Відгуки)

### 8.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  padding-y: var(--section-padding-y)   [96px]            │
│  bg: var(--bg-section-primary) [#fff]                    │
│                                                         │
│  ┌─── Заголовок секції (по центру) ──────────────────┐  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── 3 картки відгуків у grid-3 ────────────────────┐  │
│  │                                                    │  │
│  │  ┌─────────────────┐ ┌─────────────────┐ ┌───────┐  │  │
│  │  │ "Quote icon     │ │                 │ │       │  │  │
│  │  │  Текст відгуку  │ │      ...        │ │  ...  │  │  │
│  │  │  (3-4 речення)  │ │                 │ │       │  │  │
│  │  │  ⭐⭐⭐⭐⭐      │ │                 │ │       │  │  │
│  │  │  [Avatar] Name │ │                 │ │       │  │  │
│  │  │  Company       │ │                 │ │       │  │  │
│  │  └─────────────────┘ └─────────────────┘ └───────┘  │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── Логотипи клієнтів (сітка 5-6 логотипів) ───────┐  │
│  │   grayscale → color on hover                        │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 8.2. Картка відгуку

```css
.testimonial-card {
  padding: var(--space-8);          /* 32px */
  background: var(--bg-card);       /* #fff */
  border: 1px solid var(--border-light);
  border-radius: var(--radius-xl);  /* 16px */
  position: relative;
  transition: all var(--transition-base);
}
.testimonial-card:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--border-default);
}

/* Декоративні лапки */
.testimonial-card::before {
  content: '';
  position: absolute;
  top: var(--space-6);   /* 24px */
  left: var(--space-6);
  /* Використовується SVG-іконка Quote як background-image
     або Lucide компонент з absolute позиціюванням */
  width: 32px;
  height: 32px;
  color: var(--color-primary-100);
}

.testimonial-card__text {
  font-size: var(--text-sm);     /* 14px */
  line-height: 1.7;
  color: var(--text-secondary);
  font-style: italic;
  margin-bottom: var(--space-6); /* 24px */
  padding-top: var(--space-6);   /* 24px — місце під лапки */
}

/* Рейтинг-зірки */
.testimonial-card__rating {
  display: flex;
  gap: 2px;
  margin-bottom: var(--space-4); /* 16px */
  color: var(--color-warning);   /* #fab005 */
}

/* Автор */
.testimonial-card__author {
  display: flex;
  align-items: center;
  gap: var(--space-3);   /* 12px */
}

.testimonial-card__avatar {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-full);
  object-fit: cover;
  background: var(--color-primary-100);
  /* fallback: іконка User */
}

.testimonial-card__name {
  font-size: var(--text-sm);   /* 14px */
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.3;
}
.testimonial-card__role {
  font-size: var(--text-xs);   /* 12px */
  color: var(--text-tertiary);
}
```

### 8.3. Логотипи клієнтів

```css
.client-logos {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--space-12);       /* 48px між логотипами */
  margin-top: var(--space-16); /* 64px */
  padding-top: var(--space-12);
  border-top: 1px solid var(--border-light);
}
.client-logos img {
  height: 32px;
  width: auto;
  filter: grayscale(100%) opacity(0.5);
  transition: filter var(--transition-base);
}
.client-logos img:hover {
  filter: grayscale(0%) opacity(1);
}
```

---

## 9. Секція 5: Pricing (Тарифи)

### 9.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  padding-y: var(--section-padding-y)   [96px]            │
│  bg: var(--bg-section-alt) [#f8f9fa]                     │
│                                                         │
│  ┌─── Заголовок секції (по центру) ──────────────────┐  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── Тарифний перемикач (monthly / yearly) ─────────┐  │
│  │   [Місяць] ──(toggle)── [Рік — знижка 20%]        │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── 3 тарифні картки (grid-3) ─────────────────────┐  │
│  │                                                    │  │
│  │  ┌─Starter──┐  ┌─Pro (популярний)─┐  ┌─Enterprise┐ │  │
│  │  │ $49/міс  │  │     $99/міс      │  │Custom     │  │
│  │  │ ...      │  │ [Crown] Популяр. │  │...        │  │
│  │  │ [CTA]    │  │ ...              │  │[CTA]      │  │
│  │  │          │  │ [CTA primary]    │  │           │  │
│  │  └──────────┘  └──────────────────┘  └───────────┘  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 9.2. Тарифний перемикач

```css
.pricing-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-4);      /* 16px */
  margin-bottom: var(--space-12);  /* 48px */
}

.pricing-toggle__label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
}
.pricing-toggle__label--active {
  color: var(--text-primary);
}

/* Toggle switch */
.toggle-switch {
  width: 52px;
  height: 28px;
  border-radius: var(--radius-full);
  background: var(--color-primary-500);
  position: relative;
  cursor: pointer;
  transition: background var(--transition-fast);
  border: none;
  padding: 0;
}
.toggle-switch::after {
  content: '';
  position: absolute;
  top: 3px;
  left: 3px;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-full);
  background: white;
  transition: transform var(--transition-base);
}
.toggle-switch--yearly::after {
  transform: translateX(24px);
}

/* Тег знижки */
.pricing-toggle__discount {
  font-size: var(--text-xs);
  font-weight: 600;
  color: var(--color-success);
  background: var(--color-success-light);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}
```

### 9.3. Тарифна картка

```css
.pricing-card {
  padding: var(--space-10) var(--space-8);  /* 40px 32px */
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-xl);         /* 16px */
  text-align: center;
  position: relative;
  transition: all var(--transition-base);
  display: flex;
  flex-direction: column;
}
.pricing-card:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--border-default);
}

/* Популярний план */
.pricing-card--popular {
  border-color: var(--color-primary-300);
  box-shadow: var(--shadow-lg);
  background: white;
  transform: scale(1.03);
  z-index: 2;
}
.pricing-card--popular:hover {
  box-shadow: var(--shadow-card-hover);
  border-color: var(--color-primary-500);
}

/* Бейдж "Популярний" */
.pricing-card__badge {
  position: absolute;
  top: -14px;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  font-weight: 600;
  color: white;
  background: var(--gradient-accent);
  padding: 6px 16px;
  border-radius: var(--radius-full);
  white-space: nowrap;
}

.pricing-card__name {
  font-size: var(--text-lg);       /* 18px */
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--space-2);
}

.pricing-card__price {
  font-size: var(--text-5xl);      /* 48px */
  font-weight: 800;
  color: var(--text-primary);
  line-height: 1;
  margin-bottom: var(--space-2);
  transition: all var(--transition-base);
}
.pricing-card__price-period {
  font-size: var(--text-sm);
  font-weight: 400;
  color: var(--text-tertiary);
  margin-bottom: var(--space-8);   /* 32px */
}

/* Список можливостей */
.pricing-card__features {
  list-style: none;
  padding: 0;
  margin: 0 0 var(--space-8) 0;
  text-align: left;
  flex: 1;
}
.pricing-card__features li {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) 0;
  font-size: var(--text-sm);
  color: var(--text-secondary);
  border-bottom: 1px solid var(--border-light);
}
.pricing-card__features li:last-child {
  border-bottom: none;
}

/* CTA в картці */
.pricing-card__cta {
  margin-top: auto;
  width: 100%;
}
/* Для популярного плану — primary кнопка */
.pricing-card--popular .pricing-card__cta {
  /* btn-primary */
}
/* Для звичайних планів — secondary кнопка */
.pricing-card:not(.pricing-card--popular) .pricing-card__cta {
  /* btn-secondary */
}
```

---

## 10. Секція 6: FAQ

### 10.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  padding-y: var(--section-padding-y)   [96px]            │
│  bg: var(--bg-section-primary) [#fff]                    │
│                                                         │
│  ┌─── Заголовок секції (по центру) ──────────────────┐  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── Макет: ліворуч іконка, праворуч accordion ─────┐  │
│  │                                                    │  │
│  │  [HelpCircle   │  ┌── Accordion Items ──────────┐  │  │
│  │   64px,        │  │                             │  │  │
│  │   primary-100] │  │  ▸ Питання 1      [−/+]    │  │  │
│  │                │  │    Відповідь...             │  │  │
│  │                │  │  ────────────────────────   │  │  │
│  │                │  │  ▸ Питання 2      [−/+]    │  │  │
│  │                │  │  ────────────────────────   │  │  │
│  │                │  │  ▸ Питання 3...             │  │  │
│  │                │  └─────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 10.2. Accordion Item

```css
.faq-container {
  display: flex;
  gap: var(--space-12);       /* 48px */
  max-width: var(--container-narrow); /* 900px */
  margin: 0 auto;
  align-items: flex-start;
}

.faq__decoration {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-50);
  border-radius: var(--radius-xl);
}

.faq__list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);        /* 8px між питаннями */
}

.faq-item {
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);  /* 12px */
  overflow: hidden;
  background: white;
  transition: all var(--transition-base);
}
.faq-item:hover {
  border-color: var(--border-default);
  box-shadow: var(--shadow-xs);
}
.faq-item--open {
  border-color: var(--color-primary-200);
  box-shadow: var(--shadow-sm);
}

/* Заголовок питання (клікабельний) */
.faq-item__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);  /* 20px 24px */
  cursor: pointer;
  user-select: none;
  font-size: var(--text-base);   /* 16px */
  font-weight: 600;
  color: var(--text-primary);
  transition: color var(--transition-fast);
}
.faq-item__header:hover {
  color: var(--color-primary-600);
}

/* Іконка chevron */
.faq-item__icon {
  width: 20px;
  height: 20px;
  color: var(--text-tertiary);
  transition: transform var(--transition-base);
  flex-shrink: 0;
}
.faq-item--open .faq-item__icon {
  transform: rotate(180deg);
  color: var(--color-primary-500);
}

/* Відповідь */
.faq-item__body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s cubic-bezier(0.4, 0, 0.2, 1),
              padding 0.3s ease;
}
.faq-item--open .faq-item__body {
  max-height: 500px; /* достатньо для будь-якої відповіді */
}

.faq-item__content {
  padding: 0 var(--space-6) var(--space-6); /* 0 24px 24px */
  font-size: var(--text-sm);     /* 14px */
  line-height: 1.7;
  color: var(--text-secondary);
}
```

### 10.3. JS-поведінка

- Відкривається не більше одного FAQ-айтема одночасно (або дозволити multiple — вибір за бізнесом; рекомендовано single-open для чистоти).
- Клік по `faq-item__header` перемикає `faq-item--open` на батьківському `.faq-item`.
- `max-height` анімація з JS-розрахунком `scrollHeight` для точності (CSS-only із запасом у 500px — прийнятний компроміс).

---

## 11. Секція 7: Contact (Контакти)

### 11.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  padding-y: var(--section-padding-y)   [96px]            │
│  bg: var(--bg-section-alt) [#f8f9fa]                     │
│                                                         │
│  ┌─── Заголовок секції (по центру) ──────────────────┐  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─── 2 колонки: форма + контактна інформація ───────┐  │
│  │                                                    │  │
│  │  ┌─ Форма (60%) ────┐  ┌─ Контакти (40%) ────┐   │  │
│  │  │                   │  │                      │   │  │
│  │  │  [Name input]    │  │  [Mail] email@...    │   │  │
│  │  │  [Email input]   │  │  [Phone] +380...     │   │  │
│  │  │  [Company input] │  │  [MapPin] Адреса     │   │  │
│  │  │  [Message textarea]│  │                      │   │  │
│  │  │  [Send button]   │  │  [Соцмережі - іконки] │   │  │
│  │  │                   │  │                      │   │  │
│  │  └───────────────────┘  └──────────────────────┘   │  │
│  └────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 11.2. Поля форми

```css
.contact-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);   /* 20px */
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);   /* 8px */
}

.form-label {
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: var(--space-3) var(--space-4);  /* 12px 16px */
  font-size: var(--text-base);             /* 16px */
  font-family: var(--font-sans);
  color: var(--text-primary);
  background: white;
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);        /* 8px */
  transition: all var(--transition-fast);
  outline: none;
}
.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--text-tertiary);
}
.form-input:focus,
.form-textarea:focus {
  border-color: var(--border-focus);
  box-shadow: 0 0 0 3px rgba(92, 124, 250, 0.15);
}
.form-input:hover:not(:focus):not(:disabled),
.form-textarea:hover:not(:focus):not(:disabled) {
  border-color: var(--border-strong);
}

.form-textarea {
  min-height: 140px;
  resize: vertical;
}

/* Стани помилки */
.form-input--error {
  border-color: var(--color-error);
}
.form-input--error:focus {
  box-shadow: 0 0 0 3px rgba(240, 62, 62, 0.15);
}
.form-error {
  font-size: var(--text-xs);
  color: var(--color-error);
}

/* Кнопка Submit */
.form-submit {
  align-self: flex-start;
  /* стилі btn-primary + */
  min-width: 180px;
}
```

### 11.3. Контактна інформація (права колонка)

```css
.contact-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-6);   /* 24px */
  padding: var(--space-6);
}

.contact-info__item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-4);   /* 16px */
}

.contact-info__icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-50);
  border-radius: var(--radius-md);
  color: var(--color-primary-500);
  flex-shrink: 0;
}

.contact-info__label {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

.contact-info__value {
  font-size: var(--text-base);
  font-weight: 500;
  color: var(--text-primary);
}
.contact-info__value a {
  color: inherit;
  text-decoration: none;
}
.contact-info__value a:hover {
  color: var(--text-link);
}
```

### 11.4. Двоколоночний макет

```css
.contact-grid {
  display: grid;
  grid-template-columns: 1fr 400px;  /* форма 60% / контакти 40% */
  gap: var(--space-16);              /* 64px */
  max-width: var(--container-max);
  margin: 0 auto;
  align-items: start;
}
```

---

## 12. Секція 8: Footer

### 12.1. Компонування

```
┌─────────────────────────────────────────────────────────┐
│  padding-y: var(--space-16) [64px]                       │
│  bg: #1a1d23 (темний, близький до neutral-900)           │
│  color: text-inverse                                     │
│                                                         │
│  ┌─── 4 колонки ────────────────────────────────────┐   │
│  │  Колонка 1   │  Колонка 2  │  Колонка 3  │ Col 4 │   │
│  │              │             │             │       │   │
│  │ [Logo]      │  Продукти   │  Ресурси    │ Підп. │   │
│  │  Опис (2-3  │  - Features │  - Blog     │ [email│   │
│  │  речення)   │  - Pricing  │  - Docs     │  input│   │
│  │             │  - API      │  - Support  │ +btn] │   │
│  │  Соцмережі  │  - ...      │  - ...      │       │   │
│  └──────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─── Bottom bar ───────────────────────────────────┐   │
│  │  © 2026 Company. All rights reserved.             │   │
│  │                     Privacy Policy | Terms of Use │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### 12.2. Детальні стилі

```css
.footer {
  background: #1a1d23;
  color: rgba(255, 255, 255, 0.7);
  padding-top: var(--space-16);    /* 64px */
  padding-bottom: var(--space-10); /* 40px */
}

.footer__grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1.5fr;
  gap: var(--space-12);            /* 48px */
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 0 var(--space-6);
}

.footer__brand-desc {
  font-size: var(--text-sm);
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
  max-width: 30ch;
  margin-top: var(--space-4);
}

.footer__socials {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-6);
}
.footer__socials a {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  background: rgba(255, 255, 255, 0.06);
  color: rgba(255, 255, 255, 0.5);
  transition: all var(--transition-fast);
}
.footer__socials a:hover {
  background: var(--color-primary-500);
  color: white;
}

.footer__heading {
  font-size: var(--text-sm);
  font-weight: 600;
  color: white;
  margin-bottom: var(--space-6);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.footer__links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}
.footer__links a {
  font-size: var(--text-sm);
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  transition: color var(--transition-fast);
}
.footer__links a:hover {
  color: white;
}

/* Email підписка (колонка 4) */
.footer__subscribe-input {
  display: flex;
  gap: var(--space-2);
  margin-top: var(--space-2);
}
.footer__subscribe-input input {
  flex: 1;
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-md);
  color: white;
  outline: none;
  transition: border-color var(--transition-fast);
}
.footer__subscribe-input input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
.footer__subscribe-input input:focus {
  border-color: rgba(255, 255, 255, 0.3);
}

/* Bottom bar */
.footer__bottom {
  margin-top: var(--space-12);   /* 48px */
  padding-top: var(--space-6);   /* 24px */
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--text-xs);
  color: rgba(255, 255, 255, 0.35);
  max-width: var(--container-max);
  margin-left: auto;
  margin-right: auto;
  padding-left: var(--space-6);
  padding-right: var(--space-6);
}
.footer__bottom-links {
  display: flex;
  gap: var(--space-6);
}
.footer__bottom-links a {
  color: rgba(255, 255, 255, 0.35);
  text-decoration: none;
}
.footer__bottom-links a:hover {
  color: rgba(255, 255, 255, 0.7);
}
```

> **Примітка:** Footer — єдиний виняток зі світлої теми. Це стандартна практика для футерів, оскільки він візуально "закриває" сторінку. Решта всіх секцій — світлі.

---

## 13. Глобальні анімації

### 13.1. Scroll Reveal (базовий)

```css
/* Загальний клас для всіх елементів, що з'являються при скролі */
.reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 0.7s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}
.reveal--visible {
  opacity: 1;
  transform: translateY(0);
}

/* Варіації напрямку */
.reveal--left  { transform: translateX(-30px); }
.reveal--right { transform: translateX(30px); }
.reveal--up    { transform: translateY(50px); }
.reveal--scale { transform: scale(0.95); }
.reveal--visible.reveal--left,
.reveal--visible.reveal--right,
.reveal--visible.reveal--up   { transform: translate(0, 0); }
.reveal--visible.reveal--scale { transform: scale(1); }
```

### 13.2. Затримки (Stagger delays)

```css
.delay-100 { transition-delay: 100ms; }
.delay-200 { transition-delay: 200ms; }
.delay-300 { transition-delay: 300ms; }
.delay-400 { transition-delay: 400ms; }
.delay-500 { transition-delay: 500ms; }
.delay-600 { transition-delay: 600ms; }
.delay-700 { transition-delay: 700ms; }
.delay-800 { transition-delay: 800ms; }
```

### 13.3. Intersection Observer (JS-реалізація)

```javascript
// Єдиний observer для всіх reveal-елементів
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal--visible');
        // Опціонально: unobserve після появи
        revealObserver.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.1,
    rootMargin: '0px 0px -40px 0px'  // трохи раніше
  }
);

document.querySelectorAll('.reveal').forEach(el => {
  revealObserver.observe(el);
});
```

### 13.4. Hover-анімації (універсальні)

| Елемент | Ефект | Тривалість |
|---------|-------|-----------|
| Картки (features, testimonials, pricing) | `translateY(-4px) + тінь посилюється` | 250ms |
| Кнопки primary | `translateY(-2px) + тінь посилюється` | 250ms |
| Кнопки secondary | `border-color → primary, background → primary-50` | 150ms |
| Посилання в nav | `color → primary, background → primary-50` | 150ms |
| Іконки в картках | `scale(1.05) + background змінюється` | 250ms |
| Логотипи клієнтів | `grayscale(0) + opacity(1)` | 250ms |
| Соцмережі у footer | `background → primary-500, color → white` | 150ms |

### 13.5. Smooth Scroll

```css
html {
  scroll-behavior: smooth;
  scroll-padding-top: 80px; /* враховує фіксований navbar */
}
```

### 13.6. Focus-visible (accessibility)

```css
:focus-visible {
  outline: 2px solid var(--border-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
/* Для кнопок та інтерактивних елементів outline зсувається всередину */
.btn-primary:focus-visible,
.btn-secondary:focus-visible {
  outline-offset: 2px;
}
```

---

## 14. Адаптивність (Responsive)

### 14.1. Breakpoints

| Назва | Ширина | Призначення |
|-------|--------|------------|
| `xs` (mobile) | 0 - 639px | Смартфони |
| `sm` (large mobile) | 640px - 767px | Великі смартфони |
| `md` (tablet) | 768px - 1023px | Планшети |
| `lg` (small desktop) | 1024px - 1279px | Ноутбуки |
| `xl` (desktop) | 1280px+ | Великі монітори |

### 14.2. Ключові адаптивні зміни

```css
/* Tablet (768px) */
@media (max-width: 1023px) {
  :root {
    --section-padding-y: var(--space-16);  /* 64px */
  }

  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }

  /* Hero */
  .hero { flex-direction: column; text-align: center; }
  .hero__illustration { order: -1; max-width: 320px; margin: 0 auto; }
  .hero__cta-group { justify-content: center; }
  .hero__headline { font-size: 2.5rem; }

  /* Contact: 2 колонки → 1 колонка */
  .contact-grid { grid-template-columns: 1fr; gap: var(--space-8); }

  /* Footer: 4 колонки → 2 */
  .footer__grid { grid-template-columns: 1fr 1fr; }

  /* FAQ: іконка ховається */
  .faq__decoration { display: none; }

  /* Pricing: вертикальний стек */
  .pricing-card--popular { transform: none; }
}

/* Mobile (639px and below) */
@media (max-width: 639px) {
  .container {
    padding-left: var(--space-4);   /* 16px */
    padding-right: var(--space-4);
  }

  .grid-2, .grid-3, .grid-4 {
    grid-template-columns: 1fr;
  }

  /* Hero */
  .hero__headline { font-size: 2rem; }
  .hero__subtitle { font-size: var(--text-base); }
  .hero__cta-group { flex-direction: column; width: 100%; }
  .hero__cta-group .btn-primary,
  .hero__cta-group .btn-secondary { width: 100%; justify-content: center; }

  /* Features: картки в 1 колонку */
  /* HowItWorks: вертикальна стежка */
  .steps-container { flex-direction: column; align-items: center; gap: var(--space-6); }
  .step:not(:last-child)::after { display: none; }

  /* Pricing: горизонтальний скрол або вертикаль */
  /* FAQ */
  .faq-container { flex-direction: column; }

  /* Footer: 2 колонки → 1 */
  .footer__grid { grid-template-columns: 1fr; }
  .footer__bottom { flex-direction: column; gap: var(--space-3); text-align: center; }

  /* Navbar */
  .navbar__links { display: none; } /* → hamburger menu */

  /* Testimonials: картки в 1 колонку */
  .testimonial-card { max-width: 400px; margin: 0 auto; }
}
```

### 14.3. Мобільне меню (Hamburger)

```css
/* Кнопка бургер-меню — видима тільки на < 768px */
.navbar__toggle {
  display: none;          /* прихована на desktop */
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-2);
  color: var(--text-primary);
}

@media (max-width: 767px) {
  .navbar__toggle { display: flex; }
}

/* Mobile menu overlay */
.mobile-menu {
  position: fixed;
  inset: 0;
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(16px);
  z-index: 200;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-8);
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--transition-base);
}
.mobile-menu--open {
  opacity: 1;
  pointer-events: auto;
}
.mobile-menu a {
  font-size: var(--text-2xl);
  font-weight: 600;
  color: var(--text-primary);
  text-decoration: none;
}
```

---

## 15. Чеклист для розробника

### 15.1. Підготовка

- [ ] Підключити Google Fonts (Inter 400/500/600/700/800/900 + JetBrains Mono)
- [ ] Встановити `lucide` або `lucide-react` для іконок
- [ ] Скопіювати CSS-змінні з розділу [1. Дизайн-токени](#1-дизайн-токени-css-variables) у `:root`
- [ ] Налаштувати `scroll-behavior: smooth` та `scroll-padding-top`
- [ ] Створити базові класи: `.container`, `.grid`, `.grid-2`, `.grid-3`, `.grid-4`

### 15.2. Базові компоненти

- [ ] `.btn-primary` — з усіма станами (hover, active, focus-visible, disabled)
- [ ] `.btn-secondary` — з усіма станами
- [ ] `.form-input` / `.form-textarea` — з normal, hover, focus, error станами
- [ ] `.card` — базові стилі картки (padding, border, radius, shadow)
- [ ] `.section` — базові відступи секції + класи `.section--alt` для чергування фону
- [ ] `.overline` — надзаголовок секції
- [ ] `.section-title` — h2 заголовок секції
- [ ] `.section-subtitle` — p підзаголовок секції

### 15.3. Секції (зверху вниз)

- [ ] **Header/Navbar** — fixed, transparent → blur on scroll, mobile hamburger menu
- [ ] **Hero** — headline з градієнтним текстом, CTA кнопки, соціальний доказ, ілюстрація, scroll indicator
- [ ] **Features** — 6 карток у grid 3×2, scroll-reveal зі stagger
- [ ] **How It Works** — 3 кроки з лінією, circle-номерами, scroll-reveal
- [ ] **Testimonials** — 3 картки відгуків + логотипи клієнтів
- [ ] **Pricing** — toggle monthly/yearly + 3 тарифні картки (одна популярна)
- [ ] **FAQ** — accordion з анімованим розгортанням, single-open
- [ ] **Contact** — форма (4 поля + submit) + контактна інформація (2 колонки)
- [ ] **Footer** — 4 колонки + bottom bar, email subscribe

### 15.4. Анімації

- [ ] IntersectionObserver для scroll-reveal (один глобальний)
- [ ] Stagger delays для карток у Features та HowItWorks
- [ ] FAQ accordion animation (max-height + JS scrollHeight)
- [ ] Pricing toggle — плавний перехід цін
- [ ] Navbar background transition on scroll
- [ ] Hero illustration float animation
- [ ] Scroll indicator bounce animation
- [ ] Hover-ефекти на всіх інтерактивних елементах

### 15.5. Адаптивність

- [ ] Mobile (< 640px): всі grid в 1 колонку, hero CTA вертикально, FAQ без іконки
- [ ] Tablet (640-1023px): grid по 2 колонки, контакти в 1 колонку
- [ ] Desktop (1024px+): повний макет
- [ ] Перевірити всі breakpoints на реальних пристроях / DevTools

### 15.6. Accessibility (A11y)

- [ ] Усі інтерактивні елементи доступні з клавіатури (Tab, Enter, Escape)
- [ ] `:focus-visible` стилі на всіх інтерактивних елементах
- [ ] `alt` атрибути на всіх зображеннях
- [ ] `aria-expanded` на FAQ accordion
- [ ] `aria-label` на кнопках з іконками без тексту
- [ ] `role="navigation"` на navbar та footer-навігації
- [ ] Контраст тексту ≥ 4.5:1 для normal text, ≥ 3:1 для large text (WCAG AA)
- [ ] `prefers-reduced-motion` — вимкнути анімації для користувачів, які цього бажають:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

### 15.7. Продуктивність

- [ ] Зображення: WebP з fallback, lazy loading (`loading="lazy"`)
- [ ] Іконки Lucide: tree-shaking (імпортувати лише використовувані)
- [ ] Шрифти: `font-display: swap`
- [ ] CSS-анімації використовують `transform` та `opacity` (GPU-прискорені)
- [ ] Уникати layout thrashing в IntersectionObserver callback

---

##  Фінальна візуальна карта

```
┌─────────────────────────────────────────────────────────────┐
│  [Header: прозорий → blur on scroll]                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ████  HERO  ████                          [Illustration]  │
│  ████  (gradient bg)                                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  ░░░░  FEATURES (6 карток, 3×2)  ░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░  bg: #fff                       ░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────────────────────────┤
│  ░░░░  HOW IT WORKS (3 кроки)  ░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░  bg: #f8f9fa                ░░░░░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────────────────────────┤
│  ░░░░  TESTIMONIALS (3 відгуки + логотипи)  ░░░░░░░░░░░░  │
│  ░░░░  bg: #fff                              ░░░░░░░░░░░░  │
├─────────────────────────────────────────────────────────────┤
│  ░░░░  PRICING (3 тарифи + toggle)  ░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░  bg: #f8f9fa                  ░░░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────────────────────────┤
│  ░░░░  FAQ (accordion)  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░  bg: #fff          ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────────────────────────┤
│  ░░░░  CONTACT (форма + контакти)  ░░░░░░░░░░░░░░░░░░░░░  │
│  ░░░░  bg: #f8f9fa                 ░░░░░░░░░░░░░░░░░░░░░░  │
├─────────────────────────────────────────────────────────────┤
│  ▓▓▓▓  FOOTER  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│  ▓▓▓▓  bg: #1a1d23 (єдиний темний елемент)  ▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────────────────────────────────┘
```

---

**Дизайнер:** UI Designer 173f
**Статус:** Готово до розробки
**Дата:** 06.08.2026
**Фреймворк:** Агностичний (CSS-змінні + HTML — працює з React, Vue, Svelte, Vanilla)
**Тема:** Light Theme (світла)
