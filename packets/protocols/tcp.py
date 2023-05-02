import struct
import socket
from .base import TransportPacket

class TCPPacket(TransportPacket):

    def __init__(self,
                 src_port: int,
                 dest_port: int,
                 sequence: int,
                 acknowledgement: int,
                 data_offset: int,
                 reserved_bits: int,
                 cwr: bool,
                 ece: bool,
                 urg: bool,
                 ack: bool,
                 psh: bool,
                 rst: bool,
                 syn: bool,
                 fin: bool,
                 window_size: int,
                 checksum: int,
                 urgent_pointer: int,
                 data: bytes
                 ):
        self.src_port = src_port
        self.dest_port = dest_port
        self.sequence = sequence
        self.acknowledgement = acknowledgement
        self.data_offset = data_offset
        self.reserved_bits = reserved_bits
        self.cwr = cwr
        self.ece = ece
        self.urg = urg
        self.ack = ack
        self.psh = psh
        self.rst = rst
        self.syn = syn
        self.fin = fin
        self.window_size = window_size
        self.checksum = checksum
        self.urgent_pointer = urgent_pointer
        self.data = data

    def __repr__(self):
        return f"<{self.__class__.__name__} src_port={self.src_port} dest_port={self.dest_port} data={bytes(self.data)}>"

    def __len__(self):
        return struct.calcsize("H H 4s 4s H H H H") + len(self.data)

    @classmethod
    def parse(cls, packet: bytes):
        format = "H H 4s 4s H H H H"
        unpacked = struct.unpack(format, packet[:20])
        (
            src_port,
            dest_port,
            sequence,
            acknowledgement,
            offset_reserved_flags,
            window_size,
            checksum,
            urgent_pointer,
        ) = unpacked
        data_offset = offset_reserved_flags >> 12
        reserved = offset_reserved_flags & 3840
        flags = offset_reserved_flags & 255
        cwr = flags & 0b10000000
        ece = flags & 0b01000000
        urg = flags & 0b00100000
        ack = flags & 0b00010000
        psh = flags & 0b00001000
        rst = flags & 0b00000100
        syn = flags & 0b00000010
        fin = flags & 0b00000001

        data = packet[struct.calcsize(format):]
        obj = cls(
            src_port=socket.htons(src_port),
            dest_port=socket.htons(dest_port),
            sequence=sequence,
            acknowledgement=acknowledgement,
            data_offset=data_offset,
            reserved_bits=reserved,
            cwr = cwr,
            ece = ece,
            urg = urg,
            ack = ack,
            psh = psh,
            rst = rst,
            syn = syn,
            fin = fin,
            window_size=window_size,
            checksum=checksum,
            urgent_pointer=urgent_pointer,
            data=data
        )
        return obj