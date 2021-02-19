import os

from pydantic import BaseSettings


class CertificateSettings(BaseSettings):
    PRIVATE_KEY_FILE: str = None
    CERTIFICATE_FILE: str = None
    CA_FILE: str = None


certificateSettings = CertificateSettings()


class HttpClientSettings(BaseSettings):
    AIOHTTP_POOL_SIZE: int = 100
    AIOHTTP_TIMEOUT: int = 86400  # timeout 24h

    AIOHTTP_USE_SSL: bool = False


httpClientSettings = HttpClientSettings()


class MongodbSettings(BaseSettings):
    MONGODB_SERVER: str
    MONGODB_USER: str
    MONGODB_PASSWORD: str

    class Config:
        case_sensitive = True


if os.path.isdir('/secrets'):
    mongodb_settings = MongodbSettings(_secrets_dir="/secrets")
else:
    mongodb_settings = MongodbSettings()
