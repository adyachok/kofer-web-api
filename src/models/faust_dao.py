from abc import ABC
from enum import Enum

import faust
from typing import Any, Optional

from src.utils.fields import ChoiceField


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


class ModelTask(faust.Record):
    _id: Optional[str]
    model_name: str
    data: dict
    result: Optional[dict]
    # state: State = State.QUEUED
    state: str = ChoiceField(choices=['QUEUED', 'IN_PROGRESS', 'FINISHED',
                                      'ERROR'],
                             default='QUEUED', required=False)
