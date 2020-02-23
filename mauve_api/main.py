"""
api.main.py
"""

import logging

from fastapi import FastAPI, Body
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

import mauve_api.mauve_db as mauve_db
from mauve_api import models, exceptions

APP_LOGGER = logging.getLogger(__name__)
USER_COLL_NAME = "users"
PJ_COLL_NAME = "projects"

app = FastAPI(docs_url="/")


USER_EXAMPLE = {
    "name": "Thanh Nguyen",
    "email": "foo@bar.com",
    "password": "<ENCRYPTED_JWT_TOKEN>"
}

PROJECT_EXAMPLE = {
    "title": "Finding teammates!",
    "user": "Thanh Nguyen",
    "description": "Looking for teammates for the upcoming PearlHackathon",
    "skills": ["opensource", "hackathon", "any"]

}

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

@app.get("/db/{collection_name}/count")
async def test_db(collection_name: str):
    # mauve_db.insert_collection(USER_COLL_NAME, {"foo": "bar"})
    return {"count": mauve_db.count(collection_name)}

@app.post("/users", status_code=200)
async def create_user(user_profile: models.User = Body(USER_EXAMPLE, example=USER_EXAMPLE)):
    """Create new users in users collection"""
    info = {"email" : user_profile.email}
    if mauve_db.count(USER_COLL_NAME, filter=info):
        raise exceptions.DuplicatedError
    mauve_db.insert_collection(
        USER_COLL_NAME, docs=user_profile.dict()
    )
    return info


@app.get("/users", response_model=models.Users)
async def get_user_catalog():
    """Get all users"""
    return {
        "users": [
            models.User.parse_obj(user) for user in mauve_db.get_docs(USER_COLL_NAME)
        ]
    }


@app.get("/users/{email}", response_model=models.User)
async def get_user_by_email(email):
    return models.User.parse_obj(
        mauve_db.get_docs(USER_COLL_NAME, {"email" : email},many=False)
    )

@app.get("/projects", response_model=models.Projects)
async def project_catalog():
    "Check the project catalog"
    return {
        "projects": [
            models.Project.parse_obj(pj) for pj in mauve_db.get_docs(PJ_COLL_NAME)
        ]
    }


@app.post("/projects", status_code=200)
async def create_project(project: models.Project = Body(PROJECT_EXAMPLE, example=PROJECT_EXAMPLE)) -> models.Projects:
    "Post a project catalog"
    _id = mauve_db.insert_collection(PJ_COLL_NAME, docs=project.dict())
    mauve_db.update_collection(PJ_COLL_NAME, doc={"id": str(_id)}, filter={"_id": _id})
    return {"id": str(_id)}


@app.exception_handler(exceptions.DuplicatedError)
async def duplicaed_data_handler(request, exec):
    return PlainTextResponse("Email is not available for use", 409)


@app.post("/blogs")
async def create_post(whole_post: models.Blog):
    return whole_post.dict()
