from datetime import datetime

from src.core.config.constants import Constants
from src.core.exception.models.problem import Problem
from src.core.exception.models.validation_exception import ValidationException
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
            detail=str(error),
            user_message=Constants.RECURSO_ACESSO_NEGADO,
            timestamp=datetime.utcnow(),
            objects=[]
        )

    if isinstance(error, StorageException):
        return Problem(
            status=400,
            type='storage',
            title=Constants.RECURSO_ERRO_STORAGE,
            detail=str(error),
            user_message=Constants.RECURSO_ERRO_STORAGE,
            timestamp=datetime.utcnow(),
            objects=[]
        )

    if isinstance(error, GenericException):
        return Problem(
            status=400,
            type='generic',
            title=Constants.RECURSO_OPERACAO_NAO_PERMITIDA,
            detail=str(error),
            user_message=Constants.RECURSO_OPERACAO_NAO_PERMITIDA,
            timestamp=datetime.utcnow(),
            objects=[]
        )

    if isinstance(error, NotFoundException):
        return Problem(
            status=404,
            type='not_found',
            title=Constants.RECURSO_NAO_ENCONTRADO,
            detail=str(error),
            user_message=Constants.RECURSO_NAO_ENCONTRADO,
            timestamp=datetime.utcnow(),
            objects=[]
        )

    if isinstance(error, ValidationException):
        return Problem(
            status=400,
            type='validation_error',
            title="Campos inválidos",
            detail=str(error),
            user_message="Um ou mais campos estão inválidos.",
            timestamp=datetime.utcnow(),
            objects=error.objects
        )

    return Problem(
        status=500,
        type='internal_error',
        title=Constants.RECURSO_ERRO_INTERNO,
        detail=str(error),
        user_message=Constants.RECURSO_ERRO_INTERNO,
        timestamp=datetime.utcnow(),
        objects=[]
    )