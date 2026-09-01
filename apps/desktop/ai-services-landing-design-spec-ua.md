# Дизайн-концепція лендингу «ШІ, що працює на результат»

**Версія:** 1.0 · **Мова:** українська (`lang="uk"`) · **Тема:** світла  
**Формат:** односторінковий responsive-лендинг про AI-послуги  
**Ціль:** перетворити відвідувача на заявку на первинну консультацію.

Документ є handoff-специфікацією: назви секцій, контентні приклади, CSS-токени, стани компонентів та JS-логіка можна безпосередньо перенести в HTML/CSS/JS.

---

## 1. Візуальна ідея та тон

**Концепція:** «спокійна технологічність». Білий простір і темний navy-текст створюють довіру, а індиго + м'ятний акцент позначають інтелект, автоматизацію та рух уперед. Уникаємо стокових роботів і надмірного неону: hero-візуал — абстрактна схема процесу з вузлами, лініями та числовими маркерами.

**Принципи:**

- одна головна дія на екрані — **«Отримати консультацію»**;
- чітка ієрархія: eyebrow → H1/H2 → короткий доказ → дія;
- картки плоскі, з тонкою рамкою; тінь з'являється лише на hover;
- усі інтерактивні елементи мають keyboard/focus-стан;
- декоративна графіка не містить інформації, необхідної для розуміння пропозиції.

---

## 2. Палітра та контраст

### 2.1. CSS-токени

```css
:root {
  --c-bg: #ffffff;
  --c-surface: #f8fafc;
  --c-surface-blue: #eef2ff;
  --c-border: #e2e8f0;
  --c-border-strong: #cbd5e1;

  --c-ink: #0b1220;           /* заголовки, основний текст */
  --c-ink-soft: #334155;      /* body-текст */
  --c-ink-muted: #64748b;     /* другорядний текст */
  --c-on-accent: #ffffff;

  --c-primary: #4f46e5;       /* основний CTA */
  --c-primary-hover: #3730a3;
  --c-primary-soft: #eef2ff;
  --c-teal: #047857;          /* accent, success, data */
  --c-teal-soft: #ecfdf5;
  --c-warning: #b45309;
  --c-danger: #b91c1c;

  --gradient-hero: linear-gradient(135deg, #f8fafc 0%, #eef2ff 58%, #ecfdf5 100%);
  --gradient-cta: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);

  --font-sans: "Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-display: "Plus Jakarta Sans", var(--font-sans);
  --font-mono: "JetBrains Mono", ui-monospace, monospace;

  --text-xs: .75rem;
  --text-sm: .875rem;
  --text-md: 1rem;
  --text-lg: 1.125rem;
  --text-h3: clamp(1.25rem, 1.7vw, 1.5rem);
  --text-h2: clamp(1.875rem, 3.2vw, 2.75rem);
  --text-hero: clamp(2.75rem, 6vw, 5rem);

  --space-1: .25rem; --space-2: .5rem; --space-3: .75rem;
  --space-4: 1rem; --space-6: 1.5rem; --space-8: 2rem;
  --space-12: 3rem; --space-16: 4rem; --space-20: 5rem;
  --space-24: 6rem;

  --radius-sm: .5rem; --radius-md: .75rem; --radius-lg: 1.25rem;
  --radius-pill: 999px;
  --shadow-card: 0 16px 40px rgb(15 23 42 / .08);
  --shadow-cta: 0 12px 28px rgb(79 70 229 / .24);
  --ease: cubic-bezier(.2, .75, .25, 1);
}
```

### 2.2. Контрастні пари (WCAG AA)

- `--c-ink` `#0B1220` на `#FFFFFF`: **18.72:1** — AAA;
- `--c-ink-soft` `#334155` на `#FFFFFF`: **10.35:1** — AAA;
- `--c-primary` `#4F46E5` на `#FFFFFF`: **6.29:1** — AA для звичайного тексту;
- `--c-primary-hover` `#3730A3` на `#EEF2FF`: **8.88:1** — AAA;
- `--c-teal` `#047857` на `#FFFFFF`: **5.48:1** — AA;
- `--c-warning` `#B45309` на `#FFFFFF`: **5.02:1** — AA;
- `--c-danger` `#B91C1C` на `#FFFFFF`: **6.47:1** — AA.

