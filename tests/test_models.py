"""
tests.test_models.py
--------------------
Tests models
"""

import pydantic
import pytest

from api import models, types


@pytest.mark.parametrize(
    "kwarg",
    [{"name": "Chreis", "email": "chris@boohoo.com", "password": "I32WSJ28ru92@!W"}],
)
def test_valid_user(kwarg):
    assert kwarg == models.User(**kwarg).dict(exclude_unset=True)


@pytest.mark.parametrize(
    "kwarg",
    [
        {"email": "chrisbo@ohoo.com", "password": "I32WSJ28ru92@!W"},
        {"name": "Chreis", "password": "I32WSJ28ru92@!W"},
        {"name": "Chreis", "email": "chrisboohoo.com", "password": "I32WSJ28ru92@!W"},
        {"name": "Chreis", "email": 1223, "password": "I32WSJ28ru92@!W"},
        {"name": "Chreis", "email": "chrisbo@ohoo.com"},
    ],
)
def test_invalid_user(kwarg):
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        models.User(**kwarg)


@pytest.mark.parametrize(
    "kwarg",
    [
        {
            "title": "Heklo",
            "user": "chris@boohoo.com",
            "description": "Something",
            "skills": ["eating", "sleeping"],
        },
        {
            "title": "Heklo",
            "description": "Something",
            "skills": ["eating", "sleeping"],
        },
        {"title": "Heklo", "user": "chris@boohoo.com", "description": "Something",},
    ],
)
def test_valid_user(kwarg):
    assert kwarg == models.Project(**kwarg).dict(exclude_unset=True)


@pytest.mark.parametrize(
    "kwarg",
    [
        {
            "user": "chris@boohoo.com",
            "description": "Something",
            "skills": ["eating", "sleeping"],
        },
        {
            "title": "Heklo",
            "user": "chris@boohoo.com",
            "skills": ["eating", "sleeping"],
        },
        {
            "title": "Heklo",
            "user": "chris@boohoo.com",
            "description": "Something",
            "skills": "eating",
        },
    ],
)
def test_invalid_user(kwarg):
    with pytest.raises(pydantic.error_wrappers.ValidationError):
        models.Project(**kwarg)
