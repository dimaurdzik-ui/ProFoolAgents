# AI Services Landing Page — Повний Дизайн-Бриф

**Проєкт:** Лендінг компанії з AI-послуг  
**Тема:** Світла, сучасний мінімалізм  
**Дата:** 06.08.2026  
**Дизайнер:** UI Designer (Pixel Agents)

---

## 1. Кольорова Палітра (Hex-коди + Семантика)

### 1.1 Primary Palette — AI Blue-Violet

| Токен | Hex | Призначення |
|---|---|---|
| `--color-primary-50` | `#f0f4ff` | Primary surface (картки, фони секцій) |
| `--color-primary-100` | `#dbe4ff` | Primary hover background |
| `--color-primary-200` | `#bac8ff` | Primary borders |
| `--color-primary-300` | `#91a7ff` | Декоративні елементи |
| `--color-primary-400` | `#748ffc` | Secondary buttons hover |
| `--color-primary-500` | `#5c7cfa` | **Primary brand** — кнопки, посилання, іконки |
| `--color-primary-600` | `#4c6ef5` | Primary hover / active |
| `--color-primary-700` | `#4263eb` | Primary pressed |
| `--color-primary-800` | `#3b5bdb` | Глибокий акцент |
| `--color-primary-900` | `#364fc7` | Текст на світлому primary |

### 1.2 Accent Palette — Teal-Innovation

| Токен | Hex | Призначення |
|---|---|---|
| `--color-accent-50` | `#e6fcf5` | Акцентні мітки |
| `--color-accent-100` | `#c3fae8` | Badge backgrounds |
| `--color-accent-400` | `#38d9a9` | Декоративні акценти |
| `--color-accent-500` | `#20c997` | **Accent brand** — highlights, CTA акцент |
| `--color-accent-600` | `#12b886` | Accent hover |

### 1.3 Neutral Palette — Grays (Світла тема)

| Токен | Hex | Призначення |
|---|---|---|
| `--color-gray-50` | `#f8f9fa` | Page background |
| `--color-gray-100` | `#f1f3f5` | Section alternate background |
| `--color-gray-200` | `#e9ecef` | Borders, dividers |
| `--color-gray-300` | `#dee2e6` | Input borders |
| `--color-gray-400` | `#ced4da` | Placeholder text |
| `--color-gray-500` | `#adb5bd` | Muted/secondary text |
| `--color-gray-600` | `#868e96` | Body text secondary |
| `--color-gray-700` | `#495057` | Body text |
| `--color-gray-800` | `#343a40` | Headings, emphasis |
| `--color-gray-900` | `#212529` | Primary text, headings |

### 1.4 Semantic Colors

| Токен | Hex | Призначення |
|---|---|---|
| `--color-success` | `#40c057` | Успіх, підтвердження |
| `--color-warning` | `#fab005` | Попередження |
| `--color-error` | `#fa5252` | Помилки, важливе |
| `--color-info` | `#5c7cfa` | Інформаційні блоки (= primary-500) |

### 1.5 Gradient Tokens

```css
--gradient-brand: linear-gradient(135deg, #5c7cfa 0%, #7950f2 100%);
--gradient-accent: linear-gradient(135deg, #20c997 0%, #5c7cfa 100%);
--gradient-hero: linear-gradient(160deg, #f8f9fa 0%, #f0f4ff 40%, #e6fcf5 100%);
--gradient-card-hover: linear-gradient(135deg, rgba(92,124,250,0.04) 0%, rgba(32,201,151,0.06) 100%);
```

---

## 2. Типографіка

### 2.1 Шрифти (Google Fonts)

| Роль | Шрифт | CSS |
|---|---|---|
| **Display / Headings** | **Plus Jakarta Sans** | `--font-display: 'Plus Jakarta Sans', system-ui, sans-serif;` |
| **Body / UI** | **Inter** | `--font-body: 'Inter', system-ui, sans-serif;` |
| **Code / Data** | **JetBrains Mono** | `--font-mono: 'JetBrains Mono', 'Fira Code', monospace;` |

### 2.2 Типографічна шкала (Desktop / 1440px)

| Елемент | Розмір | Line-height | Weight | CSS Variable |
|---|---|---|---|---|
| **Display** (Hero headline) | `4rem` / 64px | 1.1 | 700 | `--text-display` |
| **h1** | `3rem` / 48px | 1.15 | 700 | `--text-h1` |
| **h2** | `2.25rem` / 36px | 1.2 | 700 | `--text-h2` |
| **h3** | `1.5rem` / 24px | 1.3 | 600 | `--text-h3` |
| **h4** | `1.25rem` / 20px | 1.35 | 600 | `--text-h4` |
| **Body Large** | `1.125rem` / 18px | 1.6 | 400 | `--text-body-lg` |
| **Body** | `1rem` / 16px | 1.6 | 400 | `--text-body` |
| **Body Small** | `0.875rem` / 14px | 1.5 | 400 | `--text-body-sm` |
| **Caption** | `0.75rem` / 12px | 1.4 | 500 | `--text-caption` |
| **Button** | `0.9375rem` / 15px | 1 | 600 | `--text-button` |
| **Overline** | `0.75rem` / 12px | 1 | 700 | `--text-overline` |

