import typing

from packets.protocols.base import ProtocolPacket


class Filter:
    def __init__(
        self,
        name: str,
        filter_functions: typing.Iterable[typing.Callable[[ProtocolPacket], bool]],
        packets: typing.Optional[typing.Container[typing.Type[ProtocolPacket]]],
    ):
        if packets is None:
            packets = typing.cast(
                typing.Container[typing.Type[ProtocolPacket]], [ProtocolPacket]
            )

        self.name = name
        self.filter_functions = filter_functions
        self.packets = packets
