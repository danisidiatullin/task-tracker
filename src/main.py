from typing import Optional, Union

from fastapi import FastAPI
from sqlmodel import Field, SQLModel

from db import create_db_and_tables
from endpoints import boards, tasks


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = False


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(tasks.router)
app.include_router(boards.router)
# app.include_router(pathparams.router)
# app.include_router(queryparams.router)
# app.include_router(bodyparams.router)
