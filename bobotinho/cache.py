# -*- coding: utf-8 -*-
from collections import OrderedDict
from threading import RLock
from time import time
from typing import Union

from redis import Redis


class TTLOrderedDict(OrderedDict):
    def __init__(self) -> None:
        self._lock = RLock()
        super().__init__()

    def _expired(self, key: str, now: float) -> bool:
        with self._lock:
            expire = super().__getitem__(key)[0]
            return expire and expire < now

    def _purge(self) -> None:
        now = time()
        for key in (key for key in list(super().__iter__()) if self._expired(key, now)):
            self.__delitem__(key)

    def __setitem__(self, key: str, value: str) -> None:
        with self._lock:
            expire = None
            super().__setitem__(key, (expire, value))

    def __delitem__(self, key: str) -> None:
        with self._lock:
            super().__delitem__(key)

    def __getitem__(self, key: str) -> str:
        with self._lock:
            now = time()
            if self._expired(key, now):
                self.__delitem__(key)
                raise KeyError
            return super().__getitem__(key)[1]

    def keys(self, pattern: str = None) -> list:
        with self._lock:
            self._purge()
            return super().keys()

    def set(self, key: str, value: str, ex: int = None, nx: bool = None) -> bool:
        if nx and self.get(key):
            return False
        with self._lock:
            self._purge()
            expire = time() + ex if ex else None
            super().__setitem__(key, (expire, value))
            return True

    def get(self, key: str, default: str = None) -> str:
        try:
            return self[key]
        except KeyError:
            return default

    def getset(self, key: str, value: str) -> str:
        current_value = self.get(key)
        self.set(key, value)
        return current_value

    def delete(self, key: str) -> None:
        self.__delitem__(key)

    def close(self) -> None:
        pass


class Cache(TTLOrderedDict):
    def __new__(cls, *, redis_url: str = None) -> Union[Redis, TTLOrderedDict]:
        if redis_url:
            return Redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
        return TTLOrderedDict()