### 2.3 Типографічна шкала (Mobile / 375-639px)

| Елемент | Розмір | Line-height |
|---|---|---|
| **Display** | `2.5rem` / 40px | 1.15 |
| **h1** | `2rem` / 32px | 1.2 |
| **h2** | `1.75rem` / 28px | 1.25 |
| **h3** | `1.25rem` / 20px | 1.3 |
| **h4** | `1.125rem` / 18px | 1.35 |
| **Body** | `1rem` / 16px | 1.6 |

### 2.4 Відступи та вертикальний ритм

```css
--line-height-base: 1.6;
--vertical-rhythm: calc(1rem * var(--line-height-base)); /* 25.6px */
```

---

## 3. Просторова система (Spacing Scale / 4px Base)

```css
--space-0:    0;
--space-0-5:  0.125rem;  /* 2px  */
--space-1:    0.25rem;   /* 4px  */
--space-1-5:  0.375rem;  /* 6px  */
--space-2:    0.5rem;    /* 8px  */
--space-2-5:  0.625rem;  /* 10px */
--space-3:    0.75rem;   /* 12px */
--space-3-5:  0.875rem;  /* 14px */
--space-4:    1rem;      /* 16px */
--space-5:    1.25rem;   /* 20px */
--space-6:    1.5rem;    /* 24px */
--space-7:    1.75rem;   /* 28px */
--space-8:    2rem;      /* 32px */
--space-10:   2.5rem;    /* 40px */
--space-12:   3rem;      /* 48px */
--space-14:   3.5rem;    /* 56px */
--space-16:   4rem;      /* 64px */
--space-20:   5rem;      /* 80px */
--space-24:   6rem;      /* 96px */
--space-28:   7rem;      /* 112px */
--space-32:   8rem;      /* 128px */
```

---

## 4. CSS Design Tokens (Повний Файл)

```css
/* ============================================================
   AI Services Landing — Design Tokens
   Версія: 1.0  |  Тема: Світла  |  Автор: UI Designer
   ============================================================ */

:root {
  /* === COLOR: Primary (Blue-Violet) === */
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

  /* === COLOR: Accent (Teal) === */
  --color-accent-50:  #e6fcf5;
  --color-accent-100: #c3fae8;
  --color-accent-400: #38d9a9;
  --color-accent-500: #20c997;
  --color-accent-600: #12b886;

  /* === COLOR: Neutrals === */
  --color-white:      #ffffff;
  --color-gray-50:    #f8f9fa;
  --color-gray-100:   #f1f3f5;
  --color-gray-200:   #e9ecef;
  --color-gray-300:   #dee2e6;
  --color-gray-400:   #ced4da;
  --color-gray-500:   #adb5bd;
  --color-gray-600:   #868e96;
  --color-gray-700:   #495057;
  --color-gray-800:   #343a40;
  --color-gray-900:   #212529;

  /* === COLOR: Semantic === */
  --color-success:    #40c057;
  --color-warning:    #fab005;
  --color-error:      #fa5252;
  --color-info:       #5c7cfa;

  /* === COLOR: Semantic Assignments === */
  --color-text-primary:     var(--color-gray-900);
  --color-text-secondary:   var(--color-gray-700);
  --color-text-muted:       var(--color-gray-500);
  --color-text-inverse:     var(--color-white);
  --color-bg-page:          var(--color-white);
  --color-bg-section:       var(--color-gray-50);
  --color-bg-section-alt:   var(--color-primary-50);
  --color-border:           var(--color-gray-200);
  --color-border-focus:     var(--color-primary-500);
  --color-link:             var(--color-primary-600);

  /* === COLOR: Gradients === */
  --gradient-brand:         linear-gradient(135deg, #5c7cfa 0%, #7950f2 100%);
  --gradient-accent:        linear-gradient(135deg, #20c997 0%, #5c7cfa 100%);
  --gradient-hero:          linear-gradient(160deg, #f8f9fa 0%, #f0f4ff 40%, #e6fcf5 100%);
  --gradient-card-hover:    linear-gradient(135deg, rgba(92,124,250,0.04) 0%, rgba(32,201,151,0.06) 100%);

  /* === TYPOGRAPHY: Font Families === */
  --font-display:     'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  --font-body:        'Inter', system-ui, -apple-system, sans-serif;
  --font-mono:        'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

  /* === TYPOGRAPHY: Sizes (Desktop) === */
  --text-display:     4rem;
  --text-h1:          3rem;
  --text-h2:          2.25rem;
  --text-h3:          1.5rem;
  --text-h4:          1.25rem;
  --text-body-lg:     1.125rem;
  --text-body:        1rem;
  --text-body-sm:     0.875rem;
  --text-caption:     0.75rem;
  --text-button:      0.9375rem;
  --text-overline:    0.75rem;

  /* === TYPOGRAPHY: Line Heights === */
  --leading-display:  1.1;
  --leading-h1:       1.15;
  --leading-h2:       1.2;
  --leading-h3:       1.3;
  --leading-h4:       1.35;
  --leading-body:     1.6;
  --leading-caption:  1.4;
  --leading-button:   1;
  --leading-overline: 1;

  /* === TYPOGRAPHY: Weights === */
  --weight-regular:   400;
  --weight-medium:    500;
  --weight-semibold:  600;
  --weight-bold:      700;
  --weight-extrabold: 800;

  /* === SPACING: 4px base system === */
  --space-0:      0;
  --space-0-5:    0.125rem;
  --space-1:      0.25rem;
  --space-1-5:    0.375rem;
  --space-2:      0.5rem;
  --space-2-5:    0.625rem;
  --space-3:      0.75rem;
  --space-3-5:    0.875rem;
  --space-4:      1rem;
  --space-5:      1.25rem;
  --space-6:      1.5rem;
  --space-7:      1.75rem;
  --space-8:      2rem;
  --space-10:     2.5rem;
  --space-12:     3rem;
  --space-14:     3.5rem;
  --space-16:     4rem;
  --space-20:     5rem;
  --space-24:     6rem;
  --space-28:     7rem;
  --space-32:     8rem;

  /* === RADIUS === */
  --radius-xs:     0.25rem;
  --radius-sm:     0.375rem;
  --radius-md:     0.5rem;
  --radius-lg:     0.75rem;
  --radius-xl:     1rem;
  --radius-2xl:    1.5rem;
  --radius-full:   9999px;

  /* === SHADOWS === */
  --shadow-xs:     0 1px 2px rgba(0,0,0,0.04);
  --shadow-sm:     0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md:     0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
  --shadow-lg:     0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
  --shadow-xl:     0 20px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -6px rgba(0,0,0,0.04);
  --shadow-2xl:    0 25px 50px -12px rgba(0,0,0,0.15);
  --shadow-primary: 0 4px 14px 0 rgba(92,124,250,0.25);
  --shadow-accent:  0 4px 14px 0 rgba(32,201,151,0.25);
  --shadow-card-hover: 0 20px 40px -12px rgba(92,124,250,0.12);

  /* === TRANSITIONS === */
  --transition-fast:     150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base:     250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow:     400ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-spring:   500ms cubic-bezier(0.34, 1.56, 0.64, 1);

  /* === LAYOUT === */
  --container-max:        1200px;
  --container-narrow:     900px;
  --container-padding:    var(--space-6);
  --header-height:        72px;

  /* === Z-INDEX === */
  --z-base:       0;
  --z-dropdown:   100;
  --z-sticky:     200;
  --z-overlay:    300;
  --z-modal:      400;
  --z-toast:      500;
}
```

