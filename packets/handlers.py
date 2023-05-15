import typing
import warnings

from packets.filters import Filter
from packets.protocols.base import ProtocolPacket
from packets.protocols.base import PacketStack
from packets.protocols.base import DataLinkPacket
from packets.protocols.base import NetworkPacket
from packets.protocols.base import TransportPacket

class Handler:
    def __init__(
        self,
        name: str,
        filters: typing.Optional[typing.Iterable[Filter]] = None,
        callback: typing.Optional[typing.Callable[[PacketStack], None]] = None,
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
                filter_function = filter.datalink_filter
                if filter_function is None:
                    continue
                packet = typing.cast(DataLinkPacket, packet)
                is_valid = filter_function(packet)
            elif layer == 3:
                filter_function = filter.network_filter
                if filter_function is None:
                    continue
                packet = typing.cast(NetworkPacket, packet)
                is_valid = filter_function(packet)
            elif layer == 4:
                filter_function = filter.transport_filter
                if filter_function is None:
                    continue
                is_valid = filter_function(packet)
                packet = typing.cast(TransportPacket, packet)
            else:
                raise Exception
            if not is_valid:
                return False
        return True

    def handle_success(self, packet_stack: PacketStack):
        if self.callback:
            self.callback(packet_stack)
        else:
            warnings.warn(message="Callback is not defined for the handler instance", category=RuntimeWarning)
