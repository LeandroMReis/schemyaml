import os

from yaml import safe_load

from config import Config
from validator.exceptions import SchemaException


class Schema:
    @staticmethod
    def get(path: str):
        file_name = Config.SCHEMA_CONFIG_PATH + path

        if not os.path.isfile(file_name):
            raise SchemaException('Schema file not found: ' + file_name)

        schema_raw = open(file_name, 'r')
        return safe_load(schema_raw)
