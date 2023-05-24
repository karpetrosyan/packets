import logging
import typing

from packets.data_units import DataUnit 
from packets.protocols.arp import ARPPacket
from packets.protocols.base import PacketStack, ProtocolPacket
from packets.protocols.ethernet import EthernetPacket
from packets.protocols.icmp import ICMPEchoPacket, ICMPPacket, ICMPReplyPacket
from packets.protocols.ipv4 import IPv4Packet
from packets.protocols.ipv6 import IPv6Packet
from packets.protocols.tcp import TCPPacket
from packets.protocols.udp import UDPPacket
from packets.protocols import Protocols

logger = logging.getLogger("packets")


class Layer:

    def decapsulate(
        self, data: DataUnit, stack: PacketStack
    ) -> typing.Tuple[DataUnit, ProtocolPacket]:
        raise NotImplementedError()

    def get_layer(self):
        raise NotImplementedError()


class DataLinkLayer(Layer):

    def decapsulate(
        self, data: DataUnit, stack: PacketStack
    ) -> typing.Tuple[DataUnit, ProtocolPacket]:
        # TODO: Check whatever protocol is Ethernet or not
        frame = typing.cast(DataUnit, data)
        ethernet_packet_bytes = frame.data[:14]
        ethernet_packet = EthernetPacket.parse(packet=ethernet_packet_bytes)
        stack.push(ethernet_packet)
        return DataUnit(data=frame.data[14:], end=data.end), ethernet_packet

    def get_layer(self):
        return 2


class NetworkLayer(Layer):

    def _decapsulate_arp(
        self, packet: DataUnit, stack: PacketStack
    ) -> typing.Tuple[DataUnit, ProtocolPacket]:
        arp_packet = ARPPacket.parse(packet=packet.data)
        stack.push(arp_packet)
        return DataUnit(packet.data[28:], end=packet.end), arp_packet

    def _decapsulate_icmp(self, packet: bytes) -> ICMPPacket:
        icmp_packet_bytes = packet[:4]
        icmp_packet = ICMPPacket.parse(packet=icmp_packet_bytes)
        if icmp_packet.type == 8:
            return ICMPEchoPacket.parse(packet=packet)
        elif icmp_packet.type == 0:
            return ICMPReplyPacket.parse(packet=packet)
        elif icmp_packet.type == 3:
            # TODO: Add support for Unreachable icmp
            return
        else:
            logger.warning(f"Invalid icmp packet {icmp_packet.type}")
            raise Exception

    def _decapsulate_ipv4(
        self, packet: DataUnit, stack: PacketStack
    ) -> typing.Tuple[DataUnit, ProtocolPacket]:
        ip_packet = IPv4Packet.parse(packet=packet.data)
        stack.push(ip_packet)
        return DataUnit(packet.data[20:], end=packet.end), ip_packet

    def _decapsulate_ipv6(
        self, packet: DataUnit, stack: PacketStack
    ) -> typing.Tuple[DataUnit, ProtocolPacket]:
        ip_packet_bytes = packet.data[:40]
        ip_packet = IPv6Packet.parse(packet=ip_packet_bytes)
        stack.push(ip_packet)
        return DataUnit(packet.data[40:], end=packet.end), ip_packet

    def decapsulate(
        self, data: DataUnit, stack: PacketStack
    ) -> typing.Tuple[DataUnit, ProtocolPacket]:
        assert stack.datalink_packet
        protocol_type = stack.datalink_packet.get_type()
        packet = typing.cast(DataUnit, data)
        if protocol_type == Protocols.IPv4:
            segment, ip_packet = self._decapsulate_ipv4(packet=packet, stack=stack)
            ip_packet = typing.cast(IPv4Packet, ip_packet)
            if ip_packet.get_proto() == Protocols.ICMP:
                icmp_packet = self._decapsulate_icmp(packet=segment.data)
                ip_packet.icmp = icmp_packet
                segment = DataUnit(segment.data[len(segment.data):], end=segment.end)
            return segment, ip_packet
        elif protocol_type == Protocols.IPv6:
            return self._decapsulate_ipv6(packet=packet, stack=stack)
        elif protocol_type == Protocols.ARP:
            return self._decapsulate_arp(packet=packet, stack=stack)
        else:
            logger.warning(f"Unsupported protocol type received {protocol_type}")
            raise Exception

    def get_layer(self):
        return 3


class TransportLayer(Layer):

    def _decapsualte_tcp(self, data: DataUnit, stack:PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        segment = typing.cast(DataUnit, data)
        tcp_packet = TCPPacket.parse(packet=segment.data)
        new_segment = DataUnit(data=segment.data[len(segment.data):], end=0)
        stack.push(tcp_packet)
        return new_segment, tcp_packet

    def _decapsualte_udp(self, data: DataUnit, stack:PacketStack) -> typing.Tuple[DataUnit, ProtocolPacket]:
        segment = typing.cast(DataUnit, data)
        udp_packet = UDPPacket.parse(packet=segment.data)
        new_segment = DataUnit(data=segment.data[len(segment.data):], end=0)
        stack.push(udp_packet)
        return new_segment, udp_packet

    def decapsulate(
        self, data: DataUnit, stack: PacketStack
    ) -> typing.Tuple[DataUnit, ProtocolPacket]:
        network_packet = stack.network_packet
        if network_packet.get_proto() == Protocols.TCP:
            return self._decapsualte_tcp(data=data, stack=stack)
        elif network_packet.get_proto() == Protocols.UDP:
            return self._decapsualte_udp(data=data, stack=stack)
        else:
            raise Exception(f"Tcp {network_packet.get_proto()}")

    def get_layer(self):
        return 4
