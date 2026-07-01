# before your app can read or write anything, it needs to know:

# Where is the database? → DATABASE_URL
# How do I connect to it? → engine
# How do I talk to it per request? → get_session()
# How do I create the tables on startup? → create_db_and_tables()

from sqlmodel import Session, create_engine, SQLModel

DATABASE_URL= "postgresql://postgres:password@localhost:5433/resume_app"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session