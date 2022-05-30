import pydash

from validator.data import SchemaData
from validator.exceptions import SchemaException
from validator.types.abstract import AbstractType
from validator.utils import Path, Schema


class AbstractListMapType(AbstractType):
    __sub_schema: dict

    def __init__(self, schema: SchemaData, path: Path):
        super().__init__(schema, path)
        self.__sub_schema = {}

    def _validate_import(self):
        if not self.schema().has('import'):
            return

        file_name = self.schema().get('import')
        self.__sub_schema = Schema.get(file_name)

    def sub_schema(self) -> dict:
        if not self.schema().has('schema'):
            raise SchemaException('No schema found')

        schema = self.schema().get('schema')

        if isinstance(schema, dict):
            return schema

        if not isinstance(schema, str):
            raise SchemaException('Invalid schema')

        return pydash.merge(Schema.get(schema), self.__sub_schema)
