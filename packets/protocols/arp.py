import struct

from .base import NetworkPacket

class ARPPacket(NetworkPacket):

    def __init__(self,
                 hardware_type: int,
                 protocol_type: int,
                 hardware_length: int,
                 protocol_length: int,
                 operation: int,
                 sender_hardware_address: int,
                 sender_protocol_address: int,
                 target_hardware_address: int,
                 target_protocol_address: int
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
        return f"<ARPPacket hardware_type={self.hardware_type}>"

    @classmethod
    def parse(cls, packet: bytes):
        hardware_type, protocol_type, hardware_length, protocol_length, operation, sender_hardware_address, sender_protocol_address, target_hardware_address, target_protocol_address = struct.unpack("H H B B H 6s 4s 6s 4s", packet)
        return cls(hardware_type=hardware_type,
                   protocol_type=protocol_type,
                   hardware_length=hardware_length,
                   protocol_length=protocol_length,
                   operation=operation,
                   sender_hardware_address=sender_hardware_address,
                   sender_protocol_address=sender_protocol_address,
                   target_hardware_address=target_hardware_address,
                   target_protocol_address=target_protocol_address)