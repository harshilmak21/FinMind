from app.core.database import engine , Base

from app.models import EmailRecord , Transaction

def create_tables():

    Base.metadata.create_all(bind = engine)
    print("Database tables created Successfully!!")

    print("Tables:")
    for table in Base.metadata.sorted_tables:
        print("-" , table.name)


if __name__ == "__main__":
    create_tables()