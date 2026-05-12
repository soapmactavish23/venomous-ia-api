from functools import wraps


def common_api_responses(namespace):
    def decorator(func):
        func = namespace.response(400, "Operação não permitida")(func)
        func = namespace.response(401, "Acesso negado")(func)
        func = namespace.response(403, "Permissões Insuficientes")(func)
        func = namespace.response(404, "Recurso não encontrado")(func)
        func = namespace.response(500, "Erro interno")(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator