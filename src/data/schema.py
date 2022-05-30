import pydash

from validator.utils import Path


class SchemaData:
    value: dict

    def __init__(self, value: dict):
        self.value = value

    def get(self, key: str):
        return pydash.get(self.value, key)

    def has(self, key: str):
        return pydash.has(self.value, key)

    def merge(self, schema: dict):
        return pydash.merge(self.value, schema)
