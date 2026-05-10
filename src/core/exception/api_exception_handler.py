from datetime import datetime

from src.core.config.constants import Constants
from src.core.exception.models.problem import Problem
from src.core.exception.types.auth_credential_exception import AuthCredentialException
from src.core.exception.types.generic_exception import GenericException
from src.core.exception.types.not_found_exception import NotFoundException
from src.core.exception.types.storage_exception import StorageException


def handle_errors(error: Exception) -> Problem:
    if isinstance(error, AuthCredentialException):
        return Problem(
            status=401,
            type='auth',
            title=Constants.TITLE_NAO_AUTORIZADO,
            detail=error,
            user_message=Constants.RECURSO_ACESSO_NEGADO,
            timestamp=datetime.datetime.utcnow()
        )

    if isinstance(error, StorageException):
        return Problem(
            status=400,
            type='storage',
            title=Constants.RECURSO_ERRO_STORAGE,
            detail=error,
            user_message=Constants.RECURSO_ERRO_STORAGE,
            timestamp=datetime.datetime.utcnow()
        )

    if isinstance(error, GenericException):
        return Problem(
            status=400,
            type='generic',
            title=Constants.RECURSO_OPERACAO_NAO_PERMITIDA,
            detail=error,
            user_message=Constants.RECURSO_OPERACAO_NAO_PERMITIDA,
            timestamp=datetime.datetime.utcnow()
        )

    if isinstance(error, NotFoundException):
        return Problem(
            status=404,
            type='not_found',
            title=Constants.RECURSO_NAO_ENCONTRADO,
            detail=error,
            user_message=Constants.RECURSO_NAO_ENCONTRADO,
            timestamp=datetime.datetime.utcnow()
        )

    return Problem(
        status=500,
        type='not_found',
        title=Constants.RECURSO_ERRO_INTERNO,
        detail=error,
        user_message=Constants.RECURSO_ERRO_INTERNO,
        timestamp=datetime.datetime.utcnow()
    )