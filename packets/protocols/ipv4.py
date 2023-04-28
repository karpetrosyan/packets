import socket
import struct
import typing

from ..utils import enforce_ipv4
from .base import NetworkPacket
from .icmp import ICMPPacket


class IPv4Packet(NetworkPacket):
    def __init__(
        self,
        version: int,
        ihl: int,
        type_of_service: int,
        length: int,
        flags: int,
        checksum: int,
        fragment_offset: int,
        id: int,
        ttl: int,
        protocol: int,
        src_addr: str,
        dest_addr: str,
        data: bytes,
        icmp: typing.Optional[ICMPPacket] = None,
    ):
        self.version = version
        self.ihl = (ihl,)
        self.type_of_service = type_of_service
        self.length = length
        self.flags = flags
        self.checksum = checksum
        self.fragment_offset = fragment_offset
        self.id = id
        self.ttl = ttl
        self.protocol = protocol
        self.src_addr = src_addr
        self.dest_addr = dest_addr
        self.data = data
        self.icmp = icmp

    def __repr__(self):
        return f"<IPPacket src_addr={self.src_addr} dest_addr={self.dest_addr}>"

    def get_proto(self):
        return self.protocol

    @classmethod
    def parse(cls, packet: bytes):
        version_header_length = packet[0]
        header_length = (version_header_length & 15) * 4
        (
            version_ihl,
            type_of_service,
            total_length,
            id,
            fragment_offset,
            ttl,
            proto,
            checksum,
            src,
            target,
        ) = struct.unpack("B B H H H B B H 4s 4s", packet[:20])
        data = packet[header_length:]
        src = enforce_ipv4(src)
        target = enforce_ipv4(target)
        version, ihl = version_ihl >> 4, version_ihl & 0xF
        flags = fragment_offset >> 13
        fragment_offset = fragment_offset & 0x1FFF
        obj = cls(
            version=version,
            ihl=ihl,
            type_of_service=type_of_service,
            id=id,
            checksum=socket.htons(checksum),
            flags=flags,
            fragment_offset=fragment_offset,
            length=total_length,
            ttl=ttl,
            protocol=proto,
            src_addr=src,
            dest_addr=target,
            data=data,
        )
        return obj
