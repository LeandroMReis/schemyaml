# class SchemaException:
#     def __init__(self, message):
#         self.message = message
#
#     def __str__(self):
#         return self.message

class SchemaException(Exception):
    pass
    # def __init__(self, message, errors):
    #     super().__init__(message, errors)
    #     self.errors = errors