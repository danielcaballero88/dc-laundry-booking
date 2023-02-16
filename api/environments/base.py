import os

URI_FORMAT = "mongodb"
HOST = os.environ.get("MONGO_HOST")
USER = os.environ.get("MONGO_USER")
PASS = os.environ.get("MONGO_PASS")

URI = f"{URI_FORMAT}://{USER}:{PASS}@{HOST}"
