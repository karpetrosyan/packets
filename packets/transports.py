import typing
import socket

from packets.data_units import Frame
from packets.handlers import Handler
from packets.layers import DataLinkLayer, NetworkLayer, TransportLayer
from packets.protocols.base import PacketStack
from packets.protocols.ipv4 import IPv4Packet
import logging

logger = logging.getLogger("packets")

MAXIMUM_FRAME_SIZE = 1518  # Maximum size of ethernet frame


class Transport:
    def __init__(
        self,
        handlers: typing.Iterable[Handler],
        interface: typing.Optional[str] = None,
    ):
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, 768)
        self.handlers = handlers
        if interface:
            self.socket.bind((interface, 0))

    def serve(self) -> None:
        raise NotImplementedError()

    def receive_frame(self) -> Frame:
        raise NotImplementedError()


class SyncTransport(Transport):
    def serve(self) -> None:
        layers = (
            DataLinkLayer,
            NetworkLayer,
            TransportLayer
        )
        while True:
            invalid_handlers = set()
            stack = PacketStack()
            data_unit = self.receive_frame()
            for layer in layers:
                try:
                    data_unit, packet = layer().decapsulate(data=data_unit, stack=stack)

                    for handler in self.handlers:
                        if handler not in invalid_handlers:
                            is_valid = handler.validate(packet=packet)
                            if not is_valid:
                                invalid_handlers.add(handler)

                    if data_unit.is_empty():
                        break
                except Exception as ex:
                    logger.error(str(ex))
            if not data_unit.is_empty():
                logger.debug(f"Maybe padding {bytes(data_unit.data)}")
                continue

            for handler in self.handlers:
                if handler not in invalid_handlers:
                    handler.handle_success(packet_stack=stack)





    def receive_frame(self) -> Frame:
        frame_buffer = bytearray(MAXIMUM_FRAME_SIZE)
        received = self.socket.recv_into(frame_buffer)
        return Frame(data=memoryview(frame_buffer), end=received)
