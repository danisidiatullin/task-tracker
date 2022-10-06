from fastapi import FastAPI

from endpoints import root, tasks, users, pathparams

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(pathparams.router)
