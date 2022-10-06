from typing import Union

from fastapi import APIRouter

router = APIRouter()


@router.get("/items/{x}")
def get_x(x: Union[int, float, str]):
    return {
        "value": x,
        "type": str(type(x)),
    }
