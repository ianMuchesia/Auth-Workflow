import json
from fastapi import HTTPException, status


class CustomHTTPException(HTTPException):
    def __init__(self, status_code, message):
        super().__init__(status_code=status_code, detail=message)
        self.body = {"message": message}

    def __call__(self, environ, start_response):
        start_response(
            f"{self.status_code} {self.status_phrase}",
            [("Content-Type", "application/json")],
        )
        return [json.dumps(self.body).encode()]
    
    
    

class BadRequestError(CustomHTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)
        
class UnauthorizedError(CustomHTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message)
        
class ForbiddenError(CustomHTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message)
        
class NotFoundError(CustomHTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)
        
class ConflictError(CustomHTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)