Не використовувати `#64748B` як текст на білому для body-копірайтингу без перевірки в конкретному розмірі. Колір placeholder не є єдиним способом передати стан — додавати label та текст помилки.

---

## 3. Типографіка, сітка та базові правила

- Display/headings: **Plus Jakarta Sans**, 700–800, `letter-spacing: -0.03em`.
- Body/UI: **Inter**, 400–700, `line-height: 1.55–1.65`.
- Технічні мітки/числа: **JetBrains Mono**, 500.
- Максимальна ширина контейнера: `1200px`; вузький текст: `60ch`.
- Сітка desktop: 12 колонок, `gap: 24px`; tablet: 8 колонок; mobile: 4 колонки.
- Бокові поля: desktop `32px`, tablet `24px`, mobile `20px`.
- Вертикальний padding секцій: desktop `96px`, tablet `80px`, mobile `64px`.
- Мінімальна висота target для button/link: **44px**.
- `scroll-behavior: smooth` використовувати тільки коли `prefers-reduced-motion: no-preference`.

```css
.container { width: min(1200px, calc(100% - 64px)); margin-inline: auto; }
.section { padding-block: 96px; }
.section__eyebrow { color: var(--c-teal); font: 700 var(--text-sm)/1.2 var(--font-mono); letter-spacing: .08em; text-transform: uppercase; }
.section__title { max-width: 720px; color: var(--c-ink); font: 800 var(--text-h2)/1.1 var(--font-display); }
.section__lead { max-width: 60ch; color: var(--c-ink-soft); font-size: var(--text-lg); }
@media (max-width: 1023px) { .container { width: min(100% - 48px, 760px); } .section { padding-block: 80px; } }
@media (max-width: 639px) { .container { width: min(100% - 40px, 520px); } .section { padding-block: 64px; } }
```

---

## 4. Навігація та UI-компоненти

### Header

Sticky header висотою 72px: логотип **«Вектор ШІ»**, якорі «Послуги», «Процес», «Результати», праворуч outline-link «Обговорити задачу». На scroll додається `background: rgb(255 255 255 / .88)`, `backdrop-filter: blur(12px)`, нижня hairline-рамка. На mobile — логотип + menu button; меню відкривається під header, `aria-expanded`, `aria-controls`, Esc закриває.

### Buttons

- `.button--primary`: gradient CTA, білий текст, `padding: 14px 22px`, radius `12px`, shadow `--shadow-cta`;
- `.button--secondary`: білий фон, border `#C7D2FE`, текст `#3730A3`;
- `.button--text`: без фону, індиго-текст, стрілка зрушується на 4px.

Стани: `hover` — primary темнішає до `#3730A3`, `translateY(-1px)`; `active` — `translateY(0)`, тінь зменшується; `focus-visible` — `3px solid #A5B4FC` + `2px` offset; `disabled` — opacity `.5`, cursor `not-allowed`, без hover.

### Cards / badges / form

- Service card: `background: #fff`, border `#E2E8F0`, radius `20px`, padding `28px`; hover — border `#A5B4FC`, lift `-4px`, `--shadow-card`.
- Badge: pill, `#EEF2FF` + `#3730A3`; success badge: `#ECFDF5` + `#047857`.
- Input: висота 52px, border `#CBD5E1`, radius `10px`; focus — border `#4F46E5` і зовнішнє ring; error — border `#B91C1C`, `aria-describedby` на повідомлення.
- Accordion FAQ: native `button`, `aria-expanded`; chevron rotates 180°; контент не має бути доступний лише через hover.

---

## 5. Структура сторінки: 8 секцій

### 1) Hero — «ШІ, що працює на результат»

