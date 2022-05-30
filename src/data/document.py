import pydash

from validator.utils import Path


class DocumentData:
    value: dict

    def __init__(self, value: dict):
        self.value = value

    def get(self, path: Path = None) -> dict:
        if path is None:
            return self.value

        return pydash.get(self.value, path.value)
