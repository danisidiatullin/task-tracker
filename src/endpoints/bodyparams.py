from typing import List, Union

from fastapi import APIRouter, Body
from pydantic import BaseModel

router = APIRouter()


class Post(BaseModel):
    title: str
    body: Union[str, None] = None
    tag: List[str] = []


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


@router.put("/posts/{post_id}")
def update_post(post_id: int, post: Post, user: User, importance: int = Body()):
    results = {
        "post_id": post_id,
        "post": post,
        "user": user,
        "importance": importance + 1000,
    }
    return results