`<header>` + hero з `min-height: min(760px, 100svh)`, фон `--gradient-hero`. Дві колонки 55/45. Ліворуч:

- eyebrow: **«AI-послуги для бізнесу»**;
- H1: **«Перетворюємо ШІ на вимірюваний результат»**;
- lead: «Знаходимо процеси для автоматизації, проєктуємо безпечні рішення та допомагаємо команді швидше перейти від ідеї до користі.»;
- primary CTA: **«Отримати консультацію»** → `#contact`;
- secondary: **«Переглянути послуги»** → `#services`;
- proof row: «150+ проєктів», «до 40% менше рутини», «підтримка після запуску».

Праворуч — SVG-схема з вузлами «Дані → ШІ → Рішення», `aria-hidden="true"`; не покладатися на неї для змісту.

### 2) Послуги — «Що ми впроваджуємо»

ID `services`, H2: **«AI-рішення для задач, які мають значення»**. 6 карток у grid 3×2: автоматизація процесів, корпоративні асистенти, AI-чатботи, аналітика даних, прогнозування, аудит AI-можливостей. Кожна: іконка Lucide 32px, H3, 2–3 рядки вигоди, текстове посилання «Дізнатися більше →».

### 3) Проблема → результат — «Де з’являється ефект»

Світло-сіра секція з трьома горизонтальними перетвореннями: «Ручна обробка → AI-воркфлоу», «Розрізнені дані → єдина картина», «Повільні відповіді → асистент 24/7». У кожному рядку ліворуч проблема muted, по центру connector, праворуч результат із teal-метрикою. На mobile — вертикальний stack.

### 4) Процес — «Від задачі до працюючого рішення»

4 кроки timeline: **1. Діагностика**, **2. Стратегія**, **3. Прототип**, **4. Запуск і супровід**. Desktop — горизонтальна лінія 2px з numbered circles; mobile — вертикальна лінія зліва. Під timeline primary CTA: **«Оцінити мою задачу»**.

### 5) Результати / кейси

H2: **«Результат видно в цифрах»**. 3 case cards без вигаданих логотипів: місце для реального клієнта, індустрія, задача, одна велика підтверджена метрика («−32% часу на обробку», «+18% конверсії», «95% точності прогнозу»), посилання на повний кейс. Якщо доказів немає — використовувати «приклад сценарію», не видавати його за реальний кейс.

### 6) Довіра — «Безпека та контроль за замовчуванням»

Split layout: ліворуч H2 і короткий текст, праворуч 4 принципи з shield/check icons: контроль доступів, людське рішення для критичних кроків, мінімізація даних, прозорі метрики. Teal callout: **«Ми починаємо з вашої задачі, а не з модного інструмента.»**

### 7) FAQ

5 accordion-питань: «Скільки коштує впровадження ШІ?», «Чи потрібна власна команда розробників?», «Як захищаються дані?», «Коли буде перший результат?», «Чи можна почати з малого прототипу?». Один пункт може бути відкритим за замовчуванням; стан відкриття не повинен зрушувати focus.

### 8) Фінальний CTA + контактна форма

ID `contact`, фон navy `#0B1220`, білий текст, декоративний indigo glow. H2: **«Знайдемо перший корисний сценарій для ШІ»**. Підзаголовок: «Опишіть процес, який забирає найбільше часу. Повернемося з конкретним наступним кроком.»

Форма: ім'я (required), робочий email (required), компанія, textarea «Опишіть процес або проблему», checkbox згоди з політикою. Submit: **«Обговорити AI-рішення»**. Success: «Дякуємо! Ми зв’яжемося з вами, щоб уточнити задачу та запропонувати наступний крок.» Error: зрозумілий текст біля поля + summary над формою.

Footer: логотип, email, політика конфіденційності, copyright; без зайвих навігаційних дублювань.

---

## 6. Scroll-reveal та motion specification

