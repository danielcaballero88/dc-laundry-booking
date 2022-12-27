"""Main module for the API."""
import fastapi as fa

app = fa.FastAPI()


@app.get("/")
async def hello_world():
    """Returns Hello World."""
    return {"Hello": "World"}
