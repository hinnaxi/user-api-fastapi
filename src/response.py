from typing import Optional, Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import status


class ApiResponse:
    @staticmethod
    def success(status_code: status, message: Optional[str] = None, data: Optional[Any] = None):
        resp = {
            "status": status_code,
            "success": True,
            "message": message if message is not None else "",
            "data": data if data is not None else []
        }

        return JSONResponse(status_code=status_code, content=jsonable_encoder(resp))

    @staticmethod
    def error(status_code: status, message: Optional[str] = None, error: Optional[Any] = None):
        resp = {
            "status": status_code,
            "success": False,
            "message": message if message is not None else "",
            "error": error if error is not None else []
        }

        return JSONResponse(status_code=status_code, content=jsonable_encoder(resp))
