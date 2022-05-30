from validator.types.number import NumberType


class IntegerType(NumberType):
    def _validate_type(self):
        if not isinstance(self.value(), int):
            self.add_error("The value must be integer")
