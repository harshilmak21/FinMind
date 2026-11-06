
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

db_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host="127.0.0.1",
    port=5432,
    database=os.getenv("POSTGRES_DB")
)

engine = create_engine(
    db_url,
    pool_pre_ping=True,
    echo=False
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def test_database_connection():

    try:
        with engine.connect() as connection:

            result = connection.execute(text("SELECT version()"))

            print("Database connected successfully!")
            print(result.scalar())

    except Exception as error:

        print("Database connection failed!")
        print(error)


if __name__ == "__main__":
    test_database_connection()
