import os
from functools import wraps
from hmac import compare_digest

from flask import request

from dotenv import load_dotenv

from src.core.exception.types.auth_credential_exception import AuthCredentialException

load_dotenv()

USERNAME = os.getenv("USERNAME_PYTHON")
PASSWORD = os.getenv("PASSWORD_PYTHON")

def basic_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization

        if not auth:
            raise AuthCredentialException("Credenciais não informadas.")

        username_valid = compare_digest(auth.username, USERNAME)
        password_valid = compare_digest(auth.password, PASSWORD)

        if not username_valid or not password_valid:
            raise AuthCredentialException("Usuário ou senha inválidos.")

        return func(*args, **kwargs)

    return wrapper