from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, FastAPI


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        request.state.tenantId = request.headers.get("X-TENANT-ID", None)
        if not request.state.tenantId:
            host = request.headers.get("host", "").split(":")[0]  # type: str
            request.state.tenantId = host

        response = await call_next(request)

        return response


def enable_tenant_middleware(app: FastAPI, with_db=False):
    if with_db:
        from fastapi_extra.middleware.mongoengine.tenant_db_middleware import TenantDBMiddleware
        app.add_middleware(TenantDBMiddleware)
    app.add_middleware(TenantMiddleware)
