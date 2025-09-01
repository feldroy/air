from fastapi.exceptions import HTTPException as FASTAPIHTTPException

class HTTPException(FASTAPIHTTPException):
    pass
