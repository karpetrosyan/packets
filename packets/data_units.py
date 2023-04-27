class DataUnit:

    def __init__(self, data: memoryview, pointer: int = 0):
        self._data = data
        self.pointer = pointer

    @property
    def data(self):
        return self._data[self.pointer:]

class Frame(DataUnit):
    ...

class Packet(DataUnit):
    ...

class Segment(DataUnit):
    ...
