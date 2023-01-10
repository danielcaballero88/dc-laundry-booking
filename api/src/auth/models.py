"""Custom types for the auth package."""
import datetime as dt

import pydantic as pyd


class ParsedNewUser(pyd.BaseModel):
    """Model for a Parsed New User."""

    username: str
    hashed_password: str


class Token(pyd.BaseModel):
    """Data model for the Token."""

    token_type: str
    access_token: str
    expiration: dt.datetime


class TokenData(pyd.BaseModel):
    """Model for the data stored in a token."""

    username: str
    expiration: dt.datetime


class TokenCreate(pyd.BaseModel):
    """Typed dict for the data needed to create a token."""

    sub: str
    exp: dt.datetime
