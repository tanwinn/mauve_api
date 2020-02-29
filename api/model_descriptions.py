"""
api.model_descriptions.py
~~~~~~~~~~~~~~~~~~~~~~~~~
Pydantic model description for OpenAPI
"""


USER_EXAMPLE = {
    "name": "Thanh Nguyen",
    "email": "foo@bar.com",
    "password": "<ENCRYPTED_JWT_TOKEN>",
}

PROJECT_EXAMPLE = {
    "title": "Finding teammates!",
    "user": "Thanh Nguyen",
    "description": "Looking for teammates for the upcoming PearlHackathon",
    "skills": ["opensource", "hackathon", "any"],
}
