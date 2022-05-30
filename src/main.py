from validator.data import GlobalData
from validator.data import SchemaData
from validator.types import Type
from validator.utils import Path


class Validator:
    __schema: SchemaData

    def set_schema(self, value: dict):
        self.__schema = SchemaData({
            'required': True,
            'type': 'map',
            'schema': value
        })

    @staticmethod
    def set_document(value: dict):
        GlobalData.set_document(value)

    @staticmethod
    def has_errors():
        return GlobalData.get_errors().empty() is False

    @staticmethod
    def get_errors():
        return GlobalData.get_errors().value()

    def validate(self):
        type_class = Type.get_class(self.__schema.get('type'))
        type_validator = type_class(self.__schema, Path('.'))
        type_validator.validate()
