# Vexio Studio — памятка по проекту

Сайт-визитка веб-студии Vexio (vexiostudio.ru). Flask + HTML/CSS/JS (часть страниц — React на клиенте). Репо: https://github.com/maxxmoto/vexio.git

## Как запустить

```bash
pip install -r requirements.txt
python app.py            # локально (Flask dev, порт 5000 по умолчанию)
```

Продакшен: `gunicorn -b 0.0.0.0:80 app:app` (см. `Procfile`, `amvera.yaml`). Python 3.12+.

## Структура

- `app.py` — весь бэкенд (Flask + SQLAlchemy + несколько JSON-файлов вместо БД).
- `templates/` — главные разделы (отдаются через `send_from_directory` / `render_template`).
- `static/` — статика + **отдельные «мини-сайты»** разделов.
  - `static/hr/`, `static/biz/`, `static/brief/` — самостоятельные разделы.
  - `static/projects/` — 6 демо-страниц портфолио (см. ниже).
  - `static/ai-widget.js` — общий AI-виджет «Коди» (подключается на всех страницах).
- `data/` — runtime-данные (JSON + Excel + SQLite).

## Разделы (публичные страницы)

| Роут | Файл | Рендер |
|---|---|---|
| `/` | `templates/index.html` | статический HTML |
| `/news/` | `templates/news.html` | **React CSR (пустой `#root`)** |
| `/help/` | `templates/help.html` | статический |
| `/dev/` | `templates/dev.html` | статический |
| `/business/` | `static/biz/index.html` | статический |
| `/brief/` | `static/brief/index.html` | **React CSR (пустой `#root`)** |
| `/hr/` | `static/hr/index.html` | статический |
| проекты | `static/projects/<name>/index.html` | статические |

Проекты: `1-maxxmoto`, `2-morskoy-glaz`, `3-engbot`, `5-python-forge`, `6-tennis-brutal`, `7-survivalkit`. Отдельного роута `/projects/` нет — страницы доступны по `/static/projects/...`.

**Важно (CSR):** `news.html` и `brief/index.html` рендерятся на клиенте (React + Babel standalone), весь контент в `<script type="text/babel">`, в HTML только `<div id="root"></div>`. Боты/краулеры без JS видят пустую страницу (мета-теги в `<head>` при этом есть). Не «чини» это без SSR.

## Служебные страницы (без метрики)

- `/admin` → `admin_login.html` → после входа `newadmin.html`.
- `/admin/dashboard`, `/admin/portfolio` → старый `admin.html`.
- `error.html` — 404/500.

## Роуты (app.py)

Публичные:
- `/`, `/news/`, `/help/`, `/dev/`, `/business/`, `/brief/`, `/hr/`, `/sitemap.xml`, `/robots.txt`
- `/api/submit`, `/api/hr-apply`, `/api/brief-apply`, `/api/business-apply`, `/api/help-apply`, `/api/dev-apply` — формы заявок
- `/api/ai-chat` — бэкенд Коди (только HF_KEY, без внешних LLM)
- `/api/portfolio/<category>`, `/api/news`

Админские (`@login_required`):
- `/admin/download-excel`, `/admin/dashboard`, `/admin/portfolio`, `/admin/portfolio/delete/<id>`
- `/admin/api/submissions` (GET/DELETE/status), `/admin/api/referrals`, `/api/admin/data`, `/check-files`

## Переменные окружения / секреты

| Переменная | Обязат. | Назначение |
|---|---|---|
| `ADMIN_PASSWORD` | **да** | пароль админки (хранится как hash; без него вход отключён) |
| `ADMIN_USERNAME` | нет | логин (по умолч. `admin`) |
| `SECRET_KEY` | реком. | ключ сессий Flask (иначе генерится случайно и сессии слетают при рестарте) |
| `DATABASE_URL` | нет | Postgres; по умолч. `sqlite:///vexio.db` |
| `COOKIE_SECURE` | нет | `1` по умолч. (HTTPS). `0` только для локального HTTP |
| `HF_KEY` | нет | ключ HuggingFace для LLM-ответов Коди |
| `NEWS_KEY` | нет | ключ NewsAPI для `/api/news` |

На amvera задаются в разделе «Секреты».

## Админка

- Логин: `ADMIN_USERNAME` + `ADMIN_PASSWORD` (hash через `check_password_hash`) + math-captcha.
- Rate-limit: 10 попыток / 10 мин по IP (`LOGIN_ATTEMPTS` в `app.py`).
- Сессии: `HttpOnly`, `SameSite=Lax`, `Secure`, `ProxyFix` для корректного IP за прокси.
- Заявки пишутся в `data/notifications.json` + `data/submissions.xlsx` (плюс SQLite для `/api/submit`).

## Коди (AI-виджет)

- `static/ai-widget.js` — единый для всех страниц.
- Локальные правила: `DEFAULT_RULES` (общие) + merge `window.__AI_RULES__` (свои правила на `dev.html` и `hr/index.html`). Разделовые правила **не заменяют**, а дополняют общие.
- Матчинг: `norm()` (нижний регистр, чистка пунктуации) + `match()` (по длине совпадения, потом по числу совпадений).
- Если нет совпадения → `fetch('/api/ai-chat', timeout 6s)`. Бэкенд: только если задан `HF_KEY`, иначе `{reply: null}` → виджет показывает свой fallback.
- Telegram-боты и `pollinations.ai` **удалены** (не возвращать).

## Яндекс.Метрика

ID счётчика: **111247436**. Код добавлен перед `</body>` во все 13 публичных страниц. В админке/error метрики нет (осознанно).

## Данные

- `data/portfolio.json`, `data/referrals.json` — в git (публичные/пустые).
- `data/visitors.json`, `users.json`, `notifications.json`, `submissions.json`, `submissions.xlsx` — **в `.gitignore`** (персональные данные).
- SQLite `vexio.db` — тоже gitignored (`*.db`).

## Безопасность (что уже сделано)

- Удалены хардкод-токены Telegram и сами боты (`bot_main.py`, `notify_bot.py`, `telegram_bot.py`, `bot.js`).
- Пароль админки хэшируется, rate-limit на логин.
- Закрыты утечки: `/api/notifications`, `/excel`, `/version` (не отдаёт git-hash/хост), `/check-files` (только админ).
- Cookie-флаги сессий настроены.
- CSRF — через `SameSite=Lax`.

## Готчи

- Не коммить токены/пароли в код — только env.
- `news.html` и `brief` — CSR, осторожно с изменениями (могут сломать рендер).
- `static/hr/sitemap.xml` существует, не путать с корневым `static/sitemap.xml`.
- После правок `ai-widget.js` проверять `node --check static/ai-widget.js`.
- Правки `app.py` проверять `python -m py_compile app.py`.
