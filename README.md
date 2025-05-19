## Setup Instructions


   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

1. **Start the FastAPI Server**

   Run the following command to start the development server:

   ```bash
   fastapi dev src/
   ```

   The API will be available at `http://127.0.0.1:8000`.

---

## Database Migrations

This project uses Alembic for database migrations.

```bash
   % alembic init -t async migrations
   ```

1. **Add imports and connection configurations to migrations/env.py:**
```python
from src.cars.models import Cars
from src.expenses.models import Expenses
from src.auth.models import Users
from sqlmodel import SQLModel
from src.config import db_config

database_url = db_config.DATABASE_URL

config.set_main_option('sqlalchemy.url', database_url)

***

target_metadata = SQLModel.metadata
   ```
2. **Import SQLModel to migrations/script.py.mako at the top:**
```python
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
${imports if imports else ""}
   ```

3. **Initialize DB structure (To this point it is necessary to have an existing DB called "my_whip")**

```bash
   % alembic revision --autogenerate -m "init"
   ```
4. **Create tables**
```bash
   % alembic upgrade head
   ```