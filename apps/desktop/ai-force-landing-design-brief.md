# AI-Force — Дизайн-бриф односторінкового лендінгу

**UI Designer**: UI Designer | **Дата**: 06.08.2026 | **Версія**: v1.0
**Тема**: Світла | **Стиль**: Сучасний мінімалізм | **Призначення**: AI-консалтинг та послуги

---

## 1. Кольорова палітра

### 1.1 Основні кольори (Primary)

| Токен | Hex | Призначення |
|---|---|---|
| `--color-primary-50`  | `#EEF2FF` | Фон секцій, легке підсвічування |
| `--color-primary-100` | `#E0E7FF` | Активний стан карток, теги |
| `--color-primary-200` | `#C7D2FE` | Межі при фокусі, border |
| `--color-primary-300` | `#A5B4FC` | Декоративні лінії, іконки |
| `--color-primary-400` | `#818CF8` | Hover-стани текстових посилань |
| `--color-primary-500` | `#6366F1` | **Основний акцентний** — кнопки, заголовки |
| `--color-primary-600` | `#4F46E5` | Hover на кнопках, активні стани |
| `--color-primary-700` | `#4338CA` | Pressed стан, темні акценти |
| `--color-primary-800` | `#3730A3` | Текст на світлому primary-фоні |
| `--color-primary-900` | `#312E81` | Глибокий акцент, footer-фон |
| `--color-primary-950` | `#1E1B4B` | Найтемніший акцент |

### 1.2 Акцентний градієнт (Hero / CTA)

```css
--gradient-hero: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%);
--gradient-cta:   linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
--gradient-card:  linear-gradient(180deg, rgba(99, 102, 241, 0.04) 0%, rgba(139, 92, 246, 0.02) 100%);
--gradient-glow:  radial-gradient(ellipse at 50% 0%, rgba(99, 102, 241, 0.15) 0%, transparent 60%);
```

### 1.3 Нейтральна палітра (Neutral)

| Токен | Hex | Призначення |
|---|---|---|
| `--color-neutral-50`  | `#FAFAFA` | Загальний фон сторінки |
| `--color-neutral-100` | `#F5F5F5` | Фон альтернативних секцій |
| `--color-neutral-200` | `#E5E5E5` | Межі карток, розділювачі |
| `--color-neutral-300` | `#D4D4D4` | Placeholder-текст на світлому |
| `--color-neutral-400` | `#A3A3A3` | Декоративний текст, disabled |
| `--color-neutral-500` | `#737373` | Другорядний текст |
| `--color-neutral-600` | `#525252` | Body-текст (середній контраст) |
| `--color-neutral-700` | `#404040` | Основний body-текст |
| `--color-neutral-800` | `#262626` | Підзаголовки |
| `--color-neutral-900` | `#171717` | Заголовки h1-h3 |
| `--color-neutral-950` | `#0A0A0A` | Найтемніший текст (hero) |

### 1.4 Семантичні кольори

| Токен | Hex | Призначення |
|---|---|---|
| `--color-success` | `#10B981` | Успіх, підтвердження |
| `--color-success-bg` | `#ECFDF5` | Фон для success-станів |
| `--color-warning` | `#F59E0B` | Попередження |
| `--color-warning-bg` | `#FFFBEB` | Фон для warning-станів |
| `--color-error` | `#EF4444` | Помилки |
| `--color-error-bg` | `#FEF2F2` | Фон для error-станів |
| `--color-info` | `#3B82F6` | Інформаційні повідомлення |
| `--color-info-bg` | `#EFF6FF` | Фон для info-станів |

### 1.5 Спеціальні кольори AI-тематики

| Токен | Hex | Призначення |
|---|---|---|
| `--color-ai-glow` | `#A78BFA` | Ефекти підсвічування, glow |
| `--color-ai-circuit` | `#6D28D9` | Декоративні схеми, іконки AI |
| `--color-ai-data` | `#06B6D4` | Акцент для даних, статистики |
| `--color-ai-bot` | `#8B5CF6` | Чат-бот тематика |

### 1.6 Контрастність (WCAG AA)

| Комбінація | Ratio | Статус |
|---|---|---|
| `neutral-900` на `neutral-50` | 16.1:1 | ✅ AAA |
| `neutral-700` на `neutral-50` | 9.4:1 | ✅ AAA |
| `neutral-600` на `neutral-50` | 6.4:1 | ✅ AA |
| `primary-500` на `#FFFFFF` | 4.5:1 | ✅ AA |
| `primary-600` на `#FFFFFF` | 5.9:1 | ✅ AA |
| `primary-800` на `primary-100` | 7.2:1 | ✅ AAA |

---

## 2. Типографіка

### 2.1 Шрифти

