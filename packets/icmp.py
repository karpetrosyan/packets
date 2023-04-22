import socket
import struct
import typing
from dataclasses import dataclass
from typing_extensions import Self

from .base import NetworkPacket


class ICMPPacket(NetworkPacket):

    @classmethod
    def get_from_packet(cls, icmp_packet: bytes) -> "ICMPPacket":
        icmp_type = icmp_packet[0]
        type_class = ICMP_TYPE_MAP[icmp_type]
        return type_class.parse(packet=icmp_packet)

    @classmethod
    def parse(cls, packet: bytes) -> Self:
        raise NotImplementedError()

@dataclass()
class ICMPEchoReplyPacket(ICMPPacket):
    type: int
    code: int
    checksum: int
    id: int
    seq: int
    data: bytes

    @classmethod
    def parse(cls, packet: bytes) -> Self:
        format = "B B H H H"
        type, code, checksum, id, seq = struct.unpack(format, packet[:struct.calcsize(format)])
        data = packet[struct.calcsize(format):]
        return cls(type=type,
                   code=code,
                   checksum=socket.htons(checksum),
                   id=id,
                   seq=seq,
                   data=data)

class ICMPEchoPacket(ICMPEchoReplyPacket):
    ...

class ICMPReplyPacket(ICMPEchoReplyPacket):
    ...

@dataclass()
class ICMPDestUnreachablePacket(ICMPPacket):
    type: int
    code: int
    checksum: int
    unused: int
    next_hop_MTU: int

    @classmethod
    def parse(cls, packet: bytes) -> Self:
        format = "B B H H H"
        type, code, checksum, unused, next_hop = struct.unpack(format, packet[:struct.calcsize(format)])
        return cls(type=type,
                   code=code,
                   checksum=checksum,
                   unused=unused,
                   next_hop_MTU=next_hop)

ICMP_TYPE_MAP: typing.Dict[int, typing.Type[ICMPPacket]] = {
    8: ICMPEchoPacket,
    3: ICMPDestUnreachablePacket,
    0: ICMPReplyPacket
}