from fastapi import FastAPI

from db import create_db_and_tables
from endpoints import boards, tasks, user

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(user.router)
app.include_router(tasks.router)
app.include_router(boards.router)
