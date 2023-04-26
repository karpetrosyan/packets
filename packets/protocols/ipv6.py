import socket
import struct
from dataclasses import dataclass

from ..utils import enforce_ipv4
from .base import NetworkPacket

class IPv6Packet(NetworkPacket):

    def __init__(self,
                 version: int,
                 traffic_class: int,
                 flow_label: int,
                 payload_length: int,
                 next_header: int,
                 hop_limit: int,
                 src_addr: str,
                 dest_addr: str):
        self.version = version
        self.traffic_class = traffic_class
        self.flow_label = flow_label
        self.payload_length = payload_length
        self.next_header = next_header
        self.hop_limit = hop_limit
        self.src_addr = src_addr
        self.dest_addr = dest_addr

    @classmethod
    def parse(cls, packet: bytes):
        unpacked = struct.unpack("4s H B B 128s 128s")
        breakpoint()
        print(unpacked)