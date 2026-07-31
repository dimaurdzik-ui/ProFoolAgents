# Конкурентний аналіз Pixel Agents — desktop/API-платформа AI-агентів

**Зріз ринку:** 31 липня 2026 року  
**Метод:** desk research офіційних продуктових сторінок, документації та прайсингів. Маркетингові твердження постачальників не трактуються як незалежно доведені результати.  
**Позначки:** **[Факт]** підтверджено наведеним першоджерелом; **[Висновок]** аналітична інтерпретація фактів; **[Припущення]** потребує перевірки інтерв’ю/тестом. Ціни — USD, без податків, якщо сторінка не каже інакше.

> Обмеження: `https://api.pixelagents.com/docs` під час дослідження не резолвився (DNS). Базову характеристику Pixel Agents перевірено за локальним README репозиторію та URL документації; конкурентні факти — за офіційними сайтами. Не слід публікувати порівняння до повторної перевірки документації Pixel Agents.

## 1. Executive summary

Ринок до липня 2026 року конвергував до **«agent command center»**: desktop + CLI/IDE + cloud workers + MCP/skills/hooks + паралельні/фонові задачі. Отже, самі по собі terminal/file/browser/subagents уже не є стійкою диференціацією. OpenAI Codex/ChatGPT, Claude Code, Cursor і Devin Desktop прямо охоплюють більшість цього контуру.

Найкраща потенційна позиція Pixel Agents — **не ще один AI IDE**, а **модель-агностична desktop/API control plane для загальної агентної роботи**, яка однаково добре керує локальними й віддаленими агентами, кодом, браузером, файлами та довготривалими процесами. Стійка перевага має будуватися навколо: (1) прозорої оркестрації та відновлення процесів; (2) відкритого API/automation surface; (3) переносних skills/memory; (4) контрольованого local/remote execution; (5) observability, budgets і policy.

Найнебезпечніші прямі конкуренти:
1. **OpenClaw** — найближчий category competitor у self-hosted personal-agent сегменті: local-first, open source, messaging surfaces та automation.
2. **OpenAI Codex / ChatGPT desktop** — майже повний збіг поверхонь плюс дистрибуція ChatGPT.
3. **Claude Code** — terminal/IDE/desktop/web, MCP, memory, agent teams, background agents і routines.
4. **Devin Desktop (колишній Windsurf)** — буквально позиціонується як «home for every agent», керує локальними й cloud agents через ACP.
5. **Cursor** — домінуючий developer workflow, cloud fleets, automations і multi-surface distribution.

Непрямі, але стратегічно важливі: GitHub Copilot (дистрибуція через GitHub), OpenHands (open/self-host/model-agnostic), Manus (general-purpose virtual computer), Replit (idea-to-deployed-app), Google Jules (async GitHub coding).

## 2. База порівняння: Pixel Agents