```css
/* Основний sans-serif — чистий, сучасний, геометричний */
--font-primary: 'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;

/* Для відображення коду / технічних деталей */
--font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;

/* Альтернативний для великих hero-заголовків (опціонально) */
--font-display: 'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;
```

**Рекомендація**: Inter — оптимальний вибір для AI-тематики завдяки чистій геометрії та відмінній читабельності. JetBrains Mono для технічних блоків підкреслює технологічність.

### 2.2 Розміри шрифтів

```css
/* Desktop (>1024px) */
--text-hero:    clamp(2.75rem, 5vw, 4.5rem);     /* 44px → 72px   — h1 Hero */
--text-h1:      clamp(2.25rem, 4vw, 3.5rem);      /* 36px → 56px   — h1 секцій */
--text-h2:      clamp(1.75rem, 3vw, 2.5rem);      /* 28px → 40px   — h2 */
--text-h3:      clamp(1.375rem, 2vw, 1.75rem);    /* 22px → 28px   — h3 */
--text-h4:      clamp(1.125rem, 1.5vw, 1.375rem); /* 18px → 22px   — h4 */
--text-body-lg: 1.125rem;                          /* 18px — великий body */
--text-body:    1rem;                              /* 16px — основний текст */
--text-body-sm: 0.875rem;                          /* 14px — малий текст */
--text-caption: 0.75rem;                           /* 12px — підписи, мета */
```

### 2.3 Вага шрифтів

| Токен | Значення | Застосування |
|---|---|---|
| `--font-light` | `300` | Великі hero-заголовки (стилістично) |
| `--font-normal` | `400` | Body-текст |
| `--font-medium` | `500` | Кнопки, підписи, nav |
| `--font-semibold` | `600` | h3, h4, акцентований текст |
| `--font-bold` | `700` | h1, h2, CTA |
| `--font-extrabold` | `800` | Hero h1 (опціонально) |

### 2.4 Висота рядків (Line-height)

```css
--leading-tight:   1.1;   /* Hero h1 */
--leading-snug:    1.25;  /* h1, h2 */
--leading-normal:  1.5;   /* h3, h4 */
--leading-relaxed: 1.625; /* body-lg */
--leading-loose:   1.75;  /* body, body-sm */
```

### 2.5 Міжлітерний інтервал (Letter-spacing)

```css
--tracking-tighter: -0.03em; /* Hero — стиснуто для сили */
--tracking-tight:   -0.02em; /* h1, h2 */
--tracking-normal:   0;      /* body */
--tracking-wide:     0.02em; /* caption, кнопки */
--tracking-wider:    0.05em; /* uppercase labels */
```

---

## 3. Архітектура 6 секцій

### Загальна структура сторінки

```
┌─────────────────────────────────────────────────────┐
│  NAVIGATION  (fixed, 72px)                          │
├─────────────────────────────────────────────────────┤
│  SECTION 1 — HERO                          (100vh)  │
├─────────────────────────────────────────────────────┤
│  SECTION 2 — ПОСЛУГИ                       (~720px) │
├─────────────────────────────────────────────────────┤
│  SECTION 3 — ПРОЦЕС РОБОТИ                 (~680px) │
├─────────────────────────────────────────────────────┤
│  SECTION 4 — КЕЙСИ / ТЕХНОЛОГІЇ            (~760px) │
├─────────────────────────────────────────────────────┤
│  SECTION 5 — ЧОМУ МИ                       (~620px) │
├─────────────────────────────────────────────────────┤
│  SECTION 6 — CTA + КОНТАКТИ                (~580px) │
├─────────────────────────────────────────────────────┤
│  FOOTER                                    (~200px) │
└─────────────────────────────────────────────────────┘
```

---

### SEC 1: HERO

**Призначення**: Захопити увагу, пояснити цінність, дати одну чітку дію.

**Розміри**:
- Висота: `min-height: 100vh` (мінус 72px nav)
- Max-width контенту: `1240px`
- Горизонтальний padding: `--space-8` (32px) → tablet: `--space-16` (64px)

**Структура (дві колонки)**:
```
Ліва колонка (55%)                       Права колонка (45%)
┌─────────────────────┐                  ┌───────────────────┐
│ TAG: "AI-Force"     │                  │                   │
│ (primary-100 bg,    │                  │   3D Абстракція   │
│  primary-700 text)  │                  │   нейромережі     │
│                     │                  │   (SVG / Canvas   │
│ H1: "Трансформуйте  │                  │    анімація)      │
│ бізнес за допомогою │                  │                   │
│ штучного інтелекту" │                  │   Glow-ефект:     │
│ (neutral-900,       │                  │   radial-gradient │
│  700 weight)        │                  │   ellipse 400px   │
│                     │                  │   rgba(99,102,    │
│ P: 2 речення опису  │                  │   241, 0.12)      │
│ (neutral-700, 18px) │                  │                   │
│                     │                  │   Декоративні     │
│ Primary CTA btn     │                  │   точки/лінії,    │
│ + Secondary link    │                  │   що рухаються    │
│                     │                  │   повільно        │
│ Статистика: 3 цифри │                  │                   │
│ (150+, 98%, 24/7)   │                  │                   │
└─────────────────────┘                  └───────────────────┘
        │                                       │
        └───────────────  gap: 64px ────────────┘
```

