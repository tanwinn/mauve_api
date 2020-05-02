"""
Custom data types for pydantic models
"""

import re

_EMAIL_REGEX_CACHE = re.compile(
    r"^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$"
)


class Email(str):
    """
    Simple email type
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        assert isinstance(v, str), TypeError("string required")
        assert _EMAIL_REGEX_CACHE.fullmatch(v), TypeError("invalid email string")
        return v
