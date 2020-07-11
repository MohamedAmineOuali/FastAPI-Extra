from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request


async def patch():
    from uvicorn.protocols.http.httptools_impl import HttpToolsProtocol
    old_on_url = HttpToolsProtocol.on_url

    def new_on_url(self, url):
        old_on_url(self, url)
        self.scope['transport'] = self.transport

    HttpToolsProtocol.on_url = new_on_url


patch()


class MutualTLSMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        certificate = request.scope['transport'].get_extra_info('peercert')

        response = await call_next(request)

        return response