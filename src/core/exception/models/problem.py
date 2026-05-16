from datetime import datetime
from typing import List

from src.core.exception.models.object_problem import ObjectProblem

class Problem:
    def __init__(
        self,
        status: int,
        type: str,
        title: str,
        detail: str,
        user_message: str,
        timestamp: datetime,
        objects: List[ObjectProblem]
    ):
        self.status = status
        self.type = type
        self.title = title
        self.detail = detail
        self.user_message = user_message
        self.timestamp = timestamp
        self.objects = objects

    def to_dict(self):
        return {
            "status": self.status,
            "type": self.type,
            "title": self.title,
            "detail": self.detail,
            "userMessage": self.user_message,
            "timestamp": self.timestamp.isoformat(),
            "objects": [
                obj.to_dict() if hasattr(obj, "to_dict") else obj
                for obj in self.objects
            ]
        }