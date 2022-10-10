from fastapi import FastAPI

from endpoints import bodyparams, pathparams, queryparams, root, tasks, users

app = FastAPI()
app.include_router(root.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(pathparams.router)
app.include_router(queryparams.router)
app.include_router(bodyparams.router)