**Компоненти**:
1. **Tag/badge** — `padding: 6px 16px; border-radius: 100px` — primary-100 фон
2. **h1** — hero-розмір, `--font-bold`, `--tracking-tighter`
3. **Subhead p** — 18px, `--leading-relaxed`, max-width: 520px
4. **CTA Button** (primary) — `padding: 16px 36px`, `border-radius: 12px`, градієнтний фон, `font-weight: 600`, box-shadow: `0 4px 24px rgba(99,102,241,0.35)`
5. **Secondary link** — "Дізнатись більше →", primary-500, underline-animation на hover
6. **Stats row** — 3 колонки: `150+ проектів` / `98% задоволених` / `24/7 підтримка`, цифри → neutral-900 32px bold, підписи → neutral-500 14px
7. **Visual** — абстрактна нейромережа, анімований SVG/Canvas, з glow-ефектом

**Відступи**:
- Hero padding-top: `120px` (враховуючи fixed nav)
- Hero padding-bottom: `80px`
- Між tag та h1: `24px`
- Між h1 та p: `20px`
- Між p та CTA: `36px`
- Між CTA та статистикою: `64px`

**Mobile** (< 768px):
- Одна колонка
- Текст центрований
- Візуал зменшений, розміщений над текстом (40vh)
- Hero padding-top: `96px`
- Статистика в один ряд (3 маленькі колонки) або вертикально

---

### SEC 2: ПОСЛУГИ

**Призначення**: Показати спектр AI-послуг у візуально привабливому форматі сітки.

**Розміри**:
- Padding: `100px 0`
- Max-width: `1240px`
- Фон: `--color-neutral-50`

**Структура**:
```
┌─────────────────────────────────────────────────────────────┐
│  Section label: "Що ми пропонуємо" (text-transform: uppercase,
│    letter-spacing: 0.05em, color: primary-500, 14px, semibold)
│
│  H2: "Повний спектр AI-рішень для вашого бізнесу"
│  (max-width: 700px, text-align: center, margin: 0 auto)
│  margin-bottom: 60px
│
│  GRID: 3 колонки × 2 ряди = 6 карток
│  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  │  Іконка  │  │  Іконка  │  │  Іконка  │
│  │  64×64   │  │  64×64   │  │  64×64   │
│  │          │  │          │  │          │
│  │  H3      │  │  H3      │  │  H3      │
│  │  Опис    │  │  Опис    │  │  Опис    │
│  │  "Деталь-│  │  "Деталь-│  │  "Деталь-│
│  │   ніше →"│  │   ніше →"│  │   ніше →"│
│  └──────────┘  └──────────┘  └──────────┘
│  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  │   ...    │  │   ...    │  │   ...    │
│  └──────────┘  └──────────┘  └──────────┘
│
│  gap: 24px між картками
│  Кожна картка: padding: 32px, border-radius: 16px,
│    border: 1px solid neutral-200, background: white
└─────────────────────────────────────────────────────────────┘
```

**6 Карток послуг**:
1. **AI-консалтинг** — іконка: мозок/лампочка
2. **Автоматизація процесів** — іконка: шестерні/workflow
3. **Машинне навчання** — іконка: нейрони/граф
4. **Чат-боти та AI-асистенти** — іконка: діалог/bot
5. **Аналітика даних** — іконка: графік/dashboard
6. **Computer Vision** — іконка: око/камера

**Hover-стан картки**:
- `transform: translateY(-4px)`
- `box-shadow: 0 12px 40px rgba(0,0,0,0.08)`
- `border-color: primary-300`
- Іконка: легке збільшення (`scale: 1.05`)
- Тривалість: 300ms ease-out

**Mobile** (< 768px): 1 колонка
**Tablet** (768–1024px): 2 колонки

---

### SEC 3: ПРОЦЕС РОБОТИ

**Призначення**: Показати прозорість та професіоналізм через зрозумілий процес.

**Розміри**:
- Padding: `100px 0`
- Max-width: `1240px`
- Фон: `white` (або `--color-neutral-50` з легким градієнтом)

