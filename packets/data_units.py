class DataUnit:
    def __init__(self, data: memoryview, end: int, start: int = 0):
        self._data = data
        self.start = start
        self.end = end

    @property
    def data(self):
        return self._data[self.start : self.end]

    def is_empty(self) -> bool:
        return bytes(self.data) == b''

class Frame(DataUnit):
    ...


class Packet(DataUnit):
    ...


class Segment(DataUnit):
    ...
