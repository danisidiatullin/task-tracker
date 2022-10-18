from sqlmodel import Session, SQLModel, create_engine

postgres_url = "postgresql+psycopg2://postgres:postgres@postgres/postgres_db"
# postgres_url = "postgresql+psycopg2://postgres:postgres@localhost/postgres_db"
engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
