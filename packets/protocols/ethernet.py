import socket
import struct

from ..models import enforce_mac_address


class EthernetPacket:
    def __init__(self,
                 src_addr: str,
                 dest_addr: str,
                 type: int):
        self.src_addr = src_addr
        self.dest_addr = dest_addr
        self.type = type

    @classmethod
    def parse(cls, packet: bytes):
        ethernet_frame = packet[:14]
        format = "6s 6s H"
        src_addr, dest_addr, type = struct.unpack(format, ethernet_frame)
        return cls(
            src_addr=enforce_mac_address(src_addr),
            dest_addr=enforce_mac_address(dest_addr),
            type=socket.htons(type)
        )
