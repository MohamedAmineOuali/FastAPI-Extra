import json
from starlette.responses import Response
from pydantic import typing

from fastapi_extra.shcema.response_wrapper import ResponseWrapper


class WrapperResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        response = {}
        if not isinstance(content, ResponseWrapper):
            response['result'] = content
        else:
            response = content
        return json.dumps(
            response,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