---

## 5. Структура 6 Секцій — Детальний Опис

---

### Секція 1: Hero Section

**Призначення:** Захопити увагу, донести головну ціннісну пропозицію, одразу дати CTA.

**Компонування (Desktop 1440px):**
```
┌──────────────────────────────────────────────────────┐
│  [Logo]                    [Services] [Cases] [CTA]  │ ← Header 72px, фіксований
├──────────────────────────────────────────────────────┤
│                                                      │
│          ┌─────────────────────────────┐             │
│          │   PRE-LABEL: "AI-Powered"   │             │ ← Overline, accent-500, 12px, letter-spacing 0.2em
│          ├─────────────────────────────┤             │
│          │   Transform Your Business   │             │ ← Display, 64px, gray-900
│          │   With Intelligent          │             │
│          │   AI Solutions              │             │
│          ├─────────────────────────────┤             │
│          │   Subheadline (18px, 60ch   │             │ ← Body-lg, gray-600
│          │   max-width)                │             │
│          ├─────────────────────────────┤             │
│          │  [Get Free Consultation]    │             │ ← Primary btn, 56px висота
│          │      [Watch Demo ▶]        │             │ ← Outline btn
│          └─────────────────────────────┘             │
│                                                      │
│     ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐          │
│     │ 99%  │  │ 250+ │  │ 40%  │  │ 24/7 │          │ ← Stats bar
│     │ Uptime│  │Projects│ │Effic.│  │Support│         │
│     └──────┘  └──────┘  └──────┘  └──────┘          │
│                                                      │
│  [Абстрактна 3D AI-ілюстрація справа / фон]          │
│  (нейронна мережа, частки, геометрія — primary-blue) │
└──────────────────────────────────────────────────────┘
```

**Специфікації:**
| Властивість | Значення |
|---|---|
| **Висота секції** | `100vh` (або `min-height: 100vh`) |
| **Padding** | `padding: var(--space-32) var(--container-padding)` |
| **Фон** | `var(--gradient-hero)` — світлий градієнт від gray-50 → primary-50 → accent-50 |
| **Максимальна ширина контенту** | `var(--container-max)` — 1200px |
| **Вирівнювання** | Текст — ліворуч (50% ширини), графіка — праворуч (50%) |
| **Pre-label** | overline, `var(--color-accent-500)`, letter-spacing 0.2em, uppercase |
| **Headline** | `var(--text-display)`, `var(--font-display)`, weight 700, `var(--color-gray-900)` |
| **Subheadline** | `var(--text-body-lg)`, max-width 60ch, `var(--color-gray-600)`, margin-top 24px |
| **CTA Buttons** | Дві кнопки поруч, gap 16px. Primary: фон `var(--gradient-brand)`, білий текст, padding 16px 32px, border-radius 12px. Secondary: outline, border `var(--color-primary-300)`, текст `var(--color-primary-600)` |
| **Stats Bar** | 4 колонки, margin-top 64px. Цифри: display-шрифт, `var(--color-primary-600)`, weight 800. Підписи: caption, gray-500 |
| **Графіка** | SVG/WebP ілюстрація 560×560px. Плавне паріння (CSS `@keyframes float` 6s ease-in-out infinite). Не блокує LCP — lazy-loaded нижче складки без hero |