**Структура (горизонтальний timeline)**:
```
┌─────────────────────────────────────────────────────────────┐
│  Section label: "Як ми працюємо" (як у sec2)
│  H2: "Від ідеї до результату за 4 кроки"
│  margin-bottom: 64px
│
│  ┌─────┐     ┌─────┐     ┌─────┐     ┌─────┐
│  │ 01  │────►│ 02  │────►│ 03  │────►│ 04  │
│  │     │     │     │     │     │     │     │
│  │H4   │     │H4   │     │H4   │     │H4   │
│  │Опис │     │Опис │     │Опис │     │Опис │
│  └─────┘     └─────┘     └─────┘     └─────┘
│
│  Крок 1: Аудит          Крок 3: Розробка
│  Крок 2: Стратегія      Крок 4: Запуск + супровід
│
│  З'єднувальні лінії (neutral-300, 2px)
│  з анімованим "потоком" точок (primary-400)
└─────────────────────────────────────────────────────────────┘
```

**Компонент кроку**:
- Номер кроку: 48px × 48px круг, primary-gradient фон, білий текст, 20px bold
- h4: `18px`, `--font-semibold`, `neutral-800`
- Опис: `14px`, `neutral-600`, `max-width: 240px`
- Відстань між кроками: `32px` + лінія
- Загальна ширина timeline: обмежена `900px`, центрована

**Анімація**: Точки "течуть" по лініях при скролі до секції (Intersection Observer).

**Mobile** (< 768px): Вертикальний timeline (лінія зліва, кроки справа), або вертикальний стек із з'єднувальними лініями.

---

### SEC 4: КЕЙСИ / ТЕХНОЛОГІЇ

**Призначення**: Продемонструвати експертизу через реальний досвід або технологічний стек.

**Розміри**:
- Padding: `100px 0`
- Max-width: `1240px`
- Фон: `--color-neutral-100`

**Структура (дві підсекції)**:

#### 4A. Технологічний стек (Masonry/Grid)
```
┌─────────────────────────────────────────────────────────────┐
│  Section label: "Технології"
│  H2: "Працюємо з найкращими AI-інструментами"
│  margin-bottom: 48px
│
│  Grid: 6 колонок × 2 ряди логотипів (12 технологій)
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│  │TF  │ │PyT │ │HG  │ │ONNX│ │Lang│ │Open│
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘
│  ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
│  │AWS │ │GCP │ │K8s │ │TF  │ │Dock│ │Fast│
│  └────┘ └────┘ └────┘ └────┘ └────┘ └────┘
│
│  Кожен логотип: 80×80px, grayscale → color на hover
│  margin-bottom: 32px
│
│  ─────────────────── Розділювач (hairline) ──────────────────
│  margin: 60px 0
```

#### 4B. Кейси (3 картки)
```
│  Section label: "Кейси"
│  H2: "Реальні результати для наших клієнтів"
│  margin-bottom: 48px
│
│  Grid: 3 колонки
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  │ [Industry    │ │ [Industry    │ │ [Industry    │
│  │  Icon]       │ │  Icon]       │ │  Icon]       │
│  │              │ │              │ │              │
│  │ "Збільшили   │ │ "Скоротили   │ │ "Підвищили   │
│  │ конверсію    │ │ витрати на   │ │ точність     │
│  │ на 340%"     │ │ 60%"         │ │ прогнозів    │
│  │              │ │              │ │ до 95%"      │
│  │  E-commerce  │ │  Logistics   │ │  FinTech     │
│  └──────────────┘ └──────────────┘ └──────────────┘
│
│  Картка кейсу: padding: 40px 32px, border-radius: 20px,
│    background: white, border: 1px solid neutral-200
│  Велика цифра результату: 48px bold, primary-500
│  Індустрія: 14px, neutral-500, uppercase
│  hover: lift + shadow + primary border
```

**Mobile**: 1 колонка кейсів, 3-4 колонки технологій.

---

### SEC 5: ЧОМУ МИ (Переваги)

**Призначення**: Зняти заперечення, показати унікальну цінність.

**Розміри**:
- Padding: `100px 0`
- Max-width: `1240px`
- Фон: `white`

**Структура (дві колонки: текст + візуал)**:
```
┌─────────────────────────────────────────────────────────────┐
│  ┌───────────────────────┐    ┌─────────────────────────┐   │
│  │ Section label         │    │                         │   │
│  │ H2: "Чому обирають   │    │    SVG ілюстрація:      │   │
│  │  AI-Force"            │    │    команда / партнерство│   │
│  │                       │    │    / результат          │   │
│  │ 4 переваги з іконками │    │                         │   │
│  │                       │    │    (спокійні тони,      │   │
│  │  Експертиза 10+ років│    │     primary + neutral)  │   │
│  │  Індивідуальний підхід│   │                         │   │
│  │  Прозорість та звіти  │    │                         │   │
│  │  Підтримка 24/7       │    │                         │   │
│  └───────────────────────┘    └─────────────────────────┘   │
│    50% (max 520px)              50%                         │
│    gap: 80px                                                │
└─────────────────────────────────────────────────────────────┘
```

