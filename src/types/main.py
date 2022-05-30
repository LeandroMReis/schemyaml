import importlib

from validator.exceptions import SchemaException


class Type:
    types = [
        'any',
        'boolean',
        'float',
        'integer',
        'list',
        'map',
        'number',
        'string',
    ]

    @staticmethod
    def get_class(type_name: str):
        if type_name not in Type.types:
            raise SchemaException(f'{type_name} is not a valid type')

        module = importlib.import_module('validator.types.' + type_name)
        class_name = type_name.title() + 'Type'
        return getattr(module, class_name)
