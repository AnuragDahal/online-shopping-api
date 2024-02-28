
from fastapi import HTTPException


class ErrorHandler:
    def Error(e):
        raise HTTPException(status_code=400, detail=str(e))

    def NotFound(e):
        raise HTTPException(status_code=404, detail=str(e))

    def Unauthorized(e):
        raise HTTPException(status_code=401, detail=str(e))

    def Forbidden(e):
        raise HTTPException(status_code=403, detail=str(e))

    def ServerError(e):
        raise HTTPException(status_code=500, detail=str(e))

    def Conflict(e):
        raise HTTPException(status_code=409, detail=str(e))
