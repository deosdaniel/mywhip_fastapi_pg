# MyWhip — веб-приложение для автоперекупов 🚗

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

- **Backend**: FastAPI, SQLModel, PostgreSQL, Alembic
- **Frontend**: React (Vite), Tailwind CSS + ShadCN
- **Аутентификация**: OAuth2 (JWT)
- **Миграции**: Alembic
- **Тесты**: Pytest + SQLite
- **СУБД**: PostgreSQL 17

---

## 🚀 Установка и запуск

### ✅ Предварительные требования

Установи следующие зависимости:

- [Python 3.13](https://www.python.org/downloads/)
- [PostgreSQL 17](https://www.postgresql.org/download/)
- [Node.js v22.16.0](https://nodejs.org/)

---

### 📦 Установка зависимостей

```bash
# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install

---

## Database Migrations

This project uses Alembic for database migrations.

```bash
   % alembic init -t async migrations
   ```

1. **Initialize DB structure (To this point it is necessary to have an existing DB called "my_whip")**

```bash
   % alembic revision --autogenerate -m "init"
   ```
2. **Create tables**
```bash
   % alembic upgrade head
   ```

---

## Running the Application

1. **Start the FastAPI Server**

   Run the following command to start the development server:

   ```bash
   fastapi dev src/main.py
   ```

   The API will be available at `http://127.0.0.1:8000/docs`.
   
   Now the backend is running.
3. **Start the Node.js Server**
   Run the following commands to start the development server:
   ```bash
   cd frontend
   npm run dev
   ```
   Now the frontend is running at: `http://192.168.0.4:3001/`
