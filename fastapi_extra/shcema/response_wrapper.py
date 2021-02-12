from typing import Any

from pydantic import BaseModel


class ResponseWrapper(BaseModel):
    result: Any = None
    messages: Any = None
    error: Any = None
