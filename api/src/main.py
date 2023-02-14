"""Main module for the API."""
import fastapi as fa
from fastapi.middleware import cors as fa_cors

from src.mongodb import mongodb
from src.routers import auth_router, slot_booking_router

app = fa.FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    fa_cors.CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "POST",
        "GET",
        "DELETE",
    ],
    allow_headers=["*"],
    max_age=3600,
)


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

app.include_router(slot_booking_router.router)
