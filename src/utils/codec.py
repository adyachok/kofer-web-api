from enum import Enum
from typing import Any

import msgpack
from faust import Record

from faust.serializers import codecs


class enum_raw_msgpack(codecs.Codec):

    def _dumps(self, obj: Any) -> bytes:
        if issubclass(Record, obj):
            obj = obj.asdict()
            for k, v in obj:
                if issubclass(Enum, v.__class__):
                    obj[k] = {"__enum__": str(v)}
        return msgpack.dumps(obj)

    def _loads(self, s: bytes) -> Any:
        return msgpack.loads(s)
