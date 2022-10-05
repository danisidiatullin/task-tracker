from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def root1():
    return [1, 2, 3]


# isn't working
# only first occurrence with / is working
@router.get("/")
def root2():
    return 1000
