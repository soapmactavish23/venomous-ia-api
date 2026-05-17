import os
from functools import wraps
from hmac import compare_digest

from flask import request

from src.core.exception.types.auth_credential_exception import AuthCredentialException


def basic_auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.authorization

        username = os.getenv("USERNAME_PYTHON", "admin")
        password = os.getenv("PASSWORD_PYTHON", "123456")

        if not auth:
            raise AuthCredentialException("Credenciais não informadas.")

        username_valid = compare_digest(auth.username or "", username)
        password_valid = compare_digest(auth.password or "", password)

        if not username_valid or not password_valid:
            raise AuthCredentialException("Usuário ou senha inválidos.")

        return func(*args, **kwargs)

    return wrapper