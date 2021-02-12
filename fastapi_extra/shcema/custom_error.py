from pydantic import BaseModel
from typing import Any


class CustomError(BaseModel):
    code: Any = None
    message: Any = None
