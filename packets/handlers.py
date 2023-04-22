import typing
from .filters import Filter
from .base import DatalinkPacket, NetworkPacket
import logging

logger = logging.getLogger("packets")

class Handler:

    def __init__(self,
                 name: str,
                 filters: typing.Tuple[Filter],
                 callback: typing.Optional[typing.Callable]):
        self.name = name
        self.filters = filters
        self.callback = callback

    def process_datalink(self, packet: DatalinkPacket) -> bool:
        for filter in self.filters:
            if filter.layer == 2:
                is_valid = filter.filter(packet)
                if not is_valid:
                    return False
        return True

    def process_network(self, packet: NetworkPacket) -> bool:
        for filter in self.filters:
            if filter.layer == 3:
                is_valid = filter.filter(packet)
                if not is_valid:
                    return False
        return True