import re

from validator.types.abstract import AbstractType


class StringType(AbstractType):
    _rules = [
        'allowed',
        'empty',
        'regex',
    ]

    def _validate_type(self):
        if not isinstance(self.value(), str):
            self.add_error("The value must be string")

    def _validate_empty(self):
        if not self.schema().has('empty'):
            return

        if self.schema().get('empty') is False and len(str(self.value())) == 0:
            self.add_error("The value must not be empty")

    def _validate_regex(self):
        if not self.schema().has('regex'):
            return

        # noinspection PyTypeChecker
        if not re.match(self.schema().get('regex'), self.value()):
            self.add_error("The value does not match regex")
