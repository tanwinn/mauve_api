"""
MauveDB utils& managment
"""
from typing import Dict, List, Union
from pprint import pformat as pf
import logging
import os

import pymongo

GLOBAL_MONGO = {}
MONGO_LOGGER = logging.getLogger(__name__)

# hard code configuration
MONGO_CONN_STR = os.environ.get("MONGO_CONN_STR", None)
MONGO_DB = "MAUVE"


def client_factory() -> pymongo.mongo_client.MongoClient:
    """Set the Mongo client"""
    MONGO_LOGGER.warning(f"Getting Mongo client with str={MONGO_CONN_STR}")
    client = pymongo.MongoClient(MONGO_CONN_STR)
    client.server_info()  # check server liveness
    return client

def get_db() -> pymongo.database.Database:
    """Get the database"""
    client = GLOBAL_MONGO.get("client")
    if not client:
        MONGO_LOGGER.warning("No mongo client found. Creating a new one...")
        client=client_factory()
        GLOBAL_MONGO.update(client=client)
    return client[MONGO_DB]

def shutdown_client():
    """Shut down the mongo client"""
    MONGO_LOGGER.warning("Closing mongo client connection")
    client = GLOBAL_MONGO.pop("client", None)
    if not client:
        MONGO_LOGGER.warning("No mongo client found. Do nothing...")
    client.close()

def update_collection(col_name: str, doc: Dict, filter: Dict = None):
    """Update the collection given the collection_name, doc, and filter"""
    MONGO_LOGGER.warning(f"Updating to {col_name}:\n \t {pf(doc)}")
    collection = get_db()[col_name]
    return collection.update_many(filter, {"$set": doc})

def insert_collection(col_name:str, docs: Union[Dict, List[Dict]]) -> Union[str, List[str]]:
    """Insert the collection with many or one doc"""
    MONGO_LOGGER.warning(f"Inserting {len(docs)} docs to {col_name}")
    collection = get_db()[col_name]
    print(collection)
    inserted = None
    if isinstance(docs, list):
        inserted = collection.insert_many(docs).inserted_ids
    else:
        inserted = collection.insert_one(docs).inserted_id
    MONGO_LOGGER.warning(f"Inserted doc(s) with id(s) {inserted}")
    return inserted

def get_docs(col_name: str, filter: Dict = None, many=True) -> Union[Dict, List[Dict]]:
    """Get documents from given col_name collection"""
    MONGO_LOGGER.warning(f"Getting {'many' if many else 'one'} doc(s) in {col_name} with filter={filter}")
    collection = get_db()[col_name]
    if many:
        return collection.find(filter)
    else:
        return collection.find_one(filter)

def count(col_name: str, filter: Dict = {}) -> int:
    """Get document counter"""
    MONGO_LOGGER.warning(f"Counting docs in {col_name} with filter={filter}")
    collection = get_db()[col_name]
    return collection.count_documents(filter=filter)
