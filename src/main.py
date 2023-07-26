from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from sqlalchemy.exc import StatementError
from src.config import app_configs, settings
from src.database import Base, db_engine
from src.exceptions import ApiException
from src.response import ApiResponse
from src.router import api_router
from pydantic import Field
from fastapi_pagination import add_pagination
from fastapi_pagination.links import Page

Base.metadata.create_all(bind=db_engine)
Page = Page.with_custom_options(
    size=Field(5, ge=1, le=10)
)

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

app.include_router(api_router, prefix=f"/api/v{settings.APP_VERSION}")


@app.exception_handler(404)
async def not_found_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    return ApiResponse.error(status_code=exc.status_code, message=exc.detail)


@app.exception_handler(500)
async def internal_server_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    msg = "Internal Server Failed"
    data = {
        "code": "INTERNAL_SERVER",
        "detail": exc.args
    }
    return ApiResponse.error(status_code=HTTP_500_INTERNAL_SERVER_ERROR, message=msg, error=data)


@app.exception_handler(ApiException)
async def api_exception_handler(_request: Request, exc: ApiException) -> JSONResponse:
    data = {
        "code": exc.code,
        "detail": exc.errors(),
    }
    return ApiResponse.error(status_code=exc.status_code, message=exc.message, error=data)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    msg = "Data Validation Failed"
    data = {
        "code": "REQUEST_VALIDATION_ERROR",
        "detail": exc.errors(),
    }
    return ApiResponse.error(status_code=HTTP_422_UNPROCESSABLE_ENTITY, message=msg, error=data)


@app.exception_handler(StatementError)
async def sql_alchemy_exception_handler(_request: Request, exc: StatementError) -> JSONResponse:
    data = {
        "code": exc.code,
        "detail": exc.args,
    }
    return ApiResponse.error(status_code=HTTP_400_BAD_REQUEST, error=data)


@app.exception_handler(HTTPException)
async def http_exception_handler(_request: Request, exc: HTTPException) -> JSONResponse:
    data = {
        "code": "HTTPException",
        "detail": exc.detail,
    }
    return ApiResponse.error(status_code=exc.status_code, error=data)


add_pagination(app)