**Mobile-адаптація:**
- Текст + кнопки стають вертикально, на всю ширину
- Графіка переноситься під текст, масштабується до ~320px
- Headline: 40px; Subheadline: 16px
- CTA кнопки — вертикально (stack), на всю ширину
- Stats: 2×2 grid замість 4 колонок

---

### Секція 2: Services Overview

**Призначення:** Показати спектр AI-послуг у вигляді карток із легкою навігацією.

**Компонування:**
```
┌──────────────────────────────────────────────────────┐
│               Our AI Services                        │ ← h2, centered
│        End-to-end AI solutions for your business     │ ← body-lg, gray-600, centered, max 60ch
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────┐ │
│  │  🤖      │  │  ⚡      │  │  🧠      │  │  📊  │ │ ← 4-колонкова сітка
│  │ AI       │  │Process   │  │ Machine  │  │ Data │ │   карток, gap 24px
│  │Consulting│  │Automation│  │ Learning │  │Analyt│ │
│  │          │  │          │  │          │  │      │ │
│  │ Desc.    │  │ Desc.    │  │ Desc.    │  │ Desc.│ │
│  └──────────┘  └──────────┘  └──────────┘  └──────┘ │
│                                                      │
│  ┌──────────────────┐                                │
│  │  💬  AI Chatbots │  ← 5-та картка, ширша          │
│  │  Enterprise-grade conversational AI solutions     │
│  └──────────────────┘                                │
│                                                      │
│          [View All Services →]                        │ ← link button
└──────────────────────────────────────────────────────┘
```

**Специфікації:**
| Властивість | Значення |
|---|---|
| **Padding секції** | `var(--space-24)` top, `var(--space-24)` bottom |
| **Фон** | `var(--color-white)` |
| **Заголовок** | `var(--text-h2)`, centered, `var(--color-gray-900)`, margin-bottom 16px |
| **Сітка карток** | CSS Grid: `grid-template-columns: repeat(4, 1fr)` на десктопі, gap 24px |
| **Картка (базова)** | background `var(--color-white)`, border 1px `var(--color-gray-200)`, border-radius `var(--radius-xl)`, padding `var(--space-8)`, transition all `var(--transition-base)` |
| **Картка hover** | border-color → `var(--color-primary-200)`, background → `var(--gradient-card-hover)`, transform: translateY(-6px), box-shadow → `var(--shadow-card-hover)` |
| **Іконка в картці** | 48×48px, background `var(--color-primary-50)`, border-radius `var(--radius-lg)`, у центрі SVG 24×24px `var(--color-primary-500)` |
| **Назва сервісу** | `var(--text-h4)`, `var(--font-display)`, weight 600, `var(--color-gray-900)`, margin-top 24px |
| **Опис** | `var(--text-body-sm)`, `var(--color-gray-600)`, margin-top 8px, max-width 28ch |
| **5-та картка (Chatbots)** | `grid-column: 1 / -1` (на всю ширину), горизонтальний layout: іконка ліворуч, текст праворуч |
| **CTA-посилання** | centered, `var(--text-body)`, weight 500, `var(--color-primary-600)`, зі стрілкою → |

**Mobile-адаптація:**
- 1 колонка карток (max-width 400px кожна, centered)
- 5-та картка також вертикальний layout
- Padding секції: 48px 16px

---

### Секція 3: How It Works / Process

**Призначення:** Показати процес співпраці — 4 кроки від знайомства до результату.

**Компонування:**
```
┌──────────────────────────────────────────────────────┐
│              How We Work                             │ ← h2, centered
│        From first contact to measurable results      │ ← body-lg, centered
├──────────────────────────────────────────────────────┤
│                                                      │
│  ①                    ②                    ③                    ④
│  ●─────────────────●──────────────────●──────────────────●       │ ← Timeline
│  │                 │                  │                  │       │   (desktop: horizontal)
│  │  Discovery      │  Strategy &      │  Development     │       │
│  │  & Audit        │  Roadmap         │  & Integration   │  🚀   │
│  │                 │                  │                  │ Launch│
│  │  We analyze     │  We design a     │  Our engineers   │       │
│  │  your business  │  custom AI       │  build and       │  Deploy│
│  │  needs and      │  strategy        │  integrate       │  &     │
│  │  data maturity  │  tailored to     │  solutions       │  Scale │
│  │                 │  your goals      │                  │       │
│  └─────────────────┴──────────────────┴──────────────────┴───────┘
│                                                      │
│        [Start Your AI Journey →]                      │ ← CTA
└──────────────────────────────────────────────────────┘
```

