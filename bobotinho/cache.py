# -*- coding: utf-8 -*-
import os
import time
from collections import OrderedDict
from threading import RLock
from typing import Any

from redis import Redis


class TTLOrderedDict(OrderedDict):
    def __init__(self) -> None:
        self._lock = RLock()
        super().__init__()

    def _expired(self, key: Any, now: float) -> bool:
        with self._lock:
            expire, _value = super().__getitem__(key)
            return expire and expire < now

    def _purge(self) -> None:
        now = time.time()
        [
            self.__delitem__(key)
            for key in [key for key in list(super().__iter__()) if self._expired(key, now)]
        ]

    def __setitem__(self, key: Any, value: Any) -> None:
        with self._lock:
            expire = None
            super().__setitem__(key, (expire, value))

    def __delitem__(self, key: Any) -> None:
        with self._lock:
            super().__delitem__(key)

    def __getitem__(self, key: Any) -> Any:
        with self._lock:
            now = time.time()
            if self._expired(key, now):
                self.__delitem__(key)
                raise KeyError
            item = super().__getitem__(key)[1]
            return item

    def keys(self, pattern: str = None) -> list:
        with self._lock:
            self._purge()
            return super().keys()

    def set(self, key: Any, value: Any, ex: int = None, nx: bool = None) -> bool:
        if nx and self.get(key):
            return False
        with self._lock:
            self._purge()
            expire = time.time() + ex if ex else None
            super().__setitem__(key, (expire, value))
            return True

    def get(self, key: Any, default: Any = None) -> Any:
        try:
            return self[key]
        except KeyError:
            return default

    def delete(self, key: Any) -> None:
        self.__delitem__(key)

    def close(self) -> None:
        pass


if url := os.getenv("REDIS_URL"):
    cache = Redis.from_url(url, encoding="utf-8", decode_responses=True)
else:
    cache = TTLOrderedDict()
