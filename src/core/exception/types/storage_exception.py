class StorageException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.__message = message