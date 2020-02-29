"""
api.models.py
~~~~~~~~~~~~~
Data Model for MauveDB
"""
# pylint: disable=no-member
from typing import List

import pydantic


class User(pydantic.BaseModel):
    """User data model"""

    name: str
    email: str = pydantic.Field(
        "foo@bar.com", description="Unique email identifying user"
    )
    password: str


class Project(pydantic.BaseModel):
    """Project data model"""

    title: str
    user: str = None
    description: str
    skills: List[str] = []
    id: str = None


class Projects(pydantic.BaseModel):
    """Projects data model"""

    projects: List[Project]


class Users(pydantic.BaseModel):
    """Users data model"""

    users: List[User]
