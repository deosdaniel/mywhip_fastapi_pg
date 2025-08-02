## Setup Instructions
Software requiered: 
1. PostrgeSQL 17
2. Node.js v22.16.0
3. Python 3.13

Once you have this repo downloaded, install all the requiered packages using followinng command:
   ```bash
   pip install -r requirements.txt
   cd frontend
   npm install
   ```

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
