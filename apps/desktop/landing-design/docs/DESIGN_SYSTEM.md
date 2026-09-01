# Landing Page UI Design System

##  Design Foundations

### Color System — Light Theme

| Token | Hex | Usage |
|---|---|---|
| `--color-primary-50` | `#eff6ff` | Lightest backgrounds, badges |
| `--color-primary-100` | `#dbeafe` | Subtle highlights |
| `--color-primary-200` | `#bfdbfe` | Borders, dividers |
| `--color-primary-500` | `#3b82f6` | Primary actions, links, focus rings |
| `--color-primary-600` | `#2563eb` | Primary hover, active states |
| `--color-primary-700` | `#1d4ed8` | Strong emphasis |
| `--color-primary-900` | `#1e3a8a` | Headings, dark backgrounds |

| Token | Hex | Usage |
|---|---|---|
| `--color-neutral-50` | `#fafafa` | Page background |
| `--color-neutral-100` | `#f5f5f5` | Section alt background |
| `--color-neutral-200` | `#e5e5e5` | Subtle borders |
| `--color-neutral-300` | `#d4d4d4` | Dividers |
| `--color-neutral-400` | `#a3a3a3` | Placeholder text |
| `--color-neutral-500` | `#737373` | Secondary text |
| `--color-neutral-700` | `#404040` | Body text |
| `--color-neutral-900` | `#171717` | Headings, primary text |

| Semantic | Hex | Usage |
|---|---|---|
| `--color-success` | `#16a34a` | Success states, checkmarks |
| `--color-success-bg` | `#f0fdf4` | Success backgrounds |
| `--color-warning` | `#ea580c` | Warning states |
| `--color-error` | `#dc2626` | Error states |
| `--color-info` | `#2563eb` | Info badges, tips |

### Typography System

**Font Stack**: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`

| Token | Size / Line | Weight | Usage |
|---|---|---|---|
| `--text-display` | 3.5rem / 1.1 | 800 | Hero headline |
| `--text-h1` | 2.5rem / 1.2 | 700 | Section headings |
| `--text-h2` | 1.875rem / 1.3 | 700 | Sub-section headings |
| `--text-h3` | 1.5rem / 1.35 | 600 | Card titles |
| `--text-lead` | 1.25rem / 1.6 | 400 | Hero subtitle |
| `--text-body` | 1rem / 1.65 | 400 | Body copy |
| `--text-body-lg` | 1.125rem / 1.65 | 400 | Large body |
| `--text-small` | 0.875rem / 1.5 | 400 | Captions, meta |
| `--text-xs` | 0.75rem / 1.4 | 500 | Labels, badges |

### Spacing System (8px base)

| Token | Value |
|---|---|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-6` | 24px |
| `--space-8` | 32px |
| `--space-12` | 48px |
| `--space-16` | 64px |
| `--space-20` | 80px |
| `--space-24` | 96px |

### Shadows & Elevation

| Token | Value | Usage |
|---|---|---|
| `--shadow-xs` | `0 1px 2px rgb(0 0 0 / 0.05)` | Subtle lift |
| `--shadow-sm` | `0 1px 3px rgb(0 0 0 / 0.1), 0 1px 2px rgb(0 0 0 / 0.06)` | Cards |
| `--shadow-md` | `0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)` | Elevated cards |
| `--shadow-lg` | `0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)` | Modals |
| `--shadow-xl` | `0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)` | Hero CTA glow |

### Border Radius

| Token | Value |
|---|---|
| `--radius-sm` | 6px |
| `--radius-md` | 8px |
| `--radius-lg` | 12px |
| `--radius-xl` | 16px |
| `--radius-2xl` | 24px |
| `--radius-full` | 9999px |

### Transitions

| Token | Value |
|---|---|
| `--transition-fast` | 150ms ease |
| `--transition-base` | 200ms ease |
| `--transition-slow` | 300ms ease |

---

##  Landing Page Structure

### Section 1: Hero
- **Purpose**: Capture attention, communicate core value proposition
- **Layout**: Centered, max-width 800px
- **Elements**: Headline (display), subtitle (lead), dual CTAs (primary + secondary), hero illustration/abstract shape
- **Visual**: Gradient accent blob behind headline, subtle grid pattern on background
- **Spacing**: `padding: var(--space-24) var(--space-6) var(--space-20)`