Підключати `IntersectionObserver` з `threshold: .15` і `rootMargin: "0px 0px -10%"`. Елементи отримують клас `.reveal` у HTML; JS додає `.is-visible` лише при вході. `once: true`, щоб сторінка не миготіла при повторному scroll.

```css
.reveal { opacity: 0; transform: translateY(24px); transition: opacity 600ms var(--ease), transform 600ms var(--ease); }
.reveal--left { transform: translateX(-24px); }
.reveal--scale { transform: scale(.96); }
.reveal.is-visible { opacity: 1; transform: none; }
.reveal[data-delay="1"] { transition-delay: 80ms; }
.reveal[data-delay="2"] { transition-delay: 160ms; }
.reveal[data-delay="3"] { transition-delay: 240ms; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after { animation-duration: .001ms !important; animation-iteration-count: 1 !important; transition-duration: .001ms !important; }
  .reveal, .reveal--left, .reveal--scale { opacity: 1; transform: none; }
}
```

```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const items = document.querySelectorAll('.reveal');
if (reduce || !('IntersectionObserver' in window)) {
  items.forEach((el) => el.classList.add('is-visible'));
} else {
  const observer = new IntersectionObserver((entries, obs) => {
    entries.filter((entry) => entry.isIntersecting).forEach((entry) => {
      entry.target.classList.add('is-visible');
      obs.unobserve(entry.target);
    });
  }, { threshold: .15, rootMargin: '0px 0px -10%' });
  items.forEach((el) => observer.observe(el));
}
```

Motion rules: controls respond in ≤150ms; reveal is 500–650ms; do not animate layout height, use `content-visibility` cautiously; never hide the CTA until animation completes; no infinite decorative animation under reduced motion. `prefers-reduced-motion` must result in a fully visible, static page with the same content and focus order.

---

## 7. Responsive правила

### Desktop ≥ 1200px

12-column grid, max-width 1200px, hero 55/45, 3 service cards per row, 4-step horizontal timeline, header links visible. Section padding 96px; H1 up to 80px.

### Tablet 768–1199px

8-column grid; hero 1fr 1fr until 900px, then stacked; services 2 columns; cases 2 columns; timeline remains horizontal only when each step has ≥210px; nav CTA remains, links may collapse. Section padding 80px, H1 `clamp(44px, 6vw, 60px)`.

### Mobile < 768px

4-column grid, 20px gutters; hero single column, visual after CTA; all buttons full-width or stacked; services/cases one column; timeline vertical; stats 2×2; header menu opens as a full-width panel; CTA form fields one column; minimum body size 16px; avoid horizontal overflow and fixed `100vh` (use `svh`).

### QA viewport matrix

Перевірити 375×812, 390×844, 768×1024, 1024×768, 1280×800, 1440×900. Перевірки: немає горизонтального scroll, sticky header не перекриває anchor target (`scroll-margin-top: 88px`), CTA доступна без hover, клавіатура проходить логічно, текст не обрізається при zoom 200%.

---

## 8. Accessibility та реалізаційний checklist

- Один `h1`; секції мають `aria-labelledby`; nav — `<nav aria-label="Основна навігація">`.
- Семантичні `<button>` для accordion/menu, `<a>` для переходів; не імітувати їх `<div>`.
- Focus-visible ring мінімум 3px, не прибирати outline.
- Form labels видимі; required/error повідомлення доступні через `aria-describedby`/`aria-live="polite"`.
- Контраст тексту й CTA відповідає WCAG AA; колір не є єдиним індикатором.
- Інтерактивні targets ≥44×44px; картинки мають змістовний `alt`, декоративні — `alt=""`.
- Реалізувати skip-link «Перейти до основного вмісту».
- Перевірити Lighthouse Performance/Accessibility, клавіатуру, VoiceOver/NVDA та reduced-motion.

**Готовність до handoff:** після підстановки реальних кейсів, email та URL політики цей документ покриває палітру, типографіку, 8 секцій із CTA, компоненти й стани, scroll-анімації, reduced-motion, responsive-правила та WCAG AA-вимоги.