**Компонент переваги** (повторюється 4 рази):
- Іконка: 40×40px, у кольоровому колі (primary-100), ліворуч
- Текст: h4 (17px, semibold) + p (14px, neutral-600)
- Відстань між перевагами: `28px`
- Загальний блок переваг: max-width `520px`

**Mobile** (< 768px): Одна колонка, ілюстрація зверху (меншого розміру).

---

### SEC 6: CTA + КОНТАКТИ

**Призначення**: Конверсія — головний заклик до дії та контактна форма.

**Розміри**:
- Padding: `100px 0`
- Max-width: `900px` (вужча, сфокусована)
- Фон: секція має `--gradient-cta-bg` (дуже легкий primary-50 → white)

**Структура (центрована)**:
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│         H2: "Готові трансформувати ваш бізнес?"              │
│         (text-align: center, neutral-900, 40px)             │
│                                                             │
│         P: "Залиште заявку — ми зв'яжемось протягом 2 годин"│
│         (text-align: center, neutral-600, 18px)             │
│         margin-bottom: 48px                                 │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  ФОРМА (max-width: 560px, центрована)                 │  │
│  │                                                       │  │
│  │  [Ім'я                  ]  (input: 56px висота)       │  │
│  │  [Email / Телефон       ]                             │  │
│  │  [Компанія              ]                             │  │
│  │  [Опишіть задачу...    ]  (textarea: 120px)           │  │
│  │                                                       │  │
│  │  [  Обговорити проєкт →  ]  (CTA: повна ширина, 60px) │  │
│  │                                                       │  │
│  │  privacy note: 12px, neutral-400, центровано          │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  Альтернативні контакти:                                    │
│  📧 hello@ai-force.com    📞 +380...    💬 Telegram        │
│  (flex row, центровано, neutral-600, 16px)                 │
│  margin-top: 48px                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Input-стилі**:
```css
height: 56px;
padding: 0 20px;
border: 1.5px solid var(--color-neutral-300);
border-radius: 12px;
font-size: 16px;
background: white;
transition: border-color 200ms ease, box-shadow 200ms ease;

/* focus */
border-color: var(--color-primary-400);
box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
outline: none;
```

**CTA Button (форма)**:
```css
width: 100%;
height: 60px;
background: var(--gradient-cta);
color: white;
font-weight: 600;
font-size: 17px;
border-radius: 14px;
border: none;
box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
transition: all 300ms ease;

/* hover */
transform: translateY(-2px);
box-shadow: 0 8px 30px rgba(99, 102, 241, 0.4);
```

**Mobile**: Форма на всю ширину, padding форми `24px`.

---

### FOOTER

**Розміри**:
- Padding: `60px 0 40px`
- Max-width: `1240px`
- Фон: `--color-neutral-900`
- Текст: `--color-neutral-400`

```
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌────────┐  ┌────────┐  ┌──────────────┐   │
│  │ AI-Force │  │ Послуги│  │ Компанія│  │ Контакти     │   │
│  │ Logo     │  │ -link  │  │ -link  │  │ 📧, 📞       │   │
│  │          │  │ -link  │  │ -link  │  │              │   │
│  │ Slogan   │  │ -link  │  │ -link  │  │ Social icons │   │
│  └──────────┘  └────────┘  └────────┘  └──────────────┘   │
│                                                             │
│  ─────────────── hairline (neutral-800) ──────────────────  │
│                                                             │
│  © 2026 AI-Force. Усі права захищені.  │  Privacy | Terms  │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. CSS Дизайн-токени (повний набір)

```css
/* =============================================================
   AI-FORCE — Design Token System v1.0
   ============================================================= */

:root {
  /* ─── Кольори: Primary (Indigo/Violet) ─── */
  --color-primary-50:  #EEF2FF;
  --color-primary-100: #E0E7FF;
  --color-primary-200: #C7D2FE;
  --color-primary-300: #A5B4FC;
  --color-primary-400: #818CF8;
  --color-primary-500: #6366F1;
  --color-primary-600: #4F46E5;
  --color-primary-700: #4338CA;
  --color-primary-800: #3730A3;
  --color-primary-900: #312E81;
  --color-primary-950: #1E1B4B;

  /* ─── Кольори: Neutral ─── */
  --color-neutral-50:  #FAFAFA;
  --color-neutral-100: #F5F5F5;
  --color-neutral-200: #E5E5E5;
  --color-neutral-300: #D4D4D4;
  --color-neutral-400: #A3A3A3;
  --color-neutral-500: #737373;
  --color-neutral-600: #525252;
  --color-neutral-700: #404040;
  --color-neutral-800: #262626;
  --color-neutral-900: #171717;
  --color-neutral-950: #0A0A0A;

  /* ─── Кольори: Семантичні ─── */
  --color-success:    #10B981;
  --color-success-bg: #ECFDF5;
  --color-warning:    #F59E0B;
  --color-warning-bg: #FFFBEB;
  --color-error:      #EF4444;
  --color-error-bg:   #FEF2F2;
  --color-info:       #3B82F6;
  --color-info-bg:    #EFF6FF;

  /* ─── Кольори: AI-тематичні акценти ─── */
  --color-ai-glow:    #A78BFA;
  --color-ai-circuit: #6D28D9;
  --color-ai-data:    #06B6D4;
  --color-ai-bot:     #8B5CF6;

  /* ─── Градієнти ─── */
  --gradient-hero:   linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A78BFA 100%);
  --gradient-cta:    linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
  --gradient-card:   linear-gradient(180deg, rgba(99,102,241,0.04) 0%, rgba(139,92,246,0.02) 100%);
  --gradient-glow:   radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.15) 0%, transparent 60%);
  --gradient-section: linear-gradient(180deg, var(--color-neutral-50) 0%, #FFFFFF 100%);

  /* ─── Типографіка: сімейства ─── */
  --font-primary:    'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --font-mono:       'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
  --font-display:    'Plus Jakarta Sans', 'Inter', system-ui, sans-serif;

  /* ─── Типографіка: розміри (clamp для responsive) ─── */
  --text-hero:       clamp(2.75rem, 5vw, 4.5rem);
  --text-h1:         clamp(2.25rem, 4vw, 3.5rem);
  --text-h2:         clamp(1.75rem, 3vw, 2.5rem);
  --text-h3:         clamp(1.375rem, 2vw, 1.75rem);
  --text-h4:         clamp(1.125rem, 1.5vw, 1.375rem);
  --text-body-lg:    1.125rem;  /* 18px */
  --text-body:       1rem;      /* 16px */
  --text-body-sm:    0.875rem;  /* 14px */
  --text-caption:    0.75rem;   /* 12px */

  /* ─── Типографіка: вага ─── */
  --font-light:      300;
  --font-normal:     400;
  --font-medium:     500;
  --font-semibold:   600;
  --font-bold:       700;
  --font-extrabold:  800;

  /* ─── Типографіка: line-height ─── */
  --leading-tight:   1.1;
  --leading-snug:    1.25;
  --leading-normal:  1.5;
  --leading-relaxed: 1.625;
  --leading-loose:   1.75;

  /* ─── Типографіка: letter-spacing ─── */
  --tracking-tighter: -0.03em;
  --tracking-tight:   -0.02em;
  --tracking-normal:   0;
  --tracking-wide:     0.02em;
  --tracking-wider:    0.05em;

  /* ─── Spacing (8px base grid) ─── */
  --space-1:  0.25rem;  /*  4px */
  --space-2:  0.5rem;   /*  8px */
  --space-3:  0.75rem;  /* 12px */
  --space-4:  1rem;     /* 16px */
  --space-5:  1.25rem;  /* 20px */
  --space-6:  1.5rem;   /* 24px */
  --space-8:  2rem;     /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
  --space-20: 5rem;     /* 80px */
  --space-24: 6rem;     /* 96px */
  --space-28: 7rem;     /* 112px */

  /* ─── Радіуси ─── */
  --radius-sm:    0.375rem;  /*  6px — inputs, tags */
  --radius-md:    0.5rem;    /*  8px — buttons */
  --radius-lg:    0.75rem;   /* 12px — картки */
  --radius-xl:    1rem;      /* 16px — великі картки */
  --radius-2xl:   1.25rem;   /* 20px — CTA, hero-картки */
  --radius-3xl:   1.5rem;    /* 24px — модальні вікна */
  --radius-full:  9999px;    /* pills, badges */

  /* ─── Тіні ─── */
  --shadow-xs:  0 1px 2px  rgba(0, 0, 0, 0.04);
  --shadow-sm:  0 1px 3px  rgba(0, 0, 0, 0.06), 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-md:  0 4px 6px  rgba(0, 0, 0, 0.05), 0 2px 4px rgba(0, 0, 0, 0.04);
  --shadow-lg:  0 10px 25px rgba(0, 0, 0, 0.07), 0 4px 10px rgba(0, 0, 0, 0.04);
  --shadow-xl:  0 20px 50px rgba(0, 0, 0, 0.1), 0 8px 20px rgba(0, 0, 0, 0.05);
  --shadow-cta: 0 4px 24px  rgba(99, 102, 241, 0.35);
  --shadow-cta-hover: 0 8px 30px rgba(99, 102, 241, 0.45);
  --shadow-card-hover: 0 12px 40px rgba(0, 0, 0, 0.08);

  /* ─── Переходи ─── */
  --transition-fast:   150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-normal: 300ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow:   500ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-spring: 500ms cubic-bezier(0.34, 1.56, 0.64, 1);

  /* ─── Z-індекси ─── */
  --z-nav:       100;
  --z-overlay:   200;
  --z-modal:     300;
  --z-toast:     400;
  --z-tooltip:   500;

  /* ─── Макет ─── */
  --container-max:  1240px;
  --container-narrow: 900px;
  --nav-height:     72px;

  /* ─── Borders ─── */
  --border-thin:  1px solid var(--color-neutral-200);
  --border-medium: 1.5px solid var(--color-neutral-300);
  --border-focus: 2px solid var(--color-primary-400);
}
```

---

## 5. Анімації та мікровзаємодії

### 5.1 Загальні принципи

- **Стриманість**: Анімації підсилюють контент, а не відволікають
- **Тривалість**: 150-500ms, більшість — 300ms
- **Easing**: `cubic-bezier(0.4, 0, 0.2, 1)` для природного руху
- **Performance**: `transform` + `opacity` (GPU-accelerated), уникати `width/height` анімацій
- **Reduced motion**: `@media (prefers-reduced-motion: reduce)` — вимикаємо все

### 5.2 Scroll-triggered анімації (Intersection Observer)

```css
/* Базовий клас для елементів, що з'являються при скролі */
.reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 600ms ease-out, transform 600ms ease-out;
}

