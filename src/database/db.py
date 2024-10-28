import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv() # завантажуються дані з файлу .env 

postgres_user = os.getenv("POSTGRESQL_USER")
postgres_password = os.getenv("POSTGRESQL_PASS")
postgres_db_name = os.getenv("POSTGRESQL_DB_NAME")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@localhost:5433/{postgres_db_name}"

# Перевірка наявності даних для підключення
if not all([postgres_user, postgres_password, postgres_db_name]):
    raise ValueError("Потрібно задати всі змінні середовища для підключення до бази даних.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()