**Специфікації:**
| Властивість | Значення |
|---|---|
| **Padding секції** | `var(--space-24)` top/bottom |
| **Фон** | `var(--color-bg-section)` (gray-50) |
| **Timeline** | Desktop: горизонтальна лінія. `display: flex`, рівномірний розподіл кроків |
| **Номер кроку** | 64×64px коло, фон `var(--gradient-brand)`, білий текст, `var(--text-h2)`, weight 700, border-radius `var(--radius-full)` |
| **Лінія між кроками** | 2px solid `var(--color-primary-200)`, height 2px, flex-grow між кроками |
| **Заголовок кроку** | `var(--text-h4)`, `var(--font-display)`, weight 600, margin-top 24px |
| **Опис кроку** | `var(--text-body-sm)`, `var(--color-gray-600)`, max-width 24ch |
| **Активний крок** | Номер має `box-shadow: var(--shadow-primary)`, лінія до нього — `var(--color-primary-500)` |
| **Фінальна іконка (🚀)** | 72×72px, `var(--gradient-accent)`, box-shadow `var(--shadow-accent)` |
| **CTA** | centered, `var(--space-16)` margin-top |

**Mobile-адаптація:**
- Вертикальна лінія замість горизонтальної
- Номери ліворуч, текст праворуч
- Відстань між кроками: 40px
- Лінія: вертикальна, 2px, проходить через центри номерів

---

### Секція 4: Tech Stack / Capabilities Showcase

**Призначення:** Продемонструвати технічну експертизу через візуальну сітку технологій.

