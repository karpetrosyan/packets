import typing
from .protocols import Protocol
from .base import Packet

class Filter:

    def __init__(self,
                 filter_functions: typing.List[typing.Callable],
                 layer: typing.Optional[int] = None,
                 proto: typing.Optional[Protocol] = None,
                 callback = None):

        if proto is None and layer is None:
            raise Exception
        if proto and layer:
            raise Exception

        if proto:
            layer = proto.value.layer

        self.filter_functions = filter_functions
        self.callback = callback
        self.layer = layer
        self.proto = proto

        if proto is not None:
            self.filter_functions.insert(0, lambda packet: True)

    def filter(self, packet: Packet) -> bool:
        for function in self.filter_functions:
            is_valid = function(packet)
            if not is_valid:
                return False
        if self.callback:
            self.callback(packet)
        return True