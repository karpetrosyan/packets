from typing_extensions import Self

class Packet:

    @property
    def layer(self):
        raise NotImplementedError()

class DatalinkPacket(Packet):
    layer = 2

    @classmethod
    def parse(cls, packet: bytes) -> Self:
        raise NotImplementedError()

class NetworkPacket(Packet):
    layer = 3

    @classmethod
    def parse(cls, packet: bytes) -> Self:
        raise NotImplementedError()
