"""
tests.conftest.py
~~~~~~~~~~~~~~~~~
"""
import logging
from typing import Dict, List, Union

import mongomock
import pytest

from api import mauve_db

LOGGER = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def mongomock_client():
    """Mongomock Mongo client that patches the client_factory"""
    client = mongomock.MongoClient()
    return client


@pytest.fixture
def mongo_preloader(mongomock_client):
    """
    Preload mongomock Mongo database with given documents
    Return the db. Remove inserted docs at teardown.
    """
    inserted = []

    def _factory(collection_name: str, docs: Union[Dict, List[Dict]]):
        db = mongomock_client[mauve_db.MONGO_DB]
        collection = db[collection_name]
        initial_count = collection.count_documents({})
        if isinstance(docs, dict):
            inserted.append(collection.insert_one(docs).inserted_id)
        elif isinstance(docs, list):
            inserted.extend(collection.insert_many(docs).inserted_ids)
        else:
            raise TypeError("list of dict or dict required")
        LOGGER.warning(
            f"Preloaded Mongo Collection {collection_name}: "
            f"inserted = {list(inserted)}"
        )
        inserted.extend([initial_count, collection])
        return collection

    yield _factory

    if inserted:
        # teardown
        LOGGER.warning("tearing down for mongo_preloader . . . ")
        collection = inserted.pop()
        initial_count = inserted.pop()
        assert collection.delete_many({"_id": {"$in": inserted}})
        assert initial_count == collection.count_documents({})
