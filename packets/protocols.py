from .ip import IPPacket
from .icmp import ICMPPacket
from enum import Enum

class Protocol(Enum):
    ip = IPPacket
    icmp = ICMPPacket
