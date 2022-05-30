from .document import DocumentData
from .erros import ErrorsData
# from .schema import SchemaData


class __GlobalData:
    # __schema: SchemaData
    __document: DocumentData
    __errors: ErrorsData

    def __init__(self):
        self.__errors = ErrorsData({})

    # def set_schema(self, value: dict):
    #     self.__schema = SchemaData(value)

    # def get_schema(self) -> SchemaData:
    #     return self.__schema

    def set_document(self, value: dict):
        self.__document = DocumentData(value)

    def get_document(self) -> DocumentData:
        return self.__document

    def get_errors(self) -> ErrorsData:
        return self.__errors


data = __GlobalData()
