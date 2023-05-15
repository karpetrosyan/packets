import typing

from packets.protocols.base import DataLinkPacket
from packets.protocols.base import NetworkPacket
from packets.protocols.base import TransportPacket

class Filter:
    def __init__(
            self,
            name: str,
            datalink_filter: typing.Optional[typing.Callable[[DataLinkPacket], bool]] = None,
            network_filter: typing.Optional[typing.Callable[[NetworkPacket], bool]] = None,
            transport_filter: typing.Optional[typing.Callable[[TransportPacket], bool]] = None
    ):
        self.name = name
        self.datalink_filter = datalink_filter
        self.network_filter = network_filter
        self.transport_filter = transport_filter
