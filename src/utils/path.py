class Path:
    value: str

    def __init__(self, value: str):
        self.value = value

    def current(self) -> str:
        return self.value.split('.')[-1]

    def add(self, *args: str or int):
        value = self.value
        for arg in args:
            value += arg if value[-1:] == '.' else f'.{arg}'
        return Path(value)

    def get(self, value: str = None):
        if value in [None, '', '.']:
            return self.current()

        path = Path(self.value)
        if '..' in value:
            for i in range(value.count('..')):
                path = path.parent()
            value = value.replace('..', '')
        return path.add(value)

    def parent(self):
        return Path(self.value.rsplit('.', 1)[0])
