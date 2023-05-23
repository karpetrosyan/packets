import typing

from packets.filters import Filter
from packets.protocols.base import DataLinkPacket
from packets.protocols.base import NetworkPacket
from packets.protocols.base import PacketStack
from packets.protocols.base import ProtocolPacket
from packets.protocols.base import TransportPacket


class Handler:
    def __init__(
        self,
        name: str,
        callback: typing.Optional[typing.Callable[[PacketStack], None]],
        filters: typing.Optional[typing.Iterable[Filter]] = None,
    ):
        if filters is None:
            filters = typing.cast(typing.Iterable[Filter], [])

        self.name = name
        self.filters = filters
        self.callback = callback

    def validate(self, packet: ProtocolPacket) -> bool:
        for filter in self.filters:
            layer = packet.get_layer()
            if layer == 2:
                datalink_filter = filter.datalink_filter
                if datalink_filter is None:
                    continue
                packet = typing.cast(DataLinkPacket, packet)
                is_valid = datalink_filter(packet)
            elif layer == 3:
                network_filter = filter.network_filter
                if network_filter is None:
                    continue
                packet = typing.cast(NetworkPacket, packet)
                is_valid = network_filter(packet)
            elif layer == 4:
                transport_filter = filter.transport_filter
                if transport_filter is None:
                    continue
                packet = typing.cast(TransportPacket, packet)
                is_valid = transport_filter(packet)
            else:
                raise Exception
            if not is_valid:
                return False
        return True

    def handle_success(self, packet_stack: PacketStack):
        self.callback(packet_stack)
