"""Authentication Package.

This subpackage is meant to provide all the authentication functionality
for the API (user registration and login).
To do this, it implements the username/password flow using OAuth2.
"""

import fastapi as fa
import fastapi.security as fas

from . import models as m
from .utils import password as p
from .utils import token as t

oauth2_scheme = fas.OAuth2PasswordBearer(tokenUrl="token")


def parse_new_user(username: str, password: str) -> m.ParsedNewUser:
    """Parse username and password dict.

    Checks validity of username and password (to be implemented) and hashes the
    password so it can be stored safely. Otherwise an error is raised.
    """
    # TODO (dancab - 2023-01-08): Validate username and password fields by checking:
    # - username: length and only valid characters.
    # - password: length, only valid characters, and secure enough.

    # Parse new user data.
    hashed_password = p.get_password_hash(password)

    # Assemble new user dictionary and convert to pydantic object.
    parsed_new_user = m.ParsedNewUser(
        username=username,
        hashed_password=hashed_password,
    )

    return parsed_new_user


def decode_token(token: str = fa.Depends(oauth2_scheme)) -> m.TokenData:
    """Decode the 'Authorization' bearer token.

    The token data consists of a 'username' and 'expiration' datetime.
    """
    # Decode token.
    token_data = t.decode_token(token)
    return token_data


def authenticate_user(username: str, password: str, hashed_password: str) -> m.Token:
    """Authenticate a user and return Authorization bearer token.

    Args:
        username (str): The username of the user.
        password (str): The password given for authentication.
        hashed_password (str): The hash of the password (should come from the DB).

    Returns:
        The Authorization bearer token.

    Raises:
        ValueError if the password doens't match the hash.
    """
    if not p.verify_password(password, hashed_password):
        raise ValueError("Invalid password.")

    token = t.create_access_token(username)

    return token
