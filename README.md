# GamesMarket 🎮🕹️

<p align="center">
  <b>Микросервисный маркетплейс видеоиграм на базе FastAPI, SQLAlchemy, Apache Kafka и Django.</b>
</p>

---

## 📖 О проекте

**GamesMarket** — это полноценная платформа для торговли видеоиграми и цифровым контентом. Проект построен по модульной архитектуре и состоит из двух ключевых частей:

1. **`marketAPI`**: Асинхронный бэкенд-сервис на базе **FastAPI**, предоставляющий REST API и обработку событий через **Apache Kafka**. Использует **SQLAlchemy (AsyncIO)** с **aiosqlite** для высокопроизводительной работы с БД.
2. **`front`**: Пользовательский веб-интерфейс, реализованный на **Django**.

---

## 🛠 Технологический стек

- **Бэкенд / API (`marketAPI`)**: Python 3.10+, FastAPI, Pydantic v2
- **База данных**: SQLAlchemy 2.0 (AsyncIO), SQLite / PostgreSQL
- **Брокер сообщений**: Apache Kafka (`aiokafka`)
- **Фронтенд (`front`)**: Django, HTML5/CSS3
- **Сервер приложений**: Uvicorn

---

## 📁 Структура проекта

```text
GamesMarket/
├── marketAPI/                  # Бэкенд и микросервисная логика API
│   ├── mainAPI.py              # Точка входа FastAPI, инициализация таблиц и lifespan
│   ├── routers.py              # Эндпоинты (Пользователи, Игры, Платежи)
│   ├── repository.py           # Слой взаимодействия с базой данных (CRUD)
│   ├── database.py             # Конфигурация SQLAlchemy и ORM-модели
│   ├── schemas.py              # Pydantic-схемы валидации данных
│   └── kafka_manager.py        # Фоновый консьюмер и продюсер Kafka
│
├── front/                      # Веб-интерфейс на Django
│   ├── manage.py
│   └── ...                     # Шаблоны, представления и настройки Django
│
└── README.md
```

---

## 🗄 Модели данных (Database Schema)

- **`UsersORM` (`users`)**: Информация о пользователях (`id`, `name`, `mail`, `password`, `balance`, `library` в формате JSON/текст).
- **`GamesORM` (`games`)**: Каталог товаров (`id`, `name`, `price`).
- **`PaymentORM` (`payment`)**: История финансовых операций (`id`, `user_id`, `value`, `payment_id`, `idempotence_key`, `status`). Поддерживает проверку идемпотентности запросов.

---

## 🔌 API Эндпоинты (`marketAPI`)

### 👤 Пользователи (`/user`)
- `POST /user/addUser` — Регистрация нового пользователя.
- `DELETE /user/deleteUser` — Удаление пользователя по `user_id`.
- `GET /user/checkReg` — Проверка данных авторизации (email и пароль).
- `GET /user/getUserData` — Получение данных профиля и купленных игр.

### 🎮 Игры (`/game`)
- `POST /game/addGame` — Добавление игры в каталог.
- `GET /game/getGames` — Получение списка всех доступных игр.

### 💳 Платежи и Баланс (`/pay`)
- `POST /pay/buyGame` — Покупка игры (проверка баланса, списание средств, проверка идемпотентности и добавление в библиотеку).
- `POST /pay/pupBalance` — Пополнение баланса пользователя.

---

## ⚡ Асинхронная обработка событий (Apache Kafka)

Файл `kafka_manager.py` запускает фоновую задачу для взаимодействия с Kafka (`localhost:9092`):
- **Входящие топики**: `checkreg`, `adduser`, `getuser`, `buygame`, `getgames`, `pupbalance`.
- Обработчик принимает JSON-сообщения, мапит их на Pydantic-схемы, выполняет логику через `routers.py` и отправляет результат в результирующие топики (формата `<topic>_res`).

---

## ⚙️ Быстрый старт

### 1. Подготовка окружения

```bash
git clone https://github.com/voronkov-e-r/games-market.git
cd GamesMarket

# Создание и активация виртуального окружения
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# venv\Scripts\activate   # Для Windows

# Установка зависимостей бэкенда
pip install fastapi uvicorn sqlalchemy aiosqlite pydantic aiokafka django
```

### 2. Запуск FastAPI сервера

```bash
cd marketAPI
uvicorn mainAPI:app --reload --port 8000
```

Интерактивная документация OpenAPI (Swagger) будет доступна по адресу:  
`http://127.0.0.1:8000/docs`

### 3. Запуск Django фронтенда

Откройте новый терминал и выполните:

```bash
cd GamesMarket/front
python manage.py runserver 8080
```

Приложение фронтенда будет доступно по адресу:  
`http://127.0.0.1:8080`
