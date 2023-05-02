import socket
import struct

from ..utils import enforce_mac_address
from .base import DataLinkPacket


class EthernetPacket(DataLinkPacket):
    def __init__(self, src_addr: str, dest_addr: str, type: int):
        self.src_addr = src_addr
        self.dest_addr = dest_addr
        self.type = type

    def get_type(self):
        return self.type

    def __repr__(self):
        return (
            f"<EthernetPacket src_addr={self.src_addr}"
            f" dest_addr={self.dest_addr} type={self.type}>"
        )

    def __len__(self):
        return 14

    @classmethod
    def parse(cls, packet: bytes):
        ethernet_frame = packet[:14]
        format = "6s 6s H"
        src_addr, dest_addr, type = struct.unpack(format, ethernet_frame)
        return cls(
            src_addr=enforce_mac_address(src_addr),
            dest_addr=enforce_mac_address(dest_addr),
            type=socket.htons(type),
        )
