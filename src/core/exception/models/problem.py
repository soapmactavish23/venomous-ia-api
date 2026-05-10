from datetime import datetime

from src.core.exception.models.object_problem import ObjectProblem


class Problem:
    def __init__(self,
                 status: int,
                 type: str,
                 title: str,
                 detail: str,
                 user_message: str,
                 timestamp: datetime,
                 objects: ObjectProblem[str, str]):
        self.status = status
        self.type = type
        self.title = title
        self.detail = detail
        self.user_message = user_message
        self.timestamp = timestamp
        self.objects = objects
