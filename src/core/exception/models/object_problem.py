class ObjectProblem:
    def __init__(self, name: str, user_message: str):
        self.name = name
        self.user_message = user_message

    def to_dict(self):
        return {
            "name": self.name,
            "userMessage": self.user_message
        }