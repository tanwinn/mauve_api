"""
api.main.py
"""

import logging

from fastapi import FastAPI
from pydantic import BaseModel
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

class User(BaseModel):
    name: str
    email: str
    password: str


class Blog(BaseModel): 
    title: str
    author: User
    summary: str 

    
    
app = FastAPI()

@app.get("/")
async def liveness():
    return {"status": "OK"}

@app.get("/db")
async def test_db():
    mauve_db.insert_collection("users", {"foo": "bar"})
    result = mauve_db.count("users")
    print(result)
    return result

@app.post("/users") 
async def create_user(user_profile: User):
    return {"user" : user_profile}

@app.get("/users/{emails}")
async def get_user_email(email):
    return {"email" : email}

@app.post("/blogs")
async def create_post(whole_post: Blog):
    return {"post" : whole_post}
