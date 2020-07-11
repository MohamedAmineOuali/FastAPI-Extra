import mongoengine
from mongoengine import connect

from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request

from fastapi_extra.utils import mongodb_settings

_tenant_db_ctx_var: ContextVar = ContextVar("request_context_db", default=None)
_tenant_collections_ctx_var: ContextVar = ContextVar("request_context_collections", default=None)

old_get_db = mongoengine.connection.get_db


def patch():
    def new_get_db(alias=mongoengine.DEFAULT_CONNECTION_NAME, reconnect=False):
        # return old_get_db(alias,reconnect)
        return _tenant_db_ctx_var.get()

    mongoengine.connection.get_db = new_get_db

    # old__get_collection = mongoengine.Document._get_collection.__func__

    @classmethod
    def new__get_collection(cls):
        collections = _tenant_collections_ctx_var.get()
        collection = collections.get(cls, None)

        if not collection:
            # Get the collection, either capped or regular.
            if cls._meta.get("max_size") or cls._meta.get("max_documents"):
                collection = collections[cls] = cls._get_capped_collection()
            else:
                db = cls._get_db()
                collection_name = cls._get_collection_name()
                collection = collections[cls] = db[collection_name]

            # Ensure indexes on the collection unless auto_create_index was
            # set to False.
            # Also there is no need to ensure indexes on slave.
            db = cls._get_db()
            if cls._meta.get("auto_create_index", True) and db.client.is_primary:
                cls.ensure_indexes()

        return collection



        return collection

    mongoengine.Document._get_collection = new__get_collection


patch()


class TenantDBMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ):
        tenant_info = request.state.tenant_info = {
            "db_alias": request.state.tenantId,
            "db_Name": request.state.tenantId.replace(".", "_")
        }
        connect(tenant_info['db_Name'], host=mongodb_settings.MONGODB_SERVER,
                username=mongodb_settings.MONGODB_USER,
                password=mongodb_settings.MONGODB_PASSWORD, authentication_source='admin',
                alias=tenant_info['db_alias'])
        tenant_db = old_get_db(tenant_info['db_alias'])
        old_db_ctx_token = _tenant_db_ctx_var.set(tenant_db)
        old_collections_ctx_token = _tenant_collections_ctx_var.set({})

        response = await call_next(request)

        _tenant_db_ctx_var.reset(old_db_ctx_token)
        _tenant_collections_ctx_var.reset(old_collections_ctx_token)

        return response
