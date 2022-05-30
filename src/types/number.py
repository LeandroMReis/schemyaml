from validator.types.abstract import AbstractType


class NumberType(AbstractType):
    _rules = [
        'allowed',
        'min',
        'max',
    ]

    def _validate_type(self):
        if not isinstance(self.value(), (int, float)):
            self.add_error("The value must be a number")

    def _validate_min(self):
        if not self.schema().has('min'):
            return

        min_value = self.schema().get('min')
        if self.value() < min_value:
            self.add_error(f'The value must be greater than or equal to {min_value}')

    def _validate_max(self):
        if not self.schema().has('max'):
            return

        max_value = self.schema().get('max')
        if self.value() > max_value:
            self.add_error(f'The value must be less than or equal to {max_value}')
