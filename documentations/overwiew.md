# Fitness Backend (FastAPI) — Описание проекта и требования


## 1. Сводка проекта

Fitness Backend — серверная часть мобильного фитнес-приложения. Стек: **FastAPI**, PostgreSQL, Redis, Celery/RQ + брокер Redis, (S3-совместимое хранилище), аутентификация — JWT / OAuth2. Backend предоставляет API для мобильного клиента (Flutter) и административных/веб-инструментов.

---

## 2. Цели и задачи

### 2.1 Бизнес-цели

* Предоставить пользователям мобильного приложения персонализированные рекомендации по калориям и тренировкам.
* Синхронизировать данные пользователя между устройствами.
* Обеспечить безопасную и масштабируемую серверную платформу для дальнейшего развития (подписки, платные функции, соцфункции).

### 2.2 Технические задачи

* Спроектировать RESTFUL API под мобильный клиент.
* Построить модульную архитектуру (Clean Architecture) с четкими границами: контроллеры → сервисы → доменные use-cases → репозитории → data sources.
* Обеспечить тестируемость, наблюдаемость (logging, metrics, tracing) и CI/CD.

---

## 3. Объём и границы системы (Scope)

**Включено в MVP (первый релиз):**

* Пользовательская регистрация/аутентификация (email/password, возможно OAuth2 social later).
* CRUD профиля пользователя (имя, пол, возраст, рост, вес, активность).
* Вычисление BMR/TDEE и базового плана питания (локально на бэке).
* CRUD тренировок (создание, список, удаление).
* Отчёты/статистика (история веса, суммарные калории/время за период).
* Хранение данных в PostgreSQL; кеширование промежуточных расчётов в Redis.
* Документация API (OpenAPI / Swagger) и тесты (unit/integration).

**Вне MVP, но планируется:**

* Интеграция с Google Fit / Apple Health.
* Социальные функции (друзья, челленджи).
* Сканирование штрихкодов / интеграция с базами продуктов.

---

## 4. Участники / Роли

* **Пользователь (User)** — использует мобильное приложение.
* **Администратор (Admin)** — управляет пользователями, контентом, может просматривать метрики.


---

## 5. Функциональные требования

Ниже — разбивка по модулям. Для каждого метода указано краткое описание. В сумме цель — 40–60 конечных точек, по мере разработки список будет детализироваться.

### 5.1 Auth / Пользователи

* `POST /auth/register` — регистрация по email/password. (ввод: email, password, name)
* `POST /auth/login` — авторизация, возвращает access/refresh JWT.
* `POST /auth/refresh` — обновление access token.
* `POST /auth/logout` — выход (инвалидация refresh token).
* `POST /auth/password-reset/request` — запрос сброса пароля.
* `POST /auth/password-reset/confirm` — подтверждение сброса по токену.
* `GET /users/{user_id}` — получить публичную информацию профиля (если разрешено).
* `PUT /users/{user_id}` — обновить профиль (name, age, height, weight, gender, activityLevel).
* `DELETE /users/{user_id}` — деактивация/удаление аккаунта (gdpr-safe flow).

### 5.2 Nutrition (расчёты и рекомендации)

* `POST /nutrition/calculate` — вход: UserInfo (gender, age, height, weight, activityLevel); выход: BMR, dailyCalories, macros.
* `GET /nutrition/me` — получить последние сохранённые расчёты для текущего пользователя.
* `POST /nutrition/save` — сохранить расчёт в историю.
* `GET /nutrition/history?from=&to=` — получить историю расчётов.
* `POST /nutrition/meal-suggestion` — генерация примерного рациона на день (на основе dailyCalories и предпочтений).

### 5.2.1 Расширенная бизнес-логика Nutrition

* `POST /nutrition/recalculate-on-profile-change`  
  — пересчитывает норму калорий и макросы автоматически после изменения профиля пользователя.

* `POST /nutrition/personal-plan`  
  — формирует персональный недельный план питания на основе целей, предпочтений и TDEE.

* `POST /nutrition/meal-plan/validate`  
  — проверяет пользовательский план питания на соответствие рекомендуемым дневным нормам, выявляет нарушения.

* `POST /nutrition/achievements/check`  
  — система проверяет выполнение недельных целей по питанию (например, не превышать дневные калории), сохраняет достижения.

### 5.3 Workouts

* `GET /workouts` — список тренировок пользователя (с пагинацией: page, limit).
* `POST /workouts` — создать тренировку (title, duration, exercises[], caloriesBurned (опционально)).
* `GET /workouts/{id}` — детали тренировки.
* `PUT /workouts/{id}` — обновить.
* `DELETE /workouts/{id}` — удалить.
* `GET /workouts/template` — получить набор шаблонных тренировок (predefined plans).

### 5.4 Progress / Tracking

* `GET /progress/weight?from=&to=` — история веса.
* `POST /progress/weight` — добавить запись веса (date, weight).
* `GET /progress/summary?period=` — агрегированные метрики (sum calories, total time).

### 5.4.1 Расширенная бизнес-логика Progress

* `POST /progress/weekly-report`  
  — формирование автоматического отчёта за неделю (графики, рекомендации, динамика веса).

* `POST /progress/analyze`  
  — анализ прогресса с выводом рекомендаций (например, «вес падает слишком быстро», «вы не достигаете целевых калорий»).