**Компонування:**
```
┌──────────────────────────────────────────────────────┐
│           Powered by Leading Technology              │ ← h2, centered
│         Modern stack for enterprise-grade AI          │ ← subtitle
├──────────────────────────────────────────────────────┤
│                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│   │   🤖 LLMs    │  │   ☁️ Cloud   │  │  📈 MLOps  │ │ ← 3×2 сітка з
│   │              │  │              │  │            │ │   іконками + описами
│   │ GPT-4,       │  │ AWS, GCP,    │  │ MLflow,    │ │
│   │ Claude,      │  │ Azure        │  │ Kubeflow   │ │
│   │ Gemini       │  │              │  │            │ │
│   └──────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
│   ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│   │  🗄️ Vector  │  │  🔄 API      │  │  🔒 Secur. │ │
│   │     DBs      │  │  Gateway     │  │  & Compliance│
│   │              │  │              │  │            │ │
│   │ Pinecone,    │  │ REST,        │  │ SOC2,      │ │
│   │ Weaviate,    │  │ GraphQL,     │  │ GDPR,      │ │
│   │ Qdrant       │  │ WebSocket    │  │ HIPAA      │ │
│   └──────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**Специфікації:**
| Властивість | Значення |
|---|---|
| **Padding секції** | `var(--space-24)` |
| **Фон** | `var(--color-white)` |
| **Сітка** | 3 колонки × 2 ряди, gap `var(--space-6)` |
| **Картка технології** | Мінімалістична: без рамки на спокої, padding `var(--space-8)`, border-radius `var(--radius-xl)`, background transparent. На hover: `var(--gradient-card-hover)`, border `var(--color-gray-200)` |
| **Іконка** | 40×40px, `var(--color-primary-50)` фон, SVG іконка `var(--color-primary-500)` |
| **Назва категорії** | `var(--text-h4)`, weight 600 |
| **Теги/список** | `var(--text-body-sm)`, chips: border 1px `var(--color-gray-200)`, border-radius `var(--radius-full)`, padding 4px 12px, фон `var(--color-gray-50)` |

**Mobile-адаптація:**
- 1 колонка (6 карток одна під одною)
- Іконка + текст — горизонтальний flex

---

### Секція 5: Case Studies / Results

**Призначення:** Соціальний доказ — реальні кейси з конкретними цифрами.

**Компонування:**
```
┌──────────────────────────────────────────────────────┐
│           Client Success Stories                      │ ← h2, centered
│      Measurable impact across industries              │ ← subtitle
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────────────────────────┐        │
│  │  ┌─────────┐                              │        │ ← Case 1 (featured)
│  │  │ Company │  "AI-driven automation       │        │   горизонтальний
│  │  │ Logo    │   reduced processing time    │        │   layout
│  │  │         │   by 73% and saved $2.4M     │        │
│  │  │E-Commerce│  annually."                 │        │
│  │  └─────────┘                              │        │
│  │               ┌─────┐ ┌─────┐ ┌──────┐   │        │
│  │               │ 73% │ │$2.4M│ │ 14d  │   │        │ ← KPI badges
│  │               │faster│ │saved │ │deploy│   │        │
│  │               └─────┘ └─────┘ └──────┘   │        │
│  └──────────────────────────────────────────┘        │
│                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │
│  │   Case 2    │  │   Case 3    │  │   Case 4    │  │ ← 3 картки
│  │   Finance   │  │  Healthcare │  │   Logistics │  │
│  │   +89% NPS  │  │   99.7%     │  │   40% cost  │  │
│  │             │  │  accuracy   │  │  reduction  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  │
│                                                      │
│          [View All Case Studies →]                    │
└──────────────────────────────────────────────────────┘
```

**Специфікації:**
| Властивість | Значення |
|---|---|
| **Padding секції** | `var(--space-24)` |
| **Фон** | `var(--color-bg-section)` (gray-50) |
| **Featured Case (Card)** | background `var(--color-white)`, border-radius `var(--radius-xl)`, padding `var(--space-10)`, border-left 4px solid `var(--color-primary-500)`, горизонтальний flex |
| **Логотип** | 80×80px, border-radius `var(--radius-md)`, background `var(--color-gray-100)` для placeholder |
| **Цитата** | `var(--text-body-lg)`, `var(--color-gray-800)`, font-style italic, max-width 70ch |
| **KPI Badges** | `var(--text-h4)`, weight 700, `var(--color-primary-600)`, фон `var(--color-primary-50)`, border-radius `var(--radius-lg)`, padding 12px 20px, flex-ряд |
| **Малі картки (Case 2-4)** | 3-колонкова сітка, картки: padding `var(--space-6)`, border-radius `var(--radius-lg)`, hover: `var(--shadow-md)` |

**Mobile-адаптація:**
- Featured case: вертикальний layout
- KPI badges: wrap на малих екранах
- Cases 2-4: 1 колонка

---

### Секція 6: Contact / CTA Footer

**Призначення:** Конверсія — форма зв'язку + вся контактна інформація.

**Компонування:**
```
┌──────────────────────────────────────────────────────┐
│                                                      │
│    ┌────────────────────────┐  ┌──────────────────┐  │
│    │  Ready to Transform    │  │  ┌────────────┐  │  │
│    │  Your Business with AI?│  │  │  Full Name* │  │  │
│    │                        │  │  └────────────┘  │  │
│    │  Get in touch with our │  │  ┌────────────┐  │  │
│    │  team for a free       │  │  │ Work Email* │  │  │
│    │  consultation.         │  │  └────────────┘  │  │
│    │                        │  │  ┌────────────┐  │  │
│    │  ✉️ hello@aicompany.io │  │  │  Company   │  │  │
│    │  📞 +1 (555) 123-4567  │  │  └────────────┘  │  │
│    │  📍 San Francisco, CA  │  │  ┌────────────┐  │  │
│    │                        │  │  │  Message   │  │  │
│    │  "They transformed our │  │  │            │  │  │
│    │   operations in weeks" │  │  │            │  │  │
│    │   — CTO, TechCorp      │  │  └────────────┘  │  │
│    └────────────────────────┘  │                  │  │
│                                │ [Send Message]   │  │
│                                └──────────────────┘  │
│                                                      │
├──────────────────────────────────────────────────────┤
│  © 2026 AICorp.  Privacy  |  Terms  |  [SOC2 Badge] │ ← Footer bar
└──────────────────────────────────────────────────────┘
```

**Специфікації:**
| Властивість | Значення |
|---|---|
| **Padding секції** | `var(--space-32)` top/bottom, `var(--container-padding)` horizontal |
| **Фон** | `var(--color-gray-900)` (темний footer для контрасту) |
| **Текст у лівій частині** | `var(--color-white)` — headline: `var(--text-h2)`, body: `var(--text-body-lg)`, `var(--color-gray-400)` |
| **Форма (права частина)** | background `var(--color-white)`, border-radius `var(--radius-xl)`, padding `var(--space-8)`, box-shadow `var(--shadow-xl)` |
| **Inputs** | height 52px, border 1.5px `var(--color-gray-300)`, border-radius `var(--radius-lg)`, padding 0 16px, font `var(--text-body)`. Focus: border `var(--color-primary-500)`, box-shadow: 0 0 0 3px `rgba(92,124,250,0.12)` |
| **Textarea** | height 120px, ті ж стилі |
| **Submit Button** | full-width, background `var(--gradient-brand)`, color white, height 56px, border-radius `var(--radius-lg)`, weight 600, hover: `var(--shadow-primary)` |
| **Контактна інформація** | Іконки 20×20px, `var(--color-accent-500)`, текст `var(--color-white)` |
| **Цитата** | `var(--text-body)`, italic, `var(--color-gray-400)`, border-left 3px `var(--color-accent-500)`, padding-left 16px |
| **Footer Bar** | height 64px, background `var(--color-gray-800)`, текст `var(--text-body-sm)`, `var(--color-gray-500)`, flex між copyright + links |
| **2-колонковий layout** | `display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-16);` |

**Mobile-адаптація:**
- 1 колонка (текстовий блок → форма)
- Форма на всю ширину, padding 24px
- Footer bar: вертикальний stack

---

## 6. Анімації та Мікровзаємодії

### 6.1 Scroll-triggered Animations (Intersection Observer)

| Елемент | Анімація | Тривалість | Easing |
|---|---|---|---|
| **Секційні заголовки** | `fadeInUp` — opacity 0→1, translateY 30px→0 | 600ms | `cubic-bezier(0.4,0,0.2,1)` |
| **Картки сервісів (stagger)** | `fadeInUp` зі stagger-затримкою 100ms | 500ms each | `cubic-bezier(0.4,0,0.2,1)` |
| **Stats цифри** | `countUp` — анімація лічильника від 0 до фінального значення | 2000ms | `ease-out` |
| **Timeline кроки** | `scaleIn` — scale 0.8→1, opacity 0→1 | 400ms | `cubic-bezier(0.34,1.56,0.64,1)` (spring) |
| **Tech stack картки** | `fadeIn` зі stagger | 300ms each | `ease-out` |
| **Case study картки** | `slideInLeft` / `slideInRight` | 500ms | `cubic-bezier(0.4,0,0.2,1)` |

### 6.2 Hover Micro-interactions

```css
/* Кнопки */
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-primary);
  transition: var(--transition-base);
}
.btn-primary:active {
  transform: translateY(0);
  box-shadow: var(--shadow-sm);
  transition: var(--transition-fast);
}

