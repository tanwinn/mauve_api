"""
Data Model for MauveDB
"""
from typing import List

from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    email: str = Field("foo@bar.com", description="Unique email identifying user")
    password: str


class Project(BaseModel):
    title: str
    user: str = None
    description: str
    skills: List[str] = []
    id: str = None


class Projects(BaseModel):
    projects: List[Project]


class Users(BaseModel):
    users: List[User]