import typing

from packets.filters import Filter
from packets.protocols.base import ProtocolPacket


class Handler:

    def __init__(self,
                 name: str,
                 filters: typing.Optional[typing.Iterable[Filter]] = None,
                 callback: typing.Optional[
                     typing.Callable[[typing.Dict], None]] = None):
        if filters is None:
           filters = typing.cast(typing.Iterable[Filter], [])

        self.name = name
        self.filters = filters
        self.callback = callback

    def validate(self, packet: ProtocolPacket) -> bool:
        for filter in self.filters:
            for filter_function in filter.filter_functions:
                is_valid = filter_function(packet)
                if not is_valid:
                    return False
        return True

    def handle_success(self):
        if self.callback:
            self.callback()
