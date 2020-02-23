"""
api.main.py
"""

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

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

@app.post("/users") 
async def create_user(user_profile: User):
    return {"user" : user_profile}

@app.get("/users/{emails}")
async def get_user_email(email):
    return {"email" : email}

@app.post("/blogs")
async def create_post(whole_post: Blog):
    return {"post" : whole_post}