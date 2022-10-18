from sqlmodel import create_engine

postgres_url = "postgresql+psycopg2://postgres:postgres@postgres/postgres_db"
# postgres_url = "postgresql+psycopg2://postgres:postgres@localhost/postgres_db"
engine = create_engine(postgres_url)