* `POST /progress/forecast`  
  — прогноз изменения веса на основе статистики (линейная регрессия или простая ML-модель).


### 5.5 Media / Assets

* `POST /media/upload` — получение presigned URL для загрузки в S3.
* `GET /media/{id}` — получить метаданные/URL.

### 5.6 Admin / Management (CRUD)

* `GET /admin/users` — список пользователей (фильтры).
* `GET /admin/metrics` — базовые метрики (DAU, MAU, retention).
* `POST /admin/content` — управлять шаблонами тренировок/питания.

### 5.7 Goals system (расширенная логика)

* `POST /goals` — создать новую цель (например, «сбросить 3 кг», «выполнять 4 тренировки в неделю»).
* `GET /goals` — список целей.
* `GET /goals/{id}` — детали цели.
* `PATCH /goals/{id}` — обновить прогресс или статус.
* `DELETE /goals/{id}` — удалить цель.

### 5.7.1 Сложная бизнес-логика целей

* `POST /goals/evaluate`  
  — автоматическая проверка выполнения: анализ веса, тренировок, питания.

* `POST /goals/auto-update`  
  — автопрогресс целей по событиям (новая тренировка, новое измерение веса).

* `POST /goals/streak`  
  — расчёт «серии успехов» (дней подряд, когда цель достигнута).


> *Примечание:* каждый эндпоинт поддерживает валидацию входящих данных (Pydantic), возвращает структурированные ошибки и использует уровни HTTP-кодов корректно.

---

## 6. Нефункциональные требования

### 6.1 Производительность и масштабируемость

* **Запросы:** средний response time для простых GET/POST — <200ms (при cold-cache); целевые 100ms для key-use endpoints при p90.
* **Нагрузка:** система должна выдерживать минимум 500 запросов/сек в пиковые моменты (вертикальное увеличение + горизонтальное масштабирование API через контейнеры).
* **Горизонтальное масштабирование:** stateless FastAPI приложения в контейнерах (k8s / ECS). Redis + Postgres как stateful сервисы в кластере.

### 6.2 Надёжность и доступность

* **Uptime**: стремимся к 99.9% SLA для серверной части (за исключением обслуживания).
* **Резервное копирование**: ежедневный бэкап PostgreSQL + точки восстановления за 7–14 дней.

### 6.3 Безопасность

* **Аутентификация:** JWT (access ~15m, refresh ~30d) + возможность revoke.
* **Шифрование:** TLS 1.2+/HTTPS для всего трафика. Хранение секретов — в CI/CD secrets manager/HashiCorp Vault.
* **Пароли:** хранение с bcrypt/argon2.
* **Защита от CSRF:** неактуально для REST API с JWT, но предусмотреть защиту на сторону web UI.
* **Rate limiting:** для критичных эндпоинтов (login, password-reset) — IP- и user-based rate limits.
* **Валидация:** строгая валидация входных данных (Pydantic).
* **Логи и аудит:** хранение логов доступа и действий (для admin операций).

### 6.4 Тестирование и качество кода

* **Unit tests:** 70–80% покрытия для критичных модулей.
* **Integration tests:** для всех основных flows (auth, calculate nutrition, save workout).
* **Contract tests:** если используется внешний сервис.
* **Static analysis:** flake8/ruff, mypy (type hints), black/ruff format.

### 6.5 Наблюдаемость

* **Логирование:** structured logging (JSON) с correlation_id.
* **Метрики:** Prometheus exposition endpoints + Grafana dashboards.
* **Трейсинг:** OpenTelemetry (opentelemetry-python) и интеграция с Jaeger/Tempo.
* **Алерты:** интеграция с PagerDuty / Slack.

### 6.6 Развертывание и CI/CD

* **CI:** тесты + lint + security scan (dependabot / safety) в GitHub Actions / GitLab CI.
* **CD:** автоматическое контейнерное развёртывание в тестовую среду; релизы в production по manual approval.
* **Infrastructure as Code:** Terraform / Pulumi для infra (RDS, Elasticache, S3-buckets, IAM).

---

## 7. Технологический стек

### 7.1 Backend

* **FastAPI** (uvicorn / gunicorn + uvloop) — основной фреймворк.
* **SQLAlchemy (1.4+) / asyncpg** — ORM + драйвер (использовать async patterns или sqlalchemy-core async).
* **Alembic** — миграции БД.
* **Pydantic** — схемы валидации.

### 7.2 Хранение данных

* **PostgreSQL** — основная реляционная БД.
* **Redis** — кеширование, хранение сессий / rate-limiting / pub/sub для задач.

### 7.3 Асинхронная обработка задач

* **Celery + Redis / RabbitMQ** или **RQ + Redis** — для background задач (email, heavy compute, scheduled jobs).

### 7.4 Хранение медиа

* **S3-compatible** (AWS S3 / Wasabi / MinIO) — для фото/видео пользователей.

### 7.5 Observability

* **Prometheus + Grafana** — метрики и дашборды.
* **OpenTelemetry + Jaeger** — распределённые трейсинг.

### 7.6 DevOps

* **Docker + Kubernetes** (k8s) или Docker Compose для локальной разработки.
* **GitHub Actions** для CI/CD.


