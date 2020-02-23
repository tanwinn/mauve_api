"""
api.main.py
"""

import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import pymongo

import app.mauve_db as mauve_db

APP_LOGGER = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "https://pearlhacks2020-mauve.herokuapp.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    APP_LOGGER.warning("Starting up app...")
    mauve_db.client_factory()


@app.on_event("shutdown")
async def shutdown():
    APP_LOGGER.warning("Shuting down app...")
    mauve_db.shutdown_client()

@app.get("/")
async def liveness():
    return {"status": "OK"}

@app.get("/db")
async def test_db():
    mauve_db.insert_collection("users", {"foo": "bar"})
    result = mauve_db.count("users")
    print(result)
    return result