import importlib

import pydash

from validator.data import GlobalData, SchemaData
from validator.exceptions import SchemaException
from validator.utils import Path, Schema


class AbstractType:
    __schema: SchemaData
    __path: Path

    __default_rules = [
        'check_with',
        'conditionals',
        'excludes',
        'required',
        'type',
    ]

    # to override
    _rules: list

    def __init__(self, schema: SchemaData, path: Path):
        self.__schema = schema
        self.__path = path

    def rules(self) -> list:
        return getattr(self, '_rules', [])

    def schema(self) -> SchemaData:
        return self.__schema

    def path(self) -> Path:
        return self.__path

    def value(self, path: Path = None) -> dict:
        return GlobalData.get_document().get(self.path() if path is None else path)

    def add_error(self, message: str, path: Path = None):
        GlobalData.get_errors().add(self.path() if path is None else path, message)

    def validate(self):
        self.__check_conditionals()
        self.__check_allowed_rules()
        if not self.__check_null():
            return
        self.__check_required()
        if self.value() is None:
            return
        self.__check_type()
        self.__check_excludes()
        self.__check_rules()
        self.__check_with()

    def __check_allowed_rules(self):
        schema_rules = pydash.keys(self.schema().value)
        allowed_rules = self.__default_rules + self.rules()
        unknown_rules = pydash.difference(schema_rules, allowed_rules)
        for rule in unknown_rules:
            raise SchemaException('Unknown rule: ' + rule, self.path().value)

    def __check_null(self) -> bool:
        field_exists = pydash.has(GlobalData.get_document().value, self.path().value)
        if self.value() is None and field_exists:
            self.add_error('The value must not be null')
            return False
        return True

    def __check_required(self):
        required = pydash.get(self.schema().value, 'required', False)

        if not required:
            return

        if self.value() is None:
            self.add_error('is required')

    def __check_type(self):
        type_validator = getattr(self, '_validate_type')
        if type_validator is None:
            raise Exception(self.__class__.__name__ + ': Method _validate_type not found')
        type_validator()

    def __check_conditionals(self):
        if not self.schema().has('conditionals'):
            return

        for conditional in self.schema().get('conditionals'):
            if 'when' not in conditional:
                raise SchemaException('Invalid conditional: missing when')

            if 'then' not in conditional:
                raise SchemaException('Invalid conditional: missing then')

            is_valid = True

            conditionals = conditional['when']
            if not isinstance(conditional['when'], list):
                conditionals = [conditionals]

            for _conditional in conditionals:
                field_ref = pydash.get(_conditional, 'field')
                field_path = self.path().parent().get(field_ref)
                field_value = GlobalData.get_document().get(field_path)

                if 'is' in _conditional and field_value != _conditional['is']:
                    is_valid = False
                    break

                if 'in' in _conditional and field_value not in _conditional['in']:
                    is_valid = False
                    break

            if is_valid:
                then = conditional['then']
                conditional_schema = self.schema().merge(then)

    def __check_excludes(self):
        if not self.schema().has('excludes'):
            return

        field_name = self.schema().get('excludes')
        if field_name is True:
            field_name = self.path().current()

        field_path = self.path().parent().add(field_name)
        field_value = GlobalData.get_document().get(field_path)

        if field_value is not None:
            self.add_error('Field not allowed', field_path)

    def __check_with(self):
        if not self.schema().has('check_with'):
            return

        file_name = self.schema().get('check_with')
        module_name = 'validator.schemas.'
        module_name += file_name.replace('/', '.').replace('.py', '')

        module = importlib.import_module(module_name)
        main_method = getattr(module, 'main')
        main_method(self)

    def __check_rules(self):
        for method_name in self.rules():
            rule_validator = getattr(self, '_validate_' + method_name, None)
            if rule_validator is None:
                raise Exception(self.__class__.__name__ + f': Method {method_name} not found')
            rule_validator()

    def _validate_allowed(self):
        if not self.schema().has('allowed'):
            return

        if self.value() not in self.schema().get('allowed'):
            self.add_error(f"The value '{self.value()}' is not allowed")
