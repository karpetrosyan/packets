import typing

from .data_units import DataUnit, Frame, Packet, Segment
from .protocols.base import ProtocolPacket, PacketStack
from .protocols.ethernet import EthernetPacket
from .protocols.ipv4 import IPv4Packet
from .protocols.ipv6 import IPv6Packet
from .protocols.arp import ARPPacket
import logging

logger = logging.getLogger("packets")

class Layer:

    def incapsulate(self):
        raise NotImplementedError()

    def decapsulate(self, data: DataUnit, stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        raise NotImplementedError()

    def get_layer(self):
        raise NotImplementedError()

class DataLinkLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self, data: DataUnit, stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        frame = typing.cast(Frame, data)
        ethernet_packet_bytes = frame.data[:14]
        ethernet_packet = EthernetPacket.parse(packet=ethernet_packet_bytes)
        stack.push(ethernet_packet)
        return Packet(data=frame.data[14:]), ethernet_packet

    def get_layer(self):
        return 2

class NetworkLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self, data: DataUnit, stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        protocol_type = stack.datalink_packet.get_type()
        packet = typing.cast(Packet, data)
        if protocol_type == 2048:
            ip_packet_bytes = packet.data[:20]
            ip_packet = IPv4Packet.parse(packet=ip_packet_bytes)
            stack.push(ip_packet)
            return Segment(packet.data[20:]),  ip_packet
        elif protocol_type == 34525:
            ip_packet_bytes = packet.data[:40]
            ip_packet = IPv6Packet.parse(packet=ip_packet_bytes)
            stack.push(ip_packet)
            breakpoint()
            raise Exception
            return Segment(packet.data[40:]), ip_packet
        elif protocol_type == 2054:
            breakpoint()
            arp_packet_bytes = packet.data[:28]
            arp_packet = ARPPacket.parse(packet=arp_packet_bytes)
            breakpoint()
            print(arp_packet)
            raise
        else:
            logger.warning(f"Unsupported protocol type received {protocol_type}")
    def get_layer(self):
        return 3

class TransportLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self, data: DataUnit, stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        return

    def get_layer(self):
        return 4