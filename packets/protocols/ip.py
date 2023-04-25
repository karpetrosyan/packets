import socket
import struct
from dataclasses import dataclass

from .models import enforce_ipv4


class IPPacket:


    def __init__(self,
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
                src_addr: int,
                desc_addr: int,
                data: bytes,):
        self.version = version
        self.ihl = ihl,
        self.type_of_service = type_of_service
        self.length = length
        self.flags = flags
        self.checksum = checksum
        self.fragment_offset = fragment_offset
        self.id = id
        self.ttl = ttl
        self.protocol = protocol
        self.src_addr = src_addr
        self.dest_addr = desc_addr
        self.data = data

    @classmethod
    def parse(cls, ip_packet: bytes):
        version_header_length = ip_packet[0]
        header_length = (version_header_length & 15) * 4
        version_ihl, type_of_service, total_length, id, fragment_offset, ttl, proto, checksum, src, target = struct.unpack('B B H H H B B H 4s 4s', ip_packet[:20])
        data = ip_packet[header_length:]
        src = enforce_ipv4(src)
        target = enforce_ipv4(target)
        version, ihl = version_ihl >> 4, version_ihl & 0xF
        flags = fragment_offset >> 13
        fragment_offset = fragment_offset & 0x1fff
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
            desc_addr=target,
            data=data
        )
        return obj

