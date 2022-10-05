from fastapi import FastAPI

from endpoints import root, tasks, users

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
app.include_router(tasks.router)
