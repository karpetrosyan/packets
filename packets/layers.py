import logging
import typing

from packets.data_units import DataUnit, Frame, Packet, Segment
from packets.protocols.arp import ARPPacket
from packets.protocols.base import PacketStack, ProtocolPacket
from packets.protocols.ethernet import EthernetPacket
from packets.protocols.icmp import ICMPEchoPacket, ICMPPacket, ICMPReplyPacket
from packets.protocols.ipv4 import IPv4Packet
from packets.protocols.ipv6 import IPv6Packet

logger = logging.getLogger("packets")

class Layer:

    def incapsulate(self):
        raise NotImplementedError()

    def decapsulate(self, data: DataUnit,
                    stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        raise NotImplementedError()

    def get_layer(self):
        raise NotImplementedError()

class DataLinkLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self, data: DataUnit,
                    stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        frame = typing.cast(Frame, data)
        ethernet_packet_bytes = frame.data[:14]
        ethernet_packet = EthernetPacket.parse(packet=ethernet_packet_bytes)
        stack.push(ethernet_packet)
        return Packet(data=frame.data[14:], end=data.end), ethernet_packet

    def get_layer(self):
        return 2

class NetworkLayer(Layer):

    def incapsulate(self):
        ...

    def _decapsulate_arp(self, packet: Packet,
                         stack: PacketStack) -> typing.Tuple[Segment, ProtocolPacket]:
        arp_packet_bytes = packet.data[:28]
        arp_packet = ARPPacket.parse(packet=arp_packet_bytes)
        stack.push(arp_packet)
        return Segment(packet.data[:28], end=packet.end), arp_packet

    def _decapsulate_icmp(self, packet: bytes) -> ICMPPacket:
        icmp_packet_bytes = packet[:4]
        icmp_packet = ICMPPacket.parse(packet=icmp_packet_bytes)
        if icmp_packet.type == 8:
            return ICMPEchoPacket.parse(packet=packet)
        elif icmp_packet.type == 0:
            return ICMPReplyPacket.parse(packet=packet)
        else:
            logger.warning(f"Invalid icmp packet {icmp_packet.type}")
            raise Exception

    def _decapsulate_ipv4(self, packet: Packet,
                          stack: PacketStack) -> typing.Tuple[Segment, ProtocolPacket]:
        ip_packet = IPv4Packet.parse(packet=packet.data)
        stack.push(ip_packet)
        if ip_packet.protocol == 1:
            icmp = self._decapsulate_icmp(packet=ip_packet.data)
            ip_packet.icmp = icmp
        return Segment(packet.data[20:], end=packet.end), ip_packet

    def _decapsulate_ipv6(self,
                          packet: Packet,
                          stack: PacketStack
                          ) -> typing.Tuple[Segment,ProtocolPacket, ProtocolPacket]:
        ip_packet_bytes = packet.data[:40]
        ip_packet = IPv6Packet.parse(packet=ip_packet_bytes)
        stack.push(ip_packet)
        return Segment(packet.data[40:], end=packet.end), ip_packet

    def decapsulate(self, data: DataUnit,
                    stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        assert stack.datalink_packet
        protocol_type = stack.datalink_packet.get_type()
        packet = typing.cast(Packet, data)
        if protocol_type == 2048:
            return self._decapsulate_ipv4(packet=packet, stack=stack)
        elif protocol_type == 34525:
            return self._decapsulate_ipv6(packet=packet, stack=stack)
        elif protocol_type == 2054:
            return self._decapsulate_arp(packet=packet, stack=stack)
        else:
            logger.warning(f"Unsupported protocol type received {protocol_type}")
            raise Exception
    def get_layer(self):
        return 3

class TransportLayer(Layer):

    def incapsulate(self):
        ...

    def decapsulate(self, data: DataUnit,
                    stack: PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        return  # type: ignore

    def get_layer(self):
        return 4
