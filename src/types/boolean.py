from validator.types.abstract import AbstractType


class BooleanType(AbstractType):
    def _validate_type(self):
        if not isinstance(self.value(), bool):
            self.add_error("The value must be boolean")
