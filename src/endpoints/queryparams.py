from typing import Union

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/items/")
def get_x_and_y(x: int = 0, y: int = 0):
    return {
        "x": x,
        "y": y,
        "x + y": x + y,
    }


@router.get("/params/")
def get_z(z: Union[str, None] = Query(default=None, min_length=5, max_length=10)):
    results = {
        "x": "xxxxx",
        "y": "yyyyy",
    }
    if z:
        results.update({"z": z})
    return results


@router.get("/param/")
def get_z(z: Union[str, None] = Query(default=None, min_length=5, max_length=10, alias="z-z-z")):
    results = {
        "x": "xxxxx",
        "y": "yyyyy",
    }
    if z:
        results.update({"z": z})
    return results
