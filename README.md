# Python_WEB_ht13_REST_API
REST API для зберігання та управління контактами. API повинен бути побудований з використанням інфраструктури FastAPI та використовувати SQLAlchemy для управління базою даних.


1. venv
2. pip install poetry
3. poetry install --no-root 
4. Open Docker desktop and CMD. 

4. 1.  Command in CMD: 
docker run --name hw13_base -p 5433:5432 -e POSTGRES_PASSWORD=qwerty123 -e POSTGRES_DB=hw13_base -d postgres
--> command:
docker ps
--> answer:
CONTAINER ID   IMAGE      COMMAND                  CREATED          STATUS          PORTS                    NAMES
f636dccd9d8e   postgres   "docker-entrypoint.s…"   19 seconds ago   Up 18 seconds   0.0.0.0:5433->5432/tcp   hw13_base

4. 2. Check in Docker desktop if container hw13_base is working.

5. Afted Postgres base creation and models.py is ready, perform migration of data to Postgres:
5. 1. alembic init migrations
5. 2. Оскільки ми хочемо використовувати автогенерацію SQL скриптів у міграціях alembic, нам необхідно повідомити про це оточення alembic у файлі env.py, який розташований у папці migrations. Відкриємо його і насамперед імпортуємо нашу декларативну базу Base з файлу models.py та рядок підключення SQLALCHEMY_DATABASE_URL до нашої бази даних.

from src.database.models import Base
from src.database.db import SQLALCHEMY_DATABASE_URL

Далі нам необхідно знайти наступний рядок нижче в коді файлу env.py:

target_metadata = None

і замість None, вказати наші метадані:

target_metadata = Base.metadata

Тут виконаємо заміну рядка підключення до бази даних на актуальну:

config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
5. 3. Створюємо міграцію наступною консольною командою в корені проекту.

alembic revision --autogenerate -m 'Init'
5. 4. Якщо файл з міграцією успішно створився в папці migrations/versions, то застосуємо створену міграцію:

alembic upgrade head

6. Run the uvicorn server:  uvicorn main:app --reload

7. Готово, можна користуватися - зберігати контакти, переглядати їх, редагувати, видаляти, а також перевіряти, чи є дні народження в найближчі 7 днів.




Винести дані про пошту для розслки в файл .env
