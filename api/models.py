"""
api.models.py
~~~~~~~~~~~~~
Data Model for MauveDB
"""
# pylint: disable=no-member
from typing import List

import pydantic

# local
from api import model_descriptions, types

USER_EXAMPLE = model_descriptions.USER_EXAMPLE
PROJECT_EXAMPLE = model_descriptions.PROJECT_EXAMPLE


class User(pydantic.BaseModel):
    """User data model"""

    name: str = pydantic.Field(..., example=USER_EXAMPLE["name"])
    email: types.Email = pydantic.Field(
        ..., description="Unique email identifying user", example=USER_EXAMPLE["email"]
    )
    password: str = pydantic.Field(..., example=USER_EXAMPLE["password"])


class Project(pydantic.BaseModel):
    """Project data model"""

    title: str = pydantic.Field(..., example=PROJECT_EXAMPLE["title"])
    user: str = pydantic.Field(None, example=PROJECT_EXAMPLE["user"])
    description: str = pydantic.Field(..., example=PROJECT_EXAMPLE["description"])
    skills: List[str] = pydantic.Field([], example=PROJECT_EXAMPLE["skills"])
    id: str = None
