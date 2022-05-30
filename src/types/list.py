from validator.data import SchemaData
from validator.types import Type
from validator.types.abstract_list_map import AbstractListMapType


class ListType(AbstractListMapType):
    _rules = [
        'import',
        'schema',
    ]

    def _validate_type(self):
        if not isinstance(self.value(), list):
            self.add_error("The value must be a list")
            return

    def _validate_schema(self):
        for index, _value in enumerate(self.value()):
            schema = self.sub_schema()
            type_name = schema['type'] if 'type' in schema else 'any'
            type_class = Type.get_class(type_name)
            type_validator = type_class(SchemaData(schema), self.path().add(index))
            type_validator.validate()