.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Stagger delay для карток */
.reveal-stagger-1 { transition-delay: 0ms; }
.reveal-stagger-2 { transition-delay: 100ms; }
.reveal-stagger-3 { transition-delay: 200ms; }
.reveal-stagger-4 { transition-delay: 300ms; }
.reveal-stagger-5 { transition-delay: 400ms; }
.reveal-stagger-6 { transition-delay: 500ms; }
```

### 5.3 Hero-секція

- **Заголовок**: fade-in + slide-up (600ms, delay 200ms)
- **Підзаголовок**: fade-in + slide-up (600ms, delay 400ms)
- **CTA-кнопка**: fade-in + scale (500ms, delay 600ms)
- **Статистика**: fade-in + slide-up (500ms, delay 800ms)
- **Візуал (нейромережа)**: постійна повільна анімація (частинки, пульсація), тривалість циклу 8-12s

### 5.4 Картки послуг (hover)

```css
.service-card {
  transition: transform var(--transition-normal),
              box-shadow var(--transition-normal),
              border-color var(--transition-normal);
}

.service-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card-hover);
  border-color: var(--color-primary-300);
}

.service-card:hover .service-card__icon {
  transform: scale(1.05);
}
```

### 5.5 Timeline / Процес (scroll-triggered)

- **Номери кроків**: scale-up + fade-in при скролі (stagger 200ms)
- **З'єднувальні лінії**: ширина анімується від 0 до 100% (draw effect)
- **Точки на лініях**: рухаються зліва направо (3s linear, infinite, тільки коли секція visible)

### 5.6 Кнопки

```css
.btn-primary {
  transition: all var(--transition-normal);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-cta-hover);
}

