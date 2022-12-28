"""Module for interaction with MongoDB."""
import os

import pymongo

URI_FORMAT = "mongodb"
HOST = os.environ.get("MONGO_HOST")
USER = os.environ.get("MONGO_USER")
PASS = os.environ.get("MONGO_PASS")

URI = f"{URI_FORMAT}://{USER}:{PASS}@{HOST}"


class MongoDBConnection:
    """MongoDB connection using pymongo directly."""

    def __init__(self):
        self.client = None

    def __del__(self):
        self.close_client()

    def open_client(self):
        """Opens a MongoClient if not already open."""
        if self.client is None:
            self.client = pymongo.MongoClient(URI)

    def close_client(self):
        """Closes the current MongoClient if currently open."""
        if self.client is not None:
            self.client.close()
            self.client = None

    def get_client(self):
        """Get the current MongoClient or open a new one."""
        if self.client is None:
            self.open_client()
        return self.client


mongo_db_conn = MongoDBConnection()
