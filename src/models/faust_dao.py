import faust
from typing import Any


class ModelMetadata(faust.Record):
    name: str
    latest_version: int
    server_metadata: Any
    business_metadata: Any


class ModelTask:
    id: int
    model_name: str
    model_version: str
    data: Any
    result: Any
