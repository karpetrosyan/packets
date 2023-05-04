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
            stack = PacketStack()
            data_unit = self.receive_frame()
            for layer in layers:
                try:
                    data_unit, packet = layer().decapsulate(data=data_unit, stack=stack)
                    print(packet)

                    if data_unit.is_empty():
                        break
                except Exception as ex:
                    print(ex)
            if not data_unit.is_empty():
                logger.debug(f"Maybe padding {bytes(data_unit.data)}")
                continue
            print("PACKET")
            for packet in stack:
                print(packet)





    def receive_frame(self) -> Frame:
        frame_buffer = bytearray(MAXIMUM_FRAME_SIZE)
        received = self.socket.recv_into(frame_buffer)
        return Frame(data=memoryview(frame_buffer), end=received)
