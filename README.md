[RU Русская версия](#mywhip--веб-приложение-для-частных-автобизнесменов-🚗) | [ENG English version](#english-version)
# MyWhip — веб-приложение для частных автобизнесменов 🚗

**MyWhip** — это веб-приложение, созданное для автомобильных перекупщиков. Оно позволяет:
- вести учёт автомобилей и связанных расходов,
- управлять карточками машин,
- делиться доступом к авто с коллегами,
- анализировать прибыльность и эффективность продаж с помощью аналитики.

## 📸 Скриншоты

<img width="829" height="878" alt="image" src="https://github.com/user-attachments/assets/47062a87-e4f5-46d6-8b7c-9a6a56cc118e" />


---

## ⚙️ Функциональность

- ✅ Регистрация и авторизация пользователей
- 🚘 CRUD-операции с автомобилями
- 🤝 Совместная работа — доступ к карточке авто для нескольких пользователей
- 💸 Учёт расходов по каждому автомобилю
- 📊 Метрики по прибыли, сроку владения, цене покупки/продажи и т.д.
- 🔒 Защищённый доступ на основе OAuth2
- 🧪 Покрытие backend тестами (pytest)

---

## 🧰 Технологии

- **Backend**: FastAPI, SQLModel, SQLAlchemy
- **Frontend**: React (Vite), Tailwind CSS + ShadCN
- **Аутентификация**: OAuth2 (JWT)
- **Миграции**: Alembic
- **Тесты**: Pytest + SQLite
- **СУБД**: PostgreSQL 17

---
## 📂 Структура проекта
```bash
mywhip_fastapi_pg/
├── src/                 # Backend (FastAPI)
│   ├── auth/
│   ├── cars/
│   ├── db/
│   ├── directories/
│   ├── scripts/
│   ├── shared/
│   ├── users/
│   └── utils/
│   ├── config.py
│   ├── main.py
├── frontend/            # Frontend (React)
├── migrations/          # Alembic миграции
├── tests/               # Тесты
├── requirements.txt     # Python зависимости
├── README.md
└── pytest.ini
```
## 🚀 Установка и запуск

### ✅ Предварительные требования

- [Python 3.13](https://www.python.org/downloads/)
- [PostgreSQL 17](https://www.postgresql.org/download/)
- [Node.js v22.16.0](https://nodejs.org/)

---
📥 Клонирование репозитория
```bash
git clone https://github.com/deosdaniel/mywhip_fastapi_pg.git
cd mywhip_fastapi_pg
```
## 📦 Установка зависимостей

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```
---
## 🗄️ Настройка БД и миграции
1. Убедись, что у тебя создана база данных PostgreSQL с именем my_whip.

2. Инициализация Alembic (нужно только один раз):
```bash
% alembic init -t async migrations
```
3. Генерация первой миграции:
```bash
alembic revision --autogenerate -m "init"
```
4. Применение миграций:
```bash
alembic upgrade head
```
---
## ▶️ Запуск приложения

**Backend** (FastAPI)
```bash
fastapi dev src/main.py
```
Документация API будет доступна по адресу: `http://127.0.0.1:8000/docs`.

**Frontend** (React)
```bash
cd frontend
npm run dev
```
Фронтенд будет доступен по адресу: `http://localhost:3001`

## 🧪 Запуск тестов
```bash
pytest
```

## English version
# MyWhip — A Web App for Independent Car Flippers 🚗

**MyWhip** is a web application designed for independent car dealers and flippers. It allows users to:
- track cars and related expenses,
- manage detailed car profiles,
- share access to car data with team members,
- analyze profitability and sales performance through insightful metrics.

## 📸 Screenshots

<img width="829" height="878" alt="image" src="https://github.com/user-attachments/assets/47062a87-e4f5-46d6-8b7c-9a6a56cc118e" />

---

## ⚙️ Features

- ✅ User registration and authentication
- 🚘 Full CRUD operations for vehicles
- 🤝 Team collaboration — share car cards with other users
- 💸 Expense tracking for each vehicle
- 📊 Sales analytics — profit, ownership duration, purchase/sale prices, and more
- 🔒 Secure access via OAuth2 (JWT-based)
- 🧪 Backend tests included (pytest)

---

## 🧰 Tech Stack

- **Backend**: FastAPI, SQLModel, SQLAlchemy
- **Frontend**: React (Vite), Tailwind CSS + ShadCN
- **Auth**: OAuth2 (JWT tokens)
- **Migrations**: Alembic
- **Tests**: Pytest + SQLite
- **Database**: PostgreSQL 17

---

## 📂 Project Structure

```bash
mywhip_fastapi_pg/
├── src/                 # Backend (FastAPI)
│   ├── auth/
│   ├── cars/
│   ├── db/
│   ├── directories/
│   ├── scripts/
│   ├── shared/
│   ├── users/
│   └── utils/
│   ├── config.py
│   ├── main.py
├── frontend/            # Frontend (React)
├── migrations/          # Alembic migrations
├── tests/               # Backend tests
├── requirements.txt     # Python dependencies
├── README.md
└── pytest.ini
```
## 🚀 Getting Started

### ✅ Prerequisites

- [Python 3.13](https://www.python.org/downloads/)
- [PostgreSQL 17](https://www.postgresql.org/download/)
- [Node.js v22.16.0](https://nodejs.org/)

---
📥 Clone the Repository
```bash
git clone https://github.com/deosdaniel/mywhip_fastapi_pg.git
cd mywhip_fastapi_pg
```
## 📦 Install Dependencies

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```
---
## 🗄️ Database Setup and Migrations
1. Make sure a PostgreSQL database named my_whip is created.

2. Initialize Alembic (only once):
```bash
% alembic init -t async migrations
```
3. Generate the initial migration:
```bash
alembic revision --autogenerate -m "init"
```
4. Apply the migration:
```bash
alembic upgrade head
```
---
## ▶️ Run the Application


**Backend** (FastAPI)
```bash
fastapi dev src/main.py
```
The interactive API docs will be available at: `http://127.0.0.1:8000/docs`.

**Frontend** (React)
```bash
cd frontend
npm run dev
```
The frontend will be running at: `http://localhost:3001`

## 🧪 Run tests
```bash
pytest
```
