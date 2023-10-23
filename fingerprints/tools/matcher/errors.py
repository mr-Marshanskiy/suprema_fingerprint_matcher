class MatcherError(Exception):

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return self.message
