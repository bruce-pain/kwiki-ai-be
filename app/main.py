import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError
from starlette.middleware.sessions import SessionMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.utils.logger import logger
from app.utils.limiter import limiter
from app.api.v1 import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Kwiki AI API",
    description="FastAPI backend for Kwiki AI",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
    openapi_url="/v1/openapi.json",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)


@app.get("/", tags=["Home"])
@limiter.limit("5/minute")
async def get_root(request: Request) -> dict:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"URL": "", "message": "Welcome to the Kwiki AI API"},
    )


@app.get("/probe", tags=["Home"])
async def probe():
    return {"message": "I am the Kwiki AI API responding"}


# REGISTER EXCEPTION HANDLERS
@app.exception_handler(HTTPException)
async def http_exception(request: Request, exc: HTTPException):
    """HTTP exception handler"""

    logger.error(f"HTTP Exception occured; {exc}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception(request: Request, exc: RequestValidationError):
    """Validation exception handler"""

    errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]

    logger.error(f"Validation Exception occured; {errors}")

    return JSONResponse(
        status_code=422,
        content={
            "status": False,
            "status_code": 422,
            "message": "Invalid input",
            "errors": errors,
        },
    )


@app.exception_handler(IntegrityError)
async def integrity_exception(request: Request, exc: IntegrityError):
    """Integrity error exception handlers"""

    logger.error(f"Integrity Exception occured; {exc}")

    return JSONResponse(
        status_code=400,
        content={
            "status": False,
            "status_code": 400,
            "message": f"An unexpected error occurred: {exc}",
        },
    )


@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    """Other exception handlers"""

    logger.error(f"Exception occured; {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "status": False,
            "status_code": 500,
            "message": f"An unexpected error occurred: {exc}",
        },
    )


@app.exception_handler(RateLimitExceeded)
async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
    """Rate limit exceeded exception handler"""

    logger.error(f"Rate limit exceeded! {exc}")

    return JSONResponse(
        status_code=429,
        content={
            "status": False,
            "status_code": exc.status_code,
            "message": "Too many requests. Please try again in 60 seconds.",
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=7001,
        reload=True,
        workers=4,
    )
