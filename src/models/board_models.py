from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class BoardBase(SQLModel):
    title: str = Field(index=True)


class Board(BoardBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="board")


class BoardCreate(BoardBase):
    pass


class BoardRead(BoardBase):
    id: int


class BoardUpdate(SQLModel):
    name: Optional[str] = None