.btn-primary:active {
  transform: translateY(0);
  transition-duration: 100ms;
}

/* Ripple effect (JS) */
.btn-primary .ripple {
  animation: ripple 600ms ease-out forwards;
}

@keyframes ripple {
  0%   { transform: scale(0); opacity: 0.5; }
  100% { transform: scale(4); opacity: 0; }
}
```

### 5.7 Форма (validation feedback)

- **Input focus**: border-color + box-shadow transition (200ms)
- **Помилка валідації**: label shake (400ms) + border-color → `--color-error`
- **Успішна відправка**: кнопка → spinner (400ms) → галочка (scale-in, 300ms spring)
- **Повідомлення "відправлено"**: toast знизу, slide-up, 400ms, auto-dismiss через 5s

### 5.8 Navigation

- **Scroll**: nav отримує фон `rgba(255,255,255,0.85)` + `backdrop-filter: blur(12px)` після прокрутки > 50px
- **Мобільне меню**: hamburger → повноекранне overlay, slide-in зправа (300ms)
- **Active link**: підкреслення анімується від центру (width 0→100%, 250ms)

### 5.9 Технологічні логотипи

```css
.tech-logo {
  filter: grayscale(100%);
  opacity: 0.6;
  transition: filter var(--transition-normal),
              opacity var(--transition-normal),
              transform var(--transition-normal);
}

