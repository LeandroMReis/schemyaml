import pydash

from validator.utils import Path


class ErrorsData:
    __value: dict

    def __init__(self, value: dict):
        self.__value = value

    def value(self):
        return self.__value

    def add(self, path: Path, message: str):
        value = pydash.get(self.__value, path.value)
        if value is None:
            value = message
        elif isinstance(value, str):
            value = [value, message]
        elif isinstance(value, list):
            value.append(message)
        pydash.set_(self.__value, path.value, value)

    def empty(self):
        return pydash.is_empty(self.__value)
