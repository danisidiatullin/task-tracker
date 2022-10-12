import enum
from typing import List, Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import (Column, Enum, Field, Session, SQLModel, create_engine,
                      select)

from endpoints import bodyparams, pathparams, queryparams, root


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroRead(HeroBase):
    id: int


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = False


class Status(str, enum.Enum):
    started = "started"
    finished = "finished"


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: Status = Field(sa_column=Column(Enum(Status)))
    priority: int = 10
    progress: int = 0
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


postgres_url = "postgresql+psycopg2://postgres:postgres@postgres/postgres_db"

engine = create_engine(postgres_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(*, session: Session = Depends(get_session), task: Task):
    new_task = Task.from_orm(task)

    session.add(new_task)

    session.commit()
    session.refresh(new_task)

    return new_task


@app.get("/tasks", response_model=List[Task], status_code=status.HTTP_200_OK)
def read_tasks(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()

    return tasks


@app.get("/users", response_model=List[User], status_code=status.HTTP_200_OK)
def get_users(
    *,
    session: Session = Depends(get_session),
):
    users = session.exec(select(User)).all()

    return users


@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(*, session: Session = Depends(get_session), user: User):
    new_user = User.from_orm(user)

    session.add(new_user)

    session.commit()
    session.refresh(new_user)

    return new_user


@app.post("/heroes/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=List[HeroRead])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroRead)
def read_hero(*, session: Session = Depends(get_session), hero_id: int):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroRead)
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
):
    db_hero = session.get(Hero, hero_id)
    if not db_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.dict(exclude_unset=True)
    for key, value in hero_data.items():
        setattr(db_hero, key, value)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.delete("/heroes/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int):

    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


app.include_router(root.router)
app.include_router(pathparams.router)
app.include_router(queryparams.router)
app.include_router(bodyparams.router)