.tech-logo:hover {
  filter: grayscale(0%);
  opacity: 1;
  transform: scale(1.08);
}
```

### 5.10 Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .reveal {
    opacity: 1;
    transform: none;
  }
}
```

---

## 6. Mobile-рекомендації

### 6.1 Breakpoints

```css
/* Mobile-first media queries */
/* Базові стилі = mobile (< 640px) */

/* Tablet portrait */
@media (min-width: 640px) { /* sm */ }

/* Tablet landscape */
@media (min-width: 768px) { /* md */ }

/* Desktop */
@media (min-width: 1024px) { /* lg */ }

/* Large Desktop */
@media (min-width: 1280px) { /* xl */ }
```

### 6.2 Адаптація секцій

| Секція | Desktop | Tablet | Mobile |
|---|---|---|---|
| **Hero** | 2 колонки | 2 колонки (50/50) | 1 колонка, візуал → текст |
| **Послуги** | 3×2 grid | 2×3 grid | 1×6 stack |
| **Процес** | Горизонтальний | Горизонтальний (компакт) | Вертикальний |
| **Кейси** | 3 колонки | 2+1 | 1 колонка |
| **Чому ми** | 2 колонки | 2 колонки | 1 колонка |
| **CTA** | Центрована форма | Центрована форма | Форма на всю ширину |

### 6.3 Typography Scaling

- Hero h1: `clamp(2rem, 8vw, 4.5rem)` на mobile
- Section h2: `clamp(1.5rem, 6vw, 2.5rem)` на mobile
- Body: залишається `16px` (не зменшувати нижче!)
- Кнопки: збільшити touch target до мінімум `48px` висоти

### 6.4 Navigation Mobile

- **Hamburger menu** при < 1024px
- Повноекранне overlay-меню
- Пункти меню: `font-size: 20px`, `padding: 16px`, `border-bottom: 1px solid neutral-200`
- Кнопка CTA в меню: повна ширина, `height: 52px`

### 6.5 Performance

- Зображення: `srcset` + `sizes`, WebP + AVIF
- Lazy loading: `loading="lazy"` для зображень нижче fold
- SVG для ілюстрацій та логотипів (масштабування без втрат)
- Мінімізувати layout shift: задавати розміри зображень явно

---

## 7. Чек-лист для розробника

- [ ] Усі кольори використовуються через CSS-змінні (жодних raw hex)
- [ ] Типографіка налаштована через `--text-*` токени
- [ ] `clamp()` для всіх заголовків (responsive без медіа-запитів)
- [ ] `prefers-reduced-motion` поважається
- [ ] Мінімальний touch-target: 48×48px
- [ ] Кольорові контрасти проходять WCAG AA (4.5:1)
- [ ] Усі інтерактивні елементи мають `:focus-visible` стилі
- [ ] Форма має валідацію та стани: idle → loading → success → error
- [ ] Зображення мають `alt`-тексти
- [ ] `aria-label` на іконках без тексту
- [ ] Семантичні HTML5-теги (`<nav>`, `<main>`, `<section>`, `<footer>`)
- [ ] Lazy loading для зображень нижче першого екрану
- [ ] Мета-теги: `viewport`, `description`, `og:image`, `theme-color`

---

## 8. Приклад HTML-структури

```html
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="AI-Force — AI-консалтинг, автоматизація, машинне навчання, чат-боти та аналітика даних для вашого бізнесу.">
  <meta name="theme-color" content="#6366F1">
  <title>AI-Force — ШІ-рішення для бізнесу</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="tokens.css">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <nav class="nav" id="nav">...</nav>
  <main>
    <section id="hero" class="hero">...</section>
    <section id="services" class="services">...</section>
    <section id="process" class="process">...</section>
    <section id="cases" class="cases">...</section>
    <section id="why-us" class="why-us">...</section>
    <section id="cta" class="cta">...</section>
  </main>
  <footer class="footer">...</footer>
</body>
</html>
```

---

## 9. Резюме дизайн-рішень

| Аспект | Рішення | Обґрунтування |
|---|---|---|
| **Основний колір** | Indigo (#6366F1) | Асоціюється з технологіями, інтелектом, довірою |
| **Стиль** | Світлий мінімалізм | Чистота, простір для складної AI-тематики, легке сприйняття |
| **Шрифт** | Inter | Сучасна геометрія, відмінна читабельність, підтримка кирилиці |
| **Сітка** | 3-колонкова для карток | Оптимальний баланс інформації та простору |
| **Акцент** | Градієнт Indigo → Violet | Додає глибини, асоціюється з AI/технологіями |
| **Форма** | Одна CTA-форма в кінці | Не перевантажує, дає час "дозріти" до конверсії |

---

**UI Designer**: UI Designer | **Дата**: 06.08.2026 | **Статус**: Готово до імплементації
