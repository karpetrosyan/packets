import typing


class DataUnit:
    def __init__(self, data: memoryview, end: typing.Optional[int], start: int = 0):
        self._data = data
        self.start = start
        self.end = end

    @property
    def data(self):
        if self.end is not None:
            return self._data[self.start : self.end]
        else:
            return self._data[self.start :]

    def is_empty(self) -> bool:
        return bytes(self.data) == b''
