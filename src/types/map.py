import pydash

from validator.data import SchemaData
from validator.types import Type
from validator.types.abstract_list_map import AbstractListMapType


class MapType(AbstractListMapType):
    _rules = [
        'import',
        'schema',
        'unknowns',
    ]

    def _validate_type(self):
        if not isinstance(self.value(), dict):
            self.add_error('The value must be a map')
            return

    def _validate_schema(self):
        for field_name, schema in self.sub_schema().items():
            type_name = schema['type'] if 'type' in schema else 'any'
            type_class = Type.get_class(type_name)
            type_validator = type_class(SchemaData(schema), self.path().add(field_name))
            type_validator.validate()

    def _validate_unknowns(self):
        fields = pydash.difference(pydash.keys(self.value()), pydash.keys(self.sub_schema()))
        for field_name in fields:
            self.add_error('Is not a valid field', self.path().add(field_name))
