"""
tests.test_mauve_db.py
"""
from pprint import pformat as pf

import pytest
import mongomock
import pymongo

from api import mauve_db


TEST_COL_NAME = "bisque"
SCHEME_KWARG = {"scheme": "pastel"}
SAMPLE_DOCS = [
    {"name": "Sienna", "hex": "#A0522D", **SCHEME_KWARG},
    {"name": "Lavender Blush", "hex": "#FFF0F5", **SCHEME_KWARG},
    {"name": "Pale Goldenrod", "hex": "#EEE8AA", **SCHEME_KWARG}
]

@pytest.fixture
def bisque_collection(mongomock_client):
    """Bisque Colletion is empty"""
    bisque_col = mongomock_client[mauve_db.MONGO_DB][TEST_COL_NAME]
    bisque_col.delete_many({})
    assert not bisque_col.count_documents({})
    yield bisque_col
    bisque_col.delete_many({})
    assert not bisque_col.count_documents({})


@pytest.fixture
def loaded_bisque_collection(bisque_collection, mongo_preloader):
    """Loaded Bisque collection with 3 documents"""
    bisqued = mongo_preloader(
        collection_name=bisque_collection.name,
        docs=SAMPLE_DOCS
    )
    assert bisqued.count_documents({}) == len(SAMPLE_DOCS)
    return bisqued


class TestMauveDB:
    """Test pertaining Mauve (Mongo) DB util methods using mongmock client"""
    @pytest.fixture(autouse=True)
    def _auto_mongomock_patch(self, mongomock_client, monkeypatch):
        """Return the same mongomock DB when client_factory is triggered"""
        monkeypatch.setattr(
            mauve_db, "client_factory",
            value=lambda: mongomock_client,
        )
        yield
        monkeypatch.undo()

    @pytest.fixture
    def set_global_db(self, mongomock_client):
        """Set the global mongo client. Remove client at teardown."""
        def _factory():
            mauve_db.GLOBAL_MONGO.update(client=mongomock_client)
        yield _factory
        mauve_db.GLOBAL_MONGO.pop("client", None)

    @pytest.mark.parametrize(
        "kwargs", [{"host": "dark://khaki.io"}, {"connect_timeout_ms": 1312}]
    )
    def test_client_cfg_factory(self, kwargs):
        if "host" not in kwargs:
            mauve_db.MONGO_CONN_STR = "valid-host-string"
        assert all([v for v in mauve_db.client_cfg_factory(**kwargs).values()])
        
        # teardown
        mauve_db.MONGO_CONN_STR = None

    @pytest.mark.parametrize(
        "kwargs", [{"invalid": None}, {"connect_timeout_ms": 1312}]
    )
    def test_invalid_client_cfg_factory(self, kwargs):
        assert any(
            [not v for v in mauve_db.client_cfg_factory(**kwargs).values()]
        )

    def test_client_factory(self):
        client = mauve_db.client_factory()

    @pytest.mark.parametrize("set_client", [False, True])
    def test_shutdown_client(self, set_client, set_global_db):
        if set_client:
            set_global_db()
        mauve_db.shutdown_client()

    @pytest.mark.parametrize("set_client", [False, True])
    def test_get_db(self, set_client, set_global_db):
        if set_client:
            set_global_db()
        assert isinstance(mauve_db.get_db(), mongomock.database.Database)
    
    def test_update_collection(self, loaded_bisque_collection):
        foo_bar = {"foo": "bar"}
        mauve_db.update_collection(
            col_name=TEST_COL_NAME, doc=foo_bar, filter={"scheme": "pastel"}
        )
        assert loaded_bisque_collection.count_documents(foo_bar) == 3

    @pytest.mark.parametrize("data", [SAMPLE_DOCS, SAMPLE_DOCS[0:1]])
    def test_insert_collection(self, data, bisque_collection):
        mauve_db.insert_collection(TEST_COL_NAME, data)
        assert bisque_collection.count_documents({}) == len(data)
    
    @pytest.mark.parametrize(
        "filter_kwarg, many",
        [
            (SCHEME_KWARG, True),
            (SCHEME_KWARG, False),
        ]
    )
    def test_get_docs(self, loaded_bisque_collection, many, filter_kwarg):
        assert mauve_db.get_docs(TEST_COL_NAME, filter_kwarg, many)

    @pytest.mark.parametrize(
        "filter_kwarg, many",
        [
            ({"foo": "bar"}, True),
            ({"foo": "bar"}, False),
        ]
    )
    def test_get_no_docs(self, loaded_bisque_collection, many, filter_kwarg):
        result = mauve_db.get_docs(TEST_COL_NAME, filter_kwarg, many)
        assert not result or not list(result)


    @pytest.mark.parametrize(
        "filter_kwarg, expected", [
            ({}, 3),
            (SCHEME_KWARG, 3),
            ({"name": "Sienna"}, 1)
        ]
    )
    def test_count(self, loaded_bisque_collection, filter_kwarg, expected):
        assert mauve_db.count(TEST_COL_NAME, filter_kwarg) == expected
