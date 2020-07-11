import aiohttp
from fastapi import Depends
from pydantic import AnyUrl

from fastapi_extra.utils.aiohttp_client import SingletonAiohttp, SessionClientAiohttp


class BasicServiceClient:
    url: AnyUrl = None

    def __init__(self, httpClient: aiohttp.ClientSession = Depends(SessionClientAiohttp(tenant_forward=True))):
        self.httpClient = httpClient

    async def get(self):
        result = None
        async with self.httpClient.post(self.url) as response:
            print(response.status)
            result = await response.text()

    async def post(self, data):
        result = None
        async with self.httpClient.post(self.url, data) as response:
            print(response.status)
            result = await response.text()

        return result

    async def put(self, data):
        result = None
        async with self.httpClient.put(self.url, data) as response:
            print(response.status)
            result = await response.text()

        return result

    async def delete(self, data):
        result = None
        async with self.httpClient.delete(self.url, data) as response:
            print(response.status)
            result = await response.text()

        return result
