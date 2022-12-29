"""Main module for the API."""
import fastapi as fa

import mongodb
from routers import auth_router

app = fa.FastAPI()


@app.on_event("startup")
async def startup():
    """Open MongoDB Client on app startup."""
    mongodb.mongo_db_conn.open_client()


@app.on_event("shutdown")
async def shutdown():
    """Open MongoDB Client on app shutdown."""
    mongodb.mongo_db_conn.close_client()


@app.get("/")
async def hello_world():
    """Returns Hello World."""
    return {"Hello": "World"}


app.include_router(auth_router.router)
