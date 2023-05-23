from packets.utils import enforce_mac
import struct
from packets.protocols import Protocols
from packets.protocols.ethernet import EthernetPacket
import socket


def test_ethernet_protocol():
    dest_mac = b'\xbb'*6
    src_mac = b'\xaa'*6
    type = Protocols.IPv4.to_bytes(length=2, byteorder='big')
    packet = dest_mac + src_mac + type
    unpacked_dest_mac, unpacked_src_mac, unpacked_type = struct.unpack(EthernetPacket.format,
                packet)
    assert enforce_mac(unpacked_src_mac) == "aa:aa:aa:aa:aa:aa"
    assert enforce_mac(unpacked_dest_mac) == "bb:bb:bb:bb:bb:bb"
    assert socket.ntohs(unpacked_type) == Protocols.IPv4