**[Факт, локальний README]** Native desktop для macOS/Windows/Linux; однакові agent, skills, memory, config, keys і sessions між Desktop, CLI та gateway; streaming tool activity, previews, file browser, voice, settings; локальний, remote gateway і cloud режими; headless backend через JSON-RPC/WebSocket; у remote mode tools/terminal/files виконуються на remote host. Проєкти можуть містити кілька folders, repositories, worktrees і sessions. Джерела: локальний `apps/desktop/README.md`; публічні URL: [GitHub releases](https://github.com/PixelResearch/pixel-agents/releases), [docs](https://api.pixelagents.com/docs/).

**[Задано брифом; потребує повторної перевірки docs]** browser, terminal, subagents, довготривалі процеси та API-платформа.

**Поточна теза позиціонування [Висновок]:** «Операційна система/control plane для агентів на desktop і через API», а не «редактор коду з AI».

## 3. Конкурентний landscape (10 компаній/продуктів)

### 3.0 OpenClaw — найближчий category competitor

- **ICP:** **[Факт/маркетинг]** користувачі, яким потрібен open-source personal AI assistant, що працює на їхній машині та доступний через звичні chat apps. **[Висновок]** Найбільший перетин із Pixel Agents — technical self-hosters, founders і operators, яким потрібен постійний агент поза межами одного IDE.
- **Можливості [Факт]:** офіційна сторінка заявляє local execution, open source, роботу через WhatsApp, Telegram та інші chat apps, а також сценарії inbox/email/calendar і автоматизації повсякденних дій. Доступні one-line installer та окремий apps path для macOS, Linux і Windows.
- **Підтверджене ціноутворення:** публічну ціну managed-плану на перевіреній сторінці не підтверджено; open-source/self-hosted дистрибуція доступна напряму. Не слід публікувати конкретне порівняння цін без окремої перевірки актуального packaging.
- **Сильні сторони [Висновок]:** дуже чітка категорійна обіцянка «AI that really does things», local-first narrative, messaging-led UX і велика видимість спільноти. Це робить загальне позиціонування Pixel Agents як «self-hosted personal assistant» недиференційованим.
- **Слабкі сторони / можливість для Pixel Agents [Висновок]:** Pixel Agents може уникнути прямої feature-by-feature боротьби, змістивши акцент на programmable runtime/control plane: Desktop + ACP/JSON-RPC/OpenAI-compatible API, прозоре керування local/remote execution, multi-agent orchestration, batch/eval workflows, recovery, budgets та policy.
- **Дистрибуція [Факт]:** direct website/docs/GitHub/community, one-line installer і apps.
- **Диференціація:** open-source personal agent, який живе на машині користувача та керується через наявні messaging channels.
- **Джерела:** [product and install](https://openclaw.ai/), [docs](https://docs.openclaw.ai/).

### 3.1 OpenAI Codex + ChatGPT desktop — прямий конкурент

- **ICP:** **[Факт із прайсингу]** окремі розробники; startups/growing business; enterprise/education. **[Висновок]** також knowledge workers, яким потрібна загальна робота з browser/computer/files у тому самому desktop.
- **Можливості [Факт]:** desktop local chats; Codex web/cloud, CLI, IDE, SDK/scriptable workflows; local sandbox/permissions, Git worktrees, scheduled tasks; browser preview, computer use (географічно обмежено), SSH і mobile remote control; skills, plugins, MCP, subagents/custom agents; cloud environments, GitHub/Slack/Linear delegation; паралельна довга робота. ChatGPT desktop прямо названий command center для complex work.
- **Підтверджене ціноутворення:** Free $0; Go $8/міс.; Plus $20/міс.; Pro від $100/міс. (5x/20x; $200 tier згадано); Business $20/user/міс. при річній оплаті або $25 місячно, від 2 users; Enterprise/Edu — contact sales; API key — token-based API pricing.
- **Сильні сторони [Висновок]:** максимальна ширина surfaces; ChatGPT як потужний acquisition funnel; власні моделі та єдина підписка; enterprise governance.
- **Слабкі сторони:** **[Факт]** частина computer-use функцій region-limited; API-key режим не включає cloud-based GitHub review/Slack; usage складне й кредитно/лімітне. **[Висновок]** vendor/model lock-in і складність продуктового набору.
- **Дистрибуція [Факт]:** ChatGPT web/desktop/mobile, Codex CLI/IDE/cloud, GitHub/Slack/Linear, API/SDK.
- **Диференціація:** vertically integrated model + consumer/business distribution + один workspace для knowledge work і coding.
- **Джерела:** [pricing](https://learn.chatgpt.com/docs/pricing), [desktop app](https://learn.chatgpt.com/docs/app), [Codex cloud](https://learn.chatgpt.com/docs/cloud).

### 3.2 Anthropic Claude Code + Claude desktop/Cowork — прямий конкурент

- **ICP:** **[Факт]** individuals, teams 2–150, large enterprises; **[Висновок]** професійні розробники та power users, які живуть у terminal/IDE, але потребують desktop/cloud handoff.
- **Можливості [Факт]:** читає codebase, редагує файли, запускає commands; terminal, VS Code, JetBrains, standalone desktop і web; MCP, CLAUDE.md, auto memory, skills, hooks; agent teams, background agents, Agent SDK; CI/CD, GitHub/GitLab, Slack; recurring routines на managed infrastructure, desktop schedules, remote control/message dispatch і teleport між surfaces; computer use preview.
- **Підтверджене ціноутворення:** Free $0 (без Claude Code); Pro $17/міс. при річній оплаті ($200 upfront), $20 місячно; Max від $100/міс.; Team Standard $20/seat/міс. річно або $25 місячно, Premium $100/$125; Enterprise $20/seat/міс. + usage за API rates, annual. Claude Code включено в усі paid plans.
- **Сильні сторони [Висновок]:** дуже близький до Pixel Agents feature envelope; сильні terminal ergonomics, MCP ecosystem, cross-device continuity і custom Agent SDK.
- **Слабкі сторони:** **[Факт]** usage Claude web/desktop/mobile/Code ділить спільний pool; routines на Anthropic infra, а desktop schedule — на локальній машині. **[Висновок]** Anthropic-model centric; загальний desktop менш нейтральний як multi-provider control plane.
- **Дистрибуція [Факт]:** direct web/desktop/mobile, native installers/Homebrew/WinGet, IDE marketplaces, terminal, Slack, CI/CD, API/platform.
- **Диференціація:** один Claude Code engine на багатьох surfaces + MCP/skills/hooks + agent teams/routines.
- **Джерела:** [Claude Code overview](https://code.claude.com/docs/en/overview), [Claude pricing](https://claude.com/pricing).

### 3.3 Cursor — прямий конкурент у developer ICP

- **ICP:** **[Факт/маркетинг]** individual developers, teams, enterprise software organizations; сторінка рекомендує Pro+ daily-agent users, Ultra power users. 
- **Можливості [Факт]:** desktop IDE, CLI, cloud agents із власними computers, parallel fleets на години/дні, automations за schedules/triggers, terminal/Slack/GitHub, MCP/skills/hooks, team marketplace, Bugbot code review, model choice.
- **Підтверджене ціноутворення:** Hobby Free; Individual Pro $20/міс.; Teams Standard $40/user/міс.; Enterprise custom. Сторінка показує Pro+/Ultra і Teams Premium, але їхні конкретні ціни у доступному рендері не відобразилися — **непідтверджено**.
- **Сильні сторони [Висновок]:** best-in-flow coding UX, сильний бренд/enterprise adoption, model choice, coding-specific context/indexing, local+cloud continuum.
- **Слабкі сторони:** **[Факт]** subscriptions продаються лише напряму через cursor.com, без реселерів. **[Висновок]** кодоцентричність: слабша natural fit для general browser/files/business-process agents; proprietary IDE/workflow.
- **Дистрибуція [Факт]:** direct desktop download, CLI, cloud/mobile, Slack, GitHub, enterprise direct sales, community/forum/workshops.
- **Диференціація:** AI-native IDE + cloud fleets/automations, сфокусовані на software delivery.
- **Джерела:** [product](https://cursor.com/en-US), [pricing](https://cursor.com/pricing).

### 3.4 Devin Desktop (Cognition; нова назва Windsurf) — прямий конкурент

- **ICP:** **[Факт/маркетинг]** individual developers, teams і enterprises; **[Висновок]** teams, що одночасно запускають багато local/cloud coding agents.
- **Можливості [Факт]:** «home for every agent»; керування fleets local/cloud agents; повний IDE; Spaces для shared context і Git worktrees; Kanban/multi-agent management; підтримка Devin Local/Cloud, Codex, Claude Agent, OpenCode, Cascade через Agent Client Protocol (ACP); MCP, skills/plugins; cloud handoff; Slack/Teams, Linear/Jira, GitHub/GitLab/Bitbucket.
- **Підтверджене ціноутворення:** Free $0; Pro $20/міс.; Max $200/міс.; Teams $80/міс. за team plan + $40/міс. за full developer seat; Enterprise contact sales. Paid overage — API pricing.
- **Сильні сторони [Висновок]:** найпряміша конкуренція з тезою «desktop control plane»; підтримка чужих agents/models через ACP; established Windsurf IDE base + Devin cloud.
- **Слабкі сторони:** **[Факт]** desktop download на product page був macOS; JetBrains окремо продовжує Windsurf support. **[Висновок]** головно coding; rebrand Windsurf→Devin може створити тимчасову плутанину, але це не доведена churn-проблема.
- **Дистрибуція [Факт]:** OTA migration з Windsurf, direct desktop, enterprise sales, integrations, наявна база Windsurf; сторінка заявляє 1M+ users/4000+ enterprise customers — це self-reported marketing, не незалежно верифіковано.
- **Диференціація:** multi-agent command center + ACP + Devin cloud і IDE в одному desktop.
- **Джерела:** [Devin Desktop](https://devin.ai/desktop), [pricing](https://devin.ai/pricing).

### 3.5 GitHub Copilot — прямий для coding, непрямий для broader agents

- **ICP:** **[Факт]** individuals/freelancers/students/OSS maintainers; business та enterprise development organizations.
- **Можливості [Факт]:** IDE agent mode, Copilot CLI, GitHub app/mobile, cloud agent у GitHub Actions ephemeral environment; planning, branches, tests/linters, PR; automations by schedule/event; custom agents, MCP, hooks, skills; delegation to third-party Claude Code/Codex на вищих plans; API entry points/integrations. Cloud agent працює лише з GitHub repos, одним repo/branch і одним PR за task; hard max session 59 хв.
- **Підтверджене ціноутворення (individual):** Free $0; Pro $10/user/міс.; Pro+ $39; Max $100. Cloud agent використовує AI credits і GitHub Actions minutes. Business/Enterprise тарифи в доступному фрагменті не були надійно виділені — **не наводимо**.
- **Сильні сторони [Висновок]:** unmatched GitHub-native distribution, governance/traceability, lowest confirmed paid individual entry серед прямих coding suites, marketplace/ecosystem.
- **Слабкі сторони [Факт]:** cloud agent GitHub-only, max 59 minutes, one repo/branch/PR per task; content exclusions не застосовуються до cloud agent. **[Висновок]** не general desktop control plane.
- **Дистрибуція [Факт]:** GitHub.com/Mobile, VS Code/Visual Studio/Xcode/JetBrains/Neovim/Eclipse та інші IDE, CLI, GitHub marketplace/workflows, Microsoft enterprise sales.
- **Диференціація:** agent embedded у system of record для software delivery.
- **Джерела:** [plans](https://github.com/features/copilot/plans), [cloud agent docs](https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent).

### 3.6 OpenHands — прямий open-source/API конкурент

- **ICP:** **[Факт]** individual OSS users; organizations, яким потрібні SaaS/self-host/VPC; **[Висновок]** platform engineers і regulated enterprises, що цінують model/deployment control.
- **Можливості [Факт]:** Agent Canvas browser UI/backend, local/self-host/cloud; CLI, REST/API support, composable Python Software Agent SDK, масштабування до 1000s agents; Git integrations, Slack/Jira/Linear, MCP; RBAC/budgets у Cloud; core під MIT, enterprise source-available.
- **Підтверджене ціноутворення:** Local Open Source Free; SaaS Individual Free з BYOK або provider at-cost без markup; Enterprise custom. Individual: 10 max daily conversations у comparison table; local unlimited.
- **Сильні сторони [Висновок]:** open-source/model-agnostic/self-host; SDK і прозорий execution; low-friction BYOK.
- **Слабкі сторони:** **[Факт]** legacy local GUI потребує Docker; Enterprise multi-user ліцензується; Individual cloud має 10 daily conversations. **[Висновок]** browser/coding-centric і менш polished native desktop/general computer workflow.
- **Дистрибуція [Факт]:** GitHub/OSS, local package/CLI, hosted cloud, enterprise self-host/VPC, Slack community.
- **Диференціація:** open standard/foundation for secure, transparent, model-agnostic software agents.
- **Джерела:** [pricing](https://www.openhands.dev/pricing), [docs](https://docs.openhands.dev/overview/introduction).

### 3.7 Replit Agent — непрямий конкурент (idea-to-app platform)

- **ICP:** **[Факт]** technical і non-technical creators, personal/simple apps, commercial/pro builds, enterprise; designers, ops, SMB owners/founders.
- **Можливості [Факт]:** natural-language app/site build, built-in database, deployment/publishing, integrations, collaboration; parallel agents (Core до 2, Pro до 10); high-level all-in-one hosted build/deploy.
- **Підтверджене ціноутворення:** Starter Free; Core $25 monthly або $20/міс. annual, включає $25 monthly credits; Pro $100 monthly або $95/міс. annual, $100 credits; Enterprise custom.
- **Сильні сторони [Висновок]:** shortest path from prompt to deployed product, strong non-developer onboarding, hosting/database/deploy bundled.
- **Слабкі сторони [Висновок]:** managed-cloud lock-in; менше control над local desktop/files/terminal і general-purpose automation; credit economics. Це аналітичний висновок, не офіційна заява Replit.
- **Дистрибуція [Факт]:** web platform, community/gallery/templates, direct self-serve, enterprise sales, education/creator ecosystem.
- **Диференціація:** creation + runtime + deployment in one hosted product, no-code positioning.
- **Джерела:** [Agent](https://replit.com/ai), [pricing](https://replit.com/pricing).

### 3.8 Manus (Meta) — непрямий general-purpose agent

- **ICP:** **[Факт/позиціонування]** individuals/teams/business users для slides, websites, design, research, mail, browser operations; Team/SSO/API згадані в navigation. **[Висновок]** knowledge workers і SMB, що хочуть finished deliverables, а не coding environment.
- **Можливості [Факт]:** autonomous general AI agent з власним sandbox computer, internet access, persistent filesystem, installable software/custom tools; web/desktop/mobile; browser operator, Wide Research, Mail, Slack, API згадані в офіційній навігації. Manus повідомляє, що тепер є частиною Meta.
- **Ціноутворення:** офіційна pricing URL була доступна, але конкретні числа не відобразилися у серверному контенті — **непідтверджено; не наводимо**.
- **Сильні сторони [Висновок]:** general-purpose outcome orientation; Meta distribution/capital potential; persistent virtual computer.
- **Слабкі сторони [Висновок]:** cloud sandbox замість first-class local control; менша developer depth порівняно з coding suites. Потрібен hands-on test; не видавати за факт.
- **Дистрибуція [Факт]:** web, desktop/mobile downloads, Slack, API, team/enterprise route; потенційна Meta distribution — **припущення**, поки не підтверджено конкретним channel integration.
- **Диференціація:** «virtual colleague» на власному persistent cloud computer, орієнтований на complete work products.
- **Джерела:** [home](https://manus.im/), [docs](https://manus.im/docs/introduction/welcome), [pricing URL](https://manus.im/pricing).

### 3.9 Google Jules — непрямий async coding competitor

- **ICP:** **[Факт/позиціонування]** GitHub developers від occasional fixes до daily і massively parallel workflows.
- **Можливості [Факт]:** autonomous async coding; GitHub repo/branch або issue label; clone у Cloud VM, plan, diff, PR; Gemini; scheduled tasks/CLI/REST API згадані в docs navigation; free Jules: 15 tasks/day, 3 concurrent; Pro: 100/day, 15 concurrent; Ultra: 300/day, 60 concurrent.
- **Ціноутворення:** Jules page не показує окремих сум. Офіційна Google AI plans page підтверджує, що підвищені Jules limits входять у Google AI plans, але конкретну USD ціну не вдалося надійно витягнути з локалізованої сторінки — **не наводимо**.
- **Сильні сторони [Висновок]:** Google/Gemini ecosystem, clear concurrency packaging, GitHub-native async delegation.
- **Слабкі сторони [Факт]:** docs називають Jules experimental; workflow описано навколо GitHub cloud VM. **[Висновок]** вузький coding/GitHub scope, не local/general desktop.
- **Дистрибуція [Факт]:** Google account/AI plans, Jules web, GitHub integration, CLI/REST API/docs.
- **Диференціація:** high-concurrency asynchronous Gemini coding worker із task/day packaging.
- **Джерела:** [Jules](https://jules.google/), [docs](https://jules.google/docs/), [Google AI plans](https://one.google.com/about/google-ai-plans/).

## 4. Карта позиціонування

Осі: **X = coding-specialized → general-purpose work**; **Y = managed cloud → local/self-host/control**.

```text
Local / self-host / execution control
^
| OpenHands        Cursor / Devin Desktop       Pixel Agents*       Claude Code
|                      (hybrid)                 (hybrid, broad)       (hybrid)
|
| GitHub Copilot / Jules        OpenAI Codex + ChatGPT Desktop
|      (cloud coding)                   (hybrid, broad)
|
| Replit Agent                                      Manus
| (hosted app creation)                    (hosted general agent)
+--------------------------------------------------------------------> General work
  Coding-specialized
```

`*` **Pixel Agents placement — [Висновок]** з README + наданого брифу, не результат повного feature audit через недоступність docs.

**Ключовий висновок:** Pixel Agents знаходиться у привабливому, але швидко заповнюваному квадранті **broad + hybrid/local control**. OpenAI і Anthropic уже рухаються сюди; Devin рухається з coding боку; OpenHands — з open/self-host боку.

## 5. Порівняльна матриця (стисло)

| Продукт | General work | Native desktop | Local execution | Cloud/background | Multi-agent | API/SDK | Model-agnostic |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pixel Agents | Так* | Так | Так | Так* | Так* | Так* | Так/ймовірно* |
| OpenAI Codex/ChatGPT | Так | Так | Так | Так | Так | Так | Ні/переважно OpenAI |
| Claude Code | Частково/так | Так | Так | Так | Так | Agent SDK | Ні/переважно Claude |
| Cursor | Переважно код | Так | Так | Так | Так | Обмежено/enterprise API | Так, model choice |
| Devin Desktop | Переважно код | Так | Так | Так | Так | Devin API/ACP | Так |
| GitHub Copilot | Переважно код | App/IDE | Так в IDE/CLI | Так | Custom/3rd party agents | Так/інтеграції | Так, model choice |
| OpenHands | Переважно код | Ні, web/CLI | Так | Так | SDK scale | Так | Так |
| Replit | App creation | Ні, web | Переважно hosted | Так | Parallel agents | Platform APIs/інтеграції | Непідтверджено |
| Manus | Так | Так | Ні, cloud sandbox | Так | Непідтверджено | API згадано | Непідтверджено |
| Jules | Код | Ні, web/CLI | Ні, Cloud VM | Так | Parallel tasks | REST API | Ні/Gemini |

`*` Бриф/локальний README; вимагає повного audit Pixel Agents docs.

## 6. Прогалини ринку

1. **Durable process operations, а не просто “background agents”.** [Висновок] Офіційні сторінки конкурентів говорять про background/schedules/fleets, але рідко роблять центральною цінністю checkpoint/restart, idempotency, queueing, dependency graph, retries, SLAs і incident timeline. Це потрібно перевірити hands-on.
2. **General-purpose + local-first + model-neutral.** Manus general, але cloud-first; OpenHands open/local, але coding-first; Cursor/Devin coding-first; OpenAI/Claude model-vendor suites. Pixel Agents може зайняти перетин.
3. **Єдиний control plane для heterogeneous agents.** Devin/ACP вже претендує на це. Вікно є лише якщо Pixel Agents підтримує не тільки власні subagents, а стандартизовані external runtimes/providers з portable permissions/context.
4. **Прозора економіка.** У більшості — складні quotas/credits/tasks/day/API overage. Простий usage ledger, per-run cost estimate, budget caps і BYOK можуть бути сильним wedge.
5. **Local/remote parity для non-coders.** OpenHands дає control, але технічний; Replit/Manus прості, але hosted. Native UX із file/browser/terminal policy та “safe mode” для ops/research/analyst ICP — потенційна прогалина.
6. **Portable organizational memory.** Конкуренти мають memory/instructions/skills, але portability між models/surfaces неочевидна. Exportable, inspectable, scoped memory з provenance/expiry може відрізняти Pixel Agents.
7. **Agent observability as product.** Trace, tool-output previews, approvals, artifacts, diffs, process health, audit trail і replay в одному desktop/API — можливий enterprise wedge.

## 7. Загрози

- **Feature compression:** OpenAI/Anthropic/Cursor/Devin можуть копіювати surface-level функції за тижні/місяці; checklist parity не є moat.
- **Bundling:** GitHub, ChatGPT, Claude та Google продають agent capability всередині вже куплених subscriptions/ecosystems; standalone willingness-to-pay стискається.
- **Distribution asymmetry:** GitHub owns repos/PRs, IDEs own coding flow, Meta/Google/OpenAI own massive accounts. Pixel Agents потрібен wedge-channel, не лише download page.
- **Protocol capture:** MCP і ACP знижують switching costs, але control point може перейти до найбільшого desktop host (Devin/Cursor/Claude/OpenAI).
- **Security/trust:** local terminal/browser/file execution збільшує blast radius; enterprise вимагатиме sandboxing, policy, secrets isolation, audit, SSO/SCIM та deployment controls.
- **Unit economics:** long-running multi-agent jobs споживають багато tokens/compute; unlimited-looking plans конкурентів субсидуються або мають opaque quotas.
- **Positioning ambiguity:** “AI agents platform” надто широка категорія. Без чіткого job-to-be-done Pixel Agents порівнюватимуть із дешевшим Copilot або знайомим ChatGPT.
- **Open-source pressure:** OpenHands пропонує MIT core, BYOK і self-host без license cost для single user.

## 8. Рекомендації для запуску

### 8.1 ICP і wedge

**Рекомендація:** почати з **technical power users / small product & automation teams (2–20 людей)**, які одночасно виконують coding + browser research + file/data operations і вже мають кілька model/API subscriptions. Це достатньо технічний ICP для setup, але ширший за pure coding.

Не запускатися з тезою «кращий AI coder». Формулювання:

> **Pixel Agents — local/remote command center і API для агентної роботи, що триває довше за один чат: код, браузер, файли, термінал і команди агентів — із контролем, пам’яттю та відновленням.**

### 8.2 Продуктові пріоритети

1. **Durability demo:** закрити laptop/перезапустити app/втратити network → process виживає або чітко відновлюється; показати checkpoints, retries і notifications.
2. **Execution control:** per-tool approval policies, local vs remote boundary, secrets scopes, sandbox/network allowlists, audit export.
3. **Agent/process board:** queue, running/waiting/blocked/review states, dependencies, budgets, estimated/actual cost, cancel/resume.
4. **Open API:** create/steer/cancel/list/stream runs; webhooks; idempotency keys; service accounts; SDK examples. API має бути first-class, не undocumented desktop backend.
5. **Portability:** BYOK/multi-provider, import/export skills and memory, MCP; оцінити ACP compatibility, щоб не поступитися Devin.
6. **Artifact-centric review:** browser snapshots, file diffs, terminal logs, generated docs/data та provenance в одному review surface.
7. **Cross-platform proof:** macOS/Windows/Linux installers і remote host parity як явна перевага проти macOS-only/fragmented desktop offers.

### 8.3 Packaging і pricing experiments

Це **рекомендації, не ринкові факти**:
- Free/local BYOK tier як відповідь OpenHands/Copilot Free.
- Pro seat у зоні $20–30/міс. слід A/B test, бо anchor: Codex/Claude/Cursor/Devin Pro ≈ $20.
- Окремо metered cloud/remote compute, але з прозорим cost ledger і hard budgets.
- Team tier має включати shared skills/memory, run history, policies й pooled budgets; enterprise — SSO/SCIM/audit/VPC/self-host.
- Не обіцяти “unlimited”; продавати predictable included usage + clear overage.

### 8.4 Канали дистрибуції

1. **GitHub releases + OSS/community**: reproducible demos/templates; integration recipes.
2. **CLI-to-desktop loop:** `pixel-agents desktop` як природний activation; desktop-to-API copyable snippets.
3. **MCP/skills marketplace:** кожен integration package як SEO/community acquisition surface.
4. **Use-case launches, не feature launches:** “overnight CI triage”, “research-to-brief with sources”, “multi-repo release operator”, “browser QA → issue → fix → PR”.
5. **Developer communities/Discord + content:** side-by-side cost/reliability benchmarks із відкритою методологією.
6. **API-led partnerships:** agencies, internal tools/platform teams, model providers і remote execution hosts.

## 9. Що перевірити перед зовнішнім використанням

- Повторно відкрити Pixel Agents docs і провести feature-by-feature audit, особливо API auth, run lifecycle, subagent semantics, browser support, persistence, pricing/licensing та enterprise controls.
- Провести 5 однакових hands-on сценаріїв у Pixel Agents, Codex, Claude Code, Devin Desktop і OpenHands: 2-hour task, interruption/recovery, browser+terminal, multi-agent dependency, API automation.
- Перевірити актуальні prices в checkout для країни запуску; Manus/Jules конкретні суми тут свідомо не наведено.
- Не використовувати self-reported adoption claims Cursor/Devin як незалежні market-share metrics.

## 10. Джерела

### Pixel Agents
- https://api.pixelagents.com/docs/ (під час дослідження DNS error)
- https://github.com/PixelResearch/pixel-agents/releases
- Локальний `apps/desktop/README.md`

### Конкуренти — офіційні сторінки
- OpenAI: https://learn.chatgpt.com/docs/pricing ; https://learn.chatgpt.com/docs/app ; https://learn.chatgpt.com/docs/cloud
- Anthropic: https://code.claude.com/docs/en/overview ; https://claude.com/pricing
- Cursor: https://cursor.com/en-US ; https://cursor.com/pricing
- Devin Desktop: https://devin.ai/desktop ; https://devin.ai/pricing
- GitHub Copilot: https://github.com/features/copilot/plans ; https://docs.github.com/en/copilot/concepts/agents/cloud-agent/about-cloud-agent
- OpenHands: https://www.openhands.dev/pricing ; https://docs.openhands.dev/overview/introduction
- Replit: https://replit.com/ai ; https://replit.com/pricing
- Manus: https://manus.im/ ; https://manus.im/docs/introduction/welcome ; https://manus.im/pricing
- Jules: https://jules.google/ ; https://jules.google/docs/ ; https://one.google.com/about/google-ai-plans/
