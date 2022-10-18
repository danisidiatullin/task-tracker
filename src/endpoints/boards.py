from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from starlette import status

from db import get_session
from models.board_models import Board, BoardCreate, BoardRead, BoardUpdate

router = APIRouter()


@router.post("/boards/", response_model=BoardRead, status_code=status.HTTP_201_CREATED)
def create_board(*, session: Session = Depends(get_session), team: BoardCreate):
    db_team = Board.from_orm(team)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.get("/boards/", response_model=List[BoardRead])
def read_boards(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
):
    boards = session.exec(select(Board).offset(offset).limit(limit)).all()
    return boards


@router.get("/boards/{board_id}/", response_model=BoardRead)
def read_board(*, board_id: int, session: Session = Depends(get_session)):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.delete("/boards/{board_id}/")
def delete_board(*, session: Session = Depends(get_session), board_id: int):
    board = session.get(Board, board_id)
    if not board:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(board)
    session.commit()
    return {"ok": True}


@router.patch("/boards/{board_id}/", response_model=BoardRead)
def partial_update_board(
    *,
    session: Session = Depends(get_session),
    board_id: int,
    board: BoardUpdate,
):
    db_board = session.get(Board, board_id)
    if not db_board:
        raise HTTPException(status_code=404, detail="Board not found")
    board_data = board.dict(exclude_unset=True)
    for key, value in board_data.items():
        setattr(db_board, key, value)
    session.add(db_board)
    session.commit()
    session.refresh(db_board)
    return db_board
