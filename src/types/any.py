from validator.types.abstract import AbstractType


class AnyType(AbstractType):
    _rules = [
        'allowed',
    ]

    def _validate_type(self):
        pass
