from enum import IntEnum

class Protocols(IntEnum):

    # Network Layer
    IPv4 = 2048
    IPv6 = 34525
    ARP = 2054
    ICMP = 1

    # Transport Layer
    TCP = 6
    UDP = 17
