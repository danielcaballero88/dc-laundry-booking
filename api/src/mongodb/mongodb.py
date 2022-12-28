"""Module for interaction with MongoDB."""
import os

import pymongo as pym
from pymongo import collection as pym_coll
from pymongo import database as pym_db

URI_FORMAT = "mongodb"
HOST = os.environ.get("MONGO_HOST")
USER = os.environ.get("MONGO_USER")
PASS = os.environ.get("MONGO_PASS")

URI = f"{URI_FORMAT}://{USER}:{PASS}@{HOST}"


class MongoDBConnection:
    """MongoDB connection using pymongo directly."""

    def __init__(self):
        self.client = None
        self.client = self.get_client()

    def __del__(self):
        self.close_client()

    def open_client(self) -> pym.MongoClient:
        """Opens a MongoClient if not already open."""
        if self.client is None:
            self.client = pym.MongoClient(URI)
        return self.client

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

    def get_coll(self, db_name: str, coll_name: str):
        """Get a collection."""
        client: pym.MongoClient = self.client
        database: pym_db.Database = client[db_name]
        collection: pym_coll.Collection = database[coll_name]
        return collection


mongo_db_conn = MongoDBConnection()