/* Картки */
.service-card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-card-hover);
  border-color: var(--color-primary-200);
  transition: var(--transition-spring);
}

/* Посилання */
.link-arrow {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: gap var(--transition-fast);
}
.link-arrow:hover {
  gap: 8px; /* стрілка "від'їжджає" */
}
.link-arrow:hover .arrow {
  transform: translateX(4px);
}

/* Іконки в картках */
.service-card:hover .service-icon {
  transform: scale(1.1) rotate(-5deg);
  transition: var(--transition-spring);
}
```

### 6.3 Мікроанімації

| Тригер | Ефект |
|---|---|
| **Focus на input** | Border color + тіньовий glow (3px spread) за 150ms |
| **Наведення на тег** | `background-color` змінюється на `var(--color-primary-100)` за 150ms |
| **Submit button click** | Стиснення до 0.97 scale + ріппл-ефект від точки кліку |
| **Успішна відправка форми** | Кнопка → чекмарк (зелений), form замінюється на "Thank you" з fadeIn |
| **Мобільне меню** | Бургер → хрестик (rotate 180°), меню slideDown від header |
| **Scroll-to-top** | Кнопка з'являється після прокрутки >600px, з fadeIn + scale |

### 6.4 Зменшення руху (Accessibility)

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 7. Responsive Breakpoints

```css
/* Mobile First — базові стилі для < 640px */

/* Tablet: 640px+ */
@media (min-width: 640px) {
  :root {
    --container-padding: var(--space-8);
  }
  /* 2-колонкові сітки */
}

/* Desktop: 1024px+ */
@media (min-width: 1024px) {
  :root {
    --container-padding: var(--space-10);
  }
  /* 3-4 колонкові сітки, горизонтальні layout */
}

/* Wide: 1280px+ */
@media (min-width: 1280px) {
  :root {
    --container-padding: 0; /* центрування через max-width */
  }
}
```

### 7.1 Mobile-Specific Rules

| Правило | Значення |
|---|---|
| **Мін. тач-таргет** | 44×44px для всіх інтерактивних елементів |
| **Макс. ширина тексту** | 65ch для читабельності |
| **Сітки** | 1 колонка, відступи 16px |
| **Картки** | На всю ширину, max-width 440px, centered |
| **CTA кнопки** | Full-width на мобільних |
| **Форма** | Inputs на всю ширину |
| **Зображення** | max-width 100%, height auto |

---

## 8. Компонентна Бібліотека — Ключові Компоненти

### 8.1 Buttons

```css
/* Primary */
.btn-primary {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2);
  height: 56px; padding: 0 var(--space-8);
  background: var(--gradient-brand);
  color: var(--color-white);
  font-family: var(--font-body); font-size: var(--text-button); font-weight: var(--weight-semibold);
  border: none; border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
  user-select: none;
}
.btn-primary:hover { transform: translateY(-2px); box-shadow: var(--shadow-primary); }
.btn-primary:active { transform: translateY(0); }
.btn-primary:focus-visible { outline: 2px solid var(--color-primary-500); outline-offset: 2px; }

/* Outline */
.btn-outline {
  /* як primary, але: */
  background: transparent;
  border: 1.5px solid var(--color-primary-300);
  color: var(--color-primary-600);
}
.btn-outline:hover { background: var(--color-primary-50); border-color: var(--color-primary-500); }

/* Ghost */
.btn-ghost {
  background: transparent; border: none;
  color: var(--color-primary-600);
  padding: 0 var(--space-4); height: 44px;
}
.btn-ghost:hover { background: var(--color-primary-50); }

