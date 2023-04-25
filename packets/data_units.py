

class DataUnit:

    def __init__(self, data: bytes):
        self.data = data

class Frame(DataUnit):
    ...

class Packet(DataUnit):
    ...

class Segment(DataUnit):
    ...