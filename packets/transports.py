import typing
import socket
from .handlers import Handler
from .data_units import Frame
from .layers import DataLinkLayer, NetworkLayer
from .protocols.base import PacketStack
socket.IPPROTO_ICMP
MAXIMUM_FRAME_SIZE = 1518  # Maximum size of ethernet frame
class Transport:

    def __init__(self,
                 handlers: typing.Iterable[Handler],
                 interface: typing.Optional[str] = None,
                 ):
        self.socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        self.handlers = handlers
        if interface:
            self.socket.bind((interface, 0))

    def serve(self) -> None:
        raise NotImplementedError()

    def receive_frame(self) -> Frame:
        raise NotImplementedError()


class SyncTransport(Transport):

    def serve(self) -> None:
        while True:
                stack = PacketStack()
                frame = self.receive_frame()
                layer = DataLinkLayer()
                packet, datalink_packet = layer.decapsulate(data=frame, stack=stack)
                layer = NetworkLayer()
                segment, network_packet = layer.decapsulate(data=packet, stack=stack)
                print("PACKET")
                print(datalink_packet)
                print(network_packet)
    def receive_frame(self) -> Frame:
        frame_buffer = bytearray(MAXIMUM_FRAME_SIZE)
        self.socket.recv_into(frame_buffer)
        return Frame(data=memoryview(frame_buffer))