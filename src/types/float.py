from validator.types.number import NumberType


class FloatType(NumberType):
    def _validate_type(self):
        if not isinstance(self.value(), float):
            self.add_error("The value must be float")
