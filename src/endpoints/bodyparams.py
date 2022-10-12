from typing import Union

from fastapi import APIRouter, Body
from pydantic import BaseModel, HttpUrl

router = APIRouter()


class Photo(BaseModel):
    url: HttpUrl
    name: str


class Post(BaseModel):
    title: str
    body: Union[str, None] = None
    tag: list[str] = []
    photos: Union[list[Photo], None] = []


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
