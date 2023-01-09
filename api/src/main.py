"""Main module for the API."""
import fastapi as fa
from src.mongodb import mongodb
from src.routers import auth_router, laundry_booking_router

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


app.include_router(
    auth_router.router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    laundry_booking_router.router,
    prefix="/booking",
    tags=["booking"],
)
