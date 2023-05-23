import struct

from .base import NetworkPacket
from ..utils import enforce_ipv4
from ..utils import enforce_mac


class ARPPacket(NetworkPacket):
    format = "H H B B H 6s 4s 6s 4s"

    def __init__(
        self,
        hardware_type: int,
        protocol_type: int,
        hardware_length: int,
        protocol_length: int,
        operation: int,
        sender_hardware_address: str,
        sender_protocol_address: str,
        target_hardware_address: str,
        target_protocol_address: str,
    ):
        self.hardware_type = hardware_type
        self.protocol_type = protocol_type
        self.hardware_length = hardware_length
        self.protocol_length = protocol_length
        self.operation = operation
        self.sender_hardware_address = sender_hardware_address
        self.sender_protocol_address = sender_protocol_address
        self.target_hardware_address = target_hardware_address
        self.target_protocol_address = target_protocol_address

    def __repr__(self):
        return f"<ARPPacket src_addr={self.sender_protocol_address} target_addr={self.target_protocol_address}"

    def get_proto(self):
        return None

    def __len__(self):
        return struct.calcsize(self.format)

    @classmethod
    def parse(cls, packet: bytes):
        (
            hardware_type,
            protocol_type,
            hardware_length,
            protocol_length,
            operation,
            sender_hardware_address,
            sender_protocol_address,
            target_hardware_address,
            target_protocol_address,
        ) = struct.unpack(cls.format, packet[:28])
        return cls(
            hardware_type=hardware_type,
            protocol_type=protocol_type,
            hardware_length=hardware_length,
            protocol_length=protocol_length,
            operation=operation,
            sender_hardware_address=enforce_mac(sender_hardware_address),
            sender_protocol_address=enforce_ipv4(sender_protocol_address),
            target_hardware_address=enforce_mac(target_hardware_address),
            target_protocol_address=enforce_ipv4(target_protocol_address),
        )
