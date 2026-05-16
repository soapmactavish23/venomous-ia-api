class ValidationException(Exception):
    def __init__(self, message: str, objects: list):
        super().__init__(message)
        self.objects = objects