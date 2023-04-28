import typing
import socket

from packets.data_units import Frame
from packets.handlers import Handler
from packets.layers import DataLinkLayer, NetworkLayer, TransportLayer
from packets.protocols.base import PacketStack
from packets.protocols.ipv4 import IPv4Packet

MAXIMUM_FRAME_SIZE = 1518  # Maximum size of ethernet frame


class Transport:
    def __init__(
        self,
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
            datalink_layer = DataLinkLayer()
            (packet, datalink_packet) = datalink_layer.decapsulate(
                data=frame, stack=stack
            )
            network_layer = NetworkLayer()
            (segment, network_packet) = network_layer.decapsulate(
                data=packet, stack=stack
            )

            print("PACKET")
            print(datalink_packet)
            print(network_packet)
            if isinstance(network_packet, IPv4Packet):
                if network_packet.icmp:
                    print(network_packet.icmp)
                    # print(bytes(network_packet.icmp.data))
            network_proto = stack.network_packet.get_proto()
            if network_proto is None:
                continue
            if network_proto == 6:
                transport_layer = TransportLayer()
                (_, transport_packet) = transport_layer.decapsulate(data=segment, stack=stack)
                print(transport_packet)

    def receive_frame(self) -> Frame:
        frame_buffer = bytearray(MAXIMUM_FRAME_SIZE)
        received = self.socket.recv_into(frame_buffer)
        return Frame(data=memoryview(frame_buffer), end=received)
