import asyncio
from socket import AF_INET

import aiohttp
from fastapi import Depends, Request

from .core.startup_shutdown_events import on_startup, on_shutdown
from .environment_settings import httpClientSettings, certificateSettings

ssl_ctx = None

if httpClientSettings.AIOHTTP_USE_SSL:
    import ssl

    ssl_ctx = ssl.create_default_context(cafile=certificateSettings.CA_FILE)
    ssl_ctx.load_cert_chain(certificateSettings.CERTIFICATE_FILE,
                            certificateSettings.PRIVATE_KEY_FILE)


class SingletonAiohttp:
    sem: asyncio.Semaphore = None
    aiohttp_client: aiohttp.ClientSession = None

    @classmethod
    async def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=httpClientSettings.AIOHTTP_TIMEOUT)

            connector = aiohttp.TCPConnector(family=AF_INET,
                                             limit_per_host=httpClientSettings.AIOHTTP_POOL_SIZE)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls):
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None


class SessionClientAiohttp:
    def __init__(self, enable_ssl=False, tenant_forward=True):
        self.enable_ssl = enable_ssl
        self.tenant_forward = tenant_forward
        self.tenant_id = None
        self.httpClient = None

    def __call__(self, request: Request,
                 httpClient: aiohttp.ClientSession = Depends(SingletonAiohttp.get_aiohttp_client)):
        self.httpClient = httpClient
        self.tenant_id = request.state.tenantId
        if not self.tenant_id:
            self.tenant_forward = False
        return self

    def request(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.request(*args, **kwargs, headers=headers)

    def ws_connect(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.ws_connect(*args, **kwargs, headers=headers)

    def get(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.get(*args, **kwargs, headers=headers)

    def options(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.options(*args, **kwargs, headers=headers)

    def head(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.head(*args, **kwargs, headers=headers)

    def post(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.post(*args, **kwargs, headers=headers)

    def put(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.put(*args, **kwargs, headers=headers)

    def patch(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.patch(*args, **kwargs, headers=headers)

    def delete(self, *args, headers=None, **kwargs):
        if self.enable_ssl and not kwargs['ssl']:
            kwargs['ssl'] = ssl_ctx
        if self.tenant_forward:
            if headers is None:
                headers = {}
            if 'X-TENANT-ID' not in headers:
                headers['X-TENANT-ID'] = self.tenant_id

        return self.httpClient.delete(*args, **kwargs, headers=headers)


@on_startup
async def on_start_up():
    await SingletonAiohttp.get_aiohttp_client()


@on_shutdown
async def on_shutdown():
    await SingletonAiohttp.close_aiohttp_client()
