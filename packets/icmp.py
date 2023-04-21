import socket
import struct
from dataclasses import dataclass
from dataclasses import field


class ICMPPacket:

    @classmethod
    def parse(cls, icmp_packet: bytes) -> "ICMPPacket":
        icmp_type = icmp_packet[0]
        type_class = ICMP_TYPE_MAP[icmp_type]
        return type_class.parse(icmp_packet=icmp_packet)

@dataclass()
class ICMPEchoReplyPacket(ICMPPacket):
    type: int
    code: int
    checksum: int
    id: int
    seq: int
    data: bytes

    @classmethod
    def parse(cls, icmp_packet: bytes) -> "ICMPPacket":
        format = "B B H H H"
        type, code, checksum, id, seq = struct.unpack(format, icmp_packet[:struct.calcsize(format)])
        data = icmp_packet[struct.calcsize(format):]
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
    def parse(cls, icmp_packet: bytes) -> "ICMPPacket":
        format = "B B H H H"
        type, code, checksum, unused, next_hop = struct.unpack(format, icmp_packet[:struct.calcsize(format)])
        return cls(type=type,
                   code=code,
                   checksum=checksum,
                   unused=unused,
                   next_hop_MTU=next_hop)

ICMP_TYPE_MAP = {
    8: ICMPEchoPacket,
    3: ICMPDestUnreachablePacket,
    0: ICMPReplyPacket
}