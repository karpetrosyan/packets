import struct

from ..utils import enforce_ipv6
from .base import NetworkPacket


class IPv6Packet(NetworkPacket):
    def __init__(
        self,
        version: int,
        traffic_class: int,
        flow_label: int,
        payload_length: int,
        next_header: int,
        hop_limit: int,
        src_addr: str,
        dest_addr: str,
    ):
        self.version = version
        self.traffic_class = traffic_class
        self.flow_label = flow_label
        self.payload_length = payload_length
        self.next_header = next_header
        self.hop_limit = hop_limit
        self.src_addr = src_addr
        self.dest_addr = dest_addr

    def __repr__(self):
        return f"<IPv6Packet src_addr={self.src_addr} dest_addr={self.dest_addr}>"

    def get_proto(self):
        return self.next_header

    @classmethod
    def parse(cls, packet: bytes):
        unpacked = struct.unpack("4s H B B 16s 16s", packet)
        (
            version_traffic_flow,
            payload_length,
            next_header,
            hop_limit,
            src_addr,
            dest_addr,
        ) = unpacked
        version = int.from_bytes(version_traffic_flow, "big") >> 28
        traffic_clss = int.from_bytes(version_traffic_flow, "big") & 267386880
        flow_label = int.from_bytes(version_traffic_flow, "big") & 1048575
        obj = cls(
            version=version,
            traffic_class=traffic_clss,
            flow_label=flow_label,
            payload_length=payload_length,
            next_header=next_header,
            hop_limit=hop_limit,
            src_addr=enforce_ipv6(src_addr),
            dest_addr=enforce_ipv6(src_addr),
        )
        return obj
