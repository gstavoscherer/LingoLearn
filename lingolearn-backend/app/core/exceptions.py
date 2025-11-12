class AppError(Exception):
    def __init__(self, status_code=500, message="Ocorreu um erro inesperado", headers: dict | None = None ):
        self.status_code = status_code
        self.message = message
        self.headers = headers

class ResourceNotFoundException(AppError):
    def __init__(self, message="Esse recurso não foi encontrado", headers = None):
        super().__init__(message, headers, status_code=404,)

class UserNotFoundError(AppError):
    def __init__(self, user_id=None):
        message = "Usuário não encontrado" if user_id is None else f"Não foi encontrado usuário com id: {user_id}"
        super().__init__(status_code=404, message=message)


class UserAlreadyExistsError(AppError):
    def __init__(self):
        message = "Já existe um usuário cadastrado com este e-mail."
        super().__init__(status_code=400, message=message)


class InvalidPasswordError(AppError):
    def __init__(self):
        message="A senha inserida está incorreta"
        super().__init__(status_code=401, message=message)


class AuthenticationError(AppError):
    def __init__(self, email):
        message = f'Não foi possível autenticar usuário com email: {email}'
        headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(status_code=401, message=message, headers=headers)

class InvalidTokenError(AppError):
    def __init__(self, message):
        super().__init__(status_code=401, message=message)