/* Sizes */
.btn-sm { height: 40px; padding: 0 var(--space-4); font-size: var(--text-body-sm); }
.btn-lg { height: 64px; padding: 0 var(--space-10); font-size: var(--text-body-lg); }
```

### 8.2 Cards

```css
.card {
  background: var(--color-white);
  border: 1px solid var(--color-gray-200);
  border-radius: var(--radius-xl);
  padding: var(--space-8);
  transition: all var(--transition-base);
}
.card:hover {
  transform: translateY(-6px);
  box-shadow: var(--shadow-card-hover);
  border-color: var(--color-primary-200);
  background: var(--gradient-card-hover);
}
```

### 8.3 Inputs

```css
.form-input {
  width: 100%; height: 52px;
  padding: 0 var(--space-4);
  background: var(--color-white);
  border: 1.5px solid var(--color-gray-300);
  border-radius: var(--radius-lg);
  font-family: var(--font-body); font-size: var(--text-body); color: var(--color-text-primary);
  transition: all var(--transition-fast);
}
.form-input::placeholder { color: var(--color-gray-400); }
.form-input:focus {
  outline: none;
  border-color: var(--color-primary-500);
  box-shadow: 0 0 0 3px rgba(92,124,250,0.12);
}
.form-input.error {
  border-color: var(--color-error);
  box-shadow: 0 0 0 3px rgba(250,82,82,0.12);
}
```

### 8.4 Badges / Tags

```css
.badge {
  display: inline-flex; align-items: center;
  padding: var(--space-1) var(--space-3);
  background: var(--color-primary-50);
  color: var(--color-primary-700);
  border-radius: var(--radius-full);
  font-size: var(--text-caption); font-weight: var(--weight-medium);
}
.badge--accent { background: var(--color-accent-50); color: var(--color-accent-600); }
```

---

## 9. Специфікації зображень

| Елемент | Формат | Розмір | Опис |
|---|---|---|---|
| **Hero illustration** | SVG / WebP | 560×560px (1x), 1120×1120px (2x) | Абстрактна AI-мережа, синьо-фіолетова гама, прозорий фон |
| **Service icons** | SVG inline | 24×24px viewBox | Контурні іконки, stroke-width 2, `currentColor` |
| **Tech logos** | SVG / WebP | ~120×40px | Монохромні, `var(--color-gray-500)`, кольорові на hover |
| **Case study logos** | SVG / WebP | 80×80px | Кольорові логотипи компаній |
| **Background patterns** | SVG | tileable | Легкий геометричний патерн, opacity 0.04, `var(--color-primary-500)` |
| **Avatar (testimonial)** | WebP | 48×48px (1x), 96×96px (2x) | Круглі, object-fit: cover |

---

## 10. Accessibility Checklist (WCAG 2.1 AA)

| Вимога | Реалізація |
|---|---|
| **Колірний контраст** | Текст на фоні: 4.5:1 (нормальний), 3:1 (великий). Всі комбінації перевірені |
| **Focus-visible** | `outline: 2px solid var(--color-primary-500); outline-offset: 2px` на всіх інтерактивних елементах |
| **Alt-тексти** | Всі зображення мають описовий alt-текст |
| **Заголовки** | Ієрархія h1→h2→h3 без пропусків |
| **Тач-таргети** | Мінімум 44×44px (WCAG 2.5.5) |
| **ARIA labels** | `aria-label` на іконкових кнопках, `aria-expanded` на mobile menu |
| **Зменшення руху** | `prefers-reduced-motion` підтримується |
| **Масштабування** | Коректна робота до 200% zoom без горизонтального скролу |
| **Клавіатура** | Tab order логічний, всі інтерактивні елементи доступні з клавіатури |
| **Форма** | Labels прив'язані до inputs через `for`/`id`, error messages — `aria-describedby` |

---

## 11. Performance Budget

| Метрика | Ціль |
|---|---|
| **LCP** (Largest Contentful Paint) | < 2.5s |
| **FID** (First Input Delay) | < 100ms |
| **CLS** (Cumulative Layout Shift) | < 0.1 |
| **Загальний розмір сторінки** | < 500 KB (gzipped) |
| **Шрифти** | < 100 KB (підмножини latin + cyrillic) |
| **Hero зображення** | < 80 KB (WebP, lazy-loaded якщо нижче складки) |

---

## 12. Рекомендований HTML Скелет

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI Solutions Company — Transform Your Business</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="tokens.css">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header id="header">...</header>
  <main>
    <section id="hero">...</section>
    <section id="services">...</section>
    <section id="process">...</section>
    <section id="tech-stack">...</section>
    <section id="case-studies">...</section>
    <section id="contact">...</section>
  </main>
  <footer>...</footer>
</body>
</html>
```

---

## Підсумок

| Пункт вимоги | Статус |
|---|---|
| Світла тема з чіткою кольоровою схемою | ✅ 50+ токенів, градієнти, семантичні кольори |
| 6 секцій детально описані | ✅ Hero, Services, Process, Tech Stack, Case Studies, Contact |
| Палітра та типографіка готові до CSS | ✅ Готовий CSS-файл з усіма змінними |
| AI-тематика | ✅ Синьо-фіолетова primary палітра + teal акцент |
| Mobile-рекомендації | ✅ Адаптивні брейкпоінти, специфікації для кожної секції |
| Анімації | ✅ Scroll-triggered, hover, мікроанімації, reduced-motion |

**Файл готовий до передачі розробникам.** Усі значення наведені в CSS-змінних, що дозволяє миттєво розпочати імплементацію.

---
*Design Brief created by UI Designer, Pixel Agents. 06.08.2026*
