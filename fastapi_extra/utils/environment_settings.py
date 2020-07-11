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
    MONGODB_SERVER: str = None
    MONGODB_USER: str = None
    MONGODB_PASSWORD: str = None

    class Config:
        case_sensitive = True


mongodb_settings = MongodbSettings()
