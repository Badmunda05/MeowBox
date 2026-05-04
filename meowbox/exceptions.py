class MeowBoxException(Exception):
    pass

class RateLimitError(MeowBoxException):
    def __init__(self, retry_after: int = 60):
        self.retry_after = retry_after
        super().__init__(f"Rate limit hit. Retry after {retry_after} seconds.")

class UploadError(MeowBoxException):
    pass

class DeleteError(MeowBoxException):
    pass
