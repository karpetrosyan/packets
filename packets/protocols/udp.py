import struct
import socket
from .base import TransportPacket

class UDPPacket(TransportPacket):

    def __init__(self,
                 src_port: int,
                 dest_port: int,
                 length: int,
                 checksum: int
                 ):
        self.src_port = src_port
        self.dest_port = dest_port
        self.length = length
        self.checksum = checksum

    def __repr__(self):
        return f"<{self.__class__.__name__} src_port={self.src_port} dest_port={self.dest_port}>"

    @classmethod
    def parse(cls, packet: bytes):
        format = "H H H H"
        unpacked = struct.unpack(format, packet[:8])
        (
            src_port,
            dest_port,
            length,
            checksum
        ) = unpacked
        obj = cls(
            src_port=socket.htons(src_port),
            dest_port=socket.htons(dest_port),
            length=length,
            checksum=checksum
        )
        return obj