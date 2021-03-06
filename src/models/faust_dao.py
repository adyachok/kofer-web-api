from abc import ABC
from enum import Enum

import faust
from typing import Any, Optional, List

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


class CalculationItem(faust.Record, serializer='json'):
    name: str
    unit_step: str
    type: str = ChoiceField(choices=['float', 'int', 'str', 'array', 'byte'],
                            default='str')
    value: Any


class ModelTask(faust.Record, serializer='json'):
    _id: Optional[str]
    model_name: str
    data: List[CalculationItem]
    result: Optional[List[Any]]
    # state: State = State.QUEUED
    state: str = ChoiceField(choices=['QUEUED', 'IN_PROGRESS', 'FINISHED',
                                      'ERROR'],
                             default='QUEUED', required=False)
    runner_id: Optional[str] = ''
    execution_state: Optional[int] = 0

    def _prepare_dict(self, data):
        # Remove keys with None values from payload.
        prepared_dict = {}
        for k, v in data.items():
            if isinstance(v, list) and len(v):
                if isinstance(v[0], CalculationItem):
                    v = [item.asdict() for item in v]
            prepared_dict[k] = v
        return prepared_dict


class RunnerFile(faust.Record):
    code: str
    commiter: str
    revision: int
    commit_hash: str
    createdAt: str
    updatedAt: str


class Runner(faust.Record):
    _id: Optional[str]
    name: str
    description: str
    department: str
    current_revision: int
    file: RunnerFile
    createdAt: str
    updatedAt: str

    def _prepare_dict(self, data):
        prepared_dict = {}
        for k, v in data.items():
            if isinstance(v, RunnerFile):
                v = v.asdict()
            prepared_dict[k] = v
        return prepared_dict


class ModelTaskDoEvent(faust.Record):
    task: ModelTask
    runner_code: Optional[str] = ''


class ModelTaskDoEvent(faust.Record):
    task: ModelTask
    runner_code: Optional[str] = ''
