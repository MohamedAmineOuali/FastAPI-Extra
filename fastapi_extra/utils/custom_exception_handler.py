from fastapi import FastAPI
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse


async def custom_exception_handler(request, exc):
    response = {}
    response["error"] = {"code": exc.status_code, "message": exc.detail}
    return JSONResponse(content=response, status_code=exc.status_code)


def change_exception_handling(app: FastAPI):
    app.exception_handler(HTTPException)(custom_exception_handler)

