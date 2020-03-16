from abc import ABC
from enum import Enum

import faust
from typing import Any, Optional

from bson import ObjectId
from faust.models import StringField


class ModelMetadata(faust.Record, ABC):
    _id: Optional[str]
    name: str
    latest_version: int
    server_metadata: Any
    business_metadata: Any


class State(Enum):
    QUEUED = 'queued'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    ERROR = 'error'


class ModelTask:
    # _id: str
    model_name: str
    model_version: str
    data: Any
    result: Any
    state: State = State.QUEUED