### Section 2: Features Grid
- **Purpose**: Showcase 3–6 key product features
- **Layout**: 3-column grid on desktop, 2 on tablet, 1 on mobile
- **Elements per card**: Icon (48px), title (h3), description (body), optional link
- **Card style**: White bg, `--shadow-sm`, `--radius-xl`, hover lift with `--shadow-md`
- **Spacing**: `padding: var(--space-20) var(--space-6)`

### Section 3: How It Works / Steps
- **Purpose**: Explain the product flow in 3–4 simple steps
- **Layout**: Horizontal step flow with connecting lines/arrows on desktop; vertical on mobile
- **Elements per step**: Step number badge, title, description
- **Spacing**: `padding: var(--space-20) var(--space-6)`

### Section 4: Social Proof / Testimonials
- **Purpose**: Build trust with quotes, logos, stats
- **Layout**: 2-column quote cards on desktop, single column on mobile
- **Elements**: Quote text, avatar, name, role, company logo strip above
- **Card style**: Light neutral bg, `--radius-lg`, subtle left border accent
- **Spacing**: `padding: var(--space-20) var(--space-6)`

### Section 5: Pricing / Plans (optional)
- **Purpose**: Transparent pricing with clear CTA per tier
- **Layout**: 3-column cards (Free / Pro / Enterprise)
- **Highlight**: Pro tier elevated with `--shadow-lg` and accent border
- **Spacing**: `padding: var(--space-20) var(--space-6)`

### Section 6: FAQ
- **Purpose**: Address common objections, reduce friction
- **Layout**: Single column accordion, max-width 700px centered
- **Elements**: Question (h3), expandable answer (body)
- **Spacing**: `padding: var(--space-20) var(--space-6)`

### Section 7: Final CTA
- **Purpose**: Conversion-focused closing section
- **Layout**: Centered, max-width 600px
- **Elements**: Headline (h2), description, primary CTA button, secondary link
- **Visual**: Subtle gradient background
- **Spacing**: `padding: var(--space-24) var(--space-6)`

### Section 8: Footer
- **Purpose**: Navigation, legal, social links
- **Layout**: 4-column on desktop, 2 on tablet, stacked on mobile
- **Elements**: Logo, column links, copyright, social icons
- **Spacing**: `padding: var(--space-12) var(--space-6)`

---

##  Responsive Breakpoints

| Breakpoint | Min Width | Layout Behavior |
|---|---|---|
| Mobile | 320px | Single column, stacked sections |
| Mobile Wide | 480px | Single column, comfortable padding |
| Tablet | 640px | 2-column grids, larger touch targets |
| Tablet Wide | 768px | 2-column, sidebar patterns possible |
| Desktop | 1024px | 3-column grids, full navigation |
| Desktop Wide | 1280px | Max-width container (1200px centered) |

### Container
```css
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-6);
}
```

---

##  Component State Specs

### Buttons

| State | Primary | Secondary | Ghost |
|---|---|---|---|
| Default | bg-primary-500, white text | bg-transparent, border neutral-300 | bg-transparent |
| Hover | bg-primary-600, translateY(-1px), shadow-md | bg-neutral-50, border-neutral-400 | bg-neutral-100 |
| Active | bg-primary-700, translateY(0) | bg-neutral-100 | bg-neutral-200 |
| Focus | outline: 2px solid primary-500, outline-offset: 2px | same | same |
| Disabled | opacity: 0.5, cursor: not-allowed | same | same |

### Cards

| State | Visual |
|---|---|
| Default | bg-white, shadow-sm, radius-xl |
| Hover | shadow-md, translateY(-4px), transition 300ms ease |
| Focus | outline: 2px solid primary-500 |

---

## ♿ Accessibility

- All interactive elements: minimum 44×44px touch target
- Color contrast: 4.5:1 for body text, 3:1 for large text (WCAG AA)
- Focus indicators: visible outline on all interactive elements
- `prefers-reduced-motion`: disable animations/transitions
- Semantic HTML: proper heading hierarchy, landmark regions
- Alt text: all images have descriptive alt attributes
