import socket
import struct

from typing_extensions import Self

from .base import NetworkPacket


class ICMPPacket(NetworkPacket):
    def __init__(self, type: int, code: int, checksum: int):
        self.type = type
        self.code = code
        self.checksum = checksum

    def get_proto(self):
        return None

    @classmethod
    def parse(cls, packet: bytes):
        format = "B B H"
        type, code, checksum = struct.unpack(format, packet)
        return cls(type=type, code=code, checksum=socket.htons(checksum))


class ICMPEchoReplyPacket(ICMPPacket):
    def __init__(
        self,
        type: int,
        code: int,
        checksum: int,
        identifier: int,
        sequence: int,
        data: bytes,
    ):
        super().__init__(type=type, code=code, checksum=checksum)
        self.identifier = identifier
        self.sequence = sequence
        self.data = data

    def __repr__(self):
        return (
            f"<{self.__class__.__name__} "
            f"type={self.type} code={self.code} "
            f"checksum={hex(self.checksum)}>"
        )

    @classmethod
    def parse(cls, packet: bytes) -> Self:
        format = "B B H H H"
        (type, code, checksum, id, seq) = struct.unpack(
            format, packet[: struct.calcsize(format)]
        )
        data = packet[struct.calcsize(format) :]
        return cls(
            type=type,
            code=code,
            checksum=socket.htons(checksum),
            identifier=id,
            sequence=seq,
            data=data,
        )

    def __len__(self):
        return 8

class ICMPEchoPacket(ICMPEchoReplyPacket):
    ...


class ICMPReplyPacket(ICMPEchoReplyPacket):
    ...

class ICMPUnreachable(ICMPPacket):
    format = "B B H H H"

    def __init__(
            self,
            type: int,
            code: int,
            checksum: int,
            unused: int,
            next_hop_MTU: int):
        super().__init__(type=type,
                         code=code,
                         checksum=checksum)
        self.unused = unused
        self.next_hop_MTU = next_hop_MTU

    def __len__(self):
        return struct.calcsize(self.format)

    @classmethod
    def parse(cls, packet: bytes):
        (type, code, checksum, unused, next_hop_MTU) = struct.unpack(
            cls.format, packet[: struct.calcsize(cls.format)]
        )
        return cls(
            type=type,
            code=code,
            checksum=socket.htons(checksum),
            unused=unused,
            next_hop_MTU=next_hop_MTU
        )